import sys
from js import console, document
from pyodide.ffi.wrappers import add_event_listener
import itertools
def letterSetsContain(inp, letterSets):
    for a in inp:
        for s in letterSets:
            if a in s:
                return True
    return False

def createNextPossibleLetterMap(letterSets):
    nextLetters = {}
    for i in range(len(letterSets)):
        for a in letterSets[i]:
            nextLetters[a] = []
            for j in range(len(letterSets)):
                if j != i:
                    nextLetters[a] += letterSets[j]

    return nextLetters

def findPossibleWords(letterSets):
    letters = [a for s in letterSets for a in s]
    words = {a:[] for a in letters}
    nextPossibilities = createNextPossibleLetterMap(letterSets)

    with open("filtered_words.txt") as wordList:
        for word in wordList:
            word = word.strip()
            if len(word) < 3 or word[0] not in letters:
                continue
            validWord = True
            for i in range(1,len(word)):
                if word[i] not in nextPossibilities[word[i-1]]:
                    validWord = False
                    break
            if validWord:
                words[word[0]].append(word)
    return words

def load_filtered_words():
    from pyodide.http import pyfetch

    async def fetch_text_file(url):
        response = await pyfetch(url)
        text = await response.text()
        return text

    text = fetch_text_file(r'https://raw.githubusercontent.com/danmaps/letter-boxed-solver/master/filtered_words.txt')
    # print(text)

    for line in text:
        wordList.append(line)
    return wordList

def findPossibleWords(letterSets):
    letters = [a for s in letterSets for a in s]
    words = {a:[] for a in letters}
    nextPossibilities = createNextPossibleLetterMap(letterSets)
    wordList = load_filtered_words()
    for word in wordList:
        word = word.strip()
        if len(word) < 3 or word[0] not in letters:
            continue
        validWord = True
        for i in range(1,len(word)):
            if word[i] not in nextPossibilities[word[i-1]]:
                validWord = False
                break
        if validWord:
            words[word[0]].append(word)
    return words

def bruteForceAlgorithm(letterString):
    letterSets = [letterString[i:i+3] for i in range(0, len(letterString), 3)]
    console.log("Using a brute force algorithm...")
    wordsByLetter = findPossibleWords(letterSets)
    allWords = [word for letterSet in [wordsByLetter[letter] for letter in wordsByLetter] for word in letterSet]
    allLetters = set([letter for letterSet in letterSets for letter in letterSet])
    
    bestSolutions = []
    r = 1
    while True:
        for perm in itertools.permutations(allWords, r=r):
            currSolution = []
            remainingLetters = set(allLetters)
            for word in perm:
                if currSolution and currSolution[-1][-1] != word[0]:
                    break

                currSolution.append(word)

                for a in word:
                    if a in remainingLetters:
                        remainingLetters.remove(a)

                if not remainingLetters:
                    bestSolutions.append(perm)
                    break
        if bestSolutions:
            break
        r += 1

    return bestSolutions

def solve(*args):
    # Create the output element
    # print("solve")
    output = Element("output")
    
    puzzle = document.getElementById("puzzle").value

    output.element.innerText = bruteForceAlgorithm(puzzle)

add_event_listener(document.getElementById("btn"), "click", solve)