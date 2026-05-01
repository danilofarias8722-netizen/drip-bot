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
    print(f'Bot online como {bot.user}')
    try:
        synced = await tree.sync()
        print(f'Sincronizei {len(synced)} comando(s)')
    except Exception as e:
        print(f'Erro ao sincronizar: {e}')

bot.run(os.getenv("DISCORD_TOKEN"))
