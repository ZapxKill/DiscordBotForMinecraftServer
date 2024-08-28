import discord
from discord.ext import commands
import os
import asyncio

token = ""
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="&")


@bot.event
async def on_ready():
    print("已啟動:", bot.user)


@bot.command()
async def load_cog(context, extension):  # 讀取指定Cog
    await bot.load_extension(f"cmds.{extension}")
    await context.send("loaded")  # 讀取完畢，回傳訊息


@bot.command()
async def unload_cog(context, extension):  # 卸載指定Cog
    await bot.unload_extension(f"cmds.{extension}")
    await context.send("unloaded")  # 卸載完畢，回傳訊息


@bot.command()
async def reload_cog(context, extension):  # 重新讀取指定Cog
    await bot.reload_extension(f"cmds.{extension}")
    await context.send("reloaded")  # 重新讀取完畢，回傳訊息


async def load_extension():
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension("cmds." + filename[:-3])


async def main():
    async with bot:
        await load_extension()
        await bot.start(token)


asyncio.run(main())
