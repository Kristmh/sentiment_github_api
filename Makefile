.PHONY: start
start:
	uvicorn frontend.api.main:app --reload --port 8080

test:
	pytest && pytest --cov
