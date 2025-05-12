from setuptools import setup, find_packages

ver = '1.2.1'

setup(
    name='timedependentparty',
    version=ver,
    description='A python3 party that places bids with monotonically decreasing utility',
    url='https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWeb',
    author='W.Pasman',
    packages=find_packages(exclude=["test", "test.*", "test.*.*"]),
    package_data={ 'timedependentparty': ['py.typed']    },
    install_requires=[ "geniusweb@https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/export/93/geniuswebcore/dist/geniusweb-" + ver + ".tar.gz"],
    py_modules=['party']
)
