all: Pipfile.lock requirements.txt tests/requirements.txt test lint

Pipfile.lock: Pipfile
	pipenv lock --pre

requirements.txt: Pipfile Pipfile.lock
	pipenv lock --pre --requirements | grep -v "^-i" > requirements.txt

tests/requirements.txt: Pipfile Pipfile.lock
	pipenv lock --pre --dev --requirements > tests/requirements.txt

test:
	$(MAKE) -C tests clean
	$(MAKE) -C tests all

lint:
	pylint --disable=line-too-long,missing-docstring pf_focus

build: setup.py
	pipenv run python3 setup.py sdist bdist_wheel
