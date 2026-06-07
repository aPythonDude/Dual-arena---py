import pygame
import random
import sys
import math

# --- INIT & CONSTANTS ---
pygame.init()
WIDTH, HEIGHT = 1200, 800
FLOOR_Y = HEIGHT - 120
GRAVITY = 0.8
FPS = 60

# Colors
COLOR_BG = (18, 18, 20)
COLOR_FLOOR = (28, 28, 30)
COLOR_FLOOR_LINE = (60, 60, 65)
COLOR_P1 = (180, 30, 40)         
COLOR_P2 = (40, 90, 160)         
COLOR_INK = (10, 10, 10)
COLOR_WHITE = (230, 230, 220)
COLOR_STEEL = (150, 155, 160)
COLOR_BLOOD = (138, 3, 3)
COLOR_ULT = (255, 215, 0) 
COLOR_GOD = (255, 245, 180) 
COLOR_NECRO = (50, 205, 50) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHADOW CLASH: Ultimate Edition")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont('georgia', 64, bold=True)
font_main = pygame.font.SysFont('georgia', 20, bold=True)
font_small = pygame.font.SysFont('courier', 14, bold=True)
font_large = pygame.font.SysFont('georgia', 54, bold=True)
font_mega = pygame.font.SysFont('impact', 100, italic=True)

hit_stop, shake_duration, shake_intensity = 0, 0, 0
cinematic = {'active': False, 'timer': 0, 'max_timer': 0, 'owner': None, 'target': None, 'is_execution': False, 'data': {}}
lightning_timer = 0

def trigger_hit_stop(frames):
    global hit_stop; hit_stop = frames

def trigger_screen_shake(intensity, duration):
    global shake_duration, shake_intensity
    shake_intensity, shake_duration = intensity, duration

def draw_rect_alpha(surface, color, rect, border_radius=0):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border_radius)
    surface.blit(shape_surf, rect)

