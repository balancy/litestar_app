all: up

run-app:
	@uvicorn app:app --reload

up:
	@docker-compose up -d --build

down:
	@docker-compose down

lint:
	@ruff check .
	@black .