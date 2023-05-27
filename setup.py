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
        "matplotlib == 3.7.1",
        "pandas == 2.0.1",
        "psycopg2 == 2.9.6",
        "PyMySQL == 1.0.3",
        "Requests == 2.31.0",
        "setuptools == 65.6.3",
        "lxml == 4.9.1",
    ],
    # Other optional configuration options
    # ...
)
