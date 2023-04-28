#! /usr/bin/env bash
set -e

python pre_start.py
celery worker -A cron.main -l info -c 8 --beat
