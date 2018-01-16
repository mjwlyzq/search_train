# coding: utf-8

"""Train tickets query via command-line.

Usage:
    tickets [-gdtkzl] <from> <to> <date>

Options:
    -h,--help        显示帮助菜单
    -g               高铁
    -d               动车
    -t               特快
    -k               快速
    -z               直达
    -l               普速

Example:
    python tickets.py 南京 北京 2016-07-01
    python tickets.py -dg 南京 北京 2016-07-01
"""
from docopt import docopt
from ticket_12306 import CheckTicket
import prettytable as pt

def coloring():
    """输出终端时给字体着色
       显示格式: \033[显示方式;前景色;背景色m
       只写一个字段表示前景色,背景色默认
    """
    color_dict = {
        'RED' : '\033[31m', # 红色
        'GREEN': '\033[32m', # 绿色
        'YELLOW': '\033[33m', # 黄色
        'BLUE': '\033[34m', # 蓝色
        'FUCHSIA': '\033[35m', # 紫红色
        'CYAN': '\033[36m', # 青蓝色
        'WHITE': '\033[37m', # 白色
        'RESET': '\033[0m', # 终端默认颜色
    }
    return color_dict

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    train_type = {
        'g': arguments['-g'], # 高铁
        'd': arguments['-d'], # 动车
        't': arguments['-t'], # 特快
        'k': arguments['-k'], # 快速
        'z': arguments['-z'], # 直达
        'l': arguments['-l'], # 普速
    }
    return CheckTicket(
            arguments['<from>'], # 出发站
            arguments['<to>'], # 到达站
            arguments['<date>'], # 发车日期
            train_type, # 列车类型
        ).check_ticket()

def table_shows():
    """以表格形式展示列车数据"""
    data = cli() # 车次列表
    if data:
        print('符合条件的车次有 %s列，如下列表' % len(data))
        tb = pt.PrettyTable()
        tb.field_names = ["车次",
                          "车站",
                          "发车日期",
                          "时间",
                          "历时",
                          "商务座",
                          "一等座",
                          "二等座",
                          "高级软卧",
                          "软卧",
                          "硬卧",
                          "硬座",
                          "无座",
                        ]
        for info in data:
            business = info['business']
            first_class = info['first_class']
            second_class = info['second_class']
            advanced_soft_sleeper = info['advanced_soft_sleeper']
            soft_sleeper = info['soft_sleeper']
            hard_sleeper = info['hard_sleeper']
            hard_seat = info['hard_seat']
            no_seat = info['no_seat']
            if business == '':
                business = '--'
            if first_class == '':
                first_class = '--'
            if second_class == '':
                second_class = '--'
            if advanced_soft_sleeper == '':
                advanced_soft_sleeper = '--'
            if soft_sleeper == '':
                soft_sleeper = '--'
            if hard_sleeper == '':
                hard_sleeper = '--'
            if hard_seat == '':
                hard_seat = '--'
            if no_seat == '':
                no_seat = '--'
            tb.add_row(
                [
                    info['trains'] + coloring()['RED'],
                    info['start_departure'] + coloring()['RESET'],
                    info['departure_date'] + coloring()['RED'],
                    info['start_time'] + coloring()['RESET'],
                    info['total_time'],
                    business,
                    first_class,
                    second_class,
                    advanced_soft_sleeper,
                    soft_sleeper,
                    hard_sleeper,
                    hard_seat,
                    no_seat,
                ]
            )
            tb.add_row(
                [
                    '' + coloring()['YELLOW'],
                    info['end_terminal'],
                    '',
                    info['end_time'],
                    info['remind'],
                    '' + coloring()['RESET'],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ]
            )
        print(tb) # 打印表格
    else:
        print('没有找到符合条件的车次')

if __name__ == '__main__':
    table_shows()
