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

class LojaView(discord.ui.View):
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
        except discord.Forbidden:
            await interaction.response.send_message("Ativa tuas DMs pra eu conseguir te chamar!", ephemeral=True)

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔥 Comprar Conta", style=discord.ButtonStyle.blurple)
    async def comprar_conta(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_dm = discord.Embed(
                title="🎮 Pagamento Conta Nv 15/20",
                description=f"**Chave PIX:** `{CHAVE_PIX}`\n\n**Valor:** R$ 1,50\n\n**Envie o comprovante AQUI nessa DM após pagar.**\n**Escreve 'Conta Nv 15/20' na mensagem.**",
                color=0x3498db
            )
            await interaction.user.send(embed=embed_dm)
            await interaction.response.send_message("Te chamei na DM pra fazer o PIX ✅", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Ativa tuas DMs pra eu conseguir te chamar!", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(LojaView())
    bot.add_view(ContasView())
    try:
        synced = await bot.tree.sync()
        print(f"Bot online: {bot.user} | Comandos: {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="loja", description="Mostra os planos do Drip Cliente")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(title="💎 DRIP CLIENTE", color=0x9b59b6)
    embed.add_field(name="📅 Drip Cliente 1 Dia", value="**R$ 15,00**", inline=True)
    embed.add_field(name="📅 Drip Cliente 3 Dias", value="**R$ 25,00**", inline=True)
    embed.add_field(name="📅
