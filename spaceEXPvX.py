import tkinter as tk
import random
import time
import math
from abc import ABC, abstractmethod


# ========== BASE CLASS ==========
class GameObject(ABC):
    def __init__(self, canvas, x, y, size, color, label_text="", shape_type="oval"):
        self.canvas = canvas
        self._x = x
        self._y = y
        self._size = size
        self._color = color
        self._shape_type = shape_type
        self._id = None

        if shape_type == "oval":
            self._id = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        elif shape_type == "polygon":
            half = size / 2
            points = [
                x + size, y + half,
                x, y,
                x, y + size
            ]
            self._id = canvas.create_polygon(points, fill=color, outline="")

        self._label_id = None
        if label_text:
            cx = x + size / 2
            cy = y + size / 2
            font_size = max(8, int(size / 2.5))
            self._label_id = canvas.create_text(cx, cy, text=label_text,
                                                fill='black', font=('Arial', font_size, 'bold'))

    def move(self, dx, dy):
        self.canvas.move(self._id, dx, dy)
        if self._label_id:
            self.canvas.move(self._label_id, dx, dy)
        self._x += dx
        self._y += dy

    def destroy(self):
        self.canvas.delete(self._id)
        if self._label_id:
            self.canvas.delete(self._label_id)

    def position(self):
        return self._x, self._y

    def collides_with(self, other):
        x1 = self._x + self._size / 2
        y1 = self._y + self._size / 2
        x2 = other._x + other._size / 2
        y2 = other._y + other._size / 2
        return math.hypot(x1 - x2, y1 - y2) < (self._size / 2 + other._size / 2)

    @abstractmethod
    def update(self):
        pass


# ========== PLAYER (Rotates + Directional Shoot) ==========
class Player(GameObject):
    WIDTH, HEIGHT = 800, 600

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 40, 'cyan', 'S', shape_type="polygon")
        self._speed = 6
        self.angle = 0.0
        self._last_dx = 0
        self._last_dy = -1

    def _update_rotation(self, dx, dy):
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            nx, ny = dx / length, dy / length
            self.angle = math.atan2(ny, nx)

        cx = self._x + self._size / 2
        cy = self._y + self._size / 2
        half = self._size / 2

        verts = [
            (cx + half, cy),
            (cx - half, cy - half * 0.866),
            (cx - half, cy + half * 0.866)
        ]

        c, s = math.cos(self.angle), math.sin(self.angle)
        rotated = []
        for px, py in verts:
            tx, ty = px - cx, py - cy
            rx = tx * c - ty * s
            ry = tx * s + ty * c
            rotated.extend([cx + rx, cy + ry])

        self.canvas.coords(self._id, *rotated)
        if self._label_id:
            self.canvas.itemconfig(self._label_id, angle=math.degrees(self.angle))

    def move_left(self):   self._move(-self._speed, 0, -1, 0)
    def move_right(self):  self._move(self._speed, 0, 1, 0)
    def move_up(self):     self._move(0, -self._speed, 0, -1)
    def move_down(self):   self._move(0, self._speed, 0, 1)

    def _move(self, dx, dy, dir_x, dir_y):
        if dx < 0 and self._x > 0 or dx > 0 and self._x < self.WIDTH - self._size:
            self.move(dx, 0)
        if dy < 0 and self._y > 0 or dy > 0 and self._y < self.HEIGHT - self._size:
            self.move(0, dy)
        self._update_rotation(dir_x, dir_y)

    def shoot(self):
        cx = self._x + self._size / 2
        cy = self._y + self._size / 2
        tip_x = cx + (self._size / 2) * math.cos(self.angle)
        tip_y = cy + (self._size / 2) * math.sin(self.angle)

        speed = 12
        return Bullet(self.canvas, tip_x - 3, tip_y - 3,
                      speed * math.cos(self.angle), speed * math.sin(self.angle))

    def update(self):
        pass


