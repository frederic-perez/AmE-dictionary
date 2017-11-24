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

def valid_entry_ending(entry):
    """Self-explanatory"""
    valid = entry.endswith('  ')
    return valid

def entry_has_tag_of_number(entry):
    """Self-explanatory"""
    return entry.find(':nine:') > -1 \
        or entry.find(':eight:') > -1 \
        or entry.find(':seven:') > -1 \
        or entry.find(':six:') > -1 \
        or entry.find(':five:') > -1 \
        or entry.find(':four:') > -1

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

class Checker(object):
    """The class Checker encapsulates all functionalities to check the dictionary"""
    def __init__(self, filename):
        self.filename = filename
        self.num_composite_headwords = 0
        self.num_invalid_endings = 0
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

    def get_headword_and_next_token_idx(self, tokens, do_print=False):
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
        if idx > 1:
            self.num_composite_headwords += 1
            if do_print:
                print OKBLUE + headword + GRAY + ' <<< Composite headword #' \
                    + str(self.num_composite_headwords) + ENDC
        return headword, idx

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
            if entry.count('  ') > 2:
                self.treat_too_many_double_spaces(entry)
            if entry.count('   ') > 0:
                self.treat_triple_spaces(entry)
            if entry.find(':shit:') > -1:
                self.treat_shit_tag(entry)
            if entry_has_tag_of_number(entry):
                tokens = entry.split()
                do_print = True
                headword, idx = self.get_headword_and_next_token_idx(tokens, do_print)
                part_of_speech = tokens[idx]
                if part_of_speech.find('_') == -1:
                    num_wrong_part_of_speech += 1
                    print FAIL + headword + ' ' + BOLD + part_of_speech + ENDC \
                        + ' <<< Wrong part of speech #' \
                        + str(num_wrong_part_of_speech)

        input_file.close()
        succeeded = bool(self.num_invalid_endings \
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
            headword, _ = self.get_headword_and_next_token_idx(tokens, do_print)
            if dictionary.get(headword) == 1:
                repeated[headword] = 1
            dictionary[headword] = 1

        input_file.close()

        size = len(repeated)
        if size > 0:
            repeated_sorted = sorted(repeated)
            print 'Found ' + str(size) + ' duplicated headwords, the very first being:'
            i = 0
            for headword in repeated_sorted:
                print '  ' + FAIL + headword + ENDC
                i += 1
                if i == 10:
                    break
        else:
            print OKGREEN + 'No duplicated headwords were found' + ENDC

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
                    headword, _ = self.get_headword_and_next_token_idx(tokens, do_print)
                    undefined[headword] = 1

        input_file.close()

        size = len(undefined)
        if size > 0:
            undefined_sorted = sorted(undefined)
            print 'Found ' + str(size) \
                + ' undefined high frequency headwords, the very first being:'
            i = 0
            for headword in undefined_sorted:
                print '  ' + FAIL + headword + ENDC
                i += 1
                if i == 10:
                    break
        else:
            print OKGREEN + 'No undefined high frequency headwords were found' + ENDC

def use_random(number):
    "This is a WIP function"
    # We should sort the words to study randomly--in other words, shuffle them
    if number > 0:
        print 'Random integer between 1 and', number, ":",
        print random.randint(1, number)
    else:
        print 'Input number =', number, 'is not positive'

CHECKER = Checker('dictionary.md')
CHECKER.check_entries()
CHECKER.check_duplicated_headwords()
print
CHECKER.check_undef_high_freq_keywords()
print

use_random(100)
