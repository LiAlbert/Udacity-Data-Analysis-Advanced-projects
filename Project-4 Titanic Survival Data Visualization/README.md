M# 泰坦尼号数据集可视化
by 李油

## 设计

#### 书面摘要

通过展示泰坦尼克号数据集中不同的类别的人的生还率来传达出谁更能在泰坦尼克号事件中生存下来。

#### 初始设计决策

选择数据: 从 https://www.kaggle.com/c/titanic 网站上下载
        (train.csv)泰坦尼克号数据集。

图表类型: 柱状图

数据清洗: 用Python先将数据进行探索(data_processing_first.py)，针对要表达的故事提取所要展示的数据信息,将清洗完毕的数据集放在(Titanic_first.csv)。

视觉编码: 采用d3和dimple相结合进行编码(index_first.html)

数据: 总体的生存率和死亡率，不同的座位等级、年龄、性别的人的生还率对比

布局: 整体靠左

图例: 大标题，柱状图的轴标签说明，按钮标签作为类别的图例

层次: 通过按钮选择类别，进行图形变换

动画和互动: 读者可以通过按钮找到自己感兴趣的类别进行对比，可以让读者自己探索信息得出故事。


#### 根据反馈1进行设计更改

黑色无法设置透明度，反而不利于观察。我将颜色设置成dimple默认的灰色，其opacity="0.8"，可以看到透过的网格线，整体比较舒适。

```javascript
myChart.defaultColors = [
  new dimple.color("gray");
];

```

增加性别和等级的两个类别的共同影响的生存率的对比。
```python
############# Pclass+性别 ##############

class_female_amount = data[data['Sex'] == 'female']['Pclass'].value_counts()
class_male_amount = data[data['Sex'] == 'male']['Pclass'].value_counts()

class1_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[1])
class2_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[2])
class3_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[3])

class1_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[1])
class2_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[2])
class3_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[3])
```

```javascript
var buttons2_labels = ["Ticket class", "age", "sex", "Ticket class+sex"]
```

#### 根据反馈2进行设计更改
通过css将标题设置居中显示，因为svg没有直接居中显示的设置，将svg图表整体右移达到居中显示的效果。。

```css
h1 {
  text-align: center;
  color:black;
}

svg {
  position:fixed;
  left:250px;

}
```

柱状图的宽度会随着类别而改变，类别越少，柱子越少，每根柱子就会比较宽，类别越多，柱子越多，每根柱子就会比较细。柱子的宽度改变会使得整个柱状图的大小不变，如果柱子的粗细设置为定值，整个柱状图大小会随着种类多少而改变，反而会分散读者的注意力。
#### 根据反馈3进行设计更改

由于图表类型是柱状图，需要仔细看各个轴的标签来理解图所传达的信息，动画太快反而会让读者难以理解，产生疑惑，动画太慢又会让读者等待时间太久。

因为其实除了all，其他显示都是生存率,将生存率部分划分为另一类按钮，简化x轴标签,y轴标签分为两类，“percentage”和“survived percentage” 。

```javascript
var buttons1 = d3.select("body")
                .append("div")
                .attr("class", "button type1_buttons")
                .selectAll("div")
                .data(buttons1_labels)
                .enter()
                .append("div")
                .text(function(d) {return d;});

var buttons2 = d3.select("body")
                .append("div")
                .attr("class", "button type2_buttons")
                .selectAll("div")
                .data(buttons2_labels)
                .enter()
                .append("div")
                .text(function(d) {return d;});
```
在清理数据集的时候将每个组内的总人数加到最终html要加载的csv文件中，并且设置鼠标悬浮在柱状图中的柱子时可以显示该柱子对应的组别的总人数、在svg中加入文本注释组内总人数对应的变量。

```javascript
if(t == "Ticket class+sex"){
  myChart.addSeries(["amount","type"], dimple.plot.bar);
}
else {
  myChart.addSeries("amount", dimple.plot.bar);
}
```

```javascript
svg.append("text").attr("x", 500)
   .attr("y",75)
   .style("fill", "#002171")// dark blue
   .text("amount: 每个组内的总人数");
```

#### 最终版本的书面摘要

通过展示泰坦尼克号数据集中不同的类别的人的生还率来传达出谁更能在泰坦尼克号事件中生存下来。

作者的观点和结论: 通过对比，1.得知座位等级越高的人的生存率越高, 座位等级越高的人往往越富有，这说明富人的生存率要比穷人高。2.年龄在18岁及以下生存几率比其他年龄段更大，大于60老年人生存几率最小。虽然老人和小孩一样都受到照顾的关系，但是老人自身的身体比年轻人和小孩都要差，生存下来的概率也就比年轻人和小孩都要低。3.女性比男性更容易生存下来，是因为在灾难发生时照顾女性的原因。4.等级为1或2的女性的生存率很高，接近1。

这个可视化图表是作者引导的读者自己探索的表达结构，读者可以根据自己感兴趣的分类对泰坦尼克号号数据集进行探索并发现自己一些有趣的结论。

## 反馈

#### 反馈1

可以将柱状图的长方形的颜色改为黑色，减少颜色对观众注意力的分散，使观众的注意力集中在数据上。

除了单一类别的对比，能否尝试两个类别的叠加的生存率对比


#### 反馈2

标题和图表靠左边显示有点不美观，可是设置为居中显示。


柱状图长方形的宽度有点太宽了，调细一点。


#### 反馈3

可不可以在网页运行的开头部分加入一段动画按顺序显示不同变量对生存率的影响。

x轴标签多次出现survive，使得轴标签不美观。

你的可视化体现的只是不同组别的生存率，不过生存率只是一个比例，脱离了总体的存在是没有任何意义的。因此你需要补充一下每个组内的总人数。

## 总结

数据可视化的关键是用讲故事的形式将数据中的信息准确地表现出来，这样数据分析师就可以将数据发现翻译为他人可以轻松理解的内容。在不断的更改迭代中，我体会到了可视化是一个需要不断提高的过程，通过一场场和读者的对话学会向别人展示和分享可视化，理解到可视化是一个流动过程，通常需要多次改进迭代。为了提高可视化的效果，需要提高选择最佳视觉元素来编码数据和批判性评估可视化效果的能力。在实现数据可视化的过程，我也更好的将dimple.js 和 d3.js应用与实践。
