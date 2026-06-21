import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import Database

# 🔥 IMPORTANTE: Agregar la ruta raíz para importar keep_alive
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


class DuelBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )
        self.db: Database = Database("discord-bot/data/bot.db")

    async def setup_hook(self):
        await self.db.initialize()
        await self.load_extension("cogs.duels")
        await self.load_extension("cogs.autorole")
        await self.load_extension("cogs.tickets")
        await self.load_extension("cogs.pvp_channels")
        await self.load_extension("cogs.xp_ranks")
        await self.load_extension("cogs.match_system")
        await self.tree.sync()
        print("Slash commands synced.")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="PvP Duels | /duel",
            )
        )


async def main():
    os.makedirs("discord-bot/data", exist_ok=True)
    bot = DuelBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    # 🔥 KEEP ALIVE - Mantiene el bot funcionando 24/7
    keep_alive()
    asyncio.run(main())
