import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime

# ===== CONFIGURAÇÕES DNZX STORE =====
NOME_LOJA = "DNZX STORE"
ID_CATEGORIA_TICKETS = 1504149916249886833
ID_CARGO_STAFF = 1500251010461863977
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ===== VIEWS PIX E PAGAMENTO =====
class PixView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Código copia e cola", style=discord.ButtonStyle.gray, emoji="📋")
    async def copiar_codigo(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_message(f"**Chave PIX Copia e Cola:**\n`{CHAVE_PIX}`", ephemeral=True)

    @discord.ui.button(label="Cancelar Compra", style=discord.ButtonStyle.red, emoji="❌")
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode cancelar.", ephemeral=True)
        await interaction.response.send_message("❌ Compra cancelada. Fechando ticket em 5 segundos...")
        await asyncio.sleep(5)
        await interaction.channel.delete()


class PagamentoView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Pagar com Pix", style=discord.ButtonStyle.gray, emoji="💠")
    async def pagar_pix(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        embed = discord.Embed(
            title="Pagamento via PIX criado",
            description=f"**Código copia e cola**\n```{CHAVE_PIX}```\n\n**Produto:** {self.produto}\n**Valor:** R$ {self.valor:.2f}\n\n⚠️ **Após pagar:**\n1. Envie o comprovante AQUI no ticket\n2. Aguarde a confirmação da staff\n3. Receba seu produto na DM",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"© {NOME_LOJA} #5K - 2026 | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = PixView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Pagar com Cartão", style=discord.ButtonStyle.gray, emoji="💳", disabled=True)
    async def pagar_cartao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Pagamento com cartão temporariamente indisponível. Use PIX.", ephemeral=True)

    @discord.ui.button(label="Pagar com Saldo", style=discord.ButtonStyle.gray, emoji="💰", disabled=True)
    async def pagar_saldo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Sistema de saldo em manutenção. Use PIX.", ephemeral=True)

    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="⬅️")
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
            embed = discord.Embed(
            title="Detalhes da sua compra",
            description=f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_author(name=f"{NOME_LOJA} APP", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = CarrinhoView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)

class CarrinhoView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        class CarrinhoView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="💳")
    async def pagamento(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        embed = discord.Embed(
            title="Escolha a sua forma de pagamento",
            description=f"Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = PagamentoView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="📝")
    async def editar_qtd(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_message("❌ No momento só aceitamos 1 unidade por compra. Para comprar mais, abra outro carrinho.", ephemeral=True)

    @discord.ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
    async def cupom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_modal(CupomModal(self))
        await interaction.response.send_message("❌ No momento só aceitamos 1 unidade por compra. Para comprar mais, abra outro ticket.", ephemeral=True)

    @discord.ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
    async def cupom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        class CupomModal(discord.ui.Modal, title="Aplicar Cupom"):
            cupom_input = discord.ui.TextInput(label="Digite o cupom", placeholder="Ex: 2026")

            async def on_submit(modal_self, interaction: discord.Interaction):
                cupom = modal_self.cupom_input.value.upper()
                if cupom == "2026":
                    novo_valor = self.valor * 0.9
                    self.valor = novo_valor
                    embed = discord.Embed(
                        title="✅ Cupom aplicado com sucesso!",
                        description=f"**Cupom:** {cupom} - 10% OFF\n**Novo valor:** R$ {novo_valor:.2f}",
                        color=discord.Color.green()
                    )
                    await interaction.response.send_message(embed=embed)
                    
                    embed_main = discord.Embed(
                        title="Detalhes da sua compra",
                        description=f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades**, **aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n**Produtos no Carrinho (1x)**\n`1x {self.produto} | R$ {self.valor:.2f}`\n\n**Valor à vista**\n`R$ {self.valor:.2f}`",
                        color=discord.Color.from_rgb(255, 0, 0)
                    )
                    embed_main.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
                    await interaction.message.edit(embed=embed_main)
                else:
                    await interaction.response.send_message("❌ Cupom inválido ou expirado.", ephemeral=True)

        await interaction.response.send_modal(CupomModal())

    @discord.ui.button(label="Fechar Carrinho", style=discord.ButtonStyle.red, emoji="🔒")
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id!= self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode fechar.", ephemeral=True)
        await interaction.response.send_message("🔒 Fechando carrinho em 5 segundos...")
        await asyncio.sleep(5)
        await interaction.channel.delete()


async def criar_ticket(interaction: discord.Interaction, produto: str, valor: float):
    guild = interaction.guild
    user = interaction.user
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        guild.get_role(ID_CARGO_STAFF): discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    }
    
    nome_canal = f"carrinho-{user.name}".lower().replace(" ", "-")[:100]
    categoria = guild.get_channel(ID_CATEGORIA_TICKETS)
    
    canal = await guild.create_text_channel(
        name=nome_canal,
        category=categoria,
        overwrites=overwrites
    )
    
    embed = discord.Embed(
        title="Detalhes da sua compra",
        description=f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades**, **aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n**Produtos no Carrinho (1x)**\n`1x {produto} | R$ {valor:.2f}`\n\n**Valor à vista**\n`R$ {valor:.2f}`",
        color=discord.Color.from_rgb(255, 0, 0)
    )
    embed.set_author(name=f"{NOME_LOJA} APP", icon_url=guild.icon.url if guild.icon else None)
    embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
    
    view = CarrinhoView(produto, valor, user)
    await canal.send(content=f"{user.mention}", embed=embed, view=view)
    
    await interaction.response.send_message(f"✅ Seu carrinho foi criado com êxito. {canal.mention}", ephemeral=True)


# ===== EXEMPLO COMANDO /HG =====
class HgSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="HG CHEATS 1 DIA", description="Valor: R$ 10,00", emoji="🛒", value="hg_1d"),
            discord.SelectOption(label="HG CHEATS 7 DIAS", description="Valor: R$ 30,00", emoji="🛒", value="hg_7d"),
            discord.SelectOption(label="HG CHEATS 10 DIAS", description="Valor: R$ 35,00", emoji="🛒", value="hg_10d"),
            discord.SelectOption(label="HG CHEATS 30 DIAS", description="Valor: R$ 98,00", emoji="🛒", value="hg_30d")
        ]
        super().__init__(placeholder="Selecione um Produto abaixo", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"hg_1d": 10.00, "hg_7d": 30.00, "hg_10d": 35.00, "hg_30d": 98.00}
        nomes = {"hg_1d": "HG CHEATS 1 DIA", "hg_7d": "HG CHEATS 7 DIAS", "hg_10d": "HG CHEATS 10 DIAS", "hg_30d": "HG CHEATS 30 DIAS"}
        await criar_ticket(interaction, nomes[self.values[0]], precos[self.values[0]])

class HgView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HgSelect())

@bot.tree.command(name="hg", description="Comprar HG Cheats Android")
async def hg(interaction: discord.Interaction):
    descricao = """**🪐 HG CHEATS - MOD APK EXCLUSIVO**

Compatível com todas as versões até Android 16
Tutorial completo de instalação incluso
Mod APK exclusivo

**FUNCIONALIDADES DO MENU**
- Aimbot totalmente configurável
- Suporte apenas para Free Fire normal
- Configuração de Aimbot para Cabeça, Pescoço e Peito

**VOCÊ RECEBE**
- Chave de Licença (Key)
- Tutorial / Instruções Detalhada

**⚡ ENTREGA AUTOMÁTICA VIA DM**"""

    embed = discord.Embed(title="Selecione um Produto abaixo", description=descricao, color=discord.Color.from_rgb(0, 255, 0))
    embed.set_footer(text=f"© {NOME_LOJA}")
    await interaction.response.send_message(embed=embed, view=HgView())


# ===== START DO BOT =====
@bot.event
async def on_ready():
    print(f'{bot.user} online!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} comandos")
    except Exception as e:
        print(e)

bot.run("SEU_TOKEN_AQUI")
