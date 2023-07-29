#!/bin/bash
celery -A worker worker --loglevel=info -Q keyword-extraction-queue --concurrency=1 --pool=eventlet
