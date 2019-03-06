import pandas as pd

data = pd.read_csv("train.csv")

data.head()



# calculate survive rate and dead rate in all passengers
survive = data['Survived'].value_counts()
people = data['PassengerId'].count()
survived_ratio = survive/people



# calculate survive percentage in different type
##################### sex ##########################
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



############# age ##############
data[data['Age'].isnull()]['PassengerId'].count()

minor_survived_ratio = (data[(data['Age'] <= 18) & (data['Survived'] == 1)]['PassengerId'].count()) \
                      /float(data[data['Age'] <= 18]["PassengerId"].count())
elder_survived_ratio = (data[(data['Age'] >= 60) & (data["Survived"]==1)]['PassengerId'].count()) \
                      /float(data[data['Age'] >= 60]["PassengerId"].count())
else_survived_dead_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].value_counts()
else_amount = data[(data['Age'] > 18) & (data['Age'] < 60)]['Survived'].count()
else_survived_ratio = else_survived_dead_amount[1]/float(else_amount)


############# Pclass ##############

class_amount = data['Pclass'].value_counts()
class_1_survived_ratio = (data[(data['Pclass'] == 1) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[1])
class_2_survived_ratio = (data[(data['Pclass'] == 2) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[2])
class_3_survived_ratio = (data[(data['Pclass'] == 3) & (data["Survived"]==1)]['PassengerId'].count()) \
                        /float(class_amount[3])

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

data_sub = [{"type": "all", "category": "survived", "percentage": survived_ratio[1]}, \
            {"type": "all", "category": "dead", "percentage": survived_ratio[0]}, \
            {"type": "sex", "category": "female survived", "percentage": female_survived_ratio}, \
            {"type": "sex", "category": "male survived", "percentage": male_survived_ratio}, \
            {"type": "age", "category": "minor(<=18) survived", "percentage": minor_survived_ratio},\
            {"type": "age", "category": "elder(>=60) survived", "percentage": elder_survived_ratio},\
            {"type": "age", "category": "else survived", "percentage": else_survived_ratio}, \
            {"type": "class", "category": "class1 survived", "percentage": class_1_survived_ratio},\
            {"type": "class", "category": "class2 survived", "percentage": class_2_survived_ratio},\
            {"type": "class", "category": "class3 survived", "percentage": class_3_survived_ratio},\
            {"type": "class+female", "category": "class1+female survived", "percentage": class_1_female_survived_ratio},\
            {"type": "class+female", "category": "class2+female survived", "percentage": class_2_female_survived_ratio},\
            {"type": "class+female", "category": "class3+female survived", "percentage": class_3_female_survived_ratio},\
            {"type": "class+male", "category": "class1+male survived", "percentage": class_1_male_survived_ratio},\
            {"type": "class+male", "category": "class2+male survived", "percentage": class_2_male_survived_ratio},\
            {"type": "class+male", "category": "class3+male survived", "percentage": class_3_male_survived_ratio}]
df2 = pd.DataFrame(data = data_sub)
df2

df2.to_csv("Titanic.csv", sep=',', encoding='utf-8')
