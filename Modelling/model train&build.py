# !pip install tensorflow-text==2.8.*
# !pip install tf-models-official==2.7.0

import datetime as dt
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optimizer


###assign preprocess model and encoder model by referencing to TensorFlow official website
tfhub_handle_preprocess = "https://hub.tensorflow.google.cn/tensorflow/bert_zh_preprocess/3"
tfhub_handle_encoder = "https://hub.tensorflow.google.cn/tensorflow/bert_zh_L-12_H-768_A-12/4"
bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)
bert_model = hub.KerasLayer(tfhub_handle_encoder)



###load dataset and split training dataset
AUTOTUNE = tf.data.AUTOTUNE
batch_size = 16
seed = 42


#import training dataset
raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    "1~421___0225-1932/train",
    batch_size=batch_size,
    validation_split=0.2,
    subset="training",
    seed=seed)

class_names = raw_train_ds.class_names
train_ds = raw_train_ds.cache().prefetch(buffer_size=AUTOTUNE)

#import validation set
val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    "1~421___0225-1932/train",
    batch_size=batch_size,
    validation_split=0.2,
    subset="validation",
    seed=seed)

val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

#import testing dataset
test_ds = tf.keras.utils.text_dataset_from_directory(
    "1~421___0225-1932/test",
    batch_size=batch_size)

test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)



###define model parameters
def build_classifier_model():
  text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
  preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
  encoder_inputs = preprocessing_layer(text_input)
  encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
  outputs = encoder(encoder_inputs)
  net = outputs['pooled_output']
  net = tf.keras.layers.Dropout(0.5)(net)

  net = tf.keras.layers.Dense(6, activation='softmax', name='classifier')(net)
  return tf.keras.Model(text_input, net)

classifier_model = build_classifier_model()
epochs = 5
steps_per_epoch = tf.data.experimental.cardinality(train_ds).numpy()
num_train_steps = steps_per_epoch * epochs
print(num_train_steps)
num_warmup_steps = int(0.1*num_train_steps)

init_lr = 3e-5
optimizer = optimization.create_optimizer(init_lr=init_lr,                                          num_train_steps=num_train_steps,                                          num_warmup_steps=num_warmup_steps,
optimizer_type='adamw')
loss = tf.keras.losses.SparseCategoricalCrossentropy()
metrics = tf.metrics.SparseCategoricalAccuracy()

classifier_model.compile(optimizer=optimizer,
                         loss=loss,
                         metrics=metrics)

current_time=dt.datetime.now()


history = classifier_model.fit(x=train_ds,
                               validation_data=val_ds,
                               epochs=epochs)


###train
print("training took time:", dt.datetime.now()-current_time)

loss, accuracy = classifier_model.evaluate(test_ds)

print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')



###save model
dataset_name = 'model_20220225'
saved_model_path = './{}_bert'.format(dataset_name.replace('/', '_'))

classifier_model.save(saved_model_path, include_optimizer=False)



###test the model saved in memory
import numpy as np

def print_my_examples(inputs, results):
  result_for_printing = \
    [f'input: {inputs[i]:<30} : class: {class_names[np.argmax(results[i])] }'
                         for i in range(len(inputs))]
  print(*result_for_printing, sep='\n')
  print()

examples = [
    '我是日記',
]

example_result = classifier_model(tf.constant(examples))
print_my_examples(examples,example_result)
