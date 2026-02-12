import pygame
import random
import os
import json
import time
import math

discord_enabled = True
try:
    from pypresence import Presence
    client_id = '1268557975396552797'
    RPC = Presence(client_id)
    try:
        RPC.connect()
    except:
        discord_enabled = False
        print("Discord connection failed, running without rich presence")
except ImportError:
    discord_enabled = False
    print("pypresence not found, running without Discord rich presence")

pygame.init()
pygame.mixer.init()

#conf
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
ANIMATION_ITEMS = 25
ANIMATION_DURATION = 4000  # 4 seconds
DECELERATION_START = 0.6  # Start slowing down at 60% of animation
CASE_OPEN_COOLDOWN = 500

#rgbz
BG_COLOR = (15, 15, 20)
BG_GRADIENT_TOP = (20, 20, 30)
BG_GRADIENT_BOTTOM = (10, 10, 15)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

#rareites
RARITY_COLORS = {
    "Mil-Spec": (75, 105, 255),      # Blue
    "Restricted": (136, 71, 255),     # Purple
    "Classified": (211, 44, 230),     # Pink
    "Covert": (235, 75, 75),          # Red
    "Legendary": (255, 215, 0),       # Gold
}

#rngs
RARITY_PROBABILITIES = {
    "Mil-Spec": 0.7988,
    "Restricted": 0.1598,
    "Classified": 0.032,
    "Covert": 0.0064,
    "Legendary": 0.0026
}

#screeninit
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CS2 Case Opener - Enhanced Edition")
clock = pygame.time.Clock()

def get_file_path(folder_name, file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    possible_paths = [
        os.path.join(script_dir, "Images", folder_name, file_name),
        os.path.join(script_dir, folder_name, file_name),
        os.path.join(script_dir, "Images", file_name),
        os.path.join(script_dir, file_name)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def draw_gradient_rect(surface, color1, color2, rect):
    for y in range(rect.height):
        blend = y / rect.height
        r = int(color1[0] * (1 - blend) + color2[0] * blend)
        g = int(color1[1] * (1 - blend) + color2[1] * blend)
        b = int(color1[2] * (1 - blend) + color2[2] * blend)
        pygame.draw.line(surface, (r, g, b), 
                        (rect.x, rect.y + y), 
                        (rect.x + rect.width, rect.y + y))

def draw_glow(surface, pos, radius, color, intensity=1.0):
    for i in range(3):
        glow_radius = radius + (i * 15)
        alpha = int(80 * intensity / (i + 1))
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, alpha), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (pos[0] - glow_radius, pos[1] - glow_radius), special_flags=pygame.BLEND_ALPHA_SDL2)

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2

# === PARTICLE SYSTEM ===
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.color = color
        self.lifetime = 60
        self.age = 0
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.age += 1
        return self.age < self.lifetime
    
    def draw(self, surface):
        alpha = int(255 * (1 - self.age / self.lifetime))
        color_with_alpha = (*self.color, alpha)
        
        particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, color_with_alpha, (self.size, self.size), self.size)
        surface.blit(particle_surf, (int(self.x) - self.size, int(self.y) - self.size))

