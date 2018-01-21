#coding=utf-8
from lxml import etree
import requests
import random
from read_write_ini import read_ini, write_ini
from read_write_csv import read_write_csv

def random_proxy(namefile='ipList.csv'):
    """产生随机代理"""
    proxy_list = read_write_csv(
        name=namefile
    ).read_csv()
    proxy_index = proxy_list[random.randint(0,len(proxy_list) - 1)] # 随机选择一个列表
    if 'HTTPS' in proxy_index:
        http = 'https://%s' % proxy_index[0]
        proxy = 'https,%s' % http
        print('当前使用的代理ip为：%s' % http)
        write_ini(content=proxy)
    else:
        http = 'http://%s' % proxy_index[0]
        proxy = 'http,%s' % http
        print('当前使用的代理ip为：%s' % http)
        write_ini(content=proxy)


# noinspection PyShadowingNames
class ReadHtml:
    # noinspection PyShadowingNames
    def __init__(self, url=None, headers=None, my_encode='utf-8'):
        self.url = url
        self.headers = headers
        self.my_encode = my_encode # 编码

    def read_html(self):
        # noinspection PyBroadException
        def result_data():
            # noinspection PyBroadException
            try:
                r = requests.get(self.url,
                                 headers=self.headers,
                                 proxies={read_ini().split(',')[0]: read_ini().split(',')[1]},
                                 timeout=4,
                                 )
                r.encoding = self.my_encode
                if '有道' in r.text.split('content="')[1]:
                    random_proxy('ipList_2.csv')
                    return False
                elif r.status_code == 200:
                    tree = etree.HTML(
                        r.text,
                    )
                    return tree
                else:
                    random_proxy('ipList_2.csv')
                    return False
            except Exception:
                random_proxy('ipList_2.csv')
                return False
        result = result_data()
        if result is False:
            print('数据请求失败，再次请求。。。')
            for i in range(0, 1000):
                result = result_data()
                if result is not False:
                    print('数据再次请求成功')
                    return result
        else:
            return result
if __name__ == '__main__':
    url = 'http://baike.baidu.com/city/api/citylemmalist?type=8&cityId=173&offset=0&limit=100'
    get_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Referer': 'http://baike.baidu.com/city',
    }
    url_choose = ReadHtml(url=url, headers=get_headers).read_html()

