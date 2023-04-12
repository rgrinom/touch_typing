import pygame
import pygame.freetype
import pygame.locals
import test_checker
from colors import Colors
from state import State
import Globals


class TestDrawer:
    __available_inputs = ("space", "backspace")

    def __init__(self, screen: pygame.Surface, test_checker: test_checker.TestChecker) -> None:
        self.__screen = screen
        self.__test_checker = test_checker
        self.__font = pygame.freetype.Font(None, Globals.TEST_TEXT_SIZE)
        self.__font.origin = True

    def draw(self) -> None:
        if not self.__test_checker.is_running():
            return

        self.__get_lines()
        if self.__cur_editing_line > 0:
            self.__draw_line(-1)
        self.__draw_line(0)
        if self.__cur_editing_line < len(self.__lines) - 1:
            self.__draw_line(1)

        pygame.draw.rect(
            self.__screen,
            Colors.ForeGround,
            pygame.Rect(self.__coursor_x, self.__coursor_y, Globals.COURSOR_WIDTH, self.__coursor_h))

    def __get_lines(self) -> None:
        test = self.__test_checker.get_test()

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
            add_char_state.append(test_checker.CharState.Correct)
            if self.__font.get_rect(s + add).w > self.__screen.get_size()[0] * Globals.TEST_TEXT_AREA_WIDTH_K:
                self.__lines.append(s)
                self.__char_state.append(cur_line_char_state)
                s = ""
                cur_line_char_state = []
            if ind == self.__test_checker.get_cur_word():
                self.__coursor_ind = len(s) + len(test[ind].get_actual())
                self.__cur_editing_line = len(self.__lines)
            s += add
            cur_line_char_state.extend(add_char_state)
        self.__lines.append(s)
        self.__char_state.append(cur_line_char_state)

    def __draw_line(self, shift: int) -> None:
        line = self.__lines[self.__cur_editing_line + shift]
        line_char_state = self.__char_state[self.__cur_editing_line + shift]
        text_surf_rect = self.__font.get_rect(line)
        baseline = text_surf_rect.y
        text_surf = pygame.Surface(text_surf_rect.size)
        text_surf_rect.center = self.__screen.get_rect().center
        text_surf_rect.centery += Globals.TEST_GAP_BETWEEN_LINES_K * shift * text_surf_rect.h
        metrics = self.__font.get_metrics(line)
        text_surf.fill(Colors.BackGround)
        x = 0
        for ind in range(len(line)):
            match line_char_state[ind]:
                case test_checker.CharState.Correct:
                    color = Colors.CorrectChar
                case test_checker.CharState.Incorrect:
                    color = Colors.IncorrectChar
                case test_checker.CharState.Added:
                    color = Colors.AddedChar
                case test_checker.CharState.NotTouched:
                    color = Colors.NotTouchedChar
            self.__font.render_to(text_surf, (x, baseline), line[ind], color)
            if ind == self.__coursor_ind and shift == 0:
                self.__coursor_x = (self.__screen.get_size()[
                                    0] - text_surf_rect.w) * 0.5 + x
                self.__coursor_y = (self.__screen.get_size()[
                                    1] - text_surf_rect.h) * 0.5
                self.__coursor_h = text_surf_rect.h

            x += metrics[ind][4]
        self.__screen.blit(text_surf, text_surf_rect)

    def check_clicks(self, event: pygame.event) -> State:
        if event.type != pygame.locals.KEYDOWN:
            return State.NoChanges
        if not self.__test_checker.is_running():
            return State.NoChanges
        key = pygame.key.name(event.key)
        is_char = (len(key) == 1 and (key.isalpha() or key.isdigit()))
        if is_char or key in self.__available_inputs:
            self.__test_checker.check_user_input(key)
        return State.NoChanges
