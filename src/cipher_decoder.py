import os

def decode(filename):
    decoding = {'3':'a', '9':'b', 'h':'c', 'b':'d', 'r':'e', 'x':'f', 'i':'g', 
                'g':'h', 'j':'i', 'a':'j', '4':'k', '7':'l', 'e':'m', 'd':'n', 
                'q':'o', '2':'p', 'D':'q', 'l':'r', 'y':'s', 'p':'t', 'z':'u', 
                'w':'v', '5':'w', '0':'x', 'c':'y', 'm':'z', ' ':' ', '\n': '\n'}

    swear_words = {}
    with open(filename) as f:
        for line in f:
            word = ""
            for ch in line:
                word += ch if ch not in decoding else decoding[ch]
            word = word.strip()
            swear_words[word] = 0
    return swear_words
