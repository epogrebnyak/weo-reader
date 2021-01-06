"""
GDP growth rates worldwide, as seen together with economy size.
"""

import matplotlib.pyplot as plt
import pandas as pd

from weo import download, WEO

path, url = download(2020, 2)
w = WEO(path)


def plot_mekko(
    widths,
    heights,
    title,
    nlargest=25,
    labels=["USA", "CHN", "IND", "JPN", "DEU"],
    color="dodgerblue",
    edgecolor="lightblue",
):
    plt.bar(
        x=[0] + widths.cumsum().tolist()[:-1],
        height=heights,
        width=widths,
        align="edge",
        color=color,
        edgecolor=edgecolor,
    )
    plt.title(title)
    y_shift = heights.max() * 0.025
    for lab in labels:
        z = widths.cumsum()
        bx = z.index.get_loc(lab)
        b = z.iloc[
            bx,
        ]
        ax = bx - 1
        a = (
            0
            if bx == 0
            else z.iloc[
                ax,
            ]
        )
        plt.text(
            x=(a + b) / 2,
            y=heights.loc[
                lab,
            ]
            + y_shift,
            s=lab,
            horizontalalignment="center",
        )
    return plt.Rectangle((0, 0), 1, 1, fc=color)


def largest(w, year, n):
    d_ = dict(gdp=w.gdp_usd(year), growth=w.gdp_growth(year))
    return pd.DataFrame(d_).dropna().sort_values("gdp").tail(n).sort_values("growth")


def plot_growth_mekko(source, year, nlargest=15, **kwargs):
    df = largest(w, year, nlargest)
    return plot_mekko(
        widths=df.gdp,
        heights=df.growth,
        title="Largest economies GDP growth rates in 2024 and 2018",
        **kwargs
    )


ax = plt.figure()
ar = plot_growth_mekko(
    w,
    2020,
    color="lavender",
    edgecolor="slategrey",
    labels=["USA", "CHN", "IND", "JPN", "DEU", "RUS"],
)
br = plot_growth_mekko(w, 2025, labels=["USA", "CHN", "IND"])
plt.ylim(-15, 9)
plt.xlabel("GDP, USD bln")
plt.ylabel("GDP real growth rate, %")
plt.legend([ar, br], ["2018", "2024"])
