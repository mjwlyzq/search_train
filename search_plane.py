#coding=utf-8
import requests
import plane_data
import re
import time
import datetime
import random
import json
import pygame
from time import sleep
from read_lxml import ReadHtml
from read_lxml import random_proxy
from read_write_ini import read_ini


class CheckPlane:
    def __init__(self, from_station, to_station, search_data, *kwargs):
        self.url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights'
        self.mp3_path = 'http://boscdn.bpc.baidu.com/v1/developer/531697ca-2e4e-4998-90dc-16007fd33357.mp3'
        self.search_data = search_data # 查询日期
        self.from_station = from_station # 起始站
        self.to_station = to_station # 到达站
        self.city_info_dict = {}  # 以字典列表的形式存储城市和codes值
        self.plane_info_list = [] # 机票信息列表
        self.conditions_list = [] # 条件查询后的列表
        self.timing = kwargs
        def data_pressing():
            data = plane_data.__doc__.split('suggestion=')[1][:-1][7:][:-3]
            data_pro = data.split('{')
            initialize_list = [] # 没有处理的城市数据
            city_info_list = [] # 城市信息列表
            for info in data_pro:
                city_info = info.replace('"','').replace('display:','').replace('data:','')[:-1]
                name = city_info.split(',')
                if name[0] != '' and ':' not in name[0]:
                    initialize_list.append(name)
            for i in initialize_list:
                city_dict = {
                    i[0]: i[1].split('(')[1].split(')')[0]
                }
                city_info_list.append(city_dict)
            for k in city_info_list: # 组合成长字典
                self.city_info_dict.update(k)
        data_pressing() # 获取个城市对应code值
        self.main_url = 'http://flights.ctrip.com/booking/{}-{}-day-1.html?DDate1={}'.format(self.city_info_dict[self.from_station],self.city_info_dict[self.to_station],self.search_data)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3194.4 Safari/537.36',
            'Referer': self.main_url,
        }
        print(print('可直接复制此地址在浏览器中打开查看:%s' % self.main_url))

    # noinspection PyShadowingNames,PyShadowingNames
    def get_param(self):
        """获得重要参数"""
        def my_param(tree):
            """解析数据"""
            pp = tree.xpath('''//body/script[1]/text()''')[0].split()
            CK_original = pp[3][-34:-2]
            CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]
            rk = pp[-1][18:24]
            num = random.random() * 10
            num_str = "%.15f" % num
            rk = num_str + rk
            r = pp[-1][27:len(pp[-1]) - 3]
            LogToken = pp[3].split('LogToken=')[1][:32]
            return LogToken, rk, CK, r

        # print('开始请求数据')
        result = ReadHtml(self.main_url,headers=self.headers).read_html()
        if result is False:
            print('数据请求失败，再次请求。。。')
            for i in range(0, 1000):
                result = ReadHtml(self.main_url,headers=self.headers).read_html()
                if result is not False:
                    print('数据再次请求成功')
                    return my_param(result)
        else:
            return my_param(result)

    # noinspection PyShadowingNames,PyShadowingNames
    def check_plane(self):
        """数据查询"""
        parme = self.get_param()

        # noinspection PyBroadException
        def get_data():
            """数据请求"""
            payload = {
                'DCity1': self.city_info_dict[self.from_station],
                'ACity1': self.city_info_dict[self.to_station],
                'SearchType': 'S',
                'DDate1': self.search_data,
                'IsNearAirportRecommond': 0,
                'LogToken': parme[0],
                'rk': parme[1],
                'CK': parme[2],
                'r': parme[3],
            }
            try:
                r = requests.get(
                    url=self.url,
                    headers=self.headers,
                    proxies={read_ini().split(',')[0]: read_ini().split(',')[1]},
                    params=payload,
                )
                if r.json()['Error'] is None:
                    result_data = r.json()
                    return result_data
                elif r.json()['Code'] == 1004:
                    return 1004
                else:
                    return -1
            except Exception:
                random_proxy('ipList_2.csv')
                return False
        result = get_data()
        if result == 1004 or result is False:
            print('数据请求失败，再次请求。。。')
            for i in range(0, 1000):
                result = get_data()
                if result is not False:
                    print('数据再次请求成功')
                    return result
        elif result == -1:
            print('不通航')
        else:
            return result

    # noinspection PyShadowingNames
    def data_analysis(self):
        """数据分析"""
        result = self.check_plane() # 获得数据
        #print(result)
        als = result['als'] # 航空公司名称
        fn = result['fis'] # 每个航空公司的信息
        for i in fn:
            flane_city = {
                'alc': als[i['alc']], # 所属航空公司
                'fn': i['fn'], # 飞机编号
                'dt': i['dt'][:-3], # 起飞时间
                'at': i['at'][:-3], # 到达时间
                'dpbn': i['dpbn'], # 起飞机场
                'apbn': i['apbn'], # 到达机场
                'HistoryPunctualityArr': json.loads(i['confort'])['HistoryPunctualityArr'], # 准点率
                'p': i['scs'][0]['p'], # 最低价格
                'rt':  i['scs'][0]['rt'], # 打折
            }
            self.plane_info_list.append(flane_city)

    def play_mp3(self):
        """播放音乐"""
        pygame.mixer.init()
        print("播放音乐")
        pygame.mixer.music.load('plane.mp3')
        pygame.mixer.music.play(loops=1)
        time.sleep(2)
        pygame.mixer.music.stop()

    def my_timing(self):
        """定时任务"""
        k = 0
        if self.timing[2]['f'] is False:
            self.data_analysis()  # 解析数据
            return self.plane_info_list
        else:
            system_data = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())) # 当前系统时间
            d1 = datetime.datetime.strptime(system_data, '%Y-%m-%d %H-%M-%S')
            current_data = float(d1.minute) + float(self.timing[0])
            while k == 0:
                self.data_analysis() # 解析数据
                for i in self.plane_info_list:
                    if float(i['p']) <= float(self.timing[1]):
                        self.conditions_list.append(i)
                if self.conditions_list:
                    self.play_mp3() # 播放音乐
                    return self.conditions_list
                else:
                    a_data = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))  # 当前系统时间
                    d2 = datetime.datetime.strptime(a_data, '%Y-%m-%d %H-%M-%S')
                    d2_data = float(d2.minute)
                    if d2_data >= current_data:
                        break
                    sleep(random.randint(1,5))
                    print('正在查询价格低于%s元的%s飞往%s的飞机票,定时%s分钟' % (self.timing[1],self.from_station,self.to_station,self.timing[0]))






if __name__ == '__main__':
    data = {'f': False}
    CheckPlane('北京','成都','2018-01-24',0,9,data).play_mp3()
