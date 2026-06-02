import discord
from discord.ext import commands
from discord.ui import View, Button, Select
from datetime import datetime
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# ⚠️ CONFIGURAÇÕES TODAS CORRETAS CONFORME VOCÊ PEDIU
CARGO_ADM_IDS = [1500251010461863977]  # ✅ ID DO DONO CERTO
CATEGORIA_TICKETS_ID = 1511142819069427843  # ✅ ID DA CATEGORIA DE TICKETS
CATEGORIA_CARRINHO_ID = 1511142874547355648 # ✅ ID DA CATEGORIA DE CARRINHO
NOME_BOT = "LA CASA CHEATS"
TAG_BOT = "#6K"
PIX_CODIGO = "d3169985-198b-4ca4-a119-de573d45d2ee"
PIX_QR_URL = "https://i.imgur.com/9Z7X7QH.png"
contador_carrinhos = 100
contador_tickets = 455


# ------------------- FUNÇÕES DE SISTEMA -------------------
async def criar_canal_privado(guild, usuario, nome_canal, descricao):
    """Cria canal privado com permissão SÓ do dono"""
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        usuario: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    }
    # ✅ PERMISSÕES COM O ID CERTO DO DONO
    for adm_id in CARGO_ADM_IDS:
        cargo = guild.get_role(adm_id)
        if cargo:
            overwrites[cargo] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

    categoria = guild.get_channel(CATEGORIA_CARRINHO_ID) if "carrinho" in nome_canal.lower() else guild.get_channel(CATEGORIA_TICKETS_ID)
    if not categoria:
        categoria = guild.categories[0]

    async def criar_canal_privado(guild, usuario, nome_canal, descricao):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        usuario: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    }
    for adm_id in CARGO_ADM_IDS:
        cargo = guild.get_role(adm_id)
        if cargo:
            overwrites[cargo] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

    categoria = guild.get_channel(CATEGORIA_CARRINHO_ID) if "carrinho" in nome_canal.lower() else guild.get_channel(CATEGORIA_TICKETS_ID)
    if not categoria:
        categoria = guild.categories[0]

    canal = await categoria.create_text_channel(
        name=nome_canal,
        overwrites=overwrites,
        topic=descricao
    )
    return canal
    
    
    async def suporte_android(self, interaction: discord.Interaction, button):
        global contador_tickets
        contador_tickets += 1
        numero = contador_tickets

        canal = await criar_canal_privado(
            interaction.guild, interaction.user, f"ticket-{numero}", f"Ticket aberto por {interaction.user} | Suporte Android"
        )

        mensagem_entrada = f"""**Bem-vindo(a) a #ticket-{numero}!**
Este é o começo do canal particular **#ticket-{numero}**. Aberto em {datetime.now().strftime('%d de %B de %Y às %H:%M')} por {interaction.user.mention}

───────────────────── **NOVAS MENSAGENS** ─────────────────────"""

        mensagem_ticket = f"{interaction.user.mention}\n```diff\n+ Ticket Aberto\n```\n{interaction.user.mention} criou um novo ticket 📌 **Suporte Android 🟢**.\n*Ticket King* | /close"

        botoes = View()
        fechar = discord.ui.Button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger)
        reivindicar = discord.ui.Button(label="📜 Reivindicar Ticket", style=discord.ButtonStyle.secondary)

        async def fechar_callback(inter):
            await inter.response.send_message("✅ Ticket fechado!", ephemeral=True)
            await inter.channel.delete()

        async def reivindicar_callback(inter):
            await inter.response.send_message(f"✅ {inter.user.mention} reivindicou esse ticket!", ephemeral=False)

        fechar.callback = fechar_callback
        reivindicar.callback = reivindicar_callback
        botoes.add_item(fechar)
        botoes.add_item(reivindicar)

        await canal.send(mensagem_entrada)
        await canal.send(embed=discord.Embed(description=mensagem_ticket, color=discord.Color.gold()), view=botoes)
        await interaction.response.send_message(f"✅ Ticket criado: {canal.mention}", ephemeral=True)

    @discord.ui.button(label="Suporte ios 🟣", style=discord.ButtonStyle.secondary)
    async def suporte_ios(self, interaction: discord.Interaction, button):
        global contador_tickets
        contador_tickets += 1
        numero = contador_tickets

        canal = await criar_canal_privado(
            interaction.guild, interaction.user, f"ticket-{numero}", f"Ticket aberto por {interaction.user} | Suporte IOS"
        )

        mensagem_entrada = f"""**Bem-vindo(a) a #ticket-{numero}!**
Este é o começo do canal particular **#ticket-{numero}**. Aberto em {datetime.now().strftime('%d de %B de %Y às %H:%M')} por {interaction.user.mention}

───────────────────── **NOVAS MENSAGENS** ─────────────────────"""

        mensagem_ticket = f"{interaction.user.mention}\n```diff\n+ Ticket Aberto\n```\n{interaction.user.mention} criou um novo ticket 📌 **Suporte IOS 🟣**.\n*Ticket King* | /close"

        botoes = View()
        fechar = discord.ui.Button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger)
        reivindicar = discord.ui.Button(label="📜 Reivindicar Ticket", style=discord.ButtonStyle.secondary)

        async def fechar_callback(inter):
            await inter.response.send_message("✅ Ticket fechado!", ephemeral=True)
            await inter.channel.delete()

        async def reivindicar_callback(inter):
            await inter.response.send_message(f"✅ {inter.user.mention} reivindicou esse ticket!", ephemeral=False)

        fechar.callback = fechar_callback
        reivindicar.callback = reivindicar_callback
        botoes.add_item(fechar)
        botoes.add_item(reivindicar)

        await canal.send(mensagem_entrada)
        await canal.send(embed=discord.Embed(description=mensagem_ticket, color=discord.Color.gold()), view=botoes)
        await interaction.response.send_message(f"✅ Ticket criado: {canal.mention}", ephemeral=True)

    @discord.ui.button(label="Suporte 🤵", style=discord.ButtonStyle.secondary)
    async def suporte_geral(self, interaction: discord.Interaction, button):
        global contador_tickets
        contador_tickets += 1
        numero = contador_tickets

        canal = await criar_canal_privado(
            interaction.guild, interaction.user, f"ticket-{numero}", f"Ticket aberto por {interaction.user} | Suporte Geral"
        )

        mensagem_entrada = f"""**Bem-vindo(a) a #ticket-{numero}!**
Este é o começo do canal particular **#ticket-{numero}**. Aberto em {datetime.now().strftime('%d de %B de %Y às %H:%M')} por {interaction.user.mention}

───────────────────── **NOVAS MENSAGENS** ─────────────────────"""

        mensagem_ticket = f"{interaction.user.mention}\n```diff\n+ Ticket Aberto\n```\n{interaction.user.mention} criou um novo ticket 📌 **Suporte Geral 🤵**.\n*Ticket King* | /close"

        botoes = View()
        fechar = discord.ui.Button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger)
        reivindicar = discord.ui.Button(label="📜 Reivindicar Ticket", style=discord.ButtonStyle.secondary)

        async def fechar_callback(inter):
            await inter.response.send_message("✅ Ticket fechado!", ephemeral=True)
            await inter.channel.delete()

        async def reivindicar_callback(inter):
            await inter.response.send_message(f"✅ {inter.user.mention} reivindicou esse ticket!", ephemeral=False)

        fechar.callback = fechar_callback
        reivindicar.callback = reivindicar_callback
        botoes.add_item(fechar)
        botoes.add_item(reivindicar)

        await canal.send(mensagem_entrada)
        await canal.send(embed=discord.Embed(description=mensagem_ticket, color=discord.Color.gold()), view=botoes)
        await interaction.response.send_message(f"✅ Ticket criado: {canal.mention}", ephemeral=True)


