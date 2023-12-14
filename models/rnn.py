import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt
from keras.layers import SimpleRNN, Bidirectional, BatchNormalization
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

def train_and_save_model():
    # Load the dataset
    df = pd.read_csv('importfichier.csv', header=None)

    # Convert all feature columns to numeric and set non-convertible values to NaN
    for col in df.columns[:-1]:  # Excluding the last column
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Removing rows with NaN values
    df.dropna(inplace=True)  

    # Separate features and labels
    X = df.iloc[:, :-1].values  # All columns except the last one
    y = df.iloc[:, -1].values   # Only the last column

    # Scale the features
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    # Reshape X to fit the RNN model (samples, time steps, features)
    X = X.reshape((X.shape[0], 1, X.shape[1]))
    
    # Encode the labels
    encoder = OneHotEncoder(sparse=False)
    y_encoded = encoder.fit_transform(y.reshape(-1, 1))

    # Define the RNN model
    model_rnn = Sequential()
    model_rnn.add(Bidirectional(SimpleRNN(30, activation='relu', return_sequences=True), input_shape=(X.shape[1], X.shape[2])))
    model_rnn.add(BatchNormalization())
    model_rnn.add(SimpleRNN(32, activation='relu'))
    model_rnn.add(Dropout(0.3))
    model_rnn.add(Dense(16, activation='relu'))
    model_rnn.add(Dense(y_encoded.shape[1], activation='softmax'))

    # Compile the model with categorical_crossentropy loss function
    model_rnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Add EarlyStopping as a callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Train the model
    history = model_rnn.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test), callbacks=[early_stopping])
    model_rnn.save('rnn_model.h5')

    # Save the scaler to use it in predict.py and scale the realtime data
    joblib.dump(scaler, 'rnn_scaler.joblib')

    # Access the loss and accuracy values
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']
    train_accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']

    # Make predictions on the test set
    y_pred = model_rnn.predict(X_test)

    # Convert predictions to classes
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)

    # Calculate the accuracy
    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    print(f"Accuracy on the test set: {accuracy * 100:.2f}%")
    
    # Calculate precision, recall, and F1-score
    precision = precision_score(y_test_classes, y_pred_classes, average='weighted')
    recall = recall_score(y_test_classes, y_pred_classes, average='weighted')
    f1 = f1_score(y_test_classes, y_pred_classes, average='weighted')

    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")

    # Confusion matrix
    cm = confusion_matrix(y_test_classes, y_pred_classes)
    print("Confusion Matrix:")
    print(cm)
    
    # Plot loss
    plt.figure(figsize=(10, 5))
    plt.plot(train_loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Plot accuracy
    plt.figure(figsize=(10, 5))
    plt.plot(train_accuracy, label='Training Accuracy')
    plt.plot(val_accuracy, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

train_and_save_model()
