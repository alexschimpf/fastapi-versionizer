build:
	python setup.py sdist

deploy:
	twine upload dist/*

deploy-test:
	twine upload -r testpypi dist/*

run-tests:
	pytest tests/*

type-check:
	mypy .

install-dev:
	pip install -r requirements.dev.txt
