all: run-docker

run-local:
	@uvicorn app:app --reload

run-docker:
	@docker-compose up --build

lint:
	@ruff check .