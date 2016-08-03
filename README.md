## Requirements
- python 3.4
- [RabbitMQ](https://www.rabbitmq.com/)

## Installation

You can use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) for creating virtual environments.

```
mkvirtualenv ronal -p python3.4
workon ronal
```

Installation of dependencies
```
pip install -r requirements_dev.txt
```

# ronal
Temporary data routing service (waiting for tartare)

to run it:
    `PYTHONPATH=. ./ronal/tasks.py`
    
to get custom settings:
    `./ronal/task.py --config-file my_settings_file.yml`

the python script will be run by a cron

## Tests
```
cd path/to/tartare
PYTHONPATH=. py.test tests
```