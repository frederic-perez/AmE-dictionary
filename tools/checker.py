"""module docstring should be here"""

import os.path
import re
import sys

from typing import Final

# From https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
# (see also https://en.wikipedia.org/wiki/ANSI_escape_code)
#
HEADER: Final[str] = '\033[95m'
OK_BLUE: Final[str] = '\033[94m'
OK_CYAN: Final[str] = '\033[96m'
OK_GREEN: Final[str] = '\033[92m'
WARNING: Final[str] = '\033[93m'
RED: Final[str] = '\033[31m'
GREEN: Final[str] = '\033[32m'
YELLOW: Final[str] = '\033[33m'
BLUE: Final[str] = '\033[34m'
MAGENTA: Final[str] = '\033[35m'
CYAN: Final[str] = '\033[36m'
WHITE: Final[str] = '\033[37m'
GRAY: Final[str] = '\033[90m'
FAIL: Final[str] = '\033[91m'
END_C: Final[str] = '\033[0m'
BOLD: Final[str] = '\033[1m'
ITALIC: Final[str] = '\33[3m'
UNDERLINE: Final[str] = '\033[4m'


def valid_entry_ending(entry: str) -> bool:
    """Self-explanatory"""
    valid: Final[bool] = entry.endswith('  ')
    return valid


def valid_use_of_underscores(entry: str) -> bool:
    """Returns False when finding a bad usage of underscores"""
    num_hits: Final[int] = (len(re.findall('__[a-zA-Z0-9>]+_[^_]', entry))
                            + len(re.findall('[^_]_[a-zA-Z0-9>]+__', entry)))
    if num_hits > 0:
        return False

    num_possible_headwords: Final[int] = len(re.findall('__[a-zA-Z0-9>]+__', entry))
    num_not_headwords: Final[int] = (len(re.findall('__[0-9]+[a-z]*__', entry))
                                     + len(re.findall('__[a-z]__', entry)))
    num_headwords: Final[int] = num_possible_headwords - num_not_headwords
    if num_headwords > 1:
        return False

    num_reminder_ribbons: Final[int] = 1 if entry.find('reminder_ribbon') > -1 else 0
    num_smiling_imps: Final[int] = 1 if entry.find('smiling_imp') > -1 else 0

    if entry.count('___') > 0 or (entry.count('_') - num_reminder_ribbons - num_smiling_imps) % 2 != 0 or entry.count('_:es:') > 0:
        return False
    return True


def valid_use_of_parentheses_or_brackets(entry: str) -> bool:
    """Returns False when finding a wrong number of parentheses or brackets"""
    num_open_parentheses: Final[int] = len(re.findall('\\(', entry))
    num_close_parentheses: Final[int] = len(re.findall('\\)', entry))
    if num_open_parentheses != num_close_parentheses:
        return False

    num_open_brackets: Final[int] = len(re.findall('\\[', entry))
    num_close_brackets: Final[int] = len(re.findall(']', entry))
    if num_open_brackets != num_close_brackets:
        return False

    return True


# TODO: Transform to Enum
VALID_TAGS: Final[tuple[str, ...]] = (
    'three', 'two', 'astonished', 'camera', 'dart', 'eight', 'es', 'four', 'five', 'fr', 'hammer', 'm', 'mega', 'mute',
    'nine', 'pencil2', 'reminder_ribbon', 'scroll', 'seven', 'six', 'smiling_imp', 'sound')


def valid_tag(tag: str) -> bool:
    """Returns True when tag is an allowed one; False otherwise"""
    return tag in VALID_TAGS


def valid_entry_tags(entry: str) -> tuple[bool, str]:
    """Self-explanatory"""
    tags: Final[list[str]] = re.findall(r':(\w+):', entry)
    for tag in tags:
        if not valid_tag(tag):
            return False, tag
    return True, ''


NUMBER_TO_TAG: Final[tuple[str, ...]] = (
    ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':nine::m:')


def get_tag(number: int) -> str:
    """"Given an input number, an index is set to access a list to get the corresponding tag"""
    index: Final[int] = number - 2
    return NUMBER_TO_TAG[index]


def tag_to_number(tag: str) -> int:
    """Given a tag like :seven:, returns the corresponding number, 7"""
    if tag in NUMBER_TO_TAG:
        index: int = NUMBER_TO_TAG.index(tag)
        return index + 2
    raise ValueError(f'{tag} is not in {NUMBER_TO_TAG}')


