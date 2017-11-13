'module docstring should be here'

import random # WIP

def check_dictionary():
    """Looking for mistakes in the dictionary

    Reads the contents of dictionary.md searching for :shit:,
    or :nine: without part of the speech defined
    """
    input_file = open("dictionary.md", 'r')
    num_problems_found = 0
    num_words_found = 0

    for line in input_file:
        if line.find(":shit:") > -1:
            tokens = line.split()
            word = tokens[0]
            part_of_speech = tokens[1]
            print word, part_of_speech, " <<< FIX tag (use :hammer:) in the dictionary"
            num_problems_found += 1
        elif line.find(":nine:") > -1:
            tokens = line.split()
            word = tokens[0]
            part_of_speech = tokens[1]
            if part_of_speech.find("_") == -1:
                print word, part_of_speech, " <<< FIX part of speech in the dictionary!"
                num_problems_found += 1
            else:
                print line
                num_words_found += 1

    print "num_problems_found =", num_problems_found
    print "num_words_found =", num_words_found

    input_file.close()

def use_random(number):
    "This is a WIP function"
    # We should sort the words to study randomly--in other words, shuffle them
    if number > 0:
        print 'Random integer between 1 and', number, ":",
        print random.randint(1, number)
    else:
        print 'Input number =', number, 'is not positive'

print "Script starts..."
check_dictionary()
use_random(100)
print "Script finished--exiting."
