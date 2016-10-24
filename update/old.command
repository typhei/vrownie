#!/bin/sh

cd `dirname $0`
s="urls"
d=`date +%Y%m%d`
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
cd ../db
s="seeds.rb"
if [-f ${s}]; then
    cp seeds.rb backup_seeds/$d$s
else
    echo "new file"
fi
cd ../update
python localscrape.py
rake db:seed

#heroku
cd ..
rake assets:precompile RAILS_ENV=production
git add .
comment="update"
git commit -m $comment$d
git push heroku master
heroku run rake db:seed