def entry_has_tag_of_any_number(entry: str, number_min: int, number_max: int) -> bool:
    """Self-explanatory"""
    for number in range(number_min, number_max + 1):
        if entry.find(get_tag(number)) > -1:
            return True
    return False


def entry_has_tag_of_number(entry: str, number: int) -> bool:
    """Self-explanatory"""
    return entry.find(get_tag(number)) > -1


def entry_has_tag_hammer(entry: str) -> bool:
    """Self-explanatory"""
    return entry.find(':hammer:') > -1

def print_colored(label: str, number: int) -> None:
    """Self-explanatory"""
    message: Final[str] = label + ' = ' + str(number)
    emoji, color = (lambda: ('✅', OK_GREEN) if number == 0 else ('🐞', FAIL))()
    print(emoji + ' ' + color + message + END_C)

def print_colored_if_positive(label: str, number: int) -> None:
    """Self-explanatory"""
    if number > 0:
        message: Final[str] = label + ' = ' + str(number)
        print('🐞 ' + FAIL + message + END_C)


def get_headword(entry: str) -> str:
    """Self-explanatory"""
    tokens: Final[list[str]] = entry.split()
    num_tokens: Final[int] = len(tokens)
    if num_tokens == 0:
        return '(empty)'
    headword: str = tokens[0]
    headword_completed: bool = headword.count('__') == 2
    idx: int = 0
    while not headword_completed:
        idx += 1
        if idx == num_tokens:
            headword_completed = True
        else:
            headword += ' ' + tokens[idx]
            if headword.count('__') == 2:
                headword_completed = True
    return headword


def get_headword_part_of_speech_etc(tokens: list[str], do_print: bool = False) -> tuple[str, str, list[str]]:
    """Self-explanatory"""
    num_tokens: Final[int] = len(tokens)
    headword: str = tokens[0]
    headword_completed: bool = headword.count('__') == 2
    idx: int = 0
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
        part_of_speech: str = tokens[idx]
        part_of_speech_completed: bool = part_of_speech.count('_') == 2
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
            print(OK_BLUE + headword + OK_CYAN + ' ' + part_of_speech + GRAY + ' « Composite headword' + END_C)
    return headword, part_of_speech, tokens[idx + 1:]


VALID_PARTS_OF_SPEECH: Final[tuple[str, ...]] = (
    '',
    '_adj informal_',
    '_adj vulgar slang_',
    '_adj_',
    '_adj, adv_',
    '_adj, adv, conj, pron_',
    '_adj, adv, n_',
    '_adj, adv, n, v_',
    '_adj, adv, n, vt_',
    '_adj, adv, prep_',
    '_adj, adv, pron_',
    '_adj, adv, vt_',
    '_adj, conj, n_',
    '_adj, n_',
    '_adj, n, v_',
    '_adj, v_',
    '_adj, vi_',
    '_adv_',
    '_adv, conj, prep_',
    '_adv, prep_',
    '_chat_',
    '_conj_',
    '_conj, prep_',
    '_contraction_',
    '_determiner_',
    '_fig_',
    '_gramo_',
    '_n informal_',
    '_n phr_',
    '_n pl_',
    '_n slang_',
    '_n_',
    '_n, adj_',
    '_n, n pl_',
    '_n, prep_',
    '_n, v_',
    '_n, vi_',
    '_n, vt_',
    '_phr informal_',
    '_phr v_',
    '_phr_',
    '_pl n_',
    '_prefix_',
    '_prep_',
    '_pron_',
    '_prov_',
    '_sentence connector_',
    '_suffix_',
    '_trademark_',
    '_v informal_',
    '_v_',
    '_v-link phr_',
    '_vi_',
    '_vi/t_',
    '_vt_')


def entry_misses_part_of_speech(entry: str) -> bool:
    """This should be called instead entry_including_hammer_tag_misses_part_of_speech"""
    tokens: Final[list[str]] = entry.split()
    do_print: Final[bool] = False
    _, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
    if part_of_speech not in VALID_PARTS_OF_SPEECH:
        return True
    return False


def entry_has_displaced_part_of_speech(entry: str) -> bool:
    """Self-explanatory"""
    do_print: Final[bool] = False
    for part_of_speech in VALID_PARTS_OF_SPEECH:
        if entry.count(part_of_speech) == 1:
            tokens: list[str] = entry.split()
            headword, _, _ = get_headword_part_of_speech_etc(tokens, do_print)
            return entry.count('__ ' + part_of_speech) != 1 and part_of_speech == headword
    return False


