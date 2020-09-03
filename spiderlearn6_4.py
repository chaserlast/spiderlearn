import requests
from urllib.parse import urlencode
# from pyquery import PyQuery as pq
import os
from hashlib import md5
from multiprocessing.pool import Pool

base_url = 'https://www.toutiao.com/api/search/content/?'
headers = {
    'cookie': '',
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

#获取json
def get_page(offset):
    params = {
        'offset': offset,
        'aid': '24',
        'app_name': 'web_search',
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd':'synthesis'
    }

    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers = headers)         #response = requests.get(url,params = params,headers = headers)也可以
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('error',e.args())

#解析json
def parse_page(json):
    if json.get('data'):
        # items = json.get('data')
        #
        # for item in items:
            # if item.get('title'):
            #     title = item.get('title')
            #     #toutiao['arcticle_url'] = item.get('arcticle_url')
            #     for image in item.get('image_list'):              #这种写法的问题是如果image_list不存在，是None类型，那么就无法迭代
            #         url = image.get('url')
            #         yield {
            #             'url': url,
            #             'title': title
            #
            #         }


            # else:
            #     print('无图，下一个')

        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images:
                for image in images:
                    yield {'image': image.get('url'),
                           'title': title
                           }
            else:
                print('跳过')



# 过滤title里不合法的字符
def correct_name(title):

    error_set = ('/', '\\', ':', '*', '?', '"', '|', '<', '>', '.')                       #文件名中不能包含的非法字符
    for c in title:                                                          # title是字符串，属于iterable
        if c in error_set:
            title = title.replace(c,'')
    return title
#保存图片
def save_images(item):
    dir_name = 'image/' + correct_name(item.get('title'))
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)                                            #生成与title同名的文件夹

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(dir_name,md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)                                                       #向文件夹内写入文件
            else:
                print('already download',file_path)
    except requests.ConnectionError:
        print('Fail to save image')


def main(offset):
    json = get_page(offset)
    results = parse_page(json)

    for result in results:
        print(result)
        save_images(result)





if __name__ == '__main__':
    GROUP_START = 1
    GROUP_END = 20
    pool = Pool()

    group = ([x *20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,group)
    pool.close()                                                                           #多线程下载
    pool.join()
    # for i in range(0, 6):
    #     print("第"+str(i+1)+"页开始下载！！！")
    #     offset = i * 20
    #     main(offset)
