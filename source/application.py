import test_checker
import test_statistics
import ui

class Application:
  def __init__(self, width: int, height: int) -> None:
    self.__test_statistics = test_statistics.TestStatistics()
    self.__test_checker = test_checker.TestChecker(self.__test_statistics)
    self.__ui = ui.UI(width, height, self.__test_checker)

    self.__test_checker.set_test_length(25)
  
  def run(self) -> None:
    while True:
      if not self.__test_checker.is_running():
        self.__test_checker.generate_test()
      self.__test_statistics.upd()
      self.__ui.run()
      if not self.__ui.is_running():
        break