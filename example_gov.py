import matplotlib.pyplot as plt

from weo import WEO

w = WEO('weo.csv')

def plot_axh(df, **kwarg):
    df.plot(**kwarg).axhline(y=0, ls='-', lw=0.5, color='darkgrey')

def plot_deficit(subset, source=w):
    _df = source.get('General government net lending/borrowing',
                        'Percent of GDP')[subset]
    plot_axh(_df, title="Чистое кредитование/заимствование, % ВВП")

def plot_debt(subset, source=w):
    _df = source.get('General government gross debt',
                        'Percent of GDP')[subset]
    _df.plot(title="Государственный долг, % ВВП")

brics = ['BRA', 'IND', 'CHN', 'RUS']
cri = ['ARG', 'GRC', 'RUS', ]  # can also include 'ECU', 'MEX'
oil = ['NOR', 'SAU', 'RUS', 'IRN']
g3j = ['FRA', 'DEU', 'ITA', 'GBR', 'USA']  # 'ESP', 'KOR'

plot_debt(g3j)
plot_deficit(g3j)

plot_debt(brics)
plot_deficit(brics)

plot_debt(cri)
plot_deficit(cri)

plot_debt(oil)
plot_deficit(oil)
