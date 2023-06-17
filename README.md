# polistack
**Built by RIT Students:** Rishabh Arora, Christian Haacke, Odin Wright, Arjun Kozhissery

**ROLES**
+ KPIs / DOCUMENTATION = Christian
+ INTERFACE / PRODUCT = Odin
+ MODELS / ALGORITHMS = Arjun
+ INTEGRATIONS / APIs = Rishabh
+ DATABASE / DATALAKE = Rishabh
+ ACCOUNTS / MANAGEMENT = Odin

**TECH STACK**
+ MONGO
+ PYTHON / DJANGO
+ JAVASCRIPT (AJAX) / HTML / CSS

## Configuration

To configure your local development environment in VS Code, follow these steps:

1. Open the `.vscode/settings.json` file.
2. Locate the `"python.pythonPath"` property and update it with the path to your Python installation.

## Versions

- Python/Django versions used: Check the [Pipfile](Pipfile) for the specific versions of Python and Django used in this project.

## Commands References

### Mac OS

Before running the commands, ensure that you have the latest version of Python installed.

* `pipenv install django` - Install django.
* `python3 --version` - Verify the installed Python version.
* `pip3 install pipenv` - Install Pipenv, a dependency management tool.
* `pipenv shell` - Activate the virtual environment for your project.
* `pipenv --venv` - Find path to virtual environment.
* `django-admin startproject name_of_your_project .` - Create a new Django project in the current directory.
* `python3 manage.py runserver` - Start the development server at http://127.0.0.1:8000/. 
* `source /path/to/virtual_environment/bin/activate` Sometimes the runserver command fails use this for alternative.
* `python3 manage.py startapp app_name` - Start a new django app
* `pip3 show django` - Check if django is installed and details are shown.
* `pip3 install requests`
* `pipenv install django-debug-toolbar`

#### Note: `python3` is used for avoiding using the Mac pre-installed python version.

Make sure to execute these commands in the project directory to set up and run your Django project successfully.


## Shortcuts in VS Code

### Mac OS
* `control + l` - clear terminal window.
* `command + b` - show/hide explorer panel.
* `control + \` ` -  show/hide terminal
* `command + p` - search box


## Appendix

* https://code.visualstudio.com/docs/python/tutorial-django
* https://www.youtube.com/watch?v=rHux0gMZ3Eg&ab_channel=ProgrammingwithMosh
* https://django-debug-toolbar.readthedocs.io/en/latest/
* https://code.visualstudio.com/
* https://www.mongodb.com/try/download/shell