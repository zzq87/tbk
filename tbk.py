import requests
import json
import sqlite3

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)/'
                      'Chrome/55.0.2883.75 Safari/537.36'
    }
with sqlite3.connect('tbk.db') as con:
    cur = con.cursor()
    cur.execute('create table tbk(id integer primary key autoincrement,title varchar,\
    auctionId varchar,zkPrice int,couponAmount int,couponInfo varchar)')
    def catch_json():
        for i in range(10):
            print(i)
            r = requests.get('''http://pub.alimama.com/items/channel/qqhd.json?channel=qqhd&toPage={}&dpyhq=1
                     &perPageSize=40&shopTag=dpyhq'''.format(i), headers=headers).text
            dj = json.loads(r)['data']['pageList']
            for i in dj:
                title = str(i['title'])
                auctionId = str(i['auctionId'])
                zkPrice = int(i['zkPrice'])
                couponAmount = int(i['couponAmount'])
                couponinfo = str(i['couponInfo'])
                cur.execute("insert into tbk(id,title,auctionId,zkPrice,couponAmount,couponInfo)values(null,'{}','{}','{}','{}','{}')".format(title.replace("'", ''), auctionId, zkPrice, couponAmount, couponinfo))
            con.commit()

    def l():
        cur.execute('select * from tbk where couponAmount > 10 and zkPrice < 50 ')
        d = cur.fetchall()
        for i in d:
            print(i)
    catch_json()
    l()