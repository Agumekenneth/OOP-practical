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

    # MODIFICATION 1: Added shape_type and points/radius parameters
    def __init__(self, canvas, x, y, size, color, label_text="", shape_type="oval"):
        """
        Initializes the game object, creating both the shape
        and an optional text label centered on it.
        """
        self.canvas = canvas
        self._x = x
        self._y = y
        self._size = size
        self._color = color
        self._shape_type = shape_type # Store shape type
        self._id = None
        
        # Determine shape to create based on shape_type
        if shape_type == "oval":
            # For oval (circle) shapes
            self._id = self.canvas.create_oval(x, y, x + size, y + size, fill=color)
        elif shape_type == "polygon":
            # For polygon (triangle) shapes - Player ship specific points (pointing up)
            points = [
                x + size / 2, y,            # Top tip (x_center, y)
                x, y + size,                # Bottom left corner
                x + size, y + size          # Bottom right corner
            ]
            self._id = self.canvas.create_polygon(points, fill=color)
        
        # Create the label
        self._label_id = None 
        if label_text:
            # Calculate center for the text. Using the bounding box center works for both shapes.
            center_x = x + size / 2
            # MOD: Slightly adjust y center for the player triangle to be inside the body
            center_y = y + size / 2 if shape_type == "oval" else y + size * 0.7 
            
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
        """Simple collision detection (uses bounding boxes, which is simple and works fine for this game)"""
        x1, y1 = self._x + self._size / 2, self._y + self._size / 2
        x2, y2 = other._x + other._size / 2, other._y + other._size / 2
        
        # Calculate distance between centers
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        
        # Check if distance is less than the sum of their radii/half-sizes
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
    """The player spaceship class, now represented by a triangle."""

    # Define canvas dimensions as class attributes for boundary checks
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600

    def __init__(self, canvas, x, y):
        # MODIFICATION 2: Call super() with shape_type="polygon" to create a triangle
        super().__init__(canvas, x, y, 30, 'cyan', label_text='S', shape_type="polygon") 
        self._speed = 15 # Encapsulated property

    def move_left(self):
        if self._x > 0:
            self.move(-self._speed, 0)

    def move_right(self):
        # Check against canvas width (800) minus object size (30)
        if self._x < self.CANVAS_WIDTH - self._size: 
            self.move(self._speed, 0)

    def move_up(self):
        """Move the player up, with boundary check."""
        if self._y > 0:
            self.move(0, -self._speed)

    def move_down(self):
        """Move the player down, with boundary check."""
        # Check against canvas height (600) minus object size (30)
        if self._y < self.CANVAS_HEIGHT - self._size:
            self.move(0, self._speed)

    def shoot(self):
        """Creates a new Bullet object at the player's position."""
        # MOD: Bullet now spawns from the tip of the triangle ship
        return Bullet(self.canvas, self._x + self._size / 2 - 2, self._y - 5, -10, is_alien=False) 
    
    # Player must implement the abstract update method, even if it does nothing
    def update(self):
        pass


#ALIEN CLASS (Polymorphism Example) 
class Alien(GameObject):
    """Alien that moves downwards and side to side."""

    def __init__(self, canvas, x, y):
        # MOD: Alien retains the default 'oval' shape
        super().__init__(canvas, x, y, 30, 'red', label_text='A', shape_type="oval") 
        self.vx = random.choice([-2, 2])  # horizontal speed
        self.vy = 1.2                      # downward speed
        self._direction_timer = time.time()
        self.CANVAS_WIDTH = 800 
        
        self._shoot_timer = time.time()
        self._shoot_interval = random.uniform(2, 5) 

    def shoot(self):
        """Creates a new Alien Bullet object at the alien's position."""
        # Alien bullets shoot downwards (positive speed) and are red
        return Bullet(self.canvas, self._x + 12, self._y + self._size + 5, 5, color='red', is_alien=True)

    def update(self):
        """
        Polymorphic update method.
        Moves the alien, handles direction change, and shooting.
        """
        # Switch horizontal direction every 2 seconds
        if time.time() - self._direction_timer > 2:
            self.vx *= -1
            self._direction_timer = time.time()
        
        # Bounce off the side walls
        if self._x <= 0 or self._x >= self.CANVAS_WIDTH - self._size:
             self.vx *= -1
             
        self.move(self.vx, self.vy)
        
        if time.time() - self._shoot_timer > self._shoot_interval:
            new_bullet = self.shoot()
            
            self._shoot_timer = time.time()
            self._shoot_interval = random.uniform(2, 5) 
            
            return new_bullet 
        
        return None 


