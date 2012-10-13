from time import sleep
from functools import reduce
import sqlite3

EMPTY_INDEX = '<index n/a>'
EMPTY_KEY_CODE = '<code n/a>'
EMPTY_CHAR = '<char n/a>'
EMPTY_TIME = '<time n/a>'
EMPTY_DATE = '<date n/a>'

reset_codes = {36: "\n", 48: "<TAB>", 51: "<BACK>"}

class CharTime:

    def __init__(self, index=EMPTY_INDEX):
        self.char = EMPTY_CHAR
        self.code = EMPTY_KEY_CODE
        self.date = EMPTY_DATE
        self.time = EMPTY_TIME
        self.index = index

    def set_info(self, str):
        str = str.replace('" "', "~~~~~")
        words = str.split()
        for i, word in enumerate(words):
            word = word.replace("~~~~~", '" "')

            # set date and time
            if i == 0:
                self.date = word
                continue
            if i == 1:
                self.time = word
                continue

            # set char and charcode
            word = word.replace('"="', "^^^^^")
            elements = word.split("=")
            if len(elements) < 2:
                continue
            field = elements[0]
            info = elements[1]
            info = info.replace("^^^^^", '"="')
            if field == "chars":
                info = info.replace('"', '')
                self.char = info
            elif field == "keyCode":
                self.code = int(info)
                self.reset()

    def reset(self):
        if self.code in reset_codes:
            self.char = reset_codes[self.code]

    def __repr__(self):
        #return "CharTime(char={0}, code={1}, date={2}, time={3})".format(self.char, self.code, self.date, self.time)
        return "CT({0}, {1})".format(self.char, self.time)

class WordTime(CharTime):
    def set_fields(self, char, word=None):
        if word:
            self.char = word
        else:
            self.char = char.char
        self.code = char.code
        self.date = char.date
        self.time = char.time
        self.index = char.index

def make_keycode_dict():
    keycodes = {}
    f = open('./raw_data/one_of_key.txt', 'r')
    content = f.read()

    chars, dict = make_char_list_dict(content)
    for key, value in dict.items():
        keycodes[key] = value.code
    return keycodes

def parse():
    time_dict = {}
    word_dict = {}

    f = open('./raw_data/output.txt', 'r') #second character for different reading / writing modes
    content = f.read()

    #keycodes = make_keycode_dict()
    #print(keycodes)

    chars, chars_dict = make_char_list_dict(content)
    #print(reduce(lambda x, y: x + y, [len(chars_dict[key]) for key in chars_dict]))
    output_str, time_dict, word_dict = make_timeword_dictionaries(chars)
    return output_str, time_dict, word_dict

def make_char_list_dict(content):
    chars = []
    chars_dict = {}
    lines = content.split('\n')
    for line in lines:
        char_object = CharTime()
        char_object.set_info(line)
        chars.append(char_object)
        if char_object.char not in chars_dict:
            chars_dict[char_object.char] = []
        chars_dict[char_object.char].append(char_object)
    return chars, chars_dict

def make_timeword_dictionaries(chars_list):
    def add_to_dictionaries(word, value):
        if word not in word_dict:
            word_dict[word] = []
        word_dict[word].append(value)
        time_dict[value.time] = value
    output = []
    word_dict = {}
    time_dict = {}
    current_word = []
    length = len(chars_list)
    for i, char in enumerate(chars_list):
        if char.code in reset_codes:
            if len(output) > 0 and char.code == 51: #backspace
                output.pop(len(output) - 1)
            else:
                output.append(char.char)
            word = WordTime()
            word.set_fields(char)
            add_to_dictionaries(char.char, word)

            word.set_fields(char, "".join(current_word).strip())
            add_to_dictionaries(word.char, word)
            current_word = []
        else:
            if char.code == 49 or i == length - 1: #space
                current_word.append(char.char)
                word = WordTime()
                word.set_fields(char, "".join(current_word).strip())
                add_to_dictionaries(word.char, word)
                current_word = []
            else:
                current_word.append(char.char)
            output.append(char.char)
    output_str = "".join(output)
    # print(time_dict)
    return output_str, time_dict, word_dict

if __name__ == '__main__':
    conn = sqlite3.connect('testing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE info (word text, time text, date text)''')
    output_str, time_dict, word_dict = parse()
    insertions = []
    for word, chartimes in word_dict.items():
        for chartime in chartimes:
            insertions.append((word, chartime.time, chartime.date))
    c.executemany('INSERT INTO info VALUES (?, ?, ?)', insertions)
    conn.commit()
    conn.close()
