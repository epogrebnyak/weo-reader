from weo import WEO, download

path, url = download(2022, 1)  # first (April) semiannual release
w = WEO(path)
df_cpi = w.inflation()
print(df_cpi.USA.tail(8))

# weo_2022_1.csv 18.8Mb
# Downloaded 2022-Apr WEO dataset
#         USA
# 2020  1.549
# 2021  7.426
# 2022  5.329
# 2023  2.337
# 2024  2.096
# 2025  1.970
# 2026  1.983
# 2027  2.017
