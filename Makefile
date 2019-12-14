
PHONY: static

static:
	python3 bib2html.py
	python3 escape_rooms.py

static-debug:
	python3 bib2html.py --no-check
	python3 escape_rooms.py
