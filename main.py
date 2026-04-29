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

    @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.green)
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            return await interaction.response.send_message("Só o dono pode aprovar!", ephemeral=True)
        cliente = await bot.fetch_user(self.cliente_id)
        try:
            await cliente.send("✅ **PEDIDO APROVADO!**\nTeu produto será entregue em instantes.")
            await interaction.response.edit_message(content="✅ Aprovado! Cliente avisado.", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="✅ Aprovado! Mas DM do cliente tá fechada.", embed=None, view=None)

    @discord.ui.button(label="❌ Reprovar", style=discord.ButtonStyle.red)
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            return await interaction.response.send_message("Só o dono pode reprovar!", ephemeral=True)
        cliente = await bot.fetch_user(self.cliente_id)
        try:
            await cliente.send("❌ **PEDIDO REPROVADO**\nComprovante inválido. Chama o dono.")
            await interaction.response.edit_message(content="❌ Reprovado! Cliente avisado.", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="❌ Reprovado!", embed=None, view=None)

class DripView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💸 Comprar Drip", style=discord.ButtonStyle.green)
    async def comprar_drip(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_dm = discord.Embed(
                title="💎 Pagamento Drip Cliente",
                description=f"**Chave PIX:** `{CHAVE_PIX}`\n\n**Valores:**\n1 Dia: R$ 15,00\n3 Dias: R$ 25,00\n7 Dias: R$ 45,00\n\n**Envie o comprovante AQUI nessa DM após pagar.**\n**Escreve qual plano tu pagou: 1, 3 ou 7 dias.**",
                color=0x9b59b6
            )
            await interaction.user.send(embed=embed_dm)
            await interaction.response.send_message("Te chamei na DM pra fazer o PIX ✅", ephemeral=True)
        except:
            await interaction.response.send_message("Ativa tuas DMs pra eu conseguir te chamar!", ephemeral=True)
