# coding: utf-8
require "rubygems"
require "net/http"
require "uri"
require "json"
require "pp"
require "cgi"

#パラメータ準備
API_KEY = "AIzaSyDWj0oLZ9E3FCz52wuP9ORo1JDTe2T96gw"
CSE_KEY = "017109665700922583163:vg4jfedf4li"
QUERIES = ["アダルト", "エロアニメ", "ポルノ", "巨乳", "アダルトビデオ", "セックス", "エロゲ", "美女", "美少女", "オナニー","おっぱい", "エッチ"]
Number = 1
Resnum = 10
file = File.open("urls", "w")
uArray = []

QUERIES.each do |q|
  
  #クエリ生成
  query = CGI.escape("VR" + q);

  #検索ワードごとに検索
  for i in 0..Number
    start = i * 10 + 1
    p start
    puts "start:" + start.to_s

    #APIリクエスト
    api_url = URI.parse("https://www.googleapis.com/customsearch/v1?key=#{API_KEY}&cx=#{CSE_KEY}&q=#{query}&num=#{Resnum}&start=#{start}&dateRestrict=w1")
    https = Net::HTTP.new(api_url.host, api_url.port)
    https.use_ssl = true
    res = https.start{
      https.get(api_url.request_uri)
    }

    p api_url
    #レスポンス成功
    if res.code == "200"
      puts "code:200"

      #json処理
      result = JSON.parse(res.body)
      if result != nil and result["items"] != nil 
        result["items"].each do |tag|
          tag.each do |fac|
            if fac[0] == "link" #url部分
              uArray.push(fac[1])
              puts fac[1]
            end
          end
        end

      #検索結果がない場合
      else
        puts "NIL"
      end

    #レスポンス失敗
    else
      puts "#{res.code} #{res.message}"
      sleep(10)
    end
    
  end
  
end

#重複しているURLを除去
neuArray = uArray.uniq

#ファイルurlsに書き込み
neuArray.each do |url|
  file.puts(url)
end
