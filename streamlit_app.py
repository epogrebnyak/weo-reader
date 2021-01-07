import numpy as np
import pandas as pd
import streamlit as st

import weo

st.set_page_config(
    page_title="WEO Reader",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.title("Let's look at WEO dataset")


"""Picture here"""

st.header("Reference")
st.header("Load the data")

"""
```python
import weo
w = weo.get(2020, "October")
```
"""


@st.cache
def source():
    return weo.get(2020, 2)


st.header("What is inside?")
st.subheader("Variable names")

w = source()
with st.echo():
    for c in w.core_codes:
        st.write(c, (w.from_code(c)))

"""Note: more variable codes come through `w.codes`."""

st.subheader("Countries")

with st.echo():
    st.write(w.countries("United"))


st.subheader("Years")
with st.echo():
    st.write(w.years)

"""
1. Install: 
```
$ pip install streamlit
```

After installation ```streamlit``` will be available as a command line tool and as a package.

2. Make `my_app.py`:

```python
import streamlit as st
st.write("Hello, world!")
```

3. Run:

```
$ streamlit run my_app.py
```

4. Point your broswer to http://localhost:8501. The page will refresh as you edit and save `my_app.py`.


5. Learn more with [tutorials](https://docs.streamlit.io/en/stable/getting_started.html).
"""

st.header("Small examples")

st.subheader("Input and display a number, show code")

with st.echo():
    x = st.number_input("A number please:")
    st.write("Just got", x)

st.subheader("Input and display a number, show code")

color = st.select_slider(
    "Select a color of the rainbow",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
)
st.write("My favorite color is", color)


st.subheader("Slider")

hour = st.slider("Hour", 0, 23, 12)

st.subheader("Display text, markdown, latex, variable, code")

st.write("<hr>")
st.text("Fixed width text")
st.markdown("_Markdown_")  # see *
st.latex(r"e^{i\pi} + 1 = 0")
st.write("Most objects")  # df, err, func, keras!
st.write(dict(a=1))
st.write(["st", "is <", 3])  # see *
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")

st.subheader("Line break")

st.markdown("---")

st.subheader("Graphviz chart")

st.graphviz_chart(
    """
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
"""
)

st.subheader("Checkbox as collapse control")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")

st.subheader("Input text")

with st.echo():
    name = st.text_input("Name")
    st.text(name)

st.subheader("Show dataframe or table")
st.write(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)

st.subheader("Now there is a chart")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)

st.subheader("Now there is a map")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)
st.map(map_data)
