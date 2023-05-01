#! /usr/bin/env bash
set -e

python pre_start.py
celery -A cron.process_script worker -l info -c 8 --beat