import pygame
import numpy as np
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Display configuration
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Synesthetic Canvas - Interactive Sound Painting")

# Creator information
CREATOR = "Shayan Taherkhani"
WEBSITE = "shayantaherkhani.ir"
EMAIL = "admin@shayantaherkhani.ir"

# Audio configuration
SAMPLE_RATE = 44100
NOTES = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C4 to B4
sound_channel = pygame.mixer.Channel(0)

def generate_tone(freq, duration=0.08):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 8192 * np.sin(2 * np.pi * freq * t)
    return pygame.sndarray.make_sound(wave.astype(np.int16))

# Canvas setup
canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
canvas.fill((0, 0, 0, 255))
colors = [
    (255, 50, 50, 220), 
    (50, 255, 100, 220), 
    (100, 150, 255, 220), 
    (255, 255, 100, 220),
    (255, 100, 255, 220),
    (100, 255, 255, 220)
]
brush_size = 20
last_pos = None
particles = []

# Save directory
os.makedirs("synesthetic_art", exist_ok=True)
save_counter = 0

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                canvas.fill((0, 0, 0, 255))
                save_counter += 1
                pygame.image.save(canvas, f"synesthetic_art/{CREATOR}_{save_counter}.png")
            elif event.key == pygame.K_s:
                save_counter += 1
                pygame.image.save(canvas, f"synesthetic_art/{CREATOR}_{save_counter}.png")
    
    # Drawing logic
    if pygame.mouse.get_pressed()[0]:
        current_pos = mouse_pos
        if last_pos:
            color = random.choice(colors)
            
            # Draw main brush stroke
            pygame.draw.line(
                canvas, 
                color, 
                last_pos, 
                current_pos, 
                brush_size + random.randint(-7, 7)
            
            # Generate sound based on position
            note_idx = int((current_pos[0] / WIDTH) * (len(NOTES) - 1))
            freq = NOTES[note_idx] * (0.5 + current_pos[1] / HEIGHT)
            
            if not sound_channel.get_busy():
                sound_channel.play(generate_tone(freq))
            
            # Create visual particles
            for _ in range(4):
                particle = {
                    'pos': list(current_pos),
                    'color': (
                        min(color[0] + random.randint(0, 60), 255),
                        min(color[1] + random.randint(0, 60), 255),
                        min(color[2] + random.randint(0, 60), 255),
                        random.randint(150, 220)
                    ),
                    'radius': random.randint(3, 15),
                    'velocity': [
                        random.uniform(-3, 3), 
                        random.uniform(-3, 3)
                    ],
                    'lifetime': random.randint(20, 40)
                }
                particles.append(particle)
        
        last_pos = current_pos
    else:
        last_pos = None
    
    # Update particles
    for particle in particles[:]:
        particle['pos'][0] += particle['velocity'][0]
        particle['pos'][1] += particle['velocity'][1]
        particle['lifetime'] -= 1
        
        if particle['lifetime'] <= 0:
            particles.remove(particle)
    
    # Render everything
    screen.fill((10, 10, 20))
    screen.blit(canvas, (0, 0))
    
    # Draw particles
    for particle in particles:
        pygame.draw.circle(
            screen, 
            particle['color'], 
            [int(particle['pos'][0]), int(particle['pos'][1])], 
            particle['radius']
        )
    
    # UI elements
    font_sm = pygame.font.SysFont('Arial', 16)
    font_md = pygame.font.SysFont('Arial', 24, bold=True)
    
    # Creator info
    creator_text = font_sm.render(f"Created by {CREATOR} | {WEBSITE} | {EMAIL}", True, (180, 180, 200))
    screen.blit(creator_text, (20, HEIGHT - 30))
    
    # Instructions
    instructions = [
        "DRAW: Hold Left Mouse Button",
        "CLEAR: Press C",
        "SAVE: Press S"
    ]
    
    for i, text in enumerate(instructions):
        text_surf = font_md.render(text, True, (230, 230, 150))
        screen.blit(text_surf, (WIDTH - 300, 20 + i * 40))
    
    # Title
    title = pygame.font.SysFont('Arial', 36, bold=True).render("SYNESTHETIC CANVAS", True, (255, 255, 200))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
