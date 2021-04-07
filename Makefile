all: Pipfile.lock requirements.txt tests/requirements.txt tests

Pipfile.lock: Pipfile
	pipenv lock --pre

requirements.txt: Pipfile Pipfile.lock
	pipenv lock --pre --requirements | grep -v "^-e \." | grep -v "^-i" > requirements.txt

tests/requirements.txt: Pipfile Pipfile.lock
	pipenv lock --pre --dev --requirements > tests/requirements.txt

tests:
	$(MAKE) -C tests clean
	$(MAKE) -C tests all

build: setup.py
	pipenv run python3 setup.py sdist bdist_wheel

.PHONY: tests
