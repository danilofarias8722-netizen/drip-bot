import discord
from discord import app_commands
from discord.ui import View, Button
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# TROCA PELO TEU ID DO DISCORD
DONO_ID = 123456789012345678

class ComprarView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Comprar Drip Cliente", style=discord.ButtonStyle.green, emoji="💸")
    async def comprar(self, interaction: discord.Interaction, button: Button):
        try:
            embed_dm = discord.Embed(title="💎 PAGAMENTO PIX - DRIP CLIENTE", color=0x00ff00)
            embed_dm.add_field(name="Chave PIX Copia e Cola", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
            embed_dm.add_field(name="1 Dia", value="R$ 15,00", inline=True)
            embed_dm.add_field(name="3 Dias", value="R$ 25,00", inline=True)
            embed_dm.add_field(name="7 Dias", value="R$ 45,00", inline=True)
            embed_dm.set_footer(text="Depois de pagar, manda o print do comprovante aqui na DM")
            await interaction.user.send(embed=embed_dm)
            await interaction.response.send_message("Te chamei na DM! Confere lá 📩", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Libera tua DM irmão", ephemeral=True)

@bot.tree.command(name="loja", description="Veja os planos da Drip Cliente")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 DRIP CLIENTE - PLANOS",
        description="Escolhe o melhor plano pra ti e clica em comprar:",
        color=0x9b59b6
    )
    embed.add_field(name="1 Dia", value="R$ 15,00", inline=True)
    embed.add_field(name="3 Dias", value="R$ 25,00", inline=True)
    embed.add_field(name="7 Dias", value="R$ 45,00", inline=True)
    embed.set_footer(text="Pagamento via PIX. Liberação após confirmação")
    view = ComprarView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        dono = await bot.fetch_user(DONO_ID)
        embed = discord.Embed(title="🚨 NOVO COMPROVANTE", color=0xe74c3c)
        embed.add_field(name="Cliente", value=f"{message.author.mention} `{message.author.id}`", inline=False)
        embed.set_image(url=message.attachments[0].url)
        await dono.send(embed=embed)
        await message.channel.send("Comprovante recebido! O dono já foi avisado ✅")
    await bot.process_commands(message)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizou {len(synced)} comando(s)")
    except Exception as e:
        print(e)
    print(f'Bot online: {bot.user}')

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
