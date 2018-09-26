# django_api
Basic Resfull API using Django (DRF)  

- Configure settings in app/local.env  
Eg.  
DJANGO_DEBUG=True  
DJANGO_ALLOWED_HOSTS= ['localhost']  
DATABASE_URL='sqlite:///my-local-sqlite.db'  

1. Install virtual env and activate  
2. Install requirements: `pip install -r requirements.txt` 
3. Create user: `python manage.py createsuperuser` 
4. Migrate db: `python manage.py makemigrations`  
5. Apply migrations: `python manage.py migrate`  
6. Run server: `python manage.py runserver`  
  
 7. Test API:
 Populate db with data running ths script dumpdb.py  
 
 8. Access the Admin Dashboard at: `localhost:8000/admin`  
 9. Access the API docs at: `localhost:8000/api/docs`  
 10. Access articles list at: `localhost:8000/api/v1/articles`
 11. Add like to a post using a post request to: `localhost:8000/api/v1/articles/like/<:int>`  
