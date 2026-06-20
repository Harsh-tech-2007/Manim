from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK

CHALK = "#ffffff"
YELLOW = "#ffd84d"
GREEN = "#77e6bb"
BLUE = "#9cc9ff"
PINK = "#ff9bc5"
Red= "#df4257"

class Video(MovingCameraScene):
    def chalk_text(self, text, size=42, color=CHALK):
        return Text(text, font_size=size, color=color)

    def chalk_math(self, tex, size=42, color=CHALK):
        mob = MathTex(tex, font_size=size, color=color)
        mob.set_stroke(color, width=0.4, opacity=0.55)
        return mob

    def glow(self, mob, color=YELLOW, width=10):
        return mob.copy().set_color(color).set_stroke(color, width=width, opacity=0.35)

    def construct(self):
        heading_h = MathTex(r"\mathbb{W}", font_size=108, color=WHITE)
        heading_h.stretch(1.28, dim=1)
        heading_h.set_stroke(width=1.6)
        
        heading_text = self.chalk_text("hy", 98, CHALK)
        question_1 = VGroup(heading_h, heading_text).arrange(RIGHT, buff=0, aligned_edge=UP)
        question_1.set_color_by_gradient("#ec3078", "#f1324b")        

        question_2 = self.chalk_math(r"a^2-b^2=(a+b)(a-b)?", 70)   
        question = VGroup(question_1, question_2).arrange(DOWN, buff=0.58)
        question.move_to(UP * 1.35)
        
        self.play(Write(question_1), run_time=0.8)
        self.play(Write(question_2), run_time=1.0)
        self.wait(0.25)
        self.play(question.animate.scale(0.72).to_edge(UP, buff=0.65), run_time=0.8)
      
        side_a = 5.2
        side_b = 2.0
        side_left = side_a - side_b
        square = Square(side_length=side_a, color=CHALK, stroke_width=5)
        square.move_to(UP * 1.5)
        square.set_fill("#ffffff", opacity=0.04)

        left_x = square.get_left()[0]
        right_x = square.get_right()[0]
        top_y = square.get_top()[1]
        bottom_y = square.get_bottom()[1]
        split_x = left_x + side_left
        split_y = top_y - side_left
          
        self.play(Create(square), FadeOut(question), run_time=0.9)
        self.play(
            self.camera.frame.animate.scale(0.92).move_to(square.get_center() + DOWN * 0.15),
            run_time=0.7,
        )

        vertical_split = Line([split_x, top_y, 0], [split_x, bottom_y, 0], color=BLUE, stroke_width=5)
        horizontal_split = Line([split_x, split_y, 0], [right_x, split_y, 0], color=BLUE, stroke_width=5)
        self.play(Create(vertical_split), Create(horizontal_split), run_time=0.5)

        left_rect = Rectangle(width=side_left, height=side_a, color=GREEN, stroke_width=5)
        left_rect.move_to([(left_x + split_x) / 2, (top_y + bottom_y) / 2, 0])
        left_rect.set_fill(GREEN, opacity=0.18)

        top_rect = Rectangle(width=side_b, height=side_left, color=BLUE, stroke_width=5)
        top_rect.move_to([(split_x + right_x) / 2, (top_y + split_y) / 2, 0])
        top_rect.set_fill(BLUE, opacity=0.18)

        small_square = Square(side_length=side_b, color=PINK, stroke_width=5)
        small_square.move_to([(split_x + right_x) / 2, (split_y + bottom_y) / 2, 0])
        small_square.set_fill(PINK, opacity=0.18)

        self.play(FadeIn(left_rect), FadeIn(top_rect), FadeIn(small_square), run_time=0.8)

        dim_a_bottom = BraceBetweenPoints(square.get_corner(DL), square.get_corner(DR), DOWN, color=CHALK)
        dim_a_right = BraceBetweenPoints(square.get_corner(UL), square.get_corner(DL), LEFT, color=CHALK)
        lab_a_bottom = self.chalk_math("a", 36, CHALK).next_to(dim_a_bottom, DOWN, buff=0.12)
        lab_a_right = self.chalk_math("a", 36, CHALK).next_to(dim_a_right, LEFT, buff=0.12)

        dim_left = BraceBetweenPoints([left_x, top_y, 0], [split_x, top_y, 0], UP, color=YELLOW)
        dim_b_top = BraceBetweenPoints([split_x, top_y, 0], [right_x, top_y, 0], UP, color=YELLOW)
        lab_left = self.chalk_math(r"a-b", 34, YELLOW).next_to(dim_left, UP, buff=0.1)
        lab_b_top = self.chalk_math("b", 34, YELLOW).next_to(dim_b_top, UP, buff=0.1)

        dim_right_left = BraceBetweenPoints([right_x, top_y, 0], [right_x, split_y, 0], RIGHT, color=YELLOW)
        dim_right_b = BraceBetweenPoints([right_x, split_y, 0], [right_x, bottom_y, 0], RIGHT, color=YELLOW)
        lab_right_left = self.chalk_math(r"a-b", 32, YELLOW).next_to(dim_right_left, RIGHT, buff=0.1)
        lab_right_b = self.chalk_math("b", 32, YELLOW).next_to(dim_right_b, RIGHT, buff=0.1)

        dims = VGroup(
            dim_a_bottom, dim_a_right, lab_a_bottom, lab_a_right,
            dim_left, dim_b_top, lab_left, lab_b_top,
            dim_right_left, dim_right_b, lab_right_left, lab_right_b,
        )
        self.play(LaggedStartMap(FadeIn, dims, lag_ratio=0.08), run_time=1.0)

        area_left = self.chalk_math(r"a(a-b)", 45, GREEN).move_to(left_rect)
        area_top = self.chalk_math(r"b(a-b)", 32, BLUE).move_to(top_rect)
        area_small = self.chalk_math(r"b^2", 42, PINK).move_to(small_square)
        self.play(Write(area_left), Write(area_top), Write(area_small), run_time=1.2)
        
        left_glow = self.glow(left_rect, YELLOW, 12)
        top_glow = self.glow(top_rect, YELLOW, 12)
        Small_glow = self.glow(small_square, YELLOW, 12) 
        
        equation = MathTex(
            r"a^2", r"=", r"a(a-b)", r"+", r"b(a-b)", r"+", r"b^2",
            font_size=56, color=WHITE
        )
        
        equation.to_edge(DOWN, buff=4.0)
        self.play(self.camera.frame.animate.scale(1.04).move_to(ORIGIN), run_time=0.8)

        self.play(Create(left_glow), Create(top_glow), Create(Small_glow), Write(equation[0]), run_time=1.0)
        self.play(FadeOut(left_glow), FadeOut(Small_glow), FadeOut(top_glow))
        self.play(Create(left_glow), FadeIn(equation[1]), Write(equation[2]), run_time=0.5) 
        self.play(FadeOut(left_glow))
        self.play(Create(top_glow), FadeIn(equation[3]), Write(equation[4]), run_time=0.5)
        self.play(FadeOut(top_glow))
        self.play(Create(Small_glow), FadeIn(equation[5]), Write(equation[6]), run_time=0.5)
        self.play(FadeOut(Small_glow))
        
        self.wait(0.3)
        factor_label = VGroup(
            self.chalk_text("common width:", 31, YELLOW),
            self.chalk_math(r"a-b", 38, YELLOW),
        ).arrange(RIGHT, buff=0.16)
        factor_label.next_to(square, DOWN, buff=0.85)
        self.play(Create(left_glow), Create(top_glow), Write(factor_label), run_time=1.0)
        self.wait(0.35)
         
        equation_2 = self.chalk_math(r"a^2=(a+b)(a-b)+b^2", 56)
        equation_2.move_to(equation)
        
        self.play(
            ReplacementTransform(equation, equation_2),
            FadeOut(left_glow, top_glow),
            FadeOut(factor_label),
            run_time=1.35,
        )
        self.wait(0.3)

        minus_left = self.chalk_math(r"-b^2", 38, PINK).next_to(equation_2, DOWN, buff=0.32).shift(LEFT * 2.9)
        minus_right = self.chalk_math(r"-b^2", 38, PINK).next_to(equation_2, DOWN, buff=0.32).shift(RIGHT * 2.7)
        
        x_1 = Line(small_square.get_corner(UL) + DR * 0.14, small_square.get_corner(DR) + UL * 0.14, color=PINK, stroke_width=7)
        x_2 = Line(small_square.get_corner(UR) + DL * 0.14, small_square.get_corner(DL) + UR * 0.14, color=PINK, stroke_width=7)
        
        self.play(Write(minus_left), Write(minus_right), Create(x_1), Create(x_2), run_time=1.0)
        self.wait(0.2)

        self.play(FadeOut(square), FadeOut(vertical_split), FadeOut(horizontal_split), FadeOut(dims))

        target_center = UP * 2.2
        
        left_target_pos = target_center + UP * (side_b / 2)
        top_target_pos = target_center + DOWN * (side_a / 2)
        
        dim_total_height = BraceBetweenPoints(
            left_target_pos + UP * (side_a / 2) + LEFT * (side_left / 2),
            top_target_pos + DOWN * (side_b / 2) + LEFT * (side_left / 2),
            LEFT, color=YELLOW
        )
        lab_total_height = self.chalk_math(r"a+b", 36, YELLOW).next_to(dim_total_height, LEFT, buff=0.12)
        
        dim_total_width = BraceBetweenPoints(
            left_target_pos + UP * (side_a / 2) + LEFT * (side_left / 2),
            left_target_pos + UP * (side_a / 2) + RIGHT * (side_left / 2),
            UP, color=YELLOW
        )
        lab_total_width = self.chalk_math(r"a-b", 36, YELLOW).next_to(dim_total_width, UP, buff=0.12)
        new_dims = VGroup(dim_total_height, lab_total_height, dim_total_width, lab_total_width)
        final_eq = self.chalk_math(r"a^2-b^2=(a+b)(a-b)",66)
        final_eq.set_color_by_gradient("#cf242f","#cd7223") 
        final_eq.move_to(equation_2)
        self.play(
            left_rect.animate.move_to(left_target_pos),
            area_left.animate.move_to(left_target_pos),
            top_rect.animate
            .rotate(90 * DEGREES)
            .move_to(top_target_pos)
            .set_color(BLUE),
            area_top.animate
            .rotate(90 * DEGREES)
            .move_to(top_target_pos)
            .set_color(BLUE),

            FadeOut(small_square), FadeOut(area_small), FadeOut(x_1), FadeOut(x_2),
            self.camera.frame.animate.move_to(UP * 1.0),
            ReplacementTransform(VGroup(equation_2, minus_left, minus_right), final_eq),
            run_time=1.8
        )
        self.wait(0.2)
        self.play(FadeIn(new_dims))
        self.wait(0.3)

        # --- FINALIZING EQUATION ---
        final_box = SurroundingRectangle(final_eq,buff=0.18, stroke_width=4)
        final_box.set_color_by_gradient("#e2a32d", "#e3e635", "#cfa826")  
        self.play(Create(final_box), run_time=0.7)
        self.wait(1.0)