migration: ## Autogenerate a migration: make migration m="add users"
	alembic revision --autogenerate -m "$(m)"

migrate: ## Apply all pending migrations
	alembic upgrade head

downgrade: ## Roll back one migration
	alembic downgrade -1

up: ## Start the full stack in the background
	docker compose up -d --build

down: ## Stop the stack
	docker compose down

logs: ## Tail bot logs
	docker compose logs -f bot