# --- STAGE DATA ---
STAGES = [
    {'name': 'THE DOJO', 'bg': (18,18,20), 'floor': (28,28,30), 'line': (60,60,65), 'obstacles': [], 'obs_color': (0,0,0), 'weather': 'SAKURA'},
    {'name': 'BAMBOO GROVE', 'bg': (20,28,22), 'floor': (30,40,32), 'line': (50,70,55), 'obstacles': [pygame.Rect(250, FLOOR_Y - 100, 40, 100), pygame.Rect(WIDTH - 290, FLOOR_Y - 100, 40, 100)], 'obs_color': (45,65,45), 'weather': 'RAIN'},
    {'name': 'RUINED TEMPLE', 'bg': (28,22,22), 'floor': (40,30,30), 'line': (70,50,50), 'obstacles': [pygame.Rect(WIDTH//2 - 150, FLOOR_Y - 60, 300, 60)], 'obs_color': (55,45,45), 'weather': 'ASH'},
    {'name': 'FROZEN PEAK', 'bg': (15, 25, 40), 'floor': (200, 210, 220), 'line': (150, 180, 200), 'obstacles': [pygame.Rect(100, FLOOR_Y - 80, 150, 80), pygame.Rect(WIDTH - 250, FLOOR_Y - 80, 150, 80)], 'obs_color': (180, 190, 210), 'weather': 'SNOW'},
    {'name': 'THUNDER CANYON', 'bg': (10, 10, 15), 'floor': (20, 20, 25), 'line': (100, 100, 120), 'obstacles': [pygame.Rect(WIDTH//2 - 50, FLOOR_Y - 120, 100, 120)], 'obs_color': (15, 15, 20), 'weather': 'STORM'},
    {'name': 'VOLCANIC CRATER', 'bg': (35, 10, 10), 'floor': (45, 20, 20), 'line': (200, 50, 0), 'obstacles': [pygame.Rect(WIDTH//2 - 80, FLOOR_Y - 90, 160, 90)], 'obs_color': (60, 25, 25), 'weather': 'ASH'},
    {'name': 'CRYSTAL CAVERN', 'bg': (10, 15, 30), 'floor': (25, 35, 60), 'line': (0, 200, 255), 'obstacles': [pygame.Rect(150, FLOOR_Y - 60, 80, 60), pygame.Rect(WIDTH - 230, FLOOR_Y - 60, 80, 60)], 'obs_color': (40, 50, 90), 'weather': 'SNOW'},
    {'name': 'NEON METROPOLIS', 'bg': (5, 5, 15), 'floor': (20, 20, 25), 'line': (255, 0, 150), 'obstacles': [pygame.Rect(300, FLOOR_Y - 120, 60, 120), pygame.Rect(WIDTH - 360, FLOOR_Y - 120, 60, 120)], 'obs_color': (30, 20, 40), 'weather': 'RAIN'},
    {'name': 'TOXIC WASTELAND', 'bg': (15, 35, 15), 'floor': (30, 50, 30), 'line': (100, 255, 100), 'obstacles': [pygame.Rect(WIDTH//2 - 150, FLOOR_Y - 140, 300, 20), pygame.Rect(150, FLOOR_Y - 60, 80, 60), pygame.Rect(WIDTH - 230, FLOOR_Y - 60, 80, 60)], 'obs_color': (45, 80, 45), 'weather': 'RAIN'},
    {'name': 'SKY SANCTUARY', 'bg': (120, 180, 240), 'floor': (240, 240, 245), 'line': (255, 215, 0), 'obstacles': [pygame.Rect(0, FLOOR_Y - 160, 200, 160), pygame.Rect(WIDTH - 200, FLOOR_Y - 160, 200, 160)], 'obs_color': (250, 250, 255), 'weather': 'SAKURA'},
    {'name': 'ABYSSAL VOID', 'bg': (5, 0, 10), 'floor': (10, 5, 15), 'line': (138, 43, 226), 'obstacles': [pygame.Rect(WIDTH//2 - 30, FLOOR_Y - 110, 60, 110), pygame.Rect(WIDTH//4, FLOOR_Y - 50, 40, 50), pygame.Rect(WIDTH*3//4 - 40, FLOOR_Y - 50, 40, 50)], 'obs_color': (20, 10, 30), 'weather': 'ASH'},
    {'name': 'FACTORY LABYRINTH', 'bg': (20, 20, 25), 'floor': (40, 40, 45), 'line': (200, 100, 0), 'obstacles': [pygame.Rect(200, FLOOR_Y - 80, 50, 80), pygame.Rect(400, FLOOR_Y - 160, 50, 160), pygame.Rect(750, FLOOR_Y - 160, 50, 160), pygame.Rect(950, FLOOR_Y - 80, 50, 80)], 'obs_color': (60, 60, 65), 'weather': 'ASH'},
    {'name': 'TREETOP VILLAGE', 'bg': (10, 30, 20), 'floor': (50, 35, 20), 'line': (100, 200, 100), 'obstacles': [pygame.Rect(100, FLOOR_Y - 150, 80, 150), pygame.Rect(400, FLOOR_Y - 200, 80, 200), pygame.Rect(720, FLOOR_Y - 200, 80, 200), pygame.Rect(1020, FLOOR_Y - 150, 80, 150)], 'obs_color': (40, 60, 30), 'weather': 'SAKURA'},
    {'name': 'SPIKED CHASM', 'bg': (30, 10, 10), 'floor': (20, 10, 10), 'line': (255, 50, 50), 'obstacles': [pygame.Rect(150, FLOOR_Y - 50, 40, 50), pygame.Rect(250, FLOOR_Y - 100, 40, 100), pygame.Rect(350, FLOOR_Y - 150, 40, 150), pygame.Rect(WIDTH - 390, FLOOR_Y - 150, 40, 150), pygame.Rect(WIDTH - 290, FLOOR_Y - 100, 40, 100), pygame.Rect(WIDTH - 190, FLOOR_Y - 50, 40, 50)], 'obs_color': (50, 20, 20), 'weather': 'STORM'}
]
current_stage_idx = 0

# --- PROCEDURAL DRAWING ENGINE ---
def draw_character_model(surface, x, y, facing, c_type, color, anim_timer, is_attacking=False, current_attack=None, is_hit=False, vel_x=0, is_parrying=False):
    cx, cy = x + 25, y + 50
    is_idle = not is_attacking and not is_hit and not is_parrying and abs(vel_x) < 0.5
    
    run_cycle = math.sin(anim_timer * 2.5) * 20 if not is_idle else 0
    wave = math.sin(anim_timer * 1.5) * 5 if is_idle else 0
    
    if c_type == 'GOD':
        wave = math.sin(anim_timer * 2.0) * 15
        head_y = y - 20 + wave
        pygame.draw.ellipse(surface, COLOR_ULT, (cx - 30, head_y - 35, 60, 15), 3)
        pygame.draw.circle(surface, COLOR_ULT, (cx, int(head_y) + 30), 60 + math.sin(anim_timer*4)*5, 2)
        pygame.draw.polygon(surface, COLOR_WHITE, [(cx, head_y), (cx - 20, head_y + 80), (cx + 20, head_y + 80)])
        pygame.draw.circle(surface, COLOR_WHITE, (cx, int(head_y)), 15)
        hand_x, hand_y = cx + facing * 35, head_y + 40
        if is_attacking:
            hand_x, hand_y = cx + facing * 60, head_y + 30
            pygame.draw.circle(surface, COLOR_ULT, (hand_x, hand_y), 20)
            pygame.draw.line(surface, COLOR_ULT, (cx, head_y+30), (hand_x, hand_y), 5)
        pygame.draw.circle(surface, COLOR_ULT, (hand_x, hand_y), 10)
        pygame.draw.circle(surface, COLOR_WHITE, (hand_x, hand_y), 5)
        return 

    elif c_type == 'ILLUSIONIST':
        head_y = y + 15 + wave/2
        # Split color body
        pygame.draw.rect(surface, COLOR_INK, (cx - 15, y + 30 + wave/2, 15, 50), border_radius=4)
        pygame.draw.rect(surface, COLOR_WHITE, (cx, y + 30 + wave/2, 15, 50), border_radius=4)
        
        # Jester hat
        pygame.draw.polygon(surface, COLOR_INK, [(cx, head_y), (cx - 15, head_y - 20), (cx - 5, head_y - 5)])
        pygame.draw.polygon(surface, COLOR_WHITE, [(cx, head_y), (cx + 15, head_y - 20), (cx + 5, head_y - 5)])
        pygame.draw.circle(surface, color, (cx - 15, int(head_y - 20)), 4)
        pygame.draw.circle(surface, color, (cx + 15, int(head_y - 20)), 4)
        
        pygame.draw.circle(surface, color, (cx, int(head_y)), 13) # Head
        
        pygame.draw.line(surface, COLOR_INK, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 10)
        pygame.draw.line(surface, COLOR_WHITE, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 10)
        
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40
            pygame.draw.line(surface, COLOR_WHITE, (hand_x, hand_y - 20), (hand_x, hand_y + 20), 4)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 35, y + 45
            pygame.draw.rect(surface, COLOR_WHITE, (hand_x, hand_y - 10, 10, 20))
            pygame.draw.rect(surface, color, (hand_x+2, hand_y - 8, 6, 16))
        pygame.draw.line(surface, color, (cx, y + 35 + wave/2), (hand_x, hand_y), 6)

    elif c_type == 'ALCHEMIST':
        head_y = y + 15 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 10)
        pygame.draw.line(surface, COLOR_INK, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 10)
        
        # Plague doctor mask
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 12)
        pygame.draw.polygon(surface, COLOR_WHITE, [(cx, head_y - 5), (cx, head_y + 5), (cx + facing * 25, head_y)])
        
        pygame.draw.rect(surface, COLOR_INK, (cx - 15, y + 30 + wave/2, 30, 50), border_radius=4)
        pygame.draw.rect(surface, (0, 200, 0), (cx - 5, y + 40 + wave/2, 10, 20)) # Glowing vial on chest
        
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 30, y + 30
            pygame.draw.circle(surface, (0, 255, 0), (int(hand_x), int(hand_y - 10)), 8)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 8)

    elif c_type == 'REAPER':
        # Enhanced Reaper - Floats entirely, massive scythe always visible
        wave = math.sin(anim_timer * 2.0) * 10
        head_y = y - 10 + wave
        
        # Trailing cloak instead of legs
        for i in range(5):
            cloak_y = y + 80 + wave + i*6
            pygame.draw.line(surface, COLOR_INK, (cx - 15 + i*2, cloak_y), (cx + 15 - i*2, cloak_y), 10 - i)
            
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 15)
        pygame.draw.circle(surface, COLOR_BLOOD, (cx + facing*4, int(head_y - 2)), 3) # Glowing eye
        pygame.draw.polygon(surface, color, [(cx - 20, head_y), (cx + 20, head_y), (cx, head_y - 30)])
        pygame.draw.rect(surface, COLOR_INK, (cx - 15, head_y + 15, 30, 60), border_radius=6)
        
        # Giant Scythe
        hand_x, hand_y = cx + facing * 25, head_y + 40
        scythe_handle_top = (hand_x - facing*15, hand_y - 60)
        scythe_handle_bot = (hand_x + facing*20, hand_y + 80)
        
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, head_y + 20
            scythe_handle_top = (hand_x, hand_y - 50)
            scythe_handle_bot = (hand_x, hand_y + 50)
            pygame.draw.line(surface, COLOR_STEEL, scythe_handle_top, scythe_handle_bot, 6)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 40, head_y + 30
            scythe_handle_top = (hand_x + facing*40, hand_y + 30)
            scythe_handle_bot = (hand_x - facing*30, hand_y - 40)
            pygame.draw.line(surface, COLOR_STEEL, scythe_handle_top, scythe_handle_bot, 6)
            # Scythe Blade striking
            pygame.draw.polygon(surface, COLOR_STEEL, [scythe_handle_top, (scythe_handle_top[0] - facing*80, scythe_handle_top[1] + 20), (scythe_handle_top[0] - facing*20, scythe_handle_top[1] - 10)])
            pygame.draw.arc(surface, COLOR_BLOOD, pygame.Rect(hand_x - 60, hand_y - 60, 120, 120), 0, math.pi, 8)
        else:
            pygame.draw.line(surface, COLOR_STEEL, scythe_handle_top, scythe_handle_bot, 6)
            # Scythe Blade Idle
            pygame.draw.polygon(surface, COLOR_STEEL, [scythe_handle_top, (scythe_handle_top[0] + facing*60, scythe_handle_top[1] + 20), (scythe_handle_top[0] + facing*10, scythe_handle_top[1] + 10)])
        
        pygame.draw.line(surface, COLOR_INK, (cx, head_y + 25), (hand_x, hand_y), 8)

    elif c_type == 'NECROMANCER':
        wave = math.sin(anim_timer * 1.5) * 8
        head_y = y + 10 + wave
        pygame.draw.polygon(surface, COLOR_INK, [(cx, head_y), (cx - 30, y + 100 + wave), (cx + 30, y + 100 + wave)])
        pygame.draw.polygon(surface, color, [(cx, head_y+10), (cx - 20, y + 90 + wave), (cx + 20, y + 90 + wave)])
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 14)
        pygame.draw.circle(surface, COLOR_NECRO, (cx + facing * 5, int(head_y)), 3) 
        hand_x, hand_y = cx + facing * 30, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40 + wave
            pygame.draw.circle(surface, COLOR_NECRO, (hand_x, hand_y - 20), 20, 2)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 40, y + 45 + wave
            pygame.draw.circle(surface, COLOR_NECRO, (hand_x, hand_y), 15)
        pygame.draw.circle(surface, COLOR_WHITE, (hand_x, hand_y), 6)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave), (hand_x, hand_y), 6)

    elif c_type == 'HACKER':
        head_y = y + 15 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 10)
        pygame.draw.line(surface, COLOR_INK, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 10)
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 13)
        pygame.draw.line(surface, (0, 255, 0), (cx, head_y - 2), (cx + facing*12, head_y - 2), 4)
        pygame.draw.rect(surface, color, (cx - 15, y + 30 + wave/2, 30, 45), border_radius=4)
        lap_w = 20
        lap_x = cx + (5 if facing == 1 else -25)
        lap_y = y + 50 + wave/2
        pygame.draw.rect(surface, (80, 80, 80), (lap_x, lap_y, lap_w, 4))
        scr_x = cx + (25 if facing == 1 else -29)
        pygame.draw.rect(surface, (40, 40, 40), (scr_x, lap_y - 16, 4, 16))
        pygame.draw.circle(surface, (0, 255, 0), (int(scr_x - facing*2), int(lap_y - 8)), 3)
        type_w = math.sin(anim_timer * 15) * 4 if is_attacking else 0
        hand_x = cx + facing * 15
        hand_y = lap_y - 2 + type_w
        if is_parrying:
            for i in range(3):
                px_x = cx + facing*20 + facing*i*10
                pygame.draw.line(surface, (0, 255, 0), (px_x, y + 20 + i*10), (px_x, y + 100 - i*10), 2)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 6)

    elif c_type == 'PIRATE':
        head_y = y + 20 + wave/2
        pygame.draw.line(surface, (139, 69, 19), (cx - 5, y + 80), (cx - 10 + run_cycle, y + 110), 8) 
        pygame.draw.line(surface, COLOR_INK, (cx + 5, y + 80), (cx + 10 - run_cycle, y + 110), 8) 
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 12)
        pygame.draw.rect(surface, (200, 30, 30), (cx-12, head_y-14, 24, 6)) 
        bandana_x = cx - facing * 12
        pygame.draw.line(surface, (200, 30, 30), (bandana_x, head_y-10), (bandana_x - facing*15, head_y+wave), 4)
        pygame.draw.polygon(surface, color, [(cx - 15, y + 30 + wave/2), (cx + 15, y + 30 + wave/2), (cx + 10, y + 80), (cx - 10, y + 80)])
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y - 20), (hand_x, hand_y + 20), 4)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 40, y + 45
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*10, hand_y), (hand_x + facing*30, hand_y - 10), 4)
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*10, hand_y+10), (hand_x + facing*30, hand_y + 20), 4)
        else:
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*5, hand_y), (hand_x + facing*15, hand_y - 15), 4)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 6)

    elif c_type == 'KNIGHT':
        head_y = y + 15 + wave/4
        pygame.draw.line(surface, COLOR_STEEL, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 14)
        pygame.draw.line(surface, COLOR_STEEL, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 14)
        pygame.draw.rect(surface, COLOR_STEEL, (cx - 12, head_y - 15, 24, 25), border_radius=4)
        pygame.draw.rect(surface, COLOR_INK, (cx + facing*2, head_y - 5, 8, 4)) 
        pygame.draw.line(surface, color, (cx, head_y - 15), (cx - facing*15, head_y - 25 + wave), 4)
        pygame.draw.rect(surface, color, (cx - 22, y + 30 + wave/4, 44, 55), border_radius=6)
        hand_x, hand_y = cx + facing * 20, y + 55 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 25, y + 40
            pygame.draw.rect(surface, COLOR_STEEL, (hand_x - 10, hand_y - 30, 20, 60))
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 45, y + 50
            pygame.draw.line(surface, COLOR_WHITE, (hand_x - facing*30, hand_y), (hand_x + facing*60, hand_y), 12)
        else:
            pygame.draw.line(surface, COLOR_WHITE, (hand_x - facing*20, hand_y - 30), (hand_x + facing*20, hand_y + 30), 10)
        pygame.draw.line(surface, COLOR_STEEL, (cx, y + 35 + wave/4), (hand_x, hand_y), 12)

    elif c_type == 'NINJA':
        crouch = 25 if is_idle else (15 if not is_parrying else 25)
        head_y = y + 25 + crouch + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 5, y + 70 + crouch), (cx - 15 + run_cycle, y + 110), 8)
        pygame.draw.line(surface, COLOR_INK, (cx + 5, y + 70 + crouch), (cx + 15 - run_cycle, y + 110), 8)
        scarf_x = cx - facing * 10
        for i in range(4):
            sx = scarf_x - facing * (i * 8 + math.sin(anim_timer * 3 + i) * 6) - (run_cycle/2)
            sy = head_y + i * 3 + math.cos(anim_timer * 4 + i) * 4
            pygame.draw.circle(surface, color, (int(sx), int(sy)), max(1, 5 - i))
        pygame.draw.circle(surface, COLOR_INK, (cx + facing * 5, int(head_y)), 12)
        pygame.draw.rect(surface, COLOR_WHITE, (cx + facing * 5 - (6 if facing==-1 else 0), int(head_y) - 3, 6, 3))
        pygame.draw.polygon(surface, COLOR_INK, [(cx - 10, head_y + 10), (cx + 15, head_y + 10), (cx + 10, y + 70 + crouch), (cx - 15, y + 70 + crouch)])
        pygame.draw.rect(surface, color, (cx - 12, y + 60 + crouch, 24, 6)) 
        hand1_x, hand1_y = cx + facing * 25, y + 55 + crouch + wave
        hand2_x, hand2_y = cx - facing * 10, y + 60 + crouch - wave
        if is_parrying:
            hand1_x, hand1_y = cx + facing * 30, y + 40 + crouch
            hand2_x, hand2_y = cx + facing * 20, y + 30 + crouch
            pygame.draw.line(surface, COLOR_STEEL, (hand1_x, hand1_y), (hand1_x, hand1_y - 20), 4)
            pygame.draw.line(surface, COLOR_STEEL, (hand2_x, hand2_y), (hand2_x + facing*15, hand2_y - 15), 4)
        elif is_attacking and current_attack == 'basic':
            hand1_x, hand1_y = cx + facing * 45, y + 40 + crouch
            hand2_x, hand2_y = cx + facing * 35, y + 55 + crouch
            pygame.draw.line(surface, COLOR_WHITE, (hand1_x, hand1_y), (hand1_x + facing*20, hand1_y - 15), 4)
            pygame.draw.line(surface, COLOR_WHITE, (hand2_x, hand2_y), (hand2_x + facing*20, hand2_y + 10), 4)
        elif is_hit:
            hand1_x, hand1_y = cx - facing * 15, y + 40 + crouch
        elif is_idle:
            hand1_x, hand1_y = cx + facing * 15, y + 55 + crouch + wave
            hand2_x, hand2_y = cx - facing * 5, y + 55 + crouch - wave
            pygame.draw.line(surface, COLOR_STEEL, (hand1_x, hand1_y), (hand1_x - facing*10, hand1_y + 15), 4) 
            pygame.draw.line(surface, COLOR_STEEL, (hand2_x, hand2_y), (hand2_x + facing*15, hand2_y + 5), 4)
        else:
            pygame.draw.line(surface, COLOR_STEEL, (hand1_x, hand1_y), (hand1_x + facing*15, hand1_y - 15), 4) 
            pygame.draw.line(surface, COLOR_STEEL, (hand2_x, hand2_y), (hand2_x + facing*15, hand2_y + 5), 4)  
        pygame.draw.line(surface, COLOR_INK, (cx, y + 40 + crouch + wave/2), (hand1_x, hand1_y), 6) 
        pygame.draw.line(surface, COLOR_INK, (cx, y + 40 + crouch + wave/2), (hand2_x, hand2_y), 6) 

    elif c_type == 'SAMURAI':
        head_y = y + 15 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 12, y + 75), (cx - 20 + run_cycle, y + 110), 12)
        pygame.draw.line(surface, COLOR_INK, (cx + 12, y + 75), (cx + 20 - run_cycle, y + 110), 12)
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 14)
        pygame.draw.polygon(surface, color, [(cx, head_y - 10), (cx - 15, head_y - 20), (cx - 5, head_y - 12)])
        pygame.draw.polygon(surface, color, [(cx, head_y - 10), (cx + 15, head_y - 20), (cx + 5, head_y - 12)])
        pygame.draw.rect(surface, COLOR_WHITE, (cx - 8 if facing==-1 else cx, int(head_y) - 4, 8, 4))
        pygame.draw.polygon(surface, COLOR_INK, [(cx - 20, y + 30 + wave/2), (cx + 20, y + 30 + wave/2), (cx + 18, y + 75), (cx - 18, y + 75)])
        pygame.draw.rect(surface, COLOR_INK, (cx - 25, y + 25 + wave/2, 50, 15), border_radius=4) 
        pygame.draw.rect(surface, color, (cx - 20, y + 65, 40, 10)) 
        hand_x, hand_y = cx + facing * 20, y + 55 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 25, y + 40
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y), (hand_x, hand_y - 40), 6)
        elif is_attacking and current_attack == 'basic': 
            hand_x, hand_y = cx + facing * 50, y + 60
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*10, hand_y - 10), (hand_x + facing * 60, hand_y + 30), 6)
            pygame.draw.arc(surface, COLOR_WHITE, pygame.Rect(x - 40, y + 20, 150, 100), 4.5 if facing==1 else 1.5, 6.0 if facing==1 else 3.0, 5)
        elif is_hit:
            hand_x, hand_y = cx - facing * 10, y + 30
        elif is_idle:
            hand_x, hand_y = cx - facing * 15, y + 60 + wave
            blade_tip = (cx - facing * 40, y + 90 + wave)
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y), blade_tip, 8) 
        else:
            blade_tip = (cx - facing * 25, y - 10 + wave * 2)
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y), blade_tip, 6)
        pygame.draw.line(surface, COLOR_INK, (cx + facing*10, y + 35 + wave/2), (hand_x, hand_y), 10)

    elif c_type == 'MONK':
        head_y = y + 20 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 5, y + 85), (cx - 10 + run_cycle, y + 110), 9) 
        pygame.draw.line(surface, COLOR_INK, (cx + 5, y + 85), (cx + 10 - run_cycle, y + 110), 9) 
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 12)
        pygame.draw.polygon(surface, color, [(cx - 25, head_y - 2), (cx + 25, head_y - 2), (cx, head_y - 15)])
        pygame.draw.polygon(surface, COLOR_INK, [(cx - 15, y + 30 + wave/2), (cx + 15, y + 30 + wave/2), (cx + 25, y + 85), (cx - 25, y + 85)])
        pygame.draw.circle(surface, color, (cx, y + 45 + wave/2), 10, 3) 
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 30, y + 50
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y - 50), (hand_x, hand_y + 50), 5)
        elif is_attacking and current_attack == 'basic': 
            hand_x, hand_y = cx + facing * 40, y + 50
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*30, hand_y), (hand_x + facing * 80, hand_y), 5)
        elif is_hit:
            hand_x, hand_y = cx - facing * 15, y + 30
        elif is_idle:
            hand_x, hand_y = cx + facing * 15, y + 50 + wave
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y - 50), (hand_x, y + 110), 5)
        else:
            staff_tilt = math.sin(anim_timer) * 15
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - staff_tilt, hand_y - 40), (hand_x + staff_tilt, hand_y + 60), 5)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 7)

    elif c_type == 'ARCHER':
        head_y = y + 20 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 8, y + 80), (cx - 12 + run_cycle, y + 110), 8) 
        pygame.draw.line(surface, COLOR_INK, (cx + 8, y + 80), (cx + 12 - run_cycle, y + 110), 8) 
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 12)
        pygame.draw.polygon(surface, color, [(cx - 15, head_y + 5), (cx + 15, head_y + 5), (cx, head_y - 18)])
        pygame.draw.rect(surface, COLOR_INK, (cx - 15, y + 30 + wave/2, 30, 50), border_radius=4)
        pygame.draw.rect(surface, color, (cx - 15, y + 45 + wave/2, 30, 15))
        pygame.draw.line(surface, COLOR_STEEL, (cx - facing * 10, y + 30), (cx - facing * 20, y + 70), 8)
        pygame.draw.line(surface, COLOR_WHITE, (cx - facing * 15, y + 25), (cx - facing * 10, y + 15), 2)
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40
            pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y - 30), (hand_x, hand_y + 30), 6)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 35, y + 45
            bow_rect = pygame.Rect(hand_x - 15, hand_y - 40, 30, 80)
            if facing == 1:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, -math.pi/2, math.pi/2, 4)
            else:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, math.pi/2, 3*math.pi/2, 4)
            pygame.draw.line(surface, COLOR_WHITE, (hand_x, hand_y - 40), (hand_x - facing*20, hand_y), 1)
            pygame.draw.line(surface, COLOR_WHITE, (hand_x, hand_y + 40), (hand_x - facing*20, hand_y), 1)
        elif is_hit:
            hand_x, hand_y = cx - facing * 10, y + 35
        elif is_idle:
            hand_x, hand_y = cx + facing * 15, y + 60 + wave
            bow_rect = pygame.Rect(hand_x - 10, hand_y - 20, 20, 60)
            if facing == 1:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, -math.pi/4, 3*math.pi/4, 4)
            else:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, math.pi/4, 5*math.pi/4, 4)
            pygame.draw.line(surface, COLOR_WHITE, (hand_x - 7, hand_y - 15), (hand_x + 7, hand_y + 35), 1)
        else:
            bow_rect = pygame.Rect(hand_x - 10, hand_y - 30, 20, 60)
            if facing == 1:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, -math.pi/2, math.pi/2, 4)
            else:
                pygame.draw.arc(surface, COLOR_STEEL, bow_rect, math.pi/2, 3*math.pi/2, 4)
            pygame.draw.line(surface, COLOR_WHITE, (hand_x, hand_y - 30), (hand_x, hand_y + 30), 1)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 7)

    elif c_type == 'BRAWLER':
        head_y = y + 20 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 15, y + 80), (cx - 20 + run_cycle, y + 110), 14) 
        pygame.draw.line(surface, COLOR_INK, (cx + 15, y + 80), (cx + 20 - run_cycle, y + 110), 14) 
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 14)
        pygame.draw.rect(surface, color, (cx - 12 if facing == -1 else cx + 4, int(head_y) - 2, 8, 4))
        pygame.draw.polygon(surface, COLOR_INK, [(cx - 25, y + 30 + wave/2), (cx + 25, y + 30 + wave/2), (cx + 15, y + 80), (cx - 15, y + 80)])
        pygame.draw.rect(surface, color, (cx - 25, y + 30 + wave/2, 50, 20), border_radius=4)
        hand1_x, hand1_y = cx + facing * 25, y + 45 + wave
        hand2_x, hand2_y = cx + facing * 10, y + 40 - wave
        if is_parrying:
            hand1_x, hand1_y = cx + facing * 20, y + 30
            hand2_x, hand2_y = cx + facing * 15, y + 20
        elif is_attacking and current_attack == 'basic':
            hand1_x, hand1_y = cx + facing * 50, y + 45
            hand2_x, hand2_y = cx + facing * 30, y + 45
            pygame.draw.line(surface, COLOR_WHITE, (cx, y + 45), (hand1_x, hand1_y), 3)
        elif is_hit:
            hand1_x, hand1_y = cx - facing * 10, y + 35
            hand2_x, hand2_y = cx - facing * 20, y + 40
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand1_x, hand1_y), 10)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand2_x, hand2_y), 10)
        pygame.draw.circle(surface, color, (int(hand1_x), int(hand1_y)), 12)
        pygame.draw.circle(surface, color, (int(hand2_x), int(hand2_y)), 12)
        
    elif c_type == 'MAGE':
        wave *= 2
        head_y = y + 10 + wave
        pygame.draw.polygon(surface, color, [(cx, head_y), (cx - 25, y + 100 + wave), (cx + 25, y + 100 + wave)])
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 12)
        pygame.draw.polygon(surface, COLOR_INK, [(cx - 15, head_y + 5), (cx + 15, head_y + 5), (cx, head_y - 15)])
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40 + wave
            pygame.draw.circle(surface, COLOR_WHITE, (hand_x, hand_y - 45), 15, 2)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 35, y + 45 + wave
            pygame.draw.circle(surface, COLOR_ULT, (hand_x + facing*20, hand_y), 15)
        pygame.draw.line(surface, COLOR_STEEL, (hand_x, hand_y - 40), (hand_x, hand_y + 40), 4)
        pygame.draw.circle(surface, COLOR_WHITE, (hand_x, hand_y - 45), 8)
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave), (hand_x, hand_y), 6)

    elif c_type == 'VALKYRIE':
        head_y = y + 15 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 10)
        pygame.draw.line(surface, COLOR_INK, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 10)
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 13)
        pygame.draw.line(surface, COLOR_WHITE, (cx - 15, head_y - 10), (cx - 25, head_y - 20), 3)
        pygame.draw.line(surface, COLOR_WHITE, (cx + 15, head_y - 10), (cx + 25, head_y - 20), 3)
        pygame.draw.rect(surface, color, (cx - 15, y + 30 + wave/2, 30, 45), border_radius=5)
        hand_x, hand_y = cx + facing * 20, y + 50 + wave
        if is_parrying:
            pygame.draw.polygon(surface, COLOR_WHITE, [(cx + facing*20, y+20), (cx + facing*10, y+30), (cx + facing*20, y+90)])
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 40, y + 50
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*40, hand_y), (hand_x + facing*70, hand_y), 5) 
            pygame.draw.polygon(surface, COLOR_WHITE, [(hand_x + facing*70, hand_y), (hand_x + facing*60, hand_y - 5), (hand_x + facing*60, hand_y + 5)])
        else:
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*40, hand_y - 10), (hand_x + facing*50, hand_y - 10), 5) 
        if not is_parrying:
            pygame.draw.polygon(surface, COLOR_WHITE, [(cx - facing*10, y+35), (cx - facing*20, y+45), (cx - facing*10, y+70)]) 
        pygame.draw.line(surface, COLOR_INK, (cx, y + 35 + wave/2), (hand_x, hand_y), 8)
        
    elif c_type == 'CYBORG':
        head_y = y + 15 + wave/2
        pygame.draw.line(surface, COLOR_INK, (cx - 10, y + 80), (cx - 15 + run_cycle, y + 110), 12)
        pygame.draw.line(surface, COLOR_INK, (cx + 10, y + 80), (cx + 15 - run_cycle, y + 110), 12)
        pygame.draw.circle(surface, COLOR_INK, (cx, int(head_y)), 14)
        pygame.draw.circle(surface, (255, 0, 0), (cx + facing * 5, int(head_y) - 2), 3) 
        pygame.draw.rect(surface, color, (cx - 15, y + 30 + wave/2, 30, 50), border_radius=2)
        hand_x, hand_y = cx + facing * 25, y + 50 + wave
        if is_parrying:
            hand_x, hand_y = cx + facing * 20, y + 40
            pygame.draw.circle(surface, (0, 255, 255), (hand_x, hand_y), 20, 2)
        elif is_attacking and current_attack == 'basic':
            hand_x, hand_y = cx + facing * 45, y + 50
            pygame.draw.line(surface, (0, 255, 255), (hand_x, hand_y), (hand_x + facing*30, hand_y), 8)
        else:
            pygame.draw.line(surface, COLOR_STEEL, (hand_x - facing*10, hand_y), (hand_x + facing*15, hand_y), 8)
        pygame.draw.line(surface, COLOR_STEEL, (cx, y + 35 + wave/2), (hand_x, hand_y), 10)

