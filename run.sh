#!/bin/bash

source ~/.virtualenvs/foodreserve/bin/activate

nohup gunicorn --bind=0.0.0.0:8000 --capture-output food_reserve_backend.wsgi --timeout 600 --log-file=logs/web.log
