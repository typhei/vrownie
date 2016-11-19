# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re
import os
import sqlite3
import datetime

imagetype = ["png", "gif", "jpg", "jpeg"]
#####画像のダウンロード#####
def download_img(src,path,location):
    try:
        #URLから画像を取得
        filename ="unknown"
        i = urllib2.urlopen(src)
        if location == "/pornhub/":
            filename = "".join(src.split("/")[-3:])
        else:
            filename = src.split("/")[-1]
        print "downloading..."

        if os.path.isfile(path+filename):
            return location + filename

        if filename.split(".")[-1] not in imagetype:
            raise "Unknown image type Error"

        if os.path.isfile(path+filename) != True:
            #saveDataというバイナリデータを作成
            saveData = open(path + filename, "wb")

            #saveDataに取得した画像を書き込み
            saveData.write(i.read())
            saveData.close()

            print ">>>get:",filename


        return location + filename

    #ダウンロードできなかった場合は空文字列を返す
    except Exception as e:
        print e
        print ">>>error:", src
        return False


#############
#xvideos
#############
def pull_xvideo():
    #変数定義
    url = "http://www.xvideos.com/tags/vr/0/s:uploaddate/"
    retVar = []
    hostname = "http://www.xvideos.com"
    pattern = "\(\'.+\'\)"
    rep = re.compile(pattern)
    
    res = urllib2.urlopen(url)
    soup = BeautifulSoup(res.read())
    m = soup.find_all("div", class_="mozaique")[0]
    s = m.find_all("script")
    for i in s:
        matchOB = rep.search(str(i))
        htm = BeautifulSoup(matchOB.group()[2:-2])

        #画像ダウンロード#
        gotImage = download_img(htm.find("img").get("src").replace("THUMBNUM", "15"), "../public/xvideos/", "/xvideos/")
        if gotImage is not False:
            img = gotImage
        else:
            img = "sample.jpg"

        #動画のリンク・タイトル取得#
        if htm.find("div", class_="thumb-inside") is not None:
            tag = htm.find("p").find("a")
            link = hostname + tag.get("href")
            title = tag.get("title")
        else:
            link = hostname + htm.find("a").get("href")
            title = htm.find("a").get("href").split("/")[-1]

            
        retVar.append({"title":title.replace("\n", "").replace("\"", "").encode("utf-8"), "url":link.replace("\n", ""), "image":img.replace("\n", "").encode("utf-8"), "sitename":"XVIDEOS.COM"})
        
    return retVar


###########
#AdultFesta
###########
def adultFesta():
    #変数定義
    url = "http://www.afesta.tv/vr/index.php?pid=&fid=&cid=&cat=&m_cat=10&word=&s_type=&r_type=1&x=63&y=34"
    hostname = "http://www.afesta.tv/vr/"
    retVar = []

    res = urllib2.urlopen(url)
    soup = BeautifulSoup(res.read())
    m = soup.find("div", id="contents_new")
    videos = m.find_all("div", class_="vrcol")
    for i in videos:
        gotImage = download_img(i.find("div", class_="thumb").find("img").get("src"), "../public/adultfesta/", "/adultfesta/")
        if gotImage is not False:
            img = gotImage
        else:
            img = "sample.jpg"
            
        atag = i.find("div", class_="ttl").find("a")
        link = hostname + atag.get("href")[2:].replace("\n", "")
        title = atag.text.replace("\n", "").replace("\"", "").encode("utf-8")

        retVar.append({"title":title, "url":link, "image":img.replace("\n", "").encode("utf-8"), "sitename":"Adult festa VR"})

    return retVar


def pornhub():
    url = "http://jp.pornhub.com/vr?o=cm"
    retVar = []

    res = urllib2.urlopen(url)
    soup = BeautifulSoup(res.read())
    m = soup.find("ul", class_="search-video-thumbs")
    s = m.find_all("li", class_="videoblock videoBox")
    for i in s:
        gotImage = download_img(i.find("img").get("data-mediumthumb"), "../public/pornhub/", "/pornhub/")
        if gotImage is not False:
            img = gotImage
        else:
            img = "sample.jpg"

        span = i.find("span", class_="title")
        link = "http://jp.pornhub.com" + span.find("a").get("href")
        title = span.find("a").get("title")

        retVar.append({"title":title, "url":link, "image":img.replace("\n", "").encode("utf-8"), "sitename":"Pornhub"})

    return retVar


    
def main():
    new_videos = []
    wt = open("../db/seeds.rb", "w")
    wt.write("#coding:utf-8\n")
    today = datetime.datetime.today()

    #db参照
    cur = sqlite3.connect("../db/development.sqlite3").cursor()
    inDatabase = list(cur.execute("select url from videos;"))
    inDatabase = [x[0] for x in inDatabase]

    
    new_videos.extend(pull_xvideo())
    new_videos.extend(adultFesta())
    new_videos.extend(pornhub())
    
    for video in new_videos:
        if video["url"] in inDatabase:
            continue
        
        wt.write("@video = Video.new\n")
        wt.write("@video.title = \"" + video["title"] + "\"\n")
        wt.write("@video.url = \"" + video["url"].encode("utf-8") + "\"\n")
        wt.write("@video.image = \"" + video["image"] + "\"\n")
        wt.write("@video.site_name = \"" + video["sitename"] + "\"\n")
        wt.write("@video.Date = \"" + today.strftime("%Y%m%d") + "\"\n")
        wt.write("@video.save\n\n")



if __name__ == "__main__":
    main()
