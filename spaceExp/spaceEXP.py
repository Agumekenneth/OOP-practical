import tkinter as tk
from tkinter import messagebox
import random
import math

class Entity:
    """
    Abstract base class for all game entities.
    Demonstrates ABSTRACTION by hiding implementation details.
    """
    def __init__(self, canvas, x, y, color, tags):
        self.canvas = canvas
        self.id = canvas.create_oval(x-10, y-10, x+10, y+10, fill=color, tags=tags)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.alive = True

    def move(self):
        """Abstract method for movement."""
        raise NotImplementedError

    def draw(self):
        self.canvas.coords(self.id, self.x-10, self.y-10, self.x+10, self.y+10)

    def collides_with(self, other):
        """Bounding box collision detection. ENCapsulation: internal collision logic."""
        ax1, ay1, ax2, ay2 = self.canvas.bbox(self.id)
        ox1, oy1, ox2, oy2 = self.canvas.bbox(other.id)
        return (ax1 < ox2 and ax2 > ox1 and ay1 < oy2 and ay2 > oy1)

    def destroy(self):
        self.canvas.delete(self.id)
        self.alive = False

class Spaceship(Entity):
    """
    Player's spaceship.
    Inherits from Entity: INHERITANCE.
    """
    def __init__(self, canvas):
        super().__init__(canvas, 400, 550, 'cyan', 'spaceship')
        self.speed = 5
        self.last_shot = 0

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.x = max(20, min(780, self.x))  # Screen bounds
        self.y += dy * self.speed
        self.y = max(20, min(580, self.y))

    def shoot(self, current_time):
        if current_time - self.last_shot > 300:  # Cooldown
            self.last_shot = current_time
            return Bullet(self.canvas, self.x, self.y - 15, 'yellow')
        return None

class Alien(Entity):
    """
    Alien spaceship.
    Inherits from Entity: INHERITANCE.
    """
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 'red', 'alien')
        self.vx = random.choice([-2, 2])
        self.vy = 1
        self.shoot_timer = random.randint(1000, 3000)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= 20 or self.x >= 780:
            self.vx = -self.vx
            self.y += 20  # Drop down

    def can_shoot(self, current_time):
        if current_time % self.shoot_timer == 0:
            self.shoot_timer = random.randint(1000, 3000)
            return True
        return False

    def shoot(self):
        return Bullet(self.canvas, self.x, self.y + 15, 'magenta', True)

class Planet(Entity):
    """
    Decorative planet.
    Inherits from Entity: INHERITANCE.
    """
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, random.choice(['blue', 'green', 'purple']), 'planet')
        self.radius = random.randint(30, 50)
        self.id = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius,
                                     fill=self.color, outline='white', tags='planet')
        self.vy = random.uniform(0.2, 0.5)
        self.alive = False  # Decorative, not destructible

    def move(self):
        self.y += self.vy
        if self.y > 620:
            self.y = -50
            self.x = random.randint(50, 750)

class Bullet(Entity):
    """
    Bullet fired by spaceship or alien.
    POLYMORPHISM: same class used for player and enemy bullets with direction flag.
    """
    def __init__(self, canvas, x, y, color, enemy=False):
        super().__init__(canvas, x, y, color, 'bullet')
        self.vy = 8 if not enemy else -8
        self.size = 4

    def move(self):
        self.y += self.vy
        self.canvas.coords(self.id, self.x-self.size, self.y-self.size,
                           self.x+self.size, self.y+self.size)

class SpaceExplorerGame:
    """
    Main game class. ENCapsulation: manages all game state and logic internally.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Explorer Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(self.root, bg='black', width=800, height=600)
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.aliens = []
        self.bullets = []
        self.planets = []
        self.spaceship = Spaceship(self.canvas)

        # UI
        self.score_label = self.canvas.create_text(750, 30, text="Score: 0", fill='white', font=('Arial', 16))
        self.lives_label = self.canvas.create_text(50, 30, text="Lives: 3", fill='white', font=('Arial', 16))

        # Bind keys
        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)
        self.keys = {'Left': False, 'Right': False, 'space': False}

        self.spawn_aliens()
        self.spawn_planets()
        self.update_game()

    def spawn_aliens(self):
        for i in range(5):
            for j in range(8):
                x = 100 + j * 80
                y = 50 + i * 50
                self.aliens.append(Alien(self.canvas, x, y))

    def spawn_planets(self):
        for _ in range(3):
            self.planets.append(Planet(self.canvas, random.randint(100, 700), random.randint(-100, 0)))

    def key_press(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = True
        if event.keysym == 'space':
            bullet = self.spaceship.shoot(self.current_time)
            if bullet:
                self.bullets.append(bullet)

    def key_release(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = False

    def update_game(self):
        self.current_time = self.root.after_info(0)  # Approximate time

        # Player movement POLYMORPHISM: different entities move differently
        dx = 1 if self.keys['Right'] else 0
        dx -= 1 if self.keys['Left'] else 0
        self.spaceship.move(dx, 0)
        self.spaceship.draw()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.y < 0 or bullet.y > 620:
                bullet.destroy()
                self.bullets.remove(bullet)

        # Update aliens
        for alien in self.aliens[:]:
            if alien.alive:
                alien.move()
                alien.draw()

                # Alien shooting
                if alien.can_shoot(self.current_time):
                    bullet = alien.shoot()
                    self.bullets.append(bullet)

                # Alien hits player
                if alien.collides_with(self.spaceship):
                    self.lives -= 1
                    alien.destroy()
                    self.aliens.remove(alien)
                    self.update_ui()

                # Player bullets hit alien
                for bullet in self.bullets[:]:
                    if not hasattr(bullet, 'enemy') and bullet.collides_with(alien):
                        bullet.destroy()
                        self.bullets.remove(bullet)
                        alien.destroy()
                        self.aliens.remove(alien)
                        self.score += 10
                        self.update_ui()
                        break

            # Enemy bullets hit player
            for bullet in self.bullets[:]:
                if hasattr(bullet, 'enemy') and bullet.collides_with(self.spaceship):
                    bullet.destroy()
                    self.bullets.remove(bullet)
                    self.lives -= 1
                    self.update_ui()
                    break

        # Update planets (background)
        for planet in self.planets:
            planet.move()
            planet.draw()

        self.check_game_over()
        self.root.after(30, self.update_game)  # ~33 FPS

    def update_ui(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")

    def check_game_over(self):
        if self.lives <= 0:
            messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
            self.root.quit()
        elif not self.aliens:
            messagebox.showinfo("Victory", "All aliens defeated! You win!")
            self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SpaceExplorerGame()
    game.run()