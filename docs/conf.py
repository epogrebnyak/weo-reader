"""Sphinx configuration."""

project = "weo"
author = "Evgeny Pogrebnyak"
copyright = "2021, Evgeny Pogrebnyak"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
