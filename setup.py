from setuptools import setup

setup(
   name='PST_Generator',
   version='1.0',
   description='A Module to Auto Generate the PST',
   author='Hari om Singh',
   author_email='hariomsingh2007@bt.com',
   packages=['PSTGEN'],  
   install_requires=['openpyxl']#external packages as dependencies
)
