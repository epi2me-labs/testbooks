SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

OS := $(shell uname)

ifeq ($(OS), Darwin)
	SEDI=sed -i '.bak'
else
	SEDI=sed -i
endif


PYTHON   ?= python
VENV      = venv/bin/activate
IN_VENV=. ./$(VENV)
$(VENV):
> test -d venv || virtualenv venv --python=$(PYTHON) --prompt "(build) "
> ${IN_VENV}
> pip install pip --upgrade
> pip install requests semver

.PHONY: echo_latest_upstream
echo_latest_upstream: venv/bin/activate
> ${IN_VENV}
> $(eval TAG=$(shell . venv/bin/activate; python dockerhub_tag.py $(OWNER)/$(BASENAME) --prefix v))
> echo $(TAG)

OWNER := ontresearch
BASENAME := nanolabs-notebook
UPSTREAMTAG := dev

.PHONY: epi2melabs-notebook
epi2melabs-notebook:
> echo "Using upstream ${OWNER}/${BASENAME} tag: $(UPSTREAM)"
> docker pull $(OWNER)/$(BASENAME):$(UPSTREAM)
> docker images
> docker build --rm --force-rm --build-arg BASE_CONTAINER=$(OWNER)/$(BASENAME):$(UPSTREAM) -t $(OWNER)/$@:latest -f epi2melabs.dockerfile .
