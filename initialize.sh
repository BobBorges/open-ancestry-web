#!/bin/bash

# Generate Environment
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Generating python venv |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~|~"
python3 -m venv ancestryENV

# Activate Environment
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | ...activating environment |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
source ancestryENV/bin/activate
python -m ensurepip --upgrade

# install dependencies
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Installing dependencies |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~|~"
pip install -r requirements.txt

# Secret Key
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Generating Django Secret Key |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
python generate_secretkey.py

# Migrate DB
echo "~|~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Initializing Database |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~|~"
python manage.py makemigrations
python manage.py migrate

echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Initializing track changes in DB |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
python manage.py createinitialrevisions private.Source --comment="initial revision"
python manage.py createinitialrevisions private.Person --comment="initial revision"
python manage.py createinitialrevisions private.AlternativeName --comment="initial revision"
python manage.py createinitialrevisions private.Event --comment="initial revision"
python manage.py createinitialrevisions private.Epoch --comment="initial revision"
python manage.py createinitialrevisions private.Relationship --comment="initial revision"
python manage.py createinitialrevisions private.BiographicalInfoNugget --comment="initial revision"

echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
echo " | Done : Open Ancestry Web is ready for use. |"
echo "~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~"
