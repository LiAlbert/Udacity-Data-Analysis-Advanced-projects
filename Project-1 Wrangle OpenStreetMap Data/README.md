# Project Wrangle OpenStreetMap Data

### Map Area

Huainan, Anhui Province, China

- [https://www.openstreetmap.org/relation/3262360](https://www.openstreetmap.org/relation/3262360)

这张地图是我家乡的地图，我想通过这张地图加深一下对家乡的了解，如果发现一些错误的话希望可以提出一些改进的意见。

## 在地图中遇到的问题

在对下载地图的osm文件中tag的key和value进行审计的时候，主要发现了以下几个问题：

- 电话号码的格式错误、格式不统一  *(“+86055163600661”，“+86 551 6518 9888”)*
- key street包含了一些不是街道的元素 *("West Library, USTC"，"人民南路解放路口")*
- key city包含市的下级行政区、省级行政区或者直接写成的县级行政区 *("安徽省合肥市蜀山区"，“怀远县”)*
- country标签错写成county

```xml
<tag k="is_in:county" v="China"/>
```

### 电话号码的格式错误、格式不统一

在审计包含电话号码的tag的时候发现电话号码存在格式错误、格式不统一等问题（osm文件中的电话号码都是以+86开头的）。

- 格式错误：中国的电话号码以+86开头表示国际电话号码格式，在+86之后的城市地区区号不用再加0。
- 格式不统一：有的电话号码没有用空格分割电话号码，有的用两个或三个空格分割电话号码。

python查询osm文件中电话号码的结果如下:
```
    phone | +86055163600661
    phone | +86 551 6518 9888
    phone | +86 551 65317511
    phone | +8655165317511
    phone | +86 551 65706888
    phone | +86 551 62885066
    phone | +86 551 62206666
    phone | +86 551 62268888
    phone | +86 551 6297 1777
    phone | +86 551 6297 1888
    phone | +86 551 6222 8888
    phone | +86 551 6550 9888
```

对电话号码的清理采用了两个空格分割电话号码、将+86后面城市地区区号多余的0去掉的方式，处理的函数如下：
  ``` python
  def audit_phone_number(phone_number):
      phone_number = phone_number.replace(" ", "")
      if phone_number[3] == '0':
          phone_number = str_del_by_index(phone_number, 3)
      phone_number = str_insert_by_index(phone_number, 3, ' ')
      phone_number = str_insert_by_index(phone_number, 7, ' ')
      return phone_number
  ```
其中str_del_by_index()和str_insert_by_index()为自定义的函数，str_del_by_index()用来删除string中的一个字符，str_insert_by_index()用来向字符串中插入一个字符或字符串。

### key street
key street的类型是 address，人工提交数据时就可能将地址中不属于 street 的内容也放在了 street。python 查询osm文件中不是以路、道、街、巷等字结尾的 street name 的结果如下:
```
    addr:street | 人民南路解放路口
    addr:street | 北一环
    addr:street | West Library, USTC
    addr:street | 50 meters East of the
    Cross of Fuwang Road and Shuangqing Road
    addr:street | Shuangqing Road
    addr:street | Qinghe East Road
    addr:street | G312
    addr:street | Qimen Lu
    addr:street | Lingqing
    addr:street | Fuwang Road
    addr:street | Shuangqing Road and Fuyang Road
    addr:street | 东桥镇
    addr:street | 东桥镇六岗村
```
### key city
因为通过 OpenStreetMap 的 Overpass API 选则的地图区域只能是矩形的，我将我家乡城市的区域都选到也就选到了其他城市的部分区域。我想询自己选择的地图都包含了哪些城市，结果发现 city key 对应的 value 有很多都是县城，也有些是城市的名称前面有省的名称、后面有市的下级行政区域的名称。python 查询osm文件中city name 结果如下：
```
    addr:city | 固始县
    addr:city | 安徽六安
    addr:city | 合肥
    addr:city | 合肥市
    addr:city | 太和县
    addr:city | Hefei
    addr:city | 定远县
    addr:city | 淮南市
    addr:city | Huainan
    addr:city | 阜阳市
    addr:city | Fuyang
    is_in:city | 巢湖市
    addr:city | 合肥国家高新技术产业开发区
    addr:city | 蚌埠
    addr:city | 蚌埠市怀远县
    addr:city | 阜阳市颍州区
    addr:city | 肥西县官亭镇
    addr:city | 长丰县
    addr:city | 安徽省合肥市
    addr:city | 安徽省合肥市蜀山区
    addr:city | 肥西县
    addr:city | 凤阳县
    addr:city | 安徽省六安市
    addr:city | 蚌埠市
    addr:city | 肥东县
    addr:city | 六安市
```

### country标签错写成county
在发现city name中混有county的名称之后，我便去查了一下county。python 查询osm文件中county的结果如下:
```
    is_in:county | China
    is_in:county | 长丰县
    is_in:county | 肥东县
    is_in:county | 肥西县
```
出人意料的是China竟然出现现在county的名称里，为了弄清楚错误出在哪里，我查找出对应tag的所属的node，再看看查到node的其他tag描述的是什么。
```xml
查找到node的所有tag:
    <tag k="admin_level" v="6" />
    <tag k="china_class" v="district" />
    <tag k="is_in:continent" v="Asia" />
    <tag k="is_in:county" v="China" />
    <tag k="is_in:municipality" v="Hefei" />
    <tag k="is_in:province" v="Anhui" />
    <tag k="name" v="瑶海区" />
    <tag k="name:de" v="Yaohai" />
    <tag k="name:en" v="Yaohai" />
    <tag k="name:eo" v="Yaohai" />
    <tag k="name:es" v="Yaohai" />
    <tag k="name:fr" v="Yaohai" />
    <tag k="name:ja" v="瑶海区" />
    <tag k="name:ko" v="야오하이 구" />
    <tag k="name:pt" v="Yaohai" />
    <tag k="name:sv" v="Yaohai" />
    <tag k="name:vi" v="Dao Hải" />
    <tag k="note" v="人口 population：970000&#10;
    不建议填写人口/Population tag is not recommended.&#10;
    https://wiki.openstreetmap.org/wiki/China_tagging_guidelines" />
    <tag k="place" v="city" />
    <tag k="wikidata" v="Q1364939" />
    <tag k="wikipedia" v="en:Yaohai District" />
```
观察这些tag可以发现它们都是在描述合肥市瑶海区，China应该是其所属的国家，type的值为is_in也就说瑶海区是在China之中的，显然China对应的key的值应该是country而不是county.

# 数据概述

### 文件大小
```
huainan.osm ..................... 101MB
huainan.db ...................... 54MB
nodes.csv ....................... 40MB
nodes_tags.csv .................. 1019K
ways.csv ........................ 3.0M
ways_nodes.csv .................. 15M
ways_tags.csv ................... 3.6M
```
### 节点数量

```sql
sqlite> SELECT COUNT(*) FROM nodes;

487775
```

### 路径数量

```sql
sqlite> SELECT COUNT(*) FROM ways;

51671
```

### 唯一用户数量

```sql
sqlite> SELECT COUNT(DISTINCT(users.uid))       
        FROM(SELECT uid FROM nodes UNION        
        ALL SELECT uid FROM ways) AS users;

271
```
### 贡献量前十的用户

```sql
sqlite> SELECT users.user, COUNT(*) AS num FROM (SELECT user
        FROM nodes UNION ALL SELECT user FROM  ways) AS users
        GROUP BY users.user ORDER BY num desc limit 10;

ff5722|120008
sinopitt|72510
Virgil Guo|67588
katpatuka|57397
汤鹏程|48662
peisen_wang|22108
Cscen|19855
Ge Zhu|9596
jamesks|8820
雨过昔年|8049
```

### 商店的数量

```sql
sqllite> SELECT COUNT(*) FROM nodes_tags where key="shop";

191
```

### 淮南市的人口

``` sql
sqlite> SELECT p.value FROM (SELECT * FROM nodes_tags
        WHERE key="population") AS p,nodes_tags WHERE
        p.id=nodes_tags.id AND nodes_tags.key="name"
        AND nodes_tags.value="淮南市";

3456000
```

# 关于数据集的其他想法
在对数据进行探索的时候，发现在描述一个行政区域节点的时候既用了key china_class描述其类型也用了key place 描述其类型。key china_class是根据中国的行政区域进行划分，而key place是根据地理概念进行划分的。但是在描述一个比较小的节点所属的更大一点的节点时根据place来描述的结果不是唯一的，比如说一个乡镇所属的县和所属的市的place可能都是city, 那么这个城镇所属的city根据的是key place的话既可以填它所属的县也可以填它所属的市，这样就会导致节点描述其所属节点时比较混乱，之前我发现的key city的问题部分原因也就是因为这个。</br></br>
根据china_class来描述一个节点的所属节点的优点，是可以消去其所属节点key place相同带来的不唯一，而且根据行政区域划分也比较符合中国人的区域概念。然而根据china_class来描述一个节点的所属节点也有一个比较大的缺点，在openstreetmap的WikiProject China页面中没有对key china_class的取值做出限定，key china_class的取值取决于用户, 这样会导致china_class的取值是不统一的，可能两个用户不同的取值实际上是在描述同一个china_class，而openstreetmap在Map Features页面有对key place的取值做出限定。综合来看，用户在openstreetmap上描述一个节点所属的更大的一个节点时，在其所属的节点的place不相同时应该参考place,相同再根据china_class进行判断。
