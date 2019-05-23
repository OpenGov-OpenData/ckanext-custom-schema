#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-custom_schema',
    version='0.1',
    description='',
    license='AGPL3',
    author='Jay Guo',
    author_email='jguo@opengov.com',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.custom_schema'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        cademo_schema = ckanext.custom_schema.cademo.plugins:customSchema
        fiscal_schema = ckanext.custom_schema.fiscal.plugins:customSchema
        nasalsda_schema = ckanext.custom_schema.nasalsda.plugins:customSchema
        sanjose_schema = ckanext.custom_schema.sanjose.plugins:customSchema
    """
)
