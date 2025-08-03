import json
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random

# Load intents
with open("intents.json") as file:
    data = json.load(file)

# Load trained model
model = keras.models.load_model("chat_model.h5")

# Load tokenizer and label encoder
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Chat loop
while True:
    input_text = input("Enter your command -> ")
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=50, truncating='post')
    result = model.predict(padded_sequences)
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag[0]:  
            print(np.random.choice(i['responses']))