# === ENHANCED BUTTON CLASS ===
class coolbuttomn:
    def __init__(self, x, y, width, height, text, color=(60, 60, 80), hover_color=(80, 80, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = self.rect.copy()
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.scale = 1.0
        self.font = pygame.font.Font(None, 36)
        self.glow_intensity = 0
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        target_color = self.hover_color if self.is_hovered else self.color
        self.current_color = tuple(
            int(self.current_color[i] + (target_color[i] - self.current_color[i]) * 0.1)
            for i in range(3)
        )
        target_scale = 0.8 if self.is_hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.2
        target_glow = 0.1 if self.is_hovered else 0.0 
        self.glow_intensity += (target_glow - self.glow_intensity) * 0.1
 
        scaled_width = int(self.original_rect.width * self.scale)
        scaled_height = int(self.original_rect.height * self.scale)
        self.rect.width = scaled_width
        self.rect.height = scaled_height
        self.rect.center = self.original_rect.center
    
    def draw(self, surface):

        if self.glow_intensity > 0.01:
            draw_glow(surface, self.rect.center, self.rect.width // 2, 
                     self.hover_color, self.glow_intensity)
        
        top_color = tuple(min(255, c + 20) for c in self.current_color)
        bottom_color = tuple(max(0, c - 20) for c in self.current_color)
        draw_gradient_rect(surface, top_color, bottom_color, self.rect)
        

        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1 and 
                self.is_hovered)

#caseimage and name stuff nidk
items = {
    "Dreams And Nightmares Case": [
        {"image": "SCAR-20Poultrygeist.png", "name": "SCAR-20 | Poultrygeist", "rarity": "Mil-Spec"},
        {"image": "MAG-7Foresight.png", "name": "MAG-7 | Foresight", "rarity": "Mil-Spec"},
        {"image": "P2000LiftedSpirits.png", "name": "P2000 | Lifted Spirits", "rarity": "Mil-Spec"},
        {"image": "Sawed-OffSpiritBoard.png", "name": "Sawed-Off | Spirit Board", "rarity": "Mil-Spec"},
        {"image": "MP5-SDNecroJr.png", "name": "MP5-SD | Necro Jr.", "rarity": "Mil-Spec"},
        {"image": "MAC-10Ensnared.png", "name": "MAC-10 | Ensnared", "rarity": "Mil-Spec"},
        {"image": "Five-SeveNScrawl.png", "name": "Five-SeveN | Scrawl", "rarity": "Mil-Spec"},
        {"image": "XM1014ZombieOffensive.png", "name": "XM1014 | Zombie Offensive", "rarity": "Restricted"},
        {"image": "PP-BizonSpaceCat.png", "name": "PP-Bizon | Space Cat", "rarity": "Restricted"},
        {"image": "G3SG1DreamGlade.png", "name": "G3SG1 | Dream Glade", "rarity": "Restricted"},
        {"image": "USP-STickettoHell.png", "name": "USP-S | Ticket to Hell", "rarity": "Restricted"},
        {"image": "M4A1-SNightTerror.png", "name": "M4A1-S | Night Terror", "rarity": "Restricted"},
        {"image": "FAMASRapidEyeMovement.png", "name": "FAMAS | Rapid Eye Movement", "rarity": "Classified"},
        {"image": "MP7AbyssalApparition.png", "name": "MP7 | Abyssal Apparition", "rarity": "Classified"},
        {"image": "DualBerettaMelondrama.png", "name": "Dual Berettas | Melondrama", "rarity": "Classified"},
        {"image": "MP9StarlightProtector.png", "name": "MP9 | Starlight Protector", "rarity": "Classified"},
        {"image": "AK-47Nightwish.png", "name": "AK-47 | Nightwish", "rarity": "Classified"},
        {"image": "special.png", "name": "Special Item", "rarity": "Legendary"},
    ],
}


#load case image df
def load_images():
    for case_type in items:
        for item in items[case_type]:
            image_path = get_file_path(case_type.replace(" ", ""), item["image"])
            
            if image_path:
                try:
                    original = pygame.image.load(image_path).convert_alpha()
                    item["image_obj"] = pygame.transform.smoothscale(original, (180, 180))
                except:
                    # Create placeholder
                    item["image_obj"] = create_placeholder(180, 180, item["rarity"])
            else:
                item["image_obj"] = create_placeholder(180, 180, item["rarity"])

def create_placeholder(width, height, rarity):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    color = RARITY_COLORS.get(rarity, (100, 100, 100))
    pygame.draw.rect(surf, color, surf.get_rect(), border_radius=10)
    return surf

def get_random_item(case_type):
    case_items = items[case_type]
    rarity = random.choices(
        list(RARITY_PROBABILITIES.keys()), 
        weights=list(RARITY_PROBABILITIES.values()), 
        k=1
    )[0]
    
    matching = [item for item in case_items if item["rarity"] == rarity]
    if not matching and rarity == "Mil-Spec":
        matching = [item for item in case_items if item["rarity"] == "Mil_spec"]
    
    return random.choice(matching) if matching else random.choice(case_items)

# === ANIMATION SYSTEM ===
def animate_case_opening(case_type):
    case_items = items[case_type]
    
    item_width = 200
    item_gap = 20
    total_items = ANIMATION_ITEMS
    
    anim_items = [random.choice(case_items) for _ in range(total_items)]
    
    win_item = get_random_item(case_type)
    win_index = total_items // 2
    anim_items[win_index] = win_item
    

    total_width = total_items * (item_width + item_gap)
    start_offset = SCREEN_WIDTH // 2
    target_offset = total_width - (win_index * (item_width + item_gap)) - SCREEN_WIDTH // 2 - item_width // 2

    current_offset = -start_offset
    velocity = 0
    max_velocity = 30
    acceleration = 2
    
    particles = []
    start_time = pygame.time.get_ticks()
    
    center_x = SCREEN_WIDTH // 2
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(1.0, elapsed / ANIMATION_DURATION)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        if progress < DECELERATION_START:

            velocity = min(max_velocity, velocity + acceleration)
        else:

            decel_progress = (progress - DECELERATION_START) / (1 - DECELERATION_START)
            eased = ease_out_cubic(decel_progress)
            velocity = max_velocity * (1 - eased)
        
        current_offset += velocity
        
        if current_offset >= target_offset:
            current_offset = target_offset
            running = False
        
        draw_gradient_rect(screen, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM, 
                          pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        for i, item in enumerate(anim_items):
            x = i * (item_width + item_gap) - current_offset + start_offset
            y = SCREEN_HEIGHT // 2 - 100
            

            if -item_width < x < SCREEN_WIDTH:

                dist_from_center = abs(x + item_width // 2 - center_x)
                scale = max(0.7, 1.0 - (dist_from_center / SCREEN_WIDTH) * 0.5)
                

                card_rect = pygame.Rect(x, y, item_width, 250)
                

                rarity_color = RARITY_COLORS.get(item["rarity"], WHITE)
                
                if dist_from_center < 150:
                    glow_intensity = 1.0 - (dist_from_center / 150)
                    draw_glow(screen, (x + item_width // 2, y + 125), 120, rarity_color, glow_intensity)
                

                card_surf = pygame.Surface((item_width, 250), pygame.SRCALPHA)
                pygame.draw.rect(card_surf, (40, 40, 50, 220), card_surf.get_rect(), border_radius=15)
                pygame.draw.rect(card_surf, rarity_color, card_surf.get_rect(), 3, border_radius=15)
                

                if "image_obj" in item:
                    img_rect = item["image_obj"].get_rect(center=(item_width // 2, 100))
                    card_surf.blit(item["image_obj"], img_rect)
                

                font_small = pygame.font.Font(None, 20)
                name_surf = font_small.render(item["name"][:30], True, WHITE)
                name_rect = name_surf.get_rect(center=(item_width // 2, 220))
                card_surf.blit(name_surf, name_rect)
                
                screen.blit(card_surf, card_rect)
        
   
        pygame.draw.line(screen, (255, 255, 0), (center_x, 0), (center_x, SCREEN_HEIGHT), 4)
        
  
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(screen)
        
    
        if random.random() < 0.3:
            particles.append(Particle(center_x, SCREEN_HEIGHT // 2, RARITY_COLORS.get(win_item["rarity"], WHITE)))
        
        pygame.display.flip()
    
    return win_item

def show_result(item):

    particles = []
    rarity_color = RARITY_COLORS.get(item["rarity"], WHITE)
    

    menu_btn = coolbuttomn(100, SCREEN_HEIGHT - 120, 250, 60, "Main Menu")
    again_btn = coolbuttomn(SCREEN_WIDTH - 350, SCREEN_HEIGHT - 120, 250, 60, "Open Again")
    
    start_time = pygame.time.get_ticks()
    
    running = True
    while running:
        dt = clock.tick(FPS)
        elapsed = pygame.time.get_ticks() - start_time
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if elapsed >= CASE_OPEN_COOLDOWN:
                if menu_btn.is_clicked(event):
                    return "menu"
                if again_btn.is_clicked(event):
                    return "again"
        

        menu_btn.update(mouse_pos)
        again_btn.update(mouse_pos)
        
  #partickle
        if random.random() < 0.5:
            particles.append(Particle(
                SCREEN_WIDTH // 2 + random.randint(-100, 100),
                SCREEN_HEIGHT // 2 + random.randint(-100, 100),
                rarity_color
            ))
        
        particles = [p for p in particles if p.update()]
        

        draw_gradient_rect(screen, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM, 
                          pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        

        draw_glow(screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), 180, rarity_color, 0.8)
        

        if "image_obj" in item:
            img_rect = item["image_obj"].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(item["image_obj"], img_rect)
        
   
        font_large = pygame.font.Font(None, 48)
        name_surf = font_large.render(item["name"], True, WHITE)
        name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(name_surf, name_rect)
 
        font_medium = pygame.font.Font(None, 36)
        rarity_surf = font_medium.render(item["rarity"], True, rarity_color)
        rarity_rect = rarity_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190))
        screen.blit(rarity_surf, rarity_rect)
        

        for p in particles:
            p.draw(screen)
        
    
        if elapsed >= CASE_OPEN_COOLDOWN:
            menu_btn.draw(screen)
            again_btn.draw(screen)
        else:
        
            remaining = (CASE_OPEN_COOLDOWN - elapsed) / 1000.0
            timer_surf = font_medium.render(f"Wait: {remaining:.1f}s", True, WHITE)
            timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            screen.blit(timer_surf, timer_rect)
        
        pygame.display.flip()
    
    return "quit"

def main_menu():
 
    font_title = pygame.font.Font(None, 72)
    font_subtitle = pygame.font.Font(None, 32)
    
    open_btn = coolbuttomn(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 70, "Open Case")
    quit_btn = coolbuttomn(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 70, "Quit")
    
    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if open_btn.is_clicked(event):
                return "open"
            if quit_btn.is_clicked(event):
                return "quit"
        
   
        open_btn.update(mouse_pos)
        quit_btn.update(mouse_pos)
        
     
        draw_gradient_rect(screen, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM, 
                          pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
      
        title_surf = font_title.render("CS2 case", True, GOLD)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)
        
        subtitle_surf = font_subtitle.render("epic revamp lmao", True, WHITE)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 210))
        screen.blit(subtitle_surf, subtitle_rect)
        
    
        open_btn.draw(screen)
        quit_btn.draw(screen)
        
        pygame.display.flip()
    
    return "quit"

def main():

    load_images()
    
    inventory = []
    
    running = True
    while running:
        action = main_menu()
        
        if action == "quit":
            break
        elif action == "open":
            case_type = "Dreams And Nightmares Case"
            won_item = animate_case_opening(case_type)
            
            if won_item:
                inventory.append(won_item)
                result = show_result(won_item)
                
                if result == "quit":
                    break
    
    pygame.quit()
    if discord_enabled:
        RPC.close()

if __name__ == "__main__":
    main()