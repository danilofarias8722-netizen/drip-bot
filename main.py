import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
DONO_ID = 1498844150202896446
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.default()
intents.message_content = True  # OBRIGATÓRIO pra ler DM
bot = commands.Bot(command_prefix="!", intents=intents)

# BOTÃO DE APROVAR/REPROVAR QUE VAI PRA TI
class AprovarView(discord.ui.View):
    def __init__(self, cliente_id):
        super().__init__(timeout=None)
        self.cliente_id = cliente_id

    @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.green)
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != DONO_ID:
            return await interaction.response.send_message("Só o dono pode aprovar!", ephemeral=True)
        cliente = await bot.fetch_user(self.cliente_id)
        try:
            await cliente.send("✅ **PEDIDO APROVADO!**\nTeu produto será entregue já.")
            await interaction.response.edit_message(content=f"✅ Aprovado! Cliente {cliente.mention} avisado.", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="✅ Aprovado! Mas não consegui mandar DM pro cliente.", embed=None, view=None)

    @discord.ui.button(label="❌ Reprovar", style=discord.ButtonStyle.red)
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != DONO_ID:
            return await interaction.response.send_message("Só o dono pode reprovar!", ephemeral=True)
        cliente = await bot.fetch_user(self.cliente_id)
        try:
            await cliente.send("❌ **PEDIDO REPROVADO**\nComprovante não bateu. Chama o dono.")
            await interaction.response.edit_message(content=f"❌ Reprovado! Cliente {cliente.mention} avisado.", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="❌ Reprovado!", embed=None, view=None)

# VIEW DO /LOJA
class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💸 Comprar Drip", style=discord.ButtonStyle.green, custom_id="comprar_drip")
    async def comprar_drip(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed
