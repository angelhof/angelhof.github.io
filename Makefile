
PHONY: static

static:
	python3 bib2html.py
	python3 escape_rooms.py
	@(cd cv && make)
	cp cv/cv.pdf files/cv_konstantinos_kallas.pdf

static-debug:
	python3 bib2html.py --no-check
	python3 escape_rooms.py
	@(cd cv && make)
	cp cv/cv.pdf files/cv_konstantinos_kallas.pdf
