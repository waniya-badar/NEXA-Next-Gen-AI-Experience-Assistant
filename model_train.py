#.\tf_env\Scripts\activate  
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

from sklearn.preprocessing import LabelEncoder

with open("intents.json") as file:
    data=json.load(file)

training_sentence=[]
training_labels=[]
labels=[]
responses=[]

#x are the sentences meaning patterns
# y (tags) are their labels , jinper ham train karenge 
#for example x=how are you and its y=greeting etc

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentence.append(pattern) #x feature for ttraining
        training_labels.append(intent['tag']) # y for the trainingg
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
        
number_of_classes=len(labels)

print(number_of_classes)

label_encoder = LabelEncoder()
label_encoder.fit(training_labels) # to convert it into number , tags like 1 ,greeting -1  goofbye 2 ..etc
training_labels= label_encoder.transform(training_labels)

vocab_size=1000
ovv_token = "<OOV>" #Stands for "Out Of Vocabulary" token. Any word not seen during training will be replaced with this token (e.g., <OOV>).
max_len=50
embedding_dim=16

#nlp starts from here

tokenizer=Tokenizer(num_words  =vocab_size, oov_token=ovv_token)
tokenizer.fit_on_texts(training_sentence) #Builds the vocabulary from the training_sentence list. Assigns each word a unique index.
word_index=tokenizer.word_index #Stores a dictionary mapping each word → its unique index, based on frequency (most common word gets lowest index).
sequences = tokenizer.texts_to_sequences(training_sentence) # Converts each sentence into a list of integers using word_index.
padded_sequences=pad_sequences(sequences,truncating='post',maxlen=max_len) #Ensures all sequences are exactly 50 tokens long and If a sentence is shorter than 50, zeros are added at the beginning (can be changed with padding='post')

model=Sequential()
model.add(Embedding(vocab_size ,embedding_dim,input_length=max_len )) #Converts each word index into a dense vector of fixed size (learned during training)
model.add(GlobalAveragePooling1D()) #takes average of the embedding output and reduces it to a single 16-element vector by avging across all 50 timestamps
model.add(Dense(16, activation="relu")) #fully densed layer with 16 neurons
model.add(Dense(16, activation="relu"))
model.add(Dense(number_of_classes, activation="softmax"))#final output layer for multi-class classification, ensures output values are between 0 and 1
#softwax gives probability distribution acroos no.of classes

model.compile(loss='sparse_categorical_crossentropy', optimizer="adam", metrics=["accuracy"]) #'sparse_categorical_crossentropy' used when labels are integers
model.summary()

history=model.fit(padded_sequences, np.array(training_labels), epochs=1000) #trains the data, more epochs mean more accuracy

model.save("chat_model.h5") #Saves the entire model to an HDF5 file (.h5).

with open("tokenizer.pkl","wb") as f: #Saves the tokenizer object (used for converting text to sequences) into a .pkl file using pickle.
    pickle.dump(tokenizer,f,protocol=pickle.HIGHEST_PROTOCOL) #HIGHEST_PROTOCOL: Makes the file efficient and compatible with latest Python versions.

with open("label_encoder.pkl","wb") as encoder_file:
    pickle.dump(label_encoder,encoder_file,protocol=pickle.HIGHEST_PROTOCOL)

