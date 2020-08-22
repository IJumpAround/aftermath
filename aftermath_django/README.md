## Making model changes
1. Change your models (in models.py).
1. Run `python manage.py makemigrations` to create migrations for those changes
1. Run `python manage.py migrate` to apply those changes to the database.


## Django shell with ipython
* `python manage.py shell -i ipython`