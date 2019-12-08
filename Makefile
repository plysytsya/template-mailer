#!/usr/bin/env make

install:
	pip install -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete

test:
	python setup.py test

.PHONY: test

build:
	pip install twine
	pip install wheel
	python setup.py develop
	python setup.py bdist_wheel

.PHONY: build