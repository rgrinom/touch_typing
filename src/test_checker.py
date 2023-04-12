import random
from enum import Enum
from copy import deepcopy
import test_statistics
import Globals


class CharState(Enum):
    NotTouched = 0
    Correct = 1
    Incorrect = 2
    Added = 3


class Word:
    def __init__(self, goal: str) -> None:
        self.__goal = goal
        self.__actual = ""
        self.__char_state = [CharState.NotTouched] * len(goal)

    def get_goal(self):
        return deepcopy(self.__goal)

    def get_actual(self):
        return deepcopy(self.__actual)

    def get_char_state(self):
        return deepcopy(self.__char_state)

    def add_char(self, char: str) -> None:
        self.__actual += char
        if len(self.__actual) > len(self.__goal):
            self.__char_state.append(CharState.Added)
            return
        if self.__actual[-1] == self.__goal[len(self.__actual) - 1]:
            self.__char_state[len(self.__actual) - 1] = CharState.Correct
        else:
            self.__char_state[len(self.__actual) - 1] = CharState.Incorrect

    def pop_char(self) -> bool:
        if len(self.__actual) == 0:
            return False
        if len(self.__actual) > len(self.__goal):
            self.__char_state.pop()
        else:
            self.__char_state[len(self.__actual) - 1] = CharState.NotTouched
        self.__actual = self.__actual[:-1]
        return True

    def is_actual_correct(self) -> bool:
        return self.__actual == self.__goal

    def is_last_char_correct(self) -> bool:
        if len(self.__actual) == 0:
            return False
        if len(self.__actual) > len(self.__goal):
            return False
        return self.__actual[-1] == self.__goal[len(self.__actual) - 1]

    def empty(self) -> bool:
        return len(self.__actual) == 0


class TestChecker:
    def __init__(self, statistics: test_statistics.TestStatistics) -> None:
        with open(Globals.WORDS_PATH, 'r') as fin:
            self.__words = fin.readlines()
            for i in range(len(self.__words)):
                self.__words[i] = self.__words[i].strip()
        self.__statistics = statistics
        self.__running = False

    def set_test_length(self, test_length: int) -> None:
        self.__test_length = test_length

    def get_test(self) -> list[Word]:
        return deepcopy(self.__test)

    def get_cur_word(self) -> int:
        return self.__cur_word

    def is_running(self) -> bool:
        return self.__running

    def generate_test(self) -> None:
        self.__test = []
        for _ in range(self.__test_length):
            self.__test.append(Word(random.choice(self.__words)))
        self.__cur_word = 0
        self.__statistics.reset(self.__test_length)
        self.__running = True

    def check_user_input(self, char: str) -> None:
        if char == "space":
            if not self.__test[self.__cur_word].empty():
                self.__cur_word += 1
            if self.__cur_word >= self.__test_length:
                self.__end_test()
        elif char == "backspace":
            is_last_char_correct = self.__test[self.__cur_word].is_last_char_correct(
            )
            if self.__test[self.__cur_word].pop_char():
                self.__statistics.pop_char(is_last_char_correct)
                return
            if (self.__cur_word > 0 and
                    not self.__test[self.__cur_word - 1].is_actual_correct()):
                self.__cur_word -= 1
        else:
            self.__test[self.__cur_word].add_char(char)
            if not self.__statistics.is_running():
                self.__statistics.start_test()
            self.__statistics.add_char(
                self.__test[self.__cur_word].is_last_char_correct())
            if self.__test[-1].is_actual_correct():
                self.__end_test()

    def __end_test(self) -> None:
        self.__statistics.end_test()
        self.__running = False
