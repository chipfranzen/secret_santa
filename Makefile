:PHONY santa server test

santa:
	poetry run python secret_santa.py

server:
	poetry run python -m smtpd -n -c DebuggingServer localhost:1025

test:
	poetry run python secret_santa.py --test
