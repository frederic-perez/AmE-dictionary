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
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
GRAY = '\033[90m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
ITALIC = '\33[3m'
UNDERLINE = '\033[4m'

def valid_entry_ending(entry):
    """Self-explanatory"""
    valid = entry.endswith('  ')
    return valid

def valid_use_of_underscores(entry):
    """Returns False when finding a bad usage of underscores"""
    num_hits = \
        len(re.findall('__[a-zA-Z0-9>]+_[^_]', entry)) \
        + len(re.findall('[^_]_[a-zA-Z0-9>]+__', entry))
    if num_hits > 0 or \
        entry.count('___') > 0 or \
        entry.count('_') % 2 != 0 or \
        entry.count('_:es:') > 0:
        return False
    return True

VALID_TAGS = [ \
    'three', 'two', 'astonished', 'camera', 'dart', 'eight', 'es', 'four', 'five', \
    'hammer', 'm', 'mega', 'mute', 'nine', 'octocat', 'pencil2', 'seven', 'six']

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

def tag_to_number(tag):
    """Given a tag like :seven:, returns the corresponding number, 7"""
    if tag in NUMBER_TO_TAG:
        index = NUMBER_TO_TAG.index(tag)
        return index + 2
    return None

def entry_has_tag_of_any_number(entry, number_min, number_max):
    """Self-explanatory"""
    for number in range(number_min, number_max + 1):
        if entry.find(get_tag(number)) > -1:
            return True
    return False

def entry_has_tag_of_number(entry, number):
    """Self-explanatory"""
    return entry.find(get_tag(number)) > -1

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

def get_headword_part_of_speech_etc(tokens, do_print=False):
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
        part_of_speech_completed = part_of_speech.count('_') == 2
        while not part_of_speech_completed:
            idx += 1
            if idx == num_tokens:
                part_of_speech_completed = True
            else:
                part_of_speech += ' ' + tokens[idx]
                if part_of_speech.count('_') == 2:
                    part_of_speech_completed = True
    else:
        part_of_speech = ''
    if do_print:
        if ' ' in headword:
            print OKBLUE + headword + OKCYAN + ' ' + part_of_speech + GRAY \
                + ' <<< Composite headword' \
                + ENDC
    return headword, part_of_speech, tokens[idx+1:]

VALID_PARTS_OF_SPEECH = [ \
    '', \
    '_?_', \
    '_abbr_', \
    '_adj_', \
    '_adj, adv_', \
    '_adj, adv, prep_', \
    '_adj, n_', \
    '_adj informal_', \
    '_adj vulgar slang_', \
    '_adv_', \
    '_conj_', \
    '_fig_', \
    '_idiom_', \
    '_interj_', \
    '_interj slang_', \
    '_n_', \
    '_n, adj_', \
    '_n, v_', \
    '_n informal_', \
    '_n phr_', \
    '_phr_', \
    '_phr informal_', \
    '_phr v_', \
    '_pl n_', \
    '_prep_', \
    '_trademark_', \
    '_v_', \
    '_v informal_', \
    '_v intr_', \
    '_v tr_', \
    '_v-link phr_' \
]

def entry_misses_part_of_speech(entry):
    """This should be called instead entry_including_hammer_tag_misses_part_of_speech"""
    tokens = entry.split()
    do_print = False
    _, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
    if (part_of_speech not in VALID_PARTS_OF_SPEECH) and \
        part_of_speech.count(':hammer:') < 1:
        return True
    return False

PARTS_OF_SPEECH = ['_adj_', '_adv_', '_n_', '_v_']

def entry_has_displaced_part_of_speech(entry):
    """Self-explanatory"""
    for part_of_speech in PARTS_OF_SPEECH:
        if entry.count(part_of_speech) == 1:
            return entry.count('__ ' + part_of_speech) != 1
    return False

