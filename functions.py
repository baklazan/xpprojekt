import pickle


def save(data):
    with open('questions.pickle', 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load():
    with open('questions.pickle', 'rb') as file:
        return pickle.load(file)
