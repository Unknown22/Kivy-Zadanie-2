from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random
from kivy.uix.image import Image

class Magnes(Widget):
    narysowany = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(-3)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    pozycja_x = NumericProperty(0)
    pozycja_y = NumericProperty(0)
    pozycja = ReferenceListProperty(pozycja_x, pozycja_y)
    magnet_image = ObjectProperty(Image())

    def przyspiesz(self):
        self.velocity_y -= 1

    def wyczysc(self, race):
        self.narysowany = 0
        self.pos = (random.randrange(race.width),race.height)
        self.velocity_y = -3

    def zderzenie(self, ball, race):
        if self.collide_widget(ball):
            self.narysowany = 0
            self.pos = (random.randrange(race.width),race.height)
            self.velocity_y = -3
            return True

    def move_obstacle(self, race):
        if self.narysowany == 0:
            self.pos = (random.randrange(race.width), race.height)
            self.size = (race.width * 4/10, race.height * 1/10)
            self.narysowany = 1
        self.pos = Vector(*self.velocity) + self.pos
        self.pozycja = self.pos
        if self.pozycja_y + self.height < 0:
            self.narysowany = 0

class Electron(Widget):
    score = NumericProperty(0)
    record = NumericProperty(0)
    electron_image = ObjectProperty(Image())

class RaceGame(Widget):
    ball = ObjectProperty(None)
    magnes1 = ObjectProperty(None)
    magnes2 = ObjectProperty(None)
    magnes3 = ObjectProperty(None)
    move = NumericProperty(0)
    first_draw = NumericProperty(0)
    first_draw_magnes2 = NumericProperty(0)
    first_draw_magnes3 = NumericProperty(0)
    przyspieszenie_kulki = NumericProperty(5)
    przyrost_odleglosci = NumericProperty(1)
    poziom_przyspieszenia = NumericProperty(0)
    prog_przyspieszenia = NumericProperty(500)

    def update(self, dt):
        if self.ball.score > self.prog_przyspieszenia + 1000 * self.poziom_przyspieszenia and self.poziom_przyspieszenia < 18:
            self.prog_przyspieszenia += 2000 * self.poziom_przyspieszenia
            self.magnes1.przyspiesz()
            self.magnes2.przyspiesz()
            self.magnes3.przyspiesz()
            self.poziom_przyspieszenia += 1
            self.przyrost_odleglosci += self.poziom_przyspieszenia
            self.przyspieszenie_kulki += 1


        Magnes.move_obstacle(self.magnes1, self)
        if self.magnes1.pozycja_y + self.magnes1.height / 2 < self.height * 2/3 or self.first_draw_magnes2 == 1:
            Magnes.move_obstacle(self.magnes2, self)
            self.first_draw_magnes2 = 1
            if self.magnes2.pozycja_y + self.magnes2.height / 2 < self.height * 2/3 or self.first_draw_magnes3 == 1:
              Magnes.move_obstacle(self.magnes3, self)
              self.first_draw_magnes3 = 1

        """
        Czyszczenie ekranu po kolizji
        """
        if Magnes.zderzenie(self.magnes1, self.ball, self) or Magnes.zderzenie(self.magnes2, self.ball, self) or Magnes.zderzenie(self.magnes3, self.ball, self):
            if self.ball.score > self.ball.record:
                self.ball.record = self.ball.score
            self.first_draw = 0
            self.first_draw_magnes2 = 0
            self.first_draw_magnes3 = 0
            Magnes.wyczysc(self.magnes1, self)
            Magnes.wyczysc(self.magnes2, self)
            Magnes.wyczysc(self.magnes3, self)
            self.przyrost_odleglosci = 1
            self.poziom_przyspieszenia = 0

        if self.first_draw == 0:
            self.ball.score = 0
            self.ball.center_x = self.center_x
            self.first_draw = 1
        self.ball.center_y = self.center_y * 1/10
        self.ball.score += self.przyrost_odleglosci
        if self.move == 1 and self.ball.center_x > self.width - self.width + 25:
            if self.ball.center_x - self.przyspieszenie_kulki < self.width - self.width + 25:
                self.ball.center_x = self.width - self.width + 25
            else:
                self.ball.center_x -= self.przyspieszenie_kulki
        elif self.move == 2 and self.ball.center_x < self.width - 25:
            if self.ball.center_x + self.przyspieszenie_kulki > self.width - 25:
                self.ball.center_x = self.width - 25
            else:
                self.ball.center_x += self.przyspieszenie_kulki
        pass

    """
    Reakcja na dotyk, reaguje na przytrzymanie
    """
    def on_touch_down(self, touch):
        if touch.x < self.width / 2 and self.ball.center_x > self.width - self.width + 25:
            self.move = 1
        if touch.x > self.width / 2 and self.ball.center_x < self.width - 25:
            self.move = 2

    def on_touch_up(self, touch):
        self.move = 0

class RaceApp(App):
    def build(self):
        game = RaceGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    RaceApp().run()