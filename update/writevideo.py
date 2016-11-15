# -*- coding:utf-8 -*-
import sqlite3


###############################
##########メイン関数
###############################
def main():
    
    #railsのデータベース書き込み用ファイル
    wt = open("../db/seeds.rb", "w")
    wt.write("#coding: utf-8\n")
    dbdict = {}


    c = sqlite3.connect("../db/development.sqlite3").cursor()
    db_data = list(c.execute("select title, url, image, site_name, Date from videos;"))

    for i in db_data:
        dbdict[i[0]] = i[1:]

    for k, v in sorted(dbdict.items(), reverse=True):
        str1 = "@video.title = \"" + v[0].encode("utf-8") + "\""
        str1 = str1.replace("\n", "")
        str1 += "\n"
        
        wt.write("@video = Video.new\n")
        wt.write(str1)
        wt.write("@video.url = \"" + v[1] + "\"\n")
        wt.write("@video.image = \"" + v[2] + "\"\n")
        wt.write("@video.site_name = \"" + v[4].encode("utf-8") + "\"\n")
        wt.write("@video.Date = \"" + v[5].encode("utf-8") + "\"\n")
        wt.write("@video.save\n\n")

if __name__ == "__main__":
    main()

