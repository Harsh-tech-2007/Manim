from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class tri(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
          
        heading_W = MathTex(r"\mathbb{W}", font_size=72, color=WHITE)
        heading_W.stretch(1.28, dim=1).set_stroke(width=1.6)  
        tit = Text("hy?", font_size=62, weight=BOLD)
        title = VGroup(heading_W, tit).arrange(RIGHT, buff=0.03, aligned_edge=UP)
        title.set_color_by_gradient("#ee4c37", "#ecad37")

        # Swapped x for \theta
        formula = MathTex(r"\sin^2 x", "+", r"\cos^2 x", "=", "1", font_size=66)

        opening = VGroup(title, formula).arrange(DOWN, buff=0.35)
        opening.move_to(ORIGIN)
          
        self.play(FadeIn(title, shift=UP * 0.25), run_time=0.8)
        self.play(Write(formula), run_time=1.6, rate_func=smooth)
        self.wait(0.35)
        self.play(opening.animate.scale(0.9).to_edge(UP, buff=1.5), run_time=0.9)

        # Axes with ticks enabled
        axes = Axes(
            x_range=[-TAU, TAU, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6.5,
            y_length=4.8,
            tips=False,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2,
                "include_ticks": True,
                "tick_size": 0.06,
            },
        ).shift(UP * 0.55)

        # Swapped x label for \theta
        x_label = MathTex("x", font_size=28).next_to(axes.x_axis, RIGHT, buff=0.12)
        y_label = MathTex("y", font_size=28).next_to(axes.y_axis, UP, buff=0.12)
        labels = VGroup(x_label, y_label).set_color(GREY_A)

        # Custom coordinates for X and Y axes in Degrees
        # Degree labels
        x_vals = [-TAU,-3 * PI / 2,-PI,-PI / 2,PI / 2,PI,3 * PI / 2,TAU,]

        x_tex = [
            r"-360^\circ",
            r"-270^\circ",
            r"-180^\circ",
            r"-90^\circ",
            r"90^\circ",
            r"180^\circ",
            r"270^\circ",
            r"360^\circ",
        ]

        x_coords = VGroup(*[
            MathTex(tex, font_size=22).next_to(
                axes.c2p(val, 0),
                DOWN,
                buff=0.15
            )
            for val, tex in zip(x_vals, x_tex)
        ])
       
        y_vals = [-1, 1]
        y_tex = ["-1", "1"]
        y_coords = VGroup(*[
            MathTex(tex, font_size=26).next_to(axes.c2p(0, val),LEFT, buff=0.15)
            for val, tex in zip(y_vals, y_tex)
        ])
        
        coordinates = VGroup(x_coords, y_coords).set_color(GREY_B)

        sin_graph = axes.plot(lambda x: np.sin(x), color=YELLOW, stroke_width=5)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED, stroke_width=5)
        
        # Swapped x for \theta in labels
        sin_label = MathTex(r"\sin x", font_size=34, color=YELLOW).next_to(
            axes.c2p(-5.2, np.sin(-5.2)), UP, buff=0.3)
        cos_label = MathTex(r"\cos x", font_size=34, color=RED).next_to(
            axes.c2p(-3.0, np.cos(-3.0)), DOWN, buff=0.2)

        self.play(LaggedStart(FadeIn(axes), FadeIn(coordinates), FadeIn(labels), lag_ratio=0.15), run_time=1.1)
        self.play(Write(title), Write(formula), rate_func=lambda t: smooth(1 - t),run_time=0.7)
        self.play(
            Create(sin_graph),
            FadeIn(sin_label, shift=RIGHT * 0.2),
            run_time=1.8,
        )
        self.play(
            Create(cos_graph),
            FadeIn(cos_label, shift=RIGHT * 0.2),
            run_time=1.8,
        )

        self.wait(0.5)

        sin_sq = axes.plot(lambda x: np.sin(x) ** 2, color=YELLOW, stroke_width=5)
        cos_sq = axes.plot(lambda x: np.cos(x) ** 2, color=RED, stroke_width=5)
        
        # Swapped x for \theta in squared labels
        sin_sq_label = MathTex(r"\sin^2 x", font_size=32, color=YELLOW).next_to(
            axes.c2p(-5.1, np.sin(-5.1) ** 2), UP, buff=0.3
        )
        cos_sq_label = MathTex(r"\cos^2 x", font_size=32, color=RED).next_to(
            axes.c2p(-2.8, np.cos(-2.8) ** 2), UP, buff=0.3
        )

        self.play(
            Transform(sin_graph, sin_sq),
            Transform(cos_graph, cos_sq),
            Transform(sin_label, sin_sq_label),
            Transform(cos_label, cos_sq_label),
            run_time=1.5,
        )

        one_line = axes.plot(lambda x: 1, color=BLUE, stroke_width=5)
        zero_line = axes.plot(lambda x: 0, color=GREY_C, stroke_width=2)
        fill = axes.get_area(one_line, x_range=[-TAU, TAU], bounded_graph=zero_line, color=BLUE, opacity=0.15)
        
        sum_label = MathTex("y", "=", "1", font_size=38)
        sum_label.next_to(axes.c2p(1, 1), UP, buff=0.18)
          
        self.play(FadeOut(sin_label), FadeOut(cos_label)) 
        self.play(Create(one_line), FadeIn(sum_label, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(fill), Create(zero_line), run_time=0.8)

        tracker = ValueTracker(-TAU)
        dot_sin = always_redraw(
            lambda: Dot(axes.c2p(tracker.get_value(), np.sin(tracker.get_value()) ** 2), color=YELLOW, radius=0.07)
        )
        dot_cos = always_redraw(
            lambda: Dot(axes.c2p(tracker.get_value(), np.cos(tracker.get_value()) ** 2), color=RED, radius=0.07)
        )
        dot_sum = always_redraw(
            lambda: Dot(axes.c2p(tracker.get_value(), 1), color=BLUE, radius=0.075)
        )
        vertical = always_redraw(
            lambda: DashedLine(
                axes.c2p(tracker.get_value(), 0),
                axes.c2p(tracker.get_value(), 1),
                color=WHITE,
                stroke_opacity=0.45,
                dash_length=0.08,
            )
        )
        
        # Converted radians to degrees for live display
        live_sum = always_redraw(
            lambda: VGroup(
                MathTex(rf"x = {tracker.get_value() * 180 / PI:.0f}^\circ", font_size=26, color=GREY_A),
            ).next_to(dot_sum, UP, buff=0.2)
        )
        
        # Wrapped in always_redraw and converted radians to degrees
        live_eq = always_redraw(
            lambda: (
                lambda eq: (
                    eq[0].set_color(YELLOW),
                    eq[1].set_color(BLUE),
                    eq[4].set_color(RED),
                    eq[5].set_color(BLUE),
                    eq[8].set_color(WHITE),
                    eq
                )[-1]
            )(
                MathTex(
                    r"\sin^2(",
                    rf"{tracker.get_value() * 180 / PI:.0f}^\circ",
                    r")",
                    "+",
                    r"\cos^2(",
                    rf"{tracker.get_value() * 180 / PI:.0f}^\circ",
                    r")",
                    "=",
                    "1",
                    font_size=44,
                ).next_to(axes, DOWN, buff=0.5)
            )
        )

        # NEW: Live evaluation showing the calculated float values summing to 1
        live_eval = always_redraw(
            lambda: (
                lambda eq: (
                    eq[1].set_color(YELLOW),
                    eq[3].set_color(RED),
                    eq[5].set_color(WHITE),
                    eq
                )[-1]
            )(
                MathTex(
                    r"\Rightarrow",
                    rf"{np.sin(tracker.get_value())**2:.2f}",
                    "+",
                    rf"{np.cos(tracker.get_value())**2:.2f}",
                    "=",
                    "1",
                    font_size=44,
                ).next_to(live_eq, DOWN, buff=0.35)
            )
        )
        
        self.play(
               FadeOut(sum_label),
               FadeIn(vertical),
               FadeIn(dot_sin),
               FadeIn(dot_cos),
               FadeIn(dot_sum),
               FadeIn(live_sum),
               FadeIn(live_eq),
               FadeIn(live_eval), # NEW: Fade in the evaluation tracker
               run_time=0.6
           )
           
        # Animate theta from -360° to 360°
        self.play(
               tracker.animate.set_value(TAU),
               run_time=8.2,
               rate_func=linear
           )

        final_eq = MathTex(
            r"\sin^2 x",
            "+",
            r"\cos^2 x",
            "=",
            "1",
            font_size=70
        ).move_to(UP*1)
        
        final_eq[0].set_color(YELLOW)  # sin²x
        final_eq[2].set_color(RED)     # cos²x
        final_eq[4].set_color(BLUE)    # 1
        
        # final_eq.move_to(UP*0.5)
        self.wait(0.5)   
        self.play(
               FadeOut(axes),
               FadeOut(coordinates),
               FadeOut(sin_graph),
               FadeOut(cos_graph),
               FadeOut(vertical),
               FadeOut(dot_sin),
               FadeOut(dot_cos),
               FadeOut(dot_sum),
               FadeOut(live_sum),
               FadeOut(live_eval), # NEW: Fade out the evaluation tracker
               FadeOut(one_line),
               FadeOut(zero_line),
               FadeOut(fill),
               FadeOut(y_label),
               FadeOut(x_label),
               FadeOut(live_eval),
               run_time=1.2
           )  
        self.play(ReplacementTransform(live_eq, final_eq),run_time=1.0) 
        # self.play(
        #        final_eq.animate.
        #        move_to(UP*1).
        #        scale(1.2),
        #        run_time=1
        #    )
           
        self.wait(1)