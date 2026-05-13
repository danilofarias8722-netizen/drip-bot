import discord
from discord.ext import commands
from discord import app_commands, File
import qrcode
import io
import os  # <-- ADICIONA ESSA LINHA

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# -------- CONFIGURAÇÕES DA SUA LOJA --------
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
NOME_RECEBEDOR = "Rafael"
CIDADE = "MACAPA"
CANAL_LOG = 1504149916249886833
NOME_LOJA = "DNZX STORE"
# ... resto do código igual

# -------- SISTEMA DE CARRINHO --------
carrinhos = {} # {user_id: {"itens": [], "total": 0, "cupom": None}}

def gerar_payload_pix(chave, nome, cidade, valor, txid="***"):
    valor_formatado = f"{valor:.2f}"
    payload = [
        f"000201",
        f"26{len('0014br.gov.bcb.pix01' + str(len(chave)).zfill(2) + chave):02}0014br.gov.bcb.pix01{len(chave):02}{chave}",
        f"52040000", f"5303986", f"54{len(valor_formatado):02}{valor_formatado}",
        f"5802BR", f"59{len(nome):02}{nome}", f"60{len(cidade):02}{cidade}",
        f"62{len('05' + str(len(txid)).zfill(2) + txid):02}05{len(txid):02}{txid}"
    ]
    payload_str = ''.join(payload) + '6304'
    crc = crc16(payload_str)
    return payload_str + crc

def crc16(payload):
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000: crc = (crc << 1) ^ 0x1021
            else: crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')

async def add_carrinho(interaction: discord.Interaction, produto: str, preco: float):
    user_id = interaction.user.id
    if user_id not in carrinhos:
        carrinhos[user_id] = {"itens": [], "total": 0, "cupom": None}

    for item in carrinhos[user_id]["itens"]:
        if item["nome"] == produto:
            item["qtd"] += 1
            carrinhos[user_id]["total"] += preco
            break
    else:
        carrinhos[user_id]["itens"].append({"nome": produto, "preco": preco, "qtd": 1})
        carrinhos[user_id]["total"] += preco

    class VerCarrinhoView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Ver Carrinho", style=discord.ButtonStyle.gray, emoji="📦")
        async def ver_carrinho(self, interaction: discord.Interaction, button: discord.ui.Button):
            await mostrar_carrinho(interaction)

    await interaction.response.send_message("✅ Seu carrinho foi criado com êxito.", view=VerCarrinhoView(), ephemeral=True)

