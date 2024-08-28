import discord
import base64
import os
import subprocess
import asyncio
from mcstatus import JavaServer
from discord.ext import commands

MCserver = None


class minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, context):
        try:
            server = await JavaServer.async_lookup("192.168.51.2:25565")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:zapxkill.ddns.net\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await context.send(file=file, embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description="伺服器已下線",
                color=discord.Color.red(),
            )
            await context.send(embed=embed)

    @commands.command()
    async def startServer(self, context):
        global MCserver
        try:
            server = await JavaServer.async_lookup("192.168.51.2:25565")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:zapxkill.ddns.net\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await context.send(file=file, embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"伺服器啟動中",
                color=discord.Color.yellow(),
            )
            msg = await context.send(embed=embed)
            MCserver = subprocess.Popen(
                "start.bat",
                shell=True,
                text=True,
                stdin=subprocess.PIPE,
            )
            await asyncio.sleep(15)
            server = await JavaServer.async_lookup("192.168.51.2:25565")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:zapxkill.ddns.net\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await msg.delete()
            await context.send(file=file, embed=embed)

    @commands.command()
    async def stopServer(self, context):
        global MCserver
        try:
            server = await JavaServer.async_lookup("192.168.51.2:25565")
            status = await server.async_status()
            if status.players.online == 0:
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description=f"伺服器關閉中",
                    color=discord.Color.yellow(),
                )
                msg = await context.send(embed=embed)
                MCserver.stdin.write("stop\n")
                MCserver.communicate()
                await asyncio.sleep(3)
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description="伺服器已下線",
                    color=discord.Color.red(),
                )
                await msg.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description=f"伺服器仍有玩家，無法關閉伺服器",
                    color=discord.Color.orange(),
                )
                await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description="伺服器已下線",
                color=discord.Color.red(),
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(minecraft(bot))
