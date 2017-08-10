all: test lint

test:
	$(MAKE) -C tests clean
	$(MAKE) -C tests all

lint:
	pylint --py3k format.py
