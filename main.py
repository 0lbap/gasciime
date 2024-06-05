from gasciime import Game
from pynput import keyboard
import math

class ExampleGame(Game):
  def load(self):
    self._fps = 30
    self.game_title = "EXAMPLE GAME"
    self.i = 1
    self.player_x = 21
    self.player_y = 21
    self.rect_1_x = 20
    self.rect_1_y = int(math.sin(self.i)*5)+10
    self.rect_1_w = 10
    self.rect_1_h = 5
    self.rect_2_x = int(math.sin(self.i)*7)+50
    self.rect_2_y = 10
    self.rect_2_w = 10
    self.rect_2_h = 5

  def on_key_press(self, key):
    if key == keyboard.Key.up:
      self.player_y -= 1
    elif key == keyboard.Key.down:
      self.player_y += 1
    if key == keyboard.Key.left:
      self.player_x -= 1
    elif key == keyboard.Key.right:
      self.player_x += 1
    if key == keyboard.KeyCode.from_char("q"):
      self.stop()

  def on_key_release(self, key):
    pass

  def draw(self):
    self.i += (1/self._fps)*2
    self.rect_1_y = int(math.sin(self.i)*5)+10
    self.rect_2_x = int(math.sin(self.i)*7)+50
    super().draw_text(self._window_width // 2 - len(self.game_title) // 2, 3, self.game_title)
    super().draw_text(5, 21, "You are here ->")
    super().draw_text(5, 22, "Use arrow keys to move!")
    super().draw_rect(self.rect_1_x, self.rect_1_y, self.rect_1_w, self.rect_1_h)
    super().draw_rect(self.rect_2_x, self.rect_2_y, self.rect_2_w, self.rect_2_h)
    # super().draw_rect(20, 10, 10, 5)
    # super().draw_ellipsis(5, 5, 30, 20)
    # super().draw_circle(15, 15, 5)
    super().draw_point(self.player_x, self.player_y, "O")
    super().draw_line(self.rect_1_x + self.rect_1_w // 2, self.rect_1_y + self.rect_1_h // 2, self.rect_2_x + self.rect_2_w // 2, self.rect_2_y + self.rect_2_h // 2)

game = ExampleGame()
game.run()
