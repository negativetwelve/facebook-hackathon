from time import sleep
from functools import reduce
import sqlite3

KEY = "Key"
SCREEN = "Screen"
MOUSE = "Mouse"
TIME = 'time'

EMPTY_INDEX = '<no index>'
EMPTY_KEY_CODE = '<no code>'
EMPTY_CHAR = '<no char>'
EMPTY_TIME = '<no time>'
EMPTY_DATE = '<no date>'
EMPTY_MOD = '<no mod>'
EMPTY_POSITION = '<no position>'
EMPTY_NAME = '<no name>'
EMPTY_WINDOW = '<no window>'
empty_things = [EMPTY_INDEX, EMPTY_KEY_CODE, EMPTY_CHAR,
    EMPTY_TIME, EMPTY_DATE, EMPTY_MOD, EMPTY_POSITION,
    EMPTY_NAME, EMPTY_WINDOW]

reset_codes = {36: "\n", 48: "<TAB>", 51: "<BACK>"}

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Position({0}, {1})".format(self.x, self.y)

class Event:
    def __init__(self, time=EMPTY_TIME, date=EMPTY_DATE, index=EMPTY_INDEX, window=EMPTY_WINDOW):
        self.time = time
        self.date = date
        self.index = index
        self.window = window
        self.key = self.date

    def set_key(self, thing=None):
        if (not thing) and (thing not in empty_things):
            self.key = thing
        elif self.date not in empty_things:
            self.key = self.date

    def __repr__(self):
        return "Event({0}, {1})".format(self.date, self.time)

    def set_info(self, str, window=EMPTY_WINDOW):
        self.window = window
        words = str.split()

        # set date and time
        self.date = words[0]
        self.time = words[1]

class Screen(Event):
    def __init__(self, time=EMPTY_TIME, date=EMPTY_DATE, index=EMPTY_INDEX, window=EMPTY_WINDOW, name=EMPTY_NAME):
        Event.__init__(self, time, date, index)
        self.name = name
        self.window = window

    def set_info(self, str):
        Event.set_info(self, str)

        words = str.split()
        for word in words:
            elements = word.split("=")
            if not len(elements) >= 2:
                continue
            field = elements[0]
            item = elements[1]
            if field == 'name':
                if item != '_':
                    self.name = item.replace("_", " ")
            elif field == "owner":
                self.window = item.replace("_", " ")

        self.set_key()
    def set_key(self):
        if self.window not in empty_things:
            self.key = self.window

    def __repr__(self):
        return "Screen({0}, {1})".format(self.window, self.name)

class Mouse(Event):
    def __init__(self, time=EMPTY_TIME, date=EMPTY_DATE, index=EMPTY_INDEX,
                        position=EMPTY_POSITION, window=EMPTY_WINDOW):
        Event.__init__(self, time, date, index, window)
        self.position = position

    def set_info(self, str, window):
        Event.set_info(self, str, window)
        words = str.split()

        x = None
        y = None

        for word in words:
            elements = word.split("=")
            if not len(elements) >= 2:
                continue
            field = elements[0]
            item = elements[1]
            if field == "x":
                x = float(item)
            elif field == "y":
                y = float(item)
        self.position = Position(x, y)
        self.set_key()

    def set_key(self):
        if self.position not in empty_things:
            self.key = self.position

    def __repr__(self):
        return "Mouse({0})".format(self.position)

class Key(Event):

    def __init__(self, time=EMPTY_TIME, date=EMPTY_DATE, index=EMPTY_INDEX, window=EMPTY_WINDOW,
                            char=EMPTY_CHAR, code=EMPTY_KEY_CODE, mod=EMPTY_MOD):
        Event.__init__(self, time, date, index, window)
        self.char = char
        self.code = code
        self.mod = mod

    def set_info(self, str, window):
        Event.set_info(self, str, window)
        str = str.replace('" "', "~~~~~")
        words = str.split()
        for i, word in enumerate(words):
            word = word.replace("~~~~~", '" "')

            # set char, key, mods
            word = word.replace('"="', "^^^^^")
            elements = word.split("=")
            if len(elements) < 2:
                continue
            field = elements[0]
            info = elements[1]
            info = info.replace("^^^^^", '"="')
            if field == "char":
                info = info.replace('"', '')
                self.char = info
            elif field == "key":
                self.code = int(info)
            elif field == "mods":
                info = info.replace("[", " ")
                info = info.replace("]", " ")
                info = info.replace("'", " ")
                info = info.replace("'", " ")
                info = info.strip()
                if info != "":
                    self.mod = info
        self.reset()

    def set_key(self):
        if self.char not in empty_things:
            self.key = self.char

    def reset(self):
        """Resets the char attribute if it is a whitespace character to something
        more readily printed and resets char if there is a mod"""
        if self.code in reset_codes:
            self.char = reset_codes[self.code]
        if self.mod != EMPTY_MOD:
            self.char = "<{0}-{1}>".format(self.mod, self.char)
        self.set_key()

    def __repr__(self):
        #return "CharTime(char={0}, code={1}, date={2}, time={3})".format(self.char, self.code, self.date, self.time)
        return "Key({0})".format(self.char)

    def __str__(self):
        return self.char

