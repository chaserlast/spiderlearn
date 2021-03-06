import requests
from urllib.parse import urlencode
from pyquery import  PyQuery as pq
import pymysql

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
        'host':'m.weibo.cn',
        'Referer': 'https://m.weibo.cn/u/2830678474',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'X - Requested - With': 'XMLHttpRequest'
    }

def get_page(since_id):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474'            # containerid数值错误，看看什么情况
                                                     # 前面的getindex是1005052830678474，后面是1076032830678474，前面是什么意思
    }
    if since_id!=0:
        params['since_id'] = since_id

    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('error',e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibom = {}
            weibom['id'] = item.get('id')
            weibom['text'] = pq(item.get('text')).text()
            weibom['attitudes'] = item.get('attutudes_count')
            weibom['comments'] = item.get('comments_count')
            weibom['reposts'] = item.get('reposts_count')
            yield weibom


if __name__ == '__main__':
    since_id = 0
    db = pymysql.connect(host='127.0.0.1',user='root',passwd='mysql',port = 3306,db='spider')
    cur = db.cursor()

    for page in range(1,10+1):
        json = get_page(since_id)
        since_id = json.get('data').get('cardlistInfo').get('since_id')
        results = parse_page(json)

        for result in results:
            # print(type(result))
            # with open('results.txt','a',encoding='utf-8') as f:
            #     f.write(str(result) + '\n')
            cur.execute('insert into weibo (id,text,attitudes,comments,reposts) value(%s,%s,%s,%s,%s)',(result['id'],result['text'],result['attitudes'],result['comments'],result['reposts']) )
            db.commit()

    db.close()

