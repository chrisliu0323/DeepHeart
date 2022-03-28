import os.path
import pandas as pd
from webcrawl import path_csv
from webcrawl import spec


#read from the csv file and shuffle
all_df = pd.read_csv(path_csv)
shuffled = all_df.sample(frac=1).reset_index(drop=True)


#split the dataset into training set(8) and testing set(2)
train_df = shuffled.iloc[:int(len(shuffled)*0.8)]
test_df = shuffled.iloc[int(len(shuffled)*0.8):]


#put the training dataset and testing dataset into directoy according
#to the format required by Google Bert algorithm

path1="C:\python\workspace\group4\\" + spec + "\\train\\1\\"
path2="C:\python\workspace\group4\\" + spec + "\\train\\2\\"
path3="C:\python\workspace\group4\\" + spec + "\\train\\3\\"
path4="C:\python\workspace\group4\\" + spec + "\\train\\4\\"
path5="C:\python\workspace\group4\\" + spec + "\\train\\5\\"
path6="C:\python\workspace\group4\\" + spec + "\\test\\1\\"
path7="C:\python\workspace\group4\\" + spec + "\\test\\2\\"
path8="C:\python\workspace\group4\\" + spec + "\\test\\3\\"
path9="C:\python\workspace\group4\\" + spec + "\\test\\4\\"
path10="C:\python\workspace\group4\\" + spec + "\\test\\5\\"

mypaths=[path1,path2,path3,path4,path5,path6,path7,path8,path9,path10]

for i in mypaths:
  os.makedirs(i, exist_ok=True)


for i, row in train_df.iterrows():
  if row["label"] == 1:
    with open(path1 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 2:
    with open(path2 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 3:
    with open(path3 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 4:
    with open(path4 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 5:
    with open(path5 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))


for i, row in test_df.iterrows():
  if row["label"] == 1:
    with open(path6 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 2:
    with open(path7 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 3:
    with open(path8 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 4:
    with open(path9 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))
  if row["label"] == 5:
    with open(path10 + str(i) + ".txt", "w", encoding="UTF-8") as f:
      f.write(str(row["review"]))