import discord
from discord.ext import commands
from discord import app_commands
import random
import os
import json

# Токен берётся из переменной окружения (безопасно)
TOKEN = os.environ.get("TOKEN")
SAVE_FILE = "rng_save.json"

# Discord embed colours
COLORS = {
    "GRAY": 0x808080, "GREEN": 0x00FF00, "PURPLE": 0x800080,
    "YELLOW": 0xFFFF00, "ORANGE": 0xFF8800, "RED": 0xFF0000,
    "GOLD": 0xFFD700, "CYAN": 0x00FFFF, "WHITE": 0xFFFFFF,
    "PINK": 0xFF69B4, "VOLT_BLUE": 0x33FFFF, "DARK_RED": 0x8B0000,
    "MAGENTA": 0xFF00FF, "LIGHT_BLUE": 0xADD8E6, "SILVER": 0xC0C0C0,
    "BRONZE": 0xCD7F32, "DARK_GREEN": 0x006400, "MOON": 0xF0F0F0,
}

# ── AURAS ──────────────────────────────────
auras = [
    {"name": "Common", "one_in": 3, "color": "GRAY", "description": "That common is very common."},
    {"name": "Cool", "one_in": 6, "color": "GREEN", "description": "That cool is very cool."},
    {"name": "Rare", "one_in": 32, "color": "PURPLE", "description": "That rare is rare."},
    {"name": "Lucky", "one_in": 50, "color": "GREEN", "description": "Feeling lucky!"},
    {"name": "Flame", "one_in": 100, "color": "ORANGE", "description": "It burns!"},
    {"name": "Charged", "one_in": 125, "color": "VOLT_BLUE", "description": "Electric energy flows!"},
    {"name": "Shiny", "one_in": 332, "color": "YELLOW", "description": "You are shiny!"},
    {"name": "Acid", "one_in": 400, "color": "DARK_GREEN", "description": "Toxic liquid of nuclear waste."},
    {"name": "Silver", "one_in": 431, "color": "SILVER", "description": "Expensive material."},
    {"name": "Bronze", "one_in": 256, "color": "BRONZE", "description": "Least expensive material."},
    {"name": "Paint", "one_in": 512, "color": "WHITE", "description": "That kid played with paint bruh"},
    {"name": "Gold", "one_in": 673, "color": "GOLD", "description": "Very expensive material!"},
    {"name": "Fissure", "one_in": 724, "color": "BLUE", "biome": "Calamity"},
    {"name": "Water", "one_in": 825, "color": "LIGHT_BLUE", "description": "Its time to drink water!", "biome": "Rainy"},
    {"name": "Voxel", "one_in": 937, "color": "GREEN"},
    {"name": "Vortex", "one_in": 1100, "color": "PURPLE", "description": "How did you steal a vortex from space?", "biome": "Cosmic"},
    {"name": "Starfall", "one_in": 2750, "color": "MAGENTA", "description": "The star is falling, Quick! Make a wish!", "biome": "Cosmic"},
    {"name": "Hate", "one_in": 3300, "color": "DARK_RED", "description": "Hated.", "biome": "Calamity"},
    {"name": "Windswept", "one_in": 3530, "color": "CYAN", "description": "Breezing winds sweep through your body, refreshing you.", "biome": "Windy"},
    {"name": "Static", "one_in": 4040, "color": "GRAY", "biome": "FATAL ERROR"},
    {"name": "Error", "one_in": 11111111, "color": "RED", "description": "[FATAL ERROR] exclusive.", "biome": "FATAL ERROR", "no_boost": True},
    {"name": "Shield", "one_in": 4753, "color": "BLUE", "description": "Hes protected!"},
    {"name": "Portal Master", "one_in": 5000, "color": "WHITE"},
    {"name": "Empower", "one_in": 5005, "color": "WHITE"},
    {"name": "Bloodshed", "one_in": 6666, "color": "DARK_RED", "description": "The blood.", "biome": "Crimson"},
    {"name": "Hacker", "one_in": 7777, "color": "GREEN", "description": "Binary being of the matrix world.", "biome": "Matrix"},
    {"name": "Spectral", "one_in": 8192, "color": "CYAN", "description": "The spinning souls.", "biome": "Foggy"},
    {"name": "Vortex : Blackhole", "one_in": 11100, "color": "PURPLE", "description": "It devours everything in its path.", "biome": "Cosmic"},
    {"name": "Moonstone", "one_in": 14050, "color": "MOON", "description": "A fragment of the silent moon."},
    {"name": "Teacup", "one_in": 16000, "color": "ORANGE", "description": "Submines favourite drink: Tea."},
    {"name": "Confusion", "one_in": 17000, "color": "WHITE", "description": "Im so confused."},
    {"name": "Shade", "one_in": 19000, "color": "GRAY", "description": "Pure darkness.", "biome": "Calamity"},
    {"name": "Abnormal", "one_in": 24000, "color": "CYAN"},
    {"name": "RUNES", "one_in": 30000, "color": "PINK", "description": "runes wooooooo creepy old wooo"},
    {"name": "Divine", "one_in": 32768, "color": "YELLOW", "description": "The divine being."},
    {"name": "Absolute", "one_in": 50000, "color": "ORANGE", "description": "RRRRRRAAHHHHHHHHHHHHHH!!!"},
    {"name": "Azure", "one_in": 60000, "color": "BLUE"},
    {"name": "Hacker : Virtual", "one_in": 77777, "color": "LIGHT_BLUE", "description": "Powerful binary being.", "biome": "Matrix"},
    {"name": "Genesis", "one_in": 100000, "color": "PINK", "description": "This auras element is unknown."},
    {"name": "Tornado", "one_in": 200000, "color": "GRAY", "description": "2 gust of winds spinning eternally."},
    {"name": "Ethereal", "one_in": 400000, "color": "PURPLE", "description": "Bruh"},
    {"name": "Claymore", "one_in": 596000, "color": "ORANGE", "description": "A warrior"},
    {"name": "Spectral : Blessed", "one_in": 600000, "color": "BLUE", "biome": "Foggy"},
    {"name": "Residue", "one_in": 675435, "color": "RED", "biome": "Crimson"},
    {"name": "Vines", "one_in": 730000, "color": "GREEN", "biome": "Jungle"},
    {"name": "Exotic Melody", "one_in": 888000, "color": "RED", "description": "I have very musical mind!"},
    {"name": "Genesis : Omega", "one_in": 1000000, "color": "DARK_RED"},
    {"name": "Azure : Khalira", "one_in": 1600000, "color": "BLUE"},
    {"name": "Frostbite", "one_in": 1948090, "color": "LIGHT_BLUE", "description": "The arm is frozen.", "biome": "Snowy"},
    {"name": "Voxel : Platformer", "one_in": 1995400, "color": "GREEN"},
    {"name": "Cybernetic", "one_in": 2400000, "color": "BLUE", "description": "Hologramms"},
    {"name": "Resilience", "one_in": 4000000, "color": "WHITE"},
    {"name": "Cataclysm", "one_in": 5000000, "color": "GRAY", "biome": "Calamity"},
    {"name": "Life Force", "one_in": 6000000, "color": "RED"},
    {"name": "Eternal", "one_in": 7500000, "color": "PINK"},
    {"name": "Snowfall", "one_in": 7920000, "color": "LIGHT_BLUE", "biome": "Snowy"},
    {"name": "OVERSEER", "one_in": 9240000, "color": "GREEN", "biome": "Calamity"},
    {"name": "lost", "one_in": 9606060, "color": "GRAY", "biome": "Foggy"},
    {"name": "Serenity", "one_in": 10000000, "color": "ORANGE"},
    {"name": "Nightfall", "one_in": 11000000, "color": "PURPLE", "biome": "Night"},
    {"name": "Arcane Guardian", "one_in": 14000000, "color": "BLUE"},
    {"name": "Starfall : Event Horizon", "one_in": 20000000, "color": "ORANGE", "biome": "Cosmic"},
    {"name": "RUNES : Time Limit", "one_in": 23000000, "color": "ORANGE"},
    {"name": "foregoing", "one_in": 23000000, "color": "CYAN", "biome": "Rainy"},
    {"name": "Omnipotent", "one_in": 27000000, "color": "BLUE", "biome": "Calamity"},
    {"name": "Snowfall : Blizzard", "one_in": 38360000, "color": "LIGHT_BLUE", "biome": "Snowy"},
    {"name": "Bloodshed : Ritual", "one_in": 46666666, "color": "DARK_RED", "biome": "Crimson"},
    {"name": "Desolation", "one_in": 60344706, "color": "GRAY", "biome": "Foggy"},
    {"name": "SPEEDRUN", "one_in": 65000000, "color": "WHITE", "description": "LEVEL UP!?"},
    {"name": "DEVIATION", "one_in": 75000000, "color": "GRAY"},
    {"name": "Exotic Melody : Extension", "one_in": 88800000, "color": "RED"},
    {"name": "Flame : Inferno", "one_in": 100000000, "color": "ORANGE"},
    {"name": "Sunken", "one_in": 110000000, "color": "BLUE", "biome": "Rainy"},
    {"name": "Euphoria", "one_in": 122500000, "color": "PINK"},
    {"name": "Taiga", "one_in": 160000000, "color": "DARK_GREEN"},
    {"name": "Genesis : Delta", "one_in": 250000000, "color": "GREEN"},
    {"name": "Circuit", "one_in": 253080000, "color": "GREEN", "biome": "Matrix"},
    {"name": "Nightfall : Reality", "one_in": 300000000, "color": "PURPLE", "biome": "Night"},
    {"name": "Doombringer", "one_in": 340000000, "color": "RED", "biome": "Calamity"},
    {"name": "Nightfall : Vioralis", "one_in": 377000000, "color": "BLUE", "biome": "Night"},
    {"name": "MELTDOWN", "one_in": 400000000, "color": "RED"},
    {"name": "Cataclysm : Finality", "one_in": 500000000, "color": "GRAY", "biome": "Calamity"},
    {"name": "Syntherion", "one_in": 720000000, "color": "BLUE"},
    {"name": "Destiny", "one_in": 1000000000, "color": "GOLD", "description": "The [EXOTIC] power has found you...", "special": "destiny"},
    {"name": "Infinix", "one_in": 1100000000, "color": "VOLT_BLUE", "description": "[OMEGA] has chosen you...", "special": "infinix"},
]
auras.sort(key=lambda x: x["one_in"])

