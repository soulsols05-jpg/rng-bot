import discord
from discord.ext import commands
from discord import app_commands
import random
import os
import json
import time
import threading
import asyncio
import base64

# ── Token & Save ───────────────────────────
TOKEN = os.environ.get("TOKEN")
SAVE_FILE = "rng_save.json"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "soulsols05-jpg/rng-bot"
GITHUB_PATH = "rng_save.json"

def save_to_github():
    if not GITHUB_TOKEN:
        return
    try:
        import requests
        with open(SAVE_FILE, "r") as f:
            content = f.read()
        encoded = base64.b64encode(content.encode()).decode()
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        try:
            resp = requests.get(url, headers=headers)
            sha = resp.json()["sha"] if resp.status_code == 200 else None
        except:
            sha = None
        data = {"message": "auto save", "content": encoded}
        if sha:
            data["sha"] = sha
        requests.put(url, headers=headers, json=data)
    except:
        pass

# ── Colors ──────────────────────────────────
COLORS = {
    "GRAY": 0x808080, "GREEN": 0x00FF00, "PURPLE": 0x800080,
    "YELLOW": 0xFFFF00, "ORANGE": 0xFF8800, "RED": 0xFF0000,
    "GOLD": 0xFFD700, "CYAN": 0x00FFFF, "WHITE": 0xFFFFFF,
    "PINK": 0xFF69B4, "VOLT_BLUE": 0x33FFFF, "DARK_RED": 0x8B0000,
    "MAGENTA": 0xFF00FF, "LIGHT_BLUE": 0xADD8E6, "SILVER": 0xC0C0C0,
    "BRONZE": 0xCD7F32, "DARK_GREEN": 0x006400, "MOON": 0xF0F0F0,
}

# ── BIOMES ──────────────────────────────────
BIOMES = {
    "Normal":   {"color": "GRAY",       "multiplier": 1.0, "spawn_chance": 25, "description": "Plain and simple."},
    "Windy":    {"color": "CYAN",       "multiplier": 1.5, "spawn_chance": 12, "description": "Gentle breeze boosts your luck."},
    "Foggy":    {"color": "GRAY",       "multiplier": 2.0, "spawn_chance": 8,  "description": "Thick fog reveals hidden treasures."},
    "Rainy":    {"color": "LIGHT_BLUE", "multiplier": 2.5, "spawn_chance": 7,  "description": "Rain washes away bad luck."},
    "Snowy":    {"color": "WHITE",      "multiplier": 2.0, "spawn_chance": 7,  "description": "Snowflakes carry rare auras."},
    "Night":    {"color": "PURPLE",     "multiplier": 2.5, "spawn_chance": 6,  "description": "Darkness brings power."},
    "Crimson":  {"color": "DARK_RED",   "multiplier": 3.5, "spawn_chance": 5,  "description": "Blood moon rises..."},
    "Cosmic":   {"color": "PURPLE",     "multiplier": 3.0, "spawn_chance": 5,  "description": "Stars align in your favor."},
    "Calamity": {"color": "RED",        "multiplier": 4.5, "spawn_chance": 4,  "description": "CHAOS! Everything is amplified!"},
    "Jungle":   {"color": "DARK_GREEN", "multiplier": 1.8, "spawn_chance": 4,  "description": "Wild and unpredictable."},
    "Matrix":   {"color": "GREEN",      "multiplier": 5.0, "spawn_chance": 3,  "description": "Digital realm. Luck is binary."},
    "Volcano":  {"color": "ORANGE",     "multiplier": 3.0, "spawn_chance": 3,  "description": "Magma flows everywhere!"},
    "Twilight": {"color": "MAGENTA",    "multiplier": 2.0, "spawn_chance": 4,  "description": "Between day and night..."},
    "Abyss":    {"color": "DARK_RED",   "multiplier": 5.0, "spawn_chance": 2,  "description": "The void stares back."},
    "Celestial":{"color": "GOLD",       "multiplier": 3.0, "spawn_chance": 4,  "description": "Blessed by the stars."},
    "FATAL ERROR": {"color": "RED",     "multiplier": 10.0, "spawn_chance": 0.01,"description": "SYSTEM CORRUPTED! INSANE LUCK! APPLIES TO ALL AURAS!"},
}

