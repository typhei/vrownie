#!/bin/sh

python var/www/rails/vrownie/update/pull_video.py
cd var/www/rails/vrownie/
rake db:seed RAILS_ENV=production
