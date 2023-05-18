from setuptools import setup, find_packages

setup(
    name='finance',
    version='1.0.0',
    description='Futures and Options Market Data Analysis Program',
    author='dubinets',
    author_email='dubinets.av@gmail.com',
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4 == 4.11.1",
        "matplotlib == 3.5.3",
        "matplotlib == 3.7.0",
        "pandas == 1.3.5",
        "pandas == 1.5.3",
        "psycopg2 == 2.9.3",
        "PyMySQL == 1.0.2",
        "Requests == 2.30.0",
        "setuptools == 65.6.3",
    ],
    # Other optional configuration options
    # ...
)
