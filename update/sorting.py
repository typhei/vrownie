# -*- coding:utf-8 -*-
import urllib2
import time
from bs4 import BeautifulSoup
import chardet
import math
#path = "adultVR/app/assets/images/"


        
Terms = [u"アダルト", u"エロアニメ", u"ポルノ", u"巨乳", u"アダルトビデオ", u"セックス", u"エロゲ", u"美女", u"美少女", u"オナニー", u"おっぱい",u"エッチ"  u"VR", u"漫画", u"同人"]


#ページのエンコーディングチェック
def conv_encoding(data):
    lookup = ["iso-2022-jp", "euc-jp", "euc-jisx0213", "euc-jis-2004",
              "iso-2022-jp-1", "iso-2022-jp-2", "iso-2022-jp-3",
              "iso-2022-jp-ext", "iso-2022-jp-2004", "utf-7",
              "utf-8", "utf-16", "utf-16-be", "utf-16-le",
              "cp932", "shift-jis", "shift-jisx0213", "shift-jis-2004",
              "hz-gb-2312","Big5-HKSCS","ascii"]
    encode = None
    for encoding in lookup:
        try:
            data = data.decode(encoding)
            encode = encoding
            break
        except:
            pass
    return encode


        
                
#取得したウェブページをVRに関連の強い順番にソート
def main():

    #urlファイル
    f = open("urls")
    #ソート後のファイル
    wt = open("sorted_URL", "w")
    num = 1
    termaverage,ranking = {},{}
    
    for u in f:
        try:
            print u
            url = u
            title, description, image,types  = "", "", "",""
            
            if u"http" not in url:
                url = u"http://" + url
            html = urllib2.urlopen(url).read()

            #文字コード判定・Unicodeに変換
            code = conv_encoding(html)
            if code is None:
                raise "No Encoding Error"

            #ページをBSで処理
            bfs = BeautifulSoup(html)
            soup = bfs.text.replace(" ", "").replace("\n", "")

            #OGP設定取得
            meta = bfs.find_all("meta")

            for m in meta:
                if m.get("property") is not None:
                    if m.get("property") == "og:title":
                        title = m.get("content")
                    elif m.get("property") == "og:description":
                        description = m.get("content")
                    elif m.get("property") == "og:image":
                        image = m.get("content")
                    elif m.get("property") == "og:type":
                        types = m.get("content")


            if title == "" or image == "" or types == "":
                continue

            if u"漫画" in title or u"同人" in title:
                continue
            if types != "article":
                continue

            #テキストのみ抽出
            print "タイトル：",title
            if u"VR" not in soup:
                continue
            
            textlen = math.log(len(soup))

            #リンク数、画像数
            numlinks = math.log(len(bfs.find_all("a")))
            numofimg = math.log(len(bfs.find_all("img")))



            termaverage[url] = []
            #termaverage[url].append(numlinks)
            #termaverage[url].append(numofimg)

            print "count"
            #対象文字列カウント
            for i in Terms:
                if i in soup:
                    if i == u"漫画" or i == u"同人":
                        termaverage[url].append(1.0 / soup.count(i) * 1.0)
                    else:
                        termaverage[url].append(soup.count(i)*1.0 / textlen * 1.0)
                else:
                    termaverage[url].append(0.5 / textlen * 1.0)

            if u"VR" in title:
                termaverage[url] = [x*2 for x in termaverage[url]]

            print "end?"
                
        #エラー処理
        except Exception as e:
            print "error"
            print e

    for k, v in termaverage.items():
        geometric_ave = pow(reduce(lambda x, y:x*y, v), (1.0/len(v)))
        ranking[k] = geometric_ave

    writeNum = 0
    for k, v in sorted(ranking.items(), key=lambda x:x[1],reverse=True):
        if writeNum > 10:
            break
        print k,v
        wt.write(k)
        writeNum += 1
        
    f.close()
    wt.close()

if __name__ == "__main__":
    main()
