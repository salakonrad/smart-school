# Smart School Application
## Running on local machine with manual backend from command line
- Run MySQL database and phpMyAdmin  
`docker-compose -f docker-compose-dev.yml up -d`

- Setup Virtualenv  
`python -m venv .venv`

- Activate Virtualenv  
`source .venv/bin/activate`

- Install dependencies  
`pip install -r requirements.txt`

- Create Database in MySQL called **smart_school_db**.  
You can open http://127.0.0.1:8082/ and click on **New**

- Create migrations for Database  
`python manage.py migrate`

- Create superuser for Django Admin Panel  
`python manage.py createsuperuser`

- Export Environment variables for email SMTP settings depending on service used   
  - **AWS SES**
```
export AWS_ACCESS_KEY_ID="somekeyid"
export AWS_SECRET_ACCESS_KEY="accesskey"
```
- **Normal SMTP**
```
export EMAIL_HOST_USER="xyz"
export EMAIL_HOST_PASSWORD="xyz"
```

- Run Django Backend  
`python manage.py runserver`

## Running whole stack using Docker
- Start whole stack  
`docker-compose up -d`

- Create Database in MySQL called **smart_school_db**.
You can open http://127.0.0.1:8082/ and click on **New**

- Create migrations for Database  
`docker-compose run backend python manage.py migrate`

- Create superuser for Django Admin Panel  
`docker-compose run backend python manage.py createsuperuser`

- Export Environment variables for email SMTP settings depending on service used   
  - **AWS SES**
```
export AWS_ACCESS_KEY_ID="somekeyid"
export AWS_SECRET_ACCESS_KEY="accesskey"
```
  - **Normal SMTP**
```
export EMAIL_HOST_USER="xyz"
export EMAIL_HOST_PASSWORD="xyz"
```

- Recreate whole stack in order to retry connection to MySQL  
`docker-compose up --force-recreate --build -d`

App is now ready! You can visit http://127.0.0.1:8000

## Force redeploy  
`docker-compose up --force-recreate --build -d`
