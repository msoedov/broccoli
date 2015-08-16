default: format test

test:
	@nosetests --with-coverage

clean:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -fr {} \;


format:
	@echo "Formating:"
	@yapf  -dr ./
	@yapf  -ir ./