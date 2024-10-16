all: up

run:
	@cd src && uvicorn app:app --reload

up:
	@docker-compose up -d --build

down:
	@docker-compose down

lint:
	@ruff check .
	@black .

clear:
	@docker system prune -f

test:
	@docker exec litestar-app pytest