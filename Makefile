default: format test

test:
	@nosetests --with-coverage --cover-package broccoli

clean:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -fr {} \;

format:
	@echo "Formating:"
	@yapf  -dr ./
	@yapf  -ir ./

link-examples:
	@ln -s  tests/fixtures/*.py  examples