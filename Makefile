dev-start:
	python manage.py runserver $(P) --settings=config.settings.dev

base-install:
	pip install -r requirements/base.txt

dev-install:
	pip install -r requirements/dev.txt
	sudo apt install redis-server

prod-install:
	pip install -r requirements/prod.txt

dev-migrate:
	python manage.py migrate --settings=config.settings.dev

dev-makemigrations:
	python manage.py makemigrations --settings=config.settings.dev

dev-showmigrations:
	python manage.py showmigrations --settings=config.settings.dev

dev-sqlmigrate:
	python manage.py sqlmigrate $(A) $(M) --settings=config.settings.dev

dev-rollback:
	python manage.py migrate $(A) $(M) --settings=config.settings.dev

dev-shell:
	python manage.py shell --settings=config.settings.dev

dev-test:
	python manage.py test --settings=config.settings.dev

dev-superuser:
	python manage.py createsuperuser --settings=config.settings.dev

dev-collectstatic:
	python manage.py collectstatic

