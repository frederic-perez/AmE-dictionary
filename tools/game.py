"""
Play the game by executing:
$ python -u game.py # within a `git bash` shell
                    # Credits to https://stackoverflow.com/questions/34668972
or
$ python game.py # within a CMD shell
"""

import os.path
import random  # WIP
import re

from checker import *
from typing import Final


class Game(object):
    """The class Game encapsulates all functionalities to play games with the dictionary"""

    filename: Final[str]
    list: list[list]

    def __init__(self, filename) -> None:
        self.filename = filename
        self.list = [[], [], [], [], [], [], [], [], []]

    def gather_high_frequency_headwords(self) -> None:
        """Searching for the entries of the dictionary with higher frequency"""
        input_file: Final = open(self.filename, 'r')

        for line in input_file:
            entry = line.replace('\n', '')
            if entry_has_tag_of_any_number(entry, 2, 9):
                num_additions = 0
                for i in range(10, 1, -1):
                    if entry_has_tag_of_number(entry, i):
                        self.list[get_index(i)] += [entry]
                        if i == 10:
                            break  # to avoid adding to lists :nine::m: and :nine:
                        num_additions += 1
                        if num_additions > 1:
                            print(FAIL + entry + ' <<< Too many numeric tags' + END_C)

        input_file.close()
        print(OK_CYAN + '\nSummary of high frequency headwords')
        print('-----------------------------------')
        for i in range(10, 1, -1):
            print('Entries with ' + str(get_tag(i)) + ' = ' + str(len(self.list[get_index(i)])))
        print(END_C)

    def print_nine_m(self) -> None:
        """Method aimed at learning definitions"""
        print('Entries with :nine::m: are:')
        index_9m: Final = get_index(10)
        regex: Final = re.compile(r"<sup>\d</sup>")
        do_print: Final = False
        for entry in self.list[index_9m]:
            tokens = entry.split()
            headword, _, _ = get_headword_part_of_speech_etc(tokens, do_print)
            headword_for_wordcloud = headword.replace('__', '')
            headword_for_wordcloud = regex.sub('', headword_for_wordcloud)
            headword_for_wordcloud = headword_for_wordcloud.replace(' ', '~')
            print(headword_for_wordcloud,)
        print('\n')

    def play(self) -> None:
        """Method aimed at learning definitions"""
        index_9m: Final = get_index(10)
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
            print(FAIL + 'Q' + END_C + FAIL + str(question) + ': ' + BOLD + clean_headword + ' ' + END_C + FAIL + ITALIC
                  + clean_part_of_speech + END_C)
            # print OK_CYAN + '  ' + entry + END_C
            print(format_to_print(entry))
            question += 1
            user_response = input(OK_BLUE + 'Quit (q)? ' + END_C)
            do_quit = user_response == 'q'


if __name__ == '__main__':
    DICTIONARY: Final = '../data/dictionary.md'
    game: Final = Game(DICTIONARY)
    game.gather_high_frequency_headwords()
    game.print_nine_m()
    game.play()
    print("Bye!")
