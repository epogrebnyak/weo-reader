# Download source:
# curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert(x):
    if isinstance(x, str) and "," in x:
        x = x.replace(",","")
    try:
        return float(x)
    except ValueError:
        return np.nan
    
assert convert("9,902.554") == 9902.554

class WEO:
    years = [str(x) for x in range(1980, 2024+1)]
    
    def __init__(self, filename):
        df = pd.read_csv(filename, delimiter="\t", encoding="iso-8859-1")
        ix = df['Country'].isna()
        self.df = df[~ix]
        # attributes
        self.vars = self.df['Subject Descriptor'].unique()        
        self.columns = self.df.columns
        self.units = self.df['Units'].unique()
        country_cols = ['WEO Country Code', 'ISO', 'Country']     
        self.countries_df = self.df[country_cols].drop_duplicates()          
        
    def by_subject(self, subjects):
        if isinstance(subjects, str):
            subjects = [subjects]            
        ix = self.df['Subject Descriptor'].isin(subjects) 
        return self.df[ix]                   
    
    def get(self, subject, unit):
        _df = self.by_subject(subject)
        units = _df['Units'].unique()
        if unit not in units:
            raise ValueError(f"Unit must be one of {units}, provided: {unit}")
        cols = self.years + ['ISO']
        ix = _df['Units'] == unit
        _df = _df[ix][cols] \
                 .set_index('ISO') \
                 .transpose()
        _df.columns.name = ''
        _df.index = pd.date_range(start='1980', end='2025', freq='A')
        return _df.applymap(convert)

    def find(self, country: str):
        c = country.lower()
        ix = self.countries_df['Country'].apply(lambda x: c in x.lower())
        return self.countries_df[ix]                   
  
    def gdp_usd(self, year=2018):
        return self.get('Gross domestic product, current prices', 
                        'U.S. dollars') \
                        [str(year)] \
                        .transpose() \
                        .iloc[:,0] \
                        .sort_values(ascending=False)

    
countries_doc = """Afghanistan
Albania
Algeria
Angola
Antigua and Barbuda
+Argentina
Armenia
Aruba
+Australia
Austria
Azerbaijan
The Bahamas
Bahrain
Bangladesh
Barbados
Belarus
Belgium
Belize
Benin
Bhutan
Bolivia
Bosnia and Herzegovina
Botswana
+Brazil
Brunei Darussalam
Bulgaria
Burkina Faso
Burundi
Cabo Verde
Cambodia
Cameroon
Canada
Central African Republic
Chad
Chile
+China
Colombia
Comoros
Democratic Republic of the Congo
Republic of Congo
Costa Rica
Côte d'Ivoire
Croatia
Cyprus
Czech Republic
Denmark
Djibouti
Dominica
Dominican Republic
Ecuador
Egypt
El Salvador
Equatorial Guinea
Eritrea
Estonia
Eswatini
Ethiopia
Fiji
Finland
+France
Gabon
The Gambia
Georgia
+Germany
Ghana
+Greece
Grenada
Guatemala
Guinea
Guinea-Bissau
Guyana
Haiti
Honduras
Hong Kong SAR
Hungary
Iceland
+India
Indonesia
Islamic Republic of Iran
Iraq
Ireland
Israel
+Italy
Jamaica
+Japan
Jordan
Kazakhstan
Kenya
Kiribati
Korea
Kosovo
Kuwait
Kyrgyz Republic
Lao P.D.R.
Latvia
Lebanon
Lesotho
Liberia
Libya
Lithuania
Luxembourg
Macao SAR
Madagascar
Malawi
Malaysia
Maldives
Mali
Malta
Marshall Islands
Mauritania
Mauritius
Mexico
Micronesia
Moldova
Mongolia
Montenegro
Morocco
Mozambique
Myanmar
Namibia
Nauru
Nepal
Netherlands
New Zealand
Nicaragua
Niger
Nigeria
North Macedonia
+Norway
Oman
Pakistan
Palau
Panama
Papua New Guinea
Paraguay
Peru
Philippines
Poland
Portugal
Puerto Rico
Qatar
Romania
+Russia
Rwanda
Samoa
San Marino
São Tomé and Príncipe
+Saudi Arabia
Senegal
Serbia
Seychelles
Sierra Leone
Singapore
Slovak Republic
Slovenia
Solomon Islands
Somalia
+South Africa
South Sudan
+Spain
Sri Lanka
St. Kitts and Nevis
St. Lucia
St. Vincent and the Grenadines
Sudan
Suriname
Sweden
Switzerland
Syria
Taiwan Province of China
Tajikistan
Tanzania
Thailand
Timor-Leste
Togo
Tonga
Trinidad and Tobago
Tunisia
Turkey
Turkmenistan
Tuvalu
Uganda
Ukraine
United Arab Emirates
+United Kingdom
+United States
Uruguay
Uzbekistan
Vanuatu
Venezuela
Vietnam
Yemen
Zambia
Zimbabwe"""


def plot_axh(df, title):
  df.plot(title=title) \
     .axhline(y=0, ls='-', lw=0.5, color='darkgrey')
     
if __name__  == '__main__':
    
    w = WEO('weo.csv')
    
    def find_first(s):
        return w.find(s).ISO.iloc[0]    
    
    focus_countries = [find_first(c[1:]) for c 
                       in countries_doc.split('\n') 
                       if c.startswith('+')]
    
    def plot_deficit(subset, source=w):
        _df = source.get('General government net lending/borrowing',
                         'Percent of GDP')[subset]
        plot_axh(_df, "Чистое кредитование/заимствование, % ВВП")
    
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