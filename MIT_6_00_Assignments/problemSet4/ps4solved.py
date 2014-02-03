# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random
import copy

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    
    coder = {}.copy()
    plain_lower = ' abcdefghijklmnopqrstuvwxyz'
    plain_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shifted_lower = plain_lower[shift:27] + plain_lower[0:shift]
    shifted_upper = plain_upper[shift:26] + plain_upper[0:shift]

    counter = 0    
    for p, s in zip(plain_lower, shifted_lower):
        coder[plain_lower[counter]] = shifted_lower[counter]
        counter += 1

    counter = 0    
    for p, s in zip(plain_upper, shifted_upper):
        coder[plain_upper[counter]] = shifted_upper[counter]
        counter += 1
    return coder    

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    encoder = {}
    encoder = build_coder(shift).copy()
    return encoder
    

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    code = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encoder = {}
    encoder = build_encoder(shift)
    decoder = {}
    counter = 0
    for c in code:
        decoder[encoder.get(code[counter], c)] = code[counter]
        counter += 1
    return decoder
 

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO.

    cipher = str()
    for c in text:
        cipher += coder.get(c, c)
    return cipher

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    return apply_coder(text, build_coder(shift))
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO

    split_text = []
    shifted_text = str()
    max_shift = 0
    max_score = 0
    score = 0
    hit_counter = 0
    shift_counter = 0

    while shift_counter < 27:
        shifted_text = apply_coder(text, build_decoder(shift_counter))
        split_text = shifted_text.split(' ')
        for s in split_text:
            if is_word(wordlist, s) == True:
                hit_counter += 1
                score += len(s)
        if max_score < hit_counter * score:
            max_score = hit_counter * score
            max_shift = shift_counter
        hit_counter = 0
        score = 0
        shift_counter += 1

    return max_shift                
   
#
# Problem 3: Multi-level encryption.
#

def get_distances(shifts, length):
    '''
    return a list of tuple (distance between 2 location, shift of them)
    EX:
    shifts: [(0,6), (3, 18), (12, 16)]
    len(text): 18
    returns: [(3,6), (9,18), (6,16)]
    '''

    a = (0,0)
    b = (0,0)
    distances = []

    shifts.sort()
    shifts.reverse()
    
    a = shifts.pop()    
    if a[0] != 0:
        distances.append((a[0],0))
        
    while True:
        try:
            b = shifts.pop()
            distances.append((b[0]-a[0], a[1]))
            a = b
        except:
            distances.append((length - a[0], a[1]))
            break
        
    return distances


def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.

    distances = []
    distances = get_distances(shifts, len(text))
    stored_text = str()
    shifted_text = text

    location = int()
    for d in distances:
        shifted_text = apply_shift(shifted_text, d[1])
        stored_text += shifted_text[0:d[0]]
        shifted_text = shifted_text[d[0]:len(shifted_text)]
    return stored_text
 
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """

    find_best_shifts_rec(wordlist, text, -1)
    return best_shifts    

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.
    
    if start == -1:
        global best_shifts
        best_shifts = []
        global decoded_text
        decoded_text = str()
        a = float()
        b = float(len(text))
        best_shift = int()
        shift = int()

        find_best_shifts_rec(wordlist, text, int(a))

    elif len(text) - start > 2 :

        ab = find_best_shift(wordlist, text[start: len(text)])
        best_shift = ab
        best_shifts.append((len(decoded_text), best_shift))
        print best_shifts
        next_text = apply_coder(text, build_decoder(best_shift))
        print next_text

        ##Find location of ' ' in next_text
        count = int()
        for l in next_text:
            count += 1
            if l == ' ':
                break

        ##slice decoded text into decoded_text
        decoded_text += next_text[0:count]
        next_text = next_text[count:len(next_text)]        
        find_best_shifts_rec(wordlist, next_text, 0)
        re_best_shifts = copy.copy(best_shifts)

    else:
        return

def apply_decodes(text, shifts):
    distances = get_distances(shifts, len(text))
    stored_text = str()
    shifted_text = text
    decode_counter = int()

    location = int()
    for d in distances:
        decode_counter = -d[1]
        shifted_text = apply_shift(shifted_text, decode_counter)
        stored_text += shifted_text[0:d[0]]
        shifted_text = shifted_text[d[0]:len(shifted_text)]
    return stored_text

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO
    fable = get_fable_string()
    decoded_fable = str()
    split_fable = fable.split('.')
    for s in split_fable:
        decode_shifts = find_best_shifts(wordlist, s)
        decoded_fable += apply_decodes(s, decode_shifts) + '.'
    return decoded_fable





## Test of find_best_shifts_rec
test_words = random_scrambled(wordlist, 10)
decode_shifts = find_best_shifts(wordlist, test_words)
print test_words
print decode_shifts
print apply_decodes(test_words, decode_shifts)

## Test of decrypt_fable
#print decrypt_fable()
    



    
#What is the moral of the story?
#
#
#
#
#

