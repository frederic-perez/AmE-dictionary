'module docstring should be here'

import random # WIP
import re

# From https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
#
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
GRAY = '\033[90m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def valid_entry_ending(entry):
    """Self-explanatory"""
    valid = entry.endswith('  ')
    return valid

VALID_TAGS = ['three', 'two', 'astonished', 'camera', 'dart', 'eight', 'es', 'four', 'five', \
    'hammer', 'm', 'mega', 'nine', 'octocat', 'pencil2', 'seven', 'six']

def valid_tag(tag):
    """Returns True when tag is an allowed one; False otherwise"""
    return tag in VALID_TAGS

def valid_entry_tags(entry):
    """Self-explanatory"""
    tags = re.findall(r':(\w+):', entry)
    for tag in tags:
        if not valid_tag(tag):
            return False, tag
    return True, ''

NUMBER_TO_TAG = [':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', \
    ':nine::m:']

def get_tag(number):
    """"Given an input number, an index is set to access a list to get the corresponding tag"""
    index = number - 2
    return NUMBER_TO_TAG[index]

def entry_has_tag_of_any_number(entry, number_min, number_max):
    """Self-explanatory"""
    for number in range(number_min, number_max + 1):
        if entry.find(get_tag(number)) > -1:
            return True
    return False

def entry_has_tag_of_number(entry, number):
    """Self-explanatory"""
    return entry.find(get_tag(number)) > -1

def entry_has_tag_of_high_number(entry):
    """Self-explanatory"""
    return entry.find(':nine:') > -1

def entry_has_tag_hammer(entry):
    """Self-explanatory"""
    return entry.find(':hammer:') > -1

def print_colored(label, number):
    """Self-explanatory"""
    message = label + ' = ' + str(number)
    if number == 0:
        print OKGREEN + message + ENDC
    else:
        print FAIL + message + ENDC

def get_headword_and_part_of_speech(tokens, do_print=False):
    """Self-explanatory"""
    num_tokens = len(tokens)
    headword = tokens[0]
    headword_completed = headword.count('__') == 2
    idx = 0
    while not headword_completed:
        idx += 1
        if idx == num_tokens:
            headword_completed = True
        else:
            headword += ' ' + tokens[idx]
            if headword.count('__') == 2:
                headword_completed = True
    idx += 1
    if idx < num_tokens:
        part_of_speech = tokens[idx]
    else:
        part_of_speech = ''
    if idx > 1:
        # self.num_composite_headwords += 1
        if do_print:
            print OKBLUE + headword + OKCYAN + ' ' + part_of_speech + GRAY \
                + ' <<< Composite headword #' \
                + ENDC
                #+ str(self.num_composite_headwords)
                #+ ENDC
    return headword, part_of_speech

