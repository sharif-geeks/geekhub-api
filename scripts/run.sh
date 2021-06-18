#!/bin/sh

. venv/bin/activate
export FLASK_APP=src/api
flask run
python src/gui.py