# ── AURAS ──────────────────────────────────
auras = [
    {"name": "Common",                   "one_in": 3,        "color": "GRAY",         "description": "That common is very common."},
    {"name": "Cool",                     "one_in": 6,        "color": "GREEN",        "description": "That cool is very cool."},
    {"name": "Rare",                     "one_in": 32,       "color": "PURPLE",       "description": "That rare is rare."},
    {"name": "Lucky",                    "one_in": 50,       "color": "GREEN",        "description": "Feeling lucky!"},
    {"name": "Flame",                    "one_in": 100,      "color": "ORANGE",       "description": "It burns!"},
    {"name": "Charged",                  "one_in": 125,      "color": "VOLT_BLUE",    "description": "Electric energy flows!"},
    {"name": "Shiny",                    "one_in": 332,      "color": "YELLOW",       "description": "You are shiny!"},
    {"name": "Acid",                     "one_in": 400,      "color": "DARK_GREEN",   "description": "Toxic liquid of nuclear waste."},
    {"name": "Silver",                   "one_in": 431,      "color": "SILVER",       "description": "Expensive material."},
    {"name": "Bronze",                   "one_in": 256,      "color": "BRONZE",       "description": "Least expensive material."},
    {"name": "Paint",                    "one_in": 512,      "color": "WHITE",        "description": "That kid played with paint bruh"},
    {"name": "Gold",                     "one_in": 673,      "color": "GOLD",         "description": "Very expensive material!"},
    {"name": "Fissure",                  "one_in": 724,      "color": "BLUE",         "biome": "Calamity"},
    {"name": "Water",                    "one_in": 825,      "color": "LIGHT_BLUE",   "description": "Its time to drink water!", "biome": "Rainy"},
    {"name": "Voxel",                    "one_in": 937,      "color": "GREEN"},
    {"name": "Vortex",                   "one_in": 1100,     "color": "PURPLE",       "description": "How did you steal a vortex from space?", "biome": "Cosmic"},
    {"name": "Starfall",                 "one_in": 2750,     "color": "MAGENTA",      "description": "The star is falling, Quick! Make a wish!", "biome": "Cosmic"},
    {"name": "Hate",                     "one_in": 3300,     "color": "DARK_RED",     "description": "Hated.", "biome": "Calamity"},
    {"name": "Windswept",                "one_in": 3530,     "color": "CYAN",         "description": "Breezing winds sweep through your body, refreshing you.", "biome": "Windy"},
    {"name": "Static",                   "one_in": 4040,     "color": "GRAY",         "biome": "FATAL ERROR"},
    {"name": "Error",                    "one_in": 11111111, "color": "RED",          "description": "[FATAL ERROR] exclusive.", "biome": "FATAL ERROR", "no_boost": True},
    {"name": "Shield",                   "one_in": 4753,     "color": "BLUE",         "description": "Hes protected!"},
    {"name": "Portal Master",            "one_in": 5000,     "color": "WHITE"},
    {"name": "Empower",                  "one_in": 5005,     "color": "WHITE"},
    {"name": "Bloodshed",                "one_in": 6666,     "color": "DARK_RED",     "description": "The blood.", "biome": "Crimson"},
    {"name": "Hacker",                   "one_in": 7777,     "color": "GREEN",        "description": "Binary being of the matrix world.", "biome": "Matrix"},
    {"name": "Spectral",                 "one_in": 8192,     "color": "CYAN",         "description": "The spinning souls.", "biome": "Foggy"},
    {"name": "Vortex : Blackhole",       "one_in": 11100,    "color": "PURPLE",       "description": "It devours everything in its path.", "biome": "Cosmic"},
    {"name": "Moonstone",                "one_in": 14050,    "color": "MOON",         "description": "A fragment of the silent moon."},
    {"name": "Teacup",                   "one_in": 16000,    "color": "ORANGE",       "description": "Submines favourite drink: Tea."},
    {"name": "Confusion",                "one_in": 17000,    "color": "WHITE",        "description": "Im so confused."},
    {"name": "Shade",                    "one_in": 19000,    "color": "GRAY",         "description": "Pure darkness.", "biome": "Calamity"},
    {"name": "Abnormal",                 "one_in": 24000,    "color": "CYAN"},
    {"name": "RUNES",                    "one_in": 30000,    "color": "PINK",         "description": "runes wooooooo creepy old wooo"},
    {"name": "Divine",                   "one_in": 32768,    "color": "YELLOW",       "description": "The divine being."},
    {"name": "Absolute",                 "one_in": 50000,    "color": "ORANGE",       "description": "RRRRRRAAHHHHHHHHHHHHHH!!!"},
    {"name": "Azure",                    "one_in": 60000,    "color": "BLUE"},
    {"name": "Hacker : Virtual",         "one_in": 77777,    "color": "LIGHT_BLUE",   "description": "Powerful binary being.", "biome": "Matrix"},
    {"name": "Genesis",                  "one_in": 100000,   "color": "PINK",         "description": "This auras element is unknown."},
    {"name": "Tornado",                  "one_in": 200000,   "color": "GRAY",         "description": "2 gust of winds spinning eternally."},
    {"name": "Ethereal",                 "one_in": 400000,   "color": "PURPLE",       "description": "Bruh"},
    {"name": "Claymore",                 "one_in": 596000,   "color": "ORANGE",       "description": "A warrior"},
    {"name": "Spectral : Blessed",       "one_in": 600000,   "color": "BLUE",         "biome": "Foggy"},
    {"name": "Residue",                  "one_in": 675435,   "color": "RED",          "biome": "Crimson"},
    {"name": "Vines",                    "one_in": 730000,   "color": "GREEN",        "biome": "Jungle"},
    {"name": "Exotic Melody",            "one_in": 888000,   "color": "RED",          "description": "I have very musical mind!"},
    {"name": "Genesis : Omega",          "one_in": 1000000,  "color": "DARK_RED"},
    {"name": "Azure : Khalira",          "one_in": 1600000,  "color": "BLUE"},
    {"name": "Frostbite",                "one_in": 1948090,  "color": "LIGHT_BLUE",   "description": "The arm is frozen.", "biome": "Snowy"},
    {"name": "Voxel : Platformer",       "one_in": 1995400,  "color": "GREEN"},
    {"name": "Cybernetic",               "one_in": 2400000,  "color": "BLUE",         "description": "Hologramms"},
    {"name": "Resilience",               "one_in": 4000000,  "color": "WHITE"},
    {"name": "Cataclysm",                "one_in": 5000000,  "color": "GRAY",         "biome": "Calamity"},
    {"name": "Life Force",               "one_in": 6000000,  "color": "RED"},
    {"name": "Eternal",                  "one_in": 7500000,  "color": "PINK"},
    {"name": "Snowfall",                 "one_in": 7920000,  "color": "LIGHT_BLUE",   "biome": "Snowy"},
    {"name": "OVERSEER",                 "one_in": 9240000,  "color": "GREEN",        "biome": "Calamity"},
    {"name": "lost",                     "one_in": 9606060,  "color": "GRAY",         "biome": "Foggy"},
    {"name": "Serenity",                 "one_in": 10000000, "color": "ORANGE"},
    {"name": "Nightfall",                "one_in": 11000000, "color": "PURPLE",       "biome": "Night"},
    {"name": "Arcane Guardian",          "one_in": 14000000, "color": "BLUE"},
    {"name": "Starfall : Event Horizon", "one_in": 20000000, "color": "ORANGE",       "biome": "Cosmic"},
    {"name": "RUNES : Time Limit",       "one_in": 23000000, "color": "ORANGE"},
    {"name": "foregoing",                "one_in": 23000000, "color": "CYAN",         "biome": "Rainy"},
    {"name": "Omnipotent",               "one_in": 27000000, "color": "BLUE",         "biome": "Calamity"},
    {"name": "Snowfall : Blizzard",      "one_in": 38360000, "color": "LIGHT_BLUE",   "biome": "Snowy"},
    {"name": "Bloodshed : Ritual",       "one_in": 46666666, "color": "DARK_RED",     "biome": "Crimson"},
    {"name": "Desolation",               "one_in": 60344706, "color": "GRAY",         "biome": "Foggy"},
    {"name": "SPEEDRUN",                 "one_in": 65000000, "color": "WHITE"},
    {"name": "DEVIATION",                "one_in": 75000000, "color": "GRAY"},
    {"name": "Exotic Melody : Extension","one_in": 88800000, "color": "RED"},
    {"name": "Flame : Inferno",          "one_in": 100000000,"color": "ORANGE"},
    {"name": "Sunken",                   "one_in": 110000000,"color": "BLUE",         "biome": "Rainy"},
    {"name": "Euphoria",                 "one_in": 122500000,"color": "PINK"},
    {"name": "Taiga",                    "one_in": 160000000,"color": "DARK_GREEN"},
    {"name": "Genesis : Delta",          "one_in": 250000000,"color": "GREEN"},
    {"name": "Circuit",                  "one_in": 253080000,"color": "GREEN",        "biome": "Matrix"},
    {"name": "Nightfall : Reality",      "one_in": 300000000,"color": "PURPLE",       "biome": "Night"},
    {"name": "Doombringer",              "one_in": 340000000,"color": "RED",          "biome": "Calamity"},
    {"name": "Nightfall : Vioralis",     "one_in": 377000000,"color": "BLUE",         "biome": "Night"},
    {"name": "MELTDOWN",                 "one_in": 400000000,"color": "RED"},
    {"name": "Cataclysm : Finality",     "one_in": 500000000,"color": "GRAY",         "biome": "Calamity"},
    {"name": "Syntherion",               "one_in": 720000000,"color": "BLUE"},
    {"name": "Destiny",                  "one_in": 1000000000,"color": "GOLD",        "description": "The [EXOTIC] power has found you...", "special": "destiny"},
    {"name": "Infinix",                  "one_in": 1100000000,"color": "VOLT_BLUE",   "description": "[OMEGA] has chosen you...", "special": "infinix"},
]
auras.sort(key=lambda x: x["one_in"])

