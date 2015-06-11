from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock



class Electron(Widget):
    score = NumericProperty(0)
    record = NumericProperty(0)

class RaceGame(Widget):
    ball = ObjectProperty(None)
    magnes = ObjectProperty(None)
    move = NumericProperty(0)
    first_draw = NumericProperty(0)


    def update(self, dt):
        if self.first_draw == 0:
            self.ball.center_x = self.center_x
            self.first_draw = 1
        self.ball.center_y = self.center_y * 1/10
        self.ball.score += 1
        if self.move == 1 and self.ball.center_x > self.width - self.width + 25:
            self.ball.center_x -= 5
        elif self.move == 2 and self.ball.center_x < self.width - 25:
            self.ball.center_x += 5
        pass

    def on_touch_down(self, touch):
        if touch.x < self.width / 2 and self.ball.center_x > self.width - self.width + 25:
            self.move = 1
        if touch.x > self.width / 2 and self.ball.center_x < self.width - 25:
            self.move = 2

    def on_touch_up(self, touch):
        self.move = 0

"""
    def on_touch_move(self, touch):

        if touch.x < self.width / 2 and self.ball.center_x > self.width - self.width + 25:
            self.ball.center_x -= 5
        if touch.x > self.width / 2 and self.ball.center_x < self.width - 25:
            self.ball.center_x += 5
"""
class RaceApp(App):
    def build(self):
        game = RaceGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    RaceApp().run()