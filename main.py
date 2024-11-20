import pygame
import random
import os
import json
import time
import math
from pypresence import Presence

pygame.init()
pygame.mixer.init()

client_id = '1268557975396552797'  
RPC = Presence(client_id)
RPC.connect()

ANIMATION_ITEMS = 20
DEBOUNCE_TIME = 100   
CASE_OPEN_COOLDOWN = 400

def update_discord_presence(state, details, large_image_key=None, small_image_key=None):
    RPC.update(
        state=state,
        details=details,
        large_image=large_image_key,
        small_image=small_image_key
    )

update_discord_presence("In Menu", "Selecting a case to open")


white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (100, 100, 100)
button_color = (100, 100, 255)
hover_color = (150, 150, 255)
press_color = (50, 50, 200)
text_color = (255, 255, 255)

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_file_path(folder, file_name):
    return os.path.join(script_dir, folder, file_name)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
icon_path = get_file_path("Images", "icon.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
pygame.display.set_caption("CASE2 Case Opener")


items = {
    "Weapon Case": [
        {"image": "tec9_ddpat.png", "name": "Tec-9 | Urban DDPAT", "rarity": "Common"},
        {"image": "mp9blacksand.png", "name": "MP9 | Black Sand", "rarity": "Common"},
        {"image": "bizonsand.png", "name": "PP-Bizon | Sand Dashed", "rarity": "Common"},
        {"image": "ak47safari.png", "name": "AK-47 | Safari Mesh", "rarity": "Common"},
        {"image": "deagle_bronze.png", "name": "Desert Eagle | Bronze Deco", "rarity": "Uncommon"},
        {"image": "tec9slag.png", "name": "Tec-9 | Slag", "rarity": "Uncommon"},
        {"image": "mac10lightbox.png", "name": "Mac-10 | Light Box", "rarity": "Uncommon"},
        {"image": "umpmotorized.png", "name": "UMP-45 | Motorized", "rarity": "Uncommon"},
        {"image": "ak47baroqueurple.png", "name": "AK-47 | Baroque Purple", "rarity": "Uncommon"},
        {"image": "m4a1s_mud.png", "name": "M4A1-S | Mud-Spec", "rarity": "Uncommon"},
        {"image": "dualieshideout.png", "name": "Dual Berettas | Hideout", "rarity": "Uncommon"},
        {"image": "ak47black.png", "name": "AK-47 | Slate", "rarity": "Rare"},
        {"image": "fivesevenhybrid.png", "name": "Five-SeveN | Hybrid", "rarity": "Rare"},
        {"image": "ak47_green.png", "name": "AK-47 |  Green Laminate", "rarity": "Rare"},
        {"image": "m4a1s_blacklotus.png", "name": "M4A1-S | Black Lotus", "rarity": "Rare"},
        {"image": "mp7justsmile.png", "name": "MP7 | Just Smile", "rarity": "Rare"},
        {"image": "ak47rainbow.png", "name": "AK-47 | Nightwish", "rarity": "Epic"},
        {"image": "uspjawbreaker.png", "name": "USP-S | Jawbreaker", "rarity": "Epic"},
        {"image": "sawedoffanalog.png", "name": "Sawed-Off | Analog", "rarity": "Epic"},
        {"image": "m4a4etchlord.png", "name": "M4A4 | Etch Lord", "rarity": "Epic"},
        {"image": "zeusolympus.png", "name": "Zeus x27 | Olympus", "rarity": "Epic"},
        {"image": "awp_hydra.png", "name": "Hatıra AWP | Desert Hydra", "rarity": "Legendary"},
        {"image": "ak47inheritance.png", "name": "AK-47 | Inheritance", "rarity": "Legendary"},
    ],
    "Knife Case": [
        {"image": "navaja_forest.png", "name": "Navaja Knife | Forest DDPAT", "rarity": "Common"},
        {"image": "classicknifeforest.png", "name": "Classic Knife | Forest DDPAT", "rarity": "Common"},
        {"image": "hook_scorched.png", "name": "Hook Knife | Scorched", "rarity": "Uncommon"},
        {"image": "daggersauto.png", "name": "Shadow Daggers | Autotronic", "rarity": "Uncommon"},
        {"image": "stilettokdamas.png", "name": "Stiletto Knife | Damascus Steel", "rarity": "Uncommon"},
        {"image": "survivalknifeborealforest.png", "name": "Survival Knife | Boreal Forest", "rarity": "Uncommon"},
        {"image": "gutktiger.png", "name": "Gut Knife | Tiger Tooth", "rarity": "Uncommon"},
        {"image": "bayonet_doppler.png", "name": "StatTrak™ Bayonet | Doppler", "rarity": "Rare"},
        {"image": "ursuskslaughter.png", "name": "Ursus Knife | Slaughter", "rarity": "Rare"},
        {"image": "bowiegamma.png", "name": "Bowie Knife | Gamma Doppler", "rarity": "Rare"},
        {"image": "falchionlore.png", "name": "Falchion Knife | Lore", "rarity": "Rare"},
        {"image": "skeletonbluesteel.png", "name": "Skeleton Knife | Blue Steel", "rarity": "Rare"},
        {"image": "nomadcrimson.png", "name": "Nomad Knife | Crimson Web", "rarity": "Rare"},
        {"image": "butterfly_stained.png", "name": "Butterfly Knife | Stained", "rarity": "Epic"},
        {"image": "paracordknife.png", "name": "Paracord Knife | (Vanilla)", "rarity": "Epic"},
        {"image": "flipkfade.png", "name": "Flip Knife | Fade", "rarity": "Epic"},
        {"image": "huntsmanmarble.png", "name": "Huntsman Knife | Marble Fade", "rarity": "Epic"},
        {"image": "kukribluesteel.png", "name": "Kukri Knife | Blue Steel", "rarity": "Epic"},
        {"image": "talon_case.png", "name": "Talon Knife | Case", "rarity": "Legendary"},
        {"image": "karambitultraviolet.png", "name": "Karambit | Ultraviolet", "rarity": "Legendary"},
    ],
    "Glove Case": [
        {"image": "hydra_mangrove.png", "name": "Hydra Gloves | Mangrove", "rarity": "Common"},
        {"image": "wraps_giraffe.png", "name": "Hand Wraps | Giraffe", "rarity": "Uncommon"},
        {"image": "bloodhoundbronzed.png", "name": "Bloodhound Gloves | Bronzed", "rarity": "Uncommon"},
        {"image": "specialistfield.png", "name": "Specialist Gloves | Field Agent", "rarity": "Uncommon"},
        {"image": "moto_polygon.png", "name": "Moto Gloves | Polygon", "rarity": "Rare"},
        {"image": "wrapscaution.png", "name": "Hand Wraps | CAUTION!", "rarity": "Rare"},
        {"image": "specialistcrimson.png", "name": "Specialist Gloves | Crimson Web", "rarity": "Rare"},
        {"image": "specialistmarble.png", "name": "Specialist Gloves | Marble Fade", "rarity": "Rare"},
        {"image": "driver_imperial.png", "name": "Driver Gloves | Imperial Plaid", "rarity": "Epic"},
        {"image": "motogblood.png", "name": "Moto Gloves | Blood Pressure", "rarity": "Epic"},
        {"image": "driverblacktie.png", "name": "Driver Gloves | Black Tie", "rarity": "Epic"},
        {"image": "sport_vice.png", "name": "Sport Gloves | Vice", "rarity": "Legendary"},
        {"image": "driversnowleopard.png", "name": "Driver Gloves | Snow Leopard", "rarity": "Legendary"},
        {"image": "brokenfangjade.png", "name": "Broken Fang Gloves | Jade", "rarity": "Legendary"},
    ]
}

rarity_probabilities = {
    "Common": 0.45,
    "Uncommon": 0.20,
    "Rare": 0.055,
    "Epic": 0.03,
    "Legendary": 0.003
}

rarity_colors = {
    "Common": (192, 192, 192),  
    "Uncommon": (0, 0, 255),    
    "Rare": (128, 0, 128),      
    "Epic": (255, 105, 180),    
    "Legendary": (255, 215, 0)  
}

def scale_image(image, size):
    return pygame.transform.smoothscale(image, size)

def load_images():
    for case_type in items:
        for item in items[case_type]:
            try:
                image_path = get_file_path("Images", item["image"])
                original_image = pygame.image.load(image_path).convert_alpha()
                
                large_image = scale_image(original_image, (200, 200))
                item["large_image"] = large_image
                item["small_image"] = scale_image(large_image, (150, 150))
            except pygame.error:
                print(f"Warning: {item['image']} file could not be loaded. Default color will be used.")
                item["large_image"] = pygame.Surface((200, 200), pygame.SRCALPHA)
                item["large_image"].fill(grey)
                item["small_image"] = pygame.Surface((150, 150), pygame.SRCALPHA)
                item["small_image"].fill(grey)

def get_random_item(case_type):
    rarity = random.choices(list(rarity_probabilities.keys()), weights=rarity_probabilities.values(), k=1)[0]
    return random.choice([item for item in items[case_type] if item["rarity"] == rarity])

class Button:
    def __init__(self, x, y, width, height, color, text, text_color=black, border_radius=10):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 32)
        self.border_radius = border_radius
        self.last_click_time = 0
        self.is_hovered = False
        self.is_clicked = False
        self.animation_progress = 0
        self.hover_scale = 1.05
        self.click_scale = 0.95

    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.original_rect.collidepoint(mouse_pos)
        self.is_clicked = self.is_hovered and mouse_pressed[0]

        target_progress = 1 if self.is_clicked else (0.5 if self.is_hovered else 0)
        self.animation_progress += (target_progress - self.animation_progress) * 0.2

        scale = self.click_scale + (self.hover_scale - self.click_scale) * (1 - self.animation_progress)
        new_width = int(self.original_rect.width * scale)
        new_height = int(self.original_rect.height * scale)
        self.rect.width = new_width
        self.rect.height = new_height
        self.rect.center = self.original_rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, black, self.rect, 2, border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def update_buttons(buttons):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for button in buttons:
        button.update(mouse_pos, mouse_pressed)

