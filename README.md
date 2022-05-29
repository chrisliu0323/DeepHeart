# DeepHeart

This repository contains source code for two tasks in the project DeepHeart--data processing and modelling.
The pdf file `project file` gives you a general idea of what this project includes.


## Data processing
`Data_url&label.xlsx` stores the raw data. There are 3 columns in the spreadsheet, data ID, url, and sentiment label.

`spreadsheet_connect.py` obtains the selected information in 'Data_url&label.xlsx through googlesheet API and returns a dataframe.

`webcrawl.py` extracts text on the webpage from the given url and cleanse the text to improve the quality of data. 

`split_dataset.py` splits the data into training set and testing set. Then the datasets will be saved in the way that can be directly processed by deep learning model Bert.

These 3 python program automates the process of converting large amounts of raw data into prepared data.

## Modelling
`model train&build.py` trains the data using Google Bert model, fine-tuned by our own dataset. It uses the preprocessing and encoder model below, both referenced from the TensorFlow official website:https://hub.tensorflow.google.cn/tensorflow/bert_zh_preprocess/3 and https://hub.tensorflow.google.cn/tensorflow/bert_zh_L-12_H-768_A-12/4.

`model inference.py` returns a sentiment label after sending an user input into a saved model. It should be used in deployment stage.


## Environment
The scipts in Modelling were run in Python 3.6 environment. 
The important requirements are
```
pip install tensorflow-text==2.8.*
pip install tf-models-official==2.7.0
```
Note that the requirements may not always be compatible with some of the larter versions of python. 
Also, GPU computing resource is recommended when training with higher epochs.