# --- CLASSES ---
class WeatherParticle:
    def __init__(self, w_type):
        self.w_type = w_type
        self.x = random.randint(-200, WIDTH + 200)
        self.y = random.randint(-100, 0) if w_type != 'ASH' else FLOOR_Y + random.randint(0, 50)
        self.active = True
        
        if w_type == 'RAIN':
            self.vel_y, self.vel_x = random.uniform(15, 25), random.uniform(1, 3)
            self.length = random.uniform(10, 30)
            self.color = (100, 120, 150, 100)
        elif w_type == 'STORM':
            self.vel_y, self.vel_x = random.uniform(25, 40), random.uniform(4, 8)
            self.length = random.uniform(20, 45)
            self.color = (130, 150, 180, 150)
        elif w_type == 'SNOW':
            self.vel_y, self.vel_x = random.uniform(1, 4), random.uniform(-1, 1)
            self.size = random.uniform(2, 5)
            self.color = (255, 255, 255, random.randint(150, 220))
        elif w_type == 'ASH':
            self.vel_y, self.vel_x = random.uniform(-1, -4), random.uniform(-2, 2)
            self.size = random.uniform(2, 6)
            self.color = random.choice([(255, 100, 0, 200), (255, 50, 0, 150), (100, 100, 100, 100)])
        elif w_type == 'SAKURA':
            self.vel_y, self.vel_x = random.uniform(1, 3), random.uniform(1, 3.5)
            self.size = random.uniform(3, 7)
            self.color = (255, 183, 197, random.randint(150, 220))

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        if self.w_type == 'SNOW': 
            self.x += math.sin(self.y / 20) * 1.5
        elif self.w_type == 'ASH':
            self.x += math.sin(self.y / 30) * 2
        elif self.w_type == 'SAKURA':
            self.x += math.sin(self.y / 40) * 2.5
            
        if self.y > HEIGHT + 50 or self.y < -150 or self.x > WIDTH + 300 or self.x < -300:
            self.active = False

    def draw(self, offset_x, offset_y):
        if self.w_type in ['RAIN', 'STORM']:
            pygame.draw.line(screen, self.color[:3], (self.x + offset_x, self.y + offset_y), 
                             (self.x - self.vel_x + offset_x, self.y - self.length + offset_y), 2)
        else:
            surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            if self.w_type == 'SAKURA':
                pygame.draw.ellipse(surf, self.color, (0, 0, self.size*2, self.size))
            else:
                pygame.draw.circle(surf, self.color, (self.size, self.size), self.size)
            screen.blit(surf, (self.x + offset_x, self.y + offset_y))

class Particle:
    def __init__(self, x, y, color, speed_m=1.0, is_blood=False):
        self.x, self.y = x, y
        self.color = COLOR_BLOOD if is_blood else color
        self.is_blood = is_blood
        self.size = random.uniform(4, 9) if is_blood else random.uniform(2, 6)
        self.vel_x = random.uniform(-10, 10) * speed_m
        self.vel_y = random.uniform(-15, 3) * speed_m if is_blood else random.uniform(-8, 8) * speed_m
        self.life, self.decay = 255.0, random.uniform(6, 12) if is_blood else random.uniform(4, 8)

    def update(self):
        if self.is_blood: self.vel_y += 0.5 
        else: self.vel_x *= 0.95; self.vel_y *= 0.95
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= self.decay
        self.size = max(0.1, self.size * 0.95)

    def draw(self, offset_x, offset_y):
        if self.life > 0:
            c = (*self.color, int(max(0, self.life)))
            draw_rect_alpha(screen, c, (self.x + offset_x, self.y + offset_y, self.size, self.size), border_radius=2)

class FloatingText:
    def __init__(self, x, y, text, color, mega=False):
        self.x, self.y, self.text, self.color, self.mega = x + random.uniform(-20, 20), y, text, color, mega
        self.life, self.max_life, self.vel_y = (120, 120, -0.5) if mega else (60, 60, -1.5)

    def update(self):
        self.y += self.vel_y; self.life -= 1

    def draw(self, offset_x, offset_y):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            f = font_mega if self.mega else font_main
            text_surf = f.render(self.text, True, self.color)
            text_surf.set_alpha(alpha)
            screen.blit(text_surf, text_surf.get_rect(center=(self.x + offset_x, self.y + offset_y)))

