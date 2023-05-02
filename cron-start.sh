#! /usr/bin/env bash
set -e
celery -A cron.process_script worker -l info -c 8 --beat
