#!/bin/bash
python -m uvicorn app:app --host '0.0.0.0' --port 9995 --workers 1