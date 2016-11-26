#!/bin/sh
s="urls"
d=`date +%Y%m%d%H`
if [-f ${s}]; then
    cp urls urls_backup/$s$d
else
    echo "new file"
fi
ruby vrsearch.rb
s="sorted_URL"
if [-f ${s}]; then
    cp sorted.URL.txt sorted_URL_backup/$s$d
else
    echo "new file"
fi
python sorting.py
cd /var/www/rails/vrownie/db
s="seeds.rb"
if [-f ${s}]; then
    cp seeds.rb backup_seeds/$d$s
else
    echo "new file"
fi
cd /var/www/rails/vrownie/update
python localscrape.py
~/.rbenv/shims/rake db:seed
~/.rbenv/shims/rake db:seed RAILS_ENV=production
s="news.rb"
cp /var/www/rails/vrownie/db/seeds.rb /var/www/rails/vrownie/db/newsBackup/$d$s

