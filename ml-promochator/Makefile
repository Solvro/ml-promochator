# Default target executed when no arguments are given to make
all: help

lint:
	ruff check app
	ruff format app --check

format:
	pre-commit run

test:
	pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

test_no_migrations:
	pytest -m 'not alembic' -vx --cov=app --cov-report term-missing --cov-fail-under=95

test_only_migrations:
	pytest -m 'alembic'

alembic_downgrade:
	alembic -c /app/app/core/db/migrations/alembic.ini downgrade base

migration_file:
	alembic -c /app/app/core/db/migrations/alembic.ini revision --autogenerate

jupyter:
	jupyter notebook

jupyter_stop:
	jupyter notebook stop 8888

help:
	@echo '===================='
	@echo '-- DEVELOPMENT --'
	@echo 'lint                        - run linter'
	@echo 'format                      - run pre-commit hooks'
	@echo '-- TESTS --'
	@echo 'test                        - run unit tests'
	@echo 'test_no_migrations          - run unit tests without migrations'
	@echo 'test_only_migrations        - run migration tests'
	@echo '-- MIGRATIONS --'
	@echo 'alembic_downgrade           - run alembic downgrade'
	@echo 'migration_file              - run alembic file'
	@echo '-- RESEARCH --'
	@echo 'jupyter                     - run jupyter notebook server'
	@echo 'jupyter_stop                - stop jupyter notebook server'
	@echo '-- DOCUMENTATION tasks are from the top-level Makefile --'