# TitanicData Visualization
by 谢冰

## 设计

#### 书面摘要

通过展示泰坦尼克号数据集中不同的类别的人的生还率来传达出谁更能在泰坦尼克号事件中生存下来。

#### 初始设计决策

选择数据: 从 https://www.kaggle.com/c/titanic 网站上下载
        (train.csv)泰坦尼克号数据集。

图表类型: 柱状图

数据清洗: 用Python先将数据进行探索(clean.py)，针对要表达的故事提取所要展示的数据信息,将清洗完毕的数据集放在(Titanic.csv)。

视觉编码: 采用d3和dimple相结合进行编码(index1.html)

数据: 总体的生存率和死亡率，不同的性别、年龄的人的生还率对比

布局: 图表居中，按钮居于左方

图例: 柱状图大标题，柱状图的轴标签说明，按钮标签作为类别的图例

层次: 通过按钮进行图形变换

动画和互动: 读者可以通过按钮找到自己感兴趣的类别进行对比，可以让读者自己探索信息得出故事。


#### 根据反馈1进行设计更改

增加了不同等级的人的生存率对比。


```python
class_amount = data['Pclass'].value_counts()
class_1_survived_ratio = (data[(data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[1])
class_2_survived_ratio = (data[(data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[2])
class_3_survived_ratio = (data[(data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[3])

```

修改柱状图的大小，修改柱状图的轴的字体，使得整体更方便阅读。

```javascript
//set canvas
"use strict";
var margin = 75,
  width = 800 - margin,
  height = 500 - margin;

var svg = d3.select("body")
  .append("svg")
  .attr("width", width + margin)
  .attr("height", height + margin)
  .append('g')
  .attr('class', 'chart');


x.fontSize = "15px";

y.fontSize = "15px";
```

将按钮放在右方。

```css
div.type_buttons {
  position:fixed;
  top:200px;
  left:730px;
}
```

#### 根据反馈2进行设计更改

增加的等级+性别的生存率对比

```python
############# Pclass+sex ##############

class_female_amount = data[data['Sex'] == 'female']['Pclass'].value_counts()
class_male_amount = data[data['Sex'] == 'male']['Pclass'].value_counts()

class_1_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[1])
class_2_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[2])
class_3_female_survived_ratio = (data[(data['Sex'] == "female") & (data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_female_amount[3])

class_1_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[1])
class_2_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[2])
class_3_male_survived_ratio = (data[(data['Sex'] == "male") & (data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                                /float(class_male_amount[3])
```

让y轴值域保持在(0,1)

```javascript
y.overrideMax = 1;
```

#### 根据反馈3进行设计更改

修改标题，明确引导读者对故事(Who survived from Titanic?)进行探索。

```javascript
d3.select("body")
  .append("h1")
  .text("Who survived from Titanic?");
```
增加h2副标题，通过按钮更新h2副标题，读者能更清楚看到自己选择的类别。

```javascript

d3.select("body")
    .append("h2")
    .text("all");

function update(t) {
  //update title
  d3.select("h2")
    .text(t);
}
```

改用百分数来展示数据，既方便读者明白是生存率的对比，同时增加了精确度，解决了比如class1+female的生存率由于四舍五入变为1的问题，改为百分数时变为97%。

```javascript
y.tickFormat = "%";
```
#### 最终版本的书面摘要

通过展示泰坦尼克号数据集中不同的类别的人的生还率来传达出谁更能在泰坦尼克号事件中生存下来。

作者的观点和结论: 通过对比，1.得知女性比男性更容易生存下来，是因为在灾难发生时照顾女性的原因。2.年龄在18岁及以下生存几率比其他年龄段更大，大于60老年人生存几率最小，除了有照顾老人小孩的关系，与老人自身的身体条件在也有一定关系。3.等级越高的人的生存率越高。4.等级为1或2的女性的生存率接近1。

考虑到这个作者引导的读者自己探索的表达结构，读者可以根据自己感兴趣的分类对泰坦尼克号号数据集进行探索并发现自己一些有趣的结论。

## 反馈

#### 反馈1

这个图让我能大体了解到数据的主要信息，我在可视化中可以进行不同年龄，不同性别的人的生还率对比，让我看到女性生还机会高于男性，未成年人的生还机会也比其他年龄的更高。但是我也发现几个问题。

单纯从不同性别和年龄比较未能全面展示泰坦尼克号数据。

柱状图过大，导致轴的字体与柱子相比显得太小，难以阅读。

按钮在左边不顺手。

#### 反馈2

除了单一类别的对比，能否尝试两个类别的叠加的生存率对比？

y轴的范围随着数据的范围而变化，导致不同category的图之间的对比出现困难，并且在总体数据较小时放大了差异，降低了数据的可信度。

#### 反馈3

标题未能明确引导读者对故事进行探索。

分数精确度较低，比如class1+female的生存率由于四舍五入变为1，导致数据不准确，如果能取多几位小数会更好展示数据。



## 总结

数据分析师是讲故事的人，他们可以将数据发现翻译为他人可以轻松理解的内容。他们将数据可视化视为至关重要的交流形式。在不断的更改迭代中，我体会到了可视化是一场对话，学会了向别人展示和分享可视化，理解到可视化是一个流动过程，通常需要多次改进迭代。提高了展现出选择最佳视觉元素来编码数据和批判性评估可视化效果的能力，也让我将dimple.js 或 d3.js更好的用于实践。
