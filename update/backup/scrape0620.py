# -*- coding:utf-8 -*-
import urllib2
import time
import os
from bs4 import BeautifulSoup
from PIL import Image
import unicodedata
import math
import sqlite3
path = "../app/assets/images/"
imagetype = ["png", "gif", "jpg", "jpeg"]

def download_img(src, max_size, current, location):
    try:
        #URLから画像を取得
        i = urllib2.urlopen(src)
        filename = src.split("/")[-1]

        if os.path.isfile(path+filename):
            return "",""

        if filename.split(".")[-1] not in imagetype:
            raise "Unknown image type Error"

        #saveDataというバイナリデータを作成
        saveData = open(path + filename, "wb")

        #saveDataに取得した画像を書き込み
        saveData.write(i.read())
        saveData.close()

        print ">>>get:", filename

        
        #今取得した画像の解像度計算
        kaizoudo = Image.open(path+filename).size
#        minhen = min(kaizoudo[0], kaizoudo[1])
        newsize = (kaizoudo[0] * kaizoudo[1])*1.0 / location * 1.0

        #この画像が今までの最大画像より大きければ交換する
        if newsize > max_size:
            if current != "":
                os.remove(path+current)
                print "-----removed:", current, "---------"
            return filename, newsize
        #そうでなければ空文字列を返す
        else:
            os.remove(path+filename)
            return "",""

    #ダウンロードできなかった場合は空文字列を返す
    except Exception as e:
        print e
        print ">>>error:", src
        return "", ""



def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
        return False
    
        

def main():
    
    #選別したURLの書き込み先ファイル
    f = open("sorted_URL")
    #railsのデータベース書き込み用ファイル
    wt = open("../db/seeds.rb", "a")
    wt.write("#coding: utf-8\n")

    num = 1
    
    for url in f:
        try:
            #ページを読み込み．テキスト部分とimgタグを収集
            res = urllib2.urlopen(url)
            html = res.read()
            soup = BeautifulSoup(html)
            images = soup.body.find_all("img")
            maxsz = 0
            image_file = ""
            
            print url
            
            #本文取得
            #div,p
#            explain = ""
#            maxcore = 0
#            ptag = soup.find_all("p")
#            spantag = soup.find_all("span")
#            litag = soup.find_all("li")
#            med = (len(ptag)+len(spantag)+len(litag))/2


            
#            for i, p in enumerate(ptag):
#                sen = p.text.replace(" ","").replace("\n","")
#                score = len(sen)*1.0 / (abs(med-i)+1)*1.0
#                if is_japanese(sen) and score > maxcore:
#                    explain = sen
#                    maxcore = score
#                    
#            for i, sp in enumerate(spantag):
#                sen = sp.text.replace(" ","").replace("\n", "")
#                score = len(sen)*1.0 / (abs(med-i)+1)*1.0
#                if is_japanese(sen) and score > maxcore:
#                    explain = sen
#                    maxcore = score
#
#            for i, li in enumerate(litag):
#                sen = li.text.replace(" ","").replace("\n", "")
#                score = len(sen)*1.0 / (abs(med-i)+1)*1.0
#                if is_japanese(sen) and len(sen) > len(explain):
#                    explain = sen
#                    
#            explain = explain[0:100].replace("\"", "") + "..."


            #ページ中の全画像から最大のものを選ぶ
#            medimg = len(images)/2
#            for idx, img in enumerate(images):
#                imgscore = abs(medimg-idx)+1
#                useimage, imagesize = download_img(img.get("src"), maxsz, image_file, imgscore)
#                if useimage != "":
#                    image_file  = useimage
#                if imagesize != "":
#                    maxsz = imagesize#

#            #画像が含まれないページはサンプル画像を使用する        
#            if image_file == "":
#                image_file = "sample"


            
            #データベース書き込み用ファイルにページ情報を書き込む
            str1 = "@page.title = \"" + soup.title.text.encode("utf-8") + "\""
            str1 = str1.replace("\n", "")
            str1 += "\n"
            urls = url.replace("\n", "")
            print url
            wt.write("@page = Page.new\n")
            wt.write("@page.number = " + str(num) + "\n")
            wt.write(str1)
            wt.write("@page.url = \"" + urls + "\"\n")
            wt.write("@page.image = \"/assets/" + image_file + "\"\n")
            wt.write("@page.body = \"" + explain.encode("utf-8") + "\"\n")
            wt.write("@page.save\n\n")
            num+=1
            time.sleep(1)
            if num > 10:
                break

        #エラー処理
        except Exception as e:
            print e

    f.close()
    wt.close()

if __name__ == "__main__":
    main()
