#!/bin/sh

. venv/bin/activate
export FLASK_ENV=development
python api.py
python gui.py