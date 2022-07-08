-include .env
export

lint:
	@mypy backend
	@flake8 backend

run:
	@python -m parser.hh
	