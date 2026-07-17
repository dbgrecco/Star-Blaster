import os
import random

# Force pygame to run in headless dummy mode so it doesn't need a GUI display
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

pygame.init()

# Create directories
os.makedirs("image", exist_ok=True)
os.makedirs(os.path.join("image", "Novas"), exist_ok=True)

# Helper function to draw a nebula background
def generate_background(color_tint, filename, is_jpg=False):
    width, height = 1250, 719
    surf = pygame.Surface((width, height))
    surf.fill((5, 5, 12))  # Very dark space color
    
    # Draw a simulated nebula
    nebula_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for _ in range(8):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        radius = random.randint(200, 450)
        # Create a radial gradient-like alpha circle
        for r in range(radius, 0, -30):
            alpha = int((1 - r / radius) * 15)
            pygame.draw.circle(nebula_surf, (*color_tint, alpha), (x, y), r)
    surf.blit(nebula_surf, (0, 0))
    
    # Draw stars
    for _ in range(120):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.choice([1, 1, 1, 2, 2, 3])
        brightness = random.randint(150, 255)
        color = (brightness, brightness, random.randint(200, 255))
        pygame.draw.circle(surf, color, (x, y), radius)
        
    path = os.path.join("image", filename)
    pygame.image.save(surf, path)
    print(f"Generated: {path}")

