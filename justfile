package := "weo"

# list available commands (default option to just)
list:
  just --list

install:
  npm install -g codedown
  pip install dbnomics

# launch streamlit app
st:
  streamlit run streamlit_app.py

# black and isort
lint:  
   black .
   isort . --float-to-top
   ruff check .

# run code from README
readme:
  cat README.md | codedown python > readme.py
  python readme.py

# create rst source for API documentation
apidoc:
  sphinx-apidoc -f -o docs {{package}}

# build and show documentation in browser
docs:
  poetry run sphinx-build -a docs docs/site
  start docs/site/index.html

# Generate pdf version of sphinx documentation.
pdf:
  poetry run sphinx-build -b rinoh docs/. docs/_build/rinoh

# Push sphinx documentation to gh-pages branch.
gh:
  poetry run ghp-import docs/site --follow-links --force --no-jekyll --push
