python setup.py sdist bdist_wheel

REM will prompt for password unless stored locally in a config file
REM config file location: notepad %userprofile%/.pypirc
twine upload dist/*

REM Cleaning up...
rd build /Q/S
rd dist /Q/S
rd weo.egg-info /Q/S
