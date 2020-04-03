SHELL := /bin/bash
CURRENT_DIR = $(shell pwd)

all: ;@echo 'Run with option.'

run:
		source venv/bin/activate && python server_1.py
