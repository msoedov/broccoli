default: format test

test:
	@nosetests --with-coverage --cover-package broccoli

clean:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -fr {} \;
	@rm -rf dist
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf broccoli.egg-info

format:
	@echo "Formating:"
	@yapf  -dr ./
	@yapf  -ir ./

link-examples:
	@rm -f examples
	@ln -s  tests/fixtures examples
