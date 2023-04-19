import pygame
import test_checker
import test_statistics
import test_drawer
import test_statistics_drawer
from state import State
from colors import Colors


class UI:
    def __init__(self, width: int, height: int,
                 test_checker: test_checker.TestChecker,
                 test_statistics: test_statistics.TestStatistics) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((width, height))
        self.__test_drawer = test_drawer.TestDrawer(
            self.__screen, test_checker)
        self.__test_statistics_drawer = test_statistics_drawer.TestStatisticsDrawer(
            self.__screen, test_statistics)

        self.__running = True

    def is_running(self) -> bool:
        return self.__running

    def run(self) -> State:
        self.__screen.fill(Colors.BackGround)
        self.__draw()
        pygame.display.flip()
        return self.__check_clicks()

    def set_mode(self, mode: State):
        match mode:
            case State.Testing:
                self.__current_drawers = [self.__test_drawer]
            case State.Statistics:
                self.__current_drawers = [self.__test_statistics_drawer]
                self.__test_statistics_drawer.save()

    def __draw(self) -> None:
        for drawer in self.__current_drawers:
            drawer.draw()

    def __check_clicks(self) -> State:
        ret = State.NoChanges
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self.__end_running()
                return State.EndRunning
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    self.__end_running()
                    return State.EndRunning
                elif event.key == pygame.locals.K_TAB:
                    return State.GeneratingTest

            for drawer in self.__current_drawers:
                drawer_ret = drawer.check_clicks(event)
                if drawer_ret != State.NoChanges:
                    ret = drawer_ret
        return ret

    def __end_running(self) -> None:
        self.__running = False
