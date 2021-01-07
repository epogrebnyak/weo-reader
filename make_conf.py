"""Generate configuration file (conf.py) for sphinx-doc.

Based on:
  - hypermodern python cookiecutter conf.py template
    https://github.com/cjolowicz/cookiecutter-hypermodern-python/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docs/conf.py   
  - poetry mechanism to split authors name and email from pyproject.toml
    https://github.com/python-poetry/poetry/blob/35058edf97e24ef1ac2b77563c84eed66d46939e/poetry/packages/package.py

To run: 
    
    python make_conf.py > docs/conf.py
    
Caution: this will overwrite existing conf.py file.
"""

from datetime import datetime
import toml
import re

AUTHOR_REGEX = re.compile(r"(?u)^(?P<name>[- .,\w\d'’\"()]+)(?: <(?P<email>.+?)>)?$")


def get_author(s: str) -> dict:
    m = AUTHOR_REGEX.match(s)
    name = m.group("name")
    email = m.group("email")
    return {"name": name, "email": email}


def conf_py(pyproject_filename: str) -> str:
    d = toml.load(pyproject_filename)["tool"]["poetry"]
    author = get_author(d["authors"][0])["name"]
    friendly_name = d["name"]

    return f"""\"\"\"Sphinx configuration.\"\"\"
    
project = "{friendly_name}"
author = "{author}"
copyright = "{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
"""


if __name__ == "__main__":
    print(conf_py("pyproject.toml"))
