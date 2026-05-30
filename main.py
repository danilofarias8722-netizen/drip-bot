import discord
from discord.ext import commands
from discord.utils import get
import datetime
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

CARGO_ADMIN_IDS = ["1500251010461863977", "[1500251010461863977"]

# 📌 NÃO PRECISA DE ID, SÓ NOME MESMO 📌
CATEGORIA_TICKETS = "🎟️ TICKETS"
CATEGORIA_CARRINHO = "🛒 CARRINHOS"
NOME_BOT = "LA CASA CHEATS"
TAG_BOT = "#6K"
# ✅ CÓDIGO PIX NOVO QUE VOCÊ PEDIU
CODIGO_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

@bot.event
async def on_ready():
    print(f'✅ Bot ONLINE como: {bot.user.name}')


# 🛒 FUNÇÃO: CRIAR CARRINHO PRIVADO
async def criar_carrinho(interaction: discord.Interaction, produto_nome: str, valor: str):
    await interaction.response.defer(ephemeral=True)

    # Cria categoria se não existir
    categoria = get(interaction.guild.categories, name=CATEGORIA_CARRINHO)
    if not categoria:
        categoria = await interaction.guild.create_category(name=CATEGORIA_CARRINHO, position=1)

    usuario = interaction.user
    usuario_nome = f"{usuario.name}-{usuario.discriminator}"

    # 📁 Cria canal
    canal = await interaction.guild.create_text_channel(
        name=f'carrinho-{usuario_nome.lower()}',
        category=categoria,
        topic=f'Carrinho: {usuario_nome} | Produto: {produto_nome} | Valor: R$ {valor}',
        reason="Nova compra"
    )

    # 🔒 PERMISSÕES: SÓ VOCÊ E A PESSOA VEEM
    await canal.set_permissions(interaction.guild.default_role, view_channel=False)
    await canal.set_permissions(usuario, view_channel=True, send_messages=True, read_messages=True, attach_files=True)
