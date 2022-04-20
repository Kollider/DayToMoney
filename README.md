# DayToMoney
Day to Money - save money every day

# Development

This document assumes that all commands are executed within 'DayToMoney' project directory. 
In order to do so, please type 'cd DayToMoney' once before running anything else.

## Creating virtual environment (Windows 10/11)

'c:\path\to\python\python -m venv c:\path\to\DayToMoney\'

## Installing requirements

'pip install -r requirements.txt'

## Setting environment variables

In order for DayToMoney work properly the following environment variables needed to be set. Project support '.env' files:  
'SECRET_KEY' - could be generated randomly by 'import secrets' and then 'secrets.token_urlsafe(16)'  
'EMAIL_USER' - email for outgoing messages  
'EMAIL_PASS' - password for the email  
'DATABASE_URL' - path for the database. Could be set to 'sqlite:///site.db'

## Preparing the database

'flask db init'  
'flask db migrate'
'flask db upgrade'

## Running the application

'flask run --reload --debugger --host "0.0.0.0"'
