#! python3
# _*_ coding: utf-8 _*_

# ------------------------------
# 房天下（石家庄）2017 开盘房 爬虫
# 2016-12-03 14:04:44
# ------------------------------
# alias py=python3 切换版本
# https://www.zhihu.com/question/21653286

import requests
import re
from bs4 import BeautifulSoup
import os

domain = "http://newhouse.sjz.fang.com"
urls = [
    "http://newhouse.sjz.fang.com/house/saledate/201610.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201611.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201612.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201701.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201702.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201703.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201704.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201705.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201706.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201707.htm",
    "http://newhouse.sjz.fang.com/house/saledate/201708.htm"
]

# # 匹配Element节点代码块儿
# p = re.compile('<div class="listArea" style="width:900px;">(.*?)</div>', re.S)
# # 精确匹配信息
# p = re.compile('target="_blank" class="floatl w130">(.*?)</a>', re.S)
# datas = re.findall(p, page)
# print ('编码' + response.encoding + response.apparent_encoding)
# print ("=====================")
# print (datas)
# name=os.path.basename(url)
# with open(name,'wb') as jsname:
#     jsname.write('datas.toString')


def findHouses (time, soup):
    houses = []
    # 查找
    # 查找页面房子
    for item in soup.select(".listArea > .clearfix > li"):

        name = item.select('a[class="floatl w130"]')[0].string
        houseTypeChild = item.select(".imgInfo > p")[0]
        houseType = ''

        for child in houseTypeChild:
            houseType += child.string

        area = item.select('span[class="floatr"]')[0].string
        price = item.select('.price > span')[0].string
        houseType = houseType.replace(' ', '').replace('\n', '').replace('\t', '')

        # if len(houses) != 0:
        # houses += '\n'
        houses.append(
            {
                'time': time,
                'area': area,
                'name': name,
                'houseType': houseType,
                'price': price
            }
        )

    return houses

def getPageSource (url):
    print ('获取网页源码 ' + url)
    response = requests.get(url)

    # 解决乱码 http://sh3ll.me/2014/06/18/python-requests-encoding/
    response.encoding =  response.apparent_encoding
    page = response.text
    soup = BeautifulSoup(page, "html.parser")
    return soup

def has_href_but_no_class(tag):
    return tag.has_attr('href') and not tag.has_attr('class')

def getPagingUrl(soup):
    urls = []
    pagingViews = soup.select(".page > .clearfix > .floatr")
    if len(pagingViews) >= 1:
        floatr = pagingViews[0]
        if len(floatr.contents) >= 1:
            _as = floatr.find_all(has_href_but_no_class)
            for a in _as:
                urls.append(a['href'])

    return urls


def readPage (url):
    soup = getPageSource(url)
    time = os.path.basename(url)
    print ('reading... ' + time)
    houses = findHouses(time, soup)
    pagingUrls = getPagingUrl(soup)

    for pageUrl in pagingUrls:
        soup = getPageSource(domain + pageUrl)
        houses += findHouses(time, soup)

    return houses

houses = []

for url in urls:
    houses += readPage(url)

print (len(houses))

# 保存到文件
houses = '// 自动生成\n' + 'var houses = ' + str(houses)
with open('./docs/js/houses.js','wb') as jsname:
    jsname.write(bytes(houses, 'UTF-8'))
