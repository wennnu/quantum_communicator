import bb84
from module import Cipher

if __name__ == "__main__":
    #MAIN MENU
        #host or join
        #if host
            #select to play as bob or eve
        #if join
            #connect to first available socket
            #play as whoever is available (bob or eve)
    #GAME
        #generate word
        #generate cipher
        #send cipher to bob
        #send partial cipher to eve
        #if bob
            #show hangman
            #show keyboard
            #gray out guessed letters
            #show underscores/guessed letters
            #send each guess
        #if eve
            #show bobs encoded guesses
            #show underscores and encoded partial word
            #show partial information
    #END
        #if bob ran out of guesses
            #bob loses
            #eve wins
        #if bob guessed correctly
            #eve submits one final guess
                #if eves guess is correct
                    #bob loses
                    #eve wins
                #else
                    #bob wins
                    #eve loses
        #play again?
    pass