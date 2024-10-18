all: dev

run:
	@cd src && uvicorn app:app --reload

dev:
	@docker-compose up -d --build --remove-orphans

prod:
	@docker-compose -f docker-compose.yml up -d --build --remove-orphans

down:
	@docker-compose down

lint:
	@ruff check .
	@black .

clear:
	@docker system prune -f

test:
	@docker exec litestar-app pytest