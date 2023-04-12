import test_checker
import test_statistics
import ui
from state import State


class Application:
    def __init__(self, width: int, height: int, test_length: int) -> None:
        self.__test_statistics = test_statistics.TestStatistics()
        self.__test_checker = test_checker.TestChecker(self.__test_statistics)
        self.__ui = ui.UI(width, height, self.__test_checker,
                          self.__test_statistics)

        self.__test_checker.set_test_length(test_length)
        self.__state = State.GeneratingTest

    def run(self) -> None:
        while self.__state != State.EndRunning:
            match self.__state:
                case State.GeneratingTest:
                    self.__test_checker.generate_test()
                    self.__ui.set_mode(State.Testing)
                    self.__state = State.Testing
                case State.Testing:
                    if not self.__test_checker.is_running():
                        self.__ui.set_mode(State.Statistics)
                        self.__state = State.Statistics
                        continue
                    self.__test_statistics.upd()

            ui_ret = self.__ui.run()
            if ui_ret != State.NoChanges:
                self.__state = ui_ret
