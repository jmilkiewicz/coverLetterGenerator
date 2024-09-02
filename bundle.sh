#!/usr/bin/env bash

rm -rf dist

pip install --platform manylinux2014_x86_64 --implementation cp --only-binary=:all: -r requirements.txt -t dist
# openai doesn't have a binary distribution, so need a separate install
pip install -I openai -t dist

# remove extraneous bits from installed packages
rm -r dist/*.dist-info
cp *.py dist/
cp cv.txt dist/
cp -r lambda dist/
cp -r templates dist/
cd dist && zip -r lambda.zip *