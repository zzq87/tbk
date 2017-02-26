#!/usr/bin/python3
# *-* coding:utf-8 *-*
import requests
import json
import sqlite3
import datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)/'
                      'Chrome/55.0.2883.75 Safari/537.36'
    }
with sqlite3.connect('tbk.db') as con:
    cur = con.cursor()

    def creat_tab():
        cur.execute('create table tbk(id integer primary key autoincrement,title varchar,\
        shopTitle text,auctionId varchar,zkPrice FLOAT,eventRate FLOAT,tkCommFee FLOAT,dayLeft int,couponAmount int,\
        endTime varchar,couponInfo varchar,auctionUrl text,pictUrl text)')
    
    '''条目ID，商品标题，店铺名称，商品ID，折扣价格，佣金比例，利润金额，剩余天数，优惠券面额，优惠券有效期，优惠券信息'''

    def catch_json():
        for p in range(1, 101):
            try:
                print(p)
                r = requests.get('''http://pub.alimama.com/items/channel/qqhd.json?channel=qqhd&toPage={}&\
dpyhq=1&perPageSize=100&shopTag=dpyhq'''.format(p), headers=headers).text
                dj = json.loads(r)['data']['pageList']
                for i in dj:
                    title = str(i['title'])  #商品标题
                    shopTitle = str(i['shopTitle'])  #店铺名称
                    auctionId = str(i['auctionId'])  #商品ID
                    zkPrice = float(i['zkPrice'])  #折扣价格
                    eventRate = float(i['eventRate'])  #佣金比例
                    tkCommFee = float(i['tkCommFee'])  #利润金额
                    dayLeft = int(i['dayLeft'])  #剩余天数
                    couponAmount = int(i['couponAmount'])  #优惠券面额
                    endTime = str(i['couponEffectiveEndTime'])  #优惠券有效期
                    couponinfo = str(i['couponInfo'])  #优惠券信息
                    auctionUrl = str(i['auctionUrl'])  #宝贝链接
                    pictUrl = str(i['pictUrl'])  #主图链接
                    cur.execute("insert into tbk(id,title,shopTitle,auctionId,zkPrice,eventRate,tkCommFee,dayLeft,\
                    couponAmount,endTime, couponInfo,auctionUrl,pictUrl)values(null,'{}','{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}')".format(title.replace("'", ''), shopTitle.replace("'", '-'),
            auctionId, zkPrice, eventRate, tkCommFee, dayLeft, couponAmount, endTime, couponinfo, auctionUrl, pictUrl))
                con.commit()
            except requests.exceptions as e:
                print('requests.exceptions', e)

    def l():
        cur.execute('select id,title,shopTitle,zkPrice,eventRate,tkCommFee,couponinfo from tbk where \
        eventRate>45 and zkPrice < 20')
        d = cur.fetchall()
        for i in d:
            if '女' in i[1]:
                print(i)

    #creat_tab()
    #catch_json()
    l()
