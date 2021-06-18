#!/bin/sh

. venv/bin/activate
export FLASK_ENV=development
python src/api.py
python src/gui.py