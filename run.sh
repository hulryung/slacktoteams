#!/bin/bash
set -e
export PYTHONPATH=/app
pip3 install -r /requirements.txt
python3 /app/bot.py