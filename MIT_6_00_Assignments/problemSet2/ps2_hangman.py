# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist
    
def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
def update_word(blanks, usedLetters, word):
    blanks =''
    for c in word:
        
        if c in usedLetters:
            blanks += c
        else:
            
            blanks = blanks + '-'
    return blanks




def hangman():
    wordlist = load_words()
    word = choose_word(wordlist)
    
    blanks =''
    tries = 5
    for c in word:
        blanks += '-'
    available_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                             'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                             's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
    usedLetters = ''
    while tries > 0 and '-' in blanks:
        print 'This is what the word looks like now'
        print blanks
        if len(usedLetters) > 0:
            print 'You have used these letters: ' + usedLetters
        print 'You have ' + str(tries) + ' tries left'
        print'Letters remaining ' + ''.join(available_letters)
        guess = raw_input('Next guess please:')
        if guess not in available_letters:
            print 'You guessed that letter already'
        elif guess not in word:
            tries -= 1
            usedLetters += guess
            available_letters.remove(guess)
        elif guess in word:
            usedLetters += guess
            available_letters.remove(guess)
            blanks = update_word(blanks, usedLetters, word)



    if '-' not in blanks:
        print 'Congratulations. You guessed the word correctly'
    else:
        print'Boourns'
        




