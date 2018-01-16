#coding=utf-8
import requests
import time
import random
from time import sleep
from read_lxml import ReadHtml
from read_write_csv import read_write_csv
from read_write_ini import write_ini

class proxy_ip:
    def __init__(self, link_num=100):
        self.url_list = [] # 获取代理地址的页面url列表
        self.error_url = [] # 采集失败的url列表
        self.csv_list = [] # 写入csv文件的列表
        self.csv_title = ['ip代理地址', '类型', '连接速度', '有效期', '验证时间', '所属地址', '是否匿名']
        self.bai_url = 'http://test.app.gouuse.cn/#/account/login' # 验证ip地址有效性的url
        url = 'http://www.xicidaili.com/nn/%s' # 代理url参数化
        for num in range(1,link_num):
            link = url % str(num)
            self.url_list.append(link)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer': 'http://www.xicidaili.com/nn/2',
        }
        self.get_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer': 'http://www.baidu.com',
        }
        self.ip_list_result = [] # 没有验证有效性的代理ip列表
        self.vaild_ip_list = [] # 验证有效的代理地址

    # noinspection PyBroadException
    def my_get_ip(self):
        """获取ip"""
        print('开始获取代理url页面链接')
        for url in self.url_list:
            html = ReadHtml(url, headers=self.headers).read_html()
            if html is False:
                self.error_url.append(url)
                sleep(5)
            else:
                for nums in range(2,102):
                    ip = '//table[@id="ip_list"]/tr[%s]/td[2]' % str(nums) # ip
                    port = '//table[@id="ip_list"]/tr[%s]/td[3]' % str(nums) # 端口
                    dress = '//table[@id="ip_list"]/tr[%s]/td[4]/a' % str(nums) # 地址
                    anonymous = '//table[@id="ip_list"]/tr[%s]/td[5]' % str(nums) # 是否匿名
                    types = '//table[@id="ip_list"]/tr[%s]/td[6]' % str(nums) # 类型，是http还是https
                    speed = '//table[@id="ip_list"]/tr[%s]/td[7]/div' % str(nums) # 连接速度
                    survival = '//table[@id="ip_list"]/tr[%s]/td[9]' % str(nums) # 存活时间
                    my_time = '//table[@id="ip_list"]/tr[%s]/td[10]' % str(nums) # 验证时间

                    my_ip = html.xpath(ip)[0].text
                    my_port = html.xpath(port)[0].text
                    try:
                        my_dress = html.xpath(dress)[0].text
                    except Exception:
                        my_dress = None
                    my_anonymous = html.xpath(anonymous)[0].text
                    my_types = html.xpath(types)[0].text
                    my_speed = html.xpath(speed)[0].get('title').split('秒')[0]
                    my_survival = html.xpath(survival)[0].text
                    my_time = html.xpath(my_time)[0].text
                    ip_list = '%s:%s' % (my_ip, my_port)
                    ip_dict = {
                        'ip': ip_list,
                        'dress': my_dress,
                        'anonymous': my_anonymous,
                        'types': my_types,
                        'speed': my_speed,
                        'survival': my_survival,
                        'my_time': my_time,
                    }
                    self.ip_list_result.append(ip_dict) # 获取所有ip信息
        print('获取所有ip信息完成')
        print('开始验证代理ip有效性')
        for ip in self.ip_list_result:
            my_time_times = ip['my_time'] # 验证时间
            my_time_data = my_time_times.split(' ')[0] # 分隔后验证日期
            my_time_event = my_time_times.split(' ')[1] # 分割后验证时间
            my_survival_data = ip['survival'] # 存活时间
            speed_second = float(ip['speed'])

            current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前系统日期
            current_event = time.strftime('%H:%M', time.localtime(time.time()))  # 当前系统时间
            time_current_second = int(current_event.split(':')[0]) + int(current_event.split(':')[1]) / 60 # 将当前系统分隔后时间转换为小时
            time_data_second = int(my_time_event.split(':')[0]) + int(my_time_event.split(':')[1]) / 60 # 转换为小时
            if speed_second <= 1: # 如果连接速度小于1秒
                if int(my_time_data.split('-')[0]) == int(current_data.split('-')[0][-2:]): # 判断年份
                    if int(current_data.split('-')[1]) == int(my_time_data.split('-')[1]): # 月份
                        if '天' in my_survival_data:
                            survival_second = int(my_survival_data.split('天')[0]) # 天
                            if int(current_data.split('-')[2]) - int(my_time_data.split('-')[2]) <= survival_second:
                                ip_key = {
                                    'ip': ip['ip'],
                                    'types': ip['types'],
                                    'speed': ip['speed'],
                                    'survival': ip['survival'],
                                    'my_time': ip['my_time'],
                                    'dress': ip['dress'],
                                    'anonymous': ip['anonymous'],
                                }
                                self.vaild_ip_list.append(ip_key)
                        elif '小时' in my_survival_data:
                            survival_second = int(my_survival_data.split('小时')[0]) # 小时
                            if current_data.split('-')[2] == my_time_data.split('-')[2]:
                                if time_current_second - time_data_second <= survival_second: # 如果当前系统时间减去验证时间小于有效小时数
                                    ip_key = {
                                        'ip': ip['ip'],
                                        'types': ip['types'],
                                        'speed': ip['speed'],
                                        'survival': ip['survival'],
                                        'my_time': ip['my_time'],
                                        'dress': ip['dress'],
                                        'anonymous': ip['anonymous'],
                                    }
                                    self.vaild_ip_list.append(ip_key)
                        elif '分钟' in my_survival_data:
                            pass
        print('代理ip有效性验证完成')
        for data in self.vaild_ip_list:
            """写入csv文件列表"""
            csv_list = [
                data['ip'],
                data['types'],
                data['speed'],
                data['survival'],
                data['my_time'],
                data['dress'],
                data['anonymous'],
            ]
            self.csv_list.append(csv_list)
        print('开始写入csv文件。。。')
        read_write_csv( # 写入csv文件
            name='ipList_2.csv',
            column=self.csv_title,
            write_data=self.csv_list,
        ).write_csv()

        print('没有验证有效性的代理ip列表共:%s项' % len(self.ip_list_result))
        # print('没有验证有效性的代理ip列表:%s' % self.ip_list_result)
        print('验证有效的代理地址列表共%s项' % len(self.vaild_ip_list))
        #print('验证有效的代理地址列表:%s' % self.vaild_ip_list)




if __name__ == '__main__':
    proxy_ip().my_get_ip()