class Checker(object):
    """The class Checker encapsulates all functionalities to check the dictionary"""
    def __init__(self, filename):
        self.filename = filename
        self.num_composite_headwords = 0
        self.num_displaced_part_of_speech = 0
        self.num_entries_with_triple_spaces = 0
        self.num_invalid_endings = 0
        self.num_invalid_tags = 0
        self.num_invalid_use_of_underscores = 0
        self.num_missing_part_of_speech = 0
        self.num_tag_shit = 0
        self.num_too_many_double_spaces = 0
        self.num_wrong_part_of_speech = 0

    def treat_invalid_entry_ending(self, entry):
        """Self-explanatory"""
        self.num_invalid_endings += 1
        tokens = entry.split()
        num_tokens = len(tokens)
        if num_tokens > 0:
            headword = tokens[0]
            print headword + FAIL + ' <<< Incorrect entry ending #' \
                + str(self.num_invalid_endings) + ENDC
        else:
            print '(empty)' + FAIL + ' <<< Incorrect entry ending #' \
                + str(self.num_invalid_endings) + ENDC

    def treat_invalid_underscores_use(self, entry):
        """Self-explanatory"""
        self.num_invalid_use_of_underscores += 1
        tokens = entry.split()
        headword = tokens[0]
        print headword + FAIL + ' <<< Incorrect use of underscores #' \
            + str(self.num_invalid_use_of_underscores) + ENDC

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
        print headword + FAIL + ' <<< Triple spaces #' \
            + str(self.num_entries_with_triple_spaces) + ENDC

    def treat_shit_tag(self, entry):
        """Self-explanatory"""
        self.num_tag_shit += 1
        tokens = entry.split()
        headword = tokens[0]
        part_of_speech = tokens[1]
        print headword + ' ' + part_of_speech + FAIL \
            + ' <<< :shit: found; use :hammer: instead' + ENDC

    def treat_missing_part_of_speech(self, headword, part_of_speech):
        """Self-explanatory"""
        self.num_missing_part_of_speech += 1
        if part_of_speech != '' and \
            part_of_speech != '_?_' and \
            part_of_speech.count(':hammer:') < 1:
            print headword + ' ' + part_of_speech + FAIL \
            + ' <<< missing part of speech found' + ENDC

    def treat_displaced_part_of_speech(self, headword, part_of_speech):
        """Self-explanatory"""
        self.num_displaced_part_of_speech += 1
        print headword + ' ' + part_of_speech + FAIL \
            + ' <<< displaced part of speech found' + ENDC

    def check_entry(self, entry):
        """Looking and tallying mistakes in a particular entry of the dictionary"""
        if not valid_entry_ending(entry):
            self.treat_invalid_entry_ending(entry)
        if not valid_use_of_underscores(entry):
            self.treat_invalid_underscores_use(entry)
        succeeded, invalid_tag = valid_entry_tags(entry)
        if not succeeded:
            self.treat_invalid_entry_tags(entry, invalid_tag)
        if entry.count('  ') >= 2:
            self.treat_too_many_double_spaces(entry)
        if entry.count('   ') > 0:
            self.treat_triple_spaces(entry)
        if entry.find(':shit:') > -1:
            self.treat_shit_tag(entry)
        if entry_has_tag_of_any_number(entry, 2, 9) and \
           entry_misses_part_of_speech(entry):
            tokens = entry.split()
            do_print = False
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
            self.treat_missing_part_of_speech(headword, part_of_speech)
        if entry_has_displaced_part_of_speech(entry):
            tokens = entry.split()
            do_print = False
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
            self.treat_displaced_part_of_speech(headword, part_of_speech)
        if entry_has_tag_of_any_number(entry, 3, 9):
            tokens = entry.split()
            do_print = True
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
            if part_of_speech.find('_') == -1 or \
                part_of_speech.find('?') > 0 or \
                part_of_speech == '_adverb_':
                self.num_wrong_part_of_speech += 1
                print FAIL + headword + ' ' + BOLD + part_of_speech + ENDC \
                    + ' <<< Wrong part of speech #' \
                    + str(self.num_wrong_part_of_speech)

    def check_entries(self):
        """Looking for mistakes in the entries of the dictionary

        Reads the contents of self.dictionary checking every single entry
        """
        input_file = open(self.filename, 'r')

        for line in input_file:
            entry = line.replace('\n', '')
            self.check_entry(entry)

        input_file.close()
        succeeded = bool(self.num_displaced_part_of_speech \
            + self.num_invalid_endings \
            + self.num_invalid_tags \
            + self.num_invalid_use_of_underscores \
            + self.num_tag_shit \
            + self.num_too_many_double_spaces \
            + self.num_entries_with_triple_spaces \
            + self.num_missing_part_of_speech \
            + self.num_wrong_part_of_speech == 0)
        if succeeded:
            print OKGREEN + 'No entries-related problems were found in file \'' \
                + self.filename + '\'' + ENDC
        else:
            print '\nSummary of issues found'
            print '-----------------------'
            print_colored("Entries with displaced part of speech", \
                self.num_displaced_part_of_speech)
            print_colored('Entries with invalid ending', self.num_invalid_endings)
            print_colored('Entries with invalid use of underscores', \
                self.num_invalid_use_of_underscores)
            print_colored('Entries with invalid tags', self.num_invalid_tags)
            print_colored('Entries with tag :shit:', self.num_tag_shit)
            print_colored('Entries with too many double spaces', \
                self.num_too_many_double_spaces)
            print_colored('Entries with triple spaces', self.num_entries_with_triple_spaces)
            print_colored('Entries missing part of speech', self.num_missing_part_of_speech)
            print_colored('Entries with wrong part of speech', \
                self.num_wrong_part_of_speech)
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
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
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
                    break # exit loop
        else:
            print OKGREEN + 'No duplicated headwords were found' + ENDC
        print
        return bool(size == 0)

    def check_undef_high_freq_keywords(self):
        """Self-explanatory"""
        input_file = open(self.filename, 'r')

        undefined = {}

        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, 7, 9):
                if entry_has_tag_hammer(entry):
                    tokens = entry.split()
                    do_print = False
                    headword, part_of_speech, _ = \
                        get_headword_part_of_speech_etc(tokens, do_print)
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

        return bool(size == 0)

