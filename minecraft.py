import discord
import base64
import os
import requests
import json
import subprocess
import asyncio
from mcstatus import JavaServer
from discord.ext import commands

jsonfile = open("setting.json")  # 開啟Json設定檔
setting = json.load(jsonfile)  # 讀取Json設定檔
MCserver = None
port = setting["ServerPort"]
ip = setting["ServerIP"]


class minecraft(commands.Cog):
    whilelist = None

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    server = discord.SlashCommandGroup(
        "server",
        description="Minecraft伺服器",
    )

    @server.command(description="查詢Minecraft伺服器狀態")
    async def status(self, ctx):
        await ctx.defer()
        try:
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:{ip}:{port}\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await ctx.send_followup(file=file, embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description="伺服器已下線",
                color=discord.Color.red(),
            )
            await ctx.send_followup(embed=embed)

    @server.command(description="啟動Minecraft伺服器")
    async def start(self, ctx):
        await ctx.defer()
        global MCserver
        try:
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:{ip}:{port}\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await ctx.send_followup(file=file, embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"伺服器啟動中",
                color=discord.Color.yellow(),
            )
            msg = await ctx.send_followup(embed=embed)
            MCserver = subprocess.Popen(
                "start.bat",
                shell=True,
                text=True,
                stdin=subprocess.PIPE,
            )
            await asyncio.sleep(30)
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            decoded_icon = base64.b64decode(
                status.icon.removeprefix("data:image/png;base64,")
            )
            with open("server-icon.png", "wb") as f:
                f.write(decoded_icon)
            file = discord.File("server-icon.png", filename="server-icon.png")
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description=f"IP:{ip}:{port}\n\n版本:{status.version.name}\n\n玩家:{status.players.online}/{status.players.max}\n\n{status.description}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url="attachment://server-icon.png")
            await msg.edit(file=file, embed=embed)

    @server.command(description="關閉Minecraft伺服器")
    async def stop(self, ctx):
        await ctx.defer()
        global MCserver
        try:
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            if status.players.online == 0:
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description="伺服器關閉中",
                    color=discord.Color.yellow(),
                )
                msg = await ctx.send_followup(embed=embed)
                MCserver.stdin.write("stop\n")
                MCserver.communicate()
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description="伺服器已下線",
                    color=discord.Color.red(),
                )
                await msg.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="Minecraft 伺服器",
                    description="伺服器仍有玩家，無法關閉伺服器",
                    color=discord.Color.orange(),
                )
                await ctx.send_followup(embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description="伺服器已下線",
                color=discord.Color.red(),
            )
            await ctx.send_followup(embed=embed)

    whitelist = discord.SlashCommandGroup(
        "whitelist",
        description="minecraft伺服器白名單(一個Discord帳號對一個Minecraft帳號)",
    )

    @whitelist.command(
        name="set",
        description="白名單設定(一個Discord帳號對一個Minecraft帳號)",
    )
    async def set(self, ctx, id: str):
        await ctx.defer()
        whitelistIDs = json.load(open("./botSource/whitelist.json", "r"))
        try:
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            if str(ctx.author.id) in whitelistIDs:
                MCserver.stdin.write(
                    f"whitelist remove {whitelistIDs[str(ctx.author.id)]}\n"
                )
                MCserver.stdin.flush()
                whitelistIDs[str(ctx.author.id)] = id
                MCserver.stdin.write(
                    f"whitelist add {whitelistIDs[str(ctx.author.id)]}\n"
                )
                MCserver.stdin.flush()
                embed = discord.Embed(
                    title="白名單",
                    description=f"已將你的白名單ID更改",
                    color=discord.Color.green(),
                )
                embed.set_author(name=ctx.author)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.add_field(name="Minecraft ID", value=id)
                json.dump(whitelistIDs, open("./botSource/whitelist.json", "w"))
                await ctx.send_followup(embed=embed)
                return
            whitelistIDs[str(ctx.author.id)] = id
            MCserver.stdin.write(f"whitelist add {whitelistIDs[str(ctx.author.id)]}\n")
            MCserver.stdin.flush()
            embed = discord.Embed(
                title="白名單",
                description=f"已加入白名單",
                color=discord.Color.green(),
            )
            embed.set_author(name=ctx.author)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.add_field(name="Minecraft ID", value=id)
            json.dump(whitelistIDs, open("./botSource/whitelist.json", "w"))
            await ctx.send_followup(embed=embed)
        except:
            embed = discord.Embed(
                title="Minecraft 伺服器",
                description="伺服器已下線\n無法加入白名單",
                color=discord.Color.red(),
            )
            await ctx.send_followup(embed=embed)

    @whitelist.command(
        name="show",
        description="白名單名稱對應表",
    )
    async def show(self, ctx):
        await ctx.defer()
        whitelistIDs = json.load(open("./botSource/whitelist.json", "r"))
        discordIDs = list(whitelistIDs.keys())
        minecraftIDs = list(whitelistIDs.values())
        embed = discord.Embed(
            title="白名單",
            description=f"Discord、Minecraft名稱對應表",
            color=discord.Color.nitro_pink(),
        )
        for i in range(len(whitelistIDs)):
            user = await self.bot.fetch_user(int(discordIDs[i]))
            embed.add_field(name=minecraftIDs[i], value=user.mention)
        await ctx.send_followup(embed=embed)


def setup(bot):
    bot.add_cog(minecraft(bot))
