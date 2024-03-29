# Django project for a spearfishing store with Angular frontend:

## Spearfishing Store - Django Backend This is the Django backend server for the Spearfishing Store application. The frontend is built with Angular.

Getting Started Prerequisites Python & Django ( Docker optional) 
### Setup 
1. Clone the repository:

git Clone https://github.com/haimskira/final-back.git

2. Create and activate a virtualenv:

python -m virtualenv myenv  
myenv\Scripts\activate 

3. Install dependencies:

pip install -r requirements.txt
 
4. Run database migrations:

python manage.py migrate 

5. Create admin user:

python manage.py createsuperuser 

6. Run development server:

python manage.py runserver 

The API will be available at http://127.0.0.1:8000/

Docker Setup (Optional) 
1. Build Docker image:

docker build -t djapp . 

2. Run Docker container:

docker run -p 8000:8000 djapp

License MIT License