# -------- COMANDO /HG --------
class HgSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1 DIA", description="Valor: R$ 10,00", emoji="🛒", value="hg_1d"),
            discord.SelectOption(label="7 DIAS", description="Valor: R$ 30,00", emoji="🛒", value="hg_7d"),
            discord.SelectOption(label="10 DIAS", description="Valor: R$ 35,00", emoji="🛒", value="hg_10d"),
            discord.SelectOption(label="30 DIAS", description="Valor: R$ 98,00", emoji="🛒", value="hg_30d"),
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"hg_1d": 10.00, "hg_7d": 30.00, "hg_10d": 35.00, "hg_30d": 98.00}
        nomes = {"hg_1d": "HG CHEATS 1 DIA", "hg_7d": "HG CHEATS 7 DIAS", "hg_10d": "HG CHEATS 10 DIAS", "hg_30d": "HG CHEATS 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class HgView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HgSelect())

@bot.tree.command(name="hg", description="Comprar HG Cheats")
async def hg(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ HG CHEATS",
        description="**Compatível com todas as versões até Android 16**\n**Tutorial completo de instalação incluso**\n**Mod APK exclusivo**\n\n**FUNCIONALIDADES DO MENU**\n• Aimbot totalmente configurável\n• Suporte apenas para Free Fire normal\n• Configuração de Aimbot para Cabeça, Pescoço e Peito\n\n**VOCÊ RECEBE**\n• Chave de Licença (Key)\n• Tutorial / Instruções Detalhada",
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=HgView())

# -------- COMANDO /PROXY --------
class ProxySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="7 DIAS", description="Valor: R$ 30,00", emoji="🛒", value="proxy_7d"),
            discord.SelectOption(label="30 DIAS", description="Valor: R$ 50,00", emoji="🛒", value="proxy_30d"),
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"proxy_7d": 30.00, "proxy_30d": 50.00}
        nomes = {"proxy_7d": "PROXY IOS 7 DIAS", "proxy_30d": "PROXY IOS 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class ProxyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProxySelect())

@bot.tree.command(name="proxy", description="Comprar Proxy iOS")
async def proxy(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📱 PROXY IOS",
        description="**Compatível com iPhone**\n**Tutorial completo de instalação incluso**\n**Arquivo Mobile Config**\n\n**FUNCIONALIDADES DO MENU**\n• Aimbot totalmente configurável\n• Suporte apenas para Free Fire normal\n• Configuração de Aimbot para Cabeça, Pescoço e Peito\n\n**VOCÊ RECEBE**\n• Arquivo Mobile Config\n• Tutorial / Instruções Detalhada",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=ProxyView())

# -------- COMANDO /PREMIUM --------
class PremiumSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PAINEL MONITE 7 DIAS", description="Valor: R$ 35,00", emoji="🛒", value="painel_7d"),
            discord.SelectOption(label="PAINEL MONITE 30 DIAS", description="Valor: R$ 80,00", emoji="🛒", value="painel_30d"),
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"painel_7d": 35.00, "painel_30d": 80.00}
        nomes = {"painel_7d": "PAINEL MONITE 7 DIAS", "painel_30d": "PAINEL MONITE 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PremiumSelect())

@bot.tree.command(name="premium", description="Comprar Painel Monite")
async def premium(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💎 PAINEL MONITE",
        description="**Acesso exclusivo ao Painel**\n**Suporte incluso**\n**Atualizações grátis**\n\n**FUNCIONALIDADES**\n• Visualização de dados em tempo real\n• Histórico completo\n• Interface intuitiva\n\n**VOCÊ RECEBE**\n• Acesso ao Painel\n• Suporte via Discord",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=PremiumView())# -------- MODALS DO CARRINHO --------
class CupomModal(discord.ui.Modal, title="Aplicar Cupom"):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
    cupom = discord.ui.TextInput(label="Digite o cupom", placeholder="Ex: 2026", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        if self.cupom.value == "2026":
            carrinhos[self.user_id]["cupom"] = "2026"
            await interaction.response.send_message("✅ Cupom 10% OFF aplicado!", ephemeral=True)
            await mostrar_carrinho(interaction)
        else:
            await interaction.response.send_message("❌ Cupom inválido.", ephemeral=True)

class QtdModal(discord.ui.Modal, title="Editar Quantidade"):
    def __init__(self, user_id, produto):
        super().__init__()
        self.user_id = user_id
        self.produto = produto
        self.qtd = discord.ui.TextInput(label=f"Nova quantidade para {produto}", placeholder="Digite um número", required=True)
        self.add_item(self.qtd)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            nova_qtd = int(self.qtd.value)
            if nova_qtd <= 0:
                carrinhos[self.user_id]["itens"] = [i for i in carrinhos[self.user_id]["itens"] if i["nome"]!= self.produto]
            else:
                for item in carrinhos[self.user_id]["itens"]:
                    if item["nome"] == self.produto:
                        item["qtd"] = nova_qtd
                        break
            total = 0
            for item in carrinhos[self.user_id]["itens"]:
                total += item["preco"] * item["qtd"]
            carrinhos[self.user_id]["total"] = total
            await interaction.response.send_message("✅ Quantidade atualizada!", ephemeral=True)
            await mostrar_carrinho(interaction)
        except:
            await interaction.response.send_message("❌ Digite apenas números.", ephemeral=True)

# -------- TELA DO CARRINHO --------
async def mostrar_carrinho(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in carrinhos or not carrinhos[user_id]["itens"]:
        return await interaction.response.send_message("Seu carrinho está vazio.", ephemeral=True)

    carrinho = carrinhos[user_id]
    descricao = "Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades, aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n"
    descricao += "**Produtos no Carrinho**\n"
    for item in carrinho["itens"]:
        descricao += f"{item['qtd']}x {item['nome']} | R$ {item['preco']:.2f}\n"

    total = carrinho["total"]
    descricao += f"\n**Valor à vista**\nR$ {total:.2f}"
    if carrinho["cupom"]:
        desconto = total * 0.10
        total_com_desconto = total - desconto
        descricao += f"\n\n**Cupom 10% OFF:** -R$ {desconto:.2f}"
        descricao += f"\n**Total com desconto:** R$ {total_com_desconto:.2f}"

    embed = discord.Embed(title="Detalhes da sua compra", description=descricao, color=discord.Color.red())
    embed.set_footer(text=f"{NOME_LOJA} #5K")

    class CarrinhoView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="✅")
        async def pagamento(self, interaction: discord.Interaction, button: discord.ui.Button):
            await tela_pagamento(interaction, interaction.user.id)
        @discord.ui.button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="✏️")
        async def editar_qtd(self, interaction: discord.Interaction, button: discord.ui.Button):
            if len(carrinho["itens"]) == 1:
                await interaction.response.send_modal(QtdModal(user_id, carrinho["itens"][0]["nome"]))
            else:
                options = [discord.SelectOption(label=i["nome"], value=i["nome"]) for i in carrinho["itens"]]
                select = discord.ui.Select(placeholder="Escolha o produto", options=options)
                async def callback(inter: discord.Interaction):
                    await inter.response.send_modal(QtdModal(user_id, select.values[0]))
                select.callback = callback
                view = discord.ui.View()
                view.add_item(select)
                await interaction.response.send_message("Selecione o produto:", view=view, ephemeral=True)
        @discord.ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
        async def usar_cupom(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(CupomModal(user_id))

    await interaction.response.send_message(embed=embed, view=CarrinhoView(), ephemeral=True)

# -------- TELA DE PAGAMENTO --------
class PagamentoView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
    @discord.ui.button(label="Pagar com Pix", style=discord.ButtonStyle.gray, emoji="💠")
    async def pix(self, interaction: discord.Interaction, button: discord.ui.Button):
        await gerar_pix(interaction, self.user_id)
    @discord.ui.button(label="Pagar com Cartão", style=discord.ButtonStyle.gray, emoji="💳", disabled=True)
    async def cartao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Método indisponível no momento.", ephemeral=True)
    @discord.ui.button(label="Pagar com Saldo", style=discord.ButtonStyle.gray, emoji="💰", disabled=True)
    async def saldo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Método indisponível no momento.", ephemeral=True)
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="↩️")
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await mostrar_carrinho(interaction)

async def tela_pagamento(interaction: discord.Interaction, user_id: int):
    if user_id not in carrinhos or not carrinhos[user_id]["itens"]:
        return await interaction.response.send_message("Seu carrinho está vazio.", ephemeral=True)
    carrinho = carrinhos[user_id]
    descricao = "Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática e rápida.\n\n**Produtos no Carrinho**\n"
    for item in carrinho["itens"]:
        descricao += f"{item['qtd']}x {item['nome']} | R$ {item['preco']:.2f}\n"
    total = carrinho["total"]
    if carrinho["cupom"]:
        desconto = total * 0.10
        total -= desconto
        descricao += f"\n**Cupom 10% OFF:** -R$ {desconto:.2f}"
    descricao += f"\n**Valor à vista**\nR$ {total:.2f}"
    embed = discord.Embed(title="Escolha a sua forma de pagamento", description=descricao, color=discord.Color.dark_red())
    embed.set_footer(text=f"{NOME_LOJA} #5K")
    await interaction.response.send_message(embed=embed, view=PagamentoView(user_id), ephemeral=True)# -------- GERAR PIX COMPLETO --------
async def gerar_pix(interaction: discord.Interaction, user_id: int):
    carrinho = carrinhos[user_id]
    total = carrinho["total"]
    if carrinho["cupom"]: total = total * 0.90

    payload = gerar_payload_pix(CHAVE_PIX, NOME_RECEBEDOR, CIDADE, total)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    embed = discord.Embed(
        title="Pagamento via PIX criado",
        description=f"**Código copia e cola**\n```{payload}```\n\n**Valor:** R$ {total:.2f}\n**Recebedor:** {NOME_RECEBEDOR}\nApós pagar, clique em Já paguei.",
        color=discord.Color.blue()
    )
    embed.set_image(url="attachment://qrcode.png")
    embed.set_footer(text=f"© {NOME_LOJA} - 2025")

    class PixView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=600)
        @discord.ui.button(label="Código copia e cola", style=discord.ButtonStyle.gray, emoji="📋")
        async def copiar(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f"```{payload}```", ephemeral=True)
        @discord.ui.button(label="Já paguei", style=discord.ButtonStyle.green, emoji="✅")
        async def ja_paguei(self, interaction: discord.Interaction, button: discord.ui.Button):
            canal_log = bot.get_channel(CANAL_LOG)
            await canal_log.send(f"@here {interaction.user.mention} alega que pagou R$ {total:.2f} via PIX. Verificar comprovante!")
            await interaction.response.send_message("✅ Avisamos o ADM! Envie o comprovante aqui pra liberar mais rápido.", ephemeral=True)
            carrinhos[user_id] = {"itens": [], "total": 0, "cupom": None}
        @discord.ui.button(label="Cancelar Compra", style=discord.ButtonStyle.red, emoji="❌")
        async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
            carrinhos[user_id] = {"itens": [], "total": 0, "cupom": None}
            await interaction.response.edit_message(content="❌ Compra cancelada.", embed=None, attachments=[], view=None)

    file = File(buffer, filename="qrcode.png")
    await interaction.response.send_message(embed=embed, file=file, view=PixView(), ephemeral=True)

    canal_log = bot.get_channel(CANAL_LOG)
    if canal_log:
        log_embed = discord.Embed(title="🛒 Novo Pedido PIX Gerado", color=discord.Color.yellow())
        log_embed.add_field(name="Cliente", value=f"{interaction.user.mention} `({interaction.user.id})`", inline=False)
        log_embed.add_field(name="Valor", value=f"R$ {total:.2f}", inline=True)
        produtos = "\n".join([f"{i['qtd']}x {i['nome']}" for i in carrinho["itens"]])
        log_embed.add_field(name="Produtos", value=produtos, inline=False)
        await canal_log.send("@here", embed=log_embed)

@bot.tree.command(name="carrinho", description="Ver seu carrinho de compras")
async def carrinho(interaction: discord.Interaction):
    await mostrar_carrinho(interaction)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user} online!')

bot.run(os.getenv("DISCORD_TOKEN"))
