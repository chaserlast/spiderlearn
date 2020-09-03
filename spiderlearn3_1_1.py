#学习urllib库
#使用urlopen函数
# import urllib.request
# response = urllib.request.urlopen('https://www.python.org/')
# print(response.getheader('server'))


#使用Request函数
# import urllib.request
# request = urllib.request.Request('https://www.python.org/')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))


#使用request类构造更加灵活的请求
# from urllib import parse,request
# url = 'http://httpbin.org/post '
# dict = {
#     'name': 'gemey'
# }
# head = {
#     'user-agent':'Mozilla/4.0  (compatible;  MSIE  S. S;  Windows  NT)',
#     'host':'httpbin.org'
# }
# data = bytes(parse.urlencode(dict),encoding='utf-8')
# response = request.Request(url=url,data = data,headers = head,method = 'POST')
# res = request.urlopen(response)
# print(res.read().decode('utf-8'))



#借助HTTPBasicAuthHandler请求验证页面
# from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
# from urllib.error import URLError
# username = 'username'
# password = 'password'
# url = 'http://localhost:5000/'
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None,url,username,password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)




#借助ProxyHandler搭建一个本地的代理
# from urllib.request import ProxyHandler,build_opener
# from urllib.error import URLError
#
# proxy = ProxyHandler({
#     'http':'http://127.0.0.1:9743',
#     'https':'http://127.0.0.1:9743',
# })
# opener = build_opener(proxy)
#
# try:
#     result = opener.open('https://www.baidu.com/')
#     print(result.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)



#借助HTTPCookieProcessor获取网站的cookie
# import http.cookiejar,urllib.request
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# result = opener.open('https://www.baidu.com/')
# for item in cookie:
#     print(item.name+"="+item.value)
