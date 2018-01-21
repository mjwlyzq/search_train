# coding: utf-8

"""Train plane query via command-line.

Usage:
    plane [-f] <from> <to> <date> <time> <price>

Options:
    -h,--help        显示帮助菜单
    -f               定时查询,单位为分钟

Example:
    python plane.py 南京 北京 2016-07-01 0 0
    python -f plane.py 南京 北京 2016-07-01 30 1000
    末尾的倒数第二个参数为定时的时间，需要和-f配合使用。
    最后一个参数为价格阈值,当查询到机票的价格小于或者等于该阈值时窗口会打印该机票信息
    如果不需要定时 -f 参数不需要写， 但是最后时间和价格阈值的位置必须为0
"""
from docopt import docopt
from search_plane import CheckPlane
import prettytable as pt

def coloring():
    """输出终端时给字体着色
       显示格式: \033[显示方式;前景色;背景色m
       只写一个字段表示前景色,背景色默认
    """
    color_dict = {
        'RED': '\033[31m', # 红色
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
    """命令行接受指令"""
    arguments = docopt(__doc__)
    train_type = {
        'f': arguments['-f'], # 是否定时
    }
    return CheckPlane(
            arguments['<from>'], # 出发站
            arguments['<to>'], # 到达站
            arguments['<date>'], # 起飞日期
            arguments['<time>'], # 定时，单位为分钟
            arguments['<price>'], # 价格阈值
            train_type, # 是否定时
        ).my_timing()

def table_shows():
    """以表格形式展示飞机信息"""
    data = cli() # 飞机班次列表
    if data:
        print('共有 %s 趟飞机，如下列表' % len(data))
        tb = pt.PrettyTable()
        tb.field_names = ["航班信息",
                          "起飞时间",
                          "到达时间",
                          "准点率",
                          "价格(人民币)",
                        ]
        for info in data:
            tb.add_row(
                [
                    '%s%s' % (info['alc'],info['fn']) + coloring()['CYAN'],
                    info['dt'],
                    info['at'] + coloring()['CYAN'],
                    '准点率',
                    str(info['p']) + coloring()['RESET'],
                ]
            )
            tb.add_row(
                [
                    '' + coloring()['YELLOW'],
                    info['dpbn'],
                    info['apbn'],
                    info['HistoryPunctualityArr'],
                    info['rt'] + coloring()['RESET'],
                ]
            )
        print(tb) # 打印表格
    else:
        print('没有找到符合条件的航班')

if __name__ == '__main__':
    table_shows()
