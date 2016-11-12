#coding:utf-8
import urllib2
from bs4 import BeautifulSoup

def main():
    #変数定義
    url = "http://www.afesta.tv/vr/index.php?pid=&fid=&cid=&cat=&m_cat=10&word=&s_type=&r_type=1&x=63&y=34"
    hostname = "http://www.afesta.tv/vr/"
    retVar = []

    res = urllib2.urlopen(url)
    soup = BeautifulSoup(res.read())
    m = soup.find("div", id="contents_new")
    videos = m.find_all("div", class_="vrcol")
    for i in videos:
        print i.find("div", class_="thumb").find("img").get("src")
        atag = i.find("div", class_="ttl").find("a")
        print atag.get("href")
        print atag.text
        print "-----------------------------"
    


    
if __name__ == "__main__":
    main()
