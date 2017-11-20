'module docstring should be here'

import random # WIP

# From https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
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
number_of_entries_with_invalid_ending = 0
number_of_entries_with_tag_shit = 0
number_of_entries_with_too_many_double_spaces = 0
number_of_entries_with_triple_spaces = 0

def valid_entry_ending(entry):
    valid = entry.endswith('  ')
    return valid

def treat_invalid_entry_ending(entry):
    global number_of_entries_with_invalid_ending
    number_of_entries_with_invalid_ending += 1
    tokens = entry.split()
    headword = tokens[0]
    print headword + ' ' + FAIL + ' <<< Incorrect entry ending #' \
        + str(number_of_entries_with_invalid_ending) + ENDC

def treat_too_many_double_spaces(entry):
    global number_of_entries_with_too_many_double_spaces
    number_of_entries_with_too_many_double_spaces += 1
    tokens = entry.split()
    headword = tokens[0]
    part_of_speech = tokens[1]
    print headword + ' ' + part_of_speech + FAIL \
        + ' <<< Too many double spaces #' \
        + str(number_of_entries_with_too_many_double_spaces) + ENDC

def treat_triple_spaces(entry):
    global number_of_entries_with_triple_spaces
    number_of_entries_with_triple_spaces += 1
    tokens = entry.split()
    headword = tokens[0]
    print headword + ' ' + FAIL + ' <<< Triple spaces #' \
        + str(number_of_entries_with_triple_spaces) + ENDC

def treat_shit_tag(entry):
    global number_of_entries_with_tag_shit
    number_of_entries_with_tag_shit += 1
    tokens = entry.split()
    headword = tokens[0]
    part_of_speech = tokens[1]
    print headword + ' ' + part_of_speech + FAIL \
        + ' <<< :shit: found; use :hammer: instead' + ENDC

def entry_contains_tag_of_number(entry):
    return entry.find(':nine:') > -1 \
        or entry.find(':eight:') > -1 \
        or entry.find(':seven:') > -1 \
        or entry.find(':six:') > -1 \
        or entry.find(':five:') > -1 \
        or entry.find(':four:') > -1

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

def print_colored(label, number):
    message = label + ' = ' + str(number)
    if number == 0:
        print OKGREEN + message + ENDC
    else:
        print FAIL + message + ENDC

def check_dictionary():
    """Looking for mistakes in the dictionary

    Reads the contents of dictionary.md searching for :shit:,
    or :nine: without part of the speech defined
    """
    filename = 'dictionary.md'
    input_file = open(filename, 'r')
    number_of_entries_with_wrong_part_of_speech = 0

    for line in input_file:
        entry = line.replace('\n','')
        if not valid_entry_ending(entry):
            treat_invalid_entry_ending(entry)
        if entry.count('  ') > 2:
            treat_too_many_double_spaces(entry)
        if entry.count('   ') > 0:
            treat_triple_spaces(entry)
        if entry.find(':shit:') > -1:
            treat_shit_tag(entry)
        if entry_contains_tag_of_number(entry):
            tokens = entry.split()
            headword, idx = get_headword_and_next_token_index(tokens)
            part_of_speech = tokens[idx]
            if part_of_speech.find('_') == -1:
                number_of_entries_with_wrong_part_of_speech += 1
                print FAIL + headword + ' ' + BOLD + part_of_speech + ENDC \
                    + ' <<< Wrong part of speech #' \
                    + str(number_of_entries_with_wrong_part_of_speech)

    input_file.close()
    global number_of_entries_with_invalid_ending
    global number_of_entries_with_tag_shit
    succeeded = bool(number_of_entries_with_invalid_ending + number_of_entries_with_tag_shit + number_of_entries_with_wrong_part_of_speech == 0)
    if succeeded:
        print OKGREEN + 'No problems were found in file \'' + filename + '\'' + ENDC
    else:
        print '\nSummary of issues found'
        print '-----------------------'        
        print_colored('Entries with invalid ending', number_of_entries_with_invalid_ending)
        print_colored('Entries with triple spaces', number_of_entries_with_triple_spaces)
        print_colored('Entries with too many double spaces', number_of_entries_with_too_many_double_spaces)
        print_colored('Entries with tag :shit:', number_of_entries_with_tag_shit)
        print_colored('Entries with wrong part of speech', number_of_entries_with_wrong_part_of_speech)
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
