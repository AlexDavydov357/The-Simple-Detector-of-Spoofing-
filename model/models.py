from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# simpl classifications model
def classifier(vector_length):
    model = Sequential()
    model.add(Dense(2048, input_dim=vector_length, activation='relu'))
    model.add(Dropout(0.30))
    model.add(Dense(2048, activation='relu'))
    model.add(Dropout(0.30))

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.30))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.30))

    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.30))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.30))

    model.add(Dense(1, activation='linear'))
    return model
