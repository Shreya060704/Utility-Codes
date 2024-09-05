from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
import pickle

app = Flask(_name_)

# Load label encoders
with open('label_encoders.pkl', 'rb') as le_file:
    label_encoders = pickle.load(le_file)

# Load ordinal encoder
with open('ordinal_encoder.pkl', 'rb') as oe_file:
    ordinal_encoder = pickle.load(oe_file)

# Load the trained model
model = tf.keras.models.load_model('model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract user inputs from form
    attent_span = request.form['attent_span']
    behaviour = request.form['behaviour']
    learn_style = request.form['learn_style']
    strength = request.form['strength']
    challenges = request.form['challenges']

    # Compute mean for attention span
    attent_span = compute_mean(attent_span)

    # Convert categorical features
    behaviour_encoded = encode_categorical('Behaviour', behaviour)
    learn_style_encoded = encode_categorical('Learning Style', learn_style)
    strength_encoded = encode_categorical('Strength', strength)
    challenges_encoded = encode_categorical('Challenges', challenges)

    # Convert ordinal feature
    attent_span_encoded = ordinal_encoder.transform([[attent_span]])[0][0]

    # Prepare features for prediction
    features = np.array([[attent_span_encoded, behaviour_encoded, learn_style_encoded, strength_encoded, challenges_encoded]])

    # Make prediction
    prediction = model.predict(features)
    predicted_class_index = np.argmax(prediction, axis=-1)[0]

    # Decode the predicted class
    decoded_prediction = decode_prediction(predicted_class_index)

    # Return prediction result
    return render_template('result.html', prediction=decoded_prediction)

def compute_mean(interval_str):
    if ' to ' in interval_str:
        start, end = interval_str.split(' to ')
        return (float(start) + float(end)) / 2
    elif 'upto ' in interval_str:
        numeric_part = interval_str.replace('upto ', '')
        return float(numeric_part)
    return float(interval_str)

def encode_categorical(encoder_key, value):
    try:
        encoder = label_encoders[encoder_key]
        if value not in encoder.classes_:
            raise ValueError(f"Unexpected value: {value}")
        return encoder.transform([value])[0]
    except ValueError as e:
        # Handle unexpected value error
        print(f"Encoding error: {e}")
        # You can return a default value or handle the error as needed
        return -1  # Or another suitable default value

def decode_prediction(predicted_class_index):
    # Assuming the model has a single output layer and a set of classes
    # The label encoders should be consistent with the model's output classes
    # Here you need to provide the mapping from index to label
    # For simplicity, assuming a single encoder for demonstration
    try:
        # Assuming the encoder for prediction is 'Behaviour' or the relevant encoder
        encoder = label_encoders['Behaviour']
        return encoder.classes_[predicted_class_index]
    except Exception as e:
        print(f"Decoding error: {e}")
        return "Unknown"

if _name_ == '_main_':
    app.run(debug=True)
