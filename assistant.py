import os
import librosa
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

duration = 5  # seconds
fs = 44100
word_ids = {}

## 3rd and 4th step

#file_path = 'train1.wav'

# Step 1: Preprocess the audio data to extract features using MFCCs
def extract_features(file_path):
    audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return mfccs_processed


# Step 2: Prepare the transcription data by encoding the text using one-hot encoding
def encode_text(text):
    # Tokenize the text into individual words
    #print(text)
    words = text.lower().split()
    global word_ids
    # Create a dictionary mapping each word to a unique integer ID
    word_ids = {word: i for i, word in enumerate(set(words))}
    #print(word_ids)
    # Encode the text using one-hot encoding
    encoded_text = [to_categorical(word_ids[word], num_classes=len(word_ids)) for word in words]
    #print(encoded_text)
    return encoded_text


# Step 3: Split the dataset into training and validation sets
def load_data():
    # Load the dataset (audio recordings and their corresponding transcriptions)
    audio_dir = 'C:\\Users\\User\\PycharmProjects\\projectAlexa\\audio'
    transcripts_dir = 'C:\\Users\\User\\PycharmProjects\\projectAlexa\\transcripts'
    audio_files = os.listdir(audio_dir)
    transcriptions = []
    for file_name in audio_files:
        # Extract the transcription text from the corresponding transcript file
        transcript_file_path = os.path.join(transcripts_dir, file_name[:-4] + '.txt')
        with open(transcript_file_path, 'r') as f:
            transcription = f.read().strip()
        transcriptions.append(transcription)

    # Extract features and encode transcriptions for each audio file
    features = np.array([extract_features(os.path.join(audio_dir, file_path)) for file_path in audio_files])
    #print(features)
    transcriptions_encoded = np.array([encode_text(text) for text in transcriptions],dtype=object)
    #print(transcriptions)
    #print(transcriptions_encoded)

    # Reshape the features array to have the correct shape
    #features = np.reshape(features, (features.shape[0], features.shape[1], features.shape[0], 1))

    # Split the dataset into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(features, transcriptions_encoded, test_size=0.2, random_state=42)

    return X_train, X_val, y_train, y_val


# Step 4: Train a CNN on the extracted features and the corresponding transcriptions
def train_model():
    X_train, X_val, y_train, y_val = load_data()
    print(55)
    # Define the CNN model architecture
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=X_train.shape[1:]))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=32, epochs=10)

    return model

# Step 5:
# Load the trained model
model = train_model()

# Load the new audio file
new_audio_file_path = 'check1.wav'
new_audio_features = extract_features(new_audio_file_path)

# Use the trained model to predict the transcription
prediction = model.predict(np.array([new_audio_features]))

# Convert the predicted transcription from one-hot encoding to text
word_ids = {i: word for word, i in word_ids.items()}
predicted_words = [word_ids[np.argmax(one_hot_encoding)] for one_hot_encoding in prediction[0]]
predicted_transcription = ' '.join(predicted_words)
print(predicted_transcription)
