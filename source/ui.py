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
    self.__test_drawer = test_drawer.TestDrawer(self.__screen, test_checker)
    self.__test_statistics_drawer = test_statistics_drawer.TestStatisticsDrawer(self.__screen, test_statistics)

    self.set_mode(State.Test)
    self.__running = True

  def is_running(self) -> bool:
    return self.__running

  def run(self) -> None:
    self.__screen.fill(Colors.BackGround)
    self.__draw()
    pygame.display.flip()
    self.__check_clicks()

  def set_mode(self, mode: State):
    match mode:
      case State.Test:
        self.__current_drawers = [self.__test_drawer]
      case State.Statistics:
        self.__current_drawers = [self.__test_statistics_drawer]
        self.__test_statistics_drawer.save()
    
  def __draw(self) -> None:
    for drawer in self.__current_drawers:
      drawer.draw()

  def __check_clicks(self) -> None:
    for event in pygame.event.get():
      if event.type == pygame.locals.QUIT:
        self.__end_running()
        return
      if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
        self.__end_running()
        return False

      for drawer in self.__current_drawers:
        drawer.check_clicks(event)
    return True
  
  def __end_running(self) -> None:
    self.__running = False