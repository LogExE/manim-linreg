from manim import *
from manim.utils.unit import *

def fix_tex():
    config['tex_template'] = TexTemplate(preamble=r'''
        \usepackage[T2A]{fontenc}
        \usepackage[english, russian]{babel}
        \usepackage{amsmath}
        \usepackage{amssymb}''')


class LinRegIntro(Scene):
    def construct(self):
        fix_tex()

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
        self.wait()

class LinRegTask(Scene):
    def construct(self):
        fix_tex()
        
        x_vals = ["x_i"] + [f"x_{i}" for i in range(2)] + ["\ldots"] + ["x_n"]
        y_vals = ["y_i"] + [f"y_{i}" for i in range(2)] + ["\ldots"] + ["y_n"]
        data_table = MathTable([x_vals, y_vals]).shift(4 * LEFT)
        data_table.scale_to_fit_width(40 * Percent(X_AXIS))
        uptext = Text("Наблюдаемые значения")
        uptext.add_updater(lambda mob: mob
                           .next_to(data_table, UP)
                           .scale_to_fit_width(data_table.width))

        ax = Axes(
                x_range=[-1, 15, 1],
                y_range=[-1, 15, 1],
                x_length=50 * Percent(X_AXIS),
                axis_config={'tip_shape': StealthTip}
        ).shift(3 * RIGHT)
        xylabel = ax.get_axis_labels(MathTex("x"), MathTex("y"))

        self.play(Create(uptext), Create(data_table), Create(ax), Create(xylabel))
        self.play(ApplyWave(uptext))

        def attach_coords(coords, col):
            xyobj = data_table.get_columns()[col].copy()
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
            rect = SurroundingRectangle(data_table.get_columns()[col])
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
        rect = SurroundingRectangle(data_table.get_columns()[3])
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
        data_table_mod = MathTable([x_vals, y_vals, spaces]).shift(4 * LEFT)
        data_table_mod.scale_to_fit_width(40 * Percent(X_AXIS))
        self.play(ReplacementTransform(data_table, data_table_mod))

        formula = MathTex(r'\hat{y_i} = a \cdot x_i + b')
        formula.next_to(ax, DOWN)
        self.play(FadeIn(formula))

        i_brace = 2
        for i, coords in enumerate(lcoords):
            proj = (coords[0], line1_fun(coords[0]))
            point = ax.coords_to_point(*proj)
            h, v = create_lines(point)
            red_dot = Dot(radius=0.06, color=RED).move_to(point)
            red_dot.set_z_index(1)
            self.play(Succession(Create(v), Create(red_dot), Create(h)))
            if i <= 1 or i == len(lcoords) - 1:
                if i <= 1:
                    y_hat = MathTex(r'\hat{y_%d}' % i)
                    entry = data_table_mod.get_entries((3, i + 2))
                else:
                    y_hat = MathTex(r'\hat{y_n}')
                    entry = data_table_mod.get_entries((3, 5))
                #y_hat[0].scale_to_fit_width(entry)
                y_hat.move_to(ax.coords_to_point(-1, line1_fun(coords[0])))
                self.play(Create(y_hat))
            diff = Line(ax.coords_to_point(*coords), point, color=BLUE)
            self.play(Create(diff), Uncreate(h), Uncreate(v))
            if i == i_brace:
                brace = Brace(diff, direction=RIGHT)
                br_text = brace.get_tex('|\hat{y_i} - y_i|')
                self.play(Create(brace), Write(br_text))
            if i <= 1 or i == len(lcoords) - 1:
                self.play(y_hat.animate.move_to(entry))
                self.play(Transform(entry, y_hat))
                self.remove(y_hat)
        self.wait()

        y_hat_text = Text('Теоретические значения')
        y_hat_text.scale_to_fit_width(data_table_mod.width).next_to(data_table_mod, DOWN)
        y_hat_group = VGroup(y_hat_text, data_table_mod.get_rows()[2])
        self.play(Succession(Create(y_hat_text), Indicate(y_hat_group)))
        self.wait()

        task = Tex(r'Задача:\\', r'$S(a, b) = \sum\limits_{i=1}^{n}(\hat{y_i} - y_i)^2 \rightarrow \min$')
        task.scale_to_fit_width(data_table_mod.width).next_to(y_hat_text, DOWN)
        self.play(Write(task))
        self.wait()