# PLANET CLASS 
class Planet(GameObject):
    """Decorative planet that floats slowly."""

    def __init__(self, canvas, x, y, size):
        color = random.choice(['#2E8B57', '#4682B4', '#DAA520']) 
        # MOD: Planet retains the default 'oval' shape
        super().__init__(canvas, x, y, size, color, label_text='P', shape_type="oval") 
        self.vy = random.uniform(0.4, 0.7)  # vertical speed
        self.CANVAS_HEIGHT = 600 

    def update(self):
        """
        Polymorphic update method.
        Moves the planet down and destroys it if it goes off-screen.
        """
        self.move(0, self.vy)
        if self._y > self.CANVAS_HEIGHT:
            self.destroy() 


# BULLET CLASS (Modified to handle alien bullets) 
class Bullet(GameObject):
    """Bullet fired by player or alien."""

    def __init__(self, canvas, x, y, speed, color='white', is_alien=False):
        bullet_size = 5 if not is_alien else 4 
        # MOD: Bullet retains the default 'oval' shape
        super().__init__(canvas, x, y, bullet_size, color, shape_type="oval") 
        self.speed = speed
        self.is_alien = is_alien 
        self.CANVAS_HEIGHT = 600 

    def update(self):
        """
        Polymorphic update method.
        Moves the bullet and destroys it if it goes off-screen.
        """
        self.move(0, self.speed)
        if self._y < 0 or self._y > self.CANVAS_HEIGHT:
            self.destroy()


