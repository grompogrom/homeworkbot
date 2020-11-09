def message_parser(json):
    text = ''
    for lesson, note in json.items():
        if not note or note == '':
            note = 'Заданий нет'
        text += f'{lesson}: {note} \n'
    return text


if __name__ == '__main__':
    pass
