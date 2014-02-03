ASCII_LOWER = 'abcdefghijklmnopqrstuvwxyz '
ASCII_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
LETTERS = ASCII_LOWER + ASCII_UPPER
NON_CHAR = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""

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
    lshift = zip(ASCII_LOWER, ASCII_LOWER[shift:] + ASCII_LOWER[:shift])
    ushift = zip(ASCII_UPPER, ASCII_UPPER[shift:] + ASCII_UPPER[:shift])
    return dict(ushift + lshift)


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
    return ''.join([coder[c] if c in LETTERS else c for c in text])


#
# Problem 3: Multi-level encryption.
#
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
    for location, shift in shifts:
        text = text[:location] + apply_shift(text[location:],shift)
    return text
 
#
# Problem 4: Multi-level decryption.
#

def bigger_word(L1, L2):
    """
    does L1 contain a bigger word than L2?

    L1, L2  -->  list
    returns boolean
    """
    if not L1 or not L2:
        return False
    L1 = [len(item) for item in L1]
    L2 = [len(item) for item in L2]
    return max(L1) > max(L2)

def recursive_find_best_shifts(wordlist, text, start = 0):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    # assumes that each shift starts on a word boundary,
    # at the beginning of a word - not a space

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
##    print '---------------------- *******************  --------------------------'
##    print 'start:', start,
    
    # recursion base case
    if not text:
        return []

    # find the shift that has the most consecutive
    # words at the beginning of the text
    bestcount = None
    bestshift = None
    bestpartial_list = None
    bestpartial_text = None
    for shift in xrange(0, 27):
        count = 0
        partialdecode_text = apply_coder(text, build_coder(shift))
        partialdecode_list = partialdecode_text.split()
        try:
            while is_word(wordlist, partialdecode_list[count]):
##                print 'is_word:', partialdecode_list[count], '\t\t\tshift:', shift,
                count += 1
##                print  '\tcount:', count
        except IndexError:
            pass
        # if two shifts result in the same number of words, pick the one with the longest word
        if count > bestcount or (count == bestcount and
                                 bigger_word(partialdecode_list[:count],
                                             bestpartial_list[:bestcount])):
            bestshift = shift
            bestcount = count
            bestpartial_list = partialdecode_list
            bestpartial_text = shift = partialdecode_text

    # what happens if none of the shifts work??
    if bestshift == None:
        print 'NO SHIFT FOUND FOR:'
        return text

    # peel off the clear text
    cleartext = ' '.join(bestpartial_list[:bestcount]) + ' '
    ciphertext = bestpartial_text[len(cleartext):]
##    print 'clear:', cleartext

    #where is the start of the next shift?
    nextpos = len(cleartext) + start

    # recurse
    return [(start, bestshift)] + recursive_find_best_shifts(wordlist, ciphertext, nextpos)   

def decrypt_fable():
     """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.
     s = get_fable_string()
     shifts = recursive_find_best_shifts(wordlist, s, start = 0)
     return apply_shifts(s, shifts)

print decrypt_fable()
