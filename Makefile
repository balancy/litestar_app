all: up

run-app:
	@uvicorn app:app --reload

up:
	@docker-compose up --build --watch

down:
	@docker-compose down

lint:
	@ruff check .