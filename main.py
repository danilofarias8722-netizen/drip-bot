import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
DONO_ID = 1498844150202896446
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class AprovarView(discord.ui.View):
    def __init__(self, cliente_id):
        super().__init__(timeout=None)
        self.cliente_id = cliente_id

    @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.green, custom_id="aprovar_pedido")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != DONO_ID:
            return await interaction.response.send_message("Só o dono pode aprovar!", ephemeral=True)
        
