.PHONY: start
start:
	uvicorn api.index:app --reload --port 8080

test:
	pytest && pytest --cov
