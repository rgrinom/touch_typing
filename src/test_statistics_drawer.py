import pygame
import test_statistics
import matplotlib.pyplot as plt
from colors import Colors
from state import State
import globals


class TestStatisticsDrawer:
    def __init__(self, screen: pygame.Surface, statistics: test_statistics.TestStatistics) -> None:
        self.__screen = screen
        self.__statistics = statistics
        self.__font = pygame.freetype.Font(None, globals.STATISTICS_TEXT_SIZE)
        self.__font.origin = True

        self.__working_area_width = self.__screen.get_size(
        )[0] * globals.STATISTICS_WORKING_AREA_WIDTH_K
        self.__plot_height = self.__screen.get_size(
        )[1] * globals.STATISTICS_PLOT_HEIGHT_K
        self.__left_margin = (self.__screen.get_size()[
                              0] - self.__working_area_width) * 0.5
        self.__plot_top_margin = self.__screen.get_size(
        )[1] * globals.STATISTICS_PLOT_TOP_MARGIN_K

        self.__results_titles_top_margin = self.__plot_top_margin + self.__plot_height + \
            self.__screen.get_size()[1] * \
            globals.STATISTICS_RESULTS_TITLES_TOP_GAP_K
        self.__results_top_margin = self.__results_titles_top_margin + \
            self.__screen.get_size()[1] * globals.STATISTICS_RESULTS_TOP_GAP_K

        self.__restart_left_margin = self.__screen.get_size()[0] * 0.5
        self.__restart_top_margin = self.__results_top_margin + \
            self.__screen.get_size()[1] * globals.STATISTICS_RESTART_TOP_GAP_K

    def save(self) -> None:
        my_dpi = 96
        plt.figure(figsize=(self.__working_area_width / my_dpi,
                            self.__plot_height / my_dpi),
                   dpi=my_dpi)
        plt.plot([i + 1 for i in range(self.__statistics.get_duration())],
                 self.__statistics.get_cpm(), color=Colors.DataNormalized)
        plt.rcParams['savefig.facecolor'] = Colors.BackGroundNormalized
        ax = plt.gca()
        ax.set_facecolor(Colors.PlotBackGroundNormalized)

        ax.set_ylim(ymin=0)
        ax.set_ylim(ymax=max(self.__statistics.get_cpm()) * 1.5)

        ax.spines['bottom'].set_color(Colors.BackGroundNormalized)
        ax.spines['top'].set_color(Colors.BackGroundNormalized)
        ax.spines['right'].set_color(Colors.BackGroundNormalized)
        ax.spines['left'].set_color(Colors.BackGroundNormalized)

        ax.set_ylabel("Speed (cpm)", color=Colors.HeadersNormalized)
        ax.set_xlabel("Time (s)", color=Colors.HeadersNormalized)
        ax.tick_params(labelcolor=Colors.HeadersNormalized)
        plt.savefig(globals.STATISTICS_PATH, dpi=my_dpi)

    def draw(self) -> None:
        plot_surf = pygame.image.load(globals.STATISTICS_PATH)
        plot_rect = plot_surf.get_rect(
            topleft=(self.__left_margin, self.__plot_top_margin))
        self.__screen.blit(plot_surf, plot_rect)

        self.__draw_text("cpm", self.__left_margin + self.__working_area_width *
                         0.5 / 5, self.__results_titles_top_margin, Colors.NotTouchedChar)
        self.__draw_text("acc", self.__left_margin + self.__working_area_width *
                         1.5 / 5, self.__results_titles_top_margin, Colors.NotTouchedChar)
        self.__draw_text("real acc", self.__left_margin + self.__working_area_width *
                         2.5 / 5, self.__results_titles_top_margin, Colors.NotTouchedChar)
        self.__draw_text("words", self.__left_margin + self.__working_area_width *
                         3.5 / 5, self.__results_titles_top_margin, Colors.NotTouchedChar)
        self.__draw_text("time", self.__left_margin + self.__working_area_width *
                         4.5 / 5, self.__results_titles_top_margin, Colors.NotTouchedChar)

        self.__draw_text(str(int(self.__statistics.get_cpm(
        )[-1])), self.__left_margin + self.__working_area_width * 0.5 / 5, self.__results_top_margin, Colors.ForeGround)
        self.__draw_text(str(int(self.__statistics.get_accuracy(
        ) * 100)) + '%', self.__left_margin + self.__working_area_width * 1.5 / 5, self.__results_top_margin, Colors.ForeGround)
        self.__draw_text(str(int(self.__statistics.get_real_accuracy(
        ) * 100)) + '%', self.__left_margin + self.__working_area_width * 2.5 / 5, self.__results_top_margin, Colors.ForeGround)
        self.__draw_text(str(self.__statistics.get_test_length()), self.__left_margin +
                         self.__working_area_width * 3.5 / 5, self.__results_top_margin, Colors.ForeGround)
        self.__draw_text(str(self.__statistics.get_duration()) + 's', self.__left_margin +
                         self.__working_area_width * 4.5 / 5, self.__results_top_margin, Colors.ForeGround)

        self.__draw_text("To try again press 'Tab'", self.__restart_left_margin,
                         self.__restart_top_margin, Colors.NotTouchedChar)

    def __draw_text(self, line: str, x_pos: int, y_pos: int, color: Colors):
        text_surf_rect = self.__font.get_rect('l' + line + 'p')
        baseline = text_surf_rect.y
        text_surf = pygame.Surface(text_surf_rect.size)
        text_surf_rect.center = (x_pos, y_pos)
        text_surf.fill(Colors.BackGround)
        x = self.__font.get_metrics('l' + line + 'p')[0][4]
        self.__font.render_to(text_surf, (x, baseline), line, color)
        self.__screen.blit(text_surf, text_surf_rect)

    def check_clicks(self, event: pygame.event) -> State:
        return State.NoChanges