for cargo_id in CARGO_ADMIN_IDS:
    cargo = interaction.guild.get_role(cargo_id)
    if cargo:
        await canal.set_permissions(cargo, view_channel=True, send_messages=True, read_messages=True, manage_channels=True)
        
    # ✅ Mensagem de sucesso
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Ver Carrinho", style=discord.ButtonStyle.gray, emoji="🔗", url=f"https://discord.com/channels/{interaction.guild.id}/{canal.id}"))

    await interaction.followup.send(
        f"**{NOME_BOT}**\n✅ Seu carrinho foi criado com sucesso.",
        view=view,
        ephemeral=True
    )


    # 📑 TELA 1: DETALHES DA COMPRA
    async def tela_detalhes():
        embed = discord.Embed(
            title="Detalhes da sua compra",
            description=f"""
Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode alterar quantidades, aplicar cupons ou concluir sua compra usando os botões abaixo.

**Produtos no Carrinho (1x)**
`1x {produto_nome} | R$ {valor}`

**Valor à vista**
`R$ {valor}`
            """,
            color=discord.Color.from_rgb(255, 204, 102)
        )
        embed.set_author(name=f"{NOME_BOT} {TAG_BOT}", icon_url=bot.user.display_avatar.url)
        embed.set_footer(text=f"Hoje às {datetime.datetime.now().strftime('%H:%M')}")

        botoes = discord.ui.View(timeout=None)

        btn_pagar = discord.ui.Button(label="Ir para pagamento", style=discord.ButtonStyle.success, emoji="✅")
        btn_editar = discord.ui.Button(label="Editar quantidade", style=discord.ButtonStyle.primary, emoji="✏️")
        btn_cupom = discord.ui.Button(label="Usar cupom de desconto", style=discord.ButtonStyle.secondary, emoji="🎟️")
        btn_termos = discord.ui.Button(label="Ler Termos e Condições", style=discord.ButtonStyle.blurple, emoji="📋")

        async def ir_pagamento(inter: discord.Interaction):
            await inter.response.defer()
            await tela_pagamento()

        btn_pagar.callback = ir_pagamento
        botoes.add_item(btn_pagar)
        botoes.add_item(btn_editar)
        botoes.add_item(btn_cupom)
        botoes.add_item(btn_termos)

        await canal.send(embed=embed, view=botoes)


    # 💳 TELA 2: ESCOLHA DE PAGAMENTO
    async def tela_pagamento():
        embed = discord.Embed(
            title="Escolha a sua forma de pagamento",
            description=f"""
Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática e rápida.

**Produtos no Carrinho (1x)**
`1x {produto_nome} | R$ {valor}`

**Valor à vista**
`R$ {valor}`
            """,
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_author(name=f"{NOME_BOT} {TAG_BOT}", icon_url=bot.user.display_avatar.url)
        embed.set_footer(text=f"Hoje às {datetime.datetime.now().strftime('%H:%M')}")

        botoes_pag = discord.ui.View(timeout=None)

        btn_pix = discord.ui.Button(label="Pagar com Pix", style=discord.ButtonStyle.secondary, emoji="💠")
        btn_cartao = discord.ui.Button(label="Pagar com Cartão", style=discord.ButtonStyle.secondary, emoji="💳")
        btn_voltar = discord.ui.Button(label="Voltar", style=discord.ButtonStyle.secondary, emoji="⬅️")

        async def mostrar_pix(inter: discord.Interaction):
            await inter.response.defer()
            await tela_pix()

        async def voltar_detalhes(inter: discord.Interaction):
            await inter.response.defer()
            await tela_detalhes()

        btn_pix.callback = mostrar_pix
        btn_voltar.callback = voltar_detalhes
        botoes_pag.add_item(btn_pix)
        botoes_pag.add_item(btn_cartao)
        botoes_pag.add_item(btn_voltar)

        await canal.send(embed=embed, view=botoes_pag)


    # 🟦 TELA 3: PIX COM CÓDIGO NOVO
    async def tela_pix():
        embed = discord.Embed(
            title="Código copia e cola",
            description=f"`{CODIGO_PIX}`",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_author(name=f"{NOME_BOT} {TAG_BOT}", icon_url=bot.user.display_avatar.url)
        embed.set_footer(text=f"Hoje às {datetime.datetime.now().strftime('%H:%M')}")
        # COLOQUE A URL DO SEU QR CODE AQUI:
        # embed.set_image(url="LINK_DA_IMAGEM_QRCODE")

        botoes_pix = discord.ui.View(timeout=None)
        btn_copiado = discord.ui.Button(label="Já copiei", style=discord.ButtonStyle.success, emoji="✅")
        btn_voltar = discord.ui.Button(label="Voltar", style=discord.ButtonStyle.secondary, emoji="⬅️")

        async def confirma(inter: discord.Interaction):
            await inter.response.send_message("✅ Certo! Assim que confirmarmos o pagamento, enviaremos seu produto aqui mesmo.", ephemeral=True)

        async def voltar_pagamento(inter: discord.Interaction):
            await inter.response.defer()
            await tela_pagamento()

        btn_copiado.callback = confirma
        btn_voltar.callback = voltar_pagamento
        botoes_pix.add_item(btn_copiado)
        botoes_pix.add_item(btn_voltar)

        await canal.send(embed=embed, view=botoes_pix)


    # INICIA TUDO
    await tela_detalhes()


# 🎟️ COMANDO /TICKET
@bot.command(name='ticket')
async def ticket_completo(ctx):
    mensagem = """
🎟️ **SUPORTE E ATENDIMENTO** 🎟️

Precisa de ajuda, tem dúvidas, problemas com compra ou quer pedir algo?
Crie um ticket abaixo que nossa equipe vai atender você o mais rápido possível!

📌 **Regras:**
✅ Apenas um ticket por vez
✅ Seja claro no motivo do atendimento
✅ Não abra ticket para assuntos desnecessários

━━━━━━━━━━━━━━━━━━━━━━
👇 **Clique para abrir um chamado** 👇
    """
    view = discord.ui.View(timeout=None)

    async def abrir_ticket(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Cria categoria se não existir
        categoria = get(interaction.guild.categories, name=CATEGORIA_TICKETS)
        if not categoria:
            categoria = await interaction.guild.create_category(name=CATEGORIA_TICKETS, position=0)

        usuario = interaction.user
        usuario_nome = f"{usuario.name}-{usuario.discriminator}"

        # 📁 Cria canal do ticket
        canal = await interaction.guild.create_text_channel(
            name=f'ticket-{usuario_nome.lower()}',
            category=categoria,
            topic=f'Ticket aberto por: {usuario_nome} | Data: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}',
            reason="Novo atendimento"
        )

        # 🔒 PERMISSÕES: SÓ VOCÊ E ADMS VEEM
        await canal.set_permissions(interaction.guild.default_role, view_channel=False)
        await canal.set_permissions(usuario, view_channel=True, send_messages=True, read_messages=True, attach_files=True)
        cargo_admin = interaction.guild.get_role(CARGO_ADMIN_ID)
        if cargo_admin:
            await canal.set_permissions(cargo_admin, view_channel=True, send_messages=True, manage_channels=True, manage_messages=True)

        # ✅ Mensagem de sucesso
        view_link = discord.ui.View(timeout=None)
        view_link.add_item(discord.ui.Button(label="Acessar Ticket", style=discord.ButtonStyle.gray, emoji="🔗", url=f"https://discord.com/channels/{interaction.guild.id}/{canal.id}"))

        await interaction.followup.send(
            f"**{NOME_BOT}**\n✅ Seu ticket foi criado com sucesso! Aguarde nossa resposta.",
            view=view_link,
            ephemeral=True
        )

        # 📩 Mensagem dentro do ticket
        embed = discord.Embed(
            title="🎟️ ATENDIMENTO ABERTO",
            description=f"Olá {usuario.mention}, seja bem-vindo(a)!\n\nExplique detalhadamente o que precisa, tire suas dúvidas ou informe o problema.\nNossa equipe irá responder em instantes.\n\n🔒 *Apenas você e a administração podem ver esse canal.*",
            color=discord.Color.from_rgb(102, 204, 255)
        )
        embed.set_author(name=f"{NOME_BOT} {TAG_BOT}", icon_url=bot.user.display_avatar.url)
        embed.set_footer(text=f"Aberto em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

        await canal.send(embed=embed)

    btn_abrir = discord.ui.Button(label="Abrir Ticket", style=discord.ButtonStyle.success, emoji="🎟️")
    btn_abrir.callback = abrir_ticket
    view.add_item(btn_abrir)

    await ctx.send(mensagem, view=view)


# 🟣 COMANDO /DRIP
@bot.command(name='drip')
async def drip_completo(ctx):
    mensagem = """
🟣 MOD MENU DRIP CLIENTE SEM ROOT ANDROID 🟣

🔥 *MOD COM:*
✔️ *Aimbot Legit*
✔️ *Aimkill On*
✔️ *Speed On*
✔️ *Funções Esps*

🟣 *DRIP CLIENT APKMOD SEM ROOT SAFE*🟣

📱 Drip Client Mobile
A solução definitiva para jogadores de Free Fire no celular.

✅ Compatível sem root – instale facilmente via APK.
⚡ Leve e otimizado – roda suave em qualquer aparelho.
🛡️ Atualizações frequentes – sempre na frente do anti-cheat.
🎯 Funções poderosas – AIMBOT legit, ESP e muito mais.

👉 Ideal para quem quer desempenho máximo direto no smartphone.

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)

    produtos = [
        {"nome": "DRIP CLIENTE 1 DIA", "valor": "11,50", "id": "drip1"},
        {"nome": "DRIP CLIENTE 3 DIAS", "valor": "30,00", "id": "drip3"},
        {"nome": "DRIP CLIENTE 7 DIAS", "valor": "45,00", "id": "drip7"},
        {"nome": "DRIP CLIENTE 30 DIAS", "valor": "100,00", "id": "drip30"}
    ]

    async def clique(interaction: discord.Interaction):
        for p in produtos:
            if p["id"] == interaction.data["custom_id"]:
                await criar_carrinho(interaction, p["nome"], p["valor"])

    for p in produtos:
        btn = discord.ui.Button(label=f"{p['nome']} | R$ {p['valor']}", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id=p["id"])
        btn.callback = clique
        view.add_item(btn)

    await ctx.send(mensagem, view=view)


# 🟦 COMANDO /PATO
@bot.command(name='pato')
async def pato_completo(ctx):
    mensagem = """
🟦 PATO TEAM APKMOD ANDROID 🟦

🔥 MOD COM:
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
A solução definitiva para jogadores de Free Fire no celular.

✅ Compatível sem root – instalação rápida e prática via APK.
⚡ Desempenho otimizado – leve, rápido e liso em qualquer aparelho.
🛡 Atualizações frequentes – sempre atualizado contra o anti-cheat.
🎯 Recursos avançados – AIM completo, TELEKILL, GHOST e muito mais.

👉 Ideal para quem busca vantagem máxima e jogabilidade diferenciada no smartphone.

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)

    produtos = [
        {"nome": "PATO 1 DIA", "valor": "15,00", "id": "pato1"},
        {"nome": "PATO 3 DIAS", "valor": "30,00", "id": "pato3"},
        {"nome": "PATO 7 DIAS", "valor": "40,00", "id": "pato7"},
        {"nome": "PATO 15 DIAS", "valor": "60,00", "id": "pato15"},
        {"nome": "PATO 30 DIAS", "valor": "80,00", "id": "pato30"}
    ]

    async def clique(interaction: discord.Interaction):
        for p in produtos:
            if p["id"] == interaction.data["custom_id"]:
                await criar_carrinho(interaction, p["nome"], p["valor"])

    for p in produtos:
        btn = discord.ui.Button(label=f"{p['nome']} | R$ {p['valor']}", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id=p["id"])
        btn.callback = clique
        view.add_item(btn)

    await ctx.send(mensagem, view=view)


# 📶 COMANDO /PROXYANDROID
@bot.command(name='proxyandroid')
async def proxy_android(ctx):
    mensagem = """
📶 PROXY ANDROID

PROXY ANDROID*
BYPASS 100%
COMPRA DIAMANTE
FF NORMAL DA PLAY STORE
NAO PRECISA MEXER EM
METADATAS DO JOGO
OTIMO PARA APOSTADOS
NAO PRECISA DE PC OU ALGO
DO TIPO
FUNCIONANDO EM TODOS
ANDROID ACIMA DO 11

━━━━━━━━━━━━━━━━━━━━━━
🚀 **Selecione um Produto** 🚀
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="PROXY ANDROID 1 DIA | R$ 25,00", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="proxyand1")

    async def clique(interaction):
        await criar_carrinho(interaction, "PROXY ANDROID 1 DIA", "25,00")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 🛡️ COMANDO /BYPASS
@bot.command(name='bypass')
async def bypass_completo(ctx):
    mensagem = """
```-PACK PARA DAR BYPASS 100% NOS ADM 🤑```
```PACK VEM COM SUAS VANTAGENS COMO👇```

```-COMPRAR DIAMANTE 💎💎```

```-MUDAR AS INFORMAÇÕES DO APK MOD PARA "GOOGLE PLAY STORY" QUE CONSTA QUE FOI BAIXADO PELO PLAY STORE,FAZENDO COM QUE O ADM TENHA 0 DESCONFIANÇA!```

```-PASSA O REPLAY DO MOD APK PARA O FREE FIRE NORMAL✅```

```-SCRIPT 100% FUNCIONAL✅```


```-✅SEM NECESSIDADE DE PC,ROOT OU ALGO DO TIPO✅-```

━━━━━━━━━━━━━━━━━━━━━━
👉 **Selecione um Produto 👈**
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="BYPASS FULL ANDROID | R$ 15,00", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="bypass1")

    async def clique(interaction):
        await criar_carrinho(interaction, "BYPASS FULL ANDROID", "15,00")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 🩸 COMANDO /HSPESCOÇO
@bot.command(name='hspescoço')
async def hspescoço_completo(ctx):
    mensagem = """
HS PESCOÇO 🩸 | Produto

✅ FUNCIONA EM TODAS AS VERSÕES DO ANDROID DA XIAOMI!!
✅ SEM NECESSIDADE DE PC OU ROOT
✅ ENTREGA IMEDIATA
✅ NAO É FREE FIRE MODIFICADO
✅ VC RECEBE OS DOWNLOAD+TUTORIAL DE INSTALAÇÃO

💵 | Valor à vista: R$ 10,00
📦 | Restam: 9

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="HS PESCOÇO | R$ 10,00", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="hsp1")

    async def clique(interaction):
        await criar_carrinho(interaction, "HS PESCOÇO", "10,00")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 👻 COMANDO /HOLOGRAMA
@bot.command(name='holograma')
async def holograma_completo(ctx):
    mensagem = """
HOLOGRAMA 👻 | Produto

✅ HOLOGRAMA ANDROID
✅ GELO TRANSPARENTE
✅ ANTI-BAN E ANTI-BLACK
✅ TUTORIAL DE INSTALAÇÃO
✅ ACESSO PERMANENTE
✅ ANDROID 11 PRA CIMA
✅ SEM NECESSIDADE DE PC OU ROOT

💵 | Valor à vista: R$ 4,99
📦 | Restam: 100

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="HOLOGRAMA | R$ 4,99", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="holo1")

    async def clique(interaction):
        await criar_carrinho(interaction, "HOLOGRAMA", "4,99")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 👻 COMANDO /AUXÍLIO
@bot.command(name='auxílio')
async def auxilio_completo(ctx):
    mensagem = """
HOLOGRAMA + AUXÍLIO | Produto

✅ AUXÍLIO + HOLOGRAMA
✅ GELO TRANSPARENTE
✅ ANTI-BAN E ANTI-BLACK
✅ TUTORIAL DE INSTALAÇÃO
✅ NECESSITA DE SHIZUKO
✅ ACESSO PERMANENTE

💵 | Valor à vista: R$ 10,00
📦 | Restam: 147

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="HOLOGRAMA + AUXÍLIO | R$ 10,00", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="aux1")

    async def clique(interaction):
        await criar_carrinho(interaction, "HOLOGRAMA + AUXÍLIO", "10,00")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 💎 COMANDO /MANDELA
@bot.command(name='mandela')
async def mandela_completo(ctx):
    mensagem = """
TEXTURA DO MANDELA 💎 | Produto

✅ TEXTURA MANDELA
✅ SEM NECESSIDADE DE PC OU ROOT
✅ NAO É APK OU FF MODIFICADO
✅ SEM RISCO DE BAN OU BLACK
✅ FUNCIONA EM FF MAX E NORMAL
✅ ACESSO PERMANENTE

💵 | Valor à vista: R$ 8,00
📦 | Restam: 50

━━━━━━━━━━━━━━━━━━━━━━
🛒 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)
    btn = discord.ui.Button(label="TEXTURA MANDELA | R$ 8,00", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id="mandela1")

    async def clique(interaction):
        await criar_carrinho(interaction, "TEXTURA MANDELA", "8,00")

    btn.callback = clique
    view.add_item(btn)
    await ctx.send(mensagem, view=view)


