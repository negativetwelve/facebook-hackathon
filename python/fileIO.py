from time import sleep

EMPTY_INDEX = 'index n/a'
EMPTY_KEY_CODE = 'code n/a'
EMPTY_CHAR = 'char n/a'
EMPTY_TIME = 'time n/a'
EMPTY_DATE = 'date n/a'

class CharTime:    
    
    reset_codes = {36: "\n", 48: "\t"}

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
        if self.code in CharTime.reset_codes:
            self.char = CharTime.reset_codes[self.code]
        
    def __repr__(self):
        return "CharTime(char={0}, code={1}, date={2}, time={3})".format(self.char, self.code, self.date, self.time)
        
class WordTime:
    def __init__(self, word, date, time):
        self.word = word
        self.date = date
        self.time = time    

        
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
    print(chars)
    print(make_timeword_dictionaries(chars))

def make_char_list_dict(content):  
    chars = []
    chars_dict = {}
    lines = content.split('\n')
    for line in lines:
        char_object = CharTime()
        char_object.set_info(line)
        chars.append(char_object)
        chars_dict[char_object.char] = char_object
    return chars, chars_dict
        
def make_timeword_dictionaries(chars_list):
    output = []
    word_dict = {}
    for char in chars_list:
        if len(output) > 0 and char.code == 51:
            output.pop(len(output) - 1)
        else:
            output.append(char.char)
    print("".join(output))

parse()


    
