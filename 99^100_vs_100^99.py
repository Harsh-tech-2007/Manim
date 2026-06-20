from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK


class PowerComparison(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        gold = "#dfca0c"

        def eq(tex, size=58, color=WHITE):
            return MathTex(tex, font_size=size, color=color)
        
        heading_h = MathTex(
            r"\mathbb{W}",
            font_size=70,
            color=WHITE,
        )
        heading_h.stretch(1.28, dim=1)
        heading_h.set_stroke(width=1.6)
        
        heading_text = Text(
            "hich One Is Larger?",
            font_size=60,
            color=WHITE,
            weight=LIGHT,
        )
        
        heading = VGroup(
            heading_h,
            heading_text
        ).arrange(
            RIGHT,
            buff=0,
            aligned_edge=UP
        )
        
        heading.to_edge(UP, buff=0.75)
        heading.set_color_by_gradient("#f86e5b", "#f3b645")
        final_answer = eq(r"99^{100}>100^{99}", 86)
        final_answer.set_color_by_gradient("#00ff87", "#60efff")

        steps = [
            eq(r"99^{100}\quad ?\quad 100^{99}", 82),
            eq(r"99^{100}=99^{99}\cdot 99", 72),
            eq(
                r"100^{99}=99^{99}\left(\frac{100}{99}\right)^{99}",
                58,
            ),
            eq(
                r"99\quad ?\quad \left(\frac{100}{99}\right)^{99}",
                70,
            ),
            eq(
                r"\left(\frac{100}{99}\right)^{99}"
                r"=\left(1+\frac1{99}\right)^{99}",
                60,
            ),
            eq(r"\left(1+\frac1{99}\right)^{99}<e<3", 70),
            eq(r"\left(\frac{100}{99}\right)^{99}<3", 72),
            eq(r"99>3", 78),
            VGroup(
                eq(r"99>\left(\frac{100}{99}\right)^{99}", 70),
                eq(
                    r"99^{99}\cdot99>"
                    r"99^{99}\left(\frac{100}{99}\right)^{99}",
                    54,
                ),
            ).arrange(DOWN, buff=0.5),
            final_answer,
        ]

        current = steps[0].move_to(ORIGIN)
        self.play(
            Write(heading),
            Write(current),
            run_time=1.0,
        )
        self.wait(0.8)
        self.play(FadeOut(heading), run_time=0.45)

        for next_step in steps[1:]:
            next_step.move_to(ORIGIN)
            self.play(ReplacementTransform(current, next_step), run_time=0.9)
            self.wait(0.85)
            current = next_step

        answer_box = SurroundingRectangle(
            current,
            color=gold,
            buff=0.25,
            corner_radius=0.18,
            stroke_width=6,
        )

        answer_box.set_color_by_gradient("#00ff87", "#59fac2")

        self.play(Create(answer_box), run_time=0.8)
        self.wait(1.4)
