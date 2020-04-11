install:
	poetry install

lint:
	poetry run flake8 pageloader

test:
	poetry run pytest

test-with-coverage:
	poetry run pytest --cov=pageloader tests  --cov-report xml

analyze:
	poetry run mypy pageloader

test-publish:
	poetry publish -r testpypi
