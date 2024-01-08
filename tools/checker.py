'module docstring should be here'

import os.path
import re
import sys

# From https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
# (see also https://en.wikipedia.org/wiki/ANSI_escape_code)
#
HEADER = '\033[95m'
OK_BLUE = '\033[94m'
OK_CYAN = '\033[96m'
OK_GREEN = '\033[92m'
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
END_C = '\033[0m'
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
    if num_hits > 0:
        return False

    num_possible_headwords = len(re.findall('__[a-zA-Z0-9>]+__', entry))
    num_not_headwords = \
        len(re.findall('__[0-9]+[a-z]*__', entry)) \
        + len(re.findall('__[a-z]__', entry))
    num_headwords = num_possible_headwords - num_not_headwords
    if num_headwords > 1:
        return False

    num_reminder_ribbons = 1 if entry.find('reminder_ribbon') > -1 else 0

    if entry.count('___') > 0 or \
        (entry.count('_') - num_reminder_ribbons) % 2 != 0 or \
        entry.count('_:es:') > 0:
        return False
    return True

def valid_use_of_parentheses_or_brackets(entry):
    """Returns False when finding a wrong number of parentheses or brackets"""
    num_open_char = len(re.findall('\\(', entry))
    num_close_char = len(re.findall('\\)', entry))
    if num_open_char != num_close_char:
        return False

    num_open_char = len(re.findall('\\[', entry))
    num_close_char = len(re.findall('\\]', entry))
    if num_open_char != num_close_char:
        return False

    return True

VALID_TAGS = \
    'three', 'two', 'astonished', 'camera', 'dart', 'eight', 'es', 'four', 'five', \
    'fr', 'hammer', 'm', 'mega', 'mute', 'nine', 'pencil2', \
    'reminder_ribbon','seven', 'six', 'scroll', 'sound'

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

NUMBER_TO_TAG = ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', \
    ':nine::m:'

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
        print('✅ ' + OK_GREEN + message + END_C)
    else:
        print('🐞 ' + FAIL + message + END_C)

def print_colored_if_positive(label, number):
    """Self-explanatory"""
    if number > 0:
        message = label + ' = ' + str(number)
        print('🐞 ' + FAIL + message + END_C)

def get_headword(entry):
    """Self-explanatory"""
    tokens = entry.split()
    num_tokens = len(tokens)
    if num_tokens == 0:
        return '(empty)'
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
    return headword

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
            print(OK_BLUE + headword + OK_CYAN + ' ' + part_of_speech + GRAY \
                + ' « Composite headword' \
                + END_C)
    return headword, part_of_speech, tokens[idx+1:]

VALID_PARTS_OF_SPEECH = \
    '', \
    '_adj informal_', \
    '_adj vulgar slang_', \
    '_adj_', \
    '_adj, adv_', \
    '_adj, adv, conj, pron_', \
    '_adj, adv, n_', \
    '_adj, adv, n, v_', \
    '_adj, adv, n, vt_', \
    '_adj, adv, prep_', \
    '_adj, adv, pron_', \
    '_adj, adv, vt_', \
    '_adj, conj, n_', \
    '_adj, n_', \
    '_adj, n, v_', \
    '_adj, vi_', \
    '_adv_', \
    '_adv, conj, prep_', \
    '_adv, prep_', \
    '_chat_', \
    '_conj_', \
    '_conj, prep_', \
    '_contraction_', \
    '_fig_', \
    '_gramo_', \
    '_n informal_', \
    '_n phr_', \
    '_n pl_', \
    '_n slang_', \
    '_n_', \
    '_n, adj_', \
    '_n, v_', \
    '_phr informal_', \
    '_phr v_', \
    '_phr_', \
    '_pl n_', \
    '_prefix_', \
    '_prep_', \
    '_pron_', \
    '_prov_', \
    '_sentence connector_', \
    '_suffix_', \
    '_trademark_', \
    '_v informal_', \
    '_v_', \
    '_v-link phr_', \
    '_vi_', \
    '_vi/t_', \
    '_vt_'

def entry_misses_part_of_speech(entry):
    """This should be called instead entry_including_hammer_tag_misses_part_of_speech"""
    tokens = entry.split()
    do_print = False
    _, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
    if (part_of_speech not in VALID_PARTS_OF_SPEECH):
        return True
    return False

