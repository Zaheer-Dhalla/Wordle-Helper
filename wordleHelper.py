# WORDLE HELPER
# Zaheer Dhalla
# Thursday, May 4th, 2023

# Opening a .txt file that contains all words
rawWords = open("words.txt")

wordList = []

# Putting all the words into a list
for line in rawWords:
    line = line.replace("\n", "")
    wordList.append(line.lower())
    
fiveLetterWords = []

# Filtering for 5 letter words
for word in wordList:
    if len(word) == 5:
        fiveLetterWords.append(word.lower())
        
# Finding all potential words from known information
def findPotentialWords():
    potentialWords = []      
    known = input("Type what you know (input '.' for unknown letters): ")
    usedLetters = input("Type letters you know without the position: ")
    excludedLetters = input("Type letters that are not in the word: ")
    
    # Creating a dictionary that an index number with its designated character in the word we're looking for
    knownPositions = dict()
    index = 0;
    for letter in known:
        if letter != '.':
            knownPositions[index] = letter;
        index += 1

        
    # Looping through all 5 letter words
    for word in fiveLetterWords:
        # If any word matches with the known information, that word is added to a new list
        # The '.' character represents an unknown letter
        valid = True
        
        # Checking if the letters known without position are in the current word
        for letter in usedLetters:
            if letter not in word:
                valid = False
        # Checking if the letters that aren't in the answer are also not in the current word
        for letter in excludedLetters:
            if letter in word:
                valid = False
            
        # Looping through all of the keys in the knownPositions dictionary to see if the current word
        # Matches the given info 
        for key in knownPositions.keys():
            if word[key] != knownPositions[key]:
                valid = False
        # If the current word fits with all of the information given, append that word to a list   
        if valid:
            potentialWords.append(word)
                
    # Printing all of the words it could be along with the number of words there are
    print(len(potentialWords), "Words")
    for item in potentialWords:
        print(item)
        
    # If the user has not found the word, recurse the function until they do
    recurse = input("Did you get the word? ('yes'/'no'): ")
    if recurse.lower() == 'no' or recurse.lower() == 'n':
        findPotentialWords()
    
# Calling the function
findPotentialWords()