# ── GLOVES ─────────────────────────────────
GLOVES = {
    "Metal": {"color": "GRAY", "bonus": 0, "description": "Crafting ingredient", "is_ingredient": True,
              "craft": {"Common": 3, "Cool": 3, "Rare": 1}},
    "Luck Glove": {"color": "GREEN", "bonus": 0.25, "description": "+25% Luck", "is_ingredient": False,
                   "craft": {"Metal": 1, "Common": 5, "Rare": 3}},
    "Speed Glove": {"color": "CYAN", "bonus": 0, "description": "+10% Roll Speed", "is_ingredient": False, "speed_bonus": 0.1,
                    "craft": {"Metal": 2, "Cool": 8, "Shiny": 2}},
    "Fortune Glove": {"color": "GOLD", "bonus": 0.5, "description": "+50% Luck", "is_ingredient": False,
                      "craft": {"Metal": 3, "Gold": 3, "Divine": 1, "Rare": 5}},
    "Cosmic Glove": {"color": "PURPLE", "bonus": 1.0, "description": "+100% Luck, +5% Speed", "is_ingredient": False, "speed_bonus": 0.05,
                     "craft": {"Metal": 5, "Vortex": 2, "Starfall": 1, "Vortex : Blackhole": 1}},
    "Rainbow Glove": {"color": "MAGENTA", "bonus": 1.5, "description": "+150% Luck", "is_ingredient": False,
                      "craft": {"Metal": 8, "Paint": 5, "Shiny": 3, "Exotic Melody": 1}},
    "Shadow Glove": {"color": "GRAY", "bonus": 1.8, "description": "+180% Luck, +8% Speed", "is_ingredient": False, "speed_bonus": 0.08,
                     "craft": {"Metal": 12, "Shade": 5, "Confusion": 3, "lost": 2}},
    "Matrix Glove": {"color": "GREEN", "bonus": 2.0, "description": "+200% Luck, +10% Speed", "is_ingredient": False, "speed_bonus": 0.1,
                     "craft": {"Metal": 10, "Hacker": 3, "Hacker : Virtual": 1}},
    "Volt Glove": {"color": "LIGHT_BLUE", "bonus": 2.5, "description": "+250% Luck, +12% Speed", "is_ingredient": False, "speed_bonus": 0.12,
                   "craft": {"Metal": 15, "Static": 5, "Cybernetic": 3, "Azure": 2, "Azure : Khalira": 1}},
    "Inferno Glove": {"color": "ORANGE", "bonus": 3.0, "description": "+300% Luck", "is_ingredient": False,
                      "craft": {"Metal": 20, "Flame": 10, "Flame : Inferno": 3, "MELTDOWN": 1, "Residue": 2}},
    "Crimson Glove": {"color": "DARK_RED", "bonus": 3.5, "description": "+350% Luck", "is_ingredient": False,
                      "craft": {"Metal": 25, "Bloodshed": 5, "Bloodshed : Ritual": 2, "Devil": 2, "Hate": 5}},
    "Frost Device": {"color": "WHITE", "bonus": 4.0, "description": "+400% Luck, +15% Speed", "is_ingredient": False, "speed_bonus": 0.15,
                     "craft": {"Metal": 30, "Frostbite": 5, "Snowfall": 3, "Snowfall : Blizzard": 2, "HOARFROST": 1, "CRYOGEN": 1}},
    "Void Device": {"color": "DARK_RED", "bonus": 5.0, "description": "+500% Luck", "is_ingredient": False,
                    "craft": {"Metal": 40, "Vortex": 8, "Vortex : Blackhole": 3, "Starfall : Event Horizon": 2, "Omnipotent": 1, "Cataclysm": 1, "Cataclysm : Finality": 1}},
    "Eternal Device": {"color": "PINK", "bonus": 6.0, "description": "+600% Luck, +18% Speed", "is_ingredient": False, "speed_bonus": 0.18,
                       "craft": {"Metal": 50, "Eternal": 5, "Ethereal": 3, "Serenity": 2, "Euphoria": 1, "MELTDOWN": 1}},
    "Matrix Device": {"color": "GREEN", "bonus": 7.0, "description": "+700% Luck, +20% Speed", "is_ingredient": False, "speed_bonus": 0.2,
                      "craft": {"Metal": 60, "Hacker": 10, "Hacker : Virtual": 3, "Circuit": 2, "SPEEDRUN": 1, "Genesis : Delta": 1}},
    "Omega Device": {"color": "VOLT_BLUE", "bonus": 10.0, "description": "+1000% Luck, +25% Speed", "is_ingredient": False, "speed_bonus": 0.25,
                     "craft": {"Metal": 100, "Genesis": 10, "Genesis : Omega": 5, "Genesis : Delta": 2, "Destiny": 1, "Infinix": 1}},
}

