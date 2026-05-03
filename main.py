import discord
from discord.ui import View, Button, Select
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ID DO CARGO DONO JÁ CONFIGURADO
CARGO_STAFF_ID = 1500251010461863977

@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')

@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="📨 Abrir Ticket",
        description="Selecione uma opção abaixo para abrir um ticket com a equipe.",
        color=discord.Color.blue()
    )

    select = Select(
        placeholder="Escolha o tipo de ticket",
        options=[
            discord.SelectOption(label="Suporte", description="Tirar dúvidas", emoji="❓"),
            discord.SelectOption(label="Compra", description="Problemas com compra", emoji="🛒"),
            discord.SelectOption(label="Denúncia", description="Denunciar usuário", emoji="🚨")
        ],
        custom_id="abrir_ticket_select"
    )

    view = View()
    view.add_item(select)
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:

        if interaction.data["custom_id"] == "abrir_ticket_select":
            categoria = interaction.data["values"][0]

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.get_role(CARGO_STAFF_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
            }

            canal = await interaction.guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites=overwrites,
                reason=f"Ticket aberto por {interaction.user}"
            )

            view = View()
            view.add_item(Button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="fechar_ticket"))

            embed = discord.Embed(
                title=f"Ticket - {categoria}",
                description=f"Olá {interaction.user.mention}, explique seu problema.\nA equipe já foi notificada.",
                color=discord.Color.green()
            )

            await canal.send(embed=embed, view=view)
            await interaction.response.send_message(f"Ticket criado em {canal.mention}", ephemeral=True)

        elif interaction.data["custom_id"] == "fechar_ticket":
            await interaction.response.defer()

            try:
                await interaction.channel.send("Fechando ticket em 5 segundos...")
                await asyncio.sleep(5)
                await interaction.channel.delete(reason=f"Ticket fechado por {interaction.user}")

            except discord.Forbidden:
                await interaction.followup.send(
                    "**❌ ERRO: Sem permissão pra apagar canal!**\n"
                    "1. O cargo `DnzX lá casa mods` tem que estar no TOPO da lista de cargos\n"
                    "2. Ativa `Administrador` nas perms do cargo do bot\n"
                    "3. Testa com um ticket NOVO",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.followup.send(f"**❌ Erro:** `{e}`", ephemeral=True)

bot.run("SEU_TOKEN_AQUI")
