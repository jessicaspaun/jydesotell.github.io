#!/bin/bash
cp -a . ~/Desktop/SiteRepo/jydesotell.github.io/
cd ~/Desktop/SiteRepo/jydesotell.github.io/
git add .
git commit -m "$1"
git push
