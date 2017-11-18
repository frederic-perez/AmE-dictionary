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

number_of_composite_headwords = 0
number_of_lines_with_tag_shit = 0
number_of_lines_with_too_many_double_spaces = 0
number_of_lines_with_triple_spaces = 0

def treat_too_many_double_spaces(line):
    global number_of_lines_with_too_many_double_spaces
    tokens = line.split()
    headword = tokens[0]
    part_of_speech = tokens[1]
    print headword + ' ' + part_of_speech + FAIL + ' <<< Too many double spaces' + ENDC
    number_of_lines_with_too_many_double_spaces += 1

def treat_triple_spaces(line):
    global number_of_lines_with_triple_spaces
    tokens = line.split()
    headword = tokens[0]
    print headword + ' ' + FAIL + ' <<< Triple spaces' + ENDC
    number_of_lines_with_triple_spaces += 1

def treat_shit_tag(line):
    global number_of_lines_with_tag_shit
    tokens = line.split()
    headword = tokens[0]
    part_of_speech = tokens[1]
    print headword + ' ' + part_of_speech + FAIL + ' <<< :shit: found; use :hammer: instead' + ENDC
    number_of_lines_with_tag_shit += 1

def line_contains_tag_of_number(line):
    return line.find(':nine:') > -1 \
        or line.find(':eight:') > -1 \
        or line.find(':seven:') > -1 \
        or line.find(':six:') > -1 \
        or line.find(':five:') > -1 \
        or line.find(':four:') > -1

def get_headword_and_next_token_index(tokens):
    NUM_TOKENS = len(tokens)
    headword = tokens[0]
    headword_completed = headword.count('__') == 2
    idx = 0
    while not headword_completed:
        idx += 1
        if idx == NUM_TOKENS:
            headword_completed = True
        else:
            headword += ' ' + tokens[idx]
            if headword.count('__') == 2:
                headword_completed = True
    idx += 1
    if idx > 1:
        global number_of_composite_headwords
        number_of_composite_headwords += 1
        print OKBLUE + headword + GRAY + ' <<< Composite headword #' \
            + str(number_of_composite_headwords) + ENDC
    return headword, idx

def check_dictionary():
    """Looking for mistakes in the dictionary

    Reads the contents of dictionary.md searching for :shit:,
    or :nine: without part of the speech defined
    """
    global number_of_lines_missing_part_of_speech
    filename = 'dictionary.md'
    input_file = open(filename, 'r')
    number_of_lines_with_wrong_part_of_speech = 0

    for line in input_file:
        if line.count('  ') > 2:
            treat_too_many_double_spaces(line)
        if line.count('   ') > 0:
            treat_triple_spaces(line)
        if line.find(':shit:') > -1:
            treat_shit_tag(line)
        if line_contains_tag_of_number(line):
            tokens = line.split()
            headword, idx = get_headword_and_next_token_index(tokens)
            part_of_speech = tokens[idx]
            if part_of_speech.find('_') == -1:
                number_of_lines_with_wrong_part_of_speech += 1
                print FAIL + headword + ' ' + part_of_speech + ENDC \
                    + ' <<< Wrong part of speech #' \
                    + str(number_of_lines_with_wrong_part_of_speech)

    input_file.close()
    global number_of_lines_with_tag_shit
    succeeded = bool(number_of_lines_with_tag_shit + number_of_lines_with_wrong_part_of_speech == 0)
    if succeeded:
        print OKGREEN + 'No problems were found in file \'' + filename + '\'' + ENDC
    else:
        print '\nSummary of problems found:'
        print '  Lines with triple spaces = ' + str(number_of_lines_with_triple_spaces)
        print '  Lines with too many double spaces = ' + str(number_of_lines_with_too_many_double_spaces)
        print '  Lines with tag :shit: = ' + str(number_of_lines_with_tag_shit)
        print '  Lines with wrong part of speech = ' + str(number_of_lines_with_wrong_part_of_speech)
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
