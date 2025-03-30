# ![Imagem do projeto](https://i.imgur.com/xqZZrC6.png)
<p align="center">Uma biblioteca em discord.py para a criação de embeds personalizadas no Discord, através de uma interface interativa, simples e intuitiva ao usuário</p>

<!-- <p>Fazer tabela de conteúdos</p> -->

## Instalando
Instale a versão estável (Recomendado)
```bash 
pip install embedcreator
```
Instale a versão de desenvolvimento
```bash
pip install git+https://github.com/leticiallsousa/Embed-Creator.pt-br
```

<p>Exemplo de implementação:</p>

```python
@bot.command()
async def embed(ctx):
    """Gerador de Embed com a Embed Padrão e Autor Check, então apenas o invoker pode usar o editor"""
    view = EmbedCreator(bot=bot)
    async def check(interaction: discord.Interaction):
        if interaction.user.id == ctx.author.id:
            return True
        else:
            await interaction.response.send_message(f"Apenas {ctx.author} pode usar essa interação!", ephemeral=True)
            return False
    view.interaction_check = check
    await ctx.send(embed=view.get_default_embed, view=view)
```

<!-- <p>Adicionar tecnologias, funções autores e no final:</p> -->
<p>Este software é uma modificação e tradução ao português do projeto Dispie, criado originalmente por <a href=”https://github.com/pranoymajumdar”>Pranoy Majumdar</a></p>
