#!/bin/bash

cat ~/.pypirc
python setup.py sdist upload
