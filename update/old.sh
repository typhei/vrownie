#!/bin/sh

cd /var/www/rails/vrownie/update/
s="urls"
d=`date +%Y%m%d`
if [-f ${s}]; then
    cp urls urls_backup/$s$d
else
    echo "new file"
fi
ruby /var/www/rails/vrownie/update/vrsearch.rb
s="sorted_URL"
if [-f ${s}]; then
    cp sorted.URL.txt sorted_URL_backup/$s$d
else
    echo "new file"
fi
python /var/www/rails/vrownie/update/sorting.py
cd /var/www/rails/vrownie/db
s="seeds.rb"
if [-f ${s}]; then
    cp seeds.rb backup_seeds/$d$s
else
    echo "new file"
fi
cd /var/www/rails/vrownie/
python /var/www/rails/vrownie/update/localscrape.py
rake db:seed

#heroku
rake assets:precompile RAILS_ENV=production
git add .
comment="update"
git commit -m $comment$d
rake db:seed RAILS_ENV=production