# 🍏 COMANDO /PAINELIOS ✅ EXATO COMO VOCÊ QUER
@bot.command(name='painelios')
async def painelios_completo(ctx):
    mensagem = """
        
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

━━━━━━━━━━━━━━━━━━━━━━
📥 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)

    # ✅ PRODUTOS EXATOS DA SUA FOTO
    produtos = [
        {"nome": "PAINEL MONITE 1 DIA {BASIC}", "valor": "19,90", "id": "pmb1"},
        {"nome": "PAINEL MONITE 7 DIAS {BASIC}", "valor": "39,90", "id": "pmb7"},
        {"nome": "PAINEL MONITE 30 DIAS {BASIC}", "valor": "89,90", "id": "pmb30"},
        {"nome": "{SEPARADOR DE PRODUTOS}", "valor": "1,00", "id": "sep"},
        {"nome": "PAINEL MONITE 1 DIA {PRO}", "valor": "27,90", "id": "pmp1"},
        {"nome": "PAINEL MONITE 7 DIAS {PRO}", "valor": "59,90", "id": "pmp7"},
        {"nome": "PAINEL MONITE 30 DIAS {PRO}", "valor": "99,90", "id": "pmp30"}
    ]

    async def clique(interaction: discord.Interaction):
        for p in produtos:
            if p["id"] == interaction.data["custom_id"]:
                await criar_carrinho(interaction, p["nome"], p["valor"])

    for p in produtos:
        btn = discord.ui.Button(label=f"{p['nome']} | R$ {p['valor']}", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id=p["id"])
        btn.callback = clique
        view.add_item(btn)

    await ctx.send(mensagem, view=view)


# 🍏 COMANDO /PROXYIOS ✅ EXATO COMO VOCÊ QUER
@bot.command(name='proxyios')
async def proxyios_completo(ctx):
    mensagem = """
