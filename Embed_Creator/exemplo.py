import discord
from discord.ext import commands
import asyncio
from Embed_Creator import EmbedCreator

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Estou online!')
	
@bot.command()
async def embed(ctx):
    """Gerador de Embed com a Embed Padrão e Autor Check, então apenas o invoker pode usar o editor"""
    view = EmbedCreator(bot=bot)
    async def check(interaction: discord.Interaction): # se não quiser autor check, remova esse bloco
        if interaction.user.id == ctx.author.id:
            return True
        else:
            await interaction.response.send_message(f"Apenas {ctx.author} pode usar essa interação!", ephemeral=True)
            return False
    view.interaction_check = check # isso também
    await ctx.send(embed=view.get_default_embed, view=view)

async def main():
	await bot.start('SEU TOKEN AQUI') # substitua pelo seu token

asyncio.run(main())