"""Sphinx configuration."""

from pathlib import Path

import toml

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


def project_root():
    return Path(__file__).resolve().parent.parent


def get_toml():
    return toml.load(project_root() / "pyproject.toml")


version = get_toml()["tool"]["poetry"]["version"]

rinoh_documents = [
    dict(
        doc="index",
        target="weomanual",
        title="Weo Documentation",
        subtitle=f"Release {version}",
        author="Evgeny Pogrebnyak",
        template="Article",
    )
]
