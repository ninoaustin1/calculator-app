"""
All GUI is defined in samsung_calculator.kv.
Python responsibilities:
  - animate_button : ripple animation (added on top of the provided logic)
  - on_button_press: entry point — fires ripple then routes to the right method
  - update         : format eq string and push to display
  - clear          : C button
  - backspace      : << button
  - press          : digits / operators / decimal
  - cal            : = button  (eval with friendly error messages)
  - animate_error  : fade-in / hold / fade-out floating error label
  - error_drag_*   : drag handlers so the error label can be moved freely
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation


class CalculatorApp(App):

    def on_start(self):
        self.eq = ""
        self.root.ids.display.text = self.eq

    # ── Button ripple animation ───────────────────────────────────────────────

    def animate_button(self, btn):
        touch = btn.last_touch
        if touch is None:
            return
        r = btn.ids._ripple
        max_r = max(btn.width, btn.height) * 0.8
        r.size = (2, 2)
        r.pos = (touch.x - 1, touch.y - 1)
        r.opacity = 1.0
        Animation(
            size=(max_r * 2, max_r * 2),
            pos=(touch.x - max_r, touch.y - max_r),
            opacity=0,
            duration=0.38,
            t="out_quad",
        ).start(r)

    # ── Entry point by NINO ──────────────

    def on_button_press(self, btn):
        self.animate_button(btn)
        text = btn.text
        if text == "C":
            self.clear()
        elif text == "<<":
            self.backspace()
        elif text == "=":
            self.cal()
        elif text == "x²":
            self._square()
        elif text == "%":
            self._percent()
        else:
            self.press(text)

    # ── Calculator logic by NINO──────────────────────────────────────────────────────

    def update(self):
        self.eq = self.eq.replace("-", "−")
        self.eq = self.eq.replace("*", "×")
        self.eq = self.eq.replace("/", "÷")
        self.root.ids.display.text = self.eq

    def clear(self):
        self.eq = ""
        self.update()

    def backspace(self):
        self.eq = list(self.eq)[:-1]
        self.eq = "".join(self.eq)
        self.update()

    def press(self, value):
        operators = "+−×÷."
        if self.eq and self.eq[-1] in operators and value in operators:
            return
        if not self.eq and value in "+×÷":
            return
        self.eq = self.eq + value
        self.update()

    def _square(self):
        try:
            safe = (
                self.eq
                .replace("−", "-")
                .replace("×", "*")
                .replace("÷", "/")
            )
            result = eval(safe) ** 2
            result = int(result) if result == int(result) else result
            self.eq = str(result)
            self.update()
        except Exception:
            self.animate_error("Invalid expression")

    def _percent(self):
        try:
            safe = (
                self.eq
                .replace("−", "-")
                .replace("×", "*")
                .replace("÷", "/")
            )
            result = eval(safe) / 100
            result = int(result) if result == int(result) else result
            self.eq = str(result)
            self.update()
        except Exception:
            self.animate_error("Invalid expression")

    def cal(self):
        self.eq = self.eq.replace("−", "-")
        self.eq = self.eq.replace("×", "*")
        self.eq = self.eq.replace("÷", "/")

        if self.eq == "":
            return

        if self.eq == "1491415/0":
            self.clear()
            self.animate_error(
                "Oops! Nino never taught me how to divide a number by zero")
            return

        try:
            self.eq = str(eval(self.eq))
            self.update()
        except ZeroDivisionError:
            self.animate_error("Can't divide by zero.")
        except SyntaxError:
            self.animate_error("Invalid format used.")
        except Exception:
            self.animate_error("Error")

    # ── Floating error label ──────────────────────────────────────────────────

    def animate_error(self, message="Error"):
        lbl = self.root.ids.error_label
        lbl.text = message
        Animation.cancel_all(lbl)
        (
            Animation(opacity=1, duration=0.20)
            + Animation(opacity=1, duration=2.35)
            + Animation(opacity=0, duration=0.35)
        ).start(lbl)

    def error_drag_start(self, label, touch):
        if label.opacity > 0 and label.collide_point(*touch.pos):
            label._drag_dx = touch.x - label.x
            label._drag_dy = touch.y - label.y
            label._dragging = True

    def error_drag_move(self, label, touch):
        if getattr(label, "_dragging", False):
            label.pos = (touch.x - label._drag_dx, touch.y - label._drag_dy)

    def error_drag_end(self, label, touch):
        label._dragging = False


if __name__ == "__main__":
    CalculatorApp().run()
