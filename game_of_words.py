'module docstring should be here'

import random # WIP

# From https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
#
#
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
GRAY = '\033[90m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

number_of_lines_with_tag_shit = 0

def treat_shit_tag(line):
    global number_of_lines_with_tag_shit
    tokens = line.split()
    word = tokens[0]
    part_of_speech = tokens[1]
    print word + ' ' + part_of_speech + FAIL + ' <<< :shit: found; use :hammer: instead' + ENDC
    number_of_lines_with_tag_shit += 1

def line_contains_tag_of_number(line):
    return line.find(':nine:') > -1 or line.find(':eight:') > -1 or line.find(':seven:') > -1 or line.find(':six:') > -1

def check_dictionary():
    """Looking for mistakes in the dictionary

    Reads the contents of dictionary.md searching for :shit:,
    or :nine: without part of the speech defined
    """
    global number_of_lines_with_tag_shit
    filename = 'dictionary.md'
    input_file = open(filename, 'r')
    number_of_lines_missing_part_of_speech = 0
    number_of_lines_with_wrong_part_of_speech = 0

    for line in input_file:
        if line.find(':shit:') > -1:
            treat_shit_tag(line)
        elif line_contains_tag_of_number(line):
            tokens = line.split()
            num_tokens = len(tokens)
            if num_tokens == 1:
                print line + FAIL + ' <<< Wrong line: Missing part of speech' + ENDC
                number_of_lines_missing_part_of_speech += 1
            else:
                word = tokens[0]
                if word.count('__') == 2:
                    part_of_speech = tokens[1]
                    if part_of_speech.find('_') == -1:
                        print word + ' ' + part_of_speech + FAIL + ' <<< Wrong part of speech' + ENDC
                        number_of_lines_with_wrong_part_of_speech += 1
                else:
                    word_completed = False
                    i = 0
                    while not word_completed:
                        i += 1
                        if i == num_tokens:
                            word_completed = True
                        else:
                            word += ' ' + tokens[i]
                        if word.count('__') == 2:
                            word_completed = True
                    print word + GRAY + ' <<< Composite word' + ENDC
                    i += 1
                    part_of_speech = tokens[i]
                    if part_of_speech.find('_') == -1:
                        print word + ' ' + part_of_speech + FAIL + ' <<< Wrong part of speech' + ENDC
                        number_of_lines_with_wrong_part_of_speech += 1

    input_file.close()
    succeeded = bool(number_of_lines_with_tag_shit + number_of_lines_missing_part_of_speech + number_of_lines_with_wrong_part_of_speech == 0)
    if succeeded:
        print OKGREEN + 'No problems were found in file \'' + filename + '\'' + ENDC
    else:
        print FAIL,
        print '\nSummary of problems found:'
        print '  #lines with tag :shit: = ' + str(number_of_lines_with_tag_shit)
        print '  #lines missing part of speech = ' + str(number_of_lines_missing_part_of_speech)
        print '  #lines with wrong part of speech = ' + str(number_of_lines_with_wrong_part_of_speech),
        print ENDC
    return succeeded

def use_random(number):
    "This is a WIP function"
    # We should sort the words to study randomly--in other words, shuffle them
    if number > 0:
        print '\nRandom integer between 1 and', number, ":",
        print random.randint(1, number)
    else:
        print '\nInput number =', number, 'is not positive'

check_dictionary()
use_random(100)
