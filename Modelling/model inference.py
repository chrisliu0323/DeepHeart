import datetime as dt
current_time=dt.datetime.now()

import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
from official.nlp import optimization

AUTOTUNE = tf.data.AUTOTUNE
batch_size = 16
seed = 42

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    "1~421___0225-1932/train",
    batch_size=batch_size,
    validation_split=0.2,
    subset="training",
    seed=seed)

#define class name
class_names = raw_train_ds.class_names


###inference the model saved from previous training
reloaded_model = tf.saved_model.load("C:\python\workspace\group4\model_20220228_bert")


import numpy as np

def print_my_examples(inputs, results):
  result_for_printing = \
    [f'input: {inputs[i]:<30} : class: {class_names[np.argmax(results[i])] }'
                         for i in range(len(inputs))]
  result_for_printing = \
      [f'{class_names[np.argmax(results[i])]}'
       for i in range(len(inputs))]
  print(*result_for_printing, sep='\n')
  print()


examples = [
    '我是日記',
]

reloaded_results = tf.sigmoid(reloaded_model(tf.constant(examples)))

print_my_examples(examples,reloaded_results)

print("inference took time:", dt.datetime.now()-current_time)