def draw_buttons(buttons, screen):
    for button in buttons:
        button.draw(screen)

menu_buttons = [
    Button(100, 100, 200, 50, (255, 255, 255), "Weapon Case", black),
    Button(100, 200, 200, 50, (255, 255, 255), "Knife Case", black),
    Button(100, 300, 200, 50, (255, 255, 255), "Glove Case", black),
    Button(screen_width - 300, screen_height - 100, 200, 50, (255, 255, 255), "Open Case", black),
    Button(screen_width - 300, 20, 200, 50, (255, 255, 255), "Quit", black),
    Button(screen_width - 300, screen_height - 170, 200, 50, (255, 255, 255), "Inventory", black)
]

result_buttons = [
    Button(100, screen_height - 100, 200, 50, (255, 255, 255), "Main Menu", black),
    Button(screen_width - 300, screen_height - 100, 200, 50, (255, 255, 255), "Open Again", black)
]

inventory_buttons = [
    Button(screen_width - 220, screen_height - 70, 200, 50, (255, 255, 255), "Back to Menu", black)
]

def animate_case_opening(case_type):
    item_size = 150
    item_gap = 30
    num_items = ANIMATION_ITEMS
    
    total_width = num_items * (item_size + item_gap)
    animation_duration = 2700
    start_time = pygame.time.get_ticks()
    
    randomized_items = [random.choice(items[case_type]) for _ in range(num_items)]
    
    if case_open_sound:
        case_open_sound.play()
    
    while pygame.time.get_ticks() - start_time < animation_duration:
        screen.fill(grey)
        offset = (pygame.time.get_ticks() - start_time) / animation_duration * (total_width + screen_width)
        for i in range(num_items):
            x = screen_width + (i * (item_size + item_gap)) - offset
            y = screen_height // 4 - item_size // 4
            if -item_size <= x <= screen_width:
                screen.blit(randomized_items[i]["small_image"], (x, y))
        
        pygame.draw.line(screen, red, (screen_width // 2, 0), (screen_width // 2, screen_height), 2)
        
        pygame.display.flip()
        pygame.time.delay(10)
    
    return get_random_item(case_type)

def show_result(item):
    result = None
    start_time = pygame.time.get_ticks()
    while True:
        current_time = pygame.time.get_ticks()
        screen.fill(grey)
        item_size = 200
        item_rect = pygame.Rect(screen_width // 2 - item_size // 2, screen_height // 2 - item_size // 2 - 50, item_size, item_size)
        screen.blit(item["large_image"], item_rect)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(item["name"], True, white)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(text_surface, text_rect)
        
        rarity_surface = font.render(item["rarity"], True, rarity_colors[item["rarity"]])
        rarity_rect = rarity_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 140))
        screen.blit(rarity_surface, rarity_rect)
        
        cooldown_remaining = max(0, CASE_OPEN_COOLDOWN - (current_time - start_time))
        
        for button in result_buttons:
            if cooldown_remaining > 0:
                pygame.draw.rect(screen, (100, 100, 100), button.rect, border_radius=button.border_radius)
                text_surface = button.font.render(button.text, True, (150, 150, 150))
                text_rect = text_surface.get_rect(center=button.rect.center)
                screen.blit(text_surface, text_rect)
            else:
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
                        result = button.text
        
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
            item_surface = font.render(f"{item['name']} - {item['rarity']}", True, rarity_colors[item['rarity']])
            item_rect = item_surface.get_rect(topleft=(10, y_offset - scroll_y))
            scroll_surface.blit(item_surface, item_rect)

            remove_button_rect = pygame.Rect(scroll_surface.get_width() - 210, y_offset - scroll_y, 190, 40)
            pygame.draw.rect(scroll_surface, (255, 0, 0), remove_button_rect, border_radius=5)
            remove_button_text = font.render("Remove", True, white)
            remove_button_text_rect = remove_button_text.get_rect(center=remove_button_rect.center)
            scroll_surface.blit(remove_button_text, remove_button_text_rect)

            y_offset += 60

        screen.blit(scroll_surface, (20, 70))

        for button in inventory_buttons:
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
    inventory_data = [{"name": item["name"], "rarity": item["rarity"], "image": item["image"]} for item in inventory]
    with open("inventory.json", "w") as f:
        json.dump(inventory_data, f)

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

music_file = "menumusic.mp3"
case_open_sound_file = "caseopen.mp3"

music_path = get_file_path("Sounds", music_file)
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.03)  
    pygame.mixer.music.play(-1)
else:
    print(f"Warning: {music_file} file not found.")

case_open_sound = None
case_open_sound_path = get_file_path("Sounds", case_open_sound_file)
if os.path.exists(case_open_sound_path):
    case_open_sound = pygame.mixer.Sound(case_open_sound_path)
    case_open_sound.set_volume(1)  
else:
    print(f"Warning: {case_open_sound_file} file not found.")

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
                screen.blit(text_surface, (10, 10))

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