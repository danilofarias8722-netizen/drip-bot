import discord
from discord.ext import commands
from discord import app_commands, File, PermissionOverwrite
import qrcode
import io
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
NOME_RECEBEDOR = "Rafael"
CIDADE = "MACAPA"
CANAL_LOG = 1504149916249886833
CATEGORIA_CARRINHO = 1504149916249886834
NOME_LOJA = "DNZX STORE"
carrinhos = {}

def gerar_payload_pix(chave, nome, cidade, valor, txid="***"):
    valor_formatado = f"{valor:.2f}"
    payload = [
        f"000201",
        f"26{len('0014br.gov.bcb.pix01' + str(len(chave)).zfill(2) + chave):02}0014br.gov.bcb.pix01{len(chave):02}{chave}",
        f"52040000",
        f"5303986",
        f"54{len(valor_formatado):02}{valor_formatado}",
        f"5802BR",
        f"59{len(nome):02}{nome}",
        f"60{len(cidade):02}{cidade}",
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

async def criar_canal_carrinho(interaction: discord.Interaction):
    user_id = interaction.user.id
    guild = interaction.guild
    categoria = guild.get_channel(CATEGORIA_CARRINHO)
    
    if user_id in carrinhos and carrinhos[user_id].get("canal_id"):
        canal = guild.get_channel(carrinhos[user_id]["canal_id"])
        if canal: return canal

    overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=False),
        interaction.user: PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: PermissionOverwrite(read_messages=True, send_messages=True)
    }
    nome_canal = f"carrinho-{interaction.user.name.lower()}"[:32]
    canal = await guild.create_text_channel(nome_canal, category=categoria, overwrites=overwrites)
    
    if user_id not in carrinhos: carrinhos[user_id] = {"itens": [], "total": 0, "cupom": None}
    carrinhos[user_id]["canal_id"] = canal.id
    return canal

async def add_carrinho(interaction: discord.Interaction, produto: str, preco: float):
    user_id = interaction.user.id
    if user_id not in carrinhos: carrinhos[user_id] = {"itens": [], "total": 0, "cupom": None}
    for item in carrinhos[user_id]["itens"]:
        if item["nome"] == produto: 
            item["qtd"] += 1
            carrinhos[user_id]["total"] += preco
            break
    else: 
        carrinhos[user_id]["itens"].append({"nome": produto, "preco": preco, "qtd": 1})
        carrinhos[user_id]["total"] += preco

    canal = await criar_canal_carrinho(interaction)
    await interaction.response.send_message(f"✅ Seu carrinho foi criado com êxito. Acesse: {canal.mention}", ephemeral=True)
    await mostrar_carrinho(canal, user_id)

class HgSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1 DIA", description="Valor: R$ 10,00", emoji="🛒", value="hg_1d"),
            discord.SelectOption(label="7 DIAS", description="Valor: R$ 30,00", emoji="🛒", value="hg_7d"),
            discord.SelectOption(label="10 DIAS", description="Valor: R$ 35,00", emoji="🛒", value="hg_10d"),
            discord.SelectOption(label="30 DIAS", description="Valor: R$ 98,00", emoji="🛒", value="hg_30d")
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

class ProxySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="7 DIAS", description="Valor: R$ 30,00", emoji="🛒", value="proxy_7d"),
            discord.SelectOption(label="30 DIAS", description="Valor: R$ 50,00", emoji="🛒", value="proxy_30d")
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

class PremiumSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PAINEL MONITE 7 DIAS", description="Valor: R$ 35,00", emoji="🛒", value="painel_7d"),
            discord.SelectOption(label="PAINEL MONITE 30 DIAS", description="Valor: R$ 80,00", emoji="🛒", value="painel_30d")
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
    await interaction.response.send_message(embed=embed, view=PremiumView())class PacksSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PACK INICIANTE", description="Valor: R$ 15,00", emoji="📦", value="pack_1"),
            discord.SelectOption(label="PACK AVANÇADO", description="Valor: R$ 45,00", emoji="📦", value="pack_2"),
            discord.SelectOption(label="PACK COMPLETO", description="Valor: R$ 75,00", emoji="📦", value="pack_3")
        ]
        super().__init__(placeholder="Selecione um Pack abaixo", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        precos = {"pack_1": 15.00, "pack_2": 45.00, "pack_3": 75.00}
        nomes = {"pack_1": "PACK INICIANTE", "pack_2": "PACK AVANÇADO", "pack_3": "PACK COMPLETO"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PacksSelect())

@bot.tree.command(name="packs", description="Comprar Packs DNZX")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📦 PACKS DNZX",
        description="**Combos com desconto**\n**Vários produtos em 1**\n\n**VOCÊ RECEBE**\n• Produtos do pack\n• Suporte exclusivo",
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=PacksView())

class PescocoSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="AIM PESCOÇO 7 DIAS", description="Valor: R$ 20,00", emoji="🎯", value="pesc_7d"),
            discord.SelectOption(label="AIM PESCOÇO 30 DIAS", description="Valor: R$ 40,00", emoji="🎯", value="pesc_30d")
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        precos = {"pesc_7d": 20.00, "pesc_30d": 40.00}
        nomes = {"pesc_7d": "AIM PESCOÇO 7 DIAS", "pesc_30d": "AIM PESCOÇO 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PescocoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PescocoSelect())

@bot.tree.command(name="pescoço", description="Comprar Aim Pescoço")
async def pescoco(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 AIM PESCOÇO",
        description="**Aim focado no pescoço**\n**Menos ban que cabeça**\n**Funciona em todos Android**\n\n**VOCÊ RECEBE**\n• Key de ativação\n• Tutorial completo",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=PescocoView())

class PeitoSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="AIM PEITO 7 DIAS", description="Valor: R$ 20,00", emoji="🎯", value="peito_7d"),
            discord.SelectOption(label="AIM PEITO 30 DIAS", description="Valor: R$ 40,00", emoji="🎯", value="peito_30d")
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        precos = {"peito_7d": 20.00, "peito_30d": 40.00}
        nomes = {"peito_7d": "AIM PEITO 7 DIAS", "peito_30d": "AIM PEITO 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PeitoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PeitoSelect())

@bot.tree.command(name="peito", description="Comprar Aim Peito")
async def peito(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 AIM PEITO",
        description="**Aim focado no peito**\n**Safe pra ranked**\n**Funciona em todos Android**\n\n**VOCÊ RECEBE**\n• Key de ativação\n• Tutorial completo",
        color=discord.Color.teal()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=PeitoView())

class ContasSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="CONTA LEVEL 50", description="Valor: R$ 25,00", emoji="👤", value="conta_50"),
            discord.SelectOption(label="CONTA DIAMANTES", description="Valor: R$ 60,00", emoji="💎", value="conta_dima"),
            discord.SelectOption(label="CONTA RARAS", description="Valor: R$ 120,00", emoji="🔥", value="conta_rara")
        ]
        super().__init__(placeholder="Selecione uma Conta abaixo", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        precos = {"conta_50": 25.00, "conta_dima": 60.00, "conta_rara": 120.00}
        nomes = {"conta_50": "CONTA LEVEL 50", "conta_dima": "CONTA DIAMANTES", "conta_rara": "CONTA RARAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ContasSelect())

@bot.tree.command(name="contas", description="Comprar Contas FF")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👤 CONTAS FREE FIRE",
        description="**Contas upadas e com skins**\n**Entrega automática**\n**Garantia de acesso**\n\n**VOCÊ RECEBE**\n• Login e senha\n• Email de recuperação",
        color=discord.Color.dark_blue()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=ContasView())

class HologramaSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="HOLOGRAMA 7 DIAS", description="Valor: R$ 25,00", emoji="👁️", value="holo_7d"),
            discord.SelectOption(label="HOLOGRAMA 30 DIAS", description="Valor: R$ 55,00", emoji="👁️", value="holo_30d")
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        precos = {"holo_7d": 25.00, "holo_30d": 55.00}
        nomes = {"holo_7d": "HOLOGRAMA 7 DIAS", "holo_30d": "HOLOGRAMA 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class HologramaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HologramaSelect())

@bot.tree.command(name="holograma", description="Comprar Holograma")
async def holograma(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👁️ HOLOGRAMA",
        description="**Ver inimigos através da parede**\n**ESP completo**\n**Funciona em todos Android**\n\n**VOCÊ RECEBE**\n• Key de ativação\n• Tutorial completo",
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=HologramaView())

class CupomModal(discord.ui.Modal, title="Aplicar Cupom"):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
    
    cupom = discord.ui.TextInput(label="Digite o cupom", placeholder="Ex: 2026", required=True)
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.cupom.value == "2026":
            carrinhos[self.user_id]["cupom"] = "2026"
            await interaction.response.defer()
            await mostrar_carrinho(interaction.channel, self.user_id)
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
            await interaction.response.defer()
            await mostrar_carrinho(interaction.channel, self.user_id)
        except:
            await interaction.response.send_message("❌ Digite apenas números.", ephemeral=True)

async def mostrar_carrinho(canal, user_id):
    if user_id not in carrinhos or not carrinhos[user_id]["itens"]:
        return await canal.send("Seu carrinho está vazio.")
    
    carrinho = carrinhos[user_id]
    descricao = "Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades, aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n**Produtos no Carrinho**\n"
    
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
            await tela_pagamento(interaction, user_id)
        
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
        
        @discord.ui.button(label="Fechar Carrinho", style=discord.ButtonStyle.red, emoji="🗑️")
        async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.channel.delete()
            del carrinhos[user_id]
    
    async for msg in canal.history(limit=10):
        if msg.author == bot.user:
            await msg.delete()
    
    await canal.send(embed=embed, view=CarrinhoView())

async def gerar_pix(interaction: discord.Interaction, user_id: int):
    carrinho = carrinhos[user_id]
    total = carrinho["total"]
    if carrinho["cupom"]:
        total = total * 0.9
    
    payload = gerar_payload_pix(CHAVE_PIX, NOME_RECEBEDOR, CIDADE, total)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    file = File(buffer, filename="pix.png")
    embed = discord.Embed(
        title="💠 PIX Copia e Cola",
        description=f"**Valor: R$ {total:.2f}**\n\n```{payload}```\n\nEscaneie o QR Code ou use o código acima.",
        color=discord.Color.green()
    )
    embed.set_image(url="attachment://pix.png")
    await interaction.response.send_message(embed=embed, file=file)

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
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="↩️")
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await mostrar_carrinho(interaction.channel, self.user_id)

async def tela_pagamento(interaction: discord.Interaction, user_id: int):
    if user_id not in carrinhos or not carrinhos[user_id]["itens"]:
        return await interaction.response.send_message("Seu carrinho está vazio.", ephemeral=True)
    
    carrinho = carrinhos[user_id]
    total = carrinho["total"]
    if carrinho["cupom"]:
        total = total * 0.9
    
    descricao = f"Escolha a forma de pagamento abaixo.\n\n**Total: R$ {total:.2f}**"
    embed = discord.Embed(title="💳 Pagamento", description=descricao, color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=PagamentoView(user_id))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user} online! Comandos sincronizados.')

bot.run(os.getenv("DISCORD_TOKEN"))
