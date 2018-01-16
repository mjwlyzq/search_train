#coding=utf-8
import requests
import time
import datetime
import re
from read_lxml import random_proxy
from read_write_ini import read_ini, write_ini
from data_12306 import data_12306

class CheckTicket:
    def __init__(self, start_city, end_city, search_data, species):
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3194.4 Safari/537.36',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        }
        self.station_list = [] # 车站代号列表
        self.train_info_list = [] # 火车各车次信息
        self.screening_list = [] # 经过条件筛选后的车次信息
        def data_processing():
            data = data_12306.split('@')
            del data[0]  # 删除下标为0的元素，即删除第一个空字符串
            for station in data:
                name = station.split('|')[1]
                codes = station.split('|')[2]
                station_info = {
                    'name': name,
                    'code': codes,
                }
                self.station_list.append(station_info)
        data_processing()
        time1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", search_data) # 正则匹配日期的两种情况
        if time1 is not None:
            search_data = time1.group(0)
            current_data = time.strftime('%Y-%m-%d', time.localtime(time.time())) # 当前系统日期
            d1 = datetime.datetime.strptime(current_data, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(search_data, '%Y-%m-%d')
            if d2.year == d1.year: # 判断查询年份是否和现在年份相等
                d3 = d2.year * 12 + d2.month * 30 + d2.day
                d4 = d1.year * 12 + d1.month * 30 + d1.day
                if d2.month == 2: # 2月为闰月，28天
                    my_day = 28
                if d2.month in [1,3,5,7,8,10,12]:
                    my_day = 31
                if d2.month in [4,6,9,11]:
                    my_day = 30
                if 0 <= d3 - d4 <= my_day:
                    self.search_time = search_data # 查询日期
                else:
                    self.search_time = False
            else:
                self.search_time = False
        else:
            self.search_time = False
        for code in self.station_list:
            if start_city == code['name']:
                self.from_station = code['code']
                break
            else:
                self.from_station = False
        for code in self.station_list:
            if end_city == code['name']:
                self.to_station = code['code']
                break
            else:
                self.to_station = False
        self.species = species # 接受一个字典，列车种类

    def search_city(self, codes):
        """根据code值查询城市名称"""
        for i in self.station_list:
            if i['code'] == codes:
                return i['name']

    def check_ticket(self):
        """查询是否有票"""
        if self.search_time is not False:
            if self.from_station is not False and self.to_station is not False:
                payload = {
                    'leftTicketDTO.train_date': self.search_time,
                    'leftTicketDTO.from_station': self.from_station,
                    'leftTicketDTO.to_station': self.to_station,
                    'purpose_codes': 'ADULT',
                }

                # noinspection PyBroadException
                def result_data():
                    try:
                        r = requests.get(self.url,
                                         headers=self.headers,
                                         proxies={read_ini().split(',')[0]: read_ini().split(',')[1]},
                                         params=payload,
                                         verify=True,
                                         timeout=4,
                                         )
                        return r.json()
                    except Exception:
                        random_proxy('ipList_2.csv')
                        return False
                print('开始请求数据')
                result = result_data()

                def data_process():
                    print('开始解析数据。。。')
                    # print('总共%s趟车' % len(result['data']['result']))
                    # print(result)
                    for info in result['data']['result']:
                        data = info.split('|')
                        start_time = int(data[8].split(':')[0]) + int(data[8].split(':')[1]) / 60 # 出发时间折算成小时
                        total_time = int(data[10].split(':')[0]) + int(data[10].split(':')[1]) / 60 # 历时折算成小时
                        if 24 <= start_time + total_time < 48:
                            remind = '次日到达'
                        if 48 <= start_time + total_time <= 72:
                            remind = '两日到达'
                        if start_time + total_time > 72 or data[32] == '' and data[31] == '' and data[21] == '' and data[28] == '' and data[29] == '' and data[26] == '' and data[30] == '' or data[30] == '*' and data[23] == '' or data[23] == '*':
                            remind = '暂未开售'
                        if start_time + total_time < 24:
                            remind = '当日到达'

                        city_info = {
                            'trains': data[3], # 车次
                            'of_departure': self.search_city(data[4]), # 始发站
                            'the_terminal': self.search_city(data[5]), # 终点站
                            'start_departure': self.search_city(data[6]), # 出发站
                            'end_terminal': self.search_city(data[7]), # 到达站
                            'start_time': data[8], # 出发时间
                            'end_time': data[9], # 到达时间
                            'remind': remind, # 几日到达
                            'total_time': data[10], # 历时
                            'departure_date': '%s-%s-%s' % (data[13][:4], data[13][4:6], data[13][6:8]), # 出发日期
                            'business': data[32], # 商务座/特等座
                            'first_class': data[31], # 一等座
                            'second_class': data[30], # 二等座
                            'advanced_soft_sleeper': data[21], # 高级软卧
                            'soft_sleeper': data[23], # 软卧
                            'hard_sleeper': data[28], # 硬卧
                            'hard_seat': data[29], # 硬座
                            'no_seat': data[26], # 无座
                        }
                        self.train_info_list.append(city_info)
                if result is False or result['status'] is False:
                    print('数据请求失败，再次请求。。。')
                    for i in range(0, 1000):
                        result = result_data()
                        if result is not False:
                            print('数据再次请求成功')
                            data_process()
                            break
                else:
                    data_process()

                def search_ticket():
                    """列车种类筛选"""
                    for species in self.train_info_list:
                        if self.species['g'] is True:
                            if 'G' in species['trains']:
                                self.screening_list.append(species)
                        if self.species['d'] is True:
                            if 'D' in species['trains']:
                                self.screening_list.append(species)
                        if self.species['t'] is True:
                            if 'T' in species['trains']:
                                self.screening_list.append(species)
                        if self.species['k'] is True:
                            if 'K' in species['trains']:
                                self.screening_list.append(species)
                        if self.species['z'] is True:
                            if 'Z' in species['trains']:
                                self.screening_list.append(species)
                        if self.species['l'] is True:
                            if species['trains'][0] in [str(number) for number in range(10)]:
                                self.screening_list.append(species)
                        if self.species['g'] is False and self.species['d'] is False and self.species['t'] is False and self.species['k'] is False and self.species['z'] is False and self.species['l'] is False:
                            self.screening_list.append(species)
                search_ticket() # 列车种类查询
                return self.screening_list
            else:
                print('站点输入错误')
        else:
            print('日期输入错误')



if __name__ == '__main__':
    CheckTicket('成都', '内江', '2018-02-13').check_ticket()
