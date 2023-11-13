import itertools

def createNextPossibleLetterMap(letterSets):
    """Create a map of each letter to letters in other sets."""
    return {a: [b for j, s2 in enumerate(letterSets) if j != i for b in s2] 
            for i, s in enumerate(letterSets) for a in s}

def isWordValid(word, letters, nextPossibilities):
    """Check if a word is valid based on the rules."""
    return word[0] in letters and all(word[i] in nextPossibilities[word[i-1]] for i in range(1, len(word)))

def findPossibleWords(letterSets, filename="filtered_words.txt"):
    """Find possible words from the letter sets."""
    try:
        with open(filename) as wordList:
            letters = set(a for s in letterSets for a in s)
            words = {a: [] for a in letters}
            nextPossibilities = createNextPossibleLetterMap(letterSets)
            
            for word in wordList:
                word = word.strip()
                if len(word) >= 3 and isWordValid(word, letters, nextPossibilities):
                    words[word[0]].append(word)
            
            return words
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}

def bruteForceAlgorithm(letterSets):
    """Find the best solutions using a brute-force approach."""
    print("Using a brute force algorithm...")
    wordsByLetter = findPossibleWords(letterSets)
    allWords = [word for words in wordsByLetter.values() for word in words]
    allLetters = set(letter for letterSet in letterSets for letter in letterSet)

    bestSolutions, r = [], 1
    while not bestSolutions and r <= len(allWords):
        for perm in itertools.permutations(allWords, r):
            currSolution, remainingLetters = [], set(allLetters)
            for word in perm:
                if currSolution and currSolution[-1][-1] != word[0]:
                    break
                currSolution.append(word)
                remainingLetters -= set(word)
                if not remainingLetters:
                    bestSolutions.append(perm)
                    break
        r += 1

    return bestSolutions

def displaySolutions(solutions):
    """Display the found solutions."""
    print(f"=== {len(solutions)} Solution{'' if len(solutions) == 1 else 's'} Found! ===")
    for x, seq in enumerate(solutions):
        print(f"{x+1}: " + ", ".join(seq))

if __name__ == "__main__":
    letterString = input("Enter all the letter sets as one long string: ")
    try:
        letterSets = [letterString[i:i+3] for i in range(0, len(letterString), 3)]
        result = bruteForceAlgorithm(letterSets)
        displaySolutions(result)
    except ValueError:
        print("Invalid input. Please enter a string of letters.")
