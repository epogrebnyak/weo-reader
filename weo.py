# Download source:
# curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

LATEST_YEAR = 2024

def convert(x):
    if isinstance(x, str) and "," in x:
        x = x.replace(",","")
    try:
        return float(x)
    except ValueError:
        return np.nan
    
assert convert("9,902.554") == 9902.554

class WEO:
    years = [str(x) for x in range(1980, LATEST_YEAR+1)]
    
    def __init__(self, filename):
        df = pd.read_csv(filename, delimiter="\t", encoding="iso-8859-1")
        ix = df['Country'].isna()
        self.df = df[~ix]
        # attributes
        self.columns = self.df.columns
        country_cols = ['WEO Country Code', 'ISO', 'Country']     
        self.countries_df = self.df[country_cols].drop_duplicates()

    def vars(self):
        return self.df['Subject Descriptor'].unique()                
        
    def by_subject(self, subjects):
        if isinstance(subjects, str):
            subjects = [subjects]            
        ix = self.df['Subject Descriptor'].isin(subjects) 
        return self.df[ix]                   
    
    def units(self, subject=None):
        _df = self.by_subject(subject) if subject else self.df
        return _df['Units'].unique().tolist()        
            
    def get(self, subject: str, unit: str):
        _df = self.by_subject(subject)
        units = _df['Units'].unique()
        if unit not in units:
            raise ValueError(f"Unit must be one of {units}, provided: {unit}")
        cols = self.years + ['ISO']
        _df = _df[_df['Units'] == unit] \
                 [cols] \
                 .set_index('ISO') \
                 .transpose()
        _df.columns.name = ''
        _df.index = pd.date_range(start='1980', 
                                  end=str(LATEST_YEAR+1), 
                                  freq='A')
        return _df.applymap(convert)

    def find(self, country: str):
        """Find country names that include *country* substring, 
           irrespective of lower or upper case."""
        c = country.lower()
        ix = self.countries_df['Country'].apply(lambda x: c in x.lower())
        return self.countries_df[ix]                   
    
    def iso_code(self, country: str):
        """Return ISO code for *country* name."""
        return self.find(country).ISO.iloc[0]    
  
    def gdp_usd(self, year=2018):
        return self.get('Gross domestic product, current prices', 
                        'U.S. dollars') \
                        [str(year)] \
                        .transpose() \
                        .iloc[:,0] \
                        .sort_values(ascending=False)

def plot_axh(df, **kwarg):
  df.plot(**kwarg).axhline(y=0, ls='-', lw=0.5, color='darkgrey')
     
if __name__  == '__main__':    
    w = WEO('weo.csv')
    
    def plot_deficit(subset, source=w):
        _df = source.get('General government net lending/borrowing',
                         'Percent of GDP')[subset]
        plot_axh(_df, title="Чистое кредитование/заимствование, % ВВП")
    
    def plot_debt(subset, source=w):
        _df = source.get('General government gross debt',
                         'Percent of GDP')[subset]
        _df.plot(title="Государственный долг, % ВВП")   
    
    brics = ['BRA', 'IND', 'CHN', 'RUS']
    cri = ['ARG', 'GRC', 'RUS',  ]  # can also include 'ECU', 'MEX'
    oil = ['NOR', 'SAU', 'RUS', 'IRN']
    g3j = ['FRA', 'DEU', 'ITA', 'GBR', 'USA'] # 'ESP', 'KOR'
    
    plot_debt(g3j)
    plot_deficit(g3j)
    
    plot_debt(brics)
    plot_deficit(brics)
    
    plot_debt(cri)
    plot_deficit(cri)

    plot_debt(oil)
    plot_deficit(oil)
    
    plt.figure()    
    w.gdp_usd(2018).head(20).iloc[::-1].plot.barh(title="ВВП, млрд долл. (2018)")