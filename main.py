import discord
from discord.ext import commands, tasks
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ตัวอย่างเควส
daily_quests = [
    "ทำท่า Squat 15 ครั้ง",
    "อ่านหนังสือพัฒนาตนเอง 20 นาที",
    "วางแผนเป้าหมายวันนี้",
    "ดื่มน้ำให้ครบ 2 แก้ว",
    "นั่งสมาธิ 5 นาที"
]

special_quests = [
    "เขียนไดอารี่วิเคราะห์ตัวเอง 1 หน้า",
    "ออกกำลังกาย 20 นาทีติดกัน",
    "ไม่แตะมือถือ 1 ชั่วโมง",
    "หายใจลึกช้า 10 ครั้ง พร้อมตั้งสติ",
    "ทำสิ่งที่กลัวมาโดยตลอด 1 อย่าง"
]

user_completed = False  # ไว้เช็กว่าผู้เล่นส่งเควสแล้วหรือยัง

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    special_quest_loop.start()

@bot.command()
async def quest(ctx):
    quest = random.choice(daily_quests)
    await ctx.send(f"เควสประจำวันของคุณคือ: *{quest}*")

@bot.command()
async def complete(ctx):
    global user_completed
    user_completed = True
    await ctx.send("คุณส่งเควสแล้ว ระบบจะเริ่มนับ 3 ชั่วโมงใหม่")

@tasks.loop(minutes=1)
async def special_quest_loop():
    global user_completed
    now = int(asyncio.get_event_loop().time()) % 86400  # วินาทีในวัน
    time_slots = [19800, 30600, 41400, 52200, 63000]  # ทุก 3 ชม. เริ่ม 5:30 - 21:30 (วินาที)
    if any(abs(now - t) < 60 for t in time_slots) and user_completed:
        channel = discord.utils.get(bot.get_all_channels(), name="general")
        if channel:
            quest = random.choice(special_quests)
            await channel.send(f"*[เควสพิเศษปรากฏ!]* {quest}")
            user_completed = False

# Run bot
bot.run(os.environ['TOKEN'])