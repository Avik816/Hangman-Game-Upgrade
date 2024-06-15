# CODE SUBMITTED BY AVIK CHAKRABORTY

import random, prettytable, os, sys, sqlite3 as sql


# Database Creation
db_file = 'hall_of_fame.db'

# Checking if the database file already exists
if os.path.isfile(db_file) == False:
    # If the file doesn't exist, this line will automatically create it and the table
    conn = sql.connect('hall_of_fame.db') # file gets created and sql connection is established
    dbcur = conn.cursor()
    dbcur.execute("CREATE TABLE hall_of_fame(level Varchar(255), winner_name Varchar(255), remaining_lives int(8))")
    conn.close() # connection closed
    

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']        
                
                
# secret words sets   
animal = 'ant baboon badger bat bear beaver camel cat clam cobra'.split()

# 3 seperate sets of secret words are added
shape = 'square triangle rectangle circle ellipse rhombus trapezoid'.split()
place = 'Cairo London Paris Baghdad Istanbul Riyadh'.lower().split()
plant = 'Rose Bamboo Sequoia Sunflower Orchid Cactus Fern'.lower().split()

words = {'animal': animal, 'shape': shape, 'place': place, 'plant': plant}


# clear the console screen
os.system('cls' if os.name == 'nt' else 'clear')

# accepting the name
name = input('Enter Player Name : ')


def building_the_menu():
    # building the menu
    menu1 = prettytable.PrettyTable()
    menu1.title = f'HI {name}. Welcome to HANGMAN. Play the game.'
    menu1.field_names = ['Level 1', 'Level 2', 'Level 3']
    menu1.add_row(['Easy', 'Moderate', 'Hard'])
    menu1.align = 'c'

    menu2 = prettytable.PrettyTable()
    menu2.title = 'Hall of Fame'
    menu2.field_names = ['Level', 'Winner Name', 'Remaining Lives']
    # displaying the hall of fame
    conn = sql.connect(db_file) # connection established
    dbcur = conn.cursor()
    for row in dbcur.execute('SELECT * FROM hall_of_fame'):
        # fetching data from the database
        # adding the rows to table
        menu2.add_row([row[0], row[1], row[2]])


    menu3 = prettytable.PrettyTable()
    menu3.field_names = ['About the game']
    menu3.add_row(['1. This is a game about chances where the player guess the letter if correct, the man is saved.'])
    menu3.add_row(['2. If the letter is incorrect lives are taken away from the player.'])
    menu3.add_row(['3. There are a total of 8 lives for the players.'])
    menu3.add_row(['4. Easy: The player will be given a chance to select the set from which the random word will be chosen'])
    menu3.add_row(['5. Moderate: The player will be given a chance to select the set from which the random word will be selected.\nThe number of trail will be reduced to 6.'])
    menu3.add_row(['6. Hard: The game will randomly select a set and randomly select a word from this set.\nThe player will have no clue about the secret word.\nAlso, the number of trails will remain at 6.'])
    menu3.padding_width = 2

    # menu printed
    print(menu1, menu2, menu3, sep = '\n')


building_the_menu()

missedLetters = ''
correctLetters = ''
trials = 8
print()


def level_choosing(trials):
    # choosing the level of the game
    level = input('Choose the level for the game from (easy/ moderate/ hard) : ').lower()

    menu4 = prettytable.PrettyTable()
    menu4.title = 'Secret Words'
    menu4.field_names = ['Field 1', 'Field 2', 'Field 3']

    if level == 'easy':
        menu4.add_row(['animal', 'shape', 'place'])
        print(menu4)
        
        wordSet = input('Select the set of words : ').lower()
        trials = 8

    elif level == 'moderate':
        menu4.add_row(['animal', 'plant', 'place'])
        print(menu4)

        wordSet = input('Select the set of words : ').lower()
        trials = 6

    elif level == 'hard':
        wordSet = random.choice(['animal', 'shape', 'place', 'plant'])
        trials = 6

    else:
        print('\nWRONG ENTRY! RESTART THE GAME!')
        return 'WRONG', 0

    return wordSet, trials, level


