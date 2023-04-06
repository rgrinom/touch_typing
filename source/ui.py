import pygame
import pygame.freetype
import pygame.locals
import logic

class UI:
  def __init__(self, width: int, height: int, logic: logic.Logic) -> None:
    pygame.init()
    self.__screen = pygame.display.set_mode((width, height))
    self.__logic = logic
    self.__font = pygame.freetype.Font(None, 50)
    self.__font.origin = True
    self.__line_beginnings = [0]
    self.__bgcolor = 'darkgrey'

  def run(self) -> bool:
    self.__draw()
    return self.__check_clicks()

  def __draw(self) -> None:
    self.__get_lines()
    self.__screen.fill(self.__bgcolor)
    if self.__cur_editing_line > 0:
      self.__draw_line(-1)
    self.__draw_line(0)
    if self.__cur_editing_line < len(self.__lines) - 1:
      self.__draw_line(1)
    pygame.display.flip()
    

  def __get_lines(self) -> None:
    test = self.__logic.get_test()

    self.__lines = []
    self.__char_state = []
    s = ""
    cur_line_char_state = []
    for ind in range(len(test)):
      add = test[ind].get_goal()
      add_char_state = test[ind].get_char_state()
      if len(test[ind].get_actual()) > len(test[ind].get_goal()):
        add += test[ind].get_actual()[len(test[ind].get_goal()):]
      add += ' '
      add_char_state.append(logic.CharState.Correct)
      if self.__font.get_rect(s + add).w > self.__screen.get_size()[0] * 0.8:
        self.__lines.append(s)
        self.__char_state.append(cur_line_char_state)
        s = ""
        cur_line_char_state = []
      s += add
      cur_line_char_state.extend(add_char_state)
      if ind == self.__logic.get_cur_word():
        self.__cur_editing_line = len(self.__lines)
    self.__lines.append(s)
    self.__char_state.append(cur_line_char_state)
  
  def __draw_line(self, shift: int) -> None:
    line = self.__lines[self.__cur_editing_line + shift]
    line_char_state = self.__char_state[self.__cur_editing_line + shift]
    text_surf_rect = self.__font.get_rect(line)
    baseline = text_surf_rect.y
    text_surf = pygame.Surface(text_surf_rect.size)
    text_surf_rect.center = self.__screen.get_rect().center
    text_surf_rect.centery += 1.5 * shift * text_surf_rect.h
    metrics = self.__font.get_metrics(line)
    text_surf.fill(self.__bgcolor)
    x = 0
    for ind in range(len(line)):
      match line_char_state[ind]:
        case logic.CharState.Correct:
          color = 'white'
        case logic.CharState.Incorrect:
          color = 'red'
        case logic.CharState.Added:
          color = 'red'
        case logic.CharState.NotTouched:
          color = 'lightgrey'
      self.__font.render_to(text_surf, (x, baseline), line[ind], color)
      x += metrics[ind][4]
    self.__screen.blit(text_surf, text_surf_rect)

  def __check_clicks(self) -> bool:
    for event in pygame.event.get():
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          return False
        else:
          self.__logic.check_user_input(pygame.key.name(event.key))
      elif event.type == pygame.locals.QUIT:
        return False
    return True