# ------------------- TELAS DE PAGAMENTO -------------------
def tela_pagamento(produto, valor):
    view = View(timeout=None)
    pix_btn = Button(label="Pagar com Pix", style=discord.ButtonStyle.secondary, emoji="💠")
    cartao_btn = Button(label="Pagar com Cartão", style=discord.ButtonStyle.secondary, emoji="💳", disabled=True)
    voltar_btn = Button(label="⬅️ Voltar", style=discord.ButtonStyle.secondary)

    async def pix_callback(inter):
        embed_pix = discord.Embed(
            description=f"**Código copia e cola**\n`{PIX_CODIGO}`\n© {NOME_BOT} {TAG_BOT} - 2025",
            color=discord.Color.dark_gray()
        )
        embed_pix.set_image(url=PIX_QR_URL)
        botoes_pix = View()
        copiar = Button(label="📋 Código copia e cola", style=discord.ButtonStyle.secondary)
        cancelar = Button(label="❌ Cancelar Compra", style=discord.ButtonStyle.danger)

        async def copiar_cb(inter):
            await inter.response.send_message(f"✅ Código copiado: `{PIX_CODIGO}`", ephemeral=True)

        async def cancelar_cb(inter):
            await inter.response.send_message("❌ Compra cancelada.", ephemeral=True)
            await inter.channel.delete()

        copiar.callback = copiar_cb
        cancelar.callback = cancelar_cb
        botoes_pix.add_item(copiar)
        botoes_pix.add_item(cancelar)
        await inter.response.send_message(embed=embed_pix, view=botoes_pix)

    async def voltar_cb(inter):
        await inter.response.edit_message(embed=tela_detalhes(produto, valor), view=tela_detalhes_botoes(produto, valor))

    pix_btn.callback = pix_callback
    voltar_btn.callback = voltar_cb
    view.add_item(pix_btn)
    view.add_item(cartao_btn)
    view.add_item(voltar_btn)
    return view


