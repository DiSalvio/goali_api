# Goali

## Manages goals, tasks, and sub-tasks to help you stay organized

# Jenkins Unit Tests Job Status

[![Build Status](https://ecb4-199-101-192-72.ngrok.io/buildStatus/icon?job=goali_api_unit_tests)](https://ecb4-199-101-192-72.ngrok.io/job/goali_api_unit_tests/)

# Check out the deployed app here: https://www.goali.netlify.app

#### To use this API on your machine:

Install Python3 (3.9.10)

`pip install pipenv`

`pipenv shell`

`pipenv install`

`pipenv run python manage.py migrate`

`pipenv run python manage.py runserver`

#### To run unit tests:

`pipenv run python manage.py migrate`

`pipenv run python manage.py test`

#### API test env deploy status: https://damp-hamlet-38549.herokuapp.com/

If unit tests are successfully run, this app is deployed to a test environment for API testing.

[![Build Status](https://ecb4-199-101-192-72.ngrok.io/buildStatus/icon?job=deploy_goali_api_test_environment)](https://ecb4-199-101-192-72.ngrok.io/job/deploy_goali_api_test_environment/)
