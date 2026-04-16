from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation


class CalculatorApp(App):
    def on_start(self):
        self.eq = ""
        self.root.ids.display.text = self.eq

    def update(self):
        self.eq = self.eq.replace("-", "−")
        self.eq = self.eq.replace("*", "×")
        self.eq = self.eq.replace("/", "÷")
        self.root.ids.display.text = self.eq

    def clear(self):
        self.eq = ""
        self.update()

    def backspace(self):
        eq_list = list(self.eq)
        eq_list = eq_list[:-1]
        self.eq = "".join(eq_list)  # list to str
        self.update()

    def press(self, value):

        operators = "+−×÷."
        if self.eq and self.eq[-1] in operators and value in operators:
            return

        oper = "+×÷"
        if not self.eq and value in oper:
            return

        self.eq = self.eq + value
        self.update()

    def show_error(self, message, sec, height=44):
        """Show floating error message for some seconds"""
        err = self.root.ids.error_label
        err.text = message
        err.height = height  # Show the label
        err.opacity = 1

        # bounce animation
        anim = Animation(
            pos_hint={'center_x': 0.5, 'top': 0.96},
            duration=0.2,
            t='out_bounce'
        )
        anim.start(err)

        # Auto hide after some seconds
        Clock.unschedule(self._hide_error)
        Clock.schedule_once(self._hide_error, sec)

    def _hide_error(self, *args):
        """Auto hide error after some seconds"""
        err = self.root.ids.error_label
        if err.height > 0:
            anim = Animation(opacity=0, duration=0.3)
            anim.bind(on_complete=lambda *x: setattr(err, 'height', 0))
            anim.start(err)

    def cal(self):

        self.eq = self.eq.replace("−", "-")
        self.eq = self.eq.replace("×", "*")
        self.eq = self.eq.replace("÷", "/")

        if self.eq == "":
            return

        if self.eq == "1491415/0":
            self.show_error(
                "Oops! Nino never taught me how to divide a number by zero", 5, 62)
            self.clear()
            return

        try:
            self.eq = str(eval(self.eq))
            self.update()
        except ZeroDivisionError:
            self.show_error("Can't divide by zero.", 3)
        except SyntaxError:
            self.show_error("Invalid format used.", 3)
        except Exception:
            self.show_error("Error", 3)


if __name__ == "__main__":
    CalculatorApp().run()
