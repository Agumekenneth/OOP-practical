import tkinter as tk
import random
import time
from abc import ABC, abstractmethod

#BASE CLASS (Abstraction + Inheritance)
class GameObject(ABC):
    """
    Base class for all game objects — defines position, drawing, movement,
    and an optional text label. It is an abstract base class, mandating the
    'update' method for all concrete, moving subclasses.
    """

    def __init__(self, canvas, x, y, size, color, label_text=""):
        """
        Initializes the game object, creating both the oval shape
        and an optional text label centered on it.
        """
        self.canvas = canvas
        self._x = x
        self._y = y
        self._size = size
        self._color = color
        
        # Create the main body (oval)
        self._id = self.canvas.create_oval(x, y, x + size, y + size, fill=color)
        
        # Create the label
        self._label_id = None 
        if label_text:
            # Calculate center for the text
            center_x = x + size / 2
            center_y = y + size / 2
            
            # Scale font size based on object size, ensuring a minimum
            font_size = max(8, int(size / 2.5)) 
            
            self._label_id = self.canvas.create_text(
                center_x, 
                center_y, 
                text=label_text, 
                fill='black', # Black for good contrast on all colors
                font=('Arial', font_size, 'bold')
            )

    def move(self, dx, dy):
        """Move object and its label by dx, dy"""
        self.canvas.move(self._id, dx, dy)
        
        if self._label_id:
            self.canvas.move(self._label_id, dx, dy)
            
        self._x += dx
        self._y += dy

    def destroy(self):
        """Remove object and its label from canvas"""
        self.canvas.delete(self._id)
        
        if self._label_id:
            self.canvas.delete(self._label_id)

    def position(self):
        """Return current position"""
        return self._x, self._y

    def collides_with(self, other):
        """Simple collision detection"""
        x1, y1 = self._x + self._size / 2, self._y + self._size / 2
        x2, y2 = other._x + other._size / 2, other._y + other._size / 2
        
        # Calculate distance between centers
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        
        # Check if distance is less than the sum of their radii
        return distance < (self._size / 2) + (other._size / 2)

    @abstractmethod
    def update(self):
        """
        Abstract method. All subclasses that are actively controlled by the
        main game loop must implement their unique movement/behavior logic here.
        """
        pass


#PLAYER CLASS (Encapsulation)
class Player(GameObject):
    """The player spaceship class. Note: Player movement is user-driven, so it does not use the update() method in the main loop."""

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 30, 'cyan', label_text='S')
        self._speed = 15 # Encapsulated property

    def move_left(self):
        if self._x > 0:
            self.move(-self._speed, 0)

    def move_right(self):
        # Check against canvas width (800) minus object size (30)
        if self._x < 800 - self._size: 
            self.move(self._speed, 0)

    def shoot(self):
        """Creates a new Bullet object at the player's position."""
        return Bullet(self.canvas, self._x + 12, self._y - 15, -10)
    
    # Player must implement the abstract update method, even if it does nothing
    def update(self):
        pass


#ALIEN CLASS (Polymorphism)
class Alien(GameObject):
    """Alien that moves downwards and side to side."""

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, 30, 'red', label_text='A')
        self.vx = random.choice([-2, 2])  # horizontal speed
        self.vy = 1.2                      # downward speed
        self._direction_timer = time.time()

    def update(self):
        """
        Polymorphic update method.
        Moves the alien and handles its side-to-side direction change.
        """
        # Switch horizontal direction every 2 seconds
        if time.time() - self._direction_timer > 2:
            self.vx *= -1
            self._direction_timer = time.time()
        
        # Bounce off the side walls
        if self._x <= 0 or self._x >= 800 - self._size:
             self.vx *= -1
             
        self.move(self.vx, self.vy)


#PLANET CLASS
class Planet(GameObject):
    """Decorative planet that floats slowly."""

    def __init__(self, canvas, x, y, size):
        color = random.choice(['#2E8B57', '#4682B4', '#DAA520']) # SeaGreen, SteelBlue, Goldenrod
        super().__init__(canvas, x, y, size, color, label_text='P')
        self.vy = random.uniform(0.4, 0.7)  # vertical speed

    def update(self):
        """
        Polymorphic update method.
        Moves the planet down and destroys it if it goes off-screen.
        """
        self.move(0, self.vy)
        if self._y > 600:
            self.destroy() 


#BULLET CLASS 
class Bullet(GameObject):
    """Bullet fired by player."""

    def __init__(self, canvas, x, y, speed):
        # No label needed for the bullet
        super().__init__(canvas, x, y, 5, 'white')
        self.speed = speed

    def update(self):
        """
        Polymorphic update method.
        Moves the bullet and destroys it if it goes off-screen.
        """
        self.move(0, self.speed)
        if self._y < 0 or self._y > 600:
            self.destroy()


