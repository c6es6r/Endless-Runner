default: run

run:
	python3 src/main.py

clean:
	rm -r src/__pycache__

line_count:
	wc -l src/*.py
