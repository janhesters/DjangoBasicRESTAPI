SHELL := /bin/sh

# SET THIS! Directory containing wsgi.py (<configuration_root>).
PROJECT := config
# SET THIS!
APP := # Project name root name (<django_project_root>)

# SET THIS! Localpath should relatively from here point to <repository_root>.
LOCALPATH := .
PYTHONPATH := $(LOCALPATH)/
# Production
SETTINGS := production
DJANGO_SETTINGS_MODULE = $(PROJECT).settings.$(SETTINGS)
DJANGO_POSTFIX := --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
# Local
LOCAL_SETTINGS := local
DJANGO_LOCAL_SETTINGS_MODULE = $(PROJECT).settings.$(LOCAL_SETTINGS)
DJANGO_LOCAL_POSTFIX := --settings=$(DJANGO_LOCAL_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
# Staging
STAGING_SETTINGS := staging
DJANGO_STAGING_SETTINGS_MODULE = $(PROJECT).settings.$(STAGING_SETTINGS)
DJANGO_STAGING_POSTFIX := --settings=$(DJANGO_STAGING_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
TEST_SETTINGS := local
DJANGO_TEST_SETTINGS_MODULE = $(PROJECT).settings.$(TEST_SETTINGS)
DJANGO_TEST_POSTFIX := --settings=$(DJANGO_TEST_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
PYTHON_BIN := $(VIRTUAL_ENV)/bin

.PHONY: clean showenv coverage test bootstrap pip virtualenv sdist virtual_env_set

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@$(PYTHON_BIN)/python -c "import sys; print('sys.path:', sys.path)"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'PROJECT:' $(PROJECT)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_LOCAL_SETTINGS_MODULE:' $(DJANGO_LOCAL_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)

showenv.all: showenv showenv.virtualenv showenv.site

showenv.virtualenv: virtual_env_set
	PATH := $(VIRTUAL_ENV)/bin:$(PATH)
	export $(PATH)
	@echo 'VIRTUAL_ENV:' $(VIRTUAL_ENV)
	@echo 'PATH:' $(PATH)

showenv.site: site_set
	@echo 'SITE:' $(SITE)

djangohelp: virtual_env_set
	$(PYTHON_BIN)/django-admin.py help $(DJANGO_POSTFIX)

collectstatic: virtual_env_set
	-mkdir -p .$(LOCALPATH)/static
	$(PYTHON_BIN)/django-admin.py collectstatic -c --noinput $(DJANGO_POSTFIX)

runserver: virtual_env_set
	$(PYTHON_BIN)/django-admin.py runserver $(DJANGO_POSTFIX)

syncdb: virtual_env_set
	$(PYTHON_BIN)/django-admin.py syncdb $(DJANGO_POSTFIX)

cmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_POSTFIX)

localcmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_LOCAL_POSTFIX)

refresh:
	touch /$(PROJECT)/*wsgi.py

rsync:
	rsync -avz --checksum --exclude-from .gitignore --exclude-from .rsyncignore . ${REMOTE_URI}

compare:
	rsync -avz --checksum --dry-run --exclude-from .gitignore --exclude-from .rsyncignore . ${REMOTE_URI}

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist

test: clean virtual_env_set
	-$(PYTHON_BIN)/coverage run --source=$(APP) $(PYTHON_BIN)/django-admin.py test $(APP) $(DJANGO_TEST_POSTFIX)

coverage: virtual_env_set
	$(PYTHON_BIN)/coverage html --include="$(LOCALPATH)/*" --omit="*/admin.py,*/test*"

predeploy: test

register: virtual_env_set
	python setup.py register

sdist: virtual_env_set
	python setup.py sdist

upload: sdist virtual_env_set
	python setup.py upload
	make clean

bootstrap: virtualenv pip virtual_env_set

pip: requirements/$(SETTINGS).txt virtual_env_set
	pip install -r requirements/$(SETTINGS).txt

virtualenv:
	virtualenv --no-site-packages $(VIRTUAL_ENV)
	echo $(VIRTUAL_ENV)

all: collectstatic refresh

deploystaging:
		echo -r requirements/staging.txt > requirements.txt
		git commit -am "Requirements change for staging deployment"
		# git push heroku master # For heroku or other "git push" deployments
		eb deploy # For Elastic Beanstalk
		echo -r requirements/production.txt > requirements.txt
		git commit -am "Change back to production requirements"
