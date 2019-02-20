### How to run the app ?
 - virtualenv -p python3 myenv --no-site-packages
 - source activate myenv
 - pip install -r requirements.txt
  - python manage.py runserver
 
### Maintaining requirements.txt file ( register packages based on imports )
 - pipreqs . --force

### Migration Error resolve
 - delete administration migrations
 - comment erroneous foreign keys (startup)
 - python manage.py makemigrations administrator
 - python manage.py migrate
 - Uncomment and migrate administrator
### Migrate safely
 - python manage.py makemigrations login startup investor mentor administrator
