
import requests
import re
import json
import time
from requests.exceptions import RequestException
#发送请求获取信息
def get_one_page(url):
    try:
        headers = {
            'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"

        }

        response = requests.get(url,headers = headers)     #学习实战怎么设置请求头
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#解析内容
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?'
        'integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items = re.findall(pattern,html)

    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score':item[5].strip() + item[6].strip()
        }

#写入文件
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii = False) + '\n')


#分页爬取
def main(offset):

    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(1)