def entry_has_displaced_part_of_speech(entry):
    """Self-explanatory"""
    for part_of_speech in VALID_PARTS_OF_SPEECH:
        if entry.count(part_of_speech) == 1:
            tokens = entry.split()
            do_print = False
            headword, _, _ = get_headword_part_of_speech_etc(tokens, do_print)
            return entry.count('__ ' + part_of_speech) != 1 and part_of_speech == headword
    return False

class Checker(object):
    """The class Checker encapsulates all functionalities to check the dictionary"""
    def __init__(self, filename):
        if not filename:
            raise ValueError('Filename should not be empty')
        if not os.path.exists(filename):
            raise IOError('File does not exist')

        self.filename = filename
        self.num_composite_headwords = 0
        self.num_displaced_part_of_speech = 0
        self.num_entries_with_triple_spaces = 0
        self.num_entries_with_wrong_type_of_space_character = 0
        self.num_entries_with_tab_character = 0
        self.num_entries_with_straight_single_quote = 0
        self.num_entries_with_straight_double_quote = 0
        self.num_entries_with_double_dash = 0
        self.num_entries_with_colon_underscore = 0
        self.num_entries_with_rogue_underscore = 0
        self.num_entries_with_question_mark = 0
        self.num_invalid_endings = 0
        self.num_invalid_tags = 0
        self.num_invalid_use_of_underscores = 0
        self.num_invalid_use_of_parentheses_or_brackets = 0
        self.num_invalid_syn = 0
        self.num_missing_part_of_speech = 0
        self.num_tag_shit = 0
        self.num_wrong_nine_m = 0
        self.num_too_many_double_spaces = 0
        self.num_wrong_part_of_speech = 0

    def treat_invalid_entry_ending(self, entry):
        """Self-explanatory"""
        self.num_invalid_endings += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect entry ending #' \
            + str(self.num_invalid_endings) + END_C)

    def treat_invalid_underscores_use(self, entry):
        """Self-explanatory"""
        self.num_invalid_use_of_underscores += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of underscores #' \
            + str(self.num_invalid_use_of_underscores) + END_C)

    def treat_invalid_parentheses_or_brackets_use(self, entry):
        """Self-explanatory"""
        self.num_invalid_use_of_parentheses_or_brackets += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of parentheses or brackets #' \
            + str(self.num_invalid_use_of_parentheses_or_brackets) + END_C)

    def treat_invalid_syn(self, entry):
        """Self-explanatory"""
        self.num_invalid_syn += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of syn #' \
            + str(self.num_invalid_syn) + END_C)

    def treat_invalid_entry_tags(self, entry, tag):
        """Self-explanatory"""
        self.num_invalid_tags += 1
        headword = get_headword(entry)
        print(FAIL + headword + ' ' + BOLD + ':' + tag + ':' + END_C \
             + ' « Invalid tag #' + str(self.num_invalid_tags) + END_C)

    def treat_too_many_double_spaces(self, entry):
        """Self-explanatory"""
        self.num_too_many_double_spaces += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL \
            + ' « Too many double spaces #' \
            + str(self.num_too_many_double_spaces) + END_C)

    def treat_triple_spaces(self, entry):
        """Self-explanatory"""
        self.num_entries_with_triple_spaces += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Triple spaces #' \
            + str(self.num_entries_with_triple_spaces) + END_C)

    def treat_wrong_type_of_space_character(self, entry):
        """Self-explanatory"""
        self.num_entries_with_wrong_type_of_space_character += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Wrong type of space character #' \
            + str(self.num_entries_with_wrong_type_of_space_character) + END_C)

    def treat_tab_character(self, entry):
        """Self-explanatory"""
        self.num_entries_with_tab_character += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Tab character(s) #' \
            + str(self.num_entries_with_tab_character) + END_C)

    def treat_straight_single_quote(self, entry):
        """Self-explanatory"""
        self.num_entries_with_straight_single_quote += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Straight single quote #' \
            + str(self.num_entries_with_straight_single_quote) + END_C)

    def treat_straight_double_quote(self, entry):
        """Self-explanatory"""
        self.num_entries_with_straight_double_quote += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Straight double quote #' \
            + str(self.num_entries_with_straight_double_quote) + END_C)

    def treat_double_dash(self, entry):
        """Self-explanatory"""
        self.num_entries_with_double_dash += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Double dash #' \
            + str(self.num_entries_with_double_dash) + END_C)

    def treat_colon_underscore(self, entry):
        """Self-explanatory"""
        self.num_entries_with_colon_underscore += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Colon followed by underscore #' \
            + str(self.num_entries_with_colon_underscore) + END_C)

    def treat_rogue_underscore(self, entry):
        """Self-explanatory"""
        self.num_entries_with_rogue_underscore += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Rogue underscore #' \
            + str(self.num_entries_with_rogue_underscore) + END_C)

    def treat_question_mark(self, entry):
        """Self-explanatory"""
        self.num_entries_with_question_mark += 1
        headword = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Question mark (?) #' \
            + str(self.num_entries_with_question_mark) + END_C)

    def treat_shit_tag(self, entry):
        """Self-explanatory"""
        self.num_tag_shit += 1
        tokens = entry.split()
        headword = tokens[0]
        part_of_speech = tokens[1]
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL \
            + ' « :shit: found; use :hammer: instead' + END_C)

    def treat_wrong_nine_m(self, entry):
        """Self-explanatory"""
        self.num_wrong_nine_m += 1
        tokens = entry.split()
        headword = tokens[0]
        part_of_speech = tokens[1]
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL \
            + ' « :nine:m: found; add missing colon' + END_C)

    def treat_missing_part_of_speech(self, headword, part_of_speech):
        """Self-explanatory"""
        self.num_missing_part_of_speech += 1
        if part_of_speech != '':
            print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL \
            + ' « Missing part of speech found' + END_C)

    def treat_displaced_part_of_speech(self, headword, part_of_speech):
        """Self-explanatory"""
        self.num_displaced_part_of_speech += 1
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL \
            + ' « Displaced part of speech found' + END_C)

    def check_entry(self, entry, do_check_parts_of_speech):
        """Looking and tallying mistakes in a particular entry of the dictionary"""
        if not valid_entry_ending(entry):
            self.treat_invalid_entry_ending(entry)
        if not valid_use_of_underscores(entry):
            self.treat_invalid_underscores_use(entry)
        if not valid_use_of_parentheses_or_brackets(entry):
            self.treat_invalid_parentheses_or_brackets_use(entry)
        if entry.count('_syn_') > 0:
            self.treat_invalid_syn(entry)
        succeeded, invalid_tag = valid_entry_tags(entry)
        if not succeeded:
            self.treat_invalid_entry_tags(entry, invalid_tag)
        if entry.count('  ') >= 2:
            self.treat_too_many_double_spaces(entry)
        if entry.count('   ') > 0:
            self.treat_triple_spaces(entry)
        if entry.count(' ') > 0: # Attention: The space character here is not the common one!
            self.treat_wrong_type_of_space_character(entry)
        if entry.count('	') > 0: # Attention: The space character here is a tab character!
            self.treat_tab_character(entry)
        if entry.count('\'') > 0:
            self.treat_straight_single_quote(entry)
        if entry.count('\"') > 0:
            self.treat_straight_double_quote(entry)
        if entry.count('--') > 0:
            self.treat_double_dash(entry)
        if entry.count(':_') > 0:
            self.treat_colon_underscore(entry)
        if entry.find(' _ ') > -1:
            self.treat_rogue_underscore(entry)
        if entry.find('(?)') > -1:
            self.treat_question_mark(entry)
        if entry.find(':shit:') > -1:
            self.treat_shit_tag(entry)
        if entry.find(':nine:m:') > -1:
            self.treat_wrong_nine_m(entry)
        if do_check_parts_of_speech:
            # if entry_has_tag_of_any_number(entry, 2, 9) and \
            #   entry_misses_part_of_speech(entry):
            if entry_misses_part_of_speech(entry):
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
                do_print = False # True
                headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
                if part_of_speech.find('_') == -1:
                    self.num_wrong_part_of_speech += 1
                    print(FAIL + headword + ' ' + BOLD + part_of_speech + END_C \
                        + ' « Wrong part of speech #' \
                        + str(self.num_wrong_part_of_speech))

    def check_entries(self, do_check_parts_of_speech):
        """Looking for mistakes in the entries of the dictionary

        Reads the contents of self.dictionary checking every single entry
        """
        input_file = open(self.filename, 'r', encoding='utf-8')

        for line in input_file:
            entry = line.replace('\n', '')
            self.check_entry(entry, do_check_parts_of_speech)

        input_file.close()
        succeeded = bool(self.num_displaced_part_of_speech \
            + self.num_invalid_endings \
            + self.num_invalid_tags \
            + self.num_invalid_use_of_underscores \
            + self.num_invalid_use_of_parentheses_or_brackets \
            + self.num_invalid_syn \
            + self.num_tag_shit \
            + self.num_too_many_double_spaces \
            + self.num_entries_with_triple_spaces \
            + self.num_entries_with_wrong_type_of_space_character \
            + self.num_entries_with_tab_character \
            + self.num_entries_with_straight_single_quote \
            + self.num_entries_with_straight_double_quote \
            + self.num_entries_with_double_dash \
            + self.num_entries_with_colon_underscore \
            + self.num_entries_with_rogue_underscore \
            + self.num_entries_with_question_mark \
            + self.num_missing_part_of_speech \
            + self.num_wrong_part_of_speech \
            + self.num_wrong_nine_m == 0)
        if succeeded:
            print('✅ ' + OK_GREEN + 'No entries-related problems were found in file \'' \
                + self.filename + '\'' + END_C)
        else:
            print('\n' + HEADER + 'Summary of issues found' + END_C)
            print(HEADER + '-----------------------' + END_C)
            print_colored_if_positive("Entries with displaced part of speech", \
                self.num_displaced_part_of_speech)
            print_colored_if_positive('Entries with invalid ending', self.num_invalid_endings)
            print_colored_if_positive('Entries with invalid tags', self.num_invalid_tags)
            print_colored_if_positive('Entries with invalid use of underscores', \
                self.num_invalid_use_of_underscores)
            print_colored_if_positive('Entries with invalid use of parentheses or brackets', \
                self.num_invalid_use_of_parentheses_or_brackets)
            print_colored_if_positive('Entries with invalid syn', \
                self.num_invalid_syn)
            print_colored_if_positive('Entries with tag :shit:', self.num_tag_shit)
            print_colored_if_positive('Entries with too many double spaces', \
                self.num_too_many_double_spaces)
            print_colored_if_positive('Entries with triple spaces', self.num_entries_with_triple_spaces)
            print_colored_if_positive('Entries with wrong type of space character [use $ sed -i \'s/ / /g\' ../data/todo.md]', self. num_entries_with_wrong_type_of_space_character)
            print_colored_if_positive('Entries with tab character(s)', self. num_entries_with_tab_character)
            print_colored_if_positive('Entries with straight single quote(s)', self.num_entries_with_straight_single_quote)
            print_colored_if_positive('Entries with straight double quote(s)', self.num_entries_with_straight_double_quote)
            print_colored_if_positive('Entries with double dash', self.num_entries_with_double_dash)
            print_colored_if_positive('Entries with colon followed by underscore', self.num_entries_with_colon_underscore)
            print_colored_if_positive('Entries with rogue underscore', self.num_entries_with_rogue_underscore)
            print_colored_if_positive('Entries with question mark (?)', self.num_entries_with_question_mark)
            print_colored_if_positive('Entries missing part of speech', self.num_missing_part_of_speech)
            print_colored_if_positive('Entries with wrong part of speech', \
                self.num_wrong_part_of_speech)
            print_colored_if_positive('Entries with wrong nine m', self.num_wrong_nine_m)
        print
        return succeeded

    def check_duplicated_headwords(self):
        """Self-explanatory"""
        input_file = open(self.filename, 'r', encoding='utf-8')

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
            print('Found ' + str(size) + ' duplicated headwords, the very first being:')
            i = 0
            for headword in repeated_sorted:
                print('  ' + FAIL + headword + ' ' + repeated[headword] + END_C)
                i += 1
                if i == 10:
                    break # exit loop
        else:
            print('✅ ' + OK_GREEN + 'No duplicated headwords were found' + END_C)
        print
        return bool(size == 0)

    def check_undef_high_freq_keywords(self):
        """Self-explanatory"""
        input_file = open(self.filename, 'r', encoding='utf-8')

        undefined = {}

        NUMBER_MIN = 9 # 8 # 7
        NUMBER_MAX = 9
        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, NUMBER_MIN, NUMBER_MAX):
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
            max_high_frequency_headwords_shown = 10
            print('Found ' + str(size) \
                + ' undefined high frequency headwords, the very first '
                + str(max_high_frequency_headwords_shown)
                + ' being:')
            i = 0
            for headword in undefined_sorted:
                print('  ' + FAIL + headword + ' ' + OK_CYAN + undefined[headword] + END_C)
                i += 1
                if i == max_high_frequency_headwords_shown:
                    break
        else:
            print('✅ ' + OK_GREEN + 'No undefined high frequency headwords were found' + END_C)

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
            clean_rest += leading_text + CYAN + BOLD + token.replace('__', '') + END_C + ' '
        else:
            num_underscores = len(re.findall('_', token))
            if num_underscores == 1:
                if token.find('_') == 0:
                    clean_rest += YELLOW + ITALIC + token.replace('_', '') + ' '
                else:
                    clean_rest += token.replace('_', '') + END_C + ' '
            elif num_underscores == 2:
                clean_rest += OK_GREEN + ITALIC + token.replace('_', '') + END_C + ' '
            else:
                clean_rest += token + ' '

    # Final retouches to clean_rest
    for tag in NUMBER_TO_TAG:
        number = tag_to_number(tag)
        number_str_xt = MAGENTA + '[' + str(number) + ']' + END_C
        clean_rest = clean_rest.replace(tag, number_str_xt)
    clean_rest = clean_rest.replace(':m:', MAGENTA + '(+)' + END_C)

    return CYAN + BOLD + clean_headword + ' ' \
        + END_C + CYAN + ITALIC + clean_part_of_speech + END_C + ' ' + clean_rest

