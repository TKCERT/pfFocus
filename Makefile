all: test lint

test:
	$(MAKE) -C tests clean
	$(MAKE) -C tests all

lint:
	pylint --disable=line-too-long,missing-docstring format.py
