import discord
from discord import app_commands
import os

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@tree.command(name="loja", description="Abre a loja do servidor")
async def loja(interaction: discord.Interaction):
    await interaction.response.send_message("Loja em construção...",ephemeral=True )

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    tree.clear_commands(guild=None)  # Limpa comandos fantasmas
    await tree.sync()
    print(f'Synced {len(await tree.fetch_commands())} command(s)')

bot.run(os.getenv("DISCORD_TOKEN"))
