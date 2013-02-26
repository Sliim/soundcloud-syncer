#!/bin/bash
#
# To run tests you need install nose, coverage and mock packages:
# pip-3.2 install nose coverage mock
#
nosetests-3.2 \
    -w tests/ssyncer \
    --with-coverage \
    --cover-package=ssyncer \
    --cover-erase \
    --cover-html
