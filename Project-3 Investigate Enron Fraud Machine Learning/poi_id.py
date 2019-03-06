#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pickle
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score


# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# 数据探索
print "数据集总点数为：", len(data_dict)  # 打印数据集总点数
print "特征总个数为：", len(data_dict.values()[0])-1  # 打印特征总个数，"POI"为标签,所以要减一

random.seed(2018)  # 设置随机数种子，使得每次产生一样的随机数。
n = random.randint(0, 125)  # 生成的随机数n: 0 <= n <= 145
print "任意一个人的姓名、特征和标签:", data_dict.items()[n]

keys = data_dict.keys()
poi_number = 0
non_poi_number = 0
for key in keys:
    if data_dict[key]['poi'] == True:
        poi_number += 1
    else:
        non_poi_number += 1
print "POI人数：", poi_number
print "非POI人数", non_poi_number

feature_keys = data_dict[key].keys()
for feature_key in feature_keys:
    NaN_number = 0
    for key in keys:
        if data_dict[key][feature_key] == 'NaN':
            NaN_number += 1
    print feature_key+"缺失值的个数为:", NaN_number

# Task 2: Remove outliers
features = ["salary", "bonus"]
subset = featureFormat(data_dict, features)

max_salary = subset[0][0]
for data in subset:
    salary = data[0]
    if max_salary < salary:
        max_salary = salary
    bonus = data[1]
    plt.scatter(salary, bonus)
plt.xlabel("salary")
plt.ylabel("bonus")
plt.title("bonus by salary with biggest outlier")
plt.show()

for key in keys:
    if data_dict[key]["salary"] == max_salary:
        print "最大异常点对应的人名：", key

data_dict.pop('TOTAL', 0)

features_list = ["salary", "bonus"]
subset = featureFormat(data_dict, features_list)
for data in subset:
    salary = data[0]
    bonus = data[1]
    plt.scatter(salary, bonus)
plt.xlabel("salary")
plt.ylabel("bonus")
plt.title("bonus by salary without biggest outlier")
plt.show()

print "其他两个异常点对应的人名为："
for key in data_dict.keys():
    if data_dict[key]['salary'] != 'NaN' \
            and data_dict[key]['bonus'] != 'NaN':
        if data_dict[key]['salary'] >= 1e6 \
                and data_dict[key]['bonus'] >= 5e6:
            print key

# Task 3: Create new feature(s)
def scatterplot_features(data_dict, features_list):
    '''
    画出两个特征与标签poi关系的散点图，data_dict应该是一个字典，
    features_list应该是一个有3个元素的列表，并且第一个元素应该是'poi'
    '''
    data = featureFormat(data_dict, features_list, sort_keys=True)
    for point in data:
        label = point[0]
        x = point[1]
        y = point[2]
        if label == True:
            plt.scatter(x, y, c='r')
        else:
            plt.scatter(x, y, c='b')
    red_patch = patches.Patch(color='red', label='poi')
    blue_patch = patches.Patch(color='blue', label='non poi')
    plt.legend(handles=[red_patch, blue_patch])
    plt.xlabel(features_list[1])
    plt.ylabel(features_list[2])
    plt.savefig(features_list[1]+'_by_'+features_list[2]+'.png')
    plt.show()

# Store to my_dataset for easy export below.
my_dataset = data_dict
features_list = ['poi', 'from_poi_to_this_person', 'from_this_person_to_poi']
scatterplot_features(my_dataset,features_list)

def computeRatio(poi_messages, all_messages):
    """ 
        给定来自或者发给嫌疑人的邮件总数量以及接受或发送的邮件的总数量，
        计算来着嫌疑人的邮件数量占总接收邮件数量的比例或者发给嫌疑人的
        邮件数量占总发送邮件数量的比例。
    """
    ratio = 0.
    if poi_messages != "NaN" and all_messages != "NaN":
            ratio = float(poi_messages) / all_messages
    return ratio

#向my_dataset中添加新特征from_poi_ratio和to_poi_ratio
for key in my_dataset.keys():
    from_poi = my_dataset[key]['from_poi_to_this_person']
    from_messages = my_dataset[key]['to_messages']
    my_dataset[key]['from_poi_ratio'] = computeRatio(from_poi,from_messages)
    to_poi = my_dataset[key]['from_this_person_to_poi']
    to_messages = my_dataset[key]['from_messages']
    my_dataset[key]['to_poi_ratio'] = computeRatio(to_poi, to_messages)

