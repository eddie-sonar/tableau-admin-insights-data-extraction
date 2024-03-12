#!/bin/bash

python extract_hypers.py
arch -x86_64 /usr/bin/python3 hyper_to_csv.py
python load_to_sqlite_db.py