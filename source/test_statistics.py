import time

class TestStatistics:
  def __init__(self) -> None:
    self.reset()

  def reset(self) -> None:
    self.__total_words = 0
    self.__correct_words = 0
    self.__raw_by_moment = []
    self.__wpm_by_moment = []
    self.__accuracy_by_moment = []
    self.__running = False
  
  def start_test(self) -> None:
    self.__start_time = time.time()
    self.__last_time = self.__start_time
    self.__running = True

  def end_test(self) -> None:
    self.__add_moment()
    self.__running = False

    for i in range(len(self.__raw_by_moment)):
      print(self.__raw_by_moment[i], self.__wpm_by_moment[i], self.__accuracy_by_moment[i], sep='\t')
  
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
    self.__raw_by_moment.append(self.__total_words / time_past * 60)
    self.__wpm_by_moment.append(self.__correct_words / time_past * 60)
    self.__accuracy_by_moment.append(
      self.__correct_words / self.__total_words if self.__total_words != 0 else 0)
  
  def add_word(self, is_correct: bool) -> None:
    self.__total_words += 1
    if is_correct:
      self.__correct_words += 1

  def pop_word(self, is_correct: bool) -> None:
    self.__total_words -= 1
    if is_correct:
      self.__correct_words -= 1