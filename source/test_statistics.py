import time
import matplotlib.pyplot as plt

class TestStatistics:
  def __init__(self) -> None:
    pass

  def get_test_length(self) -> int:
    return self.__test_length

  def get_duration(self) -> int:
    return self.__duration
  
  def get_raw(self) -> list[float]:
    return self.__raw_by_moment
  
  def get_cpm(self) -> list[float]:
    return self.__cpm_by_moment
  
  def get_accuracy(self) -> list[float]:
    return self.__accuracy_by_moment

  def reset(self, test_length: int) -> None:
    self.__test_length = test_length
    self.__total_chars = 0
    self.__correct_chars = 0
    self.__raw_by_moment = []
    self.__cpm_by_moment = []
    self.__accuracy_by_moment = []
    self.__running = False
  
  def start_test(self) -> None:
    self.__start_time = time.time()
    self.__last_time = self.__start_time
    self.__running = True

  def end_test(self) -> None:
    self.__add_moment()
    self.__duration = len(self.__raw_by_moment)
    self.__running = False
  
  def upd(self) -> None:
    if not self.__running:
      return
    if time.time() - self.__last_time < 1.0:
      return
    self.__add_moment()
    self.__last_time = time.time()

  def is_running(self) -> bool:
    return self.__running

  def __add_moment(self) -> None:
    time_past = time.time() - self.__start_time
    self.__raw_by_moment.append(self.__total_chars / time_past * 60)
    self.__cpm_by_moment.append(self.__correct_chars / time_past * 60)
    self.__accuracy_by_moment.append(
      self.__correct_chars / self.__total_chars if self.__total_chars != 0 else 0)
  
  def add_char(self, is_correct: bool) -> None:
    self.__total_chars += 1
    if is_correct:
      self.__correct_chars += 1

  def pop_char(self, is_correct: bool) -> None:
    self.__total_chars -= 1
    if is_correct:
      self.__correct_chars -= 1