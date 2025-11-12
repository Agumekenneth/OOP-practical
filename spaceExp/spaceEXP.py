import tkinter as tk
import random
import time

# ========== BASE CLASS (Abstraction + Inheritance) ==========
class GameObject:
    """Base class for all game objects — defines position, drawing, and movement."""

    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self._x = x
        self._y = y
        self._size = size
        self._color = color
        self._id = self.canvas.create_oval(x, y, x + size, y + size, fill=color)

    def move(self, dx, dy):
        """Move object by dx, dy"""
        self.canvas.move(self._id, dx, dy)
        self._x += dx
        self._y += dy

    def destroy(self):
        """Remove object from canvas"""
        self.canvas.delete(self._id)

    def position(self):
        """Return current position"""
        return self._x, self._y

    def collides_with(self, other):
        """Check simple collision with another object"""
        x1, y1 = self._x, self._y
        x2, y2 = other._x, other._y
        return abs(x1 - x2) < self._size and abs(y1 - y2) < other._size


# ========== PLAYER CLASS (Encapsulation) ==========
class Player(GameObject):
    """The player spaceship class."""

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 30, 'cyan')
        self._speed = 15

    def move_left(self):
        self.move(-self._speed, 0)

    def move_right(self):
        self.move(self._speed, 0)

    def shoot(self):
        return Bullet(self.canvas, self._x + 12, self._y - 15, -10)


# ========== ALIEN CLASS (Polymorphism Example) ==========
class Alien(GameObject):
    """Alien that moves downwards and side to side."""

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 30, 'red')
        self.vx = random.choice([-1, 1])
        self.vy = 0.5  # slower alien
        self._direction_timer = time.time()

    def update(self):
        """Move the alien"""
        # Switch horizontal direction every 2 seconds
        if time.time() - self._direction_timer > 2:
            self.vx *= -1
            self._direction_timer = time.time()
        self.move(self.vx, self.vy)


# ========== PLANET CLASS ==========
class Planet(GameObject):
    """Decorative planet that floats slowly."""

    def __init__(self, canvas, x, y, size):
        super().__init__(canvas, x, y, size, random.choice(['green', 'blue', 'yellow']))
        self.vy = random.uniform(0.05, 0.15)

    def update(self):
        self.move(0, self.vy)
        if self._y > 600:
            self.destroy()


# ========== BULLET CLASS ==========
class Bullet(GameObject):
    """Bullet fired by player."""

    def __init__(self, canvas, x, y, speed):
        super().__init__(canvas, x, y, 5, 'white')
        self.speed = speed

    def update(self):
        self.move(0, self.speed)
        if self._y < 0 or self._y > 600:
            self.destroy()


# ========== MAIN GAME CLASS ==========
class SpaceExplorerGame:
    """Main game controller that manages all objects."""

    def __init__(self, root):
        self.root = root
        self.root.title("Space Explorer Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        self.player = Player(self.canvas, 370, 500)
        self.aliens, self.planets, self.bullets = [], [], []

        self.lives = 5
        self.score = 0
        self.lives_label = self.canvas.create_text(60, 30, text="Lives: 5", fill='white', font=('Arial', 16))
        self.score_label = self.canvas.create_text(740, 30, text="Score: 0", fill='white', font=('Arial', 16))

        self.last_score_update = int(time.time() * 1000)

        self.root.bind("<Left>", lambda e: self.player.move_left())
        self.root.bind("<Right>", lambda e: self.player.move_right())
        self.root.bind("<space>", lambda e: self.bullets.append(self.player.shoot()))

        self.update_game()

    def update_game(self):
        """Main game loop — updates all entities and checks collisions."""

        # Add random planets
        if random.random() < 0.01:
            self.planets.append(Planet(self.canvas, random.randint(0, 780), 0, random.randint(20, 40)))

        # Add random aliens
        if random.random() < 0.02:
            self.aliens.append(Alien(self.canvas, random.randint(0, 780), 0))

        # Update planets
        for planet in self.planets[:]:
            planet.update()

        # Update aliens
        for alien in self.aliens[:]:
            alien.update()
            # Collision with player
            if alien.collides_with(self.player):
                alien.destroy()
                self.aliens.remove(alien)
                self.lives -= 1
                self.update_ui()
                if self.lives <= 0:
                    self.game_over()
                    return

        # Update bullets and handle collisions
        for bullet in self.bullets[:]:
            bullet.update()
            for alien in self.aliens[:]:
                if bullet.collides_with(alien):
                    bullet.destroy()
                    alien.destroy()
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 10
                    self.update_ui()
                    break

        # Add passive time-based scoring
        current_time = int(time.time() * 1000)
        if current_time - self.last_score_update >= 1000:
            self.score += 1
            self.last_score_update = current_time
            self.update_ui()

        self.root.after(60, self.update_game)

    def update_ui(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")

    def game_over(self):
        self.canvas.create_text(400, 300, text="GAME OVER", fill='red', font=('Arial', 40, 'bold'))


# ========== RUN THE GAME ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceExplorerGame(root)
    root.mainloop()
