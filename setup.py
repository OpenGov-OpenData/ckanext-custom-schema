#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-custom_schema',
    version='0.1',
    description='',
    license='AGPL3',
    author='Ankit Rana',
    author_email='arana@opengov.com',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.custom_schema'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        custom_schema = ckanext.custom_schema.plugins:customSchema
    """
)