def overwrite_previous_line(message: str) -> None:
    # Move the cursor up one line
    print("\033[F", end="")
    # Overwrite the line with the new message
    print(message)


class Checker(object):
    """The class Checker encapsulates all functionalities to check the dictionary"""
    file_path: Final[str]

    def __new__(cls, file_path: str) -> 'Checker':
        if not file_path:
            raise ValueError('file_path should not be empty')
        if not os.path.exists(file_path):
            raise IOError('File does not exist')
        return object.__new__(cls)

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.line_number: int = 0
        self.num_composite_headwords: int = 0
        self.num_displaced_part_of_speech: int = 0
        self.num_empty_entries: int = 0
        self.num_entries_with_triple_spaces: int = 0
        self.num_entries_with_wrong_type_of_space_character: int = 0
        self.num_entries_with_tab_character: int = 0
        self.num_entries_with_straight_single_quote: int = 0
        self.num_entries_with_straight_double_quote: int = 0
        self.num_entries_with_double_dash: int = 0
        self.num_entries_with_colon_underscore: int = 0
        self.num_entries_with_rogue_underscore: int = 0
        self.num_entries_with_question_mark: int = 0
        self.num_invalid_endings: int = 0
        self.num_invalid_tags: int = 0
        self.num_invalid_use_of_underscores: int = 0
        self.num_invalid_use_of_parentheses_or_brackets: int = 0
        self.num_invalid_syn: int = 0
        self.num_missing_part_of_speech: int = 0
        self.num_tag_shit: int = 0
        self.num_wrong_nine_m: int = 0
        self.num_too_many_double_spaces: int = 0
        self.num_wrong_part_of_speech: int = 0

    # TODO: Refactor methods below to reduce code duplication
    def treat_empty_entry(self) -> None:
        """Self-explanatory"""
        self.num_empty_entries += 1
        print(FAIL + 'Empty entry #'
              + str(self.num_empty_entries) + ' (line ' + str(self.line_number) + ')' + END_C)

    def treat_invalid_entry_ending(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_invalid_endings += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect entry ending #'
              + str(self.num_invalid_endings) + END_C)

    def treat_invalid_underscores_use(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_invalid_use_of_underscores += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of underscores #'
              + str(self.num_invalid_use_of_underscores) + END_C)

    def treat_invalid_parentheses_or_brackets_use(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_invalid_use_of_parentheses_or_brackets += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of parentheses or brackets #'
              + str(self.num_invalid_use_of_parentheses_or_brackets) + END_C)

    def treat_invalid_syn(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_invalid_syn += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Incorrect use of syn #'
              + str(self.num_invalid_syn) + END_C)

    def treat_invalid_entry_tags(self, entry: str, tag: str) -> None:
        """Self-explanatory"""
        self.num_invalid_tags += 1
        headword: Final[str] = get_headword(entry)
        print(FAIL + headword + ' ' + BOLD + ':' + tag + ':' + END_C
              + ' « Invalid tag #' + str(self.num_invalid_tags) + END_C)

    def treat_too_many_double_spaces(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_too_many_double_spaces += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL
              + ' « Too many double spaces #'
              + str(self.num_too_many_double_spaces) + END_C)

    def treat_triple_spaces(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_triple_spaces += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Triple spaces #'
              + str(self.num_entries_with_triple_spaces) + END_C)

    def treat_wrong_type_of_space_character(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_wrong_type_of_space_character += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Wrong type of space character #'
              + str(self.num_entries_with_wrong_type_of_space_character) + END_C)

    def treat_tab_character(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_tab_character += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Tab character(s) #'
              + str(self.num_entries_with_tab_character) + END_C)

    def treat_straight_single_quote(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_straight_single_quote += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Straight single quote #'
              + str(self.num_entries_with_straight_single_quote) + END_C)

    def treat_straight_double_quote(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_straight_double_quote += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Straight double quote #'
              + str(self.num_entries_with_straight_double_quote) + END_C)

    def treat_double_dash(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_double_dash += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Double dash #'
              + str(self.num_entries_with_double_dash) + END_C)

    def treat_colon_underscore(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_colon_underscore += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Colon followed by underscore #'
              + str(self.num_entries_with_colon_underscore) + END_C)

    def treat_rogue_underscore(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_rogue_underscore += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Rogue underscore #'
              + str(self.num_entries_with_rogue_underscore) + END_C)

    def treat_question_mark(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_entries_with_question_mark += 1
        headword: Final[str] = get_headword(entry)
        print(OK_BLUE + BOLD + headword + END_C + FAIL + ' « Question mark (?) #'
              + str(self.num_entries_with_question_mark) + END_C)

    def treat_shit_tag(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_tag_shit += 1
        tokens: Final[list[str]] = entry.split()
        headword: Final[str] = tokens[0]
        part_of_speech: Final[str] = tokens[1]
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL
              + ' « :shit: found; use :hammer: instead' + END_C)

    def treat_wrong_nine_m(self, entry: str) -> None:
        """Self-explanatory"""
        self.num_wrong_nine_m += 1
        tokens: Final[list[str]] = entry.split()
        headword: Final[str] = tokens[0]
        part_of_speech: Final[str] = tokens[1]
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL
              + ' « :nine:m: found; add missing colon' + END_C)

    def treat_missing_part_of_speech(self, headword: str, part_of_speech: str) -> None:
        """Self-explanatory"""
        self.num_missing_part_of_speech += 1
        if part_of_speech != '':
            print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL
                  + ' « Missing part of speech found' + END_C)

    def treat_displaced_part_of_speech(self, headword: str, part_of_speech: str) -> None:
        """Self-explanatory"""
        self.num_displaced_part_of_speech += 1
        print(OK_BLUE + BOLD + headword + END_C + ' ' + part_of_speech + FAIL
              + ' « Displaced part of speech found' + END_C)

    def check_entry(self, entry: str, do_check_parts_of_speech: bool) -> None:
        """Looking and tallying mistakes in a particular entry of the dictionary"""
        self.line_number += 1
        if not entry or entry.isspace():
            self.treat_empty_entry()
            return  # No need to check further
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
        if entry.count(' ') > 0:  # Attention: The space character here is not the common one!
            self.treat_wrong_type_of_space_character(entry)
        if entry.count('	') > 0:  # Attention: The space character here is a tab character!
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
                tokens: list[str] = entry.split()
                do_print: bool = False
                headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
                self.treat_missing_part_of_speech(headword, part_of_speech)
            if entry_has_displaced_part_of_speech(entry):
                tokens = entry.split()
                do_print = False
                headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
                self.treat_displaced_part_of_speech(headword, part_of_speech)
            if entry_has_tag_of_any_number(entry, 3, 9):
                tokens = entry.split()
                do_print = False  # True
                headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
                if part_of_speech.find('_') == -1:
                    self.num_wrong_part_of_speech += 1
                    print(FAIL + headword + ' ' + BOLD + part_of_speech + END_C
                          + ' « Wrong part of speech #'
                          + str(self.num_wrong_part_of_speech))

    def check_entries(self, do_check_parts_of_speech: bool) -> bool:
        """Looking for mistakes in the entries of the dictionary

        Reads the contents of self's file_path checking every single entry
        """
        input_file: Final = open(self.file_path, 'r', encoding='utf-8')

        for line in input_file:
            entry: str = line.replace('\n', '')
            self.check_entry(entry, do_check_parts_of_speech)

        input_file.close()
        num_failures: Final[int] = (
            self.num_empty_entries
            + self.num_displaced_part_of_speech
            + self.num_invalid_endings
            + self.num_invalid_tags
            + self.num_invalid_use_of_underscores
            + self.num_invalid_use_of_parentheses_or_brackets
            + self.num_invalid_syn
            + self.num_tag_shit
            + self.num_too_many_double_spaces
            + self.num_entries_with_triple_spaces
            + self.num_entries_with_wrong_type_of_space_character
            + self.num_entries_with_tab_character
            + self.num_entries_with_straight_single_quote
            + self.num_entries_with_straight_double_quote
            + self.num_entries_with_double_dash
            + self.num_entries_with_colon_underscore
            + self.num_entries_with_rogue_underscore
            + self.num_entries_with_question_mark
            + self.num_missing_part_of_speech
            + self.num_wrong_part_of_speech
            + self.num_wrong_nine_m)
        succeeded: Final[bool] = num_failures == 0
        if not succeeded:
            print('\n' + HEADER + f'Summary of issues found ({num_failures})' + END_C)
            print(HEADER + '-----------------------' + END_C)
            print_colored_if_positive("Empty entries", self.num_empty_entries)
            print_colored_if_positive("Entries with displaced part of speech",
                                      self.num_displaced_part_of_speech)
            print_colored_if_positive('Entries with invalid ending', self.num_invalid_endings)
            print_colored_if_positive('Entries with invalid tags', self.num_invalid_tags)
            print_colored_if_positive('Entries with invalid use of underscores',
                                      self.num_invalid_use_of_underscores)
            print_colored_if_positive('Entries with invalid use of parentheses or brackets',
                                      self.num_invalid_use_of_parentheses_or_brackets)
            print_colored_if_positive('Entries with invalid syn', self.num_invalid_syn)
            print_colored_if_positive('Entries with tag :shit:', self.num_tag_shit)
            print_colored_if_positive('Entries with too many double spaces', self.num_too_many_double_spaces)
            print_colored_if_positive('Entries with triple spaces', self.num_entries_with_triple_spaces)
            print_colored_if_positive(
                'Entries with wrong type of space character [use $ sed -i \'s/ / /g\' ../data/todo.md]',
                self.num_entries_with_wrong_type_of_space_character)
            print_colored_if_positive('Entries with tab character(s)', self.num_entries_with_tab_character)
            print_colored_if_positive('Entries with straight single quote(s)',
                                      self.num_entries_with_straight_single_quote)
            print_colored_if_positive('Entries with straight double quote(s)',
                                      self.num_entries_with_straight_double_quote)
            print_colored_if_positive('Entries with double dash', self.num_entries_with_double_dash)
            print_colored_if_positive('Entries with colon followed by underscore',
                                      self.num_entries_with_colon_underscore)
            print_colored_if_positive('Entries with rogue underscore', self.num_entries_with_rogue_underscore)
            print_colored_if_positive('Entries with question mark (?)', self.num_entries_with_question_mark)
            print_colored_if_positive('Entries missing part of speech', self.num_missing_part_of_speech)
            print_colored_if_positive('Entries with wrong part of speech', self.num_wrong_part_of_speech)
            print_colored_if_positive('Entries with wrong nine m', self.num_wrong_nine_m)
        return succeeded

    def check_duplicated_headwords(self) -> bool:
        """Self-explanatory"""
        input_file: Final = open(self.file_path, 'r', encoding='utf-8')

        repeated: dict[str, str] = {}
        dictionary: dict[str, int] = {}

        for line in input_file:
            entry: str = line.replace('\n', '')
            tokens: list[str] = entry.split()
            do_print: bool = False
            headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
            if dictionary.get(headword) == 1:
                repeated[headword] = part_of_speech
            dictionary[headword] = 1

        input_file.close()

        size: Final[int] = len(repeated)
        if size > 0:
            repeated_sorted: Final[list[str]] = sorted(repeated)
            print('Found ' + str(size) + ' duplicated headwords, the very first being:')
            i: int = 0
            for headword in repeated_sorted:
                print('  ' + FAIL + headword + ' ' + repeated[headword] + END_C)
                i += 1
                if i == 10:
                    break  # exit loop
        return size == 0

    def check_undef_high_freq_keywords(self) -> bool:
        """Self-explanatory"""
        input_file: Final = open(self.file_path, 'r', encoding='utf-8')

        undefined: dict[str, str] = {}

        number_min: Final[int] = 9  # 8 # 7
        number_max: Final[int] = 9
        for line in input_file:
            entry: str = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, number_min, number_max):
                if entry_has_tag_hammer(entry):
                    tokens: list[str] = entry.split()
                    do_print: bool = False
                    headword, part_of_speech, _ = get_headword_part_of_speech_etc(tokens, do_print)
                    undefined[headword] = part_of_speech

        input_file.close()

        size: Final[int] = len(undefined)
        if size > 0:
            undefined_sorted: Final[list[str]] = sorted(undefined)
            max_high_frequency_headwords_shown: Final[int] = 10
            print('Found ' + str(size)
                  + ' undefined high frequency headwords, the very first '
                  + str(max_high_frequency_headwords_shown)
                  + ' being:')
            i: int = 0
            for headword in undefined_sorted:
                print('  ' + FAIL + headword + ' ' + OK_CYAN + undefined[headword] + END_C)
                i += 1
                if i == max_high_frequency_headwords_shown:
                    break

        return size == 0


