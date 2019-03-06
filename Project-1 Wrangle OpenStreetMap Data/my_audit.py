import csv
import re


def str_del_by_index(s, index):
    '''
    字符串删除字符函数：从字符串中删除指定位置的一个字符后返回一个新的字符串，
    index正负都可以，正表示正序，负表示倒序。

    '''
    if type(s) != type('str'):  #防止s参数类型出错，如果出错不对s进行更改
        print "The first parameter's type should be str!"
        return s
    if type(index) != type(1):  #防止index参数类型出错，如果出错不对s进行更改
        print "The second parameter's type should be int"
        return s
    if index > len(s) - 1 or index < -len(s): #防止index越界，如果越界不对s进行更改
        print "You can't delete a character out the range of a string!"
        return s
    s_list = list(s)
    del s_list[index]
    new_s = ''.join(s_list)
    return new_s


def str_insert_by_index(s, index, sub_str):
    '''
    字符串插入字符函数：从字符串指定位置插入一个字符或字符串后返回一个新的字符串
    index的用法str_del_by_index()函数

    '''
    if type(s) != type('str'):
        print "The first parameter's type should be str!"
        return s
    if type(index) != type(1):
        print "The second parameter's type should be int"
        return s
    if type(sub_str) != type('str'):
        print "The third parameter's type should be str!"
        return s
    if index > len(s) - 1 or index < - len(s):
        print "You can't insert characa out the range of a string!"
        return s
    s_list = list(s)
    s_list.insert(index, sub_str)
    new_s = ''.join(s_list)
    return new_s


def audit_phone_number(phone_number):
    '''
    修改电话号码函数：由于所选区域中的号码都是以+86,
    所以不用对号码的国际区域码进行修改

    '''
    phone_number = phone_number.replace(" ", "") #去除电话号码中的空格
    if phone_number[3] == '0':      #如果+86后城市区域码以0开头，将开头的0删除
        phone_number = str_del_by_index(phone_number, 3)
    phone_number = str_insert_by_index(phone_number, 3, ' ') #在国际区码和城市区域码之间插入一个空格
    phone_number = str_insert_by_index(phone_number, 7, ' ') #在城市区域码和之间插入一个空格
    return phone_number

def clean_csv_phone(input_csv_file,output_csv_file):
    '''
    csv文件清理函数：
    此函数仅对csv文件中电话号码那部分进行清理，其他部分保持不变
    清理后的csv可导入sql数据库
    '''
    with open(input_csv_file,'rb') as i:
        input_csv=csv.DictReader(i)
        header=input_csv.fieldnames
        with open(output_csv_file,'wb') as o:
            output_csv=csv.DictWriter(o,fieldnames=header)
            output_csv.writeheader()
            for line in input_csv:
                if line['key']=='phone':
                    print "unaudited phone number:",line['value']
                    line['value'] = audit_phone_number(line['value'])
                    print "audited phone number:",line['value']
                    '''
                    清理的时候会显示未清理和清理后的电话号码进行对比，部分结果如下：
                    unaudited phone number: +86055163600661
                    audited phone number: +86 551 63600661
                    unaudited phone number: +86 551 6518 9888
                    audited phone number: +86 551 65189888
                    unaudited phone number: +86 551 65317511
                    audited phone number: +86 551 65317511
                    unaudited phone number: +8655165317511
                    audited phone number: +86 551 65317511
                    '''

                output_csv.writerow(line)

if __name__ == '__main__':
    clean_csv_phone('nodes_tags.csv', 'nodes_tags_audited.csv')
    clean_csv_phone('ways_tags.csv','ways_tags_audit.csv')