wordSet, trials, level = level_choosing(trials)

if wordSet == 'WRONG' and trials == 0:
    sys.exit() # Terminating the game if the wrong level is entered.

wordSet, trials, level = words[wordSet], trials, level


def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]


secretWord = getRandomWord(wordSet)
gameIsDone = False


def displayBoard(missedLetters, correctLetters, secretWord):
    # clearing the console
    os.system('cls' if os.name == 'nt' else 'clear')

    print(HANGMAN_PICS[len(missedLetters)])
    print()
 
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed, trials):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    while True:
        print(f'You have {trials} guess left.')
        guess = input('Guess a letter : ').lower()

        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess
        
def db_management(trials):
    # managing the database here
    # when the player wins their data if a new record is made will be updated by this function
    conn = sql.connect(db_file) # connection established
    dbcur = conn.cursor()

    # name of the player is selected from the database, based on the player name and level
    db_name = ''
    for row in dbcur.execute('SELECT winner_name FROM hall_of_fame WHERE winner_name = ? AND level = ?', (name, level,)):
        if row != '':
            db_name = row[0]
        break

    if db_name == name:
        # remaining of the player is selected from the database, based on the player name and level
        for row in dbcur.execute('SELECT remaining_lives FROM hall_of_fame WHERE winner_name = ? AND level = ?', (name, level,)):
            db_rl = row[0]
            break

        if trials > db_rl:
            # if a new record is made then the record is updated.
            # a reord is created if the remaining lives in database is less than the trials in game 
            dbcur.execute('UPDATE hall_of_fame SET remaining_lives = ? WHERE winner_name = ? AND level = ?', (trials, name, level))
            conn.commit()
    else:
        # if a new player is playing the game or the same player is playing on a different level then the record is added to the databse.
        # if a record is broken and a new record is set the player name with thier life is updated.
        db_level = ''
        for row in dbcur.execute('SELECT level FROM hall_of_fame WHERE level = ?', (level,)):
            if row != '':
                db_level = row[0]
                break

        if level == db_level:
            db_rl = 0
            for row in dbcur.execute('SELECT remaining_lives FROM hall_of_fame WHERE winner_name = ? AND level = ?', (name, level,)):
                db_rl = row[0]
                break

            if db_rl < trials:
                # updating the leaderboard if a diff player in the same mode exists
                dbcur.execute('UPDATE hall_of_fame SET winner_name = ?, remaining_lives = ? WHERE level = ?', (name, trials, level))
                conn.commit()
        else:
            # updating the leaderboard if a player in the present mode does not exists
            data = (level, name, trials)
            dbcur.execute('INSERT INTO hall_of_fame VALUES (?, ?, ?)', data)
            conn.commit() # database saved
    
    conn.close() # connection closed

def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print()
    return input('Do you want to play again? (yes or no) : ').lower().startswith('y')


while True:
    displayBoard(missedLetters, correctLetters, secretWord)

    # Let the player enter a letter.
    guess = getGuess(missedLetters + correctLetters, trials)

    if guess in secretWord:
        correctLetters = correctLetters + guess

        # Check if the player has won.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '"! You have won!')
            gameIsDone = True

            # Winner details added to the database
            db_management(trials)
    else:
        trials -= 1
        missedLetters = missedLetters + guess

        # checking the number of trails
        # ALso, checking if the player lost or has trials left
        if trials == 0:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True

    # Asking the player if they want to play again after the game is done.
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False

            # reprinting the menu
            building_the_menu()
            # reprinting the modes and accessing the word set
            wordSet, trials, level = level_choosing(trials)
            wordSet, trials, level = words[wordSet], trials, level

            secretWord = getRandomWord(wordSet)
        else:
            break
    