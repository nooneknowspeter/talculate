.PHONY: all clean test all run install_deps 

all:
	make install_deps
	make run
run:
	python src/main.py
install_deps:
	pip install -r requirements.txt