class Word(Key):
    def __init__(self, other=None):
        if other:
            Key.__init__(self, other.time, other.date, other.index, other.window, other.char, 
                            other.code, other.mod)
        else:
            Key.__init__(self)

    def reset_char(self, new_char):
        self.char = new_char

    def __repr__(self):
        return "Word({0})".format(self.char)

def make_keycode_dict():
    assert False; "I'm making this error because it shouldn't work right now"
    keycodes = {}
    f = open('./raw_data/one_of_key.txt', 'r')
    content = f.read()

    chars, dict = make_char_list_dict(content)
    for key, value in dict.items():
        keycodes[key] = value.code
    return keycodes

def make_charlist_dict(content):
    def add_to_dicts(dict, obj, time_dict):
        if obj.key not in dict:
            dict[obj.key] = []
        dict[obj.key].append(obj)
        if obj.time not in time_dict:
            time_dict[obj.time] = []
        time_dict[obj.time].append(obj)
    chars = []
    master_dict = {KEY: {}, SCREEN: {}, MOUSE: {}, TIME: {}}
    current_screen = Screen()
    lines = content.split('\n')
    for line in lines:
        words = line.split()
        if len(words) < 3:
            continue
        event_type = words[2]
        obj = Event()
        if event_type == KEY:
            obj = Key()
            obj.set_info(line, current_screen)
            add_to_dicts(master_dict[KEY], obj, master_dict[TIME])
            chars.append(obj)
        elif event_type == SCREEN:
            obj = Screen()
            obj.set_info(line)
            add_to_dicts(master_dict[SCREEN], obj, master_dict[TIME])
            current_screen = obj
        elif event_type == MOUSE:
            obj = Mouse()
            obj.set_info(line, current_screen)
            add_to_dicts(master_dict[MOUSE], obj, master_dict[TIME])
    return chars, master_dict

def make_timeword_dictionaries(chars_list):
    def add_to_dictionaries(word):
        if word.key not in word_dict['by words']:
            word_dict['by words'][word] = []
        word_dict['by words'][word].append(word)
        if word.time not in word_dict['by times']:
            word_dict['by times'][word.time] = []
        word_dict['by times'][word.time].append(word)
    output = []
    word_dict = {'by words' : {}, 'by times': {}}
    current_word = []
    length = len(chars_list)
    for i, char in enumerate(chars_list):
        if char.code in reset_codes:
            if len(output) > 0 and char.code == 51: #backspace
                output.pop(len(output) - 1)
            else:
                output.append(char.char)
            current_char = Word(char)
            add_to_dictionaries(current_char)

            if len(current_word) > 0:
                word = Word(current_word[len(current_word) - 1])
                word.reset_char("".join([x.char for x in current_word]).strip())
                add_to_dictionaries(word)
                current_word = []
        else:
            if char.code == 49 or i == length - 1: #space
                current_word.append(char)
                word = Word(char)
                word.reset_char("".join([x.char for x in current_word]).strip())
                add_to_dictionaries(word)
                current_word = []
            else:
                current_word.append(char)
            output.append(char.char)
    output_str = "".join(output)
    # print(time_dict)
    return output_str, word_dict

def parse():
    f = open('./raw_data/output.txt', 'r') #second character for different reading / writing modes
    content = f.read()

    #keycodes = make_keycode_dict()
    #print(keycodes)

    chars, master_dict = make_charlist_dict(content)
    #print(reduce(lambda x, y: x + y, [len(chars_dict[key]) for key in chars_dict]))
    output_str, word_dicts = make_timeword_dictionaries(chars)
    # print(output_str)
    return output_str, master_dict, word_dicts

if __name__ == '__main__':
    random_datetime = '2012-01-01'
    conn = sqlite3.connect('../db/development.sqlite3')
    c = conn.cursor()
    start_index = 0
    try:
        c.execute('''CREATE TABLE events (start_index real, event_type text, word text, window text, date text, time text, datetime1 text, datetime2 text)''')
    except Exception:
        c.execute('SELECT * FROM events')
        start_index = len(c.fetchall())

    output_str, master_dict, word_dicts = parse()
    insertions = []
    for event, values in master_dict.items():
        for key, lists in values.items():
            for item in lists:
                if event == KEY:
                    word = item.char
                elif event == SCREEN:
                    word = item.window
                elif event == MOUSE:
                    word = str((item.position.x, item.position.y))
                elif event == TIME:
                    word = key
                else:
                    print 'poop'
                    word, window = 'poop', 'poop'
                window = item.window

                # Needed for everything but Screen events
                if not isinstance(window, str):
                    window = window.window

                # For the event that the user is still typing in the terminal
                # and hasn't created a Screen event
                if window.find('<no window>') >= 0:
                    window = window.replace('<no window>', 'possibly terminal')

                insertions.append((start_index, event, str(word), window, item.date, item.time, random_datetime, random_datetime))
                start_index += 1
    for event, values in word_dicts.items():
        if event == 'by_times':
            continue
        for key, words in values.items():
            for word in words:
                window = word.window
                if not isinstance(window, str):
                    window = window.window
                insertions.append((start_index, "WORD", str(word), window, word.date, word.time, random_datetime, random_datetime))
                start_index += 1

    c.executemany('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)', insertions)
    conn.commit()
    conn.close()
