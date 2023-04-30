#! /usr/bin/env bash
set -e

python pre_start.py
celery -A extensions.celery_app worker -l info -c 8 --beat