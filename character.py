import pygame
import settings

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        skin_path = settings.SKINS[settings.selected_skin]
        self.image = pygame.image.load(skin_path).convert_alpha()
        self.rect  = self.image.get_rect()
        w, h = settings.WINDOW_DIMENSIONS

        self.pos = pygame.math.Vector2(
            (w - self.rect.width) / 2,
            (h - self.rect.height) / 2
        )
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Movement & physics parameters
        self.vel         = pygame.math.Vector2(0, 0)   # current velocity (px/sec)
        self.base_speed  = 400.0                       # px/sec minimum when input begins
        self.thrust      = 200.0                       # px/sec² base acceleration
        self.thrust_gain = 50.0                        # px/sec² added per coin
        self.damping     = 6.0                         # per second (exponential braking)
        self.max_speed   = 800.0                       # px/sec cap

        # Movement bounds
        self.max_x = w - self.rect.width
        self.max_y = h - self.rect.height

    def change_speed(self, delta):
        """Called on coin pickup: permanently improve speed and acceleration."""
        # 1) Raise your base take‑off speed so you see an instant jump
        base_gain = 20.0
        self.base_speed = min(self.max_speed, self.base_speed + delta*base_gain)

        # 2) Raise your thrust so future acceleration is quicker
        self.thrust += delta*self.thrust_gain

        # 3) Raise your max_speed so you can go faster overall
        self.max_speed += delta*self.thrust_gain

    def update(self, dt):
        """Call each frame with dt = seconds since last frame."""
        # 1) Read and normalize input direction
        keys = pygame.key.get_pressed()
        iv = pygame.math.Vector2(
            # right: D or →  
            keys[pygame.K_d] or keys[pygame.K_RIGHT] ,  
            # down: S or ↓  
            keys[pygame.K_s] or keys[pygame.K_DOWN] ,  
        )
        iv.x -= keys[pygame.K_a] or keys[pygame.K_LEFT]  # left: A or ←
        iv.y -= keys[pygame.K_w] or keys[pygame.K_UP]    # up: W or ↑
        
        if iv.length_squared():
            iv.normalize_ip()

            # 2) Compute desired speed:
            #    - Start at base_speed
            #    - Add acceleration * dt
            #    - Clamp to max_speed
            speed = max(self.vel.length(), self.base_speed)
            speed = min(self.max_speed, speed + self.thrust * dt)

            # 3) Snap velocity to exactly that speed along input direction
            self.vel = iv * speed
        else:
            # 4) No input → exponential damping
            factor = max(0.0, 1.0 - self.damping * dt)
            self.vel *= factor

        # 5) Move
        self.pos += self.vel * dt

        # 6) Clamp to screen + zero velocity on edges
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        elif self.pos.x > self.max_x:
            self.pos.x = self.max_x
            self.vel.x = 0

        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        elif self.pos.y > self.max_y:
            self.pos.y = self.max_y
            self.vel.y = 0

        # 7) Update rect
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def add_to_groups(self, *groups):
        for g in groups:
            g.add(self)
