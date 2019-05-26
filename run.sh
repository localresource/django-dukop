#!/bin/bash

THIS_DIR=$( realpath $( dirname $0 ) )
cd $THIS_DIR

if [[ ! -d .venv ]]; then
	python3 -m venv .venv
fi

source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --editable ".[dev]"

pip install bpython

./manage.py migrate
if [[ $? -ne 0 ]]; then
	echo "Migrate failed ... Trying again ..."
	./manage.py migrate
fi

USER_COUNT=$( echo 'from dukop.apps.users import models; print(models.User.objects.filter(email="nomail@localhost.localdomain").count())' | python manage.py shell  )
if [[ $USER_COUNT == "0" ]]; then
	echo "Creating admin user ..."
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('password', email='nomail@localhost.localdomain')" | python manage.py shell
fi

grep -q ALLOWED_HOSTS ./src/dukop/settings/local.py
if [[ $? -ne 0 ]]; then
	echo "Adding ALLOWED_HOSTS to local.py ..."
	echo 'ALLOWED_HOSTS = ["*"]' >> ./src/dukop/settings/local.py
fi

./manage.py runserver 0.0.0.0:8000
