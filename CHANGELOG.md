Version changes
===============

0.7.2 (2022-10-16)
------------------

- switched from requests to httpx 
- disabled Sphinx and streamlit dependencies in pyproject.toml
- above allows quicker update of poetry dependencies

0.7.1 (2022-10-16)
------------------

- added latest confirmed release date to README, it is now 2022-04
- all releases 2007-01 to 2022-04 are downloadable 
- added just command to create readme.py and run from README.md 

0.7.0 (2020-10-16)
------------------

- Fixes the url for Oct 2021 release - thanks @jm-rivera.
- Simplified code for url creation.

0.6.4 (2021-09-01)
------------------

- Changed matplotlib version to less restrictive and added
  matplotlib to development dependencies - as it used directly only 
  in examples, not in weo package itself (unless with pandas). 
  Closes [#23](https://github.com/epogrebnyak/weo-reader/issues/23).
  