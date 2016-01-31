src_dir := pytree

python ?= python

virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
pytest := $(virtualenv_dir)/bin/py.test

test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):$(src_dir) $(pytest) -s tests
.PHONY: test

$(virtualenv_dir): requirements.txt
	virtualenv $@ -p $(python)
	$(pip) install -r $^
