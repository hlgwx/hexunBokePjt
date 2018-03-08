# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request

class MyhexunspdSpider(scrapy.Spider):
    name = 'myhexunspd'
    allowed_domains = ['hexun.com']
    uid="fjrs168"
    def start_requests(self):
        yield Request("http://"+str(self.uid)+".blog.hexun.com/p1/default.html",
                      headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.4 Safari/537.36"})
    def parse(self, response):
        item=HexunpjtItem()
        item["name"]=response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item["url"]=response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        #提取存储评论数和点击数网址正则表达式
        pat1='<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        hcurl=re.compile(pat1).findall(str(response.body))[0]
        headers2=('User-Agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.4 Safari/537.36")
        opener=urllib.request.build_opener()
        opener.addheaders=[headers2]
        #将opener安装为全局
        urllib.request.install_opener(opener)
        #data为对应博客列表页所有博文的点击数与评论数数据
        data=urllib.request.urlopen(hcurl).read()
        #pat2提取文章阅读数的正则表达式
        pat2="'click\d*?','(\d*?)'"
        #pat3提取文章评论数的正则表达式shi2
        pat3="'comment\d*?','(\d*?)'"
        item["hits"]=re.compile(pat2).findall(str(data))
        item["comment"] = re.compile(pat3).findall(str(data))
        yield item
        pat4="blog.hexun.com/p(.*?)/"
        #通过正则表达式获取到的数据为一个列表，倒数第二个元素为总页数
        data2=re.compile(pat4).findall(str(response.body))
        if(len(data2)>=2):
            totalurl=data2[-2]
        else:
            totalurl=1
        #print("一共"+str(totalurl)+"页")
        for i in range(2,int(totalurl)+1):
            print("当前第" + str(i) + "页")
            nexturl="http://"+str(self.uid)+".blog.hexun.com/p"+str(i)+"/default.html"
            yield Request(nexturl,callback=self.parse,headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.4 Safari/537.36"})

