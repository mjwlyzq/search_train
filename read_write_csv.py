#coding=utf-8
import csv



# wb中的w表示写入模式，b是文件模式
# 写入一行用writerow
# 多行用writerows

class read_write_csv:
    def __init__(self, name=None, column=None, write_data=None):
        self.file_path = name
        self.column = column
        self.write_data = write_data

    def write_csv(self):
        """写入csv文件"""
        try:
            with open(self.file_path, 'w', newline='', encoding='gbk') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(self.column)
                writer.writerows(self.write_data)
        except Exception as msgs:
            print(msgs)

    def read_csv(self, start_row=1, end_row=None):
        """读取csv文件"""
        try:
            read_result = []
            csv_file = open(self.file_path, 'r')
            reader = csv.reader(csv_file)
            for line in reader:
                read_result.append(line)
            csv_file.close()
            return read_result[start_row:end_row]
        except Exception as msgs:
            print(msgs)


if __name__ == '__main__':
    # read_write_csv(name='test.csv',
    #                column=['姓名', '年龄', '电话'],
    #                write_data=[['小河','25','1234567'],['小芳','18','789456']],
    #                ).write_csv()

    read_data = read_write_csv(name='ipList.csv').read_csv(end_row=3)
    print(read_data)







