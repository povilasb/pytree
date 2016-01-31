src_dir := pytree

python ?= python

virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
pytest := $(virtualenv_dir)/bin/py.test
coverage := $(virtualenv_dir)/bin/coverage

test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):$(src_dir) $(coverage) run \
		--source $(src_dir) $(pytest) -s tests
	$(coverage) report -m
.PHONY: test

$(virtualenv_dir): requirements.txt
	virtualenv $@ -p $(python)
	$(pip) install -r $^
