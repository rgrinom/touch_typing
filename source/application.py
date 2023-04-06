# from logic import Logic
import logic
import ui

class Application:
  def __init__(self, width: int, height: int) -> None:
    self.__logic = logic.Logic()
    self.__ui = ui.UI(width, height, self.__logic)
    self.__logic.set_test_length(25)
    self.__logic.generate_test()
  
  def run(self) -> None:
    while True:
      if not self.__ui.run():
        break