# ========== BULLET ==========
class Bullet(GameObject):
    def __init__(self, canvas, x, y, vx, vy, color='white', is_alien=False):
        size = 6 if not is_alien else 5
        super().__init__(canvas, x, y, size, color, shape_type="oval")
        self.vx, self.vy = vx, vy

    def update(self):
        self.move(self.vx, self.vy)
        x, y = self.position()
        if x < -100 or x > 900 or y < -100 or y > 700:
            self.destroy()


# ========== ALIEN & PLANET ==========
class Alien(GameObject):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 35, 'red', 'A', shape_type="oval")
        self.vx = random.choice([-2, 2])
        self.vy = 1.5
        self.next_shoot = time.time() + random.uniform(1, 4)

    def shoot(self):
        return Bullet(self.canvas, self._x + 16, self._y + 35, 0, 7, 'orange', True)

    def update(self):
        if time.time() > self.next_shoot:
            self.next_shoot = time.time() + random.uniform(2, 5)
            return self.shoot()

        if self._x <= 0 or self._x >= 765:
            self.vx *= -1
        self.move(self.vx, self.vy)
        return None


class Planet(GameObject):
    def __init__(self, canvas, x, y, size):
        color = random.choice(['#2E8B57', '#4682B4', '#DAA520', '#8B4513', '#9932CC'])
        super().__init__(canvas, x, y, size, color, 'P', shape_type="oval")
        self.vy = random.uniform(0.6, 1.3)

    def update(self):
        self.move(0, self.vy)


