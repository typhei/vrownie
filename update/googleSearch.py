#-*- coding:utf-8 -*-
import urllib
import urllib2
import pprint
from bs4 import BeautifulSoup

#リクエストURL
URL = "https://www.google.co.jp/search?num=20&as_qdr=d&q="
AST = ["*", "**", "***", "****", "*****"]
KEYWORD = ["アダルト", "エロアニメ", "ポルノ", "巨乳", "アダルトビデオ", "セックス", "エロゲ", "美女", "美少女", "オナニー"]


class Google(object):
    def __init__(self, URL):
        self.url = URL
        self.agent = ("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0")

    def search(self, query):
        try:
            url = self.url + urllib.quote(query)
            opener = urllib2.build_opener()
            opener.addheaders = [self.agent]
            soup = BeautifulSoup(opener.open(url).read().decode("utf-8"))
            return soup
            
        except Exception as e:
            print e
            return ""

        
def main():
    f = open("urls", "w")
    google = Google(URL)
    for q in KEYWORD:
        term = "\"" + q + "\" \"VR\"" 
        result = google.search(term)
        result = result.find_all("div", class_="g")
        print "----------------------"
        print term
        print "----------------------"
        for i in result:
            try:
                atag = i.find("a")
                spantag = i.find("span", class_="st")
                print urllib.unquote(atag["href"].split("&")[0][7:])
                f.write(urllib.unquote(atag["href"].split("&")[0][7:]))
                f.write("\n")
                #print atag.text
                #print spantag.text
                #print "--------------"
            except Exception as e:
                print e
                pass
    f.close()
                
                
        
    

    
if __name__ == "__main__":
    main()
