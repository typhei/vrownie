#!/bin/sh
python pull_video.py
~/.rbenv/shims/rake db:seed RAILS_ENV=production
d=`date +%Y%m%d%H`
s="seeds.rb"
cp /var/www/rails/vrownie/db/seeds.rb /var/www/rails/vrownie/db/bkSeed/$d$s