class Projectile:
    def __init__(self, x, y, vel_x, vel_y, color, damage, owner, p_type='shuriken'):
        self.p_type = p_type
        if p_type == 'shockwave': self.rect = pygame.Rect(x, FLOOR_Y - 20, 40, 20)
        elif p_type in ['orb', 'skull', 'smoke']: self.rect = pygame.Rect(x, y - 20, 40, 40)
        elif p_type == 'code': self.rect = pygame.Rect(x, y - 10, 40, 20)
        elif p_type == 'virus': self.rect = pygame.Rect(x, y - 25, 50, 50)
        elif p_type in ['arrow', 'kunai', 'card']: self.rect = pygame.Rect(x, y - 5, 30, 10)
        elif p_type == 'flask': self.rect = pygame.Rect(x, y - 5, 15, 15)
        elif p_type == 'puddle': self.rect = pygame.Rect(x - 50, FLOOR_Y - 15, 100, 15)
        else: self.rect = pygame.Rect(x, y - 5, 20, 20) 
            
        self.vel_x, self.vel_y = vel_x, vel_y
        self.color, self.damage, self.owner = color, damage, owner
        self.active, self.facing = True, 1 if vel_x > 0 else -1
        self.rot = 0
        self.life = 120 if p_type in ['puddle', 'smoke'] else 255

    def update(self):
        if self.p_type == 'flask':
            self.vel_y += 0.5 # gravity
            if self.rect.bottom >= FLOOR_Y:
                self.rect.bottom = FLOOR_Y
                self.p_type = 'puddle'
                self.rect = pygame.Rect(self.rect.centerx - 60, FLOOR_Y - 15, 120, 15)
                self.vel_x = 0; self.vel_y = 0
                self.life = 150
                self.damage = 20 # Multi-hit
                trigger_screen_shake(3, 5)
                spawn_particles(self.rect.centerx, self.rect.centery, (0, 200, 0), 20)
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        if self.p_type in ['shuriken', 'card', 'flask']: self.rot += 15
        
        if self.p_type in ['smoke', 'puddle']:
            self.life -= 1
            if self.life <= 0: self.active = False
        elif not screen.get_rect().colliderect(self.rect): 
            self.active = False
        
        stage = STAGES[current_stage_idx]
        for obs in stage['obstacles']:
            if self.rect.colliderect(obs) and self.p_type not in ['orb', 'skull', 'virus', 'smoke', 'puddle']: 
                spawn_particles(self.rect.centerx, self.rect.centery, COLOR_WHITE, 10)
                self.active = False
                return

        enemy = self.owner.enemy
        targets = [enemy] + enemy.minions
        
        for target in targets:
            if target.is_dead: continue
            
            check_rect = target.rect.inflate(60, 60) if getattr(target, 'c_type', None) == 'GOD' else target.rect
            
            if self.active and self.rect.colliderect(check_rect) and target.invincible <= 0:
                if getattr(target, 'c_type', None) == 'GOD':
                    target.god_shield_timer = 20
                    spawn_particles(self.rect.centerx, self.rect.centery, COLOR_ULT, 15)
                    self.active = False
                    return

                if target.is_parrying:
                    self.vel_x *= -1.2 
                    self.facing *= -1
                    self.owner = target
                    self.color = target.color if hasattr(target, 'color') else COLOR_WHITE
                    spawn_particles(self.rect.centerx, self.rect.centery, COLOR_WHITE, 25, speed_m=1.5)
                    trigger_hit_stop(8)
                    self.rect.x += self.vel_x * 2 
                else:
                    target.take_damage(self.damage, 1 if self.vel_x > 0 else -1, 4)
                    spawn_particles(self.rect.centerx, self.rect.centery, self.color, 20, is_blood=True)
                    if self.p_type in ['orb', 'skull', 'virus']: trigger_screen_shake(8, 5)
                    
                    if self.p_type not in ['puddle', 'smoke']:
                        self.active = False
                        return 

    def draw(self, offset_x, offset_y):
        dx, dy = self.rect.centerx + offset_x, self.rect.centery + offset_y
        f = self.facing
        if self.p_type == 'shuriken':
            surf = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.polygon(surf, COLOR_STEEL, [(15,0), (20,10), (30,15), (20,20), (15,30), (10,20), (0,15), (10,10)])
            surf = pygame.transform.rotate(surf, self.rot)
            screen.blit(surf, surf.get_rect(center=(dx, dy)))
        elif self.p_type == 'card':
            surf = pygame.Surface((20, 30), pygame.SRCALPHA)
            pygame.draw.rect(surf, COLOR_WHITE, (0, 0, 20, 30), border_radius=2)
            pygame.draw.rect(surf, COLOR_BLOOD, (5, 5, 10, 20))
            surf = pygame.transform.rotate(surf, self.rot)
            screen.blit(surf, surf.get_rect(center=(dx, dy)))
        elif self.p_type == 'flask':
            surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 200, 0), (10, 15), 5)
            pygame.draw.rect(surf, COLOR_WHITE, (8, 0, 4, 10))
            surf = pygame.transform.rotate(surf, self.rot)
            screen.blit(surf, surf.get_rect(center=(dx, dy)))
        elif self.p_type == 'puddle':
            alpha = min(255, int(self.life * 2))
            draw_rect_alpha(screen, (0, 200, 0, alpha), (self.rect.x + offset_x, self.rect.y + offset_y, self.rect.w, self.rect.h), border_radius=5)
        elif self.p_type == 'smoke':
            alpha = min(200, int(self.life * 2))
            pygame.draw.circle(screen, (100, 100, 100), (dx, dy), 40 + math.sin(self.life/5.0)*10)
            draw_rect_alpha(screen, (100, 100, 100, alpha), (self.rect.x + offset_x, self.rect.y + offset_y, self.rect.w, self.rect.h), border_radius=20)
        elif self.p_type == 'shockwave':
            points = [(dx+20*f, self.rect.bottom+offset_y), (dx, self.rect.top+offset_y), (dx-20*f, self.rect.bottom+offset_y)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.p_type == 'orb':
            pygame.draw.circle(screen, (*self.color, 150), (dx, dy), 20 + math.sin(self.rot/10)*5)
            pygame.draw.circle(screen, COLOR_WHITE, (dx, dy), 12)
        elif self.p_type == 'code':
            txt = font_small.render("0110", True, (0, 255, 0))
            screen.blit(txt, txt.get_rect(center=(dx, dy)))
        elif self.p_type == 'virus':
            pygame.draw.rect(screen, (255, 0, 0), (dx - 25, dy - 25, 50, 50))
            for _ in range(5):
                pygame.draw.rect(screen, COLOR_INK, (dx - 25 + random.randint(0,40), dy - 25 + random.randint(0,40), random.randint(5,15), random.randint(2,8)))
            txt = font_small.render("ERR", True, COLOR_WHITE)
            screen.blit(txt, txt.get_rect(center=(dx, dy)))
        elif self.p_type == 'skull':
            pygame.draw.circle(screen, COLOR_NECRO, (dx, dy), 15 + math.sin(pygame.time.get_ticks()/100)*3)
            pygame.draw.circle(screen, COLOR_INK, (dx + f*5, dy - 3), 4)
            pygame.draw.circle(screen, COLOR_INK, (dx + f*10, dy - 3), 4)
        elif self.p_type == 'arrow':
            pygame.draw.line(screen, COLOR_STEEL, (dx - 15*f, dy), (dx + 15*f, dy), 3)
            pygame.draw.polygon(screen, COLOR_WHITE, [(dx + 15*f, dy), (dx + 5*f, dy - 5), (dx + 5*f, dy + 5)])
        elif self.p_type == 'kunai':
            pygame.draw.polygon(screen, COLOR_STEEL, [(dx + 15*f, dy), (dx, dy - 5), (dx - 15*f, dy - 2), (dx - 15*f, dy + 2), (dx, dy + 5)])
            pygame.draw.circle(screen, COLOR_STEEL, (dx - 18*f, dy), 4, 1)

class Minion:
    def __init__(self, owner, x, y, facing):
        self.owner = owner
        self.enemy = owner.enemy
        self.rect = pygame.Rect(x, y, 40, 90)
        self.facing = facing
        self.health = 2000
        self.max_health = 2000
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4.0
        self.is_dead = False
        self.is_hit = False
        self.hit_timer = 0
        self.is_attacking = False
        self.attack_timer = 0
        self.basic_cd = 0
        self.anim_timer = random.uniform(0, 100)
        self.grounded = False
        self.invincible = 0
        self.is_parrying = False

    def take_damage(self, amount, kb_dir, kb_power):
        if self.is_dead: return
        self.health -= amount
        self.is_hit = True
        self.hit_timer = 15
        self.vel_x = kb_dir * kb_power
        self.vel_y = -3
        spawn_particles(self.rect.centerx, self.rect.centery, COLOR_INK, 15)
        floating_texts.append(FloatingText(self.rect.centerx, self.rect.y - 20, str(amount), COLOR_WHITE))
        if self.health <= 0:
            self.is_dead = True

    def update(self):
        if self.is_dead: return
        self.anim_timer += 0.1
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.grounded = False
        
        stage = STAGES[current_stage_idx]
        if self.rect.bottom > FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.vel_y = 0
            self.grounded = True
            
        for obs in stage['obstacles']:
            if self.rect.colliderect(obs):
                if self.vel_y > 0: self.rect.bottom, self.vel_y, self.grounded = obs.top, 0, True
                elif self.vel_y < 0: self.rect.top, self.vel_y = obs.bottom, 0

        self.rect.x += self.vel_x
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        for obs in stage['obstacles']:
            if self.rect.colliderect(obs):
                if self.vel_x > 0: self.rect.right, self.vel_x = obs.left, 0
                elif self.vel_x < 0: self.rect.left, self.vel_x = obs.right, 0
        
        if self.basic_cd > 0: self.basic_cd -= 1
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0: self.is_attacking = False
        if self.is_hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0: self.is_hit = False
            
        if not self.is_attacking and not self.is_hit:
            dist = self.enemy.rect.centerx - self.rect.centerx
            if abs(dist) > 60:
                self.vel_x = self.speed if dist > 0 else -self.speed
                self.facing = 1 if dist > 0 else -1
            else:
                self.vel_x *= 0.5
                if self.basic_cd <= 0:
                    self.is_attacking = True
                    self.attack_timer = 20
                    self.basic_cd = 60
                    self.facing = 1 if dist > 0 else -1
                    hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 60, self.rect.y, 60, self.rect.height)
                    if hitbox.colliderect(self.enemy.rect):
                        self.enemy.take_damage(250, self.facing, 4)
                        if getattr(self.enemy, 'c_type', None) != 'GOD': 
                            trigger_hit_stop(3)
                            spawn_particles(self.enemy.rect.centerx, self.rect.y + 40, COLOR_BLOOD, 10, is_blood=True)

        if not self.is_hit and not self.is_attacking:
            self.vel_x *= 0.85
        
    def draw(self, off_x, off_y):
        if self.is_dead: return
        if self.is_hit and (self.hit_timer // 3) % 2 == 0:
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(surf, COLOR_WHITE, (self.rect.x+off_x, self.rect.y+off_y, self.rect.w, self.rect.height))
            screen.blit(surf, (0,0))
        else:
            cx, cy = self.rect.x + 20 + off_x, self.rect.y + 45 + off_y
            wave = math.sin(self.anim_timer * 1.5) * 5
            run_cycle = math.sin(self.anim_timer * 2.5) * 15 if abs(self.vel_x) > 0.5 else 0
            
            pygame.draw.line(screen, COLOR_INK, (cx - 5, self.rect.y + 60 + off_y), (cx - 10 + run_cycle, self.rect.bottom + off_y), 6)
            pygame.draw.line(screen, COLOR_INK, (cx + 5, self.rect.y + 60 + off_y), (cx + 10 - run_cycle, self.rect.bottom + off_y), 6)
            
            pygame.draw.circle(screen, COLOR_INK, (int(cx), int(self.rect.y + 15 + off_y + wave)), 10)
            pygame.draw.circle(screen, COLOR_NECRO, (int(cx + self.facing*3), int(self.rect.y + 13 + off_y + wave)), 2)
            pygame.draw.rect(screen, COLOR_INK, (self.rect.x + 5 + off_x, self.rect.y + 25 + off_y + wave, 30, 40), border_radius=5)
            
            hand_x, hand_y = cx + self.facing * 15, self.rect.y + 45 + off_y + wave
            if self.is_attacking:
                hand_x += self.facing * 20
                pygame.draw.line(screen, COLOR_INK, (cx, self.rect.y+35+off_y+wave), (hand_x, hand_y), 4)
                pygame.draw.line(screen, COLOR_STEEL, (hand_x - self.facing*10, hand_y), (hand_x + self.facing*30, hand_y), 5)
            else:
                pygame.draw.line(screen, COLOR_INK, (cx, self.rect.y+35+off_y+wave), (hand_x, hand_y), 4)
                pygame.draw.line(screen, COLOR_STEEL, (hand_x, hand_y - 20), (hand_x, hand_y + 20), 5)

        hp_pct = max(0, self.health / self.max_health)
        pygame.draw.rect(screen, COLOR_FLOOR, (self.rect.x + off_x - 10, self.rect.y + off_y - 15, 60, 6))
        pygame.draw.rect(screen, self.owner.color, (self.rect.x + off_x - 10, self.rect.y + off_y - 15, int(60 * hp_pct), 6))

class Fighter:
    def __init__(self, x, color, c_type, facing):
        self.start_x, self.start_facing = x, facing
        self.rect = pygame.Rect(x, FLOOR_Y - 110, 50, 110)
        self.color, self.c_type, self.facing = color, c_type, facing
        self.vel_x, self.vel_y = 0, 0
        
        # COMPLETE BALANCE PASS
        stats = {
            'SAMURAI': {'hp': 13000, 'spd': 5.5, 'jmp': -14.5, 'cd': 150},
            'NINJA': {'hp': 7500, 'spd': 10.0, 'jmp': -17.5, 'cd': 70}, 
            'MONK': {'hp': 10500, 'spd': 7.0, 'jmp': -16.0, 'cd': 110},
            'ARCHER': {'hp': 8500, 'spd': 8.5, 'jmp': -15.5, 'cd': 80},
            'REAPER': {'hp': 11500, 'spd': 5.5, 'jmp': -14.0, 'cd': 160},
            'BRAWLER': {'hp': 12500, 'spd': 8.0, 'jmp': -16.0, 'cd': 90},
            'MAGE': {'hp': 7000, 'spd': 5.5, 'jmp': -14.5, 'cd': 120},
            'VALKYRIE': {'hp': 12000, 'spd': 7.5, 'jmp': -16.5, 'cd': 110},
            'CYBORG': {'hp': 10500, 'spd': 6.5, 'jmp': -15.0, 'cd': 100},
            'PIRATE': {'hp': 10000, 'spd': 8.0, 'jmp': -15.5, 'cd': 85},
            'KNIGHT': {'hp': 15500, 'spd': 4.0, 'jmp': -12.5, 'cd': 180},
            'NECROMANCER': {'hp': 8000, 'spd': 5.5, 'jmp': -14.0, 'cd': 130},
            'HACKER': {'hp': 8500, 'spd': 7.0, 'jmp': -15.0, 'cd': 95},
            'ILLUSIONIST': {'hp': 7000, 'spd': 9.0, 'jmp': -16.5, 'cd': 80},
            'ALCHEMIST': {'hp': 9500, 'spd': 7.0, 'jmp': -15.0, 'cd': 120},
            'GOD': {'hp': 99999, 'spd': 12.0, 'jmp': -20.0, 'cd': 5} 
        }
        self.speed, self.jump_power = stats[c_type]['spd'], stats[c_type]['jmp']
        self.health = self.max_health = stats[c_type]['hp']
        self.spec_cd_max = stats[c_type]['cd']
        self.lives, self.invincible, self.ult_meter = 3, 0, 0 
        
        self.combo_count = 0
        self.combo_timer = 0
        self.god_shield_timer = 0
        
        self.is_dead, self.is_attacking, self.is_hit = False, False, False
        self.is_parrying = False
        self.grounded = False 
        self.spec_cd, self.basic_cd, self.attack_timer, self.hit_timer = 0, 0, 0, 0
        self.parry_timer, self.parry_cd = 0, 0
        self.current_attack, self.enemy = None, None
        self.anim_timer, self.shadow_trail = random.uniform(0, 100), []
        self.minions = []

    def update(self):
        if self.is_dead or cinematic['active']: return
        self.anim_timer += 0.1
        if self.invincible > 0: self.invincible -= 1
        if self.god_shield_timer > 0: self.god_shield_timer -= 1
        if self.c_type == 'GOD': self.ult_meter = 100 

        stage = STAGES[current_stage_idx]

        self.vel_y += GRAVITY

        self.rect.y += self.vel_y
        self.grounded = False

        if self.rect.bottom > FLOOR_Y: 
            self.rect.bottom, self.vel_y, self.grounded = FLOOR_Y, 0, True

        for obs in stage['obstacles']:
            if self.rect.colliderect(obs):
                if self.vel_y > 0: self.rect.bottom, self.vel_y, self.grounded = obs.top, 0, True
                elif self.vel_y < 0: self.rect.top, self.vel_y = obs.bottom, 0

        self.rect.x += self.vel_x
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        for obs in stage['obstacles']:
            if self.rect.colliderect(obs):
                if self.vel_x > 0: self.rect.right, self.vel_x = obs.left, 0
                elif self.vel_x < 0: self.rect.left, self.vel_x = obs.right, 0

        if self.spec_cd > 0: self.spec_cd -= 1
        if self.basic_cd > 0: self.basic_cd -= 1
        if self.parry_cd > 0: self.parry_cd -= 1

        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_count = 0

        if self.is_parrying:
            self.parry_timer -= 1
            self.vel_x *= 0.5 
            if self.parry_timer <= 0:
                self.is_parrying = False

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0: self.is_attacking = False
        else:
            self.shadow_trail.clear()

        if self.is_hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0: self.is_hit = False

        if not self.is_attacking and not self.is_hit and not self.is_parrying: 
            friction = 0.95 if stage['name'] == 'FROZEN PEAK' else 0.75
            self.vel_x *= friction 

    def take_damage(self, amount, kb_dir, kb_power):
        if self.is_dead or self.invincible > 0 or cinematic['active']: return
        
        if self.c_type == 'GOD':
            self.god_shield_timer = 20
            spawn_particles(self.rect.centerx, self.rect.centery, COLOR_ULT, 15)
            return

        self.health = max(0, self.health - amount)
        self.is_hit, self.hit_timer, self.is_parrying = True, 20, False
        self.vel_x, self.vel_y = kb_dir * kb_power, -4.5
        
        self.ult_meter = min(100, self.ult_meter + (amount / self.max_health) * 150)
        self.enemy.ult_meter = min(100, self.enemy.ult_meter + 5)
        
        self.enemy.combo_count += 1
        self.enemy.combo_timer = 120
        
        floating_texts.append(FloatingText(self.rect.centerx, self.rect.y - 20, str(amount), COLOR_WHITE))
        spawn_particles(self.rect.centerx, self.rect.centery, COLOR_BLOOD, 25, speed_m=1.3, is_blood=True)
        
        if self.health <= 0 and not cinematic['active']:
            self.lives -= 1
            if self.lives > 0: self.respawn()
            else: self.is_dead = True

    def respawn(self):
        self.health = self.max_health
        self.invincible = 180
        self.rect.x, self.rect.y = self.start_x, 100
        self.facing = self.start_facing
        self.vel_x, self.vel_y, self.is_attacking, self.is_hit = 0, 0, False, False
        self.is_parrying = False
        self.grounded = False 
        self.spec_cd, self.basic_cd, self.parry_cd = 0, 0, 0
        self.combo_count = 0
        self.combo_timer = 0
        self.god_shield_timer = 0
        self.minions = []

    def parry(self):
        if self.is_attacking or self.is_hit or self.is_parrying or self.parry_cd > 0 or cinematic['active']: return
        self.is_parrying = True
        self.parry_timer = 20 
        self.parry_cd = 90    

    def basic_attack(self):
        if self.is_attacking or self.is_hit or self.is_parrying or self.basic_cd > 0 or cinematic['active']: return
        self.is_attacking, self.current_attack = True, 'basic'
        
        targets = [self.enemy] + self.enemy.minions
        
        if self.c_type == 'SAMURAI':
            self.attack_timer, self.basic_cd, self.vel_x = 20, 35, self.facing * 2
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 100, self.rect.y, 100, self.rect.height)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(800, self.facing, 12)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(8); spawn_particles(t.rect.centerx, self.rect.y + 40, COLOR_BLOOD, 20, is_blood=True)
                    
        elif self.c_type == 'NINJA':
            self.attack_timer, self.basic_cd, self.vel_x = 12, 18, self.facing * 6
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 40, self.rect.y, 40, self.rect.height)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(500, self.facing, 4) 
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(4); spawn_particles(t.rect.centerx, self.rect.y + 50, COLOR_WHITE, 10)
                    
        elif self.c_type == 'MONK':
            self.attack_timer, self.basic_cd, self.vel_x = 14, 25, self.facing * 1
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 110, self.rect.y + 20, 110, 40)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(600, self.facing, 8)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(5); spawn_particles(t.rect.centerx, self.rect.y + 50, COLOR_WHITE, 10)
                    
        elif self.c_type == 'ARCHER':
            self.attack_timer, self.basic_cd, self.vel_x = 15, 22, self.facing * 1
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 20, 0, self.color, 400, self, 'arrow'))
            
        elif self.c_type == 'REAPER':
            self.attack_timer, self.basic_cd, self.vel_x = 28, 45, self.facing * 3
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 120, self.rect.y, 120, self.rect.height)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(1000, self.facing, 10)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(8); spawn_particles(t.rect.centerx, self.rect.y + 40, self.color, 15)
                    
        elif self.c_type == 'BRAWLER':
            self.attack_timer, self.basic_cd, self.vel_x = 10, 15, self.facing * 5
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 50, self.rect.y + 20, 50, 60)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(400, self.facing, 5)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(3); spawn_particles(t.rect.centerx, self.rect.y + 30, self.color, 10)
                    
        elif self.c_type == 'MAGE':
            self.attack_timer, self.basic_cd, self.vel_x = 20, 35, self.facing * 1
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 80, self.rect.y + 20, 80, 60)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(500, self.facing, 7)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(6); spawn_particles(t.rect.centerx, self.rect.y + 40, COLOR_ULT, 15)
                    
        elif self.c_type == 'VALKYRIE':
            self.attack_timer, self.basic_cd, self.vel_x = 18, 30, self.facing * 4
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 130, self.rect.y + 30, 130, 40)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(700, self.facing, 9)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(7); spawn_particles(t.rect.centerx, self.rect.y + 50, COLOR_WHITE, 12)
                    
        elif self.c_type == 'CYBORG':
            self.attack_timer, self.basic_cd, self.vel_x = 16, 25, self.facing * 2
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 60, self.rect.y + 20, 60, 40)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(550, self.facing, 8)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(5); spawn_particles(t.rect.centerx, self.rect.y + 40, (0, 255, 255), 15)
                    
        elif self.c_type == 'PIRATE':
            self.attack_timer, self.basic_cd, self.vel_x = 14, 20, self.facing * 5
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 60, self.rect.y + 20, 60, 60)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(450, self.facing, 5)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(4); spawn_particles(t.rect.centerx, self.rect.y + 40, COLOR_STEEL, 15)
                    
        elif self.c_type == 'KNIGHT':
            self.attack_timer, self.basic_cd, self.vel_x = 35, 55, self.facing * 2
            hitbox = pygame.Rect(self.rect.right if self.facing == 1 else self.rect.left - 110, self.rect.y, 110, self.rect.height)
            for t in targets:
                if t.is_dead: continue
                if hitbox.colliderect(t.rect):
                    t.take_damage(1100, self.facing, 15)
                    if getattr(t, 'c_type', None) != 'GOD': trigger_hit_stop(10); spawn_particles(t.rect.centerx, self.rect.y + 50, COLOR_WHITE, 25)
                    
        elif self.c_type == 'NECROMANCER':
            self.attack_timer, self.basic_cd, self.vel_x = 15, 25, self.facing * 1
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 12, 0, COLOR_NECRO, 400, self, 'skull'))
            
        elif self.c_type == 'HACKER':
            self.attack_timer, self.basic_cd, self.vel_x = 12, 18, 0
            px = self.rect.right if self.facing == 1 else self.rect.left - 50
            projectiles.append(Projectile(px, self.rect.y + 30, self.facing * 16, 0, (0, 255, 0), 350, self, 'code'))
            
        elif self.c_type == 'ILLUSIONIST':
            self.attack_timer, self.basic_cd, self.vel_x = 15, 22, 0
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 15, -3, self.color, 300, self, 'card'))
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 15, 0, self.color, 300, self, 'card'))
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 15, 3, self.color, 300, self, 'card'))
            
        elif self.c_type == 'ALCHEMIST':
            self.attack_timer, self.basic_cd, self.vel_x = 20, 30, self.facing * 2
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 12, -8, self.color, 600, self, 'flask'))
            
        elif self.c_type == 'GOD':
            self.attack_timer, self.basic_cd, self.vel_x = 5, 5, 0 
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.centery, self.facing * 35, 0, COLOR_ULT, 3500, self, 'shockwave'))

    def special_attack(self):
        if self.is_attacking or self.is_hit or self.is_parrying or self.spec_cd > 0 or cinematic['active']: return
        self.is_attacking, self.current_attack = True, 'special'
        self.spec_cd = self.spec_cd_max
        
        if self.c_type == 'SAMURAI':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.bottom - 20, self.facing * 20, 0, self.color, 1200, self, 'shockwave'))
        elif self.c_type == 'NINJA':
            self.attack_timer = 15
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 50, self.facing * 30, 0, self.color, 900, self, 'kunai'))
        elif self.c_type == 'MONK':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 6, 0, self.color, 1500, self, 'orb'))
        elif self.c_type == 'ARCHER':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 20, -5, self.color, 450, self, 'arrow'))
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 20, 0, self.color, 450, self, 'arrow'))
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 20, 5, self.color, 450, self, 'arrow'))
        elif self.c_type == 'REAPER':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 10, 0, self.color, 1600, self, 'orb'))
        elif self.c_type == 'BRAWLER':
            self.attack_timer = 15
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.bottom - 20, self.facing * 25, 0, self.color, 1000, self, 'shockwave'))
        elif self.c_type == 'MAGE':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 8, -2, self.color, 800, self, 'orb'))
            projectiles.append(Projectile(px, self.rect.y + 60, self.facing * 8, 2, self.color, 800, self, 'orb'))
        elif self.c_type == 'VALKYRIE':
            self.attack_timer = 20
            self.vel_x = self.facing * 10
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 50, self.facing * 25, 0, self.color, 1200, self, 'arrow'))
        elif self.c_type == 'CYBORG':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 40, self.facing * 25, 0, (0, 255, 255), 1100, self, 'arrow'))
        elif self.c_type == 'PIRATE':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 30, self.facing * 15, -2, (50, 50, 50), 1300, self, 'orb'))
        elif self.c_type == 'KNIGHT':
            self.attack_timer = 25
            self.vel_y = -8
            projectiles.append(Projectile(self.rect.right, self.rect.bottom - 20, 15, 0, COLOR_WHITE, 1000, self, 'shockwave'))
            projectiles.append(Projectile(self.rect.left - 40, self.rect.bottom - 20, -15, 0, COLOR_WHITE, 1000, self, 'shockwave'))
        elif self.c_type == 'NECROMANCER':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.bottom - 20, self.facing * 15, 0, COLOR_NECRO, 1100, self, 'shockwave'))
        elif self.c_type == 'HACKER':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 50
            projectiles.append(Projectile(px, self.rect.y + 30, self.facing * 10, 0, (255, 0, 0), 1000, self, 'virus'))
        elif self.c_type == 'ILLUSIONIST':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 40
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 3, 0, (150, 150, 150), 50, self, 'smoke'))
        elif self.c_type == 'ALCHEMIST':
            self.attack_timer = 20
            px = self.rect.right if self.facing == 1 else self.rect.left - 20
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 10, -10, self.color, 400, self, 'flask'))
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 14, -8, self.color, 400, self, 'flask'))
            projectiles.append(Projectile(px, self.rect.y + 20, self.facing * 18, -6, self.color, 400, self, 'flask'))
        elif self.c_type == 'GOD':
            self.attack_timer = 10
            self.spec_cd = 5 
            for i in range(5):
                projectiles.append(Projectile(self.rect.x + (i * 150 * self.facing), -50, 0, 15, COLOR_ULT, 5000, self, 'orb'))

    def trigger_ultimate(self):
        if self.ult_meter >= 100 and not cinematic['active'] and not self.is_dead and not self.is_hit:
            self.ult_meter = 0
            cinematic['active'] = True
            cinematic['timer'] = cinematic['max_timer'] = 140
            cinematic['owner'], cinematic['target'] = self, self.enemy
            cinematic['is_execution'] = False
            cinematic['data'] = {'slashes': [], 'angle': 0.0, 'scale': 5.0} 
            trigger_screen_shake(5, 140)

    def draw(self, off_x, off_y):
        should_draw = True
        if self.invincible > 0 and (self.invincible // 6) % 2 != 0: should_draw = False

        if should_draw:
            for i, pos in enumerate(self.shadow_trail):
                alpha = int(100 * ((i + 1) / len(self.shadow_trail)))
                surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                draw_character_model(surf, pos[0]+off_x, pos[1]+off_y, pos[2], self.c_type, self.color, self.anim_timer, vel_x=self.vel_x)
                surf.set_alpha(alpha); screen.blit(surf, (0,0))
                
            if self.is_hit and (self.hit_timer // 3) % 2 == 0:
                surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(surf, COLOR_WHITE, (self.rect.x+off_x, self.rect.y+off_y, self.rect.w, self.rect.height))
                screen.blit(surf, (0,0))
            elif not self.is_dead:
                draw_character_model(screen, self.rect.x+off_x, self.rect.y+off_y, self.facing, self.c_type, self.color, self.anim_timer, self.is_attacking, self.current_attack, self.is_hit, self.vel_x, self.is_parrying)

            if self.is_parrying:
                if self.c_type != 'HACKER': 
                    p_rect = pygame.Rect(self.rect.centerx - 25 + off_x + (self.facing * 10), self.rect.y + off_y, 50, 110)
                    start_angle = -math.pi/2 if self.facing == 1 else math.pi/2
                    end_angle = math.pi/2 if self.facing == 1 else 3*math.pi/2
                    pygame.draw.arc(screen, COLOR_WHITE, p_rect, start_angle, end_angle, 6)
                
            if self.god_shield_timer > 0:
                shield_pulse = math.sin(self.god_shield_timer) * 10
                shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(shield_surf, (*COLOR_ULT, 150), (int(self.rect.centerx + off_x), int(self.rect.centery + off_y)), int(80 + shield_pulse))
                pygame.draw.circle(shield_surf, COLOR_WHITE, (int(self.rect.centerx + off_x), int(self.rect.centery + off_y)), int(80 + shield_pulse), 5)
                screen.blit(shield_surf, (0,0))

        if self.invincible > 0 and not self.is_dead:
            pulse = math.sin(self.anim_timer * 2) * 5
            shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (*COLOR_WHITE, 150), (int(self.rect.centerx + off_x), int(self.rect.centery + off_y)), int(65 + pulse), 3)
            pygame.draw.circle(shield_surf, (*self.color, 80), (int(self.rect.centerx + off_x), int(self.rect.centery + off_y)), int(65 + pulse))
            screen.blit(shield_surf, (0,0))

# --- GLOBAL COLLECTIONS ---
particles, floating_texts, projectiles, weather_particles = [], [], [], []
def spawn_particles(x, y, color, amount, speed_m=1.0, is_blood=False):
    for _ in range(amount): particles.append(Particle(x, y, color, speed_m, is_blood))

# --- UI DRAWING ---
def draw_combat_gui(p1, p2):
    # P1 UI
    pygame.draw.rect(screen, COLOR_INK, (30, 25, 450, 120))
    pygame.draw.rect(screen, COLOR_FLOOR_LINE, (30, 25, 450, 120), 2)
    screen.blit(font_main.render(p1.c_type, True, COLOR_GOD if p1.c_type == 'GOD' else COLOR_P1), (45, 33))
    
    if p1.c_type == 'GOD':
        for i in range(3):
            lx, ly = 40 + i * 20 + random.randint(-2, 2), 55 + random.randint(-2, 2)
            c = random.choice([COLOR_WHITE, COLOR_ULT, COLOR_INK, (255, 0, 0)])
            pygame.draw.rect(screen, c, (lx, ly, random.randint(8, 14), random.randint(8, 14)))
        
        pygame.draw.rect(screen, COLOR_FLOOR, (45, 75, 420, 12))
        for _ in range(20):
            gx = 45 + random.randint(0, 400)
            gy = 75 + random.randint(-3, 6)
            gw = random.randint(10, 60)
            gh = random.randint(2, 12)
            gc = random.choice([COLOR_WHITE, COLOR_ULT, COLOR_INK, (255, 0, 0), (0, 255, 255)])
            pygame.draw.rect(screen, gc, (gx, gy, gw, gh))
            
        glitch_txt = font_small.render("ERR_DIVINE_OVERFLOW", True, COLOR_INK)
        screen.blit(glitch_txt, (50 + random.randint(-2, 2), 74))
    else:
        for i in range(p1.lives):
            pygame.draw.circle(screen, COLOR_P1, (45 + i * 20, 60), 6)
            pygame.draw.circle(screen, COLOR_WHITE, (45 + i * 20, 60), 6, 1)
        
        pygame.draw.rect(screen, COLOR_FLOOR, (45, 75, 420, 12))
        if p1.health > 0: pygame.draw.rect(screen, COLOR_P1, (45, 75, int(420 * (p1.health / p1.max_health)), 12))
    
    pygame.draw.rect(screen, COLOR_FLOOR, (45, 93, 120, 4))
    if p1.spec_cd_max > 0: pygame.draw.rect(screen, COLOR_WHITE, (45, 93, int(120 * (1 - p1.spec_cd / p1.spec_cd_max)), 4))
    pygame.draw.rect(screen, COLOR_FLOOR, (45, 103, 420, 6))
    pygame.draw.rect(screen, COLOR_ULT, (45, 103, int(420 * (p1.ult_meter / 100)), 6))
    
    screen.blit(font_small.render("V:ATK | B:SPC | C:ULT | E:PARRY", True, COLOR_WHITE), (45, 115))

    if p1.combo_count > 1:
        pulse = abs(math.sin(pygame.time.get_ticks() / 100)) * 255
        combo_color = (255, int(pulse), 0)
        combo_text = font_large.render(f"{p1.combo_count} HITS!", True, combo_color)
        screen.blit(combo_text, (45, 160))

    # P2 UI
    pygame.draw.rect(screen, COLOR_INK, (WIDTH - 480, 25, 450, 120))
    pygame.draw.rect(screen, COLOR_FLOOR_LINE, (WIDTH - 480, 25, 450, 120), 2)
    p2_name = font_main.render(p2.c_type, True, COLOR_GOD if p2.c_type == 'GOD' else COLOR_P2)
    screen.blit(p2_name, (WIDTH - 45 - p2_name.get_width(), 33))
    
    if p2.c_type == 'GOD':
        for i in range(3):
            lx, ly = WIDTH - 55 - i * 20 + random.randint(-2, 2), 55 + random.randint(-2, 2)
            c = random.choice([COLOR_WHITE, COLOR_ULT, COLOR_INK, (255, 0, 0)])
            pygame.draw.rect(screen, c, (lx, ly, random.randint(8, 14), random.randint(8, 14)))
        
        pygame.draw.rect(screen, COLOR_FLOOR, (WIDTH - 465, 75, 420, 12))
        for _ in range(20):
            gx = WIDTH - 465 + random.randint(0, 400)
            gy = 75 + random.randint(-3, 6)
            gw = random.randint(10, 60)
            gh = random.randint(2, 12)
            gc = random.choice([COLOR_WHITE, COLOR_ULT, COLOR_INK, (255, 0, 0), (0, 255, 255)])
            pygame.draw.rect(screen, gc, (gx, gy, gw, gh))
            
        glitch_txt = font_small.render("ERR_DIVINE_OVERFLOW", True, COLOR_INK)
        screen.blit(glitch_txt, (WIDTH - 460 + random.randint(-2, 2), 74))
    else:
        for i in range(p2.lives):
            pygame.draw.circle(screen, COLOR_P2, (WIDTH - 45 - i * 20, 60), 6)
            pygame.draw.circle(screen, COLOR_WHITE, (WIDTH - 45 - i * 20, 60), 6, 1)

        pygame.draw.rect(screen, COLOR_FLOOR, (WIDTH - 465, 75, 420, 12))
        if p2.health > 0:
            hp_width = int(420 * (p2.health / p2.max_health))
            pygame.draw.rect(screen, COLOR_P2, (WIDTH - 465 + (420 - hp_width), 75, hp_width, 12))
        
    pygame.draw.rect(screen, COLOR_FLOOR, (WIDTH - 165, 93, 120, 4))
    if p2.spec_cd_max > 0:
        pygame.draw.rect(screen, COLOR_WHITE, (WIDTH - 165 + (120 - int(120 * (1 - p2.spec_cd / p2.spec_cd_max))), 93, int(120 * (1 - p2.spec_cd / p2.spec_cd_max)), 4))
    pygame.draw.rect(screen, COLOR_FLOOR, (WIDTH - 465, 103, 420, 6))
    ult_width = int(420 * (p2.ult_meter / 100))
    pygame.draw.rect(screen, COLOR_ULT, (WIDTH - 465 + (420 - ult_width), 103, ult_width, 6))

    binds_p2 = font_small.render("K:ATK | L:SPC | I:ULT | O:PARRY", True, COLOR_WHITE)
    screen.blit(binds_p2, (WIDTH - 45 - binds_p2.get_width(), 115))

    if p2.combo_count > 1:
        pulse = abs(math.sin(pygame.time.get_ticks() / 100)) * 255
        combo_color = (255, int(pulse), 0)
        combo_text = font_large.render(f"{p2.combo_count} HITS!", True, combo_color)
        screen.blit(combo_text, (WIDTH - 45 - combo_text.get_width(), 160))

# --- GAME STATE LOOP ---
running, state = True, 'MENU' 
classes_list = ['SAMURAI', 'NINJA', 'MONK', 'ARCHER', 'REAPER', 'BRAWLER', 'MAGE', 'VALKYRIE', 'CYBORG', 'PIRATE', 'KNIGHT', 'NECROMANCER', 'HACKER', 'ILLUSIONIST', 'ALCHEMIST']
p1_idx, p2_idx, p1_ready, p2_ready = 0, 1, False, False
p1, p2, menu_anim_timer = None, None, 0

secret_sequence = []
god_unlocked = False
aura_timer = 0 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False; pygame.quit(); sys.exit()

        if state == 'MENU':
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    secret_sequence.append(event.unicode.lower())
                    if len(secret_sequence) > 6:
                        secret_sequence.pop(0)
                    if "".join(secret_sequence) == "unlock":
                        if not god_unlocked:
                            god_unlocked = True
                            aura_timer = 180 
                    
                if god_unlocked:
                    if event.key == pygame.K_g: 
                        if 'GOD' not in classes_list: classes_list.append('GOD')
                        p1_idx = classes_list.index('GOD')
                    if event.key == pygame.K_h: 
                        if 'GOD' not in classes_list: classes_list.append('GOD')
                        p2_idx = classes_list.index('GOD')
                    if event.key == pygame.K_x: 
                        if 'GOD' in classes_list:
                            classes_list.remove('GOD')
                            p1_idx = p1_idx % len(classes_list)
                            p2_idx = p2_idx % len(classes_list)
                    
                if not p1_ready:
                    if event.key == pygame.K_a: p1_idx = (p1_idx - 1) % len(classes_list)
                    if event.key == pygame.K_d: p1_idx = (p1_idx + 1) % len(classes_list)
                    if event.key == pygame.K_w: p1_ready = True
                if not p2_ready:
                    if event.key == pygame.K_LEFT: p2_idx = (p2_idx - 1) % len(classes_list)
                    if event.key == pygame.K_RIGHT: p2_idx = (p2_idx + 1) % len(classes_list)
                    if event.key == pygame.K_UP: p2_ready = True
                    
        elif state == 'MAP_SELECT':
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    current_stage_idx = (current_stage_idx - 1) % len(STAGES)
                    weather_particles.clear()
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    current_stage_idx = (current_stage_idx + 1) % len(STAGES)
                    weather_particles.clear()
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_w, pygame.K_UP]:
                    p1 = Fighter(200, COLOR_GOD if classes_list[p1_idx] == 'GOD' else COLOR_P1, classes_list[p1_idx], 1)
                    p2 = Fighter(WIDTH - 250, COLOR_GOD if classes_list[p2_idx] == 'GOD' else COLOR_P2, classes_list[p2_idx], -1)
                    p1.enemy, p2.enemy = p2, p1
                    state = 'COMBAT'

        elif state == 'COMBAT' and hit_stop <= 0 and not cinematic['active']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v: p1.basic_attack()
                if event.key == pygame.K_b: p1.special_attack()
                if event.key == pygame.K_c: p1.trigger_ultimate()
                if event.key == pygame.K_e: p1.parry()
                if event.key == pygame.K_k: p2.basic_attack()
                if event.key == pygame.K_l: p2.special_attack()
                if event.key == pygame.K_i: p2.trigger_ultimate()
                if event.key == pygame.K_o: p2.parry()
                
        elif state == 'GAMEOVER':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state, p1_ready, p2_ready = 'MENU', False, False
                particles.clear(); projectiles.clear(); floating_texts.clear(); weather_particles.clear()

    # Weather Processing
    stage = STAGES[current_stage_idx]
    if stage['weather'] != 'NONE':
        if len(weather_particles) < 150:  
            if stage['weather'] == 'SAKURA' and random.random() < 0.5:
                pass 
            else:
                spawn_rate = {'RAIN': 2, 'STORM': 4, 'SNOW': 1, 'ASH': 1, 'SAKURA': 1}[stage['weather']]
                for _ in range(spawn_rate):
                    weather_particles.append(WeatherParticle(stage['weather']))

    if stage['weather'] == 'STORM' and random.random() < 0.01:
        lightning_timer = 5

    # --- MENU & MAP_SELECT LOGIC ---
    if state in ['MENU', 'MAP_SELECT']:
        screen.fill(stage['bg'])
        
        if lightning_timer > 0:
            screen.fill((200, 200, 220))
            lightning_timer -= 1
            
        menu_anim_timer += 0.1
        
        pygame.draw.rect(screen, stage['floor'], (0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y))
        pygame.draw.rect(screen, stage['line'], (0, FLOOR_Y, WIDTH, 2))
        for obs in stage['obstacles']:
            pygame.draw.rect(screen, stage['obs_color'], obs)
            pygame.draw.rect(screen, COLOR_INK, obs, 2)

        for wp in weather_particles[:]:
            wp.update()
            wp.draw(0, 0)
            if not wp.active: weather_particles.remove(wp)

        if state == 'MENU':
            draw_rect_alpha(screen, (0,0,0,150), (WIDTH//2 - 250, 70, 500, 100), 10)
            title_surf = font_title.render("SELECT FIGHTER", True, COLOR_WHITE)
            screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, 120)))
            
            if aura_timer > 0:
                aura_timer -= 1
                alpha = int((aura_timer / 180.0) * 60)
                aura_txt = font_main.render("You feel a strange aura upon you...", True, COLOR_WHITE)
                aura_txt.set_alpha(alpha)
                screen.blit(aura_txt, aura_txt.get_rect(center=(WIDTH//2, 30)))

            p1_x, p2_x = WIDTH // 4 - 25, (WIDTH // 4) * 3 - 25
            p1_col = COLOR_GOD if classes_list[p1_idx] == 'GOD' else COLOR_P1
            draw_character_model(screen, p1_x, FLOOR_Y - 110, 1, classes_list[p1_idx], p1_col, menu_anim_timer)
            screen.blit(font_large.render(classes_list[p1_idx], True, p1_col), (p1_x - 50, FLOOR_Y + 25))
            screen.blit(font_main.render("P1 READY" if p1_ready else "[A/D] SELECT | [W] LOCK", True, COLOR_WHITE), (p1_x - 80, 200))

            p2_col = COLOR_GOD if classes_list[p2_idx] == 'GOD' else COLOR_P2
            draw_character_model(screen, p2_x, FLOOR_Y - 110, -1, classes_list[p2_idx], p2_col, menu_anim_timer)
            screen.blit(font_large.render(classes_list[p2_idx], True, p2_col), (p2_x - 50, FLOOR_Y + 25))
            screen.blit(font_main.render("P2 READY" if p2_ready else "[< />] SELECT | [^] LOCK", True, COLOR_WHITE), (p2_x - 80, 200))
                
            if p1_ready and p2_ready:
                state = 'MAP_SELECT'

        elif state == 'MAP_SELECT':
            draw_rect_alpha(screen, (0,0,0,150), (WIDTH//2 - 300, 70, 600, 140), 10)
            title_surf = font_title.render("SELECT MAP", True, COLOR_WHITE)
            screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, 110)))
            
            map_name = font_large.render(f"<  {stage['name']}  >", True, COLOR_ULT)
            screen.blit(map_name, map_name.get_rect(center=(WIDTH//2, 170)))
            
            instruct = font_main.render("PRESS [SPACE] OR [W] / [^] TO BATTLE", True, COLOR_WHITE)
            screen.blit(instruct, instruct.get_rect(center=(WIDTH//2, 230)))
            
            p1_col = COLOR_GOD if classes_list[p1_idx] == 'GOD' else COLOR_P1
            p2_col = COLOR_GOD if classes_list[p2_idx] == 'GOD' else COLOR_P2
            
            draw_character_model(screen, WIDTH // 2 - 150, FLOOR_Y - 110, 1, classes_list[p1_idx], p1_col, menu_anim_timer)
            draw_character_model(screen, WIDTH // 2 + 100, FLOOR_Y - 110, -1, classes_list[p2_idx], p2_col, menu_anim_timer)

    # --- COMBAT LOGIC ---
    elif state == 'COMBAT':
        if cinematic['active']:
            c_timer = cinematic['timer']
            c_timer -= 1
            cinematic['timer'] = c_timer
            if c_timer <= 0:
                cinematic['active'] = False
                
                if cinematic['owner'].c_type == 'NECROMANCER':
                    cinematic['owner'].minions.append(Minion(cinematic['owner'], cinematic['owner'].rect.centerx - 80, FLOOR_Y - 90, cinematic['owner'].facing))
                    cinematic['owner'].minions.append(Minion(cinematic['owner'], cinematic['owner'].rect.centerx + 80, FLOOR_Y - 90, cinematic['owner'].facing))
                    spawn_particles(cinematic['owner'].rect.centerx, cinematic['owner'].rect.centery, COLOR_NECRO, 50, speed_m=2.0)
                    floating_texts.append(FloatingText(cinematic['owner'].rect.centerx, cinematic['owner'].rect.y - 50, "ARMY AWAKENED", COLOR_NECRO, mega=False))
                    trigger_screen_shake(15, 10)
                else:
                    if cinematic['target'].c_type == 'GOD':
                        trigger_hit_stop(10)
                        floating_texts.append(FloatingText(cinematic['target'].rect.centerx, cinematic['target'].rect.centery - 50, "IMMUNE", COLOR_ULT, mega=True))
                    else:
                        dmg = 99999 if cinematic['owner'].c_type == 'GOD' else 3500
                        if cinematic['target'].health <= dmg and cinematic['target'].lives == 1:
                            cinematic['is_execution'] = True 
                        
                        cinematic['target'].health -= dmg
                        if cinematic['target'].health <= 0:
                            cinematic['target'].lives -= 1
                            if cinematic['target'].lives <= 0: cinematic['target'].is_dead = True
                            else: cinematic['target'].respawn()
                            
                        trigger_hit_stop(20); trigger_screen_shake(25, 20)
                        spawn_particles(cinematic['target'].rect.centerx, cinematic['target'].rect.centery, COLOR_INK, 100, 3.0)
                        
                        if cinematic['is_execution']:
                            floating_texts.append(FloatingText(WIDTH//2, HEIGHT//2, "EXECUTED", COLOR_BLOOD, mega=True))
                            trigger_hit_stop(60) 
                    
        elif hit_stop > 0: hit_stop -= 1
        else:
            keys = pygame.key.get_pressed()
            if not p1.is_hit and not p1.is_attacking and not p1.is_parrying:
                if keys[pygame.K_a]: p1.vel_x, p1.facing = -p1.speed, -1
                elif keys[pygame.K_d]: p1.vel_x, p1.facing = p1.speed, 1
                if keys[pygame.K_w] and p1.grounded: p1.vel_y = p1.jump_power
            if not p2.is_hit and not p2.is_attacking and not p2.is_parrying:
                if keys[pygame.K_LEFT]: p2.vel_x, p2.facing = -p2.speed, -1
                elif keys[pygame.K_RIGHT]: p2.vel_x, p2.facing = p2.speed, 1
                if keys[pygame.K_UP] and p2.grounded: p2.vel_y = p2.jump_power

            p1.update(); p2.update()
            
            for m in p1.minions[:]:
                m.update()
                if m.is_dead: p1.minions.remove(m)
            for m in p2.minions[:]:
                m.update()
                if m.is_dead: p2.minions.remove(m)

            if not p1.is_attacking and not p2.is_attacking and not p1.is_parrying and not p2.is_parrying:
                if p1.rect.x < p2.rect.x: p1.facing, p2.facing = 1, -1
                else: p1.facing, p2.facing = -1, 1

            for p in projectiles[:]: 
                p.update()
                if not p.active: projectiles.remove(p)
            for pt in particles[:]: 
                pt.update()
                if pt.life <= 0: particles.remove(pt)
            for ft in floating_texts[:]: 
                ft.update()
                if ft.life <= 0: floating_texts.remove(ft)

            if p1.is_dead or p2.is_dead: state = 'GAMEOVER'

        # DRAWING STAGE
        offset_x = random.uniform(-shake_intensity, shake_intensity) if shake_duration > 0 else 0
        offset_y = random.uniform(-shake_intensity, shake_intensity) if shake_duration > 0 else 0
        if shake_duration > 0: shake_duration -= 1

        screen.fill(stage['bg'])
        if lightning_timer > 0:
            screen.fill((200, 200, 220))
            lightning_timer -= 1
            
        pygame.draw.rect(screen, stage['floor'], (offset_x, FLOOR_Y + offset_y, WIDTH, HEIGHT - FLOOR_Y))
        pygame.draw.rect(screen, stage['line'], (offset_x, FLOOR_Y + offset_y, WIDTH, 2))
        for obs in stage['obstacles']:
            obs_dr = obs.move(offset_x, offset_y)
            pygame.draw.rect(screen, stage['obs_color'], obs_dr)
            pygame.draw.rect(screen, COLOR_INK, obs_dr, 2)

        if stage['weather'] == 'ASH':
            for wp in weather_particles[:]:
                wp.update()
                wp.draw(offset_x, offset_y)
                if not wp.active: weather_particles.remove(wp)

        p1.draw(offset_x, offset_y); p2.draw(offset_x, offset_y)
        
        for m in p1.minions: m.draw(offset_x, offset_y)
        for m in p2.minions: m.draw(offset_x, offset_y)
            
        for p in projectiles: p.draw(offset_x, offset_y)
        for pt in particles: pt.draw(offset_x, offset_y)
        
        if stage['weather'] != 'ASH':
            for wp in weather_particles[:]:
                wp.update()
                wp.draw(offset_x, offset_y)
                if not wp.active: weather_particles.remove(wp)
        
        # --- ULTIMATE CINEMATIC DRAWING LOGIC ---
        if cinematic['active']:
            c_timer = cinematic['timer']
            c_max = cinematic['max_timer']
            c_owner = cinematic['owner']
            c_target = cinematic['target']
            c_data = cinematic['data']
            
            draw_rect_alpha(screen, (0, 0, 0, 200), (0, 0, WIDTH, HEIGHT))
            
            if c_owner.c_type == 'NINJA':
                if c_timer > 30:
                    if c_timer % 3 == 0:
                        x1, y1 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                        x2, y2 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                        c_data['slashes'].append(((x1, y1), (x2, y2)))
                    for s in c_data['slashes']:
                        pygame.draw.line(screen, c_owner.color, s[0], s[1], 8)
                        pygame.draw.line(screen, COLOR_WHITE, s[0], s[1], 2)
                elif c_timer > 10:
                    pass 
                else:
                    pygame.draw.line(screen, COLOR_BLOOD, (0, HEIGHT//2 + random.randint(-15,15)), (WIDTH, HEIGHT//2 + random.randint(-15,15)), 60)
                    pygame.draw.line(screen, COLOR_WHITE, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 20)

            elif c_owner.c_type == 'SAMURAI':
                pygame.draw.circle(screen, COLOR_BLOOD, (WIDTH//2, HEIGHT//2 + 100), 250)
                draw_character_model(screen, WIDTH//2 - 25, HEIGHT//2, 1, 'SAMURAI', (0,0,0), 0)
                draw_length = int(WIDTH * (1 - c_timer/c_max))
                pygame.draw.line(screen, COLOR_WHITE, (0, HEIGHT//2 + 150), (draw_length, HEIGHT//2 + 150), 4)

            elif c_owner.c_type == 'MONK':
                c_data['angle'] += 0.05
                cx, cy = WIDTH//2, HEIGHT//2
                for i in range(3, 8):
                    radius = int(120 * i * (1 + math.sin(c_data['angle'])))
                    pygame.draw.circle(screen, COLOR_ULT, (cx, cy), radius, max(1, 10 - i))
                if c_timer < 40:
                    pillar_width = int(250 * ((40 - c_timer)/40))
                    tx = c_target.rect.centerx + offset_x
                    pygame.draw.rect(screen, COLOR_ULT, (tx - pillar_width//2, 0, pillar_width, HEIGHT))
                    pygame.draw.rect(screen, COLOR_WHITE, (tx - pillar_width//4, 0, pillar_width//2, HEIGHT))

            elif c_owner.c_type == 'ARCHER':
                c_data['scale'] = max(0.5, c_data['scale'] - 0.05)
                rx, ry = c_target.rect.centerx + offset_x, c_target.rect.centery + offset_y
                size = int(100 * c_data['scale'])
                pygame.draw.circle(screen, c_owner.color, (rx, ry), size, 4)
                pygame.draw.line(screen, c_owner.color, (rx - size - 40, ry), (rx + size + 40, ry), 6)
                pygame.draw.line(screen, c_owner.color, (rx, ry - size - 40), (rx, ry + size + 40), 6)
                if c_timer < 30:
                    for _ in range(8):
                        ay = ry + random.randint(-150, 150)
                        pygame.draw.line(screen, COLOR_STEEL, (0, ay), (WIDTH, ay), 15)
                        pygame.draw.line(screen, COLOR_WHITE, (0, ay), (WIDTH, ay), 5)

            elif c_owner.c_type == 'REAPER':
                if c_timer > 40:
                    for _ in range(3):
                        sx, sy = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                        pygame.draw.circle(screen, c_owner.color, (sx, sy), random.randint(5, 15))
                        pygame.draw.line(screen, COLOR_WHITE, (sx, sy), (c_target.rect.centerx + offset_x, c_target.rect.centery + offset_y), 1)
                else:
                    pygame.draw.line(screen, c_owner.color, (0, 0), (WIDTH, HEIGHT), 80)
                    pygame.draw.line(screen, COLOR_WHITE, (0, 0), (WIDTH, HEIGHT), 20)
                    pygame.draw.line(screen, c_owner.color, (WIDTH, 0), (0, HEIGHT), 80)
                    pygame.draw.line(screen, COLOR_WHITE, (WIDTH, 0), (0, HEIGHT), 20)

            elif c_owner.c_type == 'BRAWLER':
                if 'fists' not in c_data: c_data['fists'] = []
                c_data['fists'].append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
                for fx, fy in c_data['fists']:
                    pygame.draw.circle(screen, c_owner.color, (fx, fy), random.randint(30, 80))
                    pygame.draw.circle(screen, COLOR_WHITE, (fx, fy), random.randint(10, 30))
                if c_timer < 20:
                    pygame.draw.circle(screen, c_owner.color, (WIDTH//2, HEIGHT//2), 300)
                    pygame.draw.circle(screen, COLOR_WHITE, (WIDTH//2, HEIGHT//2), 150)
                    
            elif c_owner.c_type == 'MAGE':
                if 'meteors' not in c_data: c_data['meteors'] = []
                if c_timer > 20 and c_timer % 5 == 0:
                    c_data['meteors'].append([random.randint(0, WIDTH), -100])
                for m in c_data['meteors']:
                    m[1] += 25
                    pygame.draw.circle(screen, COLOR_ULT, (m[0], m[1]), 50)
                    pygame.draw.circle(screen, COLOR_WHITE, (m[0], m[1]), 20)

            elif c_owner.c_type == 'VALKYRIE':
                tx = c_target.rect.centerx + offset_x
                if c_timer > 40:
                    pygame.draw.polygon(screen, COLOR_ULT, [(c_owner.rect.centerx, c_owner.rect.centery), (c_owner.rect.centerx - 150, c_owner.rect.centery - 200), (c_owner.rect.centerx - 50, c_owner.rect.centery + 50)])
                    pygame.draw.polygon(screen, COLOR_ULT, [(c_owner.rect.centerx, c_owner.rect.centery), (c_owner.rect.centerx + 150, c_owner.rect.centery - 200), (c_owner.rect.centerx + 50, c_owner.rect.centery + 50)])
                else:
                    pygame.draw.polygon(screen, COLOR_WHITE, [(tx - 60, 0), (tx + 60, 0), (tx, HEIGHT)])
                    pygame.draw.polygon(screen, COLOR_ULT, [(tx - 30, 0), (tx + 30, 0), (tx, HEIGHT)])
                    
            elif c_owner.c_type == 'CYBORG':
                tx = c_target.rect.centerx + offset_x
                if c_timer > 60:
                    pygame.draw.line(screen, (255, 0, 0), (tx, 0), (tx, HEIGHT), 2)
                    pygame.draw.circle(screen, (255, 0, 0), (tx, c_target.rect.centery), 30, 2)
                else:
                    pygame.draw.rect(screen, (0, 255, 255), (tx - 80, 0, 160, HEIGHT))
                    pygame.draw.rect(screen, COLOR_WHITE, (tx - 40, 0, 80, HEIGHT))

            elif c_owner.c_type == 'PIRATE':
                if 'cannons' not in c_data: c_data['cannons'] = []
                if c_timer > 20 and c_timer % 4 == 0:
                    c_data['cannons'].append([random.choice([-100, WIDTH+100]), random.randint(0, HEIGHT)])
                for c in c_data['cannons']:
                    c[0] += 35 if c[0] < WIDTH//2 else -35
                    pygame.draw.circle(screen, (50, 50, 50), (c[0], c[1]), 30)
                    pygame.draw.circle(screen, (100, 100, 100), (c[0], c[1]), 15)

            elif c_owner.c_type == 'KNIGHT':
                tx = c_target.rect.centerx + offset_x
                if c_timer > 30:
                    pygame.draw.line(screen, COLOR_WHITE, (tx, 0), (tx, HEIGHT), 4)
                else:
                    pygame.draw.polygon(screen, COLOR_STEEL, [(tx - 100, -100), (tx + 100, -100), (tx + 80, HEIGHT - 50), (tx, HEIGHT), (tx - 80, HEIGHT - 50)])
                    pygame.draw.polygon(screen, COLOR_WHITE, [(tx - 40, -100), (tx + 40, -100), (tx + 30, HEIGHT - 70), (tx, HEIGHT - 20), (tx - 30, HEIGHT - 70)])

            elif c_owner.c_type == 'ILLUSIONIST':
                if 'cards' not in c_data: c_data['cards'] = []
                
                # Draw ring of clones
                for i in range(10):
                    angle = (i / 10) * 2 * math.pi + (c_timer * 0.05)
                    cx = WIDTH//2 + math.cos(angle) * 300
                    cy = HEIGHT//2 + math.sin(angle) * 200
                    draw_character_model(screen, cx-25, cy-50, 1, 'ILLUSIONIST', c_owner.color, 0)
                
                if c_timer > 20 and c_timer % 5 == 0:
                    for i in range(3):
                        c_data['cards'].append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])
                for c in c_data['cards']:
                    tx, ty = c_target.rect.centerx + offset_x, c_target.rect.centery + offset_y
                    c[0] += (tx - c[0]) * 0.2
                    c[1] += (ty - c[1]) * 0.2
                    pygame.draw.rect(screen, COLOR_WHITE, (c[0]-10, c[1]-15, 20, 30))
                    pygame.draw.rect(screen, COLOR_BLOOD, (c[0]-5, c[1]-5, 10, 10))

            elif c_owner.c_type == 'ALCHEMIST':
                if c_timer > 40:
                    # Drop giant vials
                    vy = HEIGHT - int(c_timer * 15)
                    pygame.draw.rect(screen, (0, 255, 0), (WIDTH//2 - 40, vy, 30, 80))
                    pygame.draw.rect(screen, (255, 0, 255), (WIDTH//2 + 10, vy, 30, 80))
                else:
                    # Negative color flash mushroom cloud
                    screen.fill((255, 0, 255))
                    pygame.draw.circle(screen, (0, 255, 0), (WIDTH//2, HEIGHT//2 - 100), 300 + math.sin(c_timer)*20)
                    pygame.draw.rect(screen, (0, 255, 0), (WIDTH//2 - 100, HEIGHT//2, 200, HEIGHT))

            elif c_owner.c_type == 'NECROMANCER':
                draw_rect_alpha(screen, (0, 50, 0, 80), (0, 0, WIDTH, HEIGHT)) 
                pygame.draw.circle(screen, COLOR_NECRO, (c_owner.rect.centerx + offset_x, c_owner.rect.centery + offset_y), 80 + math.sin(c_timer)*10, 5)
                
                lx = c_owner.rect.centerx - 80 + offset_x
                rx = c_owner.rect.centerx + 80 + offset_x
                
                rise_progress = max(0, min(1.0, (120 - c_timer) / 80.0))
                
                for mx in [lx, rx]:
                    if c_timer > 20 and c_timer < 120:
                        for _ in range(3):
                            dx = mx + random.randint(-20, 20)
                            dy = FLOOR_Y + offset_y - random.randint(0, 30)
                            pygame.draw.circle(screen, (40, 30, 20), (dx, dy), random.randint(3, 8))
                    
                    if rise_progress > 0:
                        my = FLOOR_Y + offset_y - int(90 * rise_progress)
                        pygame.draw.circle(screen, COLOR_INK, (int(mx), int(my + 15)), 10)
                        pygame.draw.circle(screen, COLOR_NECRO, (int(mx + c_owner.facing*3), int(my + 13)), 2)
                        pygame.draw.rect(screen, COLOR_INK, (mx - 15, my + 25, 30, 40), border_radius=5)
                        
            elif c_owner.c_type == 'HACKER':
                screen.fill((0, 10, 0)) 
                if 'matrix' not in c_data: 
                    c_data['matrix'] = [[random.randint(0, WIDTH), random.randint(-800, 0)] for _ in range(80)]
                for col in c_data['matrix']:
                    col[1] += 25
                    txt = font_small.render("".join([str(random.randint(0,1)) for _ in range(6)]), True, (0, 255, 0))
                    screen.blit(txt, (col[0], col[1]))
                    if col[1] > HEIGHT: col[1] = random.randint(-200, 0)
                
                if c_timer < 50:
                    tx, ty = c_target.rect.centerx + offset_x, c_target.rect.centery + offset_y
                    for i in range(1, int(min(5, (50 - c_timer)/5)) + 1):
                        ew, eh = 240, 140
                        ex, ey = tx - ew//2 + random.randint(-50, 50), ty - eh//2 + random.randint(-50, 50)
                        pygame.draw.rect(screen, (0, 0, 150), (ex, ey, ew, eh))
                        pygame.draw.rect(screen, COLOR_WHITE, (ex, ey, ew, eh), 3)
                        pygame.draw.rect(screen, (0, 0, 200), (ex, ey, ew, 25))
                        screen.blit(font_small.render("SYSTEM HALTED", True, COLOR_WHITE), (ex + 5, ey + 5))
                        err = font_main.render("FATAL EXCEPTION", True, COLOR_WHITE)
                        screen.blit(err, err.get_rect(center=(ex + ew//2, ey + eh//2)))
                    
            elif c_owner.c_type == 'GOD':
                if c_timer > 50:
                    radius = int((140 - c_timer) * 15)
                    pygame.draw.circle(screen, COLOR_ULT, (WIDTH//2, HEIGHT//2), radius, 10)
                elif c_timer > 10:
                    pygame.draw.circle(screen, COLOR_WHITE, (WIDTH//2, HEIGHT//2), 300 + math.sin(c_timer)*20)

            if c_timer > 30:
                ult_text = font_mega.render(f"{c_owner.c_type} ULTIMATE", True, c_owner.color if c_owner.c_type != 'GOD' else COLOR_INK)
                alpha = int(255 * (c_timer/c_max))
                ult_text.set_alpha(alpha)
                screen.blit(ult_text, ult_text.get_rect(center=(WIDTH//2 + random.randint(-3,3), HEIGHT//2 - 180)))

        for ft in floating_texts: ft.draw(offset_x, offset_y)
        draw_combat_gui(p1, p2)

    # --- GAMEOVER LOGIC ---
    elif state == 'GAMEOVER':
        draw_rect_alpha(screen, (10, 10, 10, 220), (0, 0, WIDTH, HEIGHT))
        msg = f"P2 ({p2.c_type}) WINS!" if p1.is_dead else f"P1 ({p1.c_type}) WINS!"
        screen.blit(font_large.render(msg, True, COLOR_P2 if p1.is_dead else COLOR_P1), (WIDTH//2 - 200, HEIGHT//2 - 20))
        screen.blit(font_main.render("PRESS SPACE TO REMATCH", True, COLOR_WHITE), (WIDTH//2 - 130, HEIGHT//2 + 50))

    pygame.display.flip(); clock.tick(FPS)