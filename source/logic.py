import random
from enum import Enum
from copy import deepcopy

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
  
  def is_actual_right(self) -> bool:
    return self.__actual == self.__goal
  
  def empty(self) -> bool:
    return len(self.__actual) == 0

class Logic:
  def __init__(self) -> None:
    with open("../content/words.txt", 'r') as fin:
      self.__words = fin.readlines()
      for i in range(len(self.__words)):
        self.__words[i] = self.__words[i].strip()
  
  def set_test_length(self, length: int) -> None:
    self.__length = length

  def get_test(self) -> list[Word]:
    return deepcopy(self.__test)
  
  def get_cur_word(self) -> int:
    return self.__cur_word

  def generate_test(self) -> None:
    self.__test = []
    for _ in range(self.__length):
      self.__test.append(Word(random.choice(self.__words)))
    self.__cur_word = 0
    self.__wpm_by_moment = []
    self.__accuracy_by_moment = []
  
  def check_user_input(self, char: str) -> None:
    if char == 'space':
      if not self.__test[self.__cur_word].empty():
        self.__cur_word += 1
    elif char == 'backspace':
      if self.__test[self.__cur_word].pop_char():
        return
      if (self.__cur_word > 0 and
          not self.__test[self.__cur_word - 1].is_actual_right()):
        self.__cur_word -= 1
    else:
      self.__test[self.__cur_word].add_char(char)