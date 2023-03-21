# GENEMEDE
### **Docs:** ![docs](https://github.com/genemede/genemede/actions/workflows/deploy_mkdocs.yml/badge.svg)

GENEMEDE (GEneric NEuro MEtadata DEscriptors) is a generic metadata framework that may be used to comprehensively describe a neuroscience experiment.

The tool and the website is still a **work in progress**, so please expect a lot of changes.

For more information on the project please refer to our [**Documentation**](https://genemede.github.io/)

## Installation

Make sure you have pipenv in your default python environment

```bash
pip install pipenv
```

Clone the repo and install using pipenv

```bash
git clone 
cd genemede
pipenv install --dev -e .
```

This will install the package in editable mode and the development dependencies

To activate the genemede environment, just type the following in the genemede main folder: `pipenv shell` (type `exit` or press `Ctrl+D` to deactivate).

Additionally, you can also install [**pipes**](https://pipenv-pipes.readthedocs.io/en/latest/index.html) to help with CLI pipenv environments: `pip install pipenv-pipes`

Make sure your Python IDE is using the correct environment
