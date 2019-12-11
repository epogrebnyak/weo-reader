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

class WEO:
    """Wrapper for pandas dataframe that holds 
       World Economic Outlook source data as a single table.
       
       Data source correponds to full by-country dataset.
       More inidcators are avialible for country groups. 
       Separate dataset is commodity prices. 
       
       Inspection methods:
           .vars()
           .units()
           .find_countries()
           .iso_code()
       
       Single-variable dataframe:
           .get()     
           
       Presets:
           .gdp_usd()
           .libor_usd()
           
       """
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
        return self.df['Subject Descriptor'].unique().tolist()                
        
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

    def find_countries(self, name: str):
        """Find country names that include *name* as substring, 
           case-insensitive."""
        c = name.lower()
        ix = self.countries_df['Country'].apply(lambda x: c in x.lower())
        return self.countries_df[ix]                   
    
    def iso_code(self, country: str):
        """Return ISO code for *country* name."""
        return self.find_countries(country).ISO.iloc[0]    
  
    def gdp_usd(self, year=2018):
        return self.get('Gross domestic product, current prices', 
                        'U.S. dollars') \
                        [str(year)] \
                        .transpose() \
                        .iloc[:,0] \
                        .sort_values(ascending=False)
                        
    def libor_usd(self):
        return self.get('Six-month London interbank' 
                        ' offered rate (LIBOR)', 'Percent')['USA']

def plot_axh(df, **kwarg):
  df.plot(**kwarg).axhline(y=0, ls='-', lw=0.5, color='darkgrey')
  
  # TODO: indicate data gaps
  #       check identities: CA, deflator, PPP rate, per capita GDPs
  #       savings vs investment
  #       can estimate consumption 
  #       distributions by country slice
  #       attempt timing recesssions 
  #       employment flexibility?
  #       replicate ouptput gap
  #       tiles
  #       use Dabl to visualise - https://amueller.github.io/dabl/dev/index.html
  #       cointegration tests
  #       more commodity data to extract: https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/weoreptc.aspx?sy=1998&ey=2024&scsm=1&ssd=1&sort=country&ds=.&br=1&pr1.x=30&pr1.y=15&c=001%2C110%2C163%2C119%2C123%2C998%2C200%2C505%2C511%2C903%2C205%2C400%2C603&s=NGDP_RPCH%2CNGDP_RPCHMK%2CNGDPD%2CPPPGDP%2CNGDP_D%2CNGDPRPPPPC%2CPPPPC%2CNGAP_NPGDP%2CPPPSH%2CNID_NGDP%2CNGSD_NGDP%2CPCPIPCH%2CPCPIEPCH%2CFLIBOR3%2CTRADEPCH%2CTM_RPCH%2CTMG_RPCH%2CTX_RPCH%2CTXG_RPCH%2CTTPCH%2CTTTPCH%2CTXGM_D%2CTXGM_DPCH%2CLUR%2CLE%2CGGR_NGDP%2CGGX_NGDP%2CGGXCNL_NGDP%2CGGSB_NPGDP%2CGGXONLB_NGDP%2CGGXWDN_NGDP%2CGGXWDG_NGDP%2CBCA%2CBCA_NGDPD%2CBM%2CBX%2CBF%2CBFD%2CBFP%2CBFF%2CBFO%2CBFRA%2CD%2CD_NGDPD%2CD_BX%2CDS%2CDS_NGDPD%2CDS_BX%2CDSI%2CDSI_NGDPD%2CDSI_BX%2CDSP%2CDSP_NGDPD%2CDSP_BX%2CPALLFNFW%2CPNFUELW%2CPINDUW%2CPOILAPSP%2CPOILBRE%2CPOILDUB%2CPOILWTI%2CPNRGW%2CPOILAPSPW%2CPNGASW%2CPNGASEU%2CPNGASJP%2CPNGASUS%2CPCOALW%2CPCOALAU%2CPCOALSA%2CPFANDBW%2CPFOODW%2CPCEREW%2CPWHEAMT%2CPMAIZMT%2CPRICENPQ%2CPBARL%2CPVOILW%2CPSOYB%2CPSMEA%2CPSOIL%2CPROIL%2CPPOIL%2CPSUNO%2CPOLVOIL%2CPFISH%2CPGNUTS%2CPMEATW%2CPBEEF%2CPLAMB%2CPPORK%2CPPOULT%2CPSEAFW%2CPSALM%2CPSHRI%2CPSUGAW%2CPSUGAISA%2CPSUGAUSA%2CPBANSOP%2CPORANG%2CPBEVEW%2CPCOFFW%2CPCOFFOTM%2CPCOFFROB%2CPCOCO%2CPTEA%2CPRAWMW%2CPTIMBW%2CPHARDW%2CPLOGSK%2CPSAWMAL%2CPSOFTW%2CPLOGORE%2CPSAWORE%2CPCOTTIND%2CPWOOLW%2CPWOOLF%2CPWOOLC%2CPRUBB%2CPHIDE%2CPMETAW%2CPCOPP%2CPALUM%2CPIORECR%2CPTIN%2CPNICK%2CPZINC%2CPLEAD%2CPURAN&grp=1&a=1
  
     
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