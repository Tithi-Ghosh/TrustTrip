# Trust Trip
python -m venv venv

venv\Scripts\activate

>Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

