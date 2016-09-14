def encode():
    dict = {'a':'3', 'b':'9', 'c':'h', 'd':'b', 'e':'r', 'f':'x', 'g':'i', 'h':'g', 'i':'j', 'j':'a', 'k':'4', 'l':'7', 'm':'e', 'n':'d', 'o':'q', 'p':'2', 'q':'g', 'r':'l', 's':'y', 't':'p', 'u':'z', 'v':'w', 'w':'5', 'x':'0', 'y':'c', 'z':'m', ' ':' ', '\n':'\n'}

    with open('temp.txt') as f:
        lines = f.readlines()

    fo = open("words.txt", "w")

    for line in lines:
        newline = ""
        for c in line:
            newline += dict[c]
        fo.write(newline)
    fo.close()



def decode(filename):
    dict = {'3':'a', '9':'b', 'h':'c', 'b':'d', 'r':'e', 'x':'f', 'i':'g', 'g':'h', 'j':'i', 'a':'j', '4':'k', '7':'l', 'e':'m', 'd':'n', 'q':'o', '2':'p', 'g':'q', 'l':'r', 'y':'s', 'p':'t', 'z':'u', 'w':'v', '5':'w', '0':'x', 'c':'y', 'm':'z', ' ':' ' }

    with open(filename) as f:
        lines = f.readlines()

    words = {}
    for line in lines:
        word = ""
        for c in line:
            word += dict[c]
        words[word] = 0

    return words

def deleteFile():
    #To-do: delete decoded swear word file named temp.txt when program is done running
    pass