# Draw spaceship templates facing UP
def draw_spaceship(color, size, wing_color, filename):
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    
    # Coordinates relative to center
    cx, cy = w // 2, h // 2
    
    # Wings
    wing_points = [
        (cx - w//2 + 5, cy + h//3),
        (cx, cy - h//4),
        (cx + w//2 - 5, cy + h//3),
        (cx + w//4, cy + h//2),
        (cx - w//4, cy + h//2)
    ]
    pygame.draw.polygon(surf, wing_color, wing_points)
    
    # Wing highlights
    pygame.draw.polygon(surf, (min(255, wing_color[0]+40), min(255, wing_color[1]+40), min(255, wing_color[2]+40)), 
                         [(cx - w//3, cy + h//4), (cx, cy - h//5), (cx + w//3, cy + h//4)], 2)

    # Main fuselage (body)
    body_points = [
        (cx, 5),                       # nose
        (cx - w//5, cy + h//3),       # left wing joint
        (cx - w//6, cy + h//2 - 5),   # left thruster outer
        (cx + w//6, cy + h//2 - 5),   # right thruster outer
        (cx + w//5, cy + h//3)        # right wing joint
    ]
    pygame.draw.polygon(surf, color, body_points)
    
    # Body highlight line
    pygame.draw.line(surf, (255, 255, 255), (cx, 10), (cx, cy + h//2 - 10), 2)
    
    # Cockpit canopy (glass)
    glass_color = (100, 200, 255)
    cockpit_points = [
        (cx, cy - h//4),
        (cx - w//10, cy - h//10),
        (cx, cy + h//10),
        (cx + w//10, cy - h//10)
    ]
    pygame.draw.polygon(surf, glass_color, cockpit_points)
    
    # Engine glow
    pygame.draw.circle(surf, (255, 100, 0), (cx - w//12, cy + h//2 - 5), w//12)
    pygame.draw.circle(surf, (255, 100, 0), (cx + w//12, cy + h//2 - 5), w//12)
    pygame.draw.circle(surf, (255, 200, 0), (cx - w//12, cy + h//2 - 5), w//20)
    pygame.draw.circle(surf, (255, 200, 0), (cx + w//12, cy + h//2 - 5), w//20)
    
    path = os.path.join("image", "Novas", filename)
    pygame.image.save(surf, path)
    print(f"Generated: {path}")

# Draw asteroid/meteorite templates
def draw_asteroid(size, filename):
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    
    cx, cy = w // 2, h // 2
    r = min(w, h) // 2 - 4
    
    # Create an irregular rocky polygon
    points = []
    num_points = 12
    for i in range(num_points):
        angle = (i / num_points) * 2 * 3.14159
        dist = r + random.randint(-r//4, r//4)
        px = cx + int(dist * pygame.math.Vector2(1, 0).rotate(int(angle * 180 / 3.14159)).x)
        py = cy + int(dist * pygame.math.Vector2(1, 0).rotate(int(angle * 180 / 3.14159)).y)
        points.append((px, py))
        
    pygame.draw.polygon(surf, (110, 105, 100), points)
    pygame.draw.polygon(surf, (80, 75, 70), points, 3) # Outline
    
    # Draw craters
    for _ in range(3):
        cr_x = cx + random.randint(-r//2, r//2)
        cr_y = cy + random.randint(-r//2, r//2)
        cr_r = random.randint(3, r//5)
        pygame.draw.circle(surf, (60, 55, 50), (cr_x, cr_y), cr_r)
        pygame.draw.circle(surf, (140, 135, 130), (cr_x, cr_y), cr_r, 1) # Crater rim
        
    path = os.path.join("image", filename)
    pygame.image.save(surf, path)
    print(f"Generated: {path}")

# Draw Saturn planet for powerup
def draw_saturn(size, filename):
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    
    cx, cy = w // 2, h // 2
    r = min(w, h) // 4
    
    # Draw rings back half
    ring_surf_back = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(ring_surf_back, (230, 200, 130, 180), (cx - r * 2, cy - r // 2, r * 4, r))
    # Cut hole
    pygame.draw.ellipse(ring_surf_back, (0, 0, 0, 0), (cx - r * 1.5, cy - r // 3, r * 3, r * 0.6))
    
    # Planet sphere
    pygame.draw.circle(surf, (220, 130, 60), (cx, cy), r)
    # Stripes on planet
    pygame.draw.rect(surf, (180, 100, 40), (cx - r + 2, cy - r//3, r*2 - 4, r//4))
    pygame.draw.rect(surf, (240, 160, 80), (cx - r + 3, cy + r//5, r*2 - 6, r//5))
    
    # Overlay rings front half
    # Blit rings
    surf.blit(ring_surf_back, (0, 0))
    
    path = os.path.join("image", filename)
    pygame.image.save(surf, path)
    print(f"Generated: {path}")

# Draw bola_fogo projectile
def draw_fireball(filename):
    size = 100
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Draw nested glowing circles
    for r in range(45, 0, -3):
        # Gradient from transparent red to solid white
        ratio = r / 45
        alpha = int((1 - ratio) * 255)
        color = (255, int(ratio * 255), int(ratio * 128), alpha)
        pygame.draw.circle(surf, color, (cx, cy), r)
        
    path = os.path.join("image", "Novas", filename)
    pygame.image.save(surf, path)
    print(f"Generated: {path}")


# ----------------------------------------------------
# MAIN GENERATION PROCESS
# ----------------------------------------------------

print("Starting asset generation...")

# Backgrounds
generate_background((40, 30, 90), "space.jpg", is_jpg=True)
generate_background((80, 20, 80), "bkg1.png")
generate_background((20, 70, 70), "bkg2.png")
generate_background((90, 40, 20), "bkg3.png")

# Spaceships
draw_spaceship((230, 230, 240), (80, 100), (0, 180, 255), "ship_1.png")  # Player (White & Cyan)
draw_spaceship((100, 150, 255), (70, 70), (0, 0, 255), "ship_8.png")    # Corvette (Blue)
draw_spaceship((100, 230, 100), (80, 80), (0, 200, 0), "ship_7.png")    # Frigate (Green)
draw_spaceship((255, 230, 100), (60, 60), (200, 150, 0), "ship_6.png")  # Gun boat (Yellow)
draw_spaceship((230, 100, 230), (120, 120), (150, 0, 150), "ship_2.png")# Cruiser (Purple)
draw_spaceship((255, 100, 100), (150, 150), (200, 0, 0), "ship_3.png")  # Destroyer (Red)
draw_spaceship((90, 90, 100), (250, 300), (255, 100, 0), "ship_4.png")   # Boss 1 (Grey & Orange)
draw_spaceship((50, 30, 80), (280, 320), (0, 255, 100), "ship_5.png")    # Boss 2 (Dark & Neon Green)

# Asteroids
draw_asteroid((60, 60), "asteroid.png")
draw_asteroid((60, 60), "meteorito.png")
draw_asteroid((60, 60), "meteorito2.png")

# Saturn Planet PowerUp
draw_saturn((60, 60), "saturno.png")

# Fireball Projectile
draw_fireball("bola_fogo.png")

print("All assets generated successfully!")
