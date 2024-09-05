import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder
from imblearn.over_sampling import RandomOverSampler
import tensorflow as tf
from sklearn.metrics import classification_report
import pickle

# Load data
df = pd.read_excel('.idea/Neurodivergent(1).xlsx', sheet_name='Sheet2', nrows=198)
df = df[['Attention Span(in mins)', 'Behaviour', 'Learning Style', 'Strength', 'Challenges', 'Disorder']]

# Compute mean for 'Attention Span(in mins)'
def compute_mean(interval_str):
    if ' to ' in interval_str:
        start, end = interval_str.split(' to ')
        return (float(start) + float(end)) / 2
    elif 'upto ' in interval_str:
        numeric_part = interval_str.replace('upto ', '')
        return float(numeric_part)
    return None

df['Attention Span(in mins)'] = df['Attention Span(in mins)'].apply(compute_mean)

# Encode categorical columns
cat_cols = ['Learning Style', 'Strength', 'Behaviour', 'Challenges', 'Disorder']
enc = LabelEncoder()

for col in cat_cols:
    df[col] = df[col].astype('str')  # Ensure column is of string type
    df[col] = enc.fit_transform(df[col])

# Dynamic categories for OrdinalEncoder
unique_values = df['Attention Span(in mins)'].unique()
categories = sorted(unique_values)

# Create and fit the OrdinalEncoder
ordinal_encoder = OrdinalEncoder(categories=[categories])
df['Attention Span(in mins)'] = ordinal_encoder.fit_transform(df[['Attention Span(in mins)']])

# Save the OrdinalEncoder
with open('ordinal_encoder.pkl', 'wb') as oe_file:
    pickle.dump(ordinal_encoder, oe_file)
print("Ordinal encoder saved as 'ordinal_encoder.pkl'")

# Define scaling function
def scale_dataset(dataframe, oversample=False):
    X = dataframe[dataframe.columns[:-1]].values
    y = dataframe[dataframe.columns[-1]].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    if oversample:
        ros = RandomOverSampler()
        X, y = ros.fit_resample(X, y)
    data = np.hstack((X, np.reshape(y, (-1, 1))))
    return data, X, y

# Split data
train, valid, test = np.split(df.sample(frac=1), [int(0.6 * len(df)), int(0.8 * len(df))])

train, X_train, y_train = scale_dataset(train, oversample=True)
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)
test, X_test, y_test = scale_dataset(test, oversample=False)

print(np.sum(y_train == 0))
print(np.sum(y_train == 1))
print(np.sum(y_train == 2))

# Define and train neural network
def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Sparse Categorical Crossentropy')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_accuracy(history):
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    plt.show()

class_weights = {0: 1.0, 1: 2.0, 2: 1.0}
nn_model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

nn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])
history = nn_model.fit(
    X_train, y_train, epochs=200, batch_size=32, class_weight=class_weights,
    validation_split=0.2, verbose=0
)

y_pred = np.argmax(nn_model.predict(X_test), axis=-1)
print(classification_report(y_test, y_pred))
plot_loss(history)
plot_accuracy(history)

# Save the model
nn_model.save('model.h5')

# Save label encoders
label_encoders = {col: LabelEncoder().fit(df[col]) for col in cat_cols}
with open('label_encoders.pkl', 'wb') as le_file:
    pickle.dump(label_encoders, le_file)

print("Label encoders saved as 'label_encoders.pkl'")
