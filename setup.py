# https://docs.python.org/3/distutils/setupscript.html

from setuptools import setup, find_packages
from pathlib import Path

with open('README.md', encoding='utf-8') as file:
  readme_str = '\n'.join(file.readlines())

# 0.0.3 - can download a file as download('weo.csv', 2019, 2)
# 0.0.4 - download has year limits, more data accessor functions
# 0.0.5 - fixed as pip-installable, Google Colab example
# 0.0.6 - minor change of interfaces, exchange rate added
# 0.0.7 - allow two-letter country codes

setup(name='weo',
      version='0.0.7',
      description='Python client to read IMF WEO dataset as pandas dataframe',
      url='http://github.com/epogrebnyak/weo-reader',
      author='Evgeniy Pogrebnyak',
      author_email='e.pogrebnyak@gmail.com',
      license='MIT',
      py_modules=['weo'],
      scripts=['weo.py'],
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      long_description = readme_str,
      long_description_content_type="text/markdown",
      zip_safe=False,       
      install_requires=[
        "requests",
        "pandas",
        "numpy",
        "matplotlib",
        "iso3166"
        ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",  
        "Topic :: Office/Business :: Financial"
      ]
      )
