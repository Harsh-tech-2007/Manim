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
RED = "#df4257"
PURPLE = "#da70d6"
ORANGE = "#ffb347"

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

        question = self.chalk_math(r"(a+b+c)^2 = ?", 98)
        question.set_color_by_gradient("#1cdb9b", "#29acbd")        
        question.move_to(UP * 1.35)
        self.play(Write(question), run_time=1.0)
        self.wait(0.25)
        self.play(question.animate.scale(0.72).to_edge(UP, buff=0.65), run_time=0.8)
      
        side_a = 2.2
        side_b = 1.6
        side_c = 1.2
        total_side = side_a + side_b + side_c
        
        square = Square(side_length=total_side, color=CHALK, stroke_width=5)
        square.move_to(UP * 1.5)
        square.set_fill("#ffffff", opacity=0.04)

        left_x = square.get_left()[0]
        right_x = square.get_right()[0]
        top_y = square.get_top()[1]
        bottom_y = square.get_bottom()[1]
        
        split_x_1 = left_x + side_a
        split_x_2 = left_x + side_a + side_b
        split_y_1 = top_y - side_a
        split_y_2 = top_y - side_a - side_b
          
        self.play(Create(square), FadeOut(question), run_time=0.9)
        self.play(
            self.camera.frame.animate.scale(0.92).move_to(square.get_center() + DOWN * 0.15),
            run_time=0.7,
        )

        v_split_1 = Line([split_x_1, top_y, 0], [split_x_1, bottom_y, 0], color=BLUE, stroke_width=5)
        v_split_2 = Line([split_x_2, top_y, 0], [split_x_2, bottom_y, 0], color=BLUE, stroke_width=5)
        h_split_1 = Line([left_x, split_y_1, 0], [right_x, split_y_1, 0], color=BLUE, stroke_width=5)
        h_split_2 = Line([left_x, split_y_2, 0], [right_x, split_y_2, 0], color=BLUE, stroke_width=5)
        
        self.play(Create(v_split_1), Create(v_split_2), Create(h_split_1), Create(h_split_2), run_time=0.6)

        colors = [GREEN, BLUE, PINK, BLUE, PURPLE, ORANGE, PINK, ORANGE, RED]
        regions = []
        texts = []
        
        # Row 1 (top)
        rect_a2 = Square(side_length=side_a, color=GREEN, stroke_width=5)
        rect_a2.move_to([(left_x + split_x_1) / 2, (top_y + split_y_1) / 2, 0])
        rect_a2.set_fill(GREEN, opacity=0.18)
        regions.append(rect_a2)
        text_a2 = self.chalk_math(r"a^2", 40, GREEN).move_to(rect_a2)
        texts.append(text_a2)

        rect_ab_1 = Rectangle(width=side_b, height=side_a, color=BLUE, stroke_width=5)
        rect_ab_1.move_to([(split_x_1 + split_x_2) / 2, (top_y + split_y_1) / 2, 0])
        rect_ab_1.set_fill(BLUE, opacity=0.18)
        regions.append(rect_ab_1)
        text_ab_1 = self.chalk_math(r"ab", 36, BLUE).move_to(rect_ab_1)
        texts.append(text_ab_1)

        rect_ac_1 = Rectangle(width=side_c, height=side_a, color=PINK, stroke_width=5)
        rect_ac_1.move_to([(split_x_2 + right_x) / 2, (top_y + split_y_1) / 2, 0])
        rect_ac_1.set_fill(PINK, opacity=0.18)
        regions.append(rect_ac_1)
        text_ac_1 = self.chalk_math(r"ac", 36, PINK).move_to(rect_ac_1)
        texts.append(text_ac_1)

        # Row 2 (middle)
        rect_ab_2 = Rectangle(width=side_a, height=side_b, color=BLUE, stroke_width=5)
        rect_ab_2.move_to([(left_x + split_x_1) / 2, (split_y_1 + split_y_2) / 2, 0])
        rect_ab_2.set_fill(BLUE, opacity=0.18)
        regions.append(rect_ab_2)
        text_ab_2 = self.chalk_math(r"ab", 36, BLUE).move_to(rect_ab_2)
        texts.append(text_ab_2)

        rect_b2 = Square(side_length=side_b, color=PURPLE, stroke_width=5)
        rect_b2.move_to([(split_x_1 + split_x_2) / 2, (split_y_1 + split_y_2) / 2, 0])
        rect_b2.set_fill(PURPLE, opacity=0.18)
        regions.append(rect_b2)
        text_b2 = self.chalk_math(r"b^2", 40, PURPLE).move_to(rect_b2)
        texts.append(text_b2)

        rect_bc_1 = Rectangle(width=side_c, height=side_b, color=ORANGE, stroke_width=5)
        rect_bc_1.move_to([(split_x_2 + right_x) / 2, (split_y_1 + split_y_2) / 2, 0])
        rect_bc_1.set_fill(ORANGE, opacity=0.18)
        regions.append(rect_bc_1)
        text_bc_1 = self.chalk_math(r"bc", 36, ORANGE).move_to(rect_bc_1)
        texts.append(text_bc_1)

        # Row 3 (bottom)
        rect_ac_2 = Rectangle(width=side_a, height=side_c, color=PINK, stroke_width=5)
        rect_ac_2.move_to([(left_x + split_x_1) / 2, (split_y_2 + bottom_y) / 2, 0])
        rect_ac_2.set_fill(PINK, opacity=0.18)
        regions.append(rect_ac_2)
        text_ac_2 = self.chalk_math(r"ac", 36, PINK).move_to(rect_ac_2)
        texts.append(text_ac_2)

        rect_bc_2 = Rectangle(width=side_b, height=side_c, color=ORANGE, stroke_width=5)
        rect_bc_2.move_to([(split_x_1 + split_x_2) / 2, (split_y_2 + bottom_y) / 2, 0])
        rect_bc_2.set_fill(ORANGE, opacity=0.18)
        regions.append(rect_bc_2)
        text_bc_2 = self.chalk_math(r"bc", 36, ORANGE).move_to(rect_bc_2)
        texts.append(text_bc_2)

        rect_c2 = Square(side_length=side_c, color=RED, stroke_width=5)
        rect_c2.move_to([(split_x_2 + right_x) / 2, (split_y_2 + bottom_y) / 2, 0])
        rect_c2.set_fill(RED, opacity=0.18)
        regions.append(rect_c2)
        text_c2 = self.chalk_math(r"c^2", 40, RED).move_to(rect_c2)
        texts.append(text_c2)

        self.play(FadeIn(regions[0]), FadeIn(regions[1]), FadeIn(regions[2]), run_time=0.5)
        self.play(FadeIn(regions[3]), FadeIn(regions[4]), FadeIn(regions[5]), run_time=0.5)
        self.play(FadeIn(regions[6]), FadeIn(regions[7]), FadeIn(regions[8]), run_time=0.5)
        
        self.play(*[Write(text) for text in texts], run_time=1.2)

        # --- DIMENSIONS ---
        dim_a_bottom = BraceBetweenPoints(square.get_corner(DL) + RIGHT * side_a, square.get_corner(DL), DOWN, color=CHALK)
        dim_b_bottom = BraceBetweenPoints(square.get_corner(DL) + RIGHT * (side_a + side_b), square.get_corner(DL) + RIGHT * side_a, DOWN, color=CHALK)
        dim_c_bottom = BraceBetweenPoints(square.get_corner(DR), square.get_corner(DL) + RIGHT * (side_a + side_b), DOWN, color=CHALK)
        
        lab_a_bottom = self.chalk_math("a", 32, CHALK).next_to(dim_a_bottom, DOWN, buff=0.1)
        lab_b_bottom = self.chalk_math("b", 32, CHALK).next_to(dim_b_bottom, DOWN, buff=0.1)
        lab_c_bottom = self.chalk_math("c", 32, CHALK).next_to(dim_c_bottom, DOWN, buff=0.1)

        dim_a_left = BraceBetweenPoints(square.get_corner(UL), square.get_corner(UL) + DOWN * side_a, LEFT, color=CHALK)
        dim_b_left = BraceBetweenPoints(square.get_corner(UL) + DOWN * side_a, square.get_corner(UL) + DOWN * (side_a + side_b), LEFT, color=CHALK)
        dim_c_left = BraceBetweenPoints(square.get_corner(DL), square.get_corner(UL) + DOWN * (side_a + side_b), LEFT, color=CHALK)
        
        lab_a_left = self.chalk_math("a", 32, CHALK).next_to(dim_a_left, LEFT, buff=0.1)
        lab_b_left = self.chalk_math("b", 32, CHALK).next_to(dim_b_left, LEFT, buff=0.1)
        lab_c_left = self.chalk_math("c", 32, CHALK).next_to(dim_c_left, LEFT, buff=0.1)

        dims = VGroup(
            dim_a_bottom, dim_b_bottom, dim_c_bottom, lab_a_bottom, lab_b_bottom, lab_c_bottom,
            dim_a_left, dim_b_left, dim_c_left, lab_a_left, lab_b_left, lab_c_left
        )
        self.play(LaggedStartMap(FadeIn, dims, lag_ratio=0.06), run_time=0.9)
        
        self.wait(0.5)

        # --- EQUATION BUILDING ---
        equation = MathTex(
            r"(a+b+c)^2", r"=", 
            r"a^2", r"+", r"b^2", r"+", r"c^2", r"+",
            r"2ab", r"+", r"2ac", r"+", r"2bc",
            font_size=34, color=WHITE
        )
        
        equation.to_edge(DOWN, buff=4.6)
        
        self.play(self.camera.frame.animate.scale(1.05).move_to(ORIGIN), run_time=0.8)

        self.play(Write(equation[0]),run_time=0.8)
        self.play(FadeIn(equation[1]),run_time=0.3)
        self.wait(0.15)

        # Squares
        self.play(
            Create(self.glow(rect_a2, GREEN, 10)),
            Create(self.glow(rect_b2, PURPLE, 10)),
            Create(self.glow(rect_c2, RED, 10)),
            Write(equation[2]), FadeIn(equation[3]), Write(equation[4]), FadeIn(equation[5]), Write(equation[6]), FadeIn(equation[7]),
            run_time=1.0
        )
        self.play(FadeOut(self.glow(rect_a2, GREEN, 10)), FadeOut(self.glow(rect_b2, PURPLE, 10)), FadeOut(self.glow(rect_c2, RED, 10)))
        self.wait(0.15)

        # Double products
        self.play(
            Create(self.glow(rect_ab_1, BLUE, 10)),
            Create(self.glow(rect_ab_2, BLUE, 10)),
            Write(equation[8]), FadeIn(equation[9]),
            run_time=0.7
        )
        self.play(FadeOut(self.glow(rect_ab_1, BLUE, 10)), FadeOut(self.glow(rect_ab_2, BLUE, 10)))

        self.play(
            Create(self.glow(rect_ac_1, PINK, 10)),
            Create(self.glow(rect_ac_2, PINK, 10)),
            Write(equation[10]), FadeIn(equation[11]),
            run_time=0.7
        )
        self.play(FadeOut(self.glow(rect_ac_1, PINK, 10)), FadeOut(self.glow(rect_ac_2, PINK, 10)))

        self.play(
            Create(self.glow(rect_bc_1, ORANGE, 10)),
            Create(self.glow(rect_bc_2, ORANGE, 10)),
            Write(equation[12]),
            run_time=0.7
        )
        self.play(FadeOut(self.glow(rect_bc_1, ORANGE, 10)), FadeOut(self.glow(rect_bc_2, ORANGE, 10)))

         
        final_eq = self.chalk_math(r"(a+b+c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc",35)
        final_eq.set_color_by_gradient("#24c1c1", "#22c978") 
        final_eq.move_to(equation) 
        self.play(
            FadeOut(square),
            FadeOut(v_split_1), FadeOut(v_split_2), FadeOut(h_split_1), FadeOut(h_split_2),
            run_time=0.8
        )
        
        self.play(ReplacementTransform(equation, final_eq))
        objects_to_fade = [
            mob for mob in self.mobjects 
            if mob is not final_eq and mob is not self.camera.frame
        ]
        self.play(
            *[FadeOut(mob) for mob in objects_to_fade],
            run_time=0.7
        )
    
        self.wait(0.2)
        self.play(
            self.camera.frame.animate.move_to(ORIGIN),
            final_eq.animate.move_to(ORIGIN),
            run_time=0.7
        )
        
        self.wait(0.3)
        final_box = SurroundingRectangle(final_eq, buff=0.18, stroke_width=4)
        final_box.set_color_by_gradient("#27d4c0", "#24d58e", "#26cf75")  
        self.play(Create(final_box), run_time=0.9)
        
        self.wait(2.0)