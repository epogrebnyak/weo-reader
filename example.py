from weo import download, WEO
path, url = download(2021, 2)
w = WEO(path)
print(w.inflation()[["USA"]].tail(8))