class LinRegMain(Scene):
    def construct(self):
        fix_tex()

        task = Tex(r'Задача:\\', r'$S(a, b) = \sum\limits_{i=1}^{n}(\hat{y_i} - y_i)^2 \rightarrow \min$')
        self.add(task)
        self.wait()

        eq1 = MathTex(r'S(a, b) = \sum\limits_{i=1}^{n}(\hat{y_i} - y_i)^2')
        eq1.move_to(3 * UL)
        self.play(ReplacementTransform(task, eq1))
        self.wait()
        expr1 = MathTex(r' = \sum\limits_{i=1}^{n}(\hat{y_i} - y_i)^2').next_to(eq1)
        self.play(Write(expr1))
        expr2 = MathTex(r' = \sum\limits_{i=1}^{n}(a \cdot x + b - y_i)^2').next_to(eq1)
        self.play(Transform(expr1, expr2))
        self.wait()

        note1 = Text("Решим систему:").next_to(eq1, DOWN).scale(0.8)
        self.play(Write(note1))

        sys1 = MathTex(r"""\begin{cases}
        S'(a) = 0\\
        S'(b) = 0
        \end{cases}""").next_to(note1, 2 * DOWN).align_to(note1, LEFT)
        self.play(Create(sys1))
        self.wait()

        sys2 = MathTex(r"""\Leftrightarrow\begin{cases}
        \sum\limits_{i=1}^{n}{2 \cdot (a \cdot x_i + b - y_i) \cdot x_i} = 0\\
        \sum\limits_{i=1}^{n}{2 \cdot (a \cdot x_i + b - y_i) \cdot 1} = 0
        \end{cases}""").next_to(sys1)
        self.play(Create(sys2))
        self.wait()

        sys3 = MathTex(r"""\Leftrightarrow\begin{cases}
        a \cdot \sum x_i^2 + b \cdot \sum x_i = \sum{x_i \cdot y_i}\\
        a \cdot \sum x_i + b \cdot n = \sum y_i
        \end{cases}""").next_to(sys2, 1.5 * DOWN).align_to(note1, LEFT)
        self.play(Create(sys3))
        self.wait()

        self.play(FadeOut(eq1), FadeOut(expr1), FadeOut(note1), FadeOut(sys1), FadeOut(sys2))
        self.play(sys3.animate.move_to(2 * UP))
        self.wait()

        note2 = Text('Решим систему методом Крамера:').next_to(sys3, DOWN).scale(0.8)
        self.play(Write(note2))
        self.wait()

        vars = MathTex(r'a=\dfrac{\Delta_a}{\Delta},\ b=\dfrac{\Delta_b}{\Delta}')
        vars.next_to(note2, DOWN)
        self.play(Write(vars))

        det1 = MathTex(r'''
        \Delta=\left|\begin{array}{lr}
        \sum x_i^2 & \sum x_i\\
        \sum x_i & n
        \end{array}\right|,\
        ''')
        det2 = MathTex(r'''
        \Delta_a=\left|\begin{array}{lr}
        \sum{x_i \cdot y_i} & \sum x_i\\
        \sum y_i & n
        \end{array}\right|,\ 
        ''')
        det12 = VGroup(det1, det2).arrange().next_to(vars, DOWN)
        det3 = MathTex(r'''
        \Delta_b=\left|\begin{array}{lr}
        \sum{x_i^2} & \sum{x_i \cdot y_i}\\
        \sum x_i & \sum y_i
        \end{array}\right|.
        ''').next_to(det12, DOWN)
        self.play(Succession(Write(det12), Write(det3)))
        self.wait()

        self.play(Indicate(vars))
        self.wait()
