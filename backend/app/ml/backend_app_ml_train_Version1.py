import tensorflow as tf
import numpy as np
import os
from .generate_sample_data import generate_dataset
from datetime import datetime

def build_model(K=5):
    # Input -> small conv net -> FC -> K*(4+3) outputs
    inp = tf.keras.Input(shape=(128,128,3))
    x = tf.keras.layers.Conv2D(16,3,activation='relu')(inp)
    x = tf.keras.layers.MaxPool2D()(x)
    x = tf.keras.layers.Conv2D(32,3,activation='relu')(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    out = tf.keras.layers.Dense(K*(4+3), activation='sigmoid')(x)
    model = tf.keras.Model(inputs=inp, outputs=out)
    return model

def train(output_dir="models/model_"+datetime.now().strftime("%Y%m%d_%H%M%S")):
    os.makedirs(output_dir, exist_ok=True)
    X, y = generate_dataset(200)
    K=5
    y = y.reshape((y.shape[0], K*(4+3)))
    model = build_model(K=K)
    model.compile(optimizer='adam', loss='mse')
    model.fit(X,y,epochs=3,batch_size=16,verbose=2)
    model.save(output_dir)
    print("Saved model to", output_dir)
    return output_dir

if __name__ == "__main__":
    train()