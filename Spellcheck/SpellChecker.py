import re
from collections import Counter

COUNTS=0
def tokens(text):
    return re.findall('[a-z]+', text.lower())

def known(words):
    global COUNTS
    return {w for w in words if w in COUNTS}

def correct(word):
    global COUNTS
    candidates = (known(edits0(word)) or 
                  known(edits1(word)) or 
                  known(edits2(word)) or 
                  [word])
    return max(candidates, key=COUNTS.get)



def edits0(word): 
    return {word}

def edits2(word):
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def splits(word):
    return [(word[:i], word[i:]) for i in range(len(word)+1)]

def correct_text(text):
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    word = match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)

def run(input_filepath,output_filename):
    global COUNTS
    TEXT = open('Spellcheck/big.txt').read()
    WORDS = tokens(TEXT)
    COUNTS = Counter(WORDS)

    with open(input_filepath, "r") as infile, open("Spellcheck/Correctfiles/"+output_filename, "w") as outfile:
        for line in infile:
            outfile.write(correct_text(line))

#correct_text('Speling Errurs IN somethink. Whutever; unusuel misteakes?')