#MAIN GAME CLASS (Modified to handle alien bullets)
class SpaceExplorerGame:
    """Main game controller that manages all objects and game state."""
    
    # Define constants for canvas size
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600

    def __init__(self, root):
        self.root = root
        self.root.title("Space Explorer Game")
        self.canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg='black')
        self.canvas.pack()

        # Game state variables
        self.player = Player(self.canvas, self.CANVAS_WIDTH // 2 - 15, self.CANVAS_HEIGHT - 100)
        self.aliens, self.planets, self.bullets = [], [], []
        self.alien_bullets = [] 
        self.lives = 5
        self.score = 0
        self.planets_collected = 0 
        self.paused = False
        self._game_over = False 
        self.end_message_ids = [] 

        # UI elements
        self.lives_label = self.canvas.create_text(
            60, 30, text="Lives: 5", fill='white', font=('Arial', 16), anchor='w'
        )
        self.planets_label = self.canvas.create_text(
            60, 60, text="Planets: 0", fill='white', font=('Arial', 16), anchor='w'
        ) 
        self.score_label = self.canvas.create_text(
            self.CANVAS_WIDTH - 60, 30, text="Score: 0", fill='white', font=('Arial', 16), anchor='e'
        )
        self.pause_label = None

        # Bind controls - ADDED <Up> and <Down> bindings
        self.root.bind("<Left>", lambda e: self.player.move_left() if not self.paused else None)
        self.root.bind("<Right>", lambda e: self.player.move_right() if not self.paused else None)
        self.root.bind("<Up>", lambda e: self.player.move_up() if not self.paused else None)
        self.root.bind("<Down>", lambda e: self.player.move_down() if not self.paused else None)
        self.root.bind("<space>", lambda e: self.shoot_bullet())
        self.root.bind("p", lambda e: self.toggle_pause())
        self.root.bind("x", lambda e: self.stop_game())
        self.root.bind("<Return>", lambda e: self.reset_game()) 

        self.update_game()

    def shoot_bullet(self):
        """Fire a player bullet only if the game isn’t paused and is not over."""
        if not self.paused and not self._game_over:
            self.bullets.append(self.player.shoot())

    def toggle_pause(self):
        """Pause or resume the game."""
        if self._game_over: 
            return
            
        self.paused = not self.paused
        if self.paused:
            self.pause_label = self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2, 
                text="PAUSED", fill='yellow', font=('Arial', 40, 'bold')
            )
        else:
            if self.pause_label:
                self.canvas.delete(self.pause_label)
                self.pause_label = None
    
    def reset_game(self):
        """Resets all game elements and starts a new game (bound to 'Enter')."""
        if not self._game_over and not self.paused:
            return

        for obj_list in [self.aliens, self.planets, self.bullets, self.alien_bullets]:
            for obj in obj_list:
                obj.destroy()
        
        if hasattr(self, 'player') and self.player:
             self.player.destroy()

        for msg_id in self.end_message_ids:
            self.canvas.delete(msg_id)
        self.end_message_ids = []

        if self.pause_label:
            self.canvas.delete(self.pause_label)
            self.pause_label = None
            
        self.aliens, self.planets, self.bullets, self.alien_bullets = [], [], [], []
        self.lives = 5
        self.score = 0
        self.planets_collected = 0
        self.paused = False
        self._game_over = False

        self.player = Player(self.canvas, self.CANVAS_WIDTH // 2 - 15, self.CANVAS_HEIGHT - 100)
        
        self.update_ui()


    def stop_game(self):
        """Display a neutral stop message and halt the game loop (bound to 'x')."""
        if not self._game_over: 
            self._game_over = True
            if self.pause_label:
                self.canvas.delete(self.pause_label)
                self.pause_label = None

            self.end_message_ids.append(self.canvas.create_text(self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2, text="GAME STOPPED", fill='yellow', font=('Arial', 40, 'bold')))
            self.end_message_ids.append(self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 50, text=f"Final Score: {self.score}", fill='white', font=('Arial', 20)
            ))
            self.end_message_ids.append(self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 80, text=f"Planets Collected: {self.planets_collected}", fill='white', font=('Arial', 20)
            ))

    def show_temp_message(self, text, color, duration_ms=1000):
        """Displays a temporary message in the center of the screen."""
        msg_id = self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2, text=text, fill=color, font=('Arial', 28, 'bold')
        )
        self.root.after(duration_ms, lambda: self.canvas.delete(msg_id))

    def update_game(self):
        """Main game loop — updates all entities and checks collisions."""
        if self.paused or self._game_over:
            self.root.after(40, self.update_game)
            return

        # --- Spawning ---
        if random.random() < 0.008:
            self.planets.append(Planet(self.canvas, random.randint(0, self.CANVAS_WIDTH - 20), -40, random.randint(20, 40)))

        if random.random() < 0.03:
            self.aliens.append(Alien(self.canvas, random.randint(0, self.CANVAS_WIDTH - 20), -40))

        # --- Updating and Collision (Planet Loop) ---
        for planet in self.planets[:]:
            planet.update()
            
            if planet.collides_with(self.player):
                planet.destroy()
                self.planets.remove(planet)
                self.planets_collected += 1
                
                if self.planets_collected % 5 == 0 and self.planets_collected > 0:
                    self.lives += 1
                    self.show_temp_message("EXTRA LIFE!", "cyan") 
                
                self.update_ui() 
                continue 

            if planet.position()[1] > self.CANVAS_HEIGHT: 
                self.planets.remove(planet)

        # --- Updating and Collision (Alien Loop) ---
        for alien in self.aliens[:]:
            new_bullet = alien.update()
            if new_bullet:
                self.alien_bullets.append(new_bullet)
            
            if alien.position()[1] > self.CANVAS_HEIGHT:
                alien.destroy()
                self.aliens.remove(alien)
                continue 
            
            if alien.collides_with(self.player):
                alien.destroy()
                self.aliens.remove(alien)
                self.lives -= 1
                self.show_temp_message("HIT! -1 Life", "red") 
                self.update_ui()
                if self.lives <= 0:
                    self.game_over()
                    return 

        # --- Updating and Collision (Player Bullet Loop) ---
        for bullet in self.bullets[:]:
            bullet.update()
            
            if bullet.position()[1] < 0:
                self.bullets.remove(bullet)
                continue

            hit_an_alien = False
            for alien in self.aliens[:]:
                if bullet.collides_with(alien):
                    bullet.destroy()
                    alien.destroy()
                    
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if alien in self.aliens:
                        self.aliens.remove(alien)
                        
                    self.score += 10
                    self.update_ui()
                    hit_an_alien = True
                    break 
            
            if hit_an_alien:
                continue 
        
        # --- Updating and Collision (Alien Bullet Loop) ---
        for alien_bullet in self.alien_bullets[:]:
            alien_bullet.update()

            if alien_bullet.position()[1] > self.CANVAS_HEIGHT:
                self.alien_bullets.remove(alien_bullet)
                continue

            if alien_bullet.collides_with(self.player):
                alien_bullet.destroy()
                if alien_bullet in self.alien_bullets:
                    self.alien_bullets.remove(alien_bullet)
                
                self.lives -= 1
                self.show_temp_message("SHOT DOWN! -1 Life", "red") 
                self.update_ui()
                if self.lives <= 0:
                    self.game_over()
                    return

        self.root.after(40, self.update_game)

    def update_ui(self):
        """Update the score and lives labels"""
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")
        self.canvas.itemconfig(self.planets_label, text=f"Planets: {self.planets_collected}") 

    def game_over(self):
        """Display game over message and stop the game."""
        self._game_over = True 
        
        self.end_message_ids.append(self.canvas.create_text(self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2, text="GAME OVER", fill='red', font=('Arial', 40, 'bold')))
        self.end_message_ids.append(self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 50, text=f"Final Score: {self.score}", fill='white', font=('Arial', 20)
        ))
        self.end_message_ids.append(self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 80, text=f"Planets Collected: {self.planets_collected}", fill='white', font=('Arial', 20)
        ))


# RUN THE GAME
if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceExplorerGame(root)
    root.mainloop()