#MAIN GAME CLASS
class SpaceExplorerGame:
    """Main game controller that manages all objects and game state."""

    def __init__(self, root):
        self.root = root
        self.root.title("Space Explorer Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        # Game state variables
        self.player = Player(self.canvas, 370, 500)
        self.aliens, self.planets, self.bullets = [], [], []
        self.lives = 5
        self.score = 0
        self.planets_collected = 0 
        self.paused = False
        self._game_over = False 

        # UI elements
        self.lives_label = self.canvas.create_text(
            60, 30, text="Lives: 5", fill='white', font=('Arial', 16), anchor='w'
        )
        self.planets_label = self.canvas.create_text(
            60, 60, text="Planets: 0", fill='white', font=('Arial', 16), anchor='w'
        ) 
        self.score_label = self.canvas.create_text(
            740, 30, text="Score: 0", fill='white', font=('Arial', 16), anchor='e'
        )
        self.pause_label = None

        # Bind controls
        self.root.bind("<Left>", lambda e: self.player.move_left() if not self.paused else None)
        self.root.bind("<Right>", lambda e: self.player.move_right() if not self.paused else None)
        self.root.bind("<space>", lambda e: self.shoot_bullet())
        self.root.bind("p", lambda e: self.toggle_pause())  # Pause/Resume with 'P'

        self.update_game()

    def shoot_bullet(self):
        """Fire a bullet only if the game isn’t paused and is not over."""
        if not self.paused and not self._game_over:
            self.bullets.append(self.player.shoot())

    def toggle_pause(self):
        """Pause or resume the game."""
        if self._game_over: 
            return
            
        self.paused = not self.paused
        if self.paused:
            self.pause_label = self.canvas.create_text(
                400, 300, text="PAUSED", fill='yellow', font=('Arial', 40, 'bold')
            )
        else:
            if self.pause_label:
                self.canvas.delete(self.pause_label)
                self.pause_label = None

    def show_temp_message(self, text, color, duration_ms=1000):
        """Displays a temporary message in the center of the screen."""
        msg_id = self.canvas.create_text(
            400, 300, text=text, fill=color, font=('Arial', 28, 'bold')
        )
        
        # Schedule its deletion
        self.root.after(duration_ms, lambda: self.canvas.delete(msg_id))

    def update_game(self):
        """Main game loop — updates all entities and checks collisions."""
        if self.paused or self._game_over:
            # If paused or over, just reschedule the check without updating
            self.root.after(40, self.update_game)
            return

        # --- Spawning ---
        # Add random planets
        if random.random() < 0.008:
            self.planets.append(Planet(self.canvas, random.randint(0, 780), -40, random.randint(20, 40)))

        # Add random aliens
        if random.random() < 0.03:
            self.aliens.append(Alien(self.canvas, random.randint(0, 780), -40))

        # --- Updating and Collision ---
        
        # Update planets
        for planet in self.planets[:]:
            planet.update()
            
            # Check for player collision with planet
            if planet.collides_with(self.player):
                planet.destroy()
                self.planets.remove(planet)
                self.planets_collected += 1
                
                # Check for reward (every 5 planets)
                if self.planets_collected % 5 == 0 and self.planets_collected > 0:
                    self.lives += 1
                    self.show_temp_message("EXTRA LIFE!", "cyan") # Flash message
                
                self.update_ui() 
                continue 

            if planet.position()[1] > 600: # Remove if off-screen
                self.planets.remove(planet)

        # Update aliens
        for alien in self.aliens[:]:
            alien.update()
            
            # Remove if off-screen
            if alien.position()[1] > 600:
                alien.destroy()
                self.aliens.remove(alien)
                continue 
            
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
            
            # Remove if off-screen
            if bullet.position()[1] < 0:
                self.bullets.remove(bullet)
                continue

            # Check for collision with any alien
            hit_an_alien = False
            for alien in self.aliens[:]:
                if bullet.collides_with(alien):
                    # Destroy both
                    bullet.destroy()
                    alien.destroy()
                    
                    # Remove from lists
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if alien in self.aliens:
                        self.aliens.remove(alien)
                        
                    self.score += 10
                    self.update_ui()
                    hit_an_alien = True
                    break # A bullet can only hit one alien
            
            if hit_an_alien:
                continue 


        # Schedule the next frame
        self.root.after(40, self.update_game)  # ~25 frames per second

    def update_ui(self):
        """Update the score and lives labels"""
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")
        self.canvas.itemconfig(self.planets_label, text=f"Planets: {self.planets_collected}") 

    def game_over(self):
        """Display game over message and stop the game."""
        self._game_over = True # Set the flag
        self.canvas.create_text(400, 300, text="GAME OVER", fill='red', font=('Arial', 40, 'bold'))
        # Show final stats
        self.canvas.create_text(
            400, 350, text=f"Final Score: {self.score}", fill='white', font=('Arial', 20)
        )
        self.canvas.create_text(
            400, 380, text=f"Planets Collected: {self.planets_collected}", fill='white', font=('Arial', 20)
        )


#RUN THE GAME 
if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceExplorerGame(root)
    root.mainloop()
