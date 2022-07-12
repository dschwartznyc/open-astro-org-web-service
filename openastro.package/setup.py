# python3 setup.py sdist
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup (
	name='openastro',
	version='1.1.57',
	description='Open Source Astrology',
	author='Pelle van der Scheer',
	author_email='devel@openastro.org',
	url='http://www.openastro.org',
	license='GPL',
	install_requires=[
          'pyswisseph'],
	packages=setuptools.find_packages(),
	include_package_data=True
)