**🎯 HS ALTO IOS | 100% MOBILE**

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

* 🚀 **Performance**

━━━━━━━━━━━━━━━━━━━━━━
📥 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)

    # ✅ PRODUTOS EXATOS DA SUA FOTO
    produtos = [
        {"nome": "PROXY IOS 1 HORA", "valor": "2,00", "id": "px1h"},
        {"nome": "PROXY IOS 1 DIA", "valor": "6,00", "id": "px1d"},
        {"nome": "PROXY IOS 3 DIAS", "valor": "15,00", "id": "px3d"},
        {"nome": "PROXY IOS 7 DIAS", "valor": "22,00", "id": "px7d"},
        {"nome": "PROXY IOS 30 DIAS", "valor": "48,00", "id": "px30d"}
    ]

    async def clique(interaction: discord.Interaction):
        for p in produtos:
            if p["id"] == interaction.data["custom_id"]:
                await criar_carrinho(interaction, p["nome"], p["valor"])

    for p in produtos:
        btn = discord.ui.Button(label=f"{p['nome']} | R$ {p['valor']}", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id=p["id"])
        btn.callback = clique
        view.add_item(btn)

    await ctx.send(mensagem, view=view)


# 📦 COMANDO /CONTAS ✅ EXATO COMO VOCÊ QUER
@bot.command(name='contas')
async def contas_completo(ctx):
    mensagem = """
:ea1::ea2::ea3::ea4::ea5::ea6::ea7::ea8:
🔥 CONTA GUEST – PRONTA PRA USO IMEDIATO 🔥

💎 O QUE VOCÊ RECEBE:
✔ Conta 100% funcional
✔ Acesso completo (login + senha)
✔ Entrega imediata após a compra
✔ Segurança e exclusividade garantida

📊 CATEGORIAS DISPONÍVEIS:

🔹 NÍVEL 15 AO 19

🔹 NÍVEL 20 AO 29

🔹 NÍVEL 30+

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

━━━━━━━━━━━━━━━━━━━━━━
📥 **Selecione um Produto 👇**
    """
    view = discord.ui.View(timeout=None)

    # ✅ PRODUTOS EXATOS DA SUA FOTO
    produtos = [
        {"nome": "Contas Level 15", "valor": "0,85", "id": "c15"},
        {"nome": "CONTA NIVEL 20+", "valor": "3,00", "id": "c20"},
        {"nome": "Conta nível 30+", "valor": "5,30", "id": "c30"},
        {"nome": "Vincular conta Ios/Android", "valor": "3,00", "id": "vincular"}
    ]

    async def clique(interaction: discord.Interaction):
        for p in produtos:
            if p["id"] == interaction.data["custom_id"]:
                await criar_carrinho(interaction, p["nome"], p["valor"])

    for p in produtos:
        btn = discord.ui.Button(label=f"{p['nome']} | R$ {p['valor']}", style=discord.ButtonStyle.secondary, emoji="🛒", custom_id=p["id"])
        btn.callback = clique
        view.add_item(btn)

    await ctx.send(mensagem, view=view)


# 🔑 COLOQUE SEU TOKEN AQUI
bot.run(os.getenv("DISCORD_TOKEN"))
    
