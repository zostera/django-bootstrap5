NAME:= $(shell python -c 'from setuptools.config.setupcfg import read_configuration as c; print(c("setup.cfg")["metadata"]["name"])')
VERSION:= $(shell python -c 'from setuptools.config.setupcfg import read_configuration as c; print(c("setup.cfg")["metadata"]["version"])')
PACKAGE_DIR:= src/$(subst -,_,$(NAME))
SOURCE_FILES:= ${PACKAGE_DIR} tests example *.py

.PHONY: test
test:
	coverage run manage.py test
	coverage report

.PHONY: tox
tox:
	rm -rf .tox
	tox

.PHONY: reformat
reformat:
	autoflake -ir --remove-all-unused-imports ${SOURCE_FILES}
	isort ${SOURCE_FILES}
	-docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 ${SOURCE_FILES}
	black .

.PHONY: lint
lint:
	flake8 ${SOURCE_FILES}
	pydocstyle ${SOURCE_FILES}

.PHONY: docs
docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

.PHONY: porcelain
porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit those changes!";
	@exit 1;
endif

.PHONY: branch
branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main!"
	@exit 1;
endif

.PHONY: build
build: docs
	rm -rf build dist *.egg-info
	python -m build .

.PHONY: publish
publish: porcelain branch build
	twine upload dist/*
	rm -rf build dist *.egg-info
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags

.PHONY: check-description
check-description:
	rm -rf build-check-description
	pip wheel -w build-check-description --no-deps .
	twine check build-check-description/*
	rm -rf build-check-description

.PHONY: check-manifest
check-manifest:
	check-manifest --verbose