def tela_detalhes(produto, valor):
    return discord.Embed(
        title=f"📩 {produto}",
        description=f"""**Detalhes da sua compra**
Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode alterar quantidades, aplicar cupons ou concluir sua compra usando os botões abaixo.

**Produtos no Carrinho (1x)**
`1x {produto} | {valor}`

**Valor à vista**
`{valor}`
""",
        color=discord.Color.from_rgb(255, 255, 255)
    )


def tela_detalhes_botoes(produto, valor):
    view = View(timeout=None)
    pagar = Button(label="✅ Ir para pagamento", style=discord.ButtonStyle.success)
    editar = Button(label="✏️ Editar quantidade", style=discord.ButtonStyle.primary)
    cupom = Button(label="🎟️ Usar cupom de desconto", style=discord.ButtonStyle.secondary, disabled=True)
    termos = Button(label="📄 Ler Termos e Condições", style=discord.ButtonStyle.primary)

    async def pagar_cb(inter):
        embed_pag = discord.Embed(
            title=f"📩 {inter.user.display_name}",
            description=f"""**Escolha a sua forma de pagamento**
Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática e rápida.

**Produtos no Carrinho (1x)**
`1x {produto} | {valor}`

**Valor à vista**
`{valor}`
""",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        await inter.response.edit_message(embed=embed_pag, view=tela_pagamento(produto, valor))

    async def editar_cb(inter):
        await inter.response.send_message("✏️ Edição de quantidade em desenvolvimento.", ephemeral=True)

    async def termos_cb(inter):
        await inter.response.send_message("📄 Termos: Produto digital, sem reembolso após entrega.", ephemeral=True)

    pagar.callback = pagar_cb
    editar.callback = editar_cb
    termos.callback = termos_cb
    view.add_item(pagar)
    view.add_item(editar)
    view.add_item(cupom)
    view.add_item(termos)
    return view


# ------------------- MENU DE COMPRAS -------------------
def gerar_menu(opcoes_produtos):
    class MenuSelecao(Select):
        def __init__(self, lista):
            super().__init__(
                placeholder="Selecione um Produto 👇",
                options=[
                    discord.SelectOption(
                        label=nome,
                        description=f"Valor: {valor} | Estoque: {estoque}",
                        value=f"{nome}|{valor}|{estoque}"
                    ) for nome, valor, estoque in lista
                ]
            )

        async def callback(self, interaction):
            global contador_carrinhos
            contador_carrinhos += 1
            dados = self.values[0].split("|")
            nome, valor, estoque = dados[0], dados[1], dados[2]

            canal = await criar_canal_privado(
                interaction.guild, interaction.user, f"carrinho-{contador_carrinhos}", f"Produto: {nome} | Valor: {valor}"
            )

            embed_detalhe = tela_detalhes(nome, valor)
            await canal.send(embed=embed_detalhe, view=tela_detalhes_botoes(nome, valor))
            await interaction.response.send_message(f"✅ Carrinho criado: {canal.mention}", ephemeral=True)

    return View(MenuSelecao(opcoes_produtos))


# ------------------- COMANDOS PRINCIPAIS -------------------
@bot.event
async def on_ready():
    print(f"✅ Bot ONLINE 24H como: {NOME_BOT} {TAG_BOT}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="💸 Use /drip para ver os produtos"))


@bot.command(name="ticket")
async def ticket(ctx):
    embed = discord.Embed(
        title=f"**{NOME_BOT}**",
        description="""**Seja bem-vindo**
Seja bem vindo ao centro de atendimento La casa cheats, para que possamos resolver seu problema peço que clique no botão abaixo👇""",
        color=discord.Color.dark_red()
    )
    embed.set_thumbnail(url="https://i.imgur.com/7ZbX7QH.png")
    embed.set_image(url="https://i.imgur.com/4sX7QH.png")
    await ctx.send(embed=embed, view=ViewSuporte())


@bot.command(name="drip")
async def drip(ctx):
    produtos = [
        ("DRIP CLIENTE 1 DIA", "R$ 11,50", "0"),
        ("DRIP CLIENTE  3 DIAS", "R$ 30,00", "11"),
        ("DRIP CLIENTE 7 DIAS", "R$ 45,00", "5"),
        ("DRIP CLIENTE 30 DIAS", "R$ 100,00", "42")
    ]
    embed = discord.Embed(
        title="🟣 MOD MENU DRIP CLIENTE SEM ROOT ANDROID 🟣",
        description="""🔥 *MOD COM:*
✔️ *Aimbot Legit*
✔️ *Aimkill On*
✔️ *Speed On*
✔️ *Funções Esps*

🟣 *DRIP CLIENT APKMOD SEM ROOT SAFE*🟣

📱 Drip Client Mobile
✅ Compatível sem root – instale facilmente via APK.
⚡ Leve e otimizado – roda suave em qualquer aparelho.
🛡️ Atualizações frequentes – sempre na frente do anti-cheat.
🎯 Funções poderosas – AIMBOT legit, ESP e muito mais.

**Selecione um produto 👇**
""",
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"{NOME_BOT} | Qualidade e Segurança")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="contas")
async def contas(ctx):
    produtos = [
        ("Contas Level 15", "R$ 0,85", "0"),
        ("CONTA NIVEL 20+", "R$ 3,00", "8"),
        ("Conta nível 30+", "R$ 5,30", "0"),
        ("Vincular conta Ios/Android", "R$ 3,00", "∞")
    ]
    embed = discord.Embed(
        title="🔥 CONTA GUEST – PRONTA PARA USO IMEDIATO 🔥",
        description="""💎 O QUE VOCÊ RECEBE:
✔ Conta 100% funcional
✔ Acesso completo (login + senha)
✔ Entrega imediata após a compra
✔ Segurança e exclusividade garantida

📊 CATEGORIAS DISPONÍVEIS:
🔹 NÍVEL 15 AO 19 | 🔹 NÍVEL 20 AO 29 | 🔹 NÍVEL 30+

⚡ VANTAGENS:
✔ Evita perder tempo upando do zero
✔ Ideal para testes, farm ou uso principal
✔ Excelente custo-benefício
✔ Suporte garantido

🚨 IMPORTANTE:
• Conta do tipo Guest (não vinculada)
• Recomendado vincular após a compra

🔁 POLÍTICA DE TROCA:
• Troca APENAS em caso de conta na blacklist
• Obrigatório envio de print comprovando o problema
• Sem comprovação, não haverá substituição

**Selecione um produto 👇**
""",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"{NOME_BOT} | Contas Originais")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="proxyandroid")
async def proxyandroid(ctx):
    produtos = [
        ("PROXY ANDROID 1 DIA", "R$ 25,00", "12")
    ]
    embed = discord.Embed(
        title="📶 PROXY ANDROID",
        description="""PROXY ANDROID*
BYPASS 100%
COMPRA DIAMANTE
FF NORMAL DA PLAY STORE
NÃO PRECISA MEXER EM METADATAS DO JOGO
ÓTIMO PARA APOSTADOS
NÃO PRECISA DE PC OU ALGO DO TIPO
FUNCIONANDO EM TODOS ANDROID ACIMA DO 11

**Selecione um produto 🚀**
""",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"{NOME_BOT} | Conexão Segura")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="pato")
async def pato(ctx):
    produtos = [
        ("PATO 1 DIA", "R$ 15,00", "190"),
        ("PATO 3 DIAS", "R$ 30,00", "199"),
        ("PATO 7 DIAS", "R$ 40,00", "199"),
        ("PATO 15 DIAS", "R$ 60,00", "199"),
        ("PATO 30 DIAS", "R$ 80,00", "199")
    ]
    embed = discord.Embed(
        title="🟦 PATO TEAM APKMOD ANDROID 🟦",
        description="""🔥 MOD COM:
✔ Aim Kill by Fire: Head
✔ Rain Kill: 20x
✔ Aim Kill FOV: 90°
✔ AWM (Risk)
✔ Ghost V1
✔ TeleKill
✔ TelePlayer By Fire 10M
✔ Aim Magnet

🟦 PATO TEAM MOD SEM ROOT SAFE 🟦

📱 PatoTeam Mobile
✅ Compatível sem root – instalação rápida e prática via APK.
⚡ Desempenho otimizado – leve, rápido e liso em qualquer aparelho.
🛡 Atualizações frequentes – sempre atualizado contra o anti-cheat.
🎯 Recursos avançados – AIM completo, TELEKILL, GHOST e muito mais.

**Selecione um produto 👇**
""",
        color=discord.Color.darker_gray()
    )
    embed.set_footer(text=f"{NOME_BOT} | Qualidade e Desempenho")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="bypass")
