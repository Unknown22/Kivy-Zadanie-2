from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random

class Magnes(Widget):
    narysowany = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(-3)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    pozycja_x = NumericProperty(0)
    pozycja_y = NumericProperty(0)
    pozycja = ReferenceListProperty(pozycja_x, pozycja_y)
    def move_obstacle(self, race):
        if self.narysowany == 0:
            self.pos = (random.randrange(race.width), race.height)
            self.size = (race.width * 3/10, race.height * 2/10)
            self.narysowany = 1
        self.pos = Vector(*self.velocity) + self.pos
        self.pozycja = self.pos
        if self.pozycja_y + self.height < 0:
            self.narysowany = 0

class Electron(Widget):
    score = NumericProperty(0)
    record = NumericProperty(0)

class RaceGame(Widget):
    ball = ObjectProperty(None)
    magnes = ObjectProperty(None)
    move = NumericProperty(0)
    first_draw = NumericProperty(0)
    first_draw_magnes2 = NumericProperty(0)
    first_draw_magnes3 = NumericProperty(0)

    def update(self, dt):

        Magnes.move_obstacle(self.magnes1, self)
        if self.magnes1.pozycja_y + self.magnes1.height / 2 < self.height * 2/3 or self.first_draw_magnes2 == 1:
            Magnes.move_obstacle(self.magnes2, self)
            self.first_draw_magnes2 = 1
            if self.magnes2.pozycja_y + self.magnes2.height / 2 < self.height * 2/3 or self.first_draw_magnes3 == 1:
              Magnes.move_obstacle(self.magnes3, self)
              self.first_draw_magnes3 = 1

        if self.first_draw == 0:
            self.ball.score = 0
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