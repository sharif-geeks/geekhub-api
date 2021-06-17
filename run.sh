#!/bin/sh

. venv/bin/activate
export FLASK_APP=api
flask run
python gui.py