async def bypass(ctx):
    produtos = [
        ("BYPASS FULL ANDROID", "R$ 15,00", "961")
    ]
    embed = discord.Embed(
        title="⚡ BYPASS — SEGURANÇA",
        description="""```-PACK PARA DAR BYPASS 100% NOS ADM 🤑```
```PACK VEM COM SUAS VANTAGENS COMO👇```

```-COMPRAR DIAMANTE 💎💎```
```-MUDAR AS INFORMAÇÕES DO APK MOD PARA "GOOGLE PLAY STORE" QUE CONSTA QUE FOI BAIXADO PELO PLAY STORE```
```-PASSA O REPLAY DO MOD APK PARA O FREE FIRE NORMAL✅```
```-SCRIPT 100% FUNCIONAL✅```
```-✅SEM NECESSIDADE DE PC,ROOT OU ALGO DO TIPO✅-```

**Selecione um produto 👇**
""",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"{NOME_BOT} | Proteção e Segurança")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="hspescoco")
async def hspescoco(ctx):
    produtos = [
        ("HS PESCOÇO", "R$ 10,00", "196")
    ]
    embed = discord.Embed(
        title="💀 HS PESCOÇO",
        description="""HS PESCOÇO 💧 | Produto

✅ FUNCIONA EM TODAS AS VERSÕES DO ANDROID DA XIAOMI!!
✅ SEM NECESSIDADE DE PC OU ROOT
✅ ENTREGA IMEDIATA
✅ NÃO É FREE FIRE MODIFICADO
✅ VOCÊ RECEBE OS DOWNLOAD + TUTORIAL DE INSTALAÇÃO

💵 | Valor à vista: R$ 10,00
📦 | Restam: 196

**Selecione um produto 👇**
""",
        color=discord.Color.dark_red()
    )
    embed.set_footer(text=f"{NOME_BOT} | Qualidade Garantida")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="holograma")
