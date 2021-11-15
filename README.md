# Price and quantity update service


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

Price and quantity stock update service for online store with multiple suppliers. 

## Installation and running

Clone repository 

```sh
git clone https://github.com/demchyk/csv_analyzer
```
Install the dependencies

```sh
cd csv_analyzer
pip install -r requirements.txt
```

And start the server

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Usage

To add information about suppliers pricelist open admin panel, create supplier and fill the table


![admin_suppliers](/img/admin_suppliers.png)


![supplier_info](/img/supplier_info.png)


![main](/img/main.gif)
