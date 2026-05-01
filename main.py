import discord
import os
from discord import app_commands

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    # Pega o ID da Variable GUILD_ID do Railway
    guild_id = int(os.getenv("GUILD_ID"))
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f'Bot {bot.user} tá online!')
    print('Comando /loja registrado!')

@tree.command(name="loja", description="Abre a loja do servidor")
async def loja(interaction: discord.Interaction):
    await interaction.response.send_message("A loja tá aberta! 🛒")

# Pega o TOKEN da Variable do Railway
bot.run(os.getenv("TOKEN"))
