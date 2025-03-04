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

ANIMATION_ITEMS = 20
DEBOUNCE_TIME = 100   
CASE_OPEN_COOLDOWN = 300

def update_discord_presence(state, details, large_image_key=None, small_image_key=None):
    if discord_enabled:
        try:
            RPC.update(
                state=state,
                details=details,
                large_image=large_image_key,
                small_image=small_image_key
            )
        except:
            pass


if discord_enabled:
    update_discord_presence("In Menu", "Selecting a case to open")

white = (255, 255, 255)
black = (0, 0, 0)
grey = (26, 26, 31)
red = (255, 0, 0)
text_color = (255, 255, 255)

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_file_path(folder_name, file_name):
    possible_paths = [
        os.path.join(script_dir, "Images", "DreamsAndNightmaresCase", file_name) if folder_name == "DreamsAndNightmaresCase" else os.path.join(script_dir, "Images", folder_name, file_name),
        os.path.join(script_dir, "DreamsAndNightmaresCase", file_name) if folder_name == "DreamsAndNightmaresCase" else os.path.join(script_dir, folder_name, file_name),
        os.path.join(script_dir, file_name)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    print(f"Warning: {file_name} not found in {folder_name}")
    return None

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
icon_path = get_file_path("", "icon.png")
if icon_path:
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
pygame.display.set_caption("CASE2 Case Opener")

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
    "Clutch Case": [
        {"image": "XM1014OxideBlaze.png", "name": "XM1014 | Oxide Blaze", "rarity": "Mil-Spec"},
        {"image": "PP-BizonNightRiot.png", "name": "PP-Bizon | Night Riot", "rarity": "Mil-Spec"},
        {"image": "P2000UrbanHazard.png", "name": "P2000 | Urban Hazard", "rarity": "Mil-Spec"},
        {"image": "SG553Aloha.png", "name": "SG 553 | Aloha", "rarity": "Mil-Spec"},
        {"image": "MP9BlackSand.png", "name": "MP9 | Black Sand", "rarity": "Mil-Spec"},
        {"image": "R8RevolverGrip.png", "name": "R8 Revolver | Grip", "rarity": "Mil_spec"},
        {"image": "NovaWildSix.png", "name": "Nova | Wild Six", "rarity": "Restricted"},
        {"image": "UMP-45ArcticWolf.png", "name": "UMP-45 | Arctic Wolf", "rarity": "Restricted"},
        {"image": "NegevLionfish.png", "name": "Negev | Lionfish", "rarity": "Restricted"},
        {"image": "MAG-7SWAG-7.png", "name": "MAG-7 | SWAG-7", "rarity": "Restricted"},
        {"image": "Glock-18Moonrise.png", "name": "Glock-18 | Moonrise", "rarity": "Restricted"},
        {"image": "AUGStymphalian.png", "name": "AUG | Stymphalian", "rarity": "Classified"},
        {"image": "AWPMortis.png", "name": "AWP | Mortis", "rarity": "Classified"},
        {"image": "USP-SCortex.png", "name": "USP-S | Cortex", "rarity": "Classified"},
        {"image": "M4A4Neo-Noir.png", "name": "M4A4 | Neo-Noir", "rarity": "Covert"},
        {"image": "MP7Bloodsport.png", "name": "MP7 | Bloodsport", "rarity": "Covert"},
        {"image": "special.png", "name": "Special Item", "rarity": "Legendary"},
    ],
    "Kilowatt Case": [
        {"image": "UMP-45Motorized.png", "name": "UMP-45 | Motorized", "rarity": "Mil-Spec"},
        {"image": "MAC-10Light Box.png", "name": "MAC-10 | Light Box", "rarity": "Mil-Spec"},
        {"image": "Dual BerettasHideout.png", "name": "Dual Berettas | Hideout", "rarity": "Mil-Spec"},
        {"image": "XM1014Irezumi.png", "name": "XM1014 | Irezumi", "rarity": "Mil-Spec"},
        {"image": "NovaDark Sigil.png", "name": "Nova | Dark Sigil", "rarity": "Mil-Spec"},
        {"image": "SSG 08Dezastre.png", "name": "SSG 08 | Dezastre", "rarity": "Mil-Spec"},
        {"image": "Tec-9Slag.png", "name": "Tec-9 | Slag", "rarity": "Mil-Spec"},
        {"image": "Sawed-OffAnalog Input.png", "name": "Sawed-Off | Analog Input", "rarity": "Restricted"},
        {"image": "MP7Just Smile.png", "name": "MP7 | Just Smile", "rarity": "Restricted"},
        {"image": "Glock-18Block-18.png", "name": "Glock-18 | Block-18", "rarity": "Restricted"},
        {"image": "M4A4Etch Lord.png", "name": "M4A4 | Etch Lord", "rarity": "Restricted"},
        {"image": "Five-SeveNHybrid.png", "name": "Five-SeveN | Hybrid", "rarity": "Restricted"},
        {"image": "USP-SJawbreaker.png", "name": "USP-S | Jawbreaker", "rarity": "Classified"},
        {"image": "Zeus x27Olympus.png", "name": "Zeus x27 | Olympus", "rarity": "Classified"},
        {"image": "M4A1-SBlack Lotus.png", "name": "M4A1-S | Black Lotus", "rarity": "Classified"},
        {"image": "AWPChromeCannon.png", "name": "AWP | Chrome Cannon", "rarity": "Covert"},
        {"image": "AK-47Inheritance.png", "name": "AK-47 | Inheritance", "rarity": "Covert"},
        {"image": "special.png", "name": "Special Item", "rarity": "Legendary"},
    ],
}

