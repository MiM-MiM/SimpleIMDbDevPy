import setuptools

setuptools.setup(
    name="SimpleIMDbDev",
    packages=["SimpleIMDbDev"],
    url="https://github.com/MiM-MiM/SimpleIMDbDevPy",
    version="0.1",
    description="Python3.10+ to fetch data from imdbapi.dev",
    author="MiM",
    keywords=["IMDb", "IMDbDev", "IMDbAPI", "API"],
    license="GNU General Public License v3.0",
    install_requires=[
        'importlib-metadata; python_version>="3.10"',
        "requests",
    ],
)
