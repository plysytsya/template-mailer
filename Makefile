#!/usr/bin/env make

install:
	pip install -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete

test:
	nosetests -v

.PHONY: test