async def holograma(ctx):
    produtos = [
        ("HOLOGRAMA", "R$ 4,99", "89")
    ]
    embed = discord.Embed(
        title="✨ HOLOGRAMA",
        description="""HOLOGRAMA 👻 | Produto

✅ HOLOGRAMA ANDROID
✅ GELO TRANSPARENTE
✅ ANTI-BAN E ANTI-BLACK
✅ TUTORIAL DE INSTALAÇÃO
✅ ACESSO PERMANENTE
✅ ANDROID 11 PRA CIMA
✅ SEM NECESSIDADE DE PC OU ROOT

💵 | Valor à vista: R$ 4,99
📦 | Restam: 89

**Selecione um produto 👇**
""",
        color=discord.Color.magenta()
    )
    embed.set_footer(text=f"{NOME_BOT} | Visual Exclusivo")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="auxilio")
async def auxilio(ctx):
    produtos = [
        ("HOLOGRAMA + AUXÍLIO", "R$ 10,00", "144")
    ]
    embed = discord.Embed(
        title="🆘 AUXÍLIO + HOLOGRAMA",
        description="""HOLOGRAMA + AUXÍLIO | Produto

✅ AUXÍLIO + HOLOGRAMA
✅ GELO TRANSPARENTE
✅ ANTI-BAN E ANTI-BLACK
✅ TUTORIAL DE INSTALAÇÃO
✅ NECESSITA DE SHIZUKO
✅ ACESSO PERMANENTE

💵 | Valor à vista: R$ 10,00
📦 | Restam: 144

**Selecione um produto 👇**
""",
        color=discord.Color.gold()
    )
    embed.set_image(url="https://i.imgur.com/8dR7x
    Qy.png")
    embed.set_footer(text=f"{NOME_BOT} | Suporte Completo")
    await ctx.send(embed=embed, view=gerar_me_menu(produtos))


@bot.command(name="mandela")
async def mandela(ctx):
    produtos = [
        ("TEXTURA DO MANDELA", "R$ 4,99", "159")
    ]
    embed = discord.Embed(
        title="🌌 TEXTURA DO MANDELA 💎",
        description="""TEXTURA DO MANDELA 💎 | Produto

✅ TEXTURA MANDELA
✅ SEM NECESSIDADE DE PC OU ROOT
✅ NÃO É APK OU FF MODIFICADO
✅ SEM RISCO DE BAN OU BLACK
✅ FUNCIONA EM FF MAX E NORMAL
✅ ACESSO PERMANENTE

💵 | Valor à vista: R$ 4,99
📦 | Restam: 159

**Selecione um produto 👇**
""",
        color=discord.Color.dark_blue()
    )
    embed.set_footer(text=f"{NOME_BOT} | Texturas Exclusivas")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="painelios")
