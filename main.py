import discord
from discord.ext import commands
import asyncio
import os
import qrcode
from io import BytesIO
from pixqrcodegen import Payload

# CONFIGURAÇÃO
ID_CATEGORIA_CARRINHO = 1504149916249886833
ID_CARGO_ATENDENTE = 1500251010461863977
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
NOME_RECEBEDOR = "RAFAEL"
CIDADE = "MACAPA"

# CUPONS
CUPONS = {
    "DNZX10": 10,
    "BEMVINDO": 15,
    "BLACK50": 50
}

CARRINHOS = {}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== ATUALIZAR EMBED DO CARRINHO =====
async def atualizar_carrinho_embed(canal: discord.TextChannel):
    if canal.id not in CARRINHOS:
        return None, 0

    dados = CARRINHOS[canal.id]
    produtos = dados["produtos"]
    cupom_usado = dados.get("cupom")

    if not produtos:
        embed = discord.Embed(
            title="🛒 Carrinho Vazio",
            description="Use `/packs` ou `/contas` pra adicionar produtos.",
            color=discord.Color.orange()
        )
        return embed, 0

    lista_produtos = ""
    subtotal = 0
    total_itens = 0

    for nome, info in produtos.items():
        qtd = info["qtd"]
        valor_unit = info["valor"]
        valor_total = valor_unit * qtd
        subtotal += valor_total
        total_itens += qtd
        lista_produtos += f"`{qtd}x` {nome} | R$ {valor_total:.2f}\n"

    desconto = 0
    if cupom_usado:
        desconto = subtotal * (CUPONS[cupom_usado] / 100)

    total_final = subtotal - desconto

    descricao = f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades**, **aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n"
    descricao += f"**Produtos no Carrinho ({total_itens}x)**\n{lista_produtos}\n"
    descricao += f"**Subtotal**\nR$ {subtotal:.2f}\n"

    if cupom_usado:
        descricao += f"**Cupom {cupom_usado}**\n- R$ {desconto:.2f}\n"

    descricao += f"**Valor à vista**\nR$ {total_final:.2f}"

    embed = discord.Embed(
        title="Detalhes da sua compra",
        description=descricao,
        color=discord.Color.red()
    )
    embed.set_footer(text=f"DNZX STORE #{canal.id}")

    return embed, total_final

# ===== ADICIONAR AO CARRINHO =====
async def adicionar_ao_carrinho(interaction: discord.Interaction, produto: str, valor: str):
    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    user = interaction.user
    valor_num = float(valor.replace("R$ ", "").replace(",", "."))

    canal_carrinho = None
    for channel in guild.text_channels:
        if channel.name == f"carrinho-{user.name}".lower():
            canal_carrinho = channel
            break

    if not canal_carrinho:
        categoria = guild.get_channel(ID_CATEGORIA_CARRINHO)
        cargo = guild.get_role(ID_CARGO_ATENDENTE)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
            cargo: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        nome_canal = f"carrinho-{user.name}".lower()
        canal_carrinho = await guild.create_text_channel(name=nome_canal, category=categoria, overwrites=overwrites)
        CARRINHOS[canal_carrinho.id] = {"produtos": {}, "cupom": None}
        await canal_carrinho.send(content=f"{user.mention} {cargo.mention}")

    if canal_carrinho.id not in CARRINHOS:
        CARRINHOS[canal_carrinho.id] = {"produtos": {}, "cupom": None}

    if produto in CARRINHOS[canal_carrinho.id]["produtos"]:
        CARRINHOS[canal_carrinho.id]["produtos"][produto]["qtd"] += 1
    else:
        CARRINHOS[canal_carrinho.id]["produtos"][produto] = {"qtd": 1, "valor": valor_num}

    embed, total = await atualizar_carrinho_embed(canal_carrinho)

    async for msg in canal_carrinho.history(limit=10):
        if msg.author == bot.user and msg.embeds and "Detalhes da sua compra" in msg.embeds[0].title:
            await msg.edit(embed=embed, view=CarrinhoView())
            return await interaction.followup.send(f"Produto adicionado! {canal_carrinho.mention}", ephemeral=True)

    await canal_carrinho.send(embed=embed, view=CarrinhoView())
    await interaction.followup.send(f"Carrinho criado! {canal_carrinho.mention}", ephemeral=True)

