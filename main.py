import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

# SEU ID PRA RECEBER NOTIFICAÇÃO
DONO_ID = 1498859204696346755
PIX_KEY = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="1 Dia - R$15", style=discord.ButtonStyle.green, custom_id="drip_1")
    async def comprar_1_dia(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 1 Dia", 15)

    @discord.ui.button(label="3 Dias - R$25", style=discord.ButtonStyle.blurple, custom_id="drip_3")
    async def comprar_3_dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 3 Dias", 25)

    @discord.ui.button(label="7 Dias - R$45", style=discord.ButtonStyle.red, custom_id="drip_7")
    async def comprar_7_dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 7 Dias", 45)

async def iniciar_compra(interaction: discord.Interaction, produto: str, valor: int):
    try:
        await interaction.user.send(f"**Compra iniciada: {produto} - R${valor}**\n\n"
                                  f"1. Faz o Pix pra chave:\n`{PIX_KEY}`\n"
                                  f"2. Valor: **R${valor},00**\n"
                                  f"3. Me manda o comprovante AQUI NESSA DM\n\n"
                                  f"Assim que enviar, vou avisar o dono pra aprovar!")
        await interaction.response.send_message("Te chamei na DM! Confere lá 📩", ephemeral=True)
    except:
        await interaction.response.send_message("Não consegui te chamar na DM! Ativa suas DMs e tenta de novo.", ephemeral=True)

class AprovarView(discord.ui.View):
    def __init__(self, comprador: discord.User, produto: str):
        super().__init__(timeout=None)
        self.comprador = comprador
        self.produto = produto

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green)
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            await interaction.response.send_message("Só o dono pode aprovar.", ephemeral=True)
            return
        await interaction.response.send_modal(EnviarLinkModal(self.comprador, self.produto))
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reprovar", style=discord.ButtonStyle.red)
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            await interaction.response.send_message("Só o dono pode reprovar.", ephemeral=True)
            return
        await self.comprador.send(f"❌ Sua compra do **{self.produto}** foi reprovada. Chama o dono se tiver dúvidas.")
        await interaction.response.send_message(f"Compra reprovada e {self.comprador.mention} foi avisado.")
        await interaction.message.edit(view=None)

class EnviarLinkModal(discord.ui.Modal, title="Enviar Link do Produto"):
    def __init__(self, comprador: discord.User, produto: str):
        super().__init__()
        self.comprador = comprador
        self.produto = produto

    link = discord.ui.TextInput(label="Cole o link do Drip Cliente aqui", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await self.comprador.send(f"✅ **Compra aprovada!**\n\nProduto: **{self.produto}**\nSeu link: {self.link.value}\n\nObrigado!")
        await interaction.response.send_message(f"Link enviado pra {self.comprador.mention} com sucesso!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user} online e slash commands sincronizados!')

@bot.tree.command(name="loja", description="Abre a loja do Drip Cliente")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(title="🛒 Loja Drip Cliente", color=0x00ff00)
    embed.add_field(name="1 Dia", value="R$ 15", inline=True)
    embed.add_field(name="3 Dias", value="R$ 25", inline=True)
    embed.add_field(name="7 Dias", value="R$ 45", inline=True)
    embed.set_footer(text="Clique no botão pra comprar")
    await interaction.response.send_message(embed=embed, view=LojaView())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        dono = await bot.fetch_user(DONO_ID)
        embed = discord.Embed(title="💰 NOVO COMPROVANTE RECEBIDO", color=0xffff00)
        embed.add_field(name="Comprador", value=f"{message.author.mention} - `{message.author.id}`", inline=False)
        embed.set_image(url=message.attachments[0].url)
        embed.set_footer(text="Aprove ou reprove abaixo")
        await dono.send(embed=embed, view=AprovarView(message.author, "Drip Cliente"))
        await message.channel.send("Comprovante recebido! O dono já foi notificado e vai analisar. Aguarde ✅")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
