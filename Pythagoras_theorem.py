import numpy as np
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK

CHALK = "#ffffff"
YELLOW = "#ededed"
GREEN = "#4cde73"
BLUE = "#4288de"
PINK = "#f6f312"
Red = "#e43950"
TRIANGLE_FILL_OPACITY = 0.5
TRIANGLE_STROKE_WIDTH = 5
TRIANGLE_GLOW_WIDTH = 12
TRIANGLE_GLOW_OPACITY = 0.25


class Video(MovingCameraScene):
    def chalk_text(self, text, size=42, color=CHALK):
        return Text(text, font_size=size, color=color)

    def chalk_math(self, tex, size=42, color=CHALK):
        mob = MathTex(tex, font_size=size, color=color)
        mob.set_stroke(color, width=0.4, opacity=0.55)
        return mob

    def glow(self, mob, color=YELLOW, width=10):
        return mob.copy().set_color(color).set_stroke(color, width=width, opacity=0.35)

    def style_triangle(
        self,
        tri,
        color,
        fill_opacity=TRIANGLE_FILL_OPACITY,
        glow_width=TRIANGLE_GLOW_WIDTH,
        glow_opacity=TRIANGLE_GLOW_OPACITY,
    ):
        tri.set_fill(color, opacity=fill_opacity)
        tri.set_stroke(color, width=glow_width, opacity=glow_opacity, background=True)
        tri.set_stroke(color, width=TRIANGLE_STROKE_WIDTH, opacity=1)
        return tri

    def triangle(self, a_len, b_len, color):
        tri = Polygon(ORIGIN, RIGHT * a_len, UP * b_len)
        return self.style_triangle(tri, color)

    def final_triangle(self, a_len, b_len, corner, angle, color):
        tri = self.triangle(a_len, b_len, color)
        tri.rotate(angle, about_point=ORIGIN)
        tri.shift(corner)
        return tri

    def side_label(self, tex, p1, p2, offset, size=38, color=CHALK):
        return self.chalk_math(tex, size, color).move_to((p1 + p2) / 2 + offset)

    def construct(self):
        a_len = 3.3
        b_len = 2.25
        side_sum = a_len + b_len
        half_sum = side_sum / 2
        square_center = UP * 1.28

        heading_h = MathTex(r"\mathbb{W}", font_size=108, color=WHITE)
        heading_h.stretch(1.28, dim=1)
        heading_h.set_stroke(width=1.6)
        
        heading_text = self.chalk_text("hy", 108, CHALK)
        question_1 = VGroup(heading_h, heading_text).arrange(RIGHT, buff=0, aligned_edge=UP)
        question_1.set_color_by_gradient("#ec3078", "#f1324b")        

        question_2 = self.chalk_math(r"a^2+b^2=c^2", 100)   
        question = VGroup(question_1, question_2).arrange(DOWN, buff=0.65)
        question.move_to(UP * 1.35)
        
        self.play(Write(question_1), run_time=0.8)
        self.play(Write(question_2), run_time=0.8)
        self.wait(0.25)
        self.play(question.animate.scale(0.72).to_edge(UP, buff=1.65), run_time=0.8)
 

        start_triangle = self.triangle(a_len, b_len, Red).move_to(DOWN * 0.15)
        v0, v1, v2 = start_triangle.get_vertices()
        label_a = self.side_label("a", v0, v1, DOWN * 0.34, 44, WHITE)
        label_b = self.side_label("b", v0, v2, LEFT * 0.34, 44, WHITE)
        label_c = self.side_label("c", v1, v2, (UP + RIGHT) * 0.28, 46, WHITE)
        side_labels = VGroup(label_a, label_b, label_c)

        hypotenuse = Line(v1, v2, color=WHITE, stroke_width=8)
        hypotenuse_glow = self.glow(hypotenuse, BLUE, 14)

        # self.play(FadeIn(hook_top, shift=DOWN * 0.18), Write(hook_bottom), run_time=0.85)
        self.play(Create(start_triangle),FadeIn(side_labels),run_time=0.95)
        self.play(Write(question),rate_func=lambda t: smooth(1 - t),run_time=0.7)
        self.play(Create(hypotenuse_glow), Indicate(label_c, color=BLUE, scale_factor=1.25), run_time=0.65)
        self.play(FadeOut(hypotenuse_glow), run_time=0.4)
        self.wait(0.3)

        # --- Scene 2: Duplicate and arrange four congruent triangles ---
        self.play(FadeOut(side_labels),run_time=0.5)
        start_triangle.set_z_index(2)

        green_tri = self.style_triangle(start_triangle.copy(), GREEN)
        blue_tri = self.style_triangle(start_triangle.copy(), BLUE)
        pink_tri = self.style_triangle(start_triangle.copy(), PINK)
        green_start = self.style_triangle(start_triangle.copy(), GREEN)
        blue_start = self.style_triangle(start_triangle.copy(), BLUE)
        pink_start = self.style_triangle(start_triangle.copy(), PINK)
        green_tri.shift(UP * 0.18 + RIGHT * 0.12)
        blue_tri.shift(DOWN * 0.12 + RIGHT * 0.22)
        pink_tri.shift(UP * 0.08 + LEFT * 0.18)

        self.play(
            LaggedStart(
                ReplacementTransform(green_start, green_tri),
                ReplacementTransform(blue_start, blue_tri),
                ReplacementTransform(pink_start, pink_tri),
                lag_ratio=0.18,
            ),
            run_time=1.2,rate_fun=smooth
        )

        self.play(
            Rotate(green_tri, angle=PI / 2, about_point=green_tri.get_center()),
            Rotate(blue_tri, angle=PI, about_point=blue_tri.get_center()),
            Rotate(pink_tri, angle=-PI / 2, about_point=pink_tri.get_center()),
            run_time=1.0,
        )

        corner_bl = square_center + LEFT * half_sum + DOWN * half_sum
        corner_br = square_center + RIGHT * half_sum + DOWN * half_sum
        corner_tr = square_center + RIGHT * half_sum + UP * half_sum
        corner_tl = square_center + LEFT * half_sum + UP * half_sum

        targets = VGroup(
            self.final_triangle(a_len, b_len, corner_bl, 0, Red),
            self.final_triangle(a_len, b_len, corner_br, PI / 2, GREEN),
            self.final_triangle(a_len, b_len, corner_tr, PI, BLUE),
            self.final_triangle(a_len, b_len, corner_tl, -PI / 2, PINK),
        )
        for mob in targets:
            mob.set_z_index(2)

        self.play(
            start_triangle.animate.move_to(targets[0].get_center()),
            green_tri.animate.move_to(targets[1].get_center()),
            blue_tri.animate.move_to(targets[2].get_center()),
            pink_tri.animate.move_to(targets[3].get_center()),
            run_time=1.35,
            rate_func=smooth,
        )
        self.play(
            ReplacementTransform(start_triangle, targets[0]),
            ReplacementTransform(green_tri, targets[1]),
            ReplacementTransform(blue_tri, targets[2]),
            ReplacementTransform(pink_tri, targets[3]),
            run_time=0.25,
        )
        triangles = targets

        # --- Scene 3: Reveal the outer square and central c-square ---
        outer_square = Square(side_length=side_sum, color=CHALK, stroke_width=5)
        outer_square.move_to(square_center)
        outer_square.set_z_index(4)
        outer_square.set_fill(WHITE,opacity=0.02)

        side_brace = BraceBetweenPoints(corner_tl, corner_tr, UP, color=CHALK)
        side_sum_label = self.chalk_math(r"(a+b)", 44, CHALK).next_to(side_brace, UP, buff=0.12)

        def point_in_square(x, y):
            return square_center + LEFT * half_sum + DOWN * half_sum + RIGHT * x + UP * y

        p_bottom = point_in_square(a_len, 0)
        p_right = point_in_square(side_sum, a_len)
        p_top = point_in_square(b_len, side_sum)
        p_left = point_in_square(0, b_len)
        inner_square = Polygon(p_bottom, p_right, p_top, p_left)
        inner_square.set_fill(YELLOW, opacity=0.4)
        inner_square.set_stroke(YELLOW, width=5)
        inner_square.set_z_index(5)

        c_labels = VGroup()
        for p1, p2 in [(p_bottom, p_right), (p_right, p_top), (p_top, p_left), (p_left, p_bottom)]:
            mid = (p1 + p2) / 2
            inward = square_center - mid
            inward = inward / np.linalg.norm(inward)
            c_lab = MathTex("c", font_size=38, color=BLACK).move_to(mid + inward * 0.28)
            c_lab.set_z_index(7)
            c_labels.add(c_lab)

        # inner_area = self.chalk_math(r"\text{Inner Square Area}=c^2", 42, CHALK)
        # inner_area.next_to(outer_square, DOWN, buff=0.52)

        self.play(Create(outer_square), run_time=0.55)
        self.play(FadeIn(side_brace), Write(side_sum_label), run_time=0.55)
        self.play(FadeIn(inner_square, scale=0.92), LaggedStartMap(FadeIn, c_labels, lag_ratio=0.08), run_time=0.75)
        self.play(Circumscribe(inner_square, color=YELLOW, time_width=0.6), run_time=0.85)
        self.wait(0.15)

        # --- Scene 4: Count areas ---
        area_large = self.chalk_math(r"\text{Area of Large Square}=(a+b)^2", 34, CHALK)
        area_tris = self.chalk_math(r"\text{Area of Four Triangles}=4\left(\frac{1}{2}ab\right)", 34, CHALK)
        area_inner = self.chalk_math(r"\text{Area of Inner Square}=c^2", 34, CHALK)
        area_list = VGroup(area_large, area_tris, area_inner).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        area_list.move_to(DOWN * 4)

        self.wait(0.3)

        self.play(Write(area_list[0]),run_time=0.75)
        self.play(Write(area_list[1]),run_time=0.75)
        self.play(Write(area_list[2]),run_time=0.75)
        self.wait(0.4)
        equation_1 = MathTex(
            r"(a+b)^2",
            "=",
            r"4\left(\frac{1}{2}ab\right)",
            "+",
            "c^2",
            font_size=52,
            color=CHALK,
        )
        equation_1.move_to(area_list)
        equation_1.set_stroke(CHALK, width=0.4, opacity=0.55)

        self.play(ReplacementTransform(area_list, equation_1), run_time=1.2)
        self.play(Circumscribe(equation_1[2], color=YELLOW, time_width=0.55), run_time=0.45)

        equation_2 = MathTex(
            r"(a+b)^2",
            "=",
            "2ab",
            "+",
            "c^2",
            font_size=56,
            color=CHALK,
        )
        equation_2.move_to(equation_1)
        equation_2.set_stroke(CHALK, width=0.4, opacity=0.55)

        self.play(TransformMatchingTex(equation_1, equation_2), run_time=0.9)
        self.wait(0.2)

        # --- Scene 5: Expand, cancel, and reveal the theorem ---
        self.play(Circumscribe(equation_2[0], color=BLUE, time_width=0.55), run_time=0.45)
        equation_3 = MathTex(
            "a^2",
            "+",
            "2ab",
            "+",
            "b^2",
            "=",
            "2ab",
            "+",
            "c^2",
            font_size=50,
            color=CHALK,
        )
        equation_3.move_to(equation_2)
        equation_3.set_stroke(CHALK, width=0.4, opacity=0.55)

        self.play(TransformMatchingTex(equation_2, equation_3), run_time=0.95)
        self.play(
            equation_3[2].animate.set_color(Red).set_stroke(Red, width=0.4, opacity=0.7),
            equation_3[6].animate.set_color(Red).set_stroke(Red, width=0.4, opacity=0.7),
            Indicate(equation_3[2], color=Red, scale_factor=1.15),
            Indicate(equation_3[6], color=Red, scale_factor=1.15),
            run_time=0.65,
        )
        cancel_left = Cross(equation_3[2], stroke_color=Red, stroke_width=5)
        cancel_right = Cross(equation_3[6], stroke_color=Red, stroke_width=5)
        self.play(Create(cancel_left), Create(cancel_right), run_time=0.35)

        final_equation = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=80, color=CHALK)
        final_equation.move_to(DOWN * 4.56)
        final_equation.set_color_by_gradient("#f2f20c", GREEN, BLUE, "#e35bc5")
        final_equation.set_stroke(CHALK, width=0.7, opacity=0.65)
        final_equation.set_z_index(8)
        final_glow = self.glow(final_equation, YELLOW, 16)
        final_glow.move_to(final_equation)
        final_glow.set_fill(opacity=0)
        final_glow.set_z_index(7)

        self.play(
            ReplacementTransform(equation_3[0], final_equation[0]),
            ReplacementTransform(equation_3[3], final_equation[1]),
            ReplacementTransform(equation_3[4], final_equation[2]),
            ReplacementTransform(equation_3[5], final_equation[3]),
            ReplacementTransform(equation_3[8], final_equation[4]),
            FadeOut(equation_3[1], equation_3[2], equation_3[6], equation_3[7], cancel_left, cancel_right),
            FadeIn(final_glow),
            run_time=0.9,
        )
        proof_objects = VGroup(
            triangles,
            outer_square,
            side_brace,
            side_sum_label,
            inner_square,
            c_labels,
            # final_equation,
            # final_glow,
        )
        self.play(FadeOut(proof_objects), run_time=0.65)

        heading_B  = MathTex(r"\mathbb{P}", font_size=65,  color=WHITE).stretch(1.28, dim=1).set_stroke(width=1.6)
        heading_P1 = MathTex(r"\mathbb{T}", font_size=65,  color=WHITE).stretch(1.28, dim=1).set_stroke(width=1.6)

        text_1 = Text("ythagoras", font_size=58, color=WHITE, weight=LIGHT)
        text_2 = Text("heorem ",   font_size=58, color=WHITE, weight=LIGHT)

        word_1 = VGroup(heading_B,text_1).arrange(RIGHT, buff=0.05, aligned_edge=UP)
        word_2 = VGroup(heading_P1,text_2).arrange(RIGHT, buff=0.03, aligned_edge=UP)
    

        title_1 = VGroup(word_1, word_2).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title_1.to_edge(UP, buff=5.4)
        title_1.set_color_by_gradient("#e2442f", "#eca41f")        

        self.play(
            Create(title_1),
            final_equation.animate.scale(1.1).move_to(UP * 0.45),
            final_glow.animate.scale(1.1).move_to(UP * 0.35),
            run_time=1.2,
        )
        self.play( Circumscribe(final_equation, color=YELLOW, time_width=0.65),run_time=0.8)
        self.play(Indicate(final_equation, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.wait(1)
