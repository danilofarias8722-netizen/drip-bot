import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs CONFIGURADOS
CATEGORIA_TICKET_ID = 1500253708980715712 # ID da sua categoria Ticket
DONO_ID = 1498844150202896446 # Seu ID pra receber ping
CARGO_STAFF_ID = 1399585507901575200 # ID do cargo staff

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="DÚVIDA", description="DÚVIDA COM ALGUM PRODUTO OU COMPRA", emoji="🔍"),
            discord.SelectOption(label="RESGATAR PRODUTO", description="RESGATE SEU PRODUTO AQUI", emoji="🎁"),
            discord.SelectOption(label="SUPORTE", description="SUPORTE COM ALGUM PRODUTO DA LOJA", emoji="🆘"),
            discord.SelectOption(label="QUERO SER REVENDEDOR", description="Tenha os requisitos para ser revendedor", emoji="🛒")
        ]
        super().__init__(placeholder="Clique aqui para ver as opções", options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        motivo = self.values[0]
        guild = interaction.guild
        categoria = guild.get_channel(CATEGORIA_TICKET_ID)
        cargo_staff = guild.get_role(CARGO_STAFF_ID)
        dono = guild.get_member(DONO_ID)

        # Verifica se já tem ticket aberto da pessoa
        for canal in guild.text_channels:
            if canal.topic and f"Ticket de {interaction.user.id}" in canal.topic:
                return await interaction.response.send_message(f"Você já tem um ticket aberto: {canal.mention}", ephemeral=True)

        # Conta quantos tickets já existem pra gerar o número
        numero_ticket = 1
        if categoria:
            tickets_existentes = [c for c in categoria.channels if c.name.startswith("ticket-")]
            numero_ticket = len(tickets_existentes) + 1
        else:
            tickets_existentes = [c for c in guild.text_channels if c.name.startswith("ticket-")]
            numero_ticket = len(tickets_existentes) + 1

        # Permissões do canal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            cargo_staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }
        if dono:
            overwrites[dono] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)

        # Cria o canal do ticket numerado
        canal_ticket = await guild.create_text_channel(
            name=f"ticket-{numero_ticket}",
            category=categoria,
            overwrites=overwrites,
            topic=f"Ticket de {interaction.user.id} | Motivo: {motivo} | Autor: {interaction.user.name}"
        )

        embed_ticket = discord.Embed(
            title=f"Ticket #{numero_ticket} - {motivo}",
            description=f"Olá {interaction.user.mention}\n\nDescreva seu problema com o máximo de detalhes.",
            color=0x2B2D31
        )
        embed_ticket.set_footer(text="Para fechar o ticket clique no botão abaixo")

        # Manda ping pra você e pro cargo da staff
        await canal_ticket.send(content=f"{interaction.user.mention} <@{DONO_ID}> <@&{CARGO_STAFF_ID}>", embed=embed_ticket, view=FecharTicketView())
        await interaction.response.send_message(f"Ticket criado em {canal_ticket.mention}", ephemeral=True)

class FecharTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="fechar_ticket")
    async def fechar(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Fechando ticket em 5 segundos...")
        await interaction.channel.delete(delay=5)

class PainelTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    embed = discord.Embed(
        title="Central de atendimento dnzx store",
        description="Após solicitar um atendimento, aguarde um integrante da equipe responde-lo(a). O atendimento é realizado de forma privada, contudo, somente integrantes da equipe terá acesso ao atendimento. Tenha ciência que a nossa equipe não se encontra presente 24 horas por dia, contudo, dentro dos horários citados acima nossa equipe se encontra disponibilizada a atende-lo(a).",
        color=0x2B2D31
    )
    embed.set_footer(text="Selecione uma opção abaixo para abrir um ticket")

    await ctx.send(embed=embed, view=PainelTicketView())
    await ctx.message.delete()

@bot.event
async def on_ready():
    bot.add_view(PainelTicketView())
    bot.add_view(FecharTicketView())
    print("Sistema de ticket online")

bot.run(os.getenv("DISCORD_TOKEN"))
