import math
from itertools import permutations

def get_lines(file_name):
    with open(file_name) as f:
        words = f.readlines()
        return [word.rstrip() for word in words]
    
#all scrabble words
words = get_lines('data/words.txt')

def get_all_permutations(letters, length):
    permutations_ = []
    while length > 2:
        current_permutations = list(permutations(letters,length))
        for word in current_permutations:
            permutations_.append(''.join(word))
        length -= 1
    return permutations_

def main():
    letters = list(input('Input the letters, no spaces or commas: '))
    print(f'Searching for words that contain {letters}')

    matching_words = []
    all_permutaions = get_all_permutations(letters,len(letters))  
    for word in all_permutaions:
        if word in words:
            matching_words.append(word)
    matching_words = sorted(set(matching_words), key = len)

    print()
    print(f'{len(matching_words)} matches found')

    current_length = None
    previous_length = None
    for word in matching_words:
        previous_length = current_length
        current_length = len(word)
        if current_length != previous_length:
            print()
            print(f'{current_length} letter words: ')
            print(word)
        else:
            print(word)

if __name__ == '__main__':
    main()
