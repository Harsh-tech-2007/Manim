from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK


class FamousComparison(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        WHITE = "#FFFFFF"
        MUTED = "#94A3B8"
        GREEN_1 = "#22C55E"
        GREEN_2 =  "#29EBD1"
        GREEN_3 = "#0ABB86"
        BLUE = "#32BFFC"
        AMBER = "#FBBF24"

        def eq(tex, size=78, color=WHITE):
            mob = MathTex(tex, font_size=size, color=color)
            mob.set_max_width(config.frame_width - 0.75)
            return mob

        def note(text, size=32, color=MUTED):
            mob = Text(text, font_size=size, color=color, weight=MEDIUM)
            mob.set_max_width(config.frame_width - 0.8)
            return mob

        def step(action, formula, size=74):
            return VGroup(
                note(action, 30),
                eq(formula, size),
            ).arrange(DOWN, buff=0.42,center=True,aligned_edge=ORIGIN)

        heading_h = MathTex(
            r"\mathbb{W}",
            font_size=70,
            color=WHITE,
        )
        
        # Elegant tall serif look
        heading_h.stretch(1.28, dim=1)
        
        # Slightly thinner appearance
        heading_h.set_stroke(width=1.6)
        
        heading_text = Text(
            "hich One Is Larger?",
            font_size=60,
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
        title.move_to(UP*1)
        title.set_color_by_gradient("#ec6958", "#f3b541")
        steps = [

            eq(r"e^{\pi}\quad \text{or}\quad \pi^e", 90),
            step("Take natural logarithms", r"\ln(e^{\pi})\quad \text{vs}\quad \ln(\pi^e)", 72),
            step("Bring the exponents down", r"\pi\ln(e)\quad \text{vs}\quad e\ln(\pi)", 72),
            
            step("Divide both sides by e and π        ", r"\frac{\ln(e)}{e}\quad \text{vs}\quad \frac{\ln(\pi)}{\pi}", 82),
            step("                         \n                 Using ln(e) = 1  ", r"\frac{1}{e}\quad \text{vs}\quad \frac{\ln(\pi)}{\pi}", 82),
            step("   Now compare the function\n          at  x = e and x = π", r"f(x)=\frac{\ln x}{x}", 88),
            VGroup(
                note("   Differentiate the function", 29),
                eq(r"f'(x)=\frac{x\cdot\frac1x-\ln x}{x^2}", 62),
                eq(r"f'(x)=\frac{1-\ln x}{x^2}", 72),
            ).arrange(DOWN, buff=0.6,center=True,aligned_edge=ORIGIN),
            VGroup(
                note("Set the derivative equal to zero", 29),
                eq(r"f'(x)=0", 74),
                eq(r"1-\ln x=0", 70),
                eq(r"x=e",100, GREEN_1).shift(DOWN*1.5),
            ).arrange(DOWN, buff=0.5,center=True,aligned_edge=ORIGIN),
            VGroup(
                note("The sign changes at e", 29),
                eq(r"x<e\Rightarrow f'(x)>0", 60, GREEN_1),
                eq(r"x>e\Rightarrow f'(x)<0", 60, AMBER),
            ).arrange(DOWN, buff=0.34,center=True,aligned_edge=ORIGIN),
            step("Therefore,the function attains \n          its maximum at e", r"f(e)>f(\pi)", 74),
            step("That means                                       ", r"\frac{1}{e}>\frac{\ln(\pi)}{\pi}", 82),
        ]

        answer = eq(r"e^{\pi}>\pi^e", 118)
        answer.set_color_by_gradient(GREEN_1, GREEN_2)
        steps.append(answer)

        self.play(FadeIn(title),title.animate.to_edge(UP, buff=1.25), run_time=1.1)
        
        current = steps[0].move_to(UP*0.5)
        self.play(Write(current), run_time=1.0)
        self.play(FadeOut(title),run_time=0.45)  
        # self.wait(0.25)

        for i, nxt in enumerate(steps[1:], start=1):
            nxt.move_to(UP*0.5)
            self.play(
                ReplacementTransform(current, nxt),
                run_time=0.8,
                rate_func=smooth,
            )
            current = nxt
            self.wait(0.65)

            if i == 8:
                self.show_graph(current, BLUE, GREEN_1, AMBER, WHITE, MUTED)
         
        answer_box = SurroundingRectangle(
            current,
            buff=0.25,
            corner_radius=0.18,
            stroke_width=6,
        )
        answer_box.set_color_by_gradient(GREEN_1, GREEN_2) 
        self.play(answer.animate.scale(1.12), run_time=0.2)
        self.play(Create(answer_box),answer.animate.scale(1 / 1.12), run_time=0.8)
        self.wait(1.8)

    def show_graph(self, current, blue, green, amber, white, muted):
        self.play(current.animate.shift(UP * 2.0).scale(0.78), run_time=0.5)

        graph = self.make_graph(blue, green, amber, white, muted)
        graph.shift(DOWN * 1)

        self.play(Create(graph[0]), Create(graph[1]), run_time=1.0)
        self.play(FadeIn(graph[2:]), run_time=0.65)
        self.wait(1.2)
        self.play(
            FadeOut(graph),
            current.animate.shift(DOWN * 1.8).scale(1 / 0.78),
            run_time=0.55,
        )

    def make_graph(self, blue, green, amber, white, muted):
        axes = Axes(
            x_range=[1, 4.15, 0.5],
            y_range=[0, 0.42, 0.1],
            x_length=6.35,
            y_length=3.0,
            axis_config={
                "stroke_width": 2,
                "color": WHITE,
                "include_tip": True,
                "tip_shape":StealthTip,
                "tip_length":0.25,
                "include_numbers":False,  
            },   
        )
        labels = axes.get_axis_labels(
            Tex("x").scale(0.7), Text("y").scale(0.45))
        curve = axes.plot(
            lambda x: np.log(x) / x,
            x_range=[1.02, 4.05],
            color=blue,
            stroke_width=5,
        )

        e_point = axes.c2p(np.e, 1 / np.e)
        pi_point = axes.c2p(np.pi, np.log(np.pi) / np.pi)

        e_line = DashedLine(axes.c2p(np.e, 0), e_point, color=green, stroke_width=2.5)
        pi_line = DashedLine(axes.c2p(np.pi, 0), pi_point, color=amber, stroke_width=2.5)
        e_dot = Dot(e_point, color=green, radius=0.085)
        pi_dot = Dot(pi_point, color=amber, radius=0.085)

        e_label = MathTex("e", font_size=36, color=green).next_to(axes.c2p(np.e, 0), DOWN, buff=0.16)
        pi_label = MathTex(r"\pi", font_size=36, color=amber).next_to(axes.c2p(np.pi, 0), DOWN, buff=0.16)
        y_label = MathTex(r"f(x)=\frac{\ln x}{x}", font_size=42, color=white).next_to(axes, DOWN, buff=0.35)

        e_value = MathTex(r"f(e)", font_size=34, color=green).next_to(e_dot, UP, buff=0.16)
        pi_value = MathTex(r"f(\pi)", font_size=34, color=amber).next_to(pi_dot, UP, buff=0.16)

        return VGroup(
            axes,
            curve,
            labels,
            e_line,
            pi_line,
            e_dot,
            pi_dot,
            e_label,
            pi_label,
            y_label,
            e_value,
            pi_value,

        )
