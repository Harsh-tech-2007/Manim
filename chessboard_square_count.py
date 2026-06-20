from manim import *
import numpy as np
from manim.utils.rate_functions import linear 


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color =BLACK


class ChessboardSquareCount(Scene):

    BG = "#0D0F12"
    WHITE = "#E8EAF0"
    SUBTLE = "#94A3B8"
    LIGHT_CELL = "#E7DDC8"
    DARK_CELL = "#29313D"
    GRID_LINE = "#0D0F12"
    GOLD = "#F4C542"
    BLUE = "#38BDF8"
    PINK = "#F472B6"

    FULL_BOARD_SIDE = 5.9
    DEMO_BOARD_SIDE = 5.0
    BOARD_CENTER = UP * 1.1

    def construct(self):
        self.camera.background_color = self.BG

        title = Text("How many squares", font_size=54, weight=BOLD, color=self.WHITE)
        title.to_edge(UP, buff=2.8)
        sub_tit = Text("are on a chessboard?", font_size=52, weight=BOLD, color=self.WHITE)
        sub_tit.next_to(title,DOWN, buff=0.25)
  
        chessboard = self.make_board(8, self.FULL_BOARD_SIDE, self.BOARD_CENTER)
        hook = Text("Finding the pattern.", font_size=50, color=WHITE)
        self.play(Write(title),Write(sub_tit),run_time=1),
        self.play(title.animate.to_edge(UP,buff=1),sub_tit.animate.to_edge(UP,buff=1.85), FadeIn(chessboard), run_time=0.75)
        self.wait(0.9)
        self.play(FadeOut(chessboard),FadeOut(title),FadeOut(sub_tit), run_time=0.45)
        self.play(FadeIn(hook), run_time=0.35)
        self.play(FadeOut(hook))

        for board_size in [1, 2, 3]:
            self.show_demo_board(board_size)
        
        self.show_final_answer() 

    def show_demo_board(self, board_size):
        board = self.make_board(board_size, self.DEMO_BOARD_SIDE, self.BOARD_CENTER)
        label = Text(f"{board_size}x{board_size} board", font_size=54, weight=BOLD, color=self.WHITE)
        label.to_edge(UP, buff=2.8)

        counter = Text("0", font_size=115, weight=BOLD,font="Georgia", color=self.WHITE)
        counter.move_to(DOWN * 3.5)
        counter_label = Text("squares", font_size=28, color=self.SUBTLE)
        counter_label.next_to(counter, DOWN, buff=0.3)

        self.play(FadeIn(label), FadeIn(board), FadeIn(counter), FadeIn(counter_label), run_time=0.5)

        running_total = 0
        active_marks = None
        active_note = None
        colors = [self.BLUE, self.GOLD, self.PINK]

        for square_size in range(1, board_size + 1):
            count = (board_size - square_size + 1) ** 2
            color = colors[square_size - 1]

            note = Text(
                f"{square_size}x{square_size}: {count}",
                font_size=34,
                weight=BOLD,
                color=color,
            )
            note.next_to(board, DOWN, buff=0.38)

            animations = [FadeIn(note)]
            if active_marks is not None:
                animations.insert(0, FadeOut(active_marks))
                animations.insert(1, FadeOut(active_note))

            self.play(*animations, run_time=0.25)

            active_marks = VGroup()
            for row in range(board_size - square_size + 1):
                for col in range(board_size - square_size + 1):
                    running_total += 1

                    box = self.highlight_square(board_size, square_size, row, col, color)
                    active_marks.add(box)
                    self.add(box)

                    next_counter = Text(str(running_total), font_size=112, weight=BOLD, color=self.WHITE)
                    next_counter.move_to(counter)

                    self.play(
                        Transform(counter, next_counter),
                        UpdateFromAlphaFunc(box, self.glow_outline),
                        run_time=self.count_time(square_size),
                        rate_func=linear,
                    )

            self.wait(0.25)
            active_note = note

        formula = MathTex(self.demo_formula(board_size), font_size=55, color=self.WHITE)
        formula.move_to(DOWN * 5.25)

        self.play(FadeOut(active_marks), FadeOut(active_note), FadeIn(formula), run_time=0.45)
        self.wait(0.9)
        self.play(
            FadeOut(board),
            FadeOut(label),
            FadeOut(counter),
            FadeOut(counter_label),
            FadeOut(formula),
            run_time=0.45,
        )

    def show_final_answer(self):
        board = self.make_board(8, self.FULL_BOARD_SIDE, self.BOARD_CENTER)

        heading = Text("Pattern", font_size=50, weight=BOLD, color=self.WHITE)
        heading.to_edge(UP, buff=2.3)

        pattern = VGroup(
            MathTex(r"1^2 = 1", font_size=44, color=self.WHITE),
            MathTex(r"1^2 + 2^2 = 5", font_size=44, color=self.WHITE),
            MathTex(r"1^2 + 2^2 + 3^2 = 14", font_size=44, color=self.WHITE),
            MathTex(r"1^2 + 2^2 + 3^2 + \cdots + n^2 = \sum_{k=1}^{n} k^2", font_size=42, color=self.WHITE),
        ).arrange(DOWN, buff=0.32)
        pattern.move_to(UP * 1.8)
        pattern.scale_to_fit_width(7.7)

        formula = MathTex(
            r"\sum_{k=1}^{8} k^2",
            font_size=62,
            color=self.WHITE,
        )
        formula.move_to(DOWN * 3.85)

        answer = MathTex(r"= 204", font_size=86, color=self.GOLD)
        answer.next_to(formula, RIGHT, buff=0.35)

        final_equation = VGroup(formula, answer)
        final_equation.move_to(DOWN * 4.08)

        caption = Text("total squares", font_size=30, color=self.SUBTLE)
        caption.next_to(final_equation, DOWN, buff=0.2)

        # self.play(FadeOut(title), run_time=0.35)
        self.play(Write(heading), run_time=0.45)
        for line in pattern:
            self.play(Write(line), run_time=0.45)
        self.wait(0.9)
        self.play(FadeOut(pattern), FadeOut(heading), run_time=0.45)
        self.play(FadeIn(board), run_time=0.6)
        self.play(Write(formula), run_time=0.65)
        self.play(FadeIn(answer), FadeIn(caption), run_time=0.55)
        self.wait(2.4)

    def make_board(self, n, side, center):
        cell = side / n
        cells = VGroup()

        for row in range(n):
            for col in range(n):
                fill = self.LIGHT_CELL if (row + col) % 2 == 0 else self.DARK_CELL
                square = Square(
                    side_length=cell,
                    fill_color=fill,
                    fill_opacity=1,
                    stroke_color=self.GRID_LINE,
                    stroke_width=1.0,
                )
                square.move_to(self.square_center(n, side, center, row, col, 1))
                cells.add(square)

        border = Square(side_length=side)
        border.move_to(center)
        border.set_fill(opacity=0)
        border.set_stroke(self.WHITE, width=2.4)
        return VGroup(cells, border)

    def square_center(self, n, side, center, row, col, square_size):
        cell = side / n
        left = center[0] - side / 2
        top = center[1] + side / 2
        x = left + (col + square_size / 2) * cell
        y = top - (row + square_size / 2) * cell
        return np.array([x, y, 0])

    def highlight_square(self, n, square_size, row, col, color):
        cell = self.DEMO_BOARD_SIDE / n
        square = Square(side_length=square_size * cell)
        square.move_to(self.square_center(n, self.DEMO_BOARD_SIDE, self.BOARD_CENTER, row, col, square_size))
        square.set_fill(color, opacity=0.0)
        square.set_stroke(color, width=0.0, opacity=0.0)
        return square

    def glow_outline(self, mob, alpha):
        if alpha < 0.45:
            t = alpha / 0.45
            mob.set_stroke(width=7.0 * t, opacity=0.95 * t)
        else:
            t = (alpha - 0.45) / 0.55
            mob.set_stroke(width=7.0 - 4.2 * t, opacity=0.95 - 0.2 * t)

    def count_time(self, square_size):
        return 0.2 if square_size == 1 else 0.28

    def demo_formula(self, board_size):
        terms = [f"{number}^2" for number in range(1, board_size + 1)]
        total = sum(number * number for number in range(1, board_size + 1))
        return " + ".join(terms) + f" = {total}"