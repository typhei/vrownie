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
    db_data = list(c.execute("select number,title,url,image,body,site_name,date from pages;"))

    for i in db_data:
        dbdict[i[0]] = i[1:]

    for k, v in sorted(dbdict.items(), reverse=True):
        str1 = "@page.title = \"" + v[0].encode("utf-8") + "\""
        str1 = str1.replace("\n", "")
        str1 += "\n"
        
        wt.write("@page = Page.new\n")
        wt.write("@page.number = " + str(k) + "\n")
        wt.write(str1)
        wt.write("@page.url = \"" + v[1] + "\"\n")
        wt.write("@page.image = \"" + v[2] + "\"\n")
        wt.write("@page.body = \"" + v[3].encode("utf-8") + "\"\n")
        wt.write("@page.site_name = \"" + v[4].encode("utf-8") + "\"\n")
        wt.write("@page.date = \"" + v[5].encode("utf-8") + "\"\n")
        wt.write("@page.save\n\n")

if __name__ == "__main__":
    main()

