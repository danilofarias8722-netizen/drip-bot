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

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💸 Comprar Drip Cliente", style=discord.ButtonStyle.green, custom_id="comprar_drip")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_dm = discord.Embed(
                title="💎 Pagamento Drip Cliente",
                description=f"**Chave PIX:** `{CHAVE_PIX}`\n\n**Valores:**\n1 Dia: R$ 15,00\n3 Dias: R$ 25,00\n7 Dias: R$ 45,00\n\n**Envie o comprovante AQUI nessa DM
