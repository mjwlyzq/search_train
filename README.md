# search_train
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
