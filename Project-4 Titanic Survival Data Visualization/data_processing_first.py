import pandas as pd

data = pd.read_csv("train.csv")

data.head()



# 计算所有乘客的生存率和死亡率
survive = data['Survived'].value_counts()
people = data['PassengerId'].count()
survived_ratio = survive/people



# 计算不同类别乘客的生存率

############# Pclass (Ticket class) ##############

class_amount = data['Pclass'].value_counts()
class_1_survived_ratio = (data[(data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[1])
class_2_survived_ratio = (data[(data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[2])
class_3_survived_ratio = (data[(data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[3])



############# 年龄 ##############
#年龄为空的不计入

minor_survived_ratio = (data[(data['Age'] <= 18) & (data['Survived'] == 1)]['PassengerId'].count()) \
                      /float(data[data['Age'] <= 18]["PassengerId"].count())
elder_survived_ratio = (data[(data['Age'] >= 60) & (data["Survived"]==1)]['PassengerId'].count()) \
                      /float(data[data['Age'] >= 60]["PassengerId"].count())
else_survived_dead_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].value_counts()
else_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].count()
else_survived_ratio = else_survived_dead_amount[1]/float(else_amount)


##################### 性别 ##########################
female = data[data['Sex']=='female']['Survived'].value_counts()
male = data[data['Sex']=='male']['Survived'].value_counts()

df = pd.DataFrame(data = [female,male])
df.index = ['female','male']
df.columns = ['dead','survived']
df

female_survived_ratio = df.loc['female']['survived'] \
    /float(df.loc['female']['survived']+df.loc['female']['dead'])
male_survived_ratio = df.loc['male']['survived'] \
    /float(df.loc['male']['survived']+df.loc['male']['dead'])



data_sub = [{"type": "all", "category": "survived", "percentage": survived_ratio[1]}, \
            {"type": "all", "category": "dead", "percentage": survived_ratio[0]}, \
            {"type": "sex", "category": "female survived", "percentage": female_survived_ratio}, \
            {"type": "sex", "category": "male survived", "percentage": male_survived_ratio}, \
            {"type": "age", "category": "minor(<=18) survived", "percentage": minor_survived_ratio},\
            {"type": "age", "category": "elder(>=60) survived", "percentage": elder_survived_ratio},\
            {"type": "age", "category": "else survived", "percentage": else_survived_ratio}, \
            {"type": "Ticket class", "category": "class1 survived", "percentage": class_1_survived_ratio},\
            {"type": "Ticket class", "category": "class2 survived", "percentage": class_2_survived_ratio},\
            {"type": "Ticket class", "category": "class3 survived", "percentage": class_3_survived_ratio}]
df2 = pd.DataFrame(data = data_sub)
df2

df2.to_csv("Titanic_first.csv", sep=',', encoding='utf-8')