async def painelios(ctx):
    produtos = [
        ("PAINEL MONITE 1 DIA {BASIC}", "R$ 19,00", "198"),
        ("PAINEL MONITE 7 DIAS {BASIC}", "R$ 39,90", "198"),
        ("PAINEL MONITE 30 DIAS {BASIC}", "R$ 89,90", "199"),
        ("{SEPARADOR DE PRODUTOS}", "R$ 1,00", "0"),
        ("PAINEL MONITE 1 DIA {PRO}", "R$ 27,90", "198"),
        ("PAINEL MONITE 7 DIAS {PRO}", "R$ 59,90", "199"),
        ("PAINEL MONITE 30 DIAS {PRO}", "R$ 99,90", "199")
    ]
    embed = discord.Embed(
        title="🍏 PAINEL IOS",
        description="""FUNCIONA EM TODOS iPHONES E
TODAS VERSÕES DO iOS (SEM
BLACKLIST E SEM BAN)

# PLANOS DISPONÍVEIS


 ## **PLANO BASIC** ⚙️

Funções incluídas:

* Aimbot configurável
* ESP configurável
* No Recoil
* Troca rápida de arma
* 120 FPS
* Resetar convidado
* Modo Stream
* Precisa de Gbox

## **PLANO PRO** 🛡️

Inclui tudo do Plano Basic, com **funções adicionais:**

* **Speed**
* **AIMKILL**
* **Teleport 10m**
* **Recarregamento rápida**
* **Kit médico rápido**
* **Precisa de Gbox**

## **OBSERVAÇÃO.**

Ambos os planos utilizam o mesmo painel e possuem o mesmo nível de segurança.
A diferença está apenas nas funções extras do plano Pro.

**Selecione um produto 👇**
""",
        color=discord.Color.light_grey()
    )
    embed.set_footer(text=f"{NOME_BOT} | Painel Exclusivo IOS")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="proxyios")
