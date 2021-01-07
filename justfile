package := "weo"

# launch streamlit app
st:
  streamlit run streamlit_app.py

# black and isort
lint:  
   black .
   isort .

# create rst source for API documentation
apidoc:
  sphinx-apidoc -f -o docs {{package}}

# build and show documentation in browser
docs:
  sphinx-build -a docs docs/site
  start docs/site/index.html