def get_index(tag_as_number):
    """Returns the appropriate index to use in list, skipping 1 (we start at :two:)"""
    return tag_as_number - 2

def format_to_print(entry):
    """Returns a str with the formatted version of the input"""
    tokens = entry.split()
    do_print = False
    headword, part_of_speech, rest = get_headword_part_of_speech_etc(tokens, do_print)
    clean_headword = headword.replace('__', '')
    clean_part_of_speech = part_of_speech.replace('_', '')
    clean_rest = ''
    for token in rest:
        if token.find('__') > -1:
            leading_text = '\n'
            if re.search('__[a-z]__', token) != None:
                leading_text += ' '
            clean_rest += leading_text + CYAN + BOLD + token.replace('__', '') + ENDC + ' '
        else:
            num_underscores = len(re.findall('_', token))
            if num_underscores == 1:
                if token.find('_') == 0:
                    clean_rest += YELLOW + ITALIC + token.replace('_', '') + ' '
                else:
                    clean_rest += token.replace('_', '') + ENDC + ' '
            elif num_underscores == 2:
                clean_rest += OKGREEN + ITALIC + token.replace('_', '') + ENDC + ' '
            else:
                clean_rest += token + ' '

    # Final retouches to clean_rest
    for tag in NUMBER_TO_TAG:
        number = tag_to_number(tag)
        number_str_xt = MAGENTA + '[' + str(number) + ']' + ENDC
        clean_rest = clean_rest.replace(tag, number_str_xt)
    clean_rest = clean_rest.replace(':m:', MAGENTA + '(+)' + ENDC)

    return CYAN + BOLD + clean_headword + ' ' \
        + ENDC + CYAN + ITALIC + clean_part_of_speech + ENDC + ' ' + clean_rest

class Game(object):
    """The class Game encapsulates all functionalities to play games with the dictionary"""
    def __init__(self, filename):
        self.filename = filename
        self.list = [[], [], [], [], [], [], [], [], []]

    def gather_high_frequency_headwords(self):
        """Searching for the entries of the dictionary with higher frequency"""
        input_file = open(self.filename, 'r')

        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, 2, 9):
                num_additions = 0
                for i in range(10, 1, -1):
                    if entry_has_tag_of_number(entry, i):
                        self.list[get_index(i)] += [entry]
                        if i == 10:
                            break # to avoid adding to lists :nine::m: and :nine:
                        num_additions += 1
                        if num_additions > 1:
                            print FAIL + entry \
                                + ' <<< Too many numeric tags' + ENDC

        input_file.close()
        print OKCYAN + '\nSummary of high frequency headwords'
        print '-----------------------------------'
        for i in range(10, 1, -1):
            print 'Entries with ' + str(get_tag(i)) + ' = ' + str(len(self.list[get_index(i)]))
        print ENDC

    def play(self):
        """Method aimed at learning definitions"""
        index_9m = get_index(10)
        question = 1
        do_quit = False
        while not do_quit:
            index = random.randint(0, len(self.list[index_9m]) - 1)
            entry = self.list[index_9m][index]
            tokens = entry.split()
            do_print = False
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
            clean_headword = headword.replace('__', '')
            clean_part_of_speech = part_of_speech.replace('_', '')
            print FAIL + 'Q' + ENDC + FAIL + str(question) + ': ' + BOLD + clean_headword + ' ' \
                + ENDC + FAIL + ITALIC + clean_part_of_speech + ENDC
            # print OKCYAN + '  ' + entry + ENDC
            print format_to_print(entry)
            question += 1
            user_response = raw_input(OKBLUE + 'Quit (q)? ' + ENDC)
            if user_response == 'q':
                do_quit = True

    def print_nine_m(self):
        """Method aimed at learning definitions"""
        index_9m = get_index(10)
        regex = re.compile(r"<sup>\d</sup>")
        for entry in self.list[index_9m]:
            tokens = entry.split()
            do_print = False
            headword, _, _ = get_headword_part_of_speech_etc(tokens, do_print)
            headword_for_wordcloud = headword.replace('__', '')
            headword_for_wordcloud = regex.sub('', headword_for_wordcloud)
            headword_for_wordcloud = headword_for_wordcloud.replace(' ', '~')
            print headword_for_wordcloud,
        print

# DICTIONARY = '/home/fperez/hats/fpcx-GitHub/AmE-dictionary/fleeting/pre-todo.md'
DICTIONARY = '../data/dictionary.md'

CHECKER = Checker(DICTIONARY)
CHECKER.check_entries()

game = Game(DICTIONARY)
game.gather_high_frequency_headwords()
game.print_nine_m()
game.play()
