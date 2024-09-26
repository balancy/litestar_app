all: run-local

run-local:
	@uvicorn app:app --reload

lint:
	@ruff check .