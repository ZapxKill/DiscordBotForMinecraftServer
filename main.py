import discord
import asyncio
import json
from discord.ext import commands
import os

jsonfile = open("setting.json")  # 開啟Json設定檔
setting = json.load(jsonfile)  # 讀取Json設定檔
intents = discord.Intents.default()  # 取得預設權限
intents.members = True  # 新增成員存取權限
intents.message_content = True  # 新增訊息存取全縣
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():  # 啟動完畢時，終端機顯示機器人名字
    print("已啟動:", bot.user)


@bot.slash_command(description="幫助")
async def help(ctx):
    await ctx.defer()
    embed = discord.Embed(
        title="伺服器管理機器人",
        description=f"可以從我這邊開關伺服器或加入白名單喔!",
        color=discord.Color.blue(),
    )
    embed.set_author(name=bot.user.display_name)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="查詢伺服器", value="/server status")
    embed.add_field(name="開啟伺服器", value="/server start")
    embed.add_field(name="關閉伺服器", value="/server stop\n有人的時候關不掉喔")
    embed.add_field(
        name="白名單管理方法",
        value="一個Discord帳號只能對應一個Minecraft帳號\n/whitelist set 設定你的MinecraftID\n/whitelist show 查看目前白名單",
    )
    embed.add_field(name="機器人問題請詢問", value="<@430337322123395076>")
    await ctx.send_followup(embed=embed)


for filename in os.listdir("./botSource"):
    if filename.endswith(".py"):
        bot.load_extension("botSource." + filename[:-3])
        print(f"擴充: {filename[:-3]} 已加載")

loop = asyncio.get_event_loop()
loop.run_until_complete(
    bot.start(
        setting["TOKEN"]
    )
)  # 給予Token，啟動Bot
