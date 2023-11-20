.PHONY: start
start:
	uvicorn main:app --reload --port 8080
