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
python scrape.py
rake db:seed