def get_index(tag_as_number: int) -> int:
    """Returns the appropriate index to use in list, skipping 1 (we start at :two:)"""
    return tag_as_number - 2


def format_to_print(entry: str) -> str:
    """Returns a str with the formatted version of the input"""
    tokens: Final[list[str]] = entry.split()
    do_print: Final[bool] = False
    headword, part_of_speech, rest = get_headword_part_of_speech_etc(tokens, do_print)
    clean_headword: Final[str] = headword.replace('__', '')
    clean_part_of_speech: Final[str] = part_of_speech.replace('_', '')
    clean_rest: str = ''
    for token in rest:
        if token.find('__') > -1:
            leading_text: str = '\n'
            if re.search('__[a-z]__', token) is not None:
                leading_text += ' '
            clean_rest += leading_text + CYAN + BOLD + token.replace('__', '') + END_C + ' '
        else:
            num_underscores: int = len(re.findall('_', token))
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
        number: int = tag_to_number(tag)
        number_str_xt: str = MAGENTA + '[' + str(number) + ']' + END_C
        clean_rest = clean_rest.replace(tag, number_str_xt)
    clean_rest = clean_rest.replace(':m:', MAGENTA + '(+)' + END_C)

    return CYAN + BOLD + clean_headword + ' ' \
        + END_C + CYAN + ITALIC + clean_part_of_speech + END_C + ' ' + clean_rest


