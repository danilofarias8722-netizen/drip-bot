import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
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

CONTAS = {
    "lvl15": {"nome": "Conta Nível 15", "preco": "R$ 1,50", "key": "CONTA-LVL15"},
    "lvl20": {"nome": "Conta Nível 20", "preco": "R$ 1,50", "key": "CONTA-LVL20"}
}

pedidos_pendentes = {}

class AprovarView(View):
    def __init__(self, cliente_id, produto_key, tipo):
        super().__init__(timeout=None)
        self.cliente_id = cliente_id
        self.produto_key = produto_key
        self.tipo = tipo # "pack" ou "conta"

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green, emoji="✅", custom_id="aprovar_pedido")
    async def aprovar(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id!= DONO_ID:
            return await interaction.response.send_message("Só o dono pode aprovar.", ephemeral=True)

        cliente = await bot.fetch_user(self.cliente_id)

        if self.tipo == "pack":
            produto = PRODUTOS[self.produto_key]
            msg_entrega = "O admin vai te enviar o arquivo.png em breve."
        else:
            produto = CONTAS[self.produto_key]
            msg_entrega = "O admin vai te enviar os dados da conta em breve."

        embed_cliente = discord.Embed(
            title="Pedido Aprovado!",
            description=f"**Produto:** {produto['nome']}\n**Referência:** `{produto['key']}`\n\n{msg_entrega}",
            color=0x00FF00
        )
        embed_cliente.set_footer(text="Obrigado pela compra")

        try:
            await cliente.send(embed=embed_cliente)
            await interaction.response.edit_message(content=f"Aprovado por {interaction.user.mention} ✅\nCliente notificado na DM.", view=None)
            if self.cliente_id in pedidos_pendentes:
                del pedidos_pendentes[self.cliente_id]
        except:
            await interaction.response.edit_message(content=f"Aprovado por {interaction.user.mention} ✅\nMas não consegui enviar DM pro cliente.", view=None)

    @discord.ui.button(label="Reprovar", style=discord.ButtonStyle.red, emoji="❌", custom_id="reprovar_pedido")
    async def reprovar(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id!= DONO_ID:
            return await interaction.response.send_message("Só o dono pode reprovar.", ephemeral=True)

        cliente = await bot.fetch_user(self.cliente_id)

        embed_cliente = discord.Embed(
            title="Pedido Reprovado",
            description="Seu comprovante foi reprovado.\nEntre em contato com o admin para resolver.",
            color=0xFF0000
        )

        try:
            await cliente.send(embed=embed_cliente)
            await interaction.response.edit_message(content=f"Reprovado por {interaction.user.mention} ❌\nCliente notificado na DM.", view=None)
            if self.cliente_id in pedidos_pendentes:
                del pedidos_pendentes[self.cliente_id]
        except:
            await interaction.response.edit_message(content=f"Reprovado por {interaction.user.mention} ❌\nMas não consegui enviar DM pro cliente.", view=None)

class ProdutoView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for id_produto, info in PRODUTOS.items():
            self.add_item(Button(
                label=f"{info['nome'].replace('HG PACK CONFIG - ', '')} - {info['preco']}",
                custom_id=f"pack_{id_produto}",
                style=discord.ButtonStyle.blurple
            ))

class ContaView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for id_conta, info in CONTAS.items():
            self.add_item(Button(
                label=f"{info['nome']} - {info['preco']}",
                custom_id=f"conta_{id_conta}",
                style=discord.ButtonStyle.green
            ))

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}')
    bot.add_view(ProdutoView())
    bot.add_view(ContaView())
    print(f'IDs: Dono {DONO_ID} | Vendas {CANAL_VENDAS_ID} | Logs {CANAL_LOGS_ID}')

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data['component_type'] == 2:
        custom_id = interaction.data['custom_id']

        if custom_id.startswith("pack_"):
            id_produto = custom_id.replace("pack_", "")
            produto = PRODUTOS[id_produto]
            pedidos_pendentes[interaction.user.id] = {"tipo": "pack", "id": id_produto}

            embed_pix = discord.Embed(
                title="Pedido Gerado",
                description=f"**Produto:** {produto['nome'].replace('HG PACK CONFIG - ', '')}\n**Valor:** `{produto['preco']}`\n\n**Pague via PIX:**\n```{PIX_CHAVE}```\n\n**IMPORTANTE:**\n1. Faça o pagamento\n2. **Mande o comprovante na MINHA DM** 👈\n3. Aguarde o admin aprovar\n\n⚠️ Não mande o comprovante aqui no canal. Mande na DM do bot.",
                color=COR_EMBED
            )
            embed_pix.set_footer(text="Use o ID do produto como descrição no PIX")
            await interaction.response.send_message(embed=embed_pix, ephemeral=True)

        elif custom_id.startswith("conta_"):
            id_conta = custom_id.replace("conta_", "")
            conta = CONTAS[id_conta]
            pedidos_pendentes[interaction.user.id] = {"tipo": "conta", "id": id_conta}

            embed_pix = discord.Embed(
                title="Pedido de Conta Gerado",
                description=f"**Produto:** {conta['nome']}\n**Valor:** `{conta['preco']}`\n\n**Pague via PIX:**\n```{PIX_CHAVE}```\n\n**IMPORTANTE:**\n1. Faça o pagamento\n2. **Mande o comprovante na MINHA DM** 👈\n3. Aguarde o admin aprovar\n\n⚠️ Não mande o comprovante aqui no canal. Mande na DM do bot.",
                color=0x00FF00
            )
            embed_pix.set_footer(text="Use o ID da conta como descrição no PIX")
            await interaction.response.send_message(embed=embed_pix, ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        if message.author.id in pedidos_pendentes:
            pedido = pedidos_pendentes[message.author.id]

            if pedido["tipo"] == "pack":
                produto = PRODUTOS[pedido["id"]]
            else:
                produto = CONTAS[pedido["id"]]

            canal_logs = bot.get_channel(CANAL_LOGS_ID)
            if canal_logs:
                embed_log = discord.Embed(
                    title="Novo Comprovante Recebido",
                    description=f"**Cliente:** {message.author.mention} `{message.author.id}`\n**Produto:** {produto['nome']}\n**Valor:** {produto['preco']}\n**ID:** `{produto['key']}`",
                    color=0xFFFF00
                )
                embed_log.set_image(url=message.attachments[0].url)
                embed_log.set_footer(text="Clique em Aprovar ou Reprovar")

                await canal_logs.send(embed=embed_log, view=AprovarView(message.author.id, pedido["id"], pedido["tipo"]))
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
        title="🛒 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Arquivos de referência em.png\n✅ 100% seguro\n\nClique no botão do pack que deseja comprar:",
        color=COR_EMBED
    )
    embed.set_footer(text="Após pagar, envie o comprovante na DM do bot")

    await ctx.send(embed=embed, view=ProdutoView())
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def contas(ctx):
    if ctx.channel.id!= CANAL_VENDAS_ID:
        return await ctx.send("Use esse comando no canal de vendas!", delete_after=5)

    embed = discord.Embed(
        title="🎮 Contas Nível 15 e 20",
        description="**Preço:** `R$ 1,50` cada\n\n✅ Entrega rápida via DM\n✅ Conta full acesso\n✅ 100% segura\n\nClique no botão abaixo para comprar:",
        color=0x00FF00
    )
    embed.set_footer(text="Após pagar, envie o comprovante na DM do bot")

    await ctx.send(embed=embed, view=ContaView())
    await ctx.message.delete()

bot.run(os.getenv("DISCORD_TOKEN"))
