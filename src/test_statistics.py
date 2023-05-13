import time
import globals


class TestStatistics:
    def __init__(self) -> None:
        pass

    def get_test_length(self) -> int:
        return self.__test_length

    def get_duration(self) -> int:
        return self.__duration

    def get_cpm(self) -> list[float]:
        return self.__cpm_by_moment

    def get_accuracy(self) -> float:
        return 1 - self.__left_mistakes / self.__chars_in_test

    def get_real_accuracy(self) -> float:
        return 1 - self.__total_mistakes / self.__total_chars

    def reset(self, test_length: int) -> None:
        self.__test_length = test_length
        self.__total_chars = 0
        self.__chars_in_test = 0
        self.__total_mistakes = 0
        self.__left_mistakes = 0
        self.__cpm_by_moment = []
        self.__running = False

    def start_test(self) -> None:
        self.__start_time = time.time()
        self.__last_time = self.__start_time
        self.__running = True

    def end_test(self) -> None:
        self.__add_moment()
        self.__duration = len(self.__cpm_by_moment)
        self.__running = False
        with open(globals.HISTORY_PATH, 'a') as fout:
            fout.write(str(self.__cpm_by_moment[-1]) + ' ')
            fout.write(str(self.get_real_accuracy()) + '\n')

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
        self.__cpm_by_moment.append(
            (self.__total_chars - self.__left_mistakes) / time_past * 60)

    def add_char(self, is_correct: bool, cnt: int = 1) -> None:
        self.__total_chars += cnt
        self.__chars_in_test += cnt
        if not is_correct:
            self.__total_mistakes += cnt
            self.__left_mistakes += cnt

    def pop_char(self, is_correct: bool, cnt: int = 1) -> None:
        self.__chars_in_test -= cnt
        if not is_correct:
            self.__left_mistakes -= cnt
