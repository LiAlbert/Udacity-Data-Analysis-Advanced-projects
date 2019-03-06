# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:32:14 2017

这是用来query数据库中存在问题的数据的Python文件

@author: Albert
"""
import sqlite3


def pretty_print(table):
    """
    自定义用来打印query结果的函数，可以打印出中文字符
    如果直接用print打印含中文字符的列表，中文字符不会被打印出来
    
    """
    for line in table:
        for element in line:
            if element!=line[0]:
                print '|',
            print element,
        print

map = sqlite3.connect('map.db')
cursor = map.cursor()
cursor.execute(' SELECT * FROM nodes_tags WHERE key="street" group by value ')
streets = cursor.fetchall()
print 'streets:'
pretty_print(streets)

cursor.execute(' SELECT Value,COUNT(*) AS num FROM (SELECT * FROM  nodes_tags UNION ALL \
      SELECT * FROM ways_tags)as tags WHERE key="city" group by value order by num desc')
cities = cursor.fetchall()
print 'Cities:'
pretty_print(cities)

cursor.execute(' SELECT Value,COUNT(*) AS num FROM (SELECT * FROM  nodes_tags UNION ALL \
      SELECT * FROM ways_tags)as tags WHERE key="county" group by value order by num desc')
counties = cursor.fetchall()
print 'Counties:'
pretty_print(counties)

cursor.execute(' SELECT id FROM (SELECT * FROM  nodes_tags UNION ALL \
      SELECT * FROM ways_tags)as tags WHERE key="county" AND value="China"')
county_id=cursor.fetchall()
print "county id:"
pretty_print(county_id)

cursor.execute('SELECT * FROM (SELECT * FROM  nodes_tags UNION ALL \
      SELECT * FROM ways_tags)as tags where id="3013754950" ')
same_id_tags=cursor.fetchall()
print "same id tags:"
pretty_print(same_id_tags)

map.close()
