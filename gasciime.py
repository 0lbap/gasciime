import sys
import os
import time
from pynput import keyboard

# TODO: rewrite screen with curses (use of alternate screen)
class Game():
  """
  A basic game class intended to be extended, which provides useful methods.
  """
  def __init__(self):
    self._window_width = os.get_terminal_size().columns
    self._window_height = os.get_terminal_size().lines
    self._screen = [[" " for i in range(self._window_width)] for j in range(self._window_height)]
    self._fps = 1
    self._running = False
    self._listener = keyboard.Listener(on_press = self.on_key_press, on_release = self.on_key_release)
    self._alternate_screen = True
    self.load()
    print("Game loaded.")
  
  def _draw_screen(self):
    for row in self._screen:
      for column in row:
        print(column, end="")
      print()

  def _clear_screen(self):
    self._screen = [[" " for i in range(self._window_width)] for j in range(self._window_height)]

  def draw_point(self, x, y, char="."):
    """
    Draw a point on the screen at coordinates (x, y).

    :param x: The x coordinate.
    :param y: The y coordinate.
    :param char: The character to display.
    """
    if x < 0 or x >= self._window_width:
      return
    if y < 0 or y >= self._window_height:
      return
    self._screen[y][x] = char

  def draw_line(self, x1, y1, x2, y2, char="."):
    """
    Draw a line between two points of coordinates (x1, y1) and (x2, y2).

    :param x1: The x coordinate of the first point.
    :param y1: The y coordinate of the first point.
    :param x2: The x coordinate of the second point.
    :param y2: The y coordinate of the second point.
    :param char: The character to display.
    """
    if abs(y2 - y1) < abs(x2 - x1):
      if x1 > x2:
        self._draw_line_low(x2, y2, x1, y1, char)
      else:
        self._draw_line_low(x1, y1, x2, y2, char)
    else:
      if y1 > y2:
        self._draw_line_high(x2, y2, x1, y1, char)
      else:
        self._draw_line_high(x1, y1, x2, y2, char)

  def _draw_line_low(self, x1, y1, x2, y2, char="."):
    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    if dy < 0:
      yi = -1
      dy = -dy
    d = (2 * dy) - dx
    y = y1
    for x in range(x1, x2):
      self.draw_point(x, y, char)
      if d > 0:
        y += yi
        d += (2 * (dy - dx))
      else:
        d += 2 * dy

  def _draw_line_high(self, x1, y1, x2, y2, char="."):
    dx = x2 - x1
    dy = y2 - y1
    xi = 1
    if dx < 0:
      xi = -1
      dx = -dx
    d = (2 * dx) - dy
    x = x1
    for y in range(y1, y2):
      self.draw_point(x, y, char)
      if d > 0:
        x += xi
        d += (2 * (dx - dy))
      else:
        d += 2 * dx

  def draw_rect(self, x, y, w, h, row_char = "─", column_char = "│", top_left_corner_char = "┌", top_right_corner_char = "┐", bottom_left_corner_char = "└", bottom_right_corner_char = "┘"):
    """
    Draw a rectangle of width w and height h. The top left corner is located at (x, y). All characters can be changed, including the lines and the corners.

    :param x: The x coordinate of the top left corner.
    :param y: The y coordinate of the top left corner.
    :param w: The width of the rectangle.
    :param h: The height of the rectangle.
    :param row_char: The character used to display the horizontal lines.
    :param column_char: The character used to display the vertical lines.
    :param top_left_corner_char: The character used to display the top left corner.
    :param top_right_corner_char: The character used to display the top right corner.
    :param bottom_left_corner_char: The character used to display the bottom left corner.
    :param bottom_right_corner_char: The character used to display the bottom right corner.
    """
    self.draw_point(x    , y    , top_left_corner_char)
    self.draw_point(x + w, y    , top_right_corner_char)
    self.draw_point(x    , y + h, bottom_left_corner_char)
    self.draw_point(x + w, y + h, bottom_right_corner_char)
    for i in range(x + 1, x + w):
      self.draw_point(i, y, row_char)
    for i in range(x + 1, x + w):
      self.draw_point(i, y + h, row_char)
    for j in range(y + 1, y + h):
      self.draw_point(x, j, column_char)
    for j in range(y + 1, y + h):
      self.draw_point(x + w, j, column_char)

  def draw_ellipsis(self, x1, y1, x2, y2, char = "."):
    """
    Draw an ellipsis between two points of coordinates (x1, y1) and (x2, y2).

    :param x1: The x coordinate of the first point.
    :param y1: The y coordinate of the first point.
    :param x2: The x coordinate of the second point.
    :param y2: The y coordinate of the second point.
    :param char: The character to display.
    """
    a = abs(x2 - x1)
    b = abs(y2 - y1)
    b1 = b & 1
    dx = 4 * (1 - a) * b * b
    dy = 4 * (b1 + 1) * a * a
    err = dy + dy + b1 * a * a
    e2 = 0
    if x1 > x2:
      x1, x2 = x2, x1 + a
    if y1 > y2:
      y1 = y2
    y1 += (b + 1) // 2
    y2 = y1 - b1
    a *= 8 * a
    b1 = 8 * b * b
    while x1 <= x2:
      self.draw_point(x2, y1, char)
      self.draw_point(x1, y1, char)
      self.draw_point(x1, y2, char)
      self.draw_point(x2, y2, char)
      e2 = 2 * err
      if e2 <= dy:
        y1 += 1
        y2 -= 1
        err += dy
        dy += a
      if e2 >= dx or 2 * err > dy:
        x1 += 1
        x2 -= 1
        err += dx
        dx += b1
    while y1 - y2 < b:
      self.draw_point(x1 - 1, y1, char)
      self.draw_point(x2 + 1, y1, char)
      y1 += 1
      self.draw_point(x1 - 1, y2, char)
      self.draw_point(x2 + 1, y2, char)
      y1 -= 1

  def draw_circle(self, xm, ym, r, char = "."):
    """
    Draw a circle of radius r. The middle of the circle is located at (xm, ym).

    :param xm: The x coordinate of the middle of the circle.
    :param ym: The y coordinate of the middle of the circle.
    :param r: The radius of the circle.
    :param char: The character to display.
    """
    x = -r
    y = 0
    err = 2 - 2 * r
    while x < 0:
      self.draw_point(xm - x, ym + y, char)
      self.draw_point(xm - y, ym - x, char)
      self.draw_point(xm + x, ym - y, char)
      self.draw_point(xm + y, ym + x, char)
      r = err
      if r <= y:
        y += 1
        err += y * 2 + 1
      if r > x or err > y:
        x += 1
        err += x * 2 + 1

  def draw_text(self, x, y, text, orientation = "x"):
    """
    Draw the given text at coordinates (x, y)

    :param x: The x coordinate of the text.
    :param y: The y coordinate of the text.
    :param text: The text to display.
    :param orientation: The orientation of the text. Can be horizontal ("x"), vertical ("y") or diagonal ("xy").
    """
    i = 0
    for char in text:
      match orientation:
        case "x":
          self.draw_point(x + i, y, char)
          i += 1
        case "y":
          self.draw_point(x, y + i, char)
          i += 1
        case "xy":
          self.draw_point(x + i, y + i, char) 
          i += 1
        case other:
          self.draw_point(x + i, y, char)
          i += 1

  def load(self):
    """
    Called once when the game is created. This is where you want to initialize your attributes.
    """
    pass

  def on_key_press(self, key):
    """
    Called when a key is pressed.

    :param key: The code of the pressed key.
    """
    pass

  def on_key_release(self, key):
    """
    Called when a key is released.

    :param key: The code of the released key.
    """
    pass

  def draw(self):
    """
    Called every frame. This is where you want to draw all your sprites.
    """
    pass

  def run(self):
    """
    Start the game execution.
    """
    self._running = True
    self._listener.start()
    print("Game started.")
    while self._running:
      previous_screen = self._screen
      self._clear_screen()
      self.draw()
      if previous_screen != self._screen:
        self._draw_screen()
      time.sleep(1 / self._fps)

  def stop(self):
    """
    Stop the game execution and exit the program.
    """
    self._listener.stop()
    self._running = False
    print("Game stopped.")
    sys.exit(0)
