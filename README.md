# search_train
V1.0.0
简单的一个命令就可以查询12306的车票
1、安装python版本为3.4以上(python有两个版本2.x和3.x)
https://www.python.org/ftp/python/3.6.2/python-3.6.2-amd64.exe
2、在cmd命令窗口cd到该文件夹跟目录下
d:
cd D:\search_train
3、安装依赖
pip install -r requests.txt
安装可能有点慢，请耐心等待
4、在该目录下载命令行中输入 
python tickets.py -h 获取帮助信息
该帮助信息有详细的操作说明
5、如果代理ip切换多个后任然查询不出来时，请在命令行该文件夹下运行
python proxyIp.py

运行结束后，再次查询车票

V1.1.0
增加了飞机票查询功能
使用方法
1、cd D:\search_train   2、python plane.py 兰州 成都 2018-02-29

v1.1.1
新增机票定时查询功能
python plane.py -f 兰州 成都 2018-02-29 1 500



Example:
    python plane.py 南京 北京 2016-07-01 0 0
    python -f plane.py 南京 北京 2016-07-01 30 1000
    末尾的倒数第二个参数为定时的时间，需要和-f配合使用。
    最后一个参数为价格阈值,当查询到机票的价格小于或者等于该阈值时窗口会打印该机票信息
    如果不需要定时 -f 参数不需要写， 但是最后时间和价格阈值的位置必须为0