def check(arg, do_check_parts_of_speech):
    filename = '../data/' + arg + ".md"
    print('🔵 ' + OK_BLUE + "Checking " + UNDERLINE + filename + END_C + OK_BLUE + " with do_check_parts_of_speech = " + str(do_check_parts_of_speech) + END_C)
    checker = Checker(filename)
    checker.check_entries(do_check_parts_of_speech)
    checker.check_duplicated_headwords()
    checker.check_undef_high_freq_keywords()

def usageAndAbort(progname, valid_arguments):
    print(BLUE + "Usage: " + progname + " <arguments> # with <arguments> being one or more of " + str(valid_arguments) + END_C)
    sys.exit(1)

def main(progname, argv):
    num_arguments = len(argv)
    print('🔵 ' + OK_BLUE + progname + ': Number of arguments: ' + str(num_arguments) + END_C)
    if num_arguments > 0:
        print('🔵 ' + OK_BLUE + progname + ': Argument list: ' + str(argv) + END_C)

    VALID_ARGUMENTS = [ "abbreviations+", "dictionary", "Ellroy's-lingo", "idioms", "interjections", "todo-idioms", "todo-main", "top-dictionary", "top-idioms" ]
    if num_arguments > len(VALID_ARGUMENTS):
        print(RED + "Too many arguments. Aborting..." + END_C)
        usageAndAbort(progname, VALID_ARGUMENTS)
    for arg in argv:
        if arg not in VALID_ARGUMENTS:
            print(RED + progname + ": Argument `" + arg + "` is not valid." + END_C)
            usageAndAbort(progname, VALID_ARGUMENTS)

    if num_arguments == 0:
        argv = VALID_ARGUMENTS
        print('🔵 ' + OK_BLUE + progname + ': Argument list after adding default arguments: ' + str(argv) + END_C)

    for arg in argv:
        do_check_parts_of_speech = arg != "abbreviations+" and arg != 'Ellroy\'s-lingo' and arg != 'idioms' and arg != 'interjections' and arg != 'todo-idioms' and arg != 'top-idioms'
        check(arg, do_check_parts_of_speech)

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