# ── POTIONS ────────────────────────────────
POTIONS = {
    "Divine Potion I": {"color": "YELLOW", "description": "+70,000x Luck (ONE ROLL, STACKS)", "one_time": True, "luck_bonus": 70000,
                        "craft": {"Divine": 1, "Charged": 10, "Gold": 5}},
    "Divine Potion II": {"color": "GOLD", "description": "+300,000x Luck (ONE ROLL, STACKS)", "one_time": True, "luck_bonus": 300000,
                         "craft": {"Divine": 5, "Charged": 30, "Gold": 30}},
    "Lucky Potion I": {"color": "GREEN", "description": "+1.5x Luck (3.5 min, STACKABLE)", "one_time": False, "luck_bonus_pct": 1.5, "duration": 210, "stackable": True,
                       "craft": {"Lucky": 25, "Gold": 10}},
    "Lucky Potion II": {"color": "GREEN", "description": "+2x Luck (5 min, STACKABLE)", "one_time": False, "luck_bonus_pct": 2.0, "duration": 300, "stackable": True,
                        "craft": {"Lucky": 50, "Gold": 35}},
    "Lucky Potion III": {"color": "GREEN", "description": "+3x Luck (8 min, STACKABLE)", "one_time": False, "luck_bonus_pct": 3.0, "duration": 480, "stackable": True,
                         "craft": {"Lucky": 75, "Bronze": 10, "Silver": 10, "Gold": 10}},
    "Speed Potion I": {"color": "CYAN", "description": "+30% Roll Speed (1 min, STACKABLE)", "one_time": False, "speed_bonus": 0.3, "duration": 60, "stackable": True,
                       "craft": {"Charged": 25, "Windswept": 1}},
    "Speed Potion II": {"color": "CYAN", "description": "+40% Roll Speed (1.5 min, STACKABLE)", "one_time": False, "speed_bonus": 0.4, "duration": 90, "stackable": True,
                        "craft": {"Charged": 50, "Windswept": 5}},
    "Speed Potion III": {"color": "CYAN", "description": "+50% Roll Speed (2 min, STACKABLE)", "one_time": False, "speed_bonus": 0.5, "duration": 120, "stackable": True,
                         "craft": {"Charged": 100, "Windswept": 20}},
}

