# url-shortener-backend

# running api steps

## STEP 1
Open an integrated terminal on the repository folder and execute the following command in order to install all the modules required for the project:

```
pip install -r requirements.txt
```
## STEP 2
Open an integrated terminal on the api_ego folder that contains the manage.py file and execute the following command:
```
python manage.py runserver
```

# TESTING

In order to ensure that the API is working as expected i have created a series of tests for each endpoint that can be run before working with the API or touching any part of the code.

Open an integrated terminal on the repository folder that contains the manage.py file and execute the following command:
```
python manage.py test
```
Result should be OK if all the test were successful.