rarity_probabilities = {
    "Mil-Spec": 0.45,
    "Restricted": 0.20,
    "Classified": 0.055,
    "Covert": 0.03,
    "Legendary": 0.003
}

rarity_colors = {
    "Mil-Spec": (81, 106, 242),
    "Restricted": (127, 80, 246),
    "Classified": (193, 66, 222),
    "Covert": (216, 87, 82),
    "Legendary": (255, 215, 0),
    "Mil_spec": (81, 106, 242)
}

def scale_image(image, size):
    return pygame.transform.smoothscale(image, size)

def load_images():
    for case_type in items:
        for item in items[case_type]:
            image_path = get_file_path(case_type.replace(" ", ""), item["image"])
            if image_path:
                try:
                    original_image = pygame.image.load(image_path).convert_alpha()
                    
                    large_image = scale_image(original_image, (200, 200))
                    item["large_image"] = large_image
                    item["small_image"] = scale_image(large_image, (150, 150))
                except pygame.error:
                    print(f"Warning: {item['image']} loading failed")
                    item["large_image"] = pygame.Surface((200, 200), pygame.SRCALPHA)
                    item["large_image"].fill(grey)
                    item["small_image"] = pygame.Surface((150, 150), pygame.SRCALPHA)
                    item["small_image"].fill(grey)
            else:
                print(f"Warning: {item['image']} file not found")
                item["large_image"] = pygame.Surface((200, 200), pygame.SRCALPHA)
                item["large_image"].fill(grey)
                item["small_image"] = pygame.Surface((150, 150), pygame.SRCALPHA)
                item["small_image"].fill(grey)

def load_case_icons():
    case_icons = {}
    for case_name in items:
        icon_path = get_file_path("", f"{case_name.replace(' ', '')}Icon.png")
        if icon_path and os.path.exists(icon_path):
            case_icons[case_name] = pygame.image.load(icon_path).convert_alpha()
        else:
            print(f"No icon for {case_name} found")
            case_icons[case_name] = pygame.Surface((200, 200), pygame.SRCALPHA)
            case_icons[case_name].fill((100, 100, 100))
    return case_icons

def get_random_item(case_type):

    case_items = items[case_type]
    rarity = random.choices(list(rarity_probabilities.keys()), weights=list(rarity_probabilities.values()), k=1)[0]
    
    matching_items = [item for item in case_items if item["rarity"] == rarity]
    
    if not matching_items and rarity == "Mil-Spec":
        matching_items = [item for item in case_items if item["rarity"] == "Mil_spec"]
    
    if matching_items:
        return random.choice(matching_items)
    else:

        return random.choice(case_items)