async def proxyios(ctx):
    produtos = [
        ("PROXY IOS 1 HORA", "R$ 2,00", "0"),
        ("PROXY IOS 1 DIA", "R$ 6,00", "82"),
        ("PROXY IOS 3 DIAS", "R$ 15,00", "148"),
        ("PROXY IOS 7 DIAS", "R$ 22,00", "148"),
        ("PROXY IOS 30 DIAS", "R$ 55,00", "150")
    ]
    embed = discord.Embed(
        title="🍏 PROXY IOS",
        description="""**🎯 HS ALTO IOS | 100% MOBILE**

**A REVOLUÇÃO NO IOS CHEGOU: SEM PC, SEM CERTIFICADO, APENAS O SEU CELULAR!**

Esqueça métodos complicados. O nosso **HS ALTO** foi desenvolvido para quem busca praticidade máxima e performance de elite. Instalação instantânea direto no seu aparelho!


**🔥 DIFERENCIAIS EXCLUSIVOS (MOBILE)**
O único que entrega tudo isso sem precisar de acessórios externos:

* 📱 **Instalação via Wi-Fi:** Faça tudo pelo seu próprio celular. **Não precisa de PC ou Notebook.**
* 🛡️ **Zero Certificado:** Diga adeus às revogações! Nosso método dispensa certificados comuns.
* ⚡ **Bypass Ultra Melhorado:** Exclusivo para o — a proteção mais avançada contra Blacklist e Ban do mercado.
* 🚫 **Sem Formatação:** Instalação limpa em minutos, **sem perder seus dados** ou arquivos.
* ✅ **Compatibilidade Total:** Rodando liso em **todas as versões do iOS.**


**💎 LICENÇA PERMANENTE (O MELHOR INVESTIMENTO)**
O plano favorito dos mestres, com benefícios superiores:

* 🚀 **Performance máxima**
* 🔄 **Atualizações vitalícias**
* 🛡️ **Proteção premium**
* 📞 **Suporte prioritário 24h**

**Selecione um produto 👇**
""",
        color=discord.Color.light_grey()
    )
    embed.set_image(url="https://i.imgur.com/8dR7xQy.png")
    embed.set_footer(text=f"{NOME_BOT} | Proxy Exclusivo IOS")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


@bot.command(name="gbox")
async def gbox(ctx):
    produtos = [
        ("Certificado GBOX iOS (até 1 ano)", "R$ 60,00", "197")
    ]
    embed = discord.Embed(
        title="📦 GBOX",
        description=""":package: **Produto Digital — 🥇Certificado GBOX iOS (até 1 ano) **

- :page_facing_up: **Certificado iOS**
- :mobile_phone: **Instalação fácil direto pelo celular — sem necessidade de computador**
- :tools: **Ative o Modo Desenvolvedor no seu iPhone com segurança**
- :no_entry_sign: **Corrija erros de integridade durante a instalação de apps**
- :package: **Instale arquivos .ipa sem complicações ou bloqueios**
- :calling: **Acesse mais de 1000 apps e cheats personalizados com facilidade**
- :video_game: **Ideal para quem quer segurança e praticidade ao instalar apps exclusivos**

💸 **| Valor à vista:** `R$ 60,00`
📦 **| Restam:** `197`

**Selecione um produto 👇**
""",
        color=discord.Color.light_grey()
    )
    embed.set_footer(text=f"{NOME_BOT} | Certificado Exclusivo IOS")
    await ctx.send(embed=embed, view=gerar_menu(produtos))


# ------------------- COMANDOS ADMIN -------------------
@bot.command(name="confirmarpagamento")
async def confirmarpagamento(ctx):
    cargos_user = [role.id for role in ctx.author.roles]
    if not any(adm_id in cargos_user for adm_id in CARGO_ADM_IDS):
        return await ctx.send("❌ Você não tem permissão para usar esse comando!", ephemeral=True)

    embed = discord.Embed(
        title="✅ PAGAMENTO CONFIRMADO",
        description=f"**Produto:** {ctx.channel.topic if ctx.channel.topic else 'Não definido'}\n**Status:** PAGO E LIBERADO ✅\n\n**Aproveite!**",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"{NOME_BOT} | Sistema de Vendas 24h")
    await ctx.send(embed=embed)


@bot.command(name="close")
async def fechar_ticket(ctx):
    cargos_user = [role.id for role in ctx.author.roles]
    if not any(adm_id in cargos_user for adm_id in CARGO_ADM_IDS):
        return await ctx.send("❌ Apenas ADMs podem fechar tickets!", ephemeral=True)
    await ctx.send("✅ Ticket fechado por um administrador.")
    await ctx.channel.delete()


# 🔴 CONFIGURADO PARA PEGAR O TOKEN DO FLYCTL (SEGURANÇA)
bot.run(os.getenv("TOKEN"))
    
