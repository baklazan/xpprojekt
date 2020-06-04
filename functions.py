import pickle


def save(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
