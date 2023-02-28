from setuptools import find_packages, setup

setup(
    name="housinglib",
    version='0.1.0',
    description="Housing code library",
    long_description="This library contains the functions like loading data and creating features and training the data.",
    author="Vishal-Allada",
    py_modules=['housinglib'],
    package_dir={"":'src/housinglib'},
)
