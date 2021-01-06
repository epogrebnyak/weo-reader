from weo import WEO

w = WEO("../weo.csv")

import missingno as msno

msno.matrix(w.df.sort_values(["ISO", "WEO Subject Code"]))
for label in w.core_codes:
    print(label, *w.from_code(label))
    msno.matrix(w.getc(label))

z = w.fix_year(2018)
z[~z.isna()] = 1
z.sum().sort_values().head()
z.sum().sort_values().head(20).index.map(lambda x: w.country_name(x))
cols = [c for c in w.codes if not c.endswith("_NGDP")]
msno.bar(w.fix_year(2024).transpose()[cols])
z.transpose().sum().sort_values().head(10).index.map(lambda x: w.from_code(x))

# Out[79]:
# MultiIndex([('Six-month London interbank offered rate (LIBOR)', ...),
#             (         'Output gap in percent of potential GDP', ...),
#             (                                     'Employment', ...),
#             (          'General government structural balance', ...),
#             (          'General government structural balance', ...),
#             (                    'General government net debt', ...),
#             (                    'General government net debt', ...),
#             (                              'Unemployment rate', ...),
#             (                         'Gross national savings', ...),
#             (                               'Total investment', ...)],
#            names=['WEO Subject Code', 'WEO Subject Code'])

# z.transpose().sum().sort_values().head(10).index
# Out[80]:
# Index(['FLIBOR6', 'NGAP_NPGDP', 'LE', 'GGSB_NPGDP', 'GGSB', 'GGXWDN',
#        'GGXWDN_NGDP', 'LUR', 'NGSD_NGDP', 'NID_NGDP'],
#       dtype='object', name='WEO Subject Code')