class Button:
    def __init__(self, x, y, width, height, color, text, text_color=black, border_radius=10, image=None):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()
        self.color = color
        self.hover_color = tuple(min(255, c + 50) for c in color)
        self.press_color = tuple(max(0, c - 50) for c in color)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 32)
        self.border_radius = border_radius
        self.last_click_time = 0
        self.is_hovered = False
        self.is_clicked = False
        
        self.hover_scale = 1.05
        self.click_scale = 0.95
        self.scale_progress = 1.0
        self.color_progress = 1.0
        self.shadow_offset = 3
        self.image = image

    def draw(self, screen):
        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=self.border_radius)
        
        current_color = self._interpolate_color()
        
        scaled_rect = pygame.Rect(
            self.rect.x, 
            self.rect.y, 
            int(self.rect.width * self.scale_progress), 
            int(self.rect.height * self.scale_progress)
        )
        scaled_rect.center = self.rect.center
        
        pygame.draw.rect(screen, current_color, scaled_rect, border_radius=self.border_radius)
        
        pygame.draw.rect(screen, black, scaled_rect, 2, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

        if self.image:
            scaled_image = pygame.transform.smoothscale(
                self.image, 
                (int(self.image.get_width() * self.scale_progress), 
                 int(self.image.get_height() * self.scale_progress))
            )
            image_rect = scaled_image.get_rect(center=scaled_rect.center)
            screen.blit(scaled_image, image_rect)

    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.original_rect.collidepoint(mouse_pos)
        self.is_clicked = self.is_hovered and mouse_pressed[0]
        
        if self.is_clicked:
            target_scale = self.click_scale
            target_color_progress = 0.7
        elif self.is_hovered:
            target_scale = self.hover_scale
            target_color_progress = 0.8
        else:
            target_scale = 1.0
            target_color_progress = 1.0
        
        self.scale_progress += (target_scale - self.scale_progress) * 0.2
        self.color_progress += (target_color_progress - self.color_progress) * 0.2
        
        new_width = int(self.original_rect.width * self.scale_progress)
        new_height = int(self.original_rect.height * self.scale_progress)
        self.rect.width = new_width
        self.rect.height = new_height
        self.rect.center = self.original_rect.center

    def _interpolate_color(self):
        base_r, base_g, base_b = self.color
        hover_r, hover_g, hover_b = self.hover_color
        
        interpolated_r = base_r + (hover_r - base_r) * (1 - self.color_progress)
        interpolated_g = base_g + (hover_g - base_g) * (1 - self.color_progress)
        interpolated_b = base_b + (hover_b - base_b) * (1 - self.color_progress)
        
        return (int(interpolated_r), int(interpolated_g), int(interpolated_b))

    def check_click(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

menu_buttons = [
    Button(75, 20, 350, 50, (255, 255, 255), "Dreams And Nightmares Case", black),
    Button(75, 120, 350, 50, (255, 255, 255), "Clutch Case", black),
    Button(75, 220, 350, 50, (255, 255, 255), "Kilowatt Case", black),
    Button(screen_width - 300, screen_height - 100, 200, 50, (255, 255, 255), "Open Case", black),
    Button(screen_width - 300, 20, 200, 50, (255, 255, 255), "Quit", black),
    Button(screen_width - 300, screen_height - 170, 200, 50, (255, 255, 255), "Inventory", black)
]

result_buttons = [
    Button(100, screen_height - 100, 200, 50, (255, 255, 255), "Main Menu", black),
    Button(screen_width - 300, screen_height - 100, 200, 50, (255, 255, 255), "Open One More", black)
]

inventory_buttons = [
    Button(screen_width - 300, screen_height - 100, 200, 50, (255, 255, 255), "Back to Menu", black)
]

def animate_case_opening(case_type):
    item_size = 150
    item_gap = 30
    num_items = ANIMATION_ITEMS
    total_width = num_items * (item_size + item_gap)
    animation_duration = 2700 
    start_time = pygame.time.get_ticks()
    
    case_items = items[case_type]

    if not case_items:
        print(f"Error: No items found for case type {case_type}")
        return get_random_item(case_type) 
    
    randomized_items = []
    for _ in range(num_items):

        if case_items:
            randomized_items.append(random.choice(case_items))
    
    if case_open_sound:
        case_open_sound.play()
    

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        if elapsed_time < animation_duration:
            screen.fill(grey)
            offset = elapsed_time / animation_duration * (total_width + screen_width)
            
            for i in range(num_items):
                x = screen_width + (i * (item_size + item_gap)) - offset
                y = screen_height // 4 - item_size // 4
                
                if -item_size <= x <= screen_width:
                    item = randomized_items[i]
                    if "small_image" in item:
                        screen.blit(item["small_image"], (x, y))
            
            pygame.draw.line(screen, red, (screen_width // 2, 0), (screen_width // 2, screen_height), 2)
            pygame.display.flip()
            pygame.time.delay(15)
        else:

            final_item = get_random_item(case_type)
            screen.fill(grey)
            if "large_image" in final_item:
                screen.blit(final_item["large_image"], (screen_width // 2 - item_size // 2, screen_height // 2 - item_size // 2))
            pygame.display.flip()
            break 

    return final_item


def show_result(item):
    result = None
    start_time = pygame.time.get_ticks()
    while True:
        current_time = pygame.time.get_ticks()
        screen.fill(grey)
        item_size = 200
        item_rect = pygame.Rect(screen_width // 2 - item_size // 2, screen_height // 2 - item_size // 2 - 50, item_size, item_size)
        
        if "large_image" in item:
            screen.blit(item["large_image"], item_rect)
        
        font = pygame.font.Font(None, 28)
        text_surface = font.render(item["name"], True, white)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(text_surface, text_rect)
        
        rarity = item["rarity"]
        rarity_color = rarity_colors.get(rarity, white)
        
        rarity_surface = font.render(rarity, True, rarity_color)
        rarity_rect = rarity_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 140))
        screen.blit(rarity_surface, rarity_rect)
        
        cooldown_remaining = max(0, CASE_OPEN_COOLDOWN - (current_time - start_time))
        

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for button in result_buttons:
            if cooldown_remaining > 0:
                pygame.draw.rect(screen, (100, 100, 100), button.rect, border_radius=button.border_radius)
                text_surface = button.font.render(button.text, True, (150, 150, 150))
                text_rect = text_surface.get_rect(center=button.rect.center)
                screen.blit(text_surface, text_rect)
            else:
                button.update(mouse_pos, mouse_pressed)
                button.draw(screen)
        
        if cooldown_remaining > 0:
            timer_text = f"Wait: {cooldown_remaining / 1000:.1f}s"
            timer_surface = font.render(timer_text, True, white)
            timer_rect = timer_surface.get_rect(center=(screen_width // 2, screen_height - 30))
            screen.blit(timer_surface, timer_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and cooldown_remaining == 0:
                for button in result_buttons:
                    if button.check_click(event.pos, event):
                        if button.text == "Open One More":
                            return "Open Again"
                        else:
                            return button.text
        
        if result:
            return result

def show_inventory(inventory):
    scroll_y = 0
    max_scroll = max(0, len(inventory) * 60 - (screen_height - 150))
    remove_button_pressed = False

    while True:
        screen.fill(grey)
        font = pygame.font.Font(None, 36)
        title_surface = font.render("Inventory", True, white)
        screen.blit(title_surface, (20, 20))

        scroll_surface = pygame.Surface((screen_width - 40, screen_height - 150))
        scroll_surface.fill(grey)

        y_offset = 0
        for i, item in enumerate(inventory):
            rarity = item.get("rarity", "Mil-Spec")
            rarity_color = rarity_colors.get(rarity, white)
            
            item_surface = font.render(f"{item['name']} - {rarity}", True, rarity_color)
            item_rect = item_surface.get_rect(topleft=(10, y_offset - scroll_y))
            scroll_surface.blit(item_surface, item_rect)

            remove_button_rect = pygame.Rect(scroll_surface.get_width() - 210, y_offset - scroll_y, 190, 40)
            pygame.draw.rect(scroll_surface, (255, 0, 0), remove_button_rect, border_radius=5)
            remove_button_text = font.render("Remove", True, white)
            remove_button_text_rect = remove_button_text.get_rect(center=remove_button_rect.center)
            scroll_surface.blit(remove_button_text, remove_button_text_rect)

            y_offset += 60

        screen.blit(scroll_surface, (20, 70))


        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for button in inventory_buttons:
            button.update(mouse_pos, mouse_pressed)
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = max(0, scroll_y - 20)
                elif event.button == 5:
                    scroll_y = min(max_scroll, scroll_y + 20)
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in inventory_buttons:
                        if button.check_click(mouse_pos, event):
                            return button.text
                    for i, item in enumerate(inventory):
                        remove_button_rect = pygame.Rect(screen_width - 230, i * 60 - scroll_y + 70, 190, 40)
                        if remove_button_rect.collidepoint(mouse_pos):
                            inventory.pop(i)
                            save_inventory(inventory)
                            remove_button_pressed = True
                            break

        if remove_button_pressed:
            remove_button_pressed = False
            return "inventory"
                    
def save_inventory(inventory):
    try:
        inventory_data = [{"name": item["name"], "rarity": item["rarity"], "image": item["image"]} 
                         for item in inventory if "name" in item and "rarity" in item and "image" in item]
        with open("inventory.json", "w") as f:
            json.dump(inventory_data, f)
    except Exception as e:
        print(f"Error saving inventory: {e}")

def load_inventory():
    try:
        with open("inventory.json", "r") as f:
            inventory_data = json.load(f)
        inventory = []
        for item_data in inventory_data:
            for case_type in items:
                for item in items[case_type]:
                    if item["name"] == item_data["name"] and item["rarity"] == item_data["rarity"]:
                        inventory.append(item)
                        break
                else:
                    continue
                break
        return inventory
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return []

music_file = "menumusic.mp3"
case_open_sound_file = "caseopen.mp3"

music_path = get_file_path("Sounds", music_file)
if music_path and os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.03)  
        pygame.mixer.music.play(-1)
    except pygame.error:
        print(f"Warning: Failed to play {music_file}")
else:
    print(f"Warning: {music_file} not found")

case_open_sound = None
case_open_sound_path = get_file_path("Sounds", case_open_sound_file)

case_open_sound = None
case_open_sound_path = get_file_path("Sounds", case_open_sound_file)
if os.path.exists(case_open_sound_path):
    case_open_sound = pygame.mixer.Sound(case_open_sound_path)
    case_open_sound.set_volume(1)  
else:
    print(f"Warniga: {case_open_sound_file} no file")

load_images()

def main_game_loop():
    global current_menu, selected_case, inventory

    font = pygame.font.Font(None, 36)

    current_menu = "main"
    selected_case = None
    inventory = load_inventory()

    running = True
    while running:
        screen.fill(grey)

        if current_menu == "main":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_inventory(inventory)
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menu_buttons:
                        if button.check_click(event.pos, event):
                            if button.text == "Quit":
                                save_inventory(inventory)
                                running = False
                            elif button.text == "Open Case" and selected_case:
                                current_menu = "opening"
                            elif button.text == "Inventory":
                                current_menu = "inventory"
                            else:
                                selected_case = button.text

            for button in menu_buttons:
                button.draw(screen)
            
            if selected_case:
                text_surface = font.render(f"Selected Case: {selected_case}", True, white)
                screen.blit(text_surface, (10, 550))
                font = pygame.font.Font(None, 28)

        elif current_menu == "opening":
            update_discord_presence("Opening a case", f"Opening a {selected_case}")
            selected_item = animate_case_opening(selected_case)
            inventory.append(selected_item)
            save_inventory(inventory)
            result = show_result(selected_item)

            if result == "quit":
                save_inventory(inventory)
                running = False
            elif result == "Main Menu":
                update_discord_presence("In Menu", "Selecting a case to open")
                current_menu = "main"
            elif result == "Open Again":
                continue

        elif current_menu == "inventory":
            result = show_inventory(inventory)
            if result == "Back to Menu":
                current_menu = "main"
            elif result == "quit":
                save_inventory(inventory)
                running = False

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()
    RPC.close()


if __name__ == "__main__":
    load_images()
    main_game_loop()