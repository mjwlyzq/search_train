#coding=utf-8
import configparser

def write_ini(path='config.ini', node='proxy', child='proxy', content=None):
    """写入ini文件"""
    config=configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    try:
        # config.add_section("session") #增加节点
        config.set(node, child, content)
    except configparser.DuplicateSectionError:
        print("ini配置文件写入失败")

    config.write(open(path, "w", encoding='utf-8'))


def read_ini(path='config.ini', node='proxy', child='proxy'):
    """读取ini文件"""
    config=configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    try:
        content = config.get(node, child)
        # print(content)
        return content
    except configparser.DuplicateSectionError:
        print("ini配置文件读取失败！")

if __name__ == '__main__':
    print(read_ini('config.ini'))
