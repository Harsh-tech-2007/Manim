from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60
config.background_color = BLACK


class comparison(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        gold = "#dfca0c"

        def eq(tex, size=58, color=WHITE):
            return MathTex(
                tex,
                font_size=size,
                color=color
            )
        final_answer = eq(r"x=256", 90)

        final_answer.set_color_by_gradient(
            "#00ff87",
            "#60efff"
        )
        instruction = VGroup(
            Text("Rewrite the left side in the form",font_size=34,color=WHITE),
            MathTex(r"x^{\frac1x}",font_size=54,color=WHITE)).arrange(RIGHT, buff=0.18)
       
        steps = [
            eq(r"2^x=x^{32}", 82),
            eq(r"\left(2^x\right)^{\frac1{32x}}=" r"\left(x^{32}\right)^{\frac1{32x}}",60),
            eq(r"2^{\frac1{32}}=x^{\frac1x}", 74),
            instruction,
            eq(r"2^{\frac1{32}}=2^{\frac8{256}}", 74),
            eq( r"2^{\frac8{256}}=" r"\left(2^8\right)^{\frac1{256}}",66),
            eq(r"\left(2^8\right)^{\frac1{256}}=" r"256^{\frac1{256}}",66),
            eq(r"x^{\frac1x}=256^{\frac1{256}}", 74),
            final_answer ,
        ]

        current = steps[0].move_to(ORIGIN)
        self.play(Write(current),run_time=1.0)
        self.wait(0.8)

        for next_step in steps[1:]:
            next_step.move_to(ORIGIN)
            self.play(ReplacementTransform(current, next_step),run_time=0.9)
            self.wait(0.85)
            current = next_step


        answer_box = SurroundingRectangle(
            current,
            color=gold,
            buff=0.25,
            corner_radius=0.18,
            stroke_width=6,
        )

        answer_box.set_color_by_gradient(
            "#00ff87",
            "#59fac2"
        )

        self.play(
            Create(answer_box),
            run_time=0.8
        )
        self.wait(1.4)