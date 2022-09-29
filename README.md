# YATUBE
Social network for publishing diaries
### Description
You can create posts, leave comments under posts and subscribe to your favorite authors.
### Technologies
Python 3, Django 2.2 LTS, PostgreSQL, gunicorn, nginx, Яндекс.Облако(Ubuntu 20.04), pytest, Pillow, sorl-thumbnail, Bootstrap
### Launching a project in dev mode
- Clone the repository and go to it on the command line:
- Install and activate the virtual environment:
```
For Windows users:
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
``
- Install dependencies from the file requirements.txt
``
pip install -r requirements.txt
``
- Go to the directory with the file manage.py run the commands:
Perform migrations:
``
python manage.py migrate
```
Create a super user:
``
python manage.py createsuperuser
``
Collect static:
``
python manage.py collectstatic
``
Project launch:
``
python manage.py runserver
``

### Authors
Danil Shtun