# ========== MAIN GAME ==========
class SpaceExplorerGame:
    WIDTH, HEIGHT = 800, 600

    def __init__(self, root):
        self.root = root
        self.root.title("Space Explorer - Directional Shooter")
        self.root.resizable(False, False)

        # Canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg='black')
        self.canvas.pack()

        # Control Frame (buttons)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.pause_btn = tk.Button(btn_frame, text="Pause", width=10, command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.restart_btn = tk.Button(btn_frame, text="Restart", width=10, command=self.restart_game)
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        # Game state
        self.paused = False
        self.game_over = False
        self.keys = set()

        # UI Text
        self.score = 0
        self.lives = 5
        self.planets_collected = 0

        self.score_text = self.canvas.create_text(70, 30, text="Score: 0", fill="white", font=("Arial", 16), anchor="w")
        self.lives_text = self.canvas.create_text(70, 60, text="Lives: 5", fill="white", font=("Arial", 16), anchor="w")
        self.planets_text = self.canvas.create_text(self.WIDTH-70, 30, text="Planets: 0", fill="white", font=("Arial", 16), anchor="e")
        self.pause_overlay = None

        # Start game
        self.start_new_game()

        # Bind keys
        self.root.bind("<KeyPress>", lambda e: self.keys.add(e.keysym))
        self.root.bind("<KeyRelease>", lambda e: self.keys.discard(e.keysym))
        self.root.bind("<space>", lambda e: self.shoot())

    def start_new_game(self):
        # Clear everything
        self.canvas.delete("all")
        self.game_over = False
        self.paused = False
        self.score = 0
        self.lives = 5
        self.planets_collected = 0
        self.update_ui()

        # Recreate UI
        self.score_text = self.canvas.create_text(70, 30, text="Score: 0", fill="white", font=("Arial", 16), anchor="w")
        self.lives_text = self.canvas.create_text(70, 60, text="Lives: 5", fill="white", font=("Arial", 16), anchor="w")
        self.planets_text = self.canvas.create_text(self.WIDTH-70, 30, text="Planets: 0", fill="white", font=("Arial", 16), anchor="e")

        # Create player
        self.player = Player(self.canvas, self.WIDTH//2 - 20, self.HEIGHT - 100)
        self.bullets = []
        self.aliens = []
        self.planets = []
        self.alien_bullets = []

        if self.pause_overlay:
            self.canvas.delete(self.pause_overlay)
            self.pause_overlay = None

        self.pause_btn.config(text="Pause")
        self.game_loop()

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.config(text="Resume")
            if not self.pause_overlay:
                self.pause_overlay = self.canvas.create_text(
                    self.WIDTH//2, self.HEIGHT//2, text="PAUSED", fill="yellow",
                    font=("Arial", 50, "bold")
                )
        else:
            self.pause_btn.config(text="Pause")
            if self.pause_overlay:
                self.canvas.delete(self.pause_overlay)
                self.pause_overlay = None

    def restart_game(self):
        self.start_new_game()

    def shoot(self):
        if not self.paused and not self.game_over and len(self.bullets) < 8:
            self.bullets.append(self.player.shoot())

    def update_ui(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        self.canvas.itemconfig(self.planets_text, text=f"Planets: {self.planets_collected}")

    def game_loop(self):
        if self.paused or self.game_over:
            self.root.after(16, self.game_loop)
            return

        # Player movement
        if "Left" in self.keys:   self.player.move_left()
        if "Right" in self.keys:  self.player.move_right()
        if "Up" in self.keys:     self.player.move_up()
        if "Down" in self.keys:   self.player.move_down()

        # Spawn
        if random.random() < 0.02:
            self.aliens.append(Alien(self.canvas, random.randint(30, 750), -50))
        if random.random() < 0.008:
            sz = random.randint(25, 55)
            self.planets.append(Planet(self.canvas, random.randint(0, self.WIDTH-sz), -sz, sz))

        # Update bullets
        for b in self.bullets[:]:
            b.update()
            if not self.canvas.coords(b._id):
                self.bullets.remove(b)

        # Update aliens
        for a in self.aliens[:]:
            bullet = a.update()
            if bullet:
                self.alien_bullets.append(bullet)
            if a.position()[1] > self.HEIGHT + 50:
                a.destroy()
                self.aliens.remove(a)

        # Update alien bullets
        for b in self.alien_bullets[:]:
            b.update()
            if not self.canvas.coords(b._id):
                self.alien_bullets.remove(b)

        # Update planets
        for p in self.planets[:]:
            p.update()
            if p.collides_with(self.player):
                p.destroy()
                self.planets.remove(p)
                self.planets_collected += 1
                self.score += 10
                self.update_ui()

                # +1 LIFE EVERY 5 PLANETS!
                if self.planets_collected % 5 == 0:
                    self.lives += 1
                    self.update_ui()
                    self.canvas.create_text(
                        self.WIDTH//2, 100, text="+1 LIFE!", fill="cyan",
                        font=("Arial", 30, "bold"), tags="temp"
                    )
                    self.root.after(1500, lambda: self.canvas.delete("temp"))

            elif p.position()[1] > self.HEIGHT + 50:
                self.planets.remove(p)

        # Collisions
        for b in self.bullets[:]:
            for a in self.aliens[:]:
                if b.collides_with(a):
                    b.destroy()
                    a.destroy()
                    self.bullets.remove(b)
                    self.aliens.remove(a)
                    self.score += 20
                    self.update_ui()
                    break

        for b in self.alien_bullets[:]:
            if b.collides_with(self.player):
                b.destroy()
                self.alien_bullets.remove(b)
                self.lives -= 1
                self.update_ui()
                if self.lives <= 0:
                    self.game_over_screen()

        for a in self.aliens[:]:
            if a.collides_with(self.player):
                a.destroy()
                self.aliens.remove(a)
                self.lives -= 1
                self.update_ui()
                if self.lives <= 0:
                    self.game_over_screen()

        self.root.after(16, self.game_loop)

    def game_over_screen(self):
        self.game_over = True
        self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2 - 40,
                                text="GAME OVER", fill="red", font=("Arial", 50, "bold"))
        self.canvas.create_text(self.WIDTH//2, self.HEIGHT//2 + 20,
                                text=f"Score: {self.score}  |  Planets: {self.planets_collected}",
                                fill="white", font=("Arial", 24))


# ========== RUN ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceExplorerGame(root)
    root.mainloop()