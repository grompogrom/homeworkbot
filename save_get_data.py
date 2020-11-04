def save_data(file):
    import pickle
    with open('data.picle', 'wb') as f:
        pickle.dump(file,f)


def load_data():
    import  pickle
    with open('data.picle', 'rb') as r:
        users = pickle.load(r)
    return users


if __name__ == '__main__':
    data = {'121':'srfd'}
    save_data(data)
    del data
    data = load_data()
    print(data)