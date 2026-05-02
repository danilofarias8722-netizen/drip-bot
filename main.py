import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # precisa pra pegar DM
bot = commands.Bot(command_prefix="!", intents=intents)

DONO_ID = 1498844150202896446
CANAL_VENDAS_ID = 1498880071082049706
CANAL_LOGS_ID = 1500110296402886687
COR_EMBED = 0x2B2D31
PIX_CHAVE = "d3160985-198b-4ca4-a119-de573d45d2ee"

PRODUTOS = {
    "1d": {"nome": "HG PACK CONFIG - HUD 3 Dedos", "preco": "R$ 13,58", "key": "HGPACK-1D"},
    "3d": {"nome": "HG PACK CONFIG - HUD 4 Dedos", "preco": "R$ 27,67", "key": "HGPACK-3D"},
    "7d": {"nome": "HG PACK CONFIG - Sensi + HUD", "preco": "R$ 41,71", "key": "HGPACK-7D"},
    "30d": {"nome": "HG PACK CONFIG - Completo", "preco": "R$ 91,20", "key": "HGPACK-30D"}
}

# Guarda quem clicou em qual produto pra esperar o comprovante
pedidos_pendentes = {}

class AprovarView(View):
    def __init__(self, cliente_id, produto_key, msg_comprovante_id=None):
        super().__init__(timeout=None)
        self.cliente_id = cliente_id
        self.produto_key = produto_key
        self.msg_comprovante_id = msg_comprovante_id

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green, emoji="✅", custom_id="aprovar_pedido")
    async def aprovar(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id!= DONO_ID:
            return await interaction.response.send_message("Só o dono pode aprovar.", ephemeral=True)

        cliente = await bot.fetch_user(self.cliente_id)
        produto = PRODUTOS[self.produto_key]

        embed_cliente = discord.Embed(
            title="Pedido Aprovado!",
            description=f"**Produto:** {produto['nome']}\n**Sua referência:** `{produto['key']}`\n\nO admin vai te enviar o arquivo.png em breve.",
            color=0x00FF00
        )
        embed_cliente.set_footer(text="HG PACK CONFIG - Arquivo de imagem")

        try:
            await cliente.send(embed=embed_cliente)
            await interaction.response.edit_message(content=f"Aprovado por {interaction.user.mention} ✅\nCliente notificado na DM.", view=None)
            # Remove da lista de pendentes
            if self.cliente_id in pedidos_pendentes:
                del pedidos_pendentes[self.cliente_id]
        except:
            await interaction.response.edit_message(content=f"Aprovado por {interaction.user.mention} ✅\nMas não consegui enviar DM pro cliente.", view=None)

class ProdutoView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for id_produto, info in PRODUTOS.items():
            self.add_item(Button(
                label=f"{info['nome']} - {info['preco']}",
                custom_id=id_produto,
                style=discord.ButtonStyle.blurple
            ))

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}')
    bot.add_view(ProdutoView())
    print(f'IDs: Dono {DONO_ID} | Vendas {CANAL_VENDAS_ID} | Logs {CANAL_LOGS_ID}')

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data['component_type'] == 2:
        id_produto = interaction.data['custom_id']

        if id_produto in PRODUTOS and id_produto!= "aprovar_pedido":
            produto = PRODUTOS[id_produto]

            # Marca que esse cliente tem um pedido pendente
            pedidos_pendentes[interaction.user.id] = id_produto

            embed_pix = discord.Embed(
                title="Pedido Gerado - HG PACK CONFIG",
                description=f"**Produto:** {produto['nome']}\n**Valor:** `{produto['preco']}`\n\n**Pague via PIX:**\n```{PIX_CHAVE}```\n\n**IMPORTANTE:**\n1. Faça o pagamento\n2. **Mande o comprovante na MINHA DM** 👈\n3. Aguarde o admin aprovar\n\n⚠️ Não mande o comprovante aqui no canal. Mande na DM do bot.",
                color=COR_EMBED
            )
            embed_pix.set_footer(text="Use o ID do produto como descrição no PIX")

            await interaction.response.send_message(embed=embed_pix, ephemeral=True)

@bot.event
async def on_message(message):
    # Ignora msg do próprio bot
    if message.author.bot:
        return

    # Se for DM e tem anexo = comprovante
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        if message.author.id in pedidos_pendentes:
            id_produto = pedidos_pendentes[message.author.id]
            produto = PRODUTOS[id_produto]

            canal_logs = bot.get_channel(CANAL_LOGS_ID)
            if canal_logs:
                embed_log = discord.Embed(
                    title="Novo Comprovante Recebido",
                    description=f"**Cliente:** {message.author.mention} `{message.author.id}`\n**Produto:** {produto['nome']}\n**Valor:** {produto['preco']}\n**ID:** `{produto['key']}`",
                    color=0xFFFF00
                )
                embed_log.set_image(url=message.attachments[0].url)
                embed_log.set_footer(text="Clique em Aprovar para liberar o produto")

                await canal_logs.send(embed=embed_log, view=AprovarView(message.author.id, id_produto))
                await message.reply("Comprovante recebido! Aguarde a aprovação do admin. ✅")
        else:
            await message.reply("Não encontrei nenhum pedido pendente seu. Clique em um produto no canal de vendas primeiro.")

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def loja(ctx):
    if ctx.channel.id!= CANAL_VENDAS_ID:
        return await ctx.send("Use esse comando no canal de vendas!", delete_after=5)

    embed = discord.Embed(
        title="HG PACK CONFIG - Artes Digitais",
        description="**Produto 100% seguro**\nVocê recebe arquivos de imagem.png para usar como referência no seu jogo.\n\nSelecione abaixo o pack que deseja:",
        color=COR_EMBED
    )
    embed.set_footer(text="Após pagamento, envie o comprovante na DM do bot")

    await ctx.send(embed=embed, view=ProdutoView())
    await ctx.message.delete()

bot.run(os.getenv("DISCORD_TOKEN"))