def check(arg, do_check_parts_of_speech: bool) -> None:
    home_directory: Final[str] = os.path.expanduser("~").replace("\\", "/")
    file_path: Final[str] = home_directory + '/hats/fpcx-GitHub/AmE-dictionary/data/' + arg + ".md"
    file_basename: Final[str] = os.path.basename(file_path)
    end_of_message: Final[str] = BOLD + CYAN + file_basename + END_C + OK_BLUE + ' with do_check_parts_of_speech = ' + str(do_check_parts_of_speech)
    print('🔵 ' + OK_BLUE + "Checking " + end_of_message, flush=False)
    checker: Final = Checker(file_path)
    succeeded_a: Final[bool] = checker.check_entries(do_check_parts_of_speech)
    succeeded_b: Final[bool] = checker.check_duplicated_headwords()
    succeeded_c: Final[bool] = checker.check_undef_high_freq_keywords()
    succeeded: Final[bool] = succeeded_a and succeeded_b and succeeded_c
    overwrite_previous_line('✅ ' + OK_GREEN + 'Checked ' + end_of_message) if succeeded else None


def usage_and_abort(prog_name: str, valid_arguments: list[str]) -> None:
    print(BLUE + "Usage: " + prog_name + " <arguments> # with <arguments> being one or more of "
          + str(valid_arguments) + END_C)
    sys.exit(1)