# ── ACHIEVEMENTS ───────────────────────────
ACHIEVEMENTS = [
    {"id": "welcome", "name": "Welcome", "desc": "Join the game for the first time.", "type": "join", "target": 1, "rewards": {}},
    {"id": "roll_100", "name": "Hundred of many", "desc": "Roll 100 times.", "type": "rolls", "target": 100, "rewards": {"Lucky Potion I": 10, "Speed Potion II": 10}},
    {"id": "roll_1000", "name": "Thousands of many", "desc": "Roll 1,000 times.", "type": "rolls", "target": 1000, "rewards": {"Lucky Potion I": 25, "Speed Potion I": 25, "Lucky Potion II": 5}},
    {"id": "roll_10000", "name": "I cant stop gambling", "desc": "Roll 10,000 times.", "type": "rolls", "target": 10000, "rewards": {"Lucky Potion III": 10, "Speed Potion II": 5, "Divine Potion I": 1}},
    {"id": "roll_100000", "name": "I HAVE AN ADDICT!!", "desc": "Roll 100,000 times.", "type": "rolls", "target": 100000, "rewards": {"Lucky Potion III": 25, "Speed Potion III": 25, "Divine Potion II": 2}},
    {"id": "rare_1k", "name": "That's rare!", "desc": "Roll an aura with rarity >= 1/1,000.", "type": "rarity", "target": 1000, "rewards": {"Lucky Potion I": 3}},
    {"id": "rare_10k", "name": "Getting rarer...", "desc": "Roll an aura with rarity >= 1/10,000.", "type": "rarity", "target": 10000, "rewards": {"Speed Potion I": 5}},
    {"id": "rare_100k", "name": "Super rare!", "desc": "Roll an aura with rarity >= 1/100,000.", "type": "rarity", "target": 100000, "rewards": {"Divine Potion I": 1}},
    {"id": "rare_1m", "name": "One in a million", "desc": "Roll an aura with rarity >= 1/1,000,000.", "type": "rarity", "target": 1000000, "rewards": {"Divine Potion II": 1}},
    {"id": "rare_10m", "name": "Ten millions!", "desc": "Roll an aura with rarity >= 1/10,000,000.", "type": "rarity", "target": 10000000, "rewards": {"Divine Potion II": 2}},
    {"id": "rare_100m", "name": "Hundred million!", "desc": "Roll an aura with rarity >= 1/100,000,000.", "type": "rarity", "target": 100000000, "rewards": {"Divine Potion II": 5}},
    {"id": "rare_1b", "name": "BILLIONAIRE", "desc": "Roll an aura with rarity >= 1/1,000,000,000.", "type": "rarity", "target": 1000000000, "rewards": {"Divine Potion II": 10, "Lucky Potion III": 50}},
    {"id": "stat_10k", "name": "Collector", "desc": "Reach 10,000 Stat Collected.", "type": "stat", "target": 10000, "rewards": {"Lucky Potion I": 10}},
    {"id": "stat_100k", "name": "Hoarder", "desc": "Reach 100,000 Stat Collected.", "type": "stat", "target": 100000, "rewards": {"Speed Potion II": 5}},
    {"id": "stat_1m", "name": "Treasure Hunter", "desc": "Reach 1,000,000 Stat Collected.", "type": "stat", "target": 1000000, "rewards": {"Divine Potion I": 1}},
    {"id": "stat_10m", "name": "Millionaire", "desc": "Reach 10,000,000 Stat Collected.", "type": "stat", "target": 10000000, "rewards": {"Divine Potion II": 1}},
    {"id": "stat_100m", "name": "Dragon's Hoard", "desc": "Reach 100,000,000 Stat Collected.", "type": "stat", "target": 100000000, "rewards": {"Divine Potion II": 3}},
    {"id": "stat_1b", "name": "Legendary Collector", "desc": "Reach 1,000,000,000 Stat Collected.", "type": "stat", "target": 1000000000, "rewards": {"Divine Potion II": 10, "Lucky Potion III": 25}},
    {"id": "stat_10b", "name": "GOD COLLECTOR", "desc": "Reach 10,000,000,000 Stat Collected.", "type": "stat", "target": 10000000000, "rewards": {"Divine Potion II": 50, "Lucky Potion III": 100}},
]

