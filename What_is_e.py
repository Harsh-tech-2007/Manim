from manim import *
import math


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK


class ExplainEWithGraph(Scene):
    def construct(self):
        n_values = list(range(1, 101)) + [
            200,
            500,
            1000,
            5000,
            10000,
            100000,
        ]
        data = [(n, (1 + 1 / n) ** n) for n in n_values]
             
        heading_h = MathTex(
            r"\mathbb{W}",
            font_size=98,
            color=WHITE,
        )
        heading_h.stretch(1.28, dim=1)
        
        heading_h.set_stroke(width=1.6)
        
        heading_text = Text(
            "hat is e?",
            font_size=88,
            color=WHITE,
            weight=LIGHT,
        )
        
        title = VGroup(
            heading_h,
            heading_text
        ).arrange(
            RIGHT,
            buff=0,
            aligned_edge=UP
        )
        title.to_edge(UP,buff=1.5)
        title.set_color_by_gradient("#ec3078", "#f1324b")         

        main_formula = MathTex(
            r"\left(1+\frac{1}{n}\right)^n",
            font_size=72,
            color=WHITE,
        )
        main_formula.next_to(title, DOWN, buff=0.90)

        axes = Axes(
            x_range=[0, 6.2, 1],
            y_range=[1.9, 2.82, 0.2],
            x_length=7.25,
            y_length=4.4,
            tips=False,
            axis_config={
                "stroke_width": 3  ,      
                "color": WHITE,
                "include_tip": True,
                "tip_shape":StealthTip,
                "tip_length":0.22,},
            y_axis_config={
                "decimal_number_config": {"num_decimal_places": 1},
            },
        )
        axes.move_to(DOWN * 1.5)

        e_line = DashedLine(
            axes.c2p(0, math.e),
            axes.c2p(6, math.e),
            color=YELLOW,
            stroke_width=3,
            dash_length=0.12,
        )
        e_label = MathTex(r"e", font_size=60, color=YELLOW)
        e_label.next_to(e_line,LEFT, buff=0.28)

        x_labels = self.make_x_labels(axes)
        x_in = MathTex("\infty", font_size=38, color=GREY_A)
        x_in.next_to(axes.x_axis, RIGHT+DOWN, buff=0.08).shift(LEFT*0.8)
        x_axis_label = axes.get_axis_labels(
            Text("x").scale(0.7), Text("y").scale(0.7))  
        current_n = self.make_n_text(data[0][0])
        current_value = self.make_value_text(data[0][0], data[0][1])
        current_curve = self.make_curve(axes, data[:1])
        current_dot = Dot(
            axes.c2p(self.x_from_n(data[0][0]), data[0][1]),
            color=ORANGE,
            radius=0.085,
        ).set_z_index(3)
        current_marker = self.make_marker(axes, data[0][0], data[0][1])
        current_graph_value = self.make_graph_value(axes, data[0][0], data[0][1])

        self.play(Write(title),run_time=1)
        self.wait(0.5)
        self.play(FadeIn(main_formula, shift=UP * 0.2))
        # self.wait(0.35)
        self.play(
            Create(axes),
            FadeIn(x_labels),
            FadeIn(x_axis_label),
            run_time=1,
        )
        self.play(Create(e_line), FadeIn(e_label), run_time=0.8) 
        self.play(FadeOut(title),FadeOut(main_formula),run_time=0.5)   

        self.play(
            FadeIn(current_n, shift=UP * 0.2),
            FadeIn(current_value, shift=UP * 0.2),
            Create(current_curve),
            Create(current_marker),
            FadeIn(current_dot),
            FadeIn(current_graph_value),
            run_time=0.7,
        )
        self.wait(1)  
        for index, (n, value) in enumerate(data[1:], start=1):
            next_n = self.make_n_text(n)
            next_value = self.make_value_text(n, value)
            next_curve = self.make_curve(axes, data[: index + 1])
            next_marker = self.make_marker(axes, n, value)
            next_graph_value = self.make_graph_value(axes, n, value)
            next_point = axes.c2p(self.x_from_n(n), value)

            if n <= 20:
                run_time = 0.16
            elif n <= 100:
                run_time = 0.04
            else:
                run_time = 0.55

            self.play(
                Transform(current_n, next_n),
                Transform(current_value, next_value),
                Transform(current_curve, next_curve),
                Transform(current_marker, next_marker),
                Transform(current_graph_value, next_graph_value),
                current_dot.animate.move_to(next_point),
                run_time=run_time,
            )

        limit_text = MathTex(
            r"\lim_{n\to\infty}",
            font_size=54,
            color=WHITE,
        )
        
        expression = MathTex(
            r"\left(1+\frac{1}{n}\right)^n",
            font_size=74,
            color=WHITE,
        )
        
        equals_e = MathTex(
            r"= e",
            font_size=74,
            color=YELLOW,
        )
        
        final_formula = VGroup(
            limit_text,
            expression,
            equals_e
        ).arrange(RIGHT, buff=0.15)
        
        final_formula.move_to(current_value)          
        final_answer = MathTex(r"e\approx2.71828", font_size=66, color=YELLOW)
        final_answer.to_edge(DOWN, buff=2.8)
         
        final_dot = axes.c2p(6, math.e)
        final_marker = DashedLine(
            axes.c2p(6, 1.9),
            final_dot,
            color=ORANGE,
            stroke_width=3,
            dash_length=0.09,
        )
        final_graph_value = MathTex(r"2.71828\ldots", font_size=30, color=ORANGE)
        final_graph_value.move_to(final_dot + LEFT * 0.6 + UP * 0.35)

        self.play(
            FadeOut(current_n),
            Transform(current_value, final_formula),
            current_curve.animate.set_color(YELLOW),
            Transform(current_marker, final_marker),
            Transform(current_graph_value, final_graph_value),
            current_dot.animate.move_to(final_dot),
            run_time=0.9, )
        self.play(FadeIn(x_in),FadeIn(final_answer, shift=UP * 0.25))
        self.play(FadeOut(current_curve),FadeOut(current_marker),
                  FadeOut(current_graph_value),FadeOut(current_dot),
                  FadeOut(x_in),FadeOut(axes),
                  FadeOut(x_labels),FadeOut(x_axis_label), 
                  FadeOut(e_line), FadeOut(e_label),run_time=0.2) 
        
        self.play(current_value.animate.move_to(ORIGIN),FadeOut(final_answer))
        self.play(current_value.animate.scale(1.3), rate_func=there_and_back,run_time=1)

        self.wait(1.1)

    def make_x_labels(self, axes):
        labels = VGroup()
        for power in range(6):
            tick = Line(
                axes.c2p(power, 1.9),
                axes.c2p(power, 1.94),
                color=GREY_B,
                stroke_width=2,
            )
            text = MathTex(rf"10^{power}", font_size=25, color=GREY_A)
            text.next_to(tick, DOWN, buff=0.2)
            labels.add(tick, text)
        return labels

    def make_n_text(self, n):
        label = MathTex(rf"n={self.format_tex_int(n)}", font_size=55, color=WHITE)
        label.to_edge(UP,buff=2.9)
        return label

    def make_value_text(self, n, value):
        if(n>2):
                tex = (
                    rf"\left(1+\frac{{1}}{{{self.format_tex_int(n)}}}\right)"
                    rf"^{{{self.format_tex_int(n)}}}\approx {value:.5f}")
        else:
                 tex = (
                    rf"\left(1+\frac{{1}}{{{self.format_tex_int(n)}}}\right)"
                    rf"^{{{self.format_tex_int(n)}}} = {value:.5f}")
        
        label = MathTex(tex, font_size=65,color=WHITE)
        if label.width > 7.8:
            label.scale_to_fit_width(7.8)
        label.to_edge(UP,buff=3.8)
        return label

    def make_marker(self, axes, n, value):
        x = self.x_from_n(n)
        marker = DashedLine(
            axes.c2p(x, 1.9),
            axes.c2p(x, value),
            color=ORANGE,
            stroke_width=3,
            dash_length=0.09,
        )
        marker.set_z_index(2)
        return marker

    def make_graph_value(self, axes, n, value):
        x = self.x_from_n(n)
        label = MathTex(f"{value:.5f}", font_size=38, color=ORANGE)
        shift = UP * 0.35
        if x > 6:
            shift += LEFT * 0.45
        label.move_to(axes.c2p(x, value) + shift)
        label.set_z_index(4)
        return label

    def make_curve(self, axes, data):
        points = [axes.c2p(self.x_from_n(n), value) for n, value in data]
        if len(points) == 1:
            points.append(points[0])

        curve = VMobject(color=BLUE_C, stroke_width=5)
        curve.set_points_as_corners(points)
        curve.set_z_index(1)
        return curve

    def x_from_n(self, n):
        return math.log10(n)

    def format_tex_int(self, n):
        return f"{n:,}".replace(",", r"{,}")