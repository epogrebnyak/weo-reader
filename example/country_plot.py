import matplotlib.pyplot as plt
import pandas as pd
from weo import WEO

w = WEO("../weo.csv")


fig, axes = plt.subplots(
    nrows=3, ncols=3, figsize=(12 * 3 / 2, 8 * 3 / 2), facecolor="white"
)

iso_code = "RU"
c = w.country(iso_code)

df = pd.DataFrame()
gdp = c.NGDP_RPCH.dropna()
gdp.iloc[0] = 1
# FIXME: must use .combine to fix start of GDP time series for Russia, Ukraine, etc

df["GDP"] = (c.NGDP_RPCH.dropna() / 100 + 1).cumprod() * 100
df["CPI"] = c.PCPIPCH
df["FX"] = c.NGDP / c.NGDPD
df["DEFICIT"] = (c.GGR - c.GGX) / c.NGDP * 100
df["CA"] = c.BCA / c.NGDPD * 100

df["_GDEBT"] = (c.GGXWDG / c.NGDP) * 100
df["_NDEBT"] = (c.GGXWDN / c.NGDP) * 100

df.GDP.plot(ax=axes[0, 0], title=f"GDP growth, {gdp.index[0].year}=100")
c.LUR.plot(ax=axes[1, 0], title="Unemployment, %")
c.PCPIPCH.plot(
    ax=axes[0, 1], title="Inflation, annual average, %"
)  # FIXME: can draw deflator too here
df.FX.plot(
    ax=axes[1, 1], title="Exchange rate, national currency / USD, annual average"
)  # this is 1 for the US
(c.BCA / c.NGDPD * 100).plot(ax=axes[0, 2], title="Current account, % GDP").axhline(
    y=0, ls="-", lw=1, color="darkgrey"
)
df.DEFICIT.plot(ax=axes[1, 2], title="Budget deficit, % GDP").axhline(
    y=0, ls="-", lw=1, color="darkgrey"
)
df._GDEBT.plot(ax=axes[2, 2], title="Gross government debt, % GDP").axhline(
    y=0, ls="-", lw=1, color="darkgrey"
)
c.LP.plot(ax=axes[2, 0], title="Population, mln")
c.NGSD_NGDP.plot(ax=axes[2, 1], title="Savings and investment, % GDP")
c.NID_NGDP.plot(ax=axes[2, 1], color="lightblue")

plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.02)

fig.suptitle(w.country_name(iso_code) + f" ({iso_code})", x=0.02, ha="left")

for row in axes:
    for ax in row:
        ax.axvline(x="2019", ls="-", lw=0.5, color="lightblue")

plt.savefig(iso_code + ".png")