# ── Helpers ────────────────────────────────
def fmt_number(n):
    return f"{n:,}"

def format_stat(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)

# ── Game Data per User ─────────────────────
# Structure: user_id (str) -> { rolls, inventory, stat, glove_inventory, equipped_glove, potion_inventory, active_potions, achievements_state, obby_active, obby_end_time, obby_cooldown_end, obby_variant, auto_roll_active, bonus_ready, current_biome, biome_change_time, last_roll_time, one_time_counts }
game_data = {}

def get_user_data(uid):
    if uid not in game_data:
        game_data[uid] = {
            "rolls": 0,
            "inventory": {},
            "stat": 0,
            "glove_inventory": {},
            "equipped_glove": None,
            "potion_inventory": {},
            "active_potions": {},
            "achievements_state": {},
            "obby_active": False,
            "obby_end_time": 0,
            "obby_cooldown_end": 0,
            "obby_variant": "Default Obby",
            "auto_roll_active": False,
            "bonus_ready": False,
            "current_biome": "Windy",
            "biome_change_time": time.time() + random.randint(30, 120),
            "last_roll_time": 0,
            "one_time_counts": {},
        }
    return game_data[uid]

def save_all():
    with open(SAVE_FILE, "w") as f:
        json.dump(game_data, f)
    save_to_github()

def load_all():
    global game_data
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            game_data = json.load(f)