def main(prog_name: str, argv: list[str]) -> None:
    num_arguments: Final[int] = len(argv)
    spy: Final[bool] = False
    if spy:
        print(OK_CYAN + 'ℹ️ #arguments: ' + str(num_arguments) + ' ' + str(argv) + END_C)
    valid_arguments: Final[list[str]] = [
        "abbreviations+", "dictionary", "Ellroy's-lingo", "idioms", "interjections", "todo-idioms", "todo-main",
        "top-dictionary", "top-idioms", "wip", "_wip"]
    if num_arguments > len(valid_arguments):
        print(RED + "Too many arguments. Aborting..." + END_C)
        usage_and_abort(prog_name, valid_arguments)
    for arg in argv:
        if arg not in valid_arguments:
            print(RED + prog_name + ": Argument `" + arg + "` is not valid." + END_C)
            usage_and_abort(prog_name, valid_arguments)

    if num_arguments == 0:
        argv = valid_arguments
        print('🔵 ' + OK_BLUE + prog_name + ': Argument list after adding default arguments: ' + str(argv) + END_C)

    for arg in argv:
        do_check_parts_of_speech: bool = (
            arg != "abbreviations+" and arg != 'Ellroy\'s-lingo' and arg != 'idioms'
            and arg != 'interjections' and arg != 'todo-idioms' and arg != 'top-idioms'
            and arg != 'wip' and arg != "_wip")
        check(arg, do_check_parts_of_speech)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