# ===== VIEWS DE PRODUTOS =====
class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple)
    async def hud3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "HUD 3 Dedos", "R$ 13,58")

    @discord.ui.button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple)
    async def hud4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "HUD 4 Dedos", "R$ 27,67")

    @discord.ui.button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple)
    async def sensi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "Sensi + HUD", "R$ 41,71")

    @discord.ui.button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple)
    async def completo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "Completo", "R$ 91,20")

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Conta Nível 15 - R$ 1,50", style=discord.ButtonStyle.green)
    async def conta15(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "Conta Nível 15", "R$ 1,50")

    @discord.ui.button(label="Conta Nível 20 - R$ 1,50", style=discord.ButtonStyle.green)
    async def conta20(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adicionar_ao_carrinho(interaction, "Conta Nível 20", "R$ 1,50")

# ===== VIEW DO CARRINHO =====
class CarrinhoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="✅")
    async def pagamento(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.channel.id not in CARRINHOS or not CARRINHOS[interaction.channel.id]["produtos"]:
            return await interaction.response.send_message("Carrinho vazio!", ephemeral=True)

        embed, total = await atualizar_carrinho_embed(interaction.channel)
        produtos = CARRINHOS[interaction.channel.id]["produtos"]
        lista_produtos = ""
        total_itens = 0

        for nome, info in produtos.items():
            qtd = info["qtd"]
            valor_total = info["valor"] * qtd
            total_itens += qtd
            lista_produtos += f"`{qtd}x` {nome} | R$ {valor_total:.2f}\n"

        embed_pagamento = discord.Embed(
            title="Escolha a sua forma de pagamento",
            description=f"Dê uma última olhada na sua compra e escolha como deseja pagar.\n\n**Produtos no Carrinho ({total_itens}x)**\n{lista_produtos}\n**Valor à vista**\nR$ {total:.2f}",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(embed=embed_pagamento, view=PagamentoView())

    @discord.ui.button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.channel.id not in CARRINHOS or not CARRINHOS[interaction.channel.id]["produtos"]:
            return await interaction.response.send_message("Carrinho vazio!", ephemeral=True)
        await interaction.response.send_modal(EditarQuantidadeModal())

    @discord.ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
    async def cupom(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CupomModal())

    @discord.ui.button(label="Cancelar Carrinho", style=discord.ButtonStyle.red, emoji="❌")
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelando carrinho...", ephemeral=True)
        if interaction.channel.id in CARRINHOS:
            del CARRINHOS[interaction.channel.id]
        await asyncio.sleep(2)
        await interaction.channel.delete()

# ===== VIEW DE PAGAMENTO =====
class PagamentoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pagar com Pix", style=discord.ButtonStyle.green, emoji="💠")
    async def pagar_pix(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if interaction.channel.id not in CARRINHOS:
            return await interaction.followup.send("Erro: carrinho não encontrado.", ephemeral=True)

        embed, total = await atualizar_carrinho_embed(interaction.channel)

        # Gera código Pix com valor
        payload = Payload(
            nome=NOME_RECEBEDOR,
            chavepix=CHAVE_PIX,
            valor=f"{total:.2f}",
            cidade=CIDADE,
            txtId=f"DNZX{interaction.channel.id}"
        )

        codigo_pix = payload.gerarPayload()

        # Gera QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(codigo_pix)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        arquivo_qr = discord.File(buffer, filename="pix_qr.png")

        embed_pix = discord.Embed(
            title="Pagamento via PIX criado",
            description=f"**Valor: R$ {total:.2f}**\n\n**Código copia e cola**\n```{codigo_pix}```\n\n⚠️ **Após pagar, envie o comprovante aqui**\nUm atendente vai confirmar e liberar seu produto.",
            color=discord.Color.red()
        )
        embed_pix.set_image(url="attachment://pix_qr.png")
        embed_pix.set_footer(text="DNZX STORE")

        view = discord.ui.View(timeout=None)
        btn_copiar = discord.ui.Button(label="Código copia e cola", style=discord.ButtonStyle.gray, emoji="📋")
        btn_voltar = discord.ui.Button(label="Voltar", style=discord.ButtonStyle.gray, emoji="⬅️")

        async def copiar_callback(interaction_btn: discord.Interaction):
            await interaction_btn.response.send_message(f"```{codigo_pix}```", ephemeral=True)

        async def voltar_callback(interaction_btn: discord.Interaction):
            embed_carrinho, _ = await atualizar_carrinho_embed(interaction_btn.channel)
            await interaction_btn.response.edit_message(embed=embed_carrinho, view=CarrinhoView())

        btn_copiar.callback = copiar_callback
        btn_voltar.callback = voltar_callback
        view.add_item(btn_copiar)
        view.add_item(btn_voltar)

        await interaction.followup.send(embed=embed_pix, file=arquivo_qr, view=view)

    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="⬅️")
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, _ = await atualizar_carrinho_embed(interaction.channel)
        await interaction.response.edit_message(embed=embed, view=CarrinhoView())

# ===== MODAIS =====
class CupomModal(discord.ui.Modal, title="Aplicar Cupom"):
    codigo = discord.ui.TextInput(label="Código do Cupom", placeholder="Ex: DNZX10", max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        codigo_up = self.codigo.value.upper()

        if codigo_up not in CUPONS:
            return await interaction.response.send_message(f"❌ Cupom `{codigo_up}` inválido.", ephemeral=True)

        if CARRINHOS[interaction.channel.id].get("cupom"):
            return await interaction.response.send_message("❌ Você já usou um cupom.", ephemeral=True)

        CARRINHOS[interaction.channel.id]["cupom"] = codigo_up
        embed, total = await atualizar_carrinho_embed(interaction.channel)

        async for msg in interaction.channel.history(limit=10):
            if msg.author == interaction.client.user and msg.embeds:
                await msg.edit(embed=embed, view=CarrinhoView())
                break

        await interaction.response.send_message(f"✅ Cupom `{codigo_up}` aplicado! {CUPONS[codigo_up]}% de desconto.", ephemeral=True)

class EditarQuantidadeModal(discord.ui.Modal, title="Editar Quantidade"):
    produto = discord.ui.TextInput(label="Nome do Produto", placeholder="Ex: HUD 3 Dedos")
    quantidade = discord.ui.TextInput(label="Nova Quantidade", placeholder="0 pra remover", max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        nome_produto = self.produto.value
        try:
            qtd_nova = int(self.quantidade.value)
        except:
            return await interaction.response.send_message("❌ Quantidade inválida.", ephemeral=True)

        if nome_produto not in CARRINHOS[interaction.channel.id]["produtos"]:
            return await interaction.response.send_message(f"❌ Produto não está no carrinho.", ephemeral=True)

        if qtd_nova <= 0:
            del CARRINHOS[interaction.channel.id]["produtos"][nome_produto]
        else:
            CARRINHOS[interaction.channel.id]["produtos"][nome_produto]["qtd"] = qtd_nova

        embed, total = await atualizar_carrinho_embed(interaction.channel)

        async for msg in interaction.channel.history(limit=10):
            if msg.author == interaction.client.user and msg.embeds:
                await msg.edit(embed=embed, view=CarrinhoView())
                break

        await interaction.response.send_message("✅ Carrinho atualizado!", ephemeral=True)@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos")
    except Exception as e:
        print(e)

@bot.tree.command(name="packs", description="Ver packs disponíveis")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 Packs Disponíveis",
        description="Clique no botão do pack que deseja adicionar ao carrinho:",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, view=PacksView())

@bot.tree.command(name="contas", description="Ver contas disponíveis")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👤 Contas Disponíveis",
        description="Clique no botão da conta que deseja adicionar ao carrinho:",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=ContasView())

@bot.tree.command(name="cupons", description="Ver cupons ativos")
async def cupons(interaction: discord.Interaction):
    lista = "\n".join([f"`{codigo}` - {desconto}% OFF" for codigo, desconto in CUPONS.items()])
    embed = discord.Embed(
        title="🎟️ Cupons Ativos",
        description=lista,
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
