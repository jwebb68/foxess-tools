SHELL:=/bin/sh

pkg:=$(patsubst src/%/__init__.py,%,$(wildcard src/*/__init__.py))

.PHONY: all
all:
	@echo "whut?"

.PHONY: distclean
distclean: clean
distclean:
	$(RM) -r dist/
	$(RM) -r htmlcov/

.PHONY: clean
clean:
	find src -name '*.pyc' -delete
	find tests -name '*.pyc' -delete
	$(RM) .coverage
	$(RM) dist/*.whl
	$(RM) dist/*.tar.gz

.PHONY: build
build: _install
build:
	poetry build

.PHONY: lint
lint: _install
lint:
	poetry run pylint -j0 --rcfile=pylintrc --output-format=parseable src tests

.PHONY: format
format: _install
format:
	poetry run black -l 80 src tests
	poetry run isort -j$(shell nproc) src tests

.PHONY: check test
test: check
check: _install
check:
	poetry run py.test $(pytest_opts) $(foreach v,$(pkg),--cov=$v) --cov-branch --cov-report=html src/ tests/

_install:
	poetry install
