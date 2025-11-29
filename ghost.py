import pygame
import random
from game_object import GameObject
from constants import *

class Ghost(GameObject):
    """Base Ghost class"""
    
    def __init__(self, x, y, color):
        super().__init__(x, y, int(CELL_WIDTH//2), int(CELL_HEIGHT//1.2), color)
        self.start_x = x
        self.start_y = y
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.vulnerable_duration = 300  # frames
        self.step = "left"
        self.step_timer = 0
        self.last_RL_direction = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    def update(self, maze, pacman):
        """Update ghost position and state"""
        # Update vulnerable state
        if self.vulnerable:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0
        
        # Update ghost animation
        self.step_timer += 1
        if self.step_timer >= 10:
            self.step = "right" if self.step == "left" else "left"
            self.step_timer = 0
        
        # Move ghost
        self.move(maze, pacman)
    
    def move(self, maze, pacman):
        """Basic ghost movement (random direction on collision)"""
        
        new_x, new_y, hitbox = self.get_next_position()
        
        # Check for collision with walls
        if maze.is_wall_collision(hitbox):
            # Change direction randomly
            self.direction = random.randint(0, 3)
        else:
            self.x = new_x
            self.y = new_y
    
    def get_next_position(self):
        """Get next position based on current direction"""
        new_x, new_y = self.x, self.y
        hitbox = None

        if self.direction in [0, 2]:  # Right or Left
            self.last_RL_direction = self.direction
            if self.direction == 0:  # Right
                new_x += self.speed
                hitbox = pygame.Rect(new_x + self.width * 0.1, new_y + self.height * 0.1, self.width * 0.8, self.height * 0.8)
            else:  # Left
                new_x -= self.speed
                hitbox = pygame.Rect(new_x + self.width * 0.1, new_y + self.height * 0.1, self.width * 0.8, self.height * 0.8)

        elif self.direction in [1, 3]:  # Down or Up
            if self.direction == 1:  # Down
                new_y += self.speed
                hitbox = pygame.Rect(new_x + self.width * 0.1, new_y + self.height * 0.1, self.width * 0.8, self.height * 0.8)
            else:  # Up
                new_y -= self.speed
                hitbox = pygame.Rect(new_x + self.width * 0.1, new_y + self.height * 0.1, self.width * 0.8, self.height * 0.8)
        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0
        if new_x + self.width > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - self.width
        if new_y + self.height > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - self.height
        
        return new_x, new_y, hitbox
            
    def draw(self, screen):
        """Load ghost image"""
        # TODO: Écrire votre code ici
        if self.vulnerable == False:
        
            path_image = (f"imgs/{self.color}_ghost.png")
        
        else:

            path_image = (f"imgs/weak_ghost.png")

        load_image = pygame.image.load(path_image)

        image_scale = pygame.transform.scale(load_image, (self.width, self.height))

        if hasattr(self,"step"):
            if self.step == "left":
                image_scale = pygame.transform.rotate(image_scale, 10)
            else:
                image_scale = pygame.transform.rotate(image_scale, -10)
        
        if hasattr(self,"last_RL_direction"):
            if self.last_RL_direction == 0:
                image_scale = pygame.transform.flip(image_scale, True, False)
                


        screen.blit(image_scale, (self.x, self.y))

    
    def make_vulnerable(self):
        """Make the ghost vulnerable to being eaten"""
        self.vulnerable = True
        self.vulnerable_timer = 0
    
    def reset_position(self):
        """Reset ghost to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.vulnerable = False
        self.vulnerable_timer = 0

class RedGhost(Ghost):
    """Red ghost - aggressive, chases Pacman directly"""
    
    def __init__(self, x, y, color="red"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Aggressive movement - chase Pacman directly"""
        if self.vulnerable:
            # Run away from Pacman when vulnerable
            self.flee_from_pacman(maze, pacman)
        else:
            # Chase Pacman
            self.chase_pacman(maze, pacman)
    
    def chase_pacman(self, maze, pacman):
        """Move towards Pacman"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        dx = pacman_x - self.x
        dy = pacman_y - self.y 

        
        if abs(dx) > abs(dy):
            desired = 0 if dx > 0  else 2
        
        else:
            desired = 1 if dy > 0 else 3
        
        self.direction = desired
        new_x, new_y, hitbox = self.get_next_position()
        
        if maze.is_wall_collision(hitbox):
            alternatives = [0,1,2,3]
            random.shuffle(alternatives)
            
            for d in alternatives:
                self.direction = d
                nx, ny, hb = self.get_next_position()
                if not maze.is_wall_collision(hb):
                    return super().move(maze, pacman)
        
            return
        
        return super().move(maze, pacman)

        
        
        

    def flee_from_pacman(self, maze, pacman):
        """Run away from Pacman when vulnerable"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici

        dx = pacman_x - self.x
        dy = pacman_y - self.y

        if abs(dx) > abs(dy):
            self.direction = 2 if dx > 0 else 0
        else:
            self.direction = 3 if dy > 0 else 1
        
        new_x, new_y, hitbox = self.get_next_position()
        
        if maze.is_wall_collision(hitbox):
            self.direction = random.randint(0,3)
            return super().move(maze, pacman)
        
        self.x, self.y = new_x, new_y


class PinkGhost(Ghost):
    """Pink ghost - tries to ambush Pacman"""

    def __init__(self, x, y, color="pink"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Ambush movement - try to get ahead of Pacman"""
        if self.vulnerable:
            super().move(maze, pacman)  # Random movement when vulnerable
        else:
            self.ambush_pacman(maze, pacman)

    def ambush_pacman(self, maze, pacman):
        """Try to position ahead of Pacman"""
        # Try to position ahead of Pacman
        pacman_x, pacman_y = pacman.get_position()
        ghost_x, ghost_y = self.x, self.y
        
        
        # TODO: Écrire votre code ici
        
        dx = pacman_x - self.x
        dy = pacman_y - self.y

        target_x = pacman_x + dx * 0.5
        target_y = pacman_y + dy * 0.5

        dx2 = target_x - ghost_x
        dy2 = target_y - ghost_y



        if abs(dx2) > abs(dy2):
            self.direction = 0 if dx > 0 else 2
        else:
            self.direction = 1 if dy > 0 else 3

        new_x, new_y, hitbox = self.get_next_position()

        if maze.is_wall_collision(hitbox):
            self.direction = random.randint(0,3)
            
            return super().move(maze, pacman)
        self.x, self.y = new_x, new_y
        
        
        

class BlueGhost(Ghost):
    """Blue ghost - patrol behavior"""

    def __init__(self, x, y, color="blue"):
        super().__init__(x, y, color)
        self.patrol_timer = 0
        self.patrol_duration = 120
    
    def move(self, maze, pacman):
        """Patrol movement - changes direction periodically"""
        self.patrol_timer += 1
        
        # TODO: Écrire votre code ici

        if self.patrol_timer >= self.patrol_duration:
            self.direction = random.choice([0,1,2,3])
            self.patrol_timer = 0

        new_x, new_y, hitbox = self.get_next_position()

        if maze.is_wall_collision(hitbox):
            self.direction = random.choice([0,1,2,3])
            return super().move(maze, pacman)
        
        self.x, self.y = new_x, new_y

class OrangeGhost(RedGhost):
    """Orange ghost - mixed behavior"""

    def __init__(self, x, y, color="orange"):
        super().__init__(x, y, color)
        self.behavior_timer = 0
        self.chase_mode = True
        self.behavior_duration = 180  # frames
    
    def move(self, maze, pacman):
        """Mixed behavior - alternates between chasing and fleeing"""
        self.behavior_timer += 1
        
        # TODO: Écrire votre code ici

        pacman_x, pacman_y = pacman.get_position()

        distance = abs(pacman_x - self.x) + abs(pacman_y - self.y)

        if distance < 80:
            return self.flee_from_pacman(maze, pacman)
        
        return self.chase_pacman(maze, pacman)


ghosts_dict = {
            "red": RedGhost,
            "pink": PinkGhost,
            "blue": BlueGhost,
            "orange": OrangeGhost
        }