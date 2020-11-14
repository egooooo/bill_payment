# BILL PAYMENT

* Project was tested on manOS Big Sur 
* Version 11.0.1

## Installation
1. Create virtualenv and activate:
```bash
virtualenv venv_bill --python=python3.8

source venv_bill/bin/activate
```

2. Database
```bash
python manage.py db init

python manage.py db migrate

python manage.py db upgrade
```

## Run backend
```bash
python manage.py run
```

## Logs
```bash
tail -f logs/log.log 
```

## Frontend 
In field ``frontend`` open ``index.html`` in browser.
