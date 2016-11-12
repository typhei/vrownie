# -*- coding:utf-8 -*-
import urllib2
import time
import os
from bs4 import BeautifulSoup
from PIL import Image
import math
import psycopg2
import urlparse
import datetime

path = "../public/images/"
imagetype = ["png", "gif", "jpg", "jpeg"]
NUM = 10

#####画像のダウンロード#####
def download_img(src,maxsize,current):
    try:
        #URLから画像を取得
        filename ="unknown"
        i = urllib2.urlopen(src)
        filename = src.split("/")[-1]
        print "downloading..."

        if os.path.isfile(path+filename):
            return filename,""
            print "one"

        if filename.split(".")[-1] not in imagetype:
            print "here"
            raise "Unknown image type Error"

        if os.path.isfile(path+filename) != True:
            print "two"
            #saveDataというバイナリデータを作成
            saveData = open(path + filename, "wb")

            #saveDataに取得した画像を書き込み
            saveData.write(i.read())
            saveData.close()

            print ">>>get:",filename

        print "three"
        #画像解像度
        newsize = reduce(lambda x,y:x*y, Image.open(path+filename).size)

        if newsize > maxsize:
            
            #前の候補画像を削除
            if current != "":
                os.remove(path+current)
                print "-----removed:",current, "-----"
                
            return filename, newsize
        
        else:
            return "",""
        


        return filename

    #ダウンロードできなかった場合は空文字列を返す
    except Exception as e:
        print "error"
        print e
        print ">>>error:", src
        return ""



###############################
##########メイン関数
###############################
def main():
    
    #選別したURLの書き込み先ファイル
    f = open("sorted_URL")
    #railsのデータベース書き込み用ファイル
    wt = open("../db/seeds.rb", "w")
    wt.write("#coding: utf-8\n")

    #日付
    today = datetime.date.today()
    if int(today.month) < 10:
        mon = "0" + str(today.month)
    else:
        mon = str(today.month)
    if int(today.day) < 10:
        day = "0" + str(today.day)
    else:
        day = str(today.day)
    updt = str(today.year) + "/" + mon + "/" + day
    

    count = 1
    
    #c = sqlite3.connect("../db/development.sqlite3").cursor()
    #db_data = list(c.execute("select url from pages;"))
    #db_data = [x[0] for x in db_data]
    #maxnum = list(c.execute("select max(number) from pages;"))[0][0]
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)

    cur = conn.cursor()

    cur.execute("SELECT max(number) FROM pages;")
    maxnum = cur.fetchall()[0][0]
    cur.execute("select url from pages;")
    db_data = [x[0] for x in cur.fetchall()]
    
    
    if maxnum is None:
        maxnum = 0

        

    listNum = 1
    uparticles = {}
    
    for url in f:
        try:
            if count > NUM:
                break
            #ページを読み込み．テキスト部分とimgタグを収集
            print url
            res = urllib2.urlopen(url)
            html = res.read()
            soup = BeautifulSoup(html)
            meta = soup.find_all("meta")
            title,description,image = "","",""
            image_file = ""
            maxsz = 0
            current = ""
            image = ""
            site_name = ""
            
            for m in meta:
                if m.get("property") == "og:title":
                    title = m.get("content")
                elif m.get("property") == "og:description":
                    description = m.get("content")
                elif m.get("property") == "og:image":
                    image = m.get("content")
                    print "image:",image
                    result,imagesize = download_img(image,maxsz,image_file)
                    if result != "":
                        image_file = result
                    if imagesize != "":
                        maxsz = imagesize
                elif m.get("property") == "og:site_name":
                    site_name = m.get("content")

            print "--------------------"
            print image_file
            print "--------------------"

            
            if url.replace("\n","") in db_data:
                print "continue"
                continue

            if site_name == "":
                continue
            
            #データベース書き込み用ファイルにページ情報を書き込む
            str1 = "@page.title = \"" + title.encode("utf-8").replace("\"", "") + "\""
            str1 = str1.replace("\n", "")
            str1 += "\n"
            urls = url.replace("\n", "")

            uparticles[listNum] = {"title":str1,
                                   "url":urls,
                                   "image":image_file,
                                   "description":description.replace("\"", "").replace("\n", ""),
                                   "sitename":site_name.replace("\"", ""),
                                   "date":updt}
            
            print url
            count += 1
            listNum += 1
            time.sleep(1)

        except Exception as e:
            print e


    maxnum += len(uparticles)
    
    for k, v in sorted(uparticles.items()):
        wt.write("@page = Page.new\n")
        wt.write("@page.number = " + str(maxnum) + "\n")
        wt.write(v["title"])
        wt.write("@page.url = \"" + v["url"] + "\"\n")
        wt.write("@page.image = \"/images/" + v["image"] + "\"\n")
        wt.write("@page.body = \"" + v["description"].encode("utf-8") + "\"\n")
        wt.write("@page.site_name = \"" + v["sitename"].encode("utf-8") + "\"\n")
        wt.write("@page.date = \"" + v["date"].encode("utf-8") + "\"\n")
        wt.write("@page.save\n\n")
        maxnum -= 1


    f.close()
    wt.close()

if __name__ == "__main__":
    main()