# ── Bot Setup ──────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    load_all()
    try:
        synced = await bot.tree.sync()
        print(f"Bot online! Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

# ── Biome management ──────────────────────
def update_biome(data):
    if time.time() >= data["biome_change_time"]:
        prev = data["current_biome"]
        available = [b for b in BIOMES if b != prev]
        weights = [BIOMES[b]["spawn_chance"] for b in available]
        data["current_biome"] = random.choices(available, weights=weights, k=1)[0]
        data["biome_change_time"] = time.time() + random.randint(30, 120)

def get_biome_multiplier(data):
    return BIOMES[data["current_biome"]]["multiplier"]

# ── Glove bonuses ──────────────────────────
def get_glove_bonus(data):
    eq = data.get("equipped_glove")
    if eq and eq in GLOVES:
        return GLOVES[eq]["bonus"]
    return 0

def get_glove_speed_bonus(data):
    eq = data.get("equipped_glove")
    if eq and eq in GLOVES:
        return GLOVES[eq].get("speed_bonus", 0)
    return 0

# ── Potion logic ──────────────────────────
def get_active_potion_luck_pct(data):
    pct = 0
    now = time.time()
    for key, end_time in list(data["active_potions"].items()):
        base_name = key.rsplit("_", 1)[0] if "_" in key else key
        if now < end_time and base_name in POTIONS:
            p = POTIONS[base_name]
            if not p.get("one_time", False):
                pct += p.get("luck_bonus_pct", 0)
    return pct

def get_active_potion_speed(data):
    spd = 0
    now = time.time()
    for key, end_time in list(data["active_potions"].items()):
        base_name = key.rsplit("_", 1)[0] if "_" in key else key
        if now < end_time and base_name in POTIONS:
            p = POTIONS[base_name]
            if not p.get("one_time", False):
                spd += p.get("speed_bonus", 0)
    return spd

def get_roll_cooldown(data):
    base = 0.5
    glove_spd = get_glove_speed_bonus(data)
    potion_spd = get_active_potion_speed(data)
    total_bonus = glove_spd + potion_spd
    return max(0.1, base * (1.0 - total_bonus))

# ── Stat Collected ─────────────────────────
def get_stat(data):
    total = 0
    for aura in auras:
        cnt = data["inventory"].get(aura["name"], 0)
        total += aura["one_in"] * cnt
    return total

# ── Main Roll Logic ────────────────────────
def do_roll_logic(data):
    update_biome(data)
    data["rolls"] += 1

    if data["rolls"] % 10 == 0:
        data["bonus_ready"] = True

    base_luck = 2 if data["bonus_ready"] else 1
    obby_mult = 1
    if data["obby_active"] and time.time() < data["obby_end_time"]:
        obby_mult = {"Default Obby": 1.0, "Obby+": 1.5, "Obby++": 2.5}[data["obby_variant"]]
    glove_bonus = get_glove_bonus(data)
    potion_pct = get_active_potion_luck_pct(data)

    # Consume ONE one-time potion
    one_time_bonus = 0
    now = time.time()
    for uid, end_time in list(data["active_potions"].items()):
        base_name = uid.rsplit("_", 1)[0] if "_" in uid else uid
        if base_name in POTIONS and POTIONS[base_name].get("one_time", False):
            if now < end_time:
                if one_time_bonus == 0:
                    one_time_bonus = POTIONS[base_name]["luck_bonus"]
                del data["active_potions"][uid]
                break

    player_luck = base_luck * obby_mult + glove_bonus + potion_pct + one_time_bonus
    if player_luck < 1:
        player_luck = 1

    biome_mult = get_biome_multiplier(data)
    biome_name = data["current_biome"]

    # Build rollable auras
    rollable = []
    for aura in auras:
        aura_biome = aura.get("biome")
        no_boost = aura.get("no_boost", False)

        if no_boost and aura_biome == "FATAL ERROR":
            if biome_name == "FATAL ERROR":
                rollable.append((aura, 1.0))
            continue

        if biome_name == "FATAL ERROR":
            eff = player_luck * biome_mult
        elif aura_biome and aura_biome == biome_name:
            eff = player_luck * biome_mult
        else:
            eff = player_luck

        if eff < 1:
            eff = 1
        if eff > aura["one_in"] and not no_boost:
            continue
        rollable.append((aura, eff))

    if not rollable:
        best_aura = auras[-1]
        best_mult = 1
        for aura in reversed(auras):
            if aura.get("no_boost") and aura.get("biome") == "FATAL ERROR":
                if biome_name == "FATAL ERROR":
                    best_aura, best_mult = aura, 1
                    break
            else:
                ab = aura.get("biome")
                if biome_name == "FATAL ERROR":
                    eff = player_luck * biome_mult
                elif ab and ab == biome_name:
                    eff = player_luck * biome_mult
                else:
                    eff = player_luck
                if eff < 1: eff = 1
                if eff <= aura["one_in"]:
                    best_aura, best_mult = aura, eff
                    break
        rollable = [(best_aura, best_mult)]

    total_weight = sum(1.0 / a["one_in"] * m for a, m in rollable)
    roll_val = random.random() * total_weight
    cumulative = 0
    for aura, eff in rollable:
        cumulative += (1.0 / aura["one_in"]) * eff
        if roll_val <= cumulative:
            name = aura["name"]
            color = COLORS.get(aura["color"], 0xFFFFFF)
            one_in = aura["one_in"]
            desc = aura.get("description", "")
            special = aura.get("special", "")

            # Update inventory & stat
            data["inventory"][name] = data["inventory"].get(name, 0) + 1
            data["bonus_ready"] = False

            # Rarity achievements
            for ach in ACHIEVEMENTS:
                if ach["type"] == "rarity":
                    if ach["id"] not in data["achievements_state"]:
                        data["achievements_state"][ach["id"]] = {"unlocked": False, "claimed": False}
                    if not data["achievements_state"][ach["id"]]["unlocked"] and one_in >= ach["target"]:
                        data["achievements_state"][ach["id"]]["unlocked"] = True

            # Roll achievements
            for ach in ACHIEVEMENTS:
                if ach["type"] == "rolls":
                    if ach["id"] not in data["achievements_state"]:
                        data["achievements_state"][ach["id"]] = {"unlocked": False, "claimed": False}
                    if not data["achievements_state"][ach["id"]]["unlocked"] and data["rolls"] >= ach["target"]:
                        data["achievements_state"][ach["id"]]["unlocked"] = True

            # Stat achievements
            stat_val = get_stat(data)
            for ach in ACHIEVEMENTS:
                if ach["type"] == "stat":
                    if ach["id"] not in data["achievements_state"]:
                        data["achievements_state"][ach["id"]] = {"unlocked": False, "claimed": False}
                    if not data["achievements_state"][ach["id"]]["unlocked"] and stat_val >= ach["target"]:
                        data["achievements_state"][ach["id"]]["unlocked"] = True

            save_all()
            return name, one_in, color, desc, special, player_luck, biome_name

    # Fallback
    aura = auras[0]
    data["inventory"]["Common"] = data["inventory"].get("Common", 0) + 1
    data["bonus_ready"] = False
    save_all()
    return "Common", 3, COLORS["GRAY"], auras[0]["description"], "", player_luck, biome_name

# ── Slash Commands ─────────────────────────

@bot.tree.command(name="roll", description="Roll for a random aura")
async def slash_roll(interaction: discord.Interaction):
    data = get_user_data(str(interaction.user.id))
    now = time.time()
    cooldown = get_roll_cooldown(data)
    if now - data["last_roll_time"] < cooldown:
        await interaction.response.send_message("Slow down! Wait a moment before rolling again.", ephemeral=True)
        return
    data["last_roll_time"] = now

    name, one_in, color, desc, special, luck, biome = do_roll_logic(data)
    embed = discord.Embed(title=f">>> ROLLED: {name}!", description=desc or "", color=color)
    embed.add_field(name="Rarity", value=f"1/{one_in:,}", inline=True)
    embed.add_field(name="Rolls", value=str(data["rolls"]), inline=True)
    embed.set_footer(text=f"Stat Collected: {format_stat(get_stat(data))} | Biome: {biome}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="inv", description="Show your aura inventory")
async def slash_inv(interaction: discord.Interaction):
    data = get_user_data(str(interaction.user.id))
    inv = data["inventory"]
    if not inv:
        await interaction.response.send_message("Your inventory is empty. Use /roll first!")
        return
    embed = discord.Embed(title="Inventory", color=0x00FF00)
    for aura in auras:
        if aura["name"] in inv:
            embed.add_field(name=aura["name"], value=f"x{inv[aura['name']]} (1/{aura['one_in']:,})", inline=True)
    embed.set_footer(text=f"Rolls: {data['rolls']:,} | Stat: {format_stat(get_stat(data))}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="lb", description="Leaderboard by Stat Collected")
async def slash_lb(interaction: discord.Interaction):
    if not game_data:
        await interaction.response.send_message("Nobody has played yet!")
        return
    sorted_u = sorted(game_data.items(), key=lambda x: get_stat(x[1]), reverse=True)[:10]
    embed = discord.Embed(title="Leaderboard", color=0xFFD700)
    for i, (uid, udata) in enumerate(sorted_u):
        user = bot.get_user(int(uid)) or (await bot.fetch_user(int(uid)))
        name = user.name if user else f"Unknown"
        stat_val = get_stat(udata)
        embed.add_field(name=f"{i+1}. {name}", value=f"Stat: {format_stat(stat_val)} | Rolls: {udata['rolls']:,}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="achievements", description="View your achievements")
async def slash_achievements(interaction: discord.Interaction):
    data = get_user_data(str(interaction.user.id))
    embed = discord.Embed(title="Achievements", color=0x00FF00)
    for ach in ACHIEVEMENTS:
        aid = ach["id"]
        if aid not in data["achievements_state"]:
            data["achievements_state"][aid] = {"unlocked": False, "claimed": False}
        st = data["achievements_state"][aid]
        if st["claimed"]:
            status = "[CLAIMED]"
        elif st["unlocked"]:
            status = "[CLAIM REWARDS]"
        else:
            if ach["type"] == "rolls":
                status = f"({data['rolls']}/{ach['target']} rolls)"
            elif ach["type"] == "stat":
                status = f"({format_stat(get_stat(data))}/{format_stat(ach['target'])})"
            elif ach["type"] == "rarity":
                status = "[???]"
            else:
                status = "[LOCKED]"
        embed.add_field(name=ach["name"], value=f"{ach['desc']} -- {status}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="List all commands")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(title="Commands", color=0x00FF00)
    embed.add_field(name="/roll", value="Roll for an aura", inline=False)
    embed.add_field(name="/inv", value="Show inventory", inline=False)
    embed.add_field(name="/lb", value="Leaderboard", inline=False)
    embed.add_field(name="/achievements", value="Achievements", inline=False)
    await interaction.response.send_message(embed=embed)

if TOKEN is None:
    print("TOKEN not found! Set it as an environment variable.")
else:
    bot.run(TOKEN)
