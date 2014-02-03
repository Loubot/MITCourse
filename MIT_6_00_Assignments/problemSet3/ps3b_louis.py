from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    compList = []
    maxScore = 0
    maxWord =''
    workingHand = hand.copy()
    length = calculate_handlen(hand)
    
    
    for i in range (1, length +1):
        tempList = get_perms(workingHand,i)
        for temp in tempList:
            
            if temp in word_list:
                
                if get_word_score(temp, len(temp)) > maxScore:
                    maxScore = get_word_score(temp, len(temp)) 
                    maxWord = temp
            
##    print maxWord
    return maxWord

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    handLength = calculate_handlen(hand)
    score = 0
    total = 0
    while True:
        
        display_hand(hand)
        chosenWord = comp_choose_word(hand, word_list)
        if chosenWord == '':
            break
        print chosenWord
        score = get_word_score(chosenWord, handLength)
        total += score
        print '"%s" earned %d points. Total is now %d' %(chosenWord, score, total)
        hand = update_hand(hand, chosenWord)

    print 'No more valid words. Total score: %d points.' % total
        
    
        
        



#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hand = deal_hand(HAND_SIZE)
    choice = ''
    while True:
        while choice != 'n' and choice != 'r' and choice != 'e':
            choice = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
            if choice == 'e':
                break
            elif choice == 'n':
                hand = deal_hand(HAND_SIZE)
                break
##            elif choice == 'r':
##                hand = hand
##                break
        if choice == 'e':
            break

        while choice != 'c' and choice != 'u':
            choice = raw_input('Enter u to have yourself play, c to have the computer play: ')
            if choice == 'c':
                comp_play_hand(hand, word_list)
                break
            elif choice == u:
                play_hand(hand, word_list)
                break

            print 'Invalid command'


    print 'finished'

            
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


    
