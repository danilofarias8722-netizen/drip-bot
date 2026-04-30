import discord
from discord import app_commands
from discord.ext import commands

# CONFIGURADO COM TEUS DADOS
GUILD_ID = 1498859204696346755 # <-- TROCA ISSO
DONO_ID = 1498844150202896446 
TOKEN =  # <-- TROCA ISSO
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
NOME_PIX = "Pablo Dalmo de Lima Carvalho"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Comprar 1 Dia - R$15", style=discord.ButtonStyle.green, custom_id="compra_1dia")
    async def comprar_1dia(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 1 Dia", "R$15,00")

    @discord.ui.button(label="Comprar 3 Dias - R$25", style=discord.ButtonStyle.blurple, custom_id="compra_3dias")
    async def comprar_3dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 3 Dias", "R$25,00")

    @discord.ui.button(label="Comprar 7 Dias - R$45", style=discord.ButtonStyle.blurple, custom_id="compra_7dias")
    async def comprar_7dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 7 Dias", "R$45,00")

async def iniciar_compra(interaction: discord.Interaction, produto: str, valor: str):
    try:
        await interaction.user.send(
            f"**Compra iniciada: {produto} - {valor}**\n\n"
            f"1. Faz o Pix de {valor} pra chave abaixo\n"
            f"2. Manda o comprovante AQUI na DM\n\n"
            f"**Chave Pix:** `{CHAVE_PIX}`\n"
            f"**Nome:** {NOME_PIX}"
        )
        await interaction.response.send_message("Te chamei na DM! Confere lá pra finalizar a compra.", ephemeral=True)
    except:
        await interaction.response.send_message("Não consegui te chamar na DM. Ativa as DMs do servidor e tenta de novo.", ephemeral=True)

class AprovarView(discord.ui.View):
    def __init__(self, user_id: int, produto: str):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.produto = produto

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green, custom_id="aprovar")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LinkModal(self.user_id, self.produto))

    @discord.ui.button(label="Reprovar", style=discord.ButtonStyle.red, custom_id="reprovar")
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = await bot.fetch_user(self.user_id)
        await user.send(f"**Pagamento reprovado**\n\nTeu comprovante do {self.produto} foi reprovado. Chama o suporte se achar que é erro.")
        await interaction.response.edit_message(content=f"❌ Reprovado. Avisei o <@{self.user_id}>", view=None)

class LinkModal(discord.ui.Modal, title="Enviar link do produto"):
    def __init__(self, user_id: int, produto: str):
        super().__init__()
        self.user_id = user_id
        self.produto = produto

    link = discord.ui.TextInput(label="Link pra enviar pro cliente", placeholder="https://...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user = await bot.fetch_user(self.user_id)
        await user.send(f"**Pagamento aprovado! ✅**\n\nProduto: {self.produto}\nAqui está teu acesso: {self.link.value}")
        await interaction.response.edit_message(content=f"✅ Aprovado! Link enviado pra <@{self.user_id}>", view=None)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    bot.add_view(LojaView())
    bot.add_view(AprovarView(0, ""))
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"Sincronizado {len(synced)} comandos no servidor")
    except Exception as e:
        print(e)

@bot.tree.command(name="loja", description="Ver os planos disponíveis")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(title="🛒 Loja Drip Cliente", color=0x00ff00)
    embed.add_field(name="1 Dia", value="R$15,00", inline=True)
    embed.add_field(name="3 Dias", value="R$25,00", inline=True)
    embed.add_field(name="7 Dias", value="R$45,00", inline=True)
    embed.set_footer(text="Clique no botão pra comprar")
    await interaction.response.send_message(embed=embed, view=LojaView())

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        dono = await bot.fetch_user(DONO_ID)
        embed = discord.Embed(title="📎 Produto informado", color=0xffa500)
        embed.add_field(name="Cliente", value=f"{message.author.mention}\nID: {message.author.id}", inline=False)
        embed.set_image(url=message.attachments[0].url)
        embed.set_footer(text="Use os botões para aprovar ou reprovar")

        await dono.send(embed=embed, view=AprovarView(message.author.id, "Drip Cliente"))
        await message.reply("**Comprovante recebido!** Vou analisar e já te aviso.")

    await bot.process_commands(message)

bot.run(TOKEN)
