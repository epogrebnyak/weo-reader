import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from weo import WEO
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SubPlot:
    values: pd.Series
    row: int
    col: int
    name: str
    latest: pd.Series = pd.Series()
    unit: str = "%"
    abline_zero: bool = False
    digits: int = 1


def gdp_string(x):
    if x > 1000:
        return "${:.2f}T".format(x / 1000)
    return "${:.0f}B".format(x)


def make_subplots(c):
    df = make_plottable_df(c)
    gdp = gdp_string(c.NGDPD["2018"])
    return [
        SubPlot(df.GDP, 0, 0, f"GDP: {gdp} (2018)", latest=c.NGDP_RPCH),
        SubPlot(df.CPI, 0, 1, "Inflation", abline_zero=True),
        SubPlot(df.CA, 0, 2, "Current account", unit="% GDP", abline_zero=True),
        SubPlot(df.POP, 1, 0, "Population", unit="m"),
        SubPlot(df.FX, 1, 1, "Exchange rate", unit=""),
        SubPlot(df.DEFICIT, 1, 2, "Budget deficit", unit="% GDP", abline_zero=True),
    ]


def last(s):
    ts = s.values if s.latest.empty else s.latest
    return ts.tail(1).round(s.digits).iloc[0]


def title(s):
    return f"{s.name}\n(2024: {last(s)}{s.unit})"


def plot_one(s, axes):
    ax = s.values.plot(ax=axes[s.row, s.col], title=title(s))
    if s.abline_zero:
        ax.axhline(y=0, ls="-", lw=1, color="darkgrey")
    return ax


def upper_lim(n):
    def cap(x):
        return np.nan if x > n else x

    return cap


def make_plottable_df(c):
    df = pd.DataFrame()
    df["GDP"] = (c.NGDP_RPCH.dropna() / 100 + 1).cumprod() * 100
    df["CPI"] = c.PCPIPCH.apply(upper_lim(20))
    df["FX"] = c.NGDP / c.NGDPD
    df["DEFICIT"] = (c.GGR - c.GGX) / c.NGDP * 100
    df["CA"] = c.BCA / c.NGDPD * 100
    df["POP"] = c.LP
    return df


def filename(code):
    return code.lower() + ".png"


def plot_sparklines(c, iso_code, title="", footer=True):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8, 2.8), facecolor="white")
    plt.subplots_adjust(hspace=0.8, wspace=0.2, top=0.7)

    for sp in make_subplots(c):
        plot_one(sp, axes)

    for ax in [ax for axlist in axes for ax in axlist]:
        for k, v in ax.spines.items():
            v.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")
        ax.title.set_size(10)

    if title:
        fig.suptitle(title, ha="left", weight="bold")

    if footer:
        _ = plt.figtext(0.46, 0, "Years: 1980-2024. Source: IMF WEO, October 2019.")

    plt.savefig(filename(iso_code))


def make_title(w, code):
    return f"{w.country_name(code)} ({code})"


def plot(w, code):
    c = w.country(code)
    plot_sparklines(c, code, title=make_title(w, code), footer=True)


# script

w = WEO("weo.csv")
plot(w, "UA")

head = """
<HTML>
<HEAD></HEAD>
<BODY><CENTER>
<H1>IMF World Economic Outlook (WEO) for selected countries</H1> 
October 2019
"""


def add_image(code):
    return f'<img src="{filename(code)}">\n<BR>\n'


bottom = """
</CENTER>
</BODY>
</HTML>
"""

countries = {
    "North America": ["USA", "CAN", "MEX"],
    "Europe": ["DEU", "GBR", "FRA", "ITA", "ESP", "CHE"],
    "CIS": ["RUS", "UA", "KZ", "BLR"],
    "DM Asia": ["JPN", "KOR", "AUS"],
    "EM Asia": ["CHN", "IND", "IDN"],
    "Latin America": ["BRA", "ARG"],
    "Africa": ["ZAF", "NGA", "EGY"],
}

contents = head
for group, members in countries.items():
    contents += f"<H2>{group}</H2>"
    for code in members:
        contents += f"<H3>{w.country_name(code)}</H3>"
        contents += add_image(code)
        c = w.country(code)
        plot_sparklines(c, code, title="", footer=False)
contents += bottom
Path("index.html").write_text(contents)


# TODO:
# make a dot-point on the graph

# NOT TODO:
# https://stackoverflow.com/questions/3609585/how-to-insert-a-small-image-on-the-corner-of-a-plot-with-matplotlib
