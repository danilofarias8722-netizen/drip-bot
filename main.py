import discord
from discord.ext import commands
from discord import ui
import urllib.parse
import asyncio
from datetime import datetime

# Inicializa o bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CONFIGURAÇÃO =====
CATEGORIA_COMPRAS_ID = 1504149916249886833
DONO_ID = 1498844150202896446
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"
NOME_PIX = "Rafael"
CIDADE_PIX = "Macapa"
# ========================

def gerar_pix_copia_cola(chave, nome, cidade, valor):
    valor_formatado = f"{float(valor.replace(',', '.')):.2f}"
    payload = [
        "000201",
        "010211",
        f"26{len(f'0014br.gov.bcb.pix01{len(chave):02d}{chave}'):02d}0014br.gov.bcb.pix01{len(chave):02d}{chave}",
        "52040000",
        "5303986",
        f"54{len(valor_formatado):02d}{valor_formatado}",
        "5802BR",
        f"59{len(nome):02d}{nome}",
        f"60{len(cidade):02d}{cidade}",
        "62070503***",
        "6304"
    ]
    return ''.join(payload) + "FFFF"

class PixView(ui.View):
    def __init__(self, produto, preco):
        super().__init__(timeout=None)
        self.produto = produto
        self.preco = preco

    @ui.button(label="Código copia e cola", style=discord.ButtonStyle.gray, emoji="📋")
    async def copiar_pix(self, interaction: discord.Interaction, button: ui.Button):
        codigo = gerar_pix_copia_cola(CHAVE_PIX, NOME_PIX, CIDADE_PIX, self.preco)
        await interaction.response.send_message(f"```{codigo}```", ephemeral=True)

    @ui.button(label="Cancelar Compra", style=discord.ButtonStyle.red, emoji="✖️")
    async def cancelar_compra(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Compra cancelada. Canal será deletado em 5s...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class PagamentoView(ui.View):
    def __init__(self, produto, preco, user_id):
        super().__init__(timeout=None)
        self.produto = produto
        self.preco = preco
        self.user_id = user_id

    @ui.button(label="Pagar com Pix", style=discord.ButtonStyle.gray, emoji="💠")
    async def pagar_pix(self, interaction: discord.Interaction, button: ui.Button):
        codigo_pix = gerar_pix_copia_cola(CHAVE_PIX, NOME_PIX, CIDADE_PIX, self.preco)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(codigo_pix)}"

        embed = discord.Embed(title="Pagamento via PIX criado", color=0x2B2D31)
        embed.add_field(name="Código copia e cola", value=f"```{codigo_pix[:100]}...```", inline=False)
        embed.set_image(url=qr_url)
        embed.set_footer(text=f"Valor: R$ {self.preco} | Hoje às {datetime.now().strftime('%H:%M')}")

        await interaction.response.send_message(embed=embed, view=PixView(self.produto, self.preco))

    @ui.button(label="Pagar com Cartão", style=discord.ButtonStyle.gray, emoji="💳", disabled=True)
    async def pagar_cartao(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Pagamento com cartão indisponível. Use PIX.", ephemeral=True)

    @ui.button(label="Pagar com Saldo", style=discord.ButtonStyle.gray, emoji="💰", disabled=True)
    async def pagar_saldo(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Você não possui saldo.", ephemeral=True)

    @ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="⬅️")
    async def voltar(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Carrinho fechado.", ephemeral=True)
        await interaction.channel.delete()class CarrinhoView(ui.View):
    def __init__(self, produto, preco, user_id):
        super().__init__(timeout=None)
        self.produto = produto
        self.preco = preco
        self.user_id = user_id

    @ui.button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="✔️")
    async def ir_pagamento(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(color=0x2B2D31)
        embed.set_author(name="danilofariasnaochamopv", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.add_field(name="Escolha a sua forma de pagamento", value=(
            "Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática e rápida.\n\n"
            f"**Produtos no Carrinho (1x)**\n"
            f"1x {self.produto} | R$ {self.preco}\n\n"
            f"**Valor à vista**\n"
            f"R$ {self.preco}"
        ), inline=False)
        embed.set_footer(text=f"Hoje às {datetime.now().strftime('%H:%M')}")

        await interaction.response.send_message(embed=embed, view=PagamentoView(self.produto, self.preco, self.user_id))

    @ui.button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def editar_qtd(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Só é possível comprar 1 unidade por vez.", ephemeral=True)

    @ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
    async def cupom(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Nenhum cupom disponível no momento.", ephemeral=True)

    @ui.button(label="Ler Termos e Condições", style=discord.ButtonStyle.blurple, emoji="📋")
    async def termos(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(
            title="📋 Termos e Condições",
            description=(
                "1. Vendemos apenas **configurações de sensibilidade e HUD**.\n"
                "2. Não comercializamos hacks, xits ou programas ilegais.\n"
                "3. Produto 100% permitido pela Garena.\n"
                "4. Não há reembolso após entrega da config.\n"
                "5. Suporte apenas via ticket."
            ),
            color=0xED4245
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ComprarView(ui.View):
    def __init__(self, produto, preco):
        super().__init__(timeout=300)
        self.produto = produto
        self.preco = preco

    @ui.button(label="💰 Comprar Agora", style=discord.ButtonStyle.green)
    async def comprar(self, interaction: discord.Interaction, button: ui.Button):
        guild = interaction.guild
        nome_canal = f"🛒-carrinho-{interaction.user.name}".lower().replace(" ", "-")[:50]

        for channel in guild.text_channels:
            if channel.topic and f"Carrinho: {interaction.user.id}" in channel.topic:
                await interaction.response.send_message(f"❌ Tu já tem um carrinho aberto: {channel.mention}", ephemeral=True)
                return

        dono = guild.get_member(DONO_ID)
        categoria = guild.get_channel(CATEGORIA_COMPRAS_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            dono: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        canal = await guild.create_text_channel(
            name=nome_canal,
            category=categoria,
            overwrites=overwrites,
            topic=f"Carrinho: {interaction.user.id} | Produto: {self.produto} | Valor: R$ {self.preco}"
        )

        embed = discord.Embed(color=0x2B2D31)
        embed.set_author(name="danilofariasnaochamopv", icon_url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Detalhes da sua compra", value=(
            "Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode alterar quantidades, aplicar cupons ou concluir sua compra usando os botões abaixo.\n\n"
            f"**Produtos no Carrinho (1x)**\n"
            f"1x {self.produto} | R$ {self.preco}\n\n"
            f"**Valor à vista**\n"
            f"R$ {self.preco}"
        ), inline=False)
        embed.set_footer(text=f"Hoje às {datetime.now().strftime('%H:%M')}")

        await canal.send(
            content=f"{interaction.user.mention} {dono.mention}",
            embed=embed,
            view=CarrinhoView(self.produto, self.preco, interaction.user.id)
        )

        embed_resp = discord.Embed(description="✅ Seu carrinho foi criado com êxito.", color=0x57F287)
        view_ir = ui.View()
        view_ir.add_item(ui.Button(label="Ver Carrinho", style=discord.ButtonStyle.gray, emoji="↗️", url=canal.jump_url))
        await interaction.response.send_message(embed=embed_resp, view=view_ir, ephemeral=True)class PainelView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            discord.SelectOption(label="DRIP CLIENTE 1 DIA - R$ 15,00", value="drip_1dia", emoji="💎"),
            discord.SelectOption(label="HG CONFIG PRO - R$ 30,00", value="pro", emoji="🔥"),
            discord.SelectOption(label="HG CONFIG ELITE - R$ 35,00", value="elite", emoji="💎"),
            discord.SelectOption(label="HG CONFIG MASTER - R$ 98,00", value="master", emoji="👑")
        ]
        select = ui.Select(placeholder="Escolha sua config 👇", options=options)
        select.callback = self.produto_callback
        self.add_item(select)

    async def produto_callback(self, interaction: discord.Interaction):
        valores = {
            "drip_1dia": ("DRIP CLIENTE 1 DIA", "15,00"),
            "pro": ("HG CONFIG PRO", "30,00"),
            "elite": ("HG CONFIG ELITE", "35,00"),
            "master": ("HG CONFIG MASTER", "98,00")
        }
        produto, preco = valores[interaction.data["values"][0]]

        embed = discord.Embed(
            title=f"🎯 {produto}",
            description=f"**Valor: R$ {preco}**\n\nConfig 100% permitida pela Garena.\nClique em comprar para abrir seu carrinho privado.",
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed, view=ComprarView(produto, preco), ephemeral=True)

@bot.tree.command(name="painel", description="Abre a loja")
async def painel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 LOJA DRIP CONFIGS",
        description=(
            "**⚠️ AVISO IMPORTANTE**\n"
            "Vendemos apenas **configurações de sensibilidade e HUD**.\n"
            "Não comercializamos hacks, xits ou programas ilegais.\n"
            "Uso 100% permitido pela Garena.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Selecione abaixo o produto desejado:"
        ),
        color=0xED4245
    )
    await interaction.response.send_message(embed=embed, view=PainelView())

@bot.event
async def on_ready():
    bot.add_view(PainelView())
    await bot.tree.sync()
    print(f'Bot online: {bot.user}')

# COLOCA TEU TOKEN AQUI
bot.run(os.getenv("DISCORD_TOKEN"))
