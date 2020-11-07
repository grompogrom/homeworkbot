def save_users(file):
    import pickle
    with open('users_info.picle', 'wb') as f:
        pickle.dump(file, f)


def load_users():
    import pickle
    users = {}
    with open('users_info.picle', 'rb') as r:
        users = pickle.load(r)
    return users


def save_reged(file):
    import pickle
    with open('reged.picle', 'wb') as f:
        pickle.dump(file, f)


def load_reged():
    import pickle
    users = []
    with open('reged.picle', 'rb') as r:
        users = pickle.load(r)
    return users


if __name__ == '__main__':
    save_users({})
    save_reged([])