#-*- coding:utf-8 -*-
from google import search
from bs4 import BeautifulSoup
import urllib

def main():
    for url in search("VR", stop=20 ,lang="ja"):
        soup = BeautifulSoup(urllib.urlopen(url))
        for i in soup.find_all("div" ,class_="g"):
            try:
                atag = i.find("a")
                print urllib.unquote(atag["href"].split("&")[0][7:])
            except Exception as e:
                print e
                pass
                
if __name__ == "__main__":
    main()
