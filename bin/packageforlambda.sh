#!/bin/bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.9/site-packages
echo "Python dependencies location: $SITE_PACKAGES"
DIR=$(pwd)
OUT_DIR=$DIR/out

mkdir -p $OUT_DIR

# Make sure pipenv is good to go
echo "Doing a fresh pipenv install"
pipenv install

echo "Zipping for Lambda..."
cd $SITE_PACKAGES
zip -r9 $OUT_DIR/package.zip *

cd $DIR
zip -rg $OUT_DIR/package.zip src/