# ── GAME DATA ──────────────────────────────
game_data = {}

def save_all():
    with open(SAVE_FILE, "w") as f:
        json.dump(game_data, f)

def load_all():
    global game_data
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            game_data = json.load(f)

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

def get_user_data(user_id: str):
    if user_id not in game_data:
        game_data[user_id] = {"rolls": 0, "inventory": {}, "stat": 0}
    return game_data[user_id]

# ── BOT SETUP ──────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    load_all()
    try:
        synced = await bot.tree.sync()
        print(f"✅ {bot.user} is online! Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

# ── /roll ──────────────────────────────────
@bot.tree.command(name="roll", description="Roll for a random aura")
async def slash_roll(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    data = get_user_data(uid)
    data["rolls"] += 1

    for aura in auras:
        if random.random() < 1.0 / aura["one_in"]:
            name = aura["name"]
            color = COLORS.get(aura["color"], 0xFFFFFF)
            if name in data["inventory"]:
                data["inventory"][name] += 1
            else:
                data["inventory"][name] = 1
            data["stat"] += aura["one_in"]
            save_all()

            embed = discord.Embed(title=f">>> ROLLED: {name}!", description=aura.get("description", ""), color=color)
            embed.add_field(name="Rarity", value=f"1/{aura['one_in']:,}", inline=True)
            embed.add_field(name="Rolls", value=str(data["rolls"]), inline=True)
            embed.set_footer(text=f"Stat Collected: {format_stat(data['stat'])}")
            await interaction.response.send_message(embed=embed)
            return

    aura = auras[0]
    data["inventory"]["Common"] = data["inventory"].get("Common", 0) + 1
    data["stat"] += 3
    save_all()
    embed = discord.Embed(title=">>> ROLLED: Common!", description="That common is very common.", color=COLORS["GRAY"])
    embed.add_field(name="Rarity", value="1/3", inline=True)
    embed.add_field(name="Rolls", value=str(data["rolls"]), inline=True)
    await interaction.response.send_message(embed=embed)

# ── /inv ───────────────────────────────────
@bot.tree.command(name="inv", description="Show your aura inventory")
async def slash_inv(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    data = get_user_data(uid)
    inv = data.get("inventory", {})
    if not inv:
        await interaction.response.send_message("Your inventory is empty. Use `/roll` first!")
        return
    embed = discord.Embed(title="🎒 Inventory", color=0x00FF00)
    for aura in auras:
        if aura["name"] in inv:
            embed.add_field(name=aura["name"], value=f"x{inv[aura['name']]} (1/{aura['one_in']:,})", inline=True)
    embed.set_footer(text=f"Rolls: {data['rolls']:,} | Stat: {format_stat(data.get('stat', 0))}")
    await interaction.response.send_message(embed=embed)

# ── /lb ────────────────────────────────────
@bot.tree.command(name="lb", description="Leaderboard by Stat Collected")
async def slash_lb(interaction: discord.Interaction):
    if not game_data:
        await interaction.response.send_message("Nobody has played yet!")
        return
    sorted_u = sorted(game_data.items(), key=lambda x: x[1].get("stat", 0), reverse=True)
    embed = discord.Embed(title="🏆 Leaderboard", color=0xFFD700)
    for i, (uid, udata) in enumerate(sorted_u[:10]):
        user = await bot.fetch_user(int(uid))
        name = user.name if user else "Unknown"
        embed.add_field(name=f"{i+1}. {name}", value=f"Stat: {format_stat(udata.get('stat', 0))} | Rolls: {udata.get('rolls', 0):,}", inline=False)
    await interaction.response.send_message(embed=embed)

# ── /achievements ──────────────────────────
@bot.tree.command(name="achievements", description="View your achievements")
async def slash_achievements(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    data = get_user_data(uid)
    ach_list = [
        {"name": "Welcome", "desc": "Join the game.", "target": 1, "type": "rolls"},
        {"name": "Hundred of many", "desc": "Roll 100 times.", "target": 100, "type": "rolls"},
        {"name": "Thousands of many", "desc": "Roll 1,000 times.", "target": 1000, "type": "rolls"},
        {"name": "Collector", "desc": "Reach 10,000 Stat.", "target": 10000, "type": "stat"},
        {"name": "Hoarder", "desc": "Reach 100,000 Stat.", "target": 100000, "type": "stat"},
        {"name": "Treasure Hunter", "desc": "Reach 1,000,000 Stat.", "target": 1000000, "type": "stat"},
        {"name": "Millionaire", "desc": "Reach 10,000,000 Stat.", "target": 10000000, "type": "stat"},
        {"name": "Dragon's Hoard", "desc": "Reach 100,000,000 Stat.", "target": 100000000, "type": "stat"},
    ]
    embed = discord.Embed(title="🏅 Achievements", color=0x00FF00)
    rolls = data["rolls"]
    stat = data["stat"]
    for ach in ach_list:
        target = ach["target"]
        current = rolls if ach["type"] == "rolls" else stat
        status = "✅" if current >= target else f"❌ ({format_stat(current)}/{format_stat(target)})"
        embed.add_field(name=ach["name"], value=f"{ach['desc']} — {status}", inline=False)
    await interaction.response.send_message(embed=embed)

# ── /help ──────────────────────────────────
@bot.tree.command(name="help", description="List all commands")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Commands", color=0x00FF00)
    embed.add_field(name="/roll", value="Roll for an aura", inline=False)
    embed.add_field(name="/inv", value="Show inventory", inline=False)
    embed.add_field(name="/lb", value="Leaderboard", inline=False)
    embed.add_field(name="/achievements", value="Achievements", inline=False)
    await interaction.response.send_message(embed=embed)

# ── START ──────────────────────────────────
if TOKEN is None:
    print("❌ TOKEN not found! Set it as an environment variable.")
else:
    bot.run(TOKEN)
