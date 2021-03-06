# ckanext-custom_schema

A CKAN extension to customize datasets' schema. By adding custom fields to the schema, this extension allows users to provide more information about datasets.

This extension adds customized metadata fields to datasets. After enableing it, go to ${URL}/dataset/edit/${YOUR-DATASET} to edit the custom fields.

# Repo Structure 
This is a mono-repo. Each branch contains a customer's schema. Before doing any work, please make sure that you are on the right branch. 

# Dependencies
This extension is dependent on the `ckanext-scheming` extension. Before installing this extension, click [here](https://github.com/OpenGov-OpenData/ckanext-scheming) to install the `ckanext-scheming` extension.

# Installation
To install, activate your CKAN virtualenv, install dependencies, and install the module in develop mode, which just puts the directory in your Python path.

```
. path/to/pyenv/bin/activate
pip install -r requirements.txt
python setup.py develop
```

Then in your CKAN .ini file, add `custom_schema` to your ckan.plugins line:
Please note that the `custom_schema` extension needs to come before the `scheming_datasets` extension.

```
ckan.plugins = (other plugins here...) custom_schema scheming_datasets
```
