from weo import WEO
from matplotlib.pyplot import figure

w = WEO('weo.csv')

# Variables
print(w.df[['WEO Subject Code', 'Subject Descriptor', 'Units']].drop_duplicates().sort_values('WEO Subject Code').to_csv(index=False))

# Real growth
(w.country('DEU').NGDP_RPCH / 100 + 1).cumprod().plot()

# Inflation
df = w.inflation()
df[df<100]
df[df<100].plot()
df[df<0].plot()

# What are the largest economies?
w.gdp_usd(2018).dropna().sort_values(ascending=True).tail(15).plot.barh()

# Is everyone growing fast?
figure()
g = ((w.gdp_growth().loc['2018':, ] / 100 + 1).prod() ** (1 / 7) - 1) * 100
g.hist(bins=50)

figure()
w.gdp_growth()['RUS'].plot.bar()  # change time axis

# So why is everyone centering around 2% inflation?
figure()
w.inflation(2024).where(lambda x: x < 15).dropna().hist(bins=40)

# Care to look at current accounts?
ca = w.current_account()

# Why current accounts not zero-summ?
ca['2018'].transpose().sum()

# Net exporters
figure()
ca.loc[:, ca.max() > 200].plot()

# Net importers
figure()
ca.loc[:, ca.min() < -100].plot()

# Who has most debt? Who is running a deficit?
brics = ['BRA', 'IND', 'CHN', 'RUS']
cri = ['ARG', 'GRC', 'RUS', ]  # can also include 'ECU', 'MEX'
oil = ['NOR', 'SAU', 'RUS', 'IRN']
dev = ['FRA', 'DEU', 'ITA', 'GBR', 'USA']  # 'ESP', 'KOR'

for subset in [brics, cri, oil, dev]:
    w.gov_debt_pgdp()[subset].plot(title="Государственный долг, % ВВП")
    w.gov_net_lending_pgdp()[subset] .plot(
        title="Чистое кредитование/заимствование госсектора, % ВВП").axhline(
        y=0, ls='-', lw=0.5, color='darkgrey')
