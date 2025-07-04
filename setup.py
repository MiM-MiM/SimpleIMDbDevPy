import setuptools

DEV_PACKAGES = ["responses", "flake8", "pytest"]

setuptools.setup(
    name="SimpleIMDbDev",
    packages=["SimpleIMDbDev"],
    url="https://github.com/MiM-MiM/SimpleIMDbDevPy",
    version="1.1.0",
    description="Python3.10+ to fetch data from imdbapi.dev",
    author="MiM",
    keywords=["IMDb", "IMDbDev", "IMDbAPI", "API"],
    license="GNU General Public License v3.0",
    extras_require={
        "dev": DEV_PACKAGES,
    },
    install_requires=[
        'importlib-metadata; python_version>="3.10"',
        "requests",
    ],
)
