import test_checker
import test_statistics
import ui
from state import State

class Application:
  def __init__(self, width: int, height: int) -> None:
    self.__test_statistics = test_statistics.TestStatistics()
    self.__test_checker = test_checker.TestChecker(self.__test_statistics)
    self.__ui = ui.UI(width, height, self.__test_checker, self.__test_statistics)

    self.__test_checker.set_test_length(25)
    self.__state = State.Test
    self.__test_checker.generate_test()
  
  def run(self) -> None:
    while True:
      match self.__state:
        case State.Test:
          if not self.__test_checker.is_running():
            self.__state = State.Statistics
            self.__ui.set_mode(State.Statistics)
          self.__test_statistics.upd()
      self.__ui.run()
      if not self.__ui.is_running():
        break