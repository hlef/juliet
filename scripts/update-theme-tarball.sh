#!/bin/bash

THEME_URL="https://github.com/hlef/juliet-gram-theme/"

rm -rf juliet/resources/gram.zip .theme-tmp/
git clone ${THEME_URL} .theme-tmp/
cd .theme-tmp/
zip -r ../juliet/resources/gram.zip ./*
cd ../
rm -rf .theme-tmp/
