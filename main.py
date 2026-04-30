import discord
from discord import app_commands
import os

GUILD_ID = 1498859204696346755
DONO_ID = 1498844150202896446
PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
TOKEN = os.getenv("")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Dicionário pra guardar quem comprou o que
pedidos = {}

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Drip Cliente 1 Dia - R$15", style=discord.ButtonStyle.blurple, custom_id="compra_1dia")
    async def um_dia(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 1 Dia", "R$15,00")

    @discord.ui.button(label="Drip Cliente 3 Dias - R$25", style=discord.ButtonStyle.blurple, custom_id="compra_3dias")
    async def tres_dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 3 Dias", "R$25,00")

    @discord.ui.button(label="Drip Cliente 7 Dias - R$45", style=discord.ButtonStyle.blurple, custom_id="compra_7dias")
    async def sete_dias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await iniciar_compra(interaction, "Drip Cliente 7 Dias", "R$45,00")

async def iniciar_compra(interaction: discord.Interaction, produto: str, valor: str):
    embed = discord.Embed(
        title="💎 Finalizar Compra",
        description=f"**Produto:** {produto} - **{valor}**\n\n"
                   f"1️⃣ Faz o Pix pra chave abaixo\n"
                   f"2️⃣ **Me envia o comprovante AQUI na DM**\n"
                   f"3️⃣ Aguarda eu aprovar\n\n"
                   f"**Chave Pix:**\n```{PIX}```",
        color=0x00ff00
    )

    try:
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("Te chamei na DM! Confere lá pra finalizar a compra.", ephemeral=True)
        pedidos[interaction.user.id] = {"produto": produto, "valor": valor}
    except:
        await interaction.response.send_message("Não consegui te chamar na DM. Ativa as DMs do servidor e tenta de novo.", ephemeral=True)

class AprovarView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.green, custom_id="aprovar")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            await interaction.response.send_message("Só o dono pode aprovar.", ephemeral=True)
            return

        modal = LinkModal(self.user_id)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="❌ Reprovar", style=discord.ButtonStyle.red, custom_id="reprovar")
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= DONO_ID:
            await interaction.response.send_message("Só o dono pode reprovar.", ephemeral=True)
            return

        user = await client.fetch_user(self.user_id)
        await user.send("❌ **Pagamento reprovado.** Chama o suporte se achar que é um erro.")
        await interaction.response.edit_message(content="**Pagamento reprovado.**", view=None)

class LinkModal(discord.ui.Modal, title="Enviar Link do Produto"):
    link = discord.ui.TextInput(label="Cole o link aqui", style=discord.TextStyle.short)

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        user = await client.fetch_user(self.user_id)
        produto = pedidos.get(self.user_id, {}).get("produto", "Produto")

        await user.send(f"✅ **Pagamento aprovado!**\n\n**Produto:** {produto}\n**Seu link:** {self.link.value}")
        await interaction.response.edit_message(content=f"**Aprovado!** Link enviado pra {user.mention}", view=None)
        if self.user_id in pedidos:
            del pedidos[self.user_id]

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f'Bot online como {client.user}')

@tree.command(name="loja", description="Abre a loja de Drip Cliente", guild=discord.Object(id=GUILD_ID))
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 Loja Drip Cliente",
        description="**Escolha seu plano abaixo:**\n\n"
                   "💎 **Drip Cliente 1 Dia** - R$15,00\n"
                   "💎 **Drip Cliente 3 Dias** - R$25,00\n"
                   "💎 **Drip Cliente 7 Dias** - R$45,00\n\n"
                   "Clique no botão pra comprar!",
        color=0x5865F2
    )
    await interaction.response.send_message(embed=embed, view=LojaView())

@client.event
async def on_message(message):
    # Ignora msgs do próprio bot
    if message.author == client.user:
        return

    # Se for DM e tiver anexo = comprovante
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        if message.author.id in pedidos:
            dono = await client.fetch_user(DONO_ID)
            embed = discord.Embed(
                title="📸 Novo Comprovante Recebido",
                description=f"**Cliente:** {message.author.mention} `{message.author.id}`\n"
                           f"**Produto:** {pedidos[message.author.id]['produto']}\n"
                           f"**Valor:** {pedidos[message.author.id]['valor']}",
                color=0xffa500
            )
            embed.set_image(url=message.attachments[0].url)

            view = AprovarView(message.author.id)
            await dono.send(embed=embed, view=view)
            await message.reply("✅ Comprovante recebido! Aguarde a aprovação.")

    await client.process_commands(message)

client.run(TOKEN)