features_list = ['poi', 'from_poi_ratio', 'to_poi_ratio']
scatterplot_features(my_dataset, features_list)

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".(because it is the target, \
# targetFeatureSplit will split the first one out)

###没有加入新特征的特征列表
features_list_no_new = ['poi','salary', 'total_payments',
                   'exercised_stock_options', 'bonus', 'restricted_stock',
                   'deferred_income', 'total_stock_value', 'expenses',
                   'other', 'long_term_incentive', 'shared_receipt_with_poi',
                   'from_poi_to_this_person', 'to_messages', 
                   'from_this_person_to_poi', 'from_messages'
                   ]
### 加入新特征的特征列表
features_extracted = ['poi', 'salary', 'total_payments',
                      'exercised_stock_options', 'bonus', 'restricted_stock',
                      'deferred_income', 'total_stock_value', 'expenses',
                      'other', 'long_term_incentive', 'shared_receipt_with_poi',
                      'to_poi_ratio', 'from_poi_ratio']

def selectKbestFeatures(k,features, print_score=True):
    '''
    对特征的得分进行排序，打印得分最高的k个特征的得分，
    并将最终选好的特征存入features_list中
    '''
    features_list=['poi']
    selector = SelectKBest(k=select_number)
    features_selected = selector.fit_transform(features, labels)
    scores = list(selector.scores_)
    scores_sorted = sorted(scores, reverse=True)
    for score in scores_sorted[:k]:
        feature = features_extracted[1:][scores.index(score)]
        features_list.append(feature)
        if print_score == True: 
            print feature + ':',score
    return features_list,features_selected

# Task 4: Try a varity of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

# decision tree algorithm & validation


def myDecisionTree(features_selected, labels, print_para=True, print_score = False):
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features_selected, labels,
                         test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier()
    parameters = {"min_samples_split": range(5, 80, 5)}
    grid = GridSearchCV(clf, parameters)
    grid.fit(features_train, labels_train)
    clf = grid.best_estimator_
    if print_para:
        print "决策树的min_samples_split参数的最佳值为：",
        print clf.min_samples_split
        print
    if print_score:
        pred = clf.predict(features_test)
        print "决策树的性能:"
        print "recall score:", recall_score(labels_test, pred)
        print "precision score:", precision_score(labels_test, pred)
        print

    return clf


# naivebays algorithm & validation
def myGaussianNB(features_selected, labels, print_score = False):
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features_selected, labels,
                         test_size=0.3, random_state=42)
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    if print_score:
        pred = clf.predict(features_test)
        print "朴素贝叶斯性能:"
        print "recall score:", recall_score(labels_test, pred)
        print "precision score:", precision_score(labels_test, pred)
        print
    return clf

# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

from tester import test_classifier

print "没有加入新特征的朴素贝叶斯算法测试："
data_no_new_features = featureFormat(
    data_dict, features_list_no_new, sort_keys=True)
labels, features_no_new = targetFeatureSplit(data_no_new_features)
for select_number in range(1, 10):
    features_list, features_selected = selectKbestFeatures(
        select_number, features_no_new,False)
    print "特征个数：", select_number
    test_classifier(myGaussianNB(features_selected, labels), data_dict, features_list)


###测试加了新特征朴素贝叶斯和决策树算法的性能
data = featureFormat(my_dataset, features_extracted, sort_keys=True)
labels, features = targetFeatureSplit(data)
for select_number in range(1,10):
    features_list,features_selected = selectKbestFeatures(select_number,features,False) 
    print "特征个数：",select_number
    print "朴素贝叶斯算法评估："
    test_classifier(myGaussianNB(features_selected, labels),
                    my_dataset, features_list)
    print "决策树算法评估："
    test_classifier(myDecisionTree(features_selected,
                                   labels, False), my_dataset, features_list)

###决策树性能最佳时的交叉检验
features_list, features_selected = selectKbestFeatures(1, features,False)
myDecisionTree(features_selected, labels, print_score=True)

###保持最终的分类器，数据集和特征列表
print "最终选择的得分最高的6个特征及其得分为："
features_list, features_selected = selectKbestFeatures( 6, features)
clf = myGaussianNB(features_selected, labels, True)  # 决策树性能最佳时的交叉检验

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