class Checker(object):
    """The class Checker encapsulates all functionalities to check the dictionary"""
    def __init__(self, filename):
        self.filename = filename
        self.num_composite_headwords = 0
        self.num_invalid_endings = 0
        self.num_invalid_tags = 0
        self.num_tag_shit = 0
        self.num_too_many_double_spaces = 0
        self.num_entries_with_triple_spaces = 0

    def treat_invalid_entry_ending(self, entry):
        """Self-explanatory"""
        self.num_invalid_endings += 1
        tokens = entry.split()
        headword = tokens[0]
        print headword + ' ' + FAIL + ' <<< Incorrect entry ending #' \
            + str(self.num_invalid_endings) + ENDC

    def treat_invalid_entry_tags(self, entry, tag):
        """Self-explanatory"""
        self.num_invalid_tags += 1
        tokens = entry.split()
        headword = tokens[0]
        print FAIL + headword + ' ' + BOLD + ':' + tag + ':' + ENDC \
             + ' <<< Invalid tag #' + str(self.num_invalid_tags) + ENDC

    def treat_too_many_double_spaces(self, entry):
        """Self-explanatory"""
        self.num_too_many_double_spaces += 1
        tokens = entry.split()
        headword = tokens[0]
        part_of_speech = tokens[1]
        print headword + ' ' + part_of_speech + FAIL \
            + ' <<< Too many double spaces #' \
            + str(self.num_too_many_double_spaces) + ENDC

    def treat_triple_spaces(self, entry):
        """Self-explanatory"""
        self.num_entries_with_triple_spaces += 1
        tokens = entry.split()
        headword = tokens[0]
        print headword + ' ' + FAIL + ' <<< Triple spaces #' \
            + str(self.num_entries_with_triple_spaces) + ENDC

    def treat_shit_tag(self, entry):
        """Self-explanatory"""
        self.num_tag_shit += 1
        tokens = entry.split()
        headword = tokens[0]
        part_of_speech = tokens[1]
        print headword + ' ' + part_of_speech + FAIL \
            + ' <<< :shit: found; use :hammer: instead' + ENDC

    def check_entries(self):
        """Looking for mistakes in the entries of the dictionary

        Reads the contents of self.dictionary searching for :shit:,
        or :nine: without part of the speech defined
        """
        input_file = open(self.filename, 'r')
        num_wrong_part_of_speech = 0

        for line in input_file:
            entry = line.replace('\n', '')
            if not valid_entry_ending(entry):
                self.treat_invalid_entry_ending(entry)
            succeeded, invalid_tag = valid_entry_tags(entry)
            if not succeeded:
                self.treat_invalid_entry_tags(entry, invalid_tag)
            if entry.count('  ') >= 2:
                self.treat_too_many_double_spaces(entry)
            if entry.count('   ') > 0:
                self.treat_triple_spaces(entry)
            if entry.find(':shit:') > -1:
                self.treat_shit_tag(entry)
            if entry_has_tag_of_any_number(entry, 3, 9):
                tokens = entry.split()
                do_print = True
                headword, part_of_speech = get_headword_and_part_of_speech(tokens, do_print)
                if part_of_speech.find('_') == -1:
                    num_wrong_part_of_speech += 1
                    print FAIL + headword + ' ' + BOLD + part_of_speech + ENDC \
                        + ' <<< Wrong part of speech #' \
                        + str(num_wrong_part_of_speech)

        input_file.close()
        succeeded = bool(self.num_invalid_endings \
            + self.num_invalid_tags \
            + self.num_tag_shit \
            + self.num_too_many_double_spaces \
            + self.num_entries_with_triple_spaces \
            + num_wrong_part_of_speech == 0)
        if succeeded:
            print OKGREEN + 'No entries-related problems were found in file \'' \
                + self.filename + '\'' + ENDC
        else:
            print '\nSummary of issues found'
            print '-----------------------'
            print_colored('Entries with invalid ending', self.num_invalid_endings)
            print_colored('Entries with invalid tags', self.num_invalid_tags)
            print_colored('Entries with tag :shit:', self.num_tag_shit)
            print_colored('Entries with too many double spaces', \
                self.num_too_many_double_spaces)
            print_colored('Entries with triple spaces', self.num_entries_with_triple_spaces)
            print_colored('Entries with wrong part of speech', \
                num_wrong_part_of_speech)
        print
        return succeeded

    def check_duplicated_headwords(self):
        """Self-explanatory"""
        input_file = open(self.filename, 'r')

        repeated = {}
        dictionary = {}

        for line in input_file:
            entry = line.replace('\n', '')
            tokens = entry.split()
            do_print = False
            headword, part_of_speech = get_headword_and_part_of_speech(tokens, do_print)
            if dictionary.get(headword) == 1:
                repeated[headword] = part_of_speech
            dictionary[headword] = 1

        input_file.close()

        size = len(repeated)
        if size > 0:
            repeated_sorted = sorted(repeated)
            print 'Found ' + str(size) + ' duplicated headwords, the very first being:'
            i = 0
            for headword in repeated_sorted:
                print '  ' + FAIL + headword + ' ' + repeated[headword] + ENDC
                i += 1
                if i == 10:
                    break
        else:
            print OKGREEN + 'No duplicated headwords were found' + ENDC
        print

    def check_undef_high_freq_keywords(self):
        """Self-explanatory"""
        input_file = open(self.filename, 'r')

        undefined = {}

        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_high_number(entry):
                if entry_has_tag_hammer(entry):
                    tokens = entry.split()
                    do_print = False
                    headword, part_of_speech = \
                        get_headword_and_part_of_speech(tokens, do_print)
                    undefined[headword] = part_of_speech

        input_file.close()

        size = len(undefined)
        if size > 0:
            undefined_sorted = sorted(undefined)
            print 'Found ' + str(size) \
                + ' undefined high frequency headwords, the very first being:'
            i = 0
            for headword in undefined_sorted:
                print '  ' + FAIL + headword + ' ' + OKCYAN + undefined[headword] + ENDC
                i += 1
                if i == 10:
                    break
        else:
            print OKGREEN + 'No undefined high frequency headwords were found' + ENDC

class Gamer(object):
    """The class Gamer encapsulates all functionalities to play games with the dictionary"""
    def __init__(self, filename):
        self.filename = filename
        self.list = [[], [], [], [], [], [], [], [], []]

    def get_index(self, tag_as_number):
        """Returns the appropriate index to use in list, skipping 1 (we start at :two:)"""
        return tag_as_number - 2

    def gather_high_frequency_headwords(self):
        """Searching for the entries of the dictionary with higher frequency"""
        input_file = open(self.filename, 'r')

        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, 2, 9):
                tokens = entry.split()
                do_print = False
                headword = get_headword_and_part_of_speech(tokens, do_print)[0]
                for i in range(10, 1, -1):
                    if entry_has_tag_of_number(entry, i):
                        self.list[self.get_index(i)] += [headword]

        input_file.close()
        print OKCYAN + '\nSummary of high frequency headwords'
        print '-----------------------------------'
        for i in range(10, 1, -1):
            print 'Entries with ' + str(get_tag(i)) + ' = ' + str(len(self.list[self.get_index(i)]))
        print ENDC

    def play(self):
        index_9m = self.get_index(10)
        question = 1
        for i in range(1, 6):
            index = random.randint(1, len(self.list[index_9m]) - 1)
            print 'Q' + str(question) + ': ' + self.list[index_9m][index]
            question += 1

CHECKER = Checker('dictionary.md')
CHECKER.check_entries()
CHECKER.check_duplicated_headwords()
CHECKER.check_undef_high_freq_keywords()

GAMER = Gamer('dictionary.md')
GAMER.gather_high_frequency_headwords()
GAMER.play()