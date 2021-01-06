"""
AutoViz example, see https://github.com/AutoViML
"""
from weo import get

from autoviz.AutoViz_Class import AutoViz_Class

AV = AutoViz_Class()

w = get(2019, "Oct")
dft = AV.AutoViz(
    "",
    depVar="NGDP_RPCH",
    dfte=w.fix_year(2024).T,
    header=0,
    verbose=2,
    lowess=False,
    chart_format="svg",
    max_rows_analyzed=1000,
    max_cols_analyzed=30,
)
