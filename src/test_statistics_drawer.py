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
        with open(globals.HISTORY_PATH, 'r') as fin:
            cpm = []
            acc = []
            for line in fin.readlines():
                cur_cpm, cur_acc = map(float, line.split())
                cpm.append(cur_cpm)
                acc.append(cur_acc * 100)

        my_dpi = 96
        plt.rcParams['savefig.facecolor'] = Colors.BackGroundNormalized

        fig, ax1 = plt.subplots()

        ax1.figure.set_figwidth(self.__working_area_width / my_dpi)
        ax1.figure.set_figheight(self.__plot_height / my_dpi)
        ax1.set_facecolor(Colors.PlotBackGroundNormalized)
        ax1.spines['bottom'].set_color(Colors.BackGroundNormalized)
        ax1.spines['top'].set_color(Colors.BackGroundNormalized)
        ax1.spines['right'].set_color(Colors.BackGroundNormalized)
        ax1.spines['left'].set_color(Colors.BackGroundNormalized)
        ax1.set_xlabel("Tests taken", color=Colors.HeadersNormalized)
        ax1.set_ylabel("Speed (cpm)", color=Colors.DataNormalized)
        ax1.set_ylim(ymin=0)
        ax1.set_ylim(ymax=max(cpm) * 1.5)
        ax1.plot([i + 1 for i in range(len(cpm))], cpm,
                 color=Colors.DataNormalized, marker='o')
        ax1.tick_params(labelcolor=Colors.HeadersNormalized)

        ax2 = ax1.twinx()
        ax2.spines['bottom'].set_color(Colors.BackGroundNormalized)
        ax2.spines['top'].set_color(Colors.BackGroundNormalized)
        ax2.spines['right'].set_color(Colors.BackGroundNormalized)
        ax2.spines['left'].set_color(Colors.BackGroundNormalized)
        ax2.set_ylabel("Accuracy (%)", color=Colors.AccuracyNormalized)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=110)
        ax2.plot([i + 1 for i in range(len(acc))], acc,
                 color=Colors.AccuracyNormalized, marker='o')
        ax2.tick_params(labelcolor=Colors.HeadersNormalized)
        fig.tight_layout()
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
