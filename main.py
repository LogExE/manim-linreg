from manim import *
from manim.utils.unit import *


config['tex_template'] = TexTemplate(preamble=r'''
\usepackage[T2A]{fontenc}
\usepackage[english, russian]{babel}
\usepackage{amsmath}''')

class LinReg(Scene):
    def title(self):
        mnk = Tex("М", "Н", "К")
        self.play(FadeIn(mnk))
        self.wait(2)
        self.play(mnk.animate.shift(UP))
        g = Tex("Метод ", "Наименьших ", "Квадратов")
        self.play(
            AnimationGroup(
                ReplacementTransform(mnk[0], g[0]),
                ReplacementTransform(mnk[1], g[1]),
                ReplacementTransform(mnk[2], g[2]),
                lag_ratio=0.5,
                run_time=3,
            )
        )
        self.wait()
        linreg = Text("Линейная регрессия").move_to(DOWN)
        self.play(Write(linreg))
        self.play(Indicate(linreg))

        self.play(FadeOut(g), FadeOut(linreg))
        self.wait()
        self.clear()

    def regr(self):
        x_vals = ["x_i"] + [f"x_{i}" for i in range(2)] + ["\ldots"] + ["x_n"]
        y_vals = ["y_i"] + [f"y_{i}" for i in range(2)] + ["\ldots"] + ["y_n"]
        t1 = MathTable([x_vals, y_vals]).shift(4 * LEFT)
        t1.width = 40 * Percent(X_AXIS)
        uptext = (
            Text("Наблюдаемые значения").next_to(t1, UP).scale_to_fit_width(t1.width)
        )

        ax = Axes(
                x_range=[-1, 15, 1],
                y_range=[-1, 15, 1],
                x_length=50 * Percent(X_AXIS),
                axis_config={'tip_shape': StealthTip}
        ).shift(3 * RIGHT)
        xylabel = ax.get_axis_labels(MathTex("x"), MathTex("y"))

        self.play(Create(uptext), Create(t1), Create(ax), Create(xylabel))
        self.play(ApplyWave(uptext))

        def attach_coords(coords, col):
            xyobj = t1.get_columns()[col].copy()
            x, y = coords
            self.play(
                xyobj[0].animate.move_to(ax.coords_to_point(x, -1)),
                xyobj[1].animate.move_to(ax.coords_to_point(-1, y)),
            )

        def create_lines(point):
            return (ax.get_horizontal_line(point),
                    ax.get_vertical_line(point))
        
        def show_dot(coords, show_lines=True):
            point = ax.coords_to_point(*coords)
            dot = Dot(radius=0.04).move_to(point)
            if show_lines:
                h, v = create_lines(point)
                self.play(Succession(Create(VGroup(h, v)), Create(dot)))
                self.play(Uncreate(h), Uncreate(v))
            else:
                self.play(Create(dot))
            self.wait()



        def make_full(coords, col):
            rect = SurroundingRectangle(t1.get_columns()[col])
            self.play(Create(rect), run_time=2)
            self.wait()
            attach_coords(coords, col)
            self.wait()
            show_dot(coords)
            self.wait()
            self.play(Uncreate(rect))

        def create_line(p1, p2):
            return Line(ax.coords_to_point(*p1), ax.coords_to_point(*p2))

        lcoords = [(1, 2), (6, 8), (5, 1), (3, 3), (11, 10), (4, 9), (14, 7)]

        # first two
        make_full(lcoords[0], 1)
        make_full(lcoords[1], 2)

        # ...
        rect = SurroundingRectangle(t1.get_columns()[3])
        self.play(Create(rect), run_time=2)
        self.wait()
        for i, point in enumerate(lcoords[2:-1]):
            show_dot(point, i <= 1)
        self.play(Uncreate(rect))
        self.wait()

        # last
        make_full(lcoords[-1], 4)
        
        line1_fun = lambda x: x / 3 + 4
        line1 = ax.plot(line1_fun, x_range=[0, 15]).set_color(RED)
        text_label = Tex(r'Уравнение прямой\\', r'$y = a \cdot x + b$')
        line1_label = ax.get_graph_label(line1, label=text_label, direction=3 * UP + RIGHT)
        line1_label.set_color(WHITE)
        self.play(Create(line1), Create(line1_label))
        self.play(ApplyWave(text_label[0]))
        self.wait()
        
        spaces = [r"\hat{y_i}"] + ["-", "-", r"\ldots", "-"]
        t2 = MathTable([x_vals, y_vals, spaces]).shift(4 * LEFT)
        t2.width = 40 * Percent(X_AXIS)
        self.play(ReplacementTransform(t1, t2), uptext.animate.next_to(t2, UP))

        for i, coords in enumerate(lcoords):
            proj = (coords[0], line1_fun(coords[0]))
            point = ax.coords_to_point(*proj)
            h, v = create_lines(point)
            red_dot = Dot(radius=0.06, color=RED).move_to(point)
            red_dot.set_z_index(abs(line1.z_index) + abs(h.z_index) + abs(v.z_index) + 1)
            self.play(Succession(Create(v), Create(red_dot), Create(h)))
            if i <= 1 or i == len(lcoords) - 1:
                if i <= 1:
                    y_hat = MathTex(r'\hat{y_%d}' % i)
                else:
                    y_hat = MathTex(r'\hat{y_n}')
                y_hat.move_to(ax.coords_to_point(-1, line1_fun(coords[0])))
                self.play(Create(y_hat))
            diff = Line(ax.coords_to_point(*coords), point, color=BLUE)
            self.play(Create(diff), Uncreate(h), Uncreate(v))
            if i <= 1 or i == len(lcoords) - 1:
                if i <= 1:
                    i += 2
                else:
                    i = 5
                self.play(y_hat.animate.move_to(t2.get_entries((3, i))))
                self.play(ReplacementTransform(t2.get_entries((3, i)), y_hat))
        self.wait()

    def construct(self):
        self.title()
        self.regr()
