# -*- coding: utf-8 -*-

import pandas as pd

data = pd.read_csv("train.csv")

# 计算所有乘客的生存率和死亡率
survive = data['Survived'].value_counts()
people = data['PassengerId'].count()
survived_ratio = survive/people

# 计算不同类别乘客的生存率


############# Pclass (Ticket class) ##############

class_amount = data['Pclass'].value_counts()
class1_survived_ratio = (data[(data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[1])
class2_survived_ratio = (data[(data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[2])
class3_survived_ratio = (data[(data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[3])



############# 年龄 ##############
#年龄为空的不计入
minor_amount = data[data['Age'] <= 18]["PassengerId"].count()
minor_survived_ratio = (data[(data['Age'] <= 18) & (data['Survived'] == 1)]['PassengerId'].count()) \
                      /float(minor_amount)

elder_amount = data[data['Age'] >= 60]["PassengerId"].count()
elder_survived_ratio = (data[(data['Age'] >= 60) & (data["Survived"]==1)]['PassengerId'].count()) \
                      /float(elder_amount)
else_survived_dead_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].value_counts()
else_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].count()
else_survived_ratio = else_survived_dead_amount[1]/float(else_amount)



##################### 性别 ##########################
female = data[data['Sex']=='female']['Survived'].value_counts()
male = data[data['Sex']=='male']['Survived'].value_counts()

df = pd.DataFrame(data = [female,male])
df.index = ['female','male']
df.columns = ['dead','survived']

female_accout = df.loc['female']['survived']+df.loc['female']['dead']
female_survived_ratio = df.loc['female']['survived'] \
    /float(female_accout)

male_accout = df.loc['male']['survived']+df.loc['male']['dead']
male_survived_ratio = df.loc['male']['survived'] \
    /float(male_accout)






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

my_dataset = [{"filter": "all", "category": "survived", "percentage": survived_ratio[1], "amount":str(survive[1])}, \
            {"filter": "all", "category": "dead", "percentage": survived_ratio[0], "amount":str(survive[0])}, \
            {"filter": "Ticket class", "category": "class 1", "survived percentage": class1_survived_ratio, "amount":str(class_amount[1])},\
            {"filter": "Ticket class", "category": "class 2", "survived percentage": class2_survived_ratio, "amount":str(class_amount[2])},\
            {"filter": "Ticket class", "category": "class 3", "survived percentage": class3_survived_ratio, "amount":str(class_amount[3])},\
            {"filter": "age", "category": "minor(<=18)", "survived percentage": minor_survived_ratio, "amount":str(minor_amount)},\
            {"filter": "age", "category": "elder(>=60)", "survived percentage": elder_survived_ratio, "amount":str(elder_amount)},\
            {"filter": "age", "category": "else", "survived percentage": else_survived_ratio, "amount":str(else_amount)}, \
            {"filter": "sex", "category": "female", "survived percentage": female_survived_ratio,"amount":str(female_accout)}, \
            {"filter": "sex", "category": "male", "survived percentage": male_survived_ratio,"amount":str(male_accout)}, \
            {"filter": "Ticket class+sex", "category": "class 1", "survived percentage": class1_male_survived_ratio,\
             "type":"male","amount": str(class_male_amount[1])},\
            {"filter": "Ticket class+sex", "category": "class 2", "survived percentage": class2_male_survived_ratio, \
            "type":"male","amount": str(class_male_amount[2])},\
            {"filter": "Ticket class+sex", "category": "class 3", "survived percentage": class3_male_survived_ratio,\
             "type":"male","amount": str(class_male_amount[3])},\
            {"filter": "Ticket class+sex", "category": "class 1", "survived percentage": class1_female_survived_ratio, \
            "type":"female","amount":str(class_female_amount[1])},\
            {"filter": "Ticket class+sex", "category": "class 2", "survived percentage": class2_female_survived_ratio, \
            "type":"female","amount":str(class_female_amount[2])},\
            {"filter": "Ticket class+sex", "category": "class 3", "survived percentage": class3_female_survived_ratio, \
            "type":"female","amount":str(class_female_amount[3])}]

df2 = pd.DataFrame(data = my_dataset)
df2

df2.to_csv("Titanic_final.csv", sep=',', encoding='utf-8')
