from manim import *
import numpy as np

# Vertical Reel Format
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class PolarTracedReel(MovingCameraScene):
    def construct(self):
        # ── Background Plane ──────────────────────────────────────────────
        plane = PolarPlane(
            radius_max=3.0,
            size=7.5,
            azimuth_units="PI radians",
            background_line_style={
                "stroke_color": "#00E5FF",
                "stroke_width": 1.5,
                "stroke_opacity": 0.2,
            },
        )
        plane.scale(0.95).shift(UP * 1)

        # ── Title ─────────────────────────────────────────────────────────
        heading_B  = MathTex(r"\mathbb{B}", font_size=72,  color=WHITE).stretch(1.28, dim=1).set_stroke(width=1.6)
        heading_P1 = MathTex(r"\mathbb{P}", font_size=68,  color=WHITE).stretch(1.28, dim=1).set_stroke(width=1.6)
        heading_P2 = MathTex(r"\mathbb{P}", font_size=68,  color=WHITE).stretch(1.28, dim=1).set_stroke(width=1.6)

        text_eauty_of = Text("eauty of", font_size=58, color=WHITE, weight=LIGHT)
        text_olar     = Text("olar",     font_size=58, color=WHITE, weight=LIGHT)
        text_lane     = Text("lane",     font_size=58, color=WHITE, weight=LIGHT)

        word_1 = VGroup(heading_B,  text_eauty_of).arrange(RIGHT, buff=0.05, aligned_edge=UP)
        word_2 = VGroup(heading_P1, text_olar    ).arrange(RIGHT, buff=0.03, aligned_edge=UP)
        word_3 = VGroup(heading_P2, text_lane    ).arrange(RIGHT, buff=0.03, aligned_edge=UP)

        title_1 = VGroup(word_1, word_2, word_3).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title_1.to_edge(UP, buff=1.4)
        title_1.set_color_by_gradient("#ef4d38", "#f3af32")

        # ── Formula list ──────────────────────────────────────────────────
        formulas = [
            {
                "tex": r"r=0.6\left(e^{\sin\theta}-2\cos(4\theta)+\sin^5\left(\frac{2\theta-\pi}{24}\right)\right)",
                "func": lambda theta: 0.6 * (
                    np.exp(np.sin(theta))
                    - 2 * np.cos(4 * theta)
                    + np.sin((2 * theta - np.pi) / 24) ** 5
                ),
                "theta_max": 24 * PI,
                "color": "#FF00AA",
                "run":60,
            },
        ]

        # ── Opening animation ─────────────────────────────────────────────
        self.play(Write(title_1), FadeIn(plane, scale=0.9), run_time=2.5)

        title          = None
        previous_curve = None

        for item in formulas:
            func      = item["func"]
            theta_max = item["theta_max"]
            color     = item["color"]
            run_time  = item["run"]

            # ── Formula label ─────────────────────────────────────────────
            font_size  = 42 if color == "#FF00AA" else 62
            next_title = MathTex(item["tex"], color=color, font_size=font_size)
            next_title.next_to(plane, DOWN, buff=1.1)

            if title is None:
                self.play(Write(next_title), run_time=1)
            else:
                self.play(
                    ReplacementTransform(title, next_title),
                    FadeOut(previous_curve, scale=0.8, shift=DOWN * 0.5),
                    run_time=1,
                )

            tracker = ValueTracker(0.0)

            STEP = 0.003  
            def make_glow(tr, f, t_max, c):
                return always_redraw(lambda: ParametricFunction(
                    lambda t: plane.polar_to_point(f(t), t),
                    t_range=[0, max(tr.get_value(), 1e-4), STEP],
                    color=c,
                    stroke_width=14,
                    stroke_opacity=0.25,
                ))

            def make_core(tr, f, t_max):
                return always_redraw(lambda: ParametricFunction(
                    lambda t: plane.polar_to_point(f(t), t),
                    t_range=[0, max(tr.get_value(), 1e-4), STEP],
                    color=WHITE,
                    stroke_width=3,
                    stroke_opacity=1.0,
                ))

            glow_curve = make_glow(tracker, func, theta_max, color)
            core_curve = make_core(tracker, func, theta_max)

            # ── Leading dot + neon halo (position derived from tracker) ───
            def make_lead_dot(tr, f):
                return always_redraw(lambda: Dot(
                    point=plane.polar_to_point(f(max(tr.get_value(), 1e-4)),
                                               max(tr.get_value(), 1e-4)),
                    radius=0.07,
                    color=WHITE,
                    z_index=2,
                ))

            def make_halo(tr, f, c):
                return always_redraw(lambda: Circle(
                    radius=0.18,
                    color=c,
                    stroke_opacity=0.5,
                    stroke_width=5,
                ).move_to(plane.polar_to_point(f(max(tr.get_value(), 1e-4)),
                                               max(tr.get_value(), 1e-4))))

            lead_dot = make_lead_dot(tracker, func)
            lead_halo = make_halo(tracker, func, color)

            self.add(glow_curve, core_curve, lead_dot, lead_halo)

            start_pt = plane.polar_to_point(func(0), 0)
            self.camera.frame.save_state()
            self.play(
                self.camera.frame.animate.scale(0.15).move_to(start_pt),
                run_time=1.2,
                rate_func=smooth,
            )
            def make_cam_updater(tr, f):
                def updater(cam, dt):
                    theta   = max(tr.get_value(), 1e-4)
                    target  = plane.polar_to_point(f(theta), theta)
                    current = cam.get_center()
                    cam.move_to(current + (target - current) * min(1.0, dt * 6))
                return updater

            cam_updater = make_cam_updater(tracker, func)
            self.camera.frame.add_updater(cam_updater)

            self.play(
                tracker.animate.set_value(theta_max),
                run_time=run_time,
                rate_func=linear,
            )

            self.camera.frame.remove_updater(cam_updater)
            self.play(Restore(self.camera.frame), run_time=1.5, rate_func=smooth)


            self.remove(glow_curve, core_curve, lead_dot, lead_halo)

            static_glow = ParametricFunction(
                lambda t, f=func: plane.polar_to_point(f(t), t),
                t_range=[0, theta_max, STEP],
                color=color,
                stroke_width=0,
                stroke_opacity=0.25,
            )
            static_core = ParametricFunction(
                lambda t, f=func: plane.polar_to_point(f(t), t),
                t_range=[0, theta_max, STEP],
                color=WHITE,
                stroke_width=0.9,
                stroke_opacity=1.0,
            )
            finished_curve = VGroup(static_glow, static_core)
            self.add(finished_curve)

            self.wait(0.5)

            title          = next_title
            previous_curve = finished_curve

        final_group = VGroup(plane, previous_curve)
        self.play(
            final_group.animate.scale(1.1),
            run_time=2,
            rate_func=there_and_back,
        )
        self.wait(1)