# Mark countries you want to select with +

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


from weo import WEO

w = WEO('weo.csv')
focus_countries = [w.iso_code(c[1:]) for c 
                   in countries_doc.split('\n') 
                   if c.startswith('+')]

print(focus_countries)
