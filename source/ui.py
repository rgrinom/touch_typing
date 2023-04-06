import pygame
import test_drawer
import test_checker

class UI:
  def __init__(self, width: int, height: int, test_checker: test_checker.TestChecker) -> None:
    pygame.init()
    self.__screen = pygame.display.set_mode((width, height))
    self.__test_checker = test_checker
    self.__test_drawer = test_drawer.TestDrawer(self.__screen, self.__test_checker)

    self.__current_drawers = [self.__test_drawer]
    self.__running = True

  def is_running(self) -> bool:
    return self.__running

  def run(self) -> None:
    self.__draw()
    self.__check_clicks()

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