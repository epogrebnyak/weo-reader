"""
GDP growth rates worldwide, as seen together with economy size.

In 2018 US was the fastest growing ecomony
except India, China, Indonesia and Poland.
ARG contracted. 

# Plotting details at https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.bar.html
"""

import matplotlib.pyplot as plt
import pandas as pd

from weo import WEO

w = WEO('weo.csv')

def plot_mekko(widths, 
               heights,
               title,
               nlargest = 25, 
               labels = ['USA', 'CHN', 'IND', 'JPN', 'DEU'],
               color='dodgerblue',
               edgecolor = 'lightblue'):
    df = pd.DataFrame(dict(w=widths, h=heights)) \
            .dropna() \
            .sort_values('w') \
            .tail(nlargest) \
            .sort_values('h')
    plt.bar(x=[0]+df.w.cumsum().tolist()[:-1],
            height=df.h,
            width=df.w,
            align='edge',
            color=color,
            edgecolor=edgecolor)
    plt.title(title)
    y_shift = df.h.max() * .025
    for lab in labels:
        z = df.w.cumsum()
        bx = z.index.get_loc(lab)
        b = z.iloc[bx,] 
        ax = bx-1       
        a = 0 if bx == 0 else z.iloc[ax,]        
        plt.text(x=(a+b)/2,
                 y=df.h.loc[lab,] + y_shift,
                 s=lab,
                 horizontalalignment='center')
    return plt.Rectangle((0, 0), 1, 1, fc=color)    
    

def plot_growth_mekko(source, year, **kwargs):
    return plot_mekko(w.gdp_usd(year),
               w.gdp_growth(year),
               f'GDP growth rates vs base economy size in 2024 and 2018',
               **kwargs)

ax = plt.figure()
ar = plot_growth_mekko(w, 2018, color='lavender',
                   edgecolor = 'slategrey',
                   labels=['USA', 'CHN', 'IND', 'JPN', 'DEU', 'ARG'])    
br = plot_growth_mekko(w,                   2024, 
                  labels=['USA', 'CHN', 'IND'])
plt.ylim(-3,9)
plt.xlabel("GDP, USD bln")
plt.ylabel("GDP real growth rate, %")
plt.legend([ar, br], ["2018", "2024"])


#legend((line1, line2, line3), ('label1', 'label2', 'label3'))    

#df = pd.DataFrame(dict(g24=w.gdp_growth(2024), 
#                  g18=w.gdp_growth(2014), 
#                 s=w.gdp_usd(2018)))