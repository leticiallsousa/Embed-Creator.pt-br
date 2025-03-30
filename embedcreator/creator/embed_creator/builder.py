from __future__ import annotations
from typing import Optional, Any
from discord import ButtonStyle, CategoryChannel, Embed, ForumChannel, HTTPException, Interaction, StageChannel, Colour, SelectOption
from discord.ext.commands import Bot
from discord.ui import Item, Select, select, Button, button, View
from creator.embed_creator.methods import CreatorMethods
from creator.input import ChannelSelectPrompt

__all__ = ("EmbedCreator")

class EmbedCreator(View):
    """
    Essa classe é uma subclasse de `discord.ui.View`.
    Destina-se a ser usada como uma classe base para criar um painel que permite os usuários criarem embeds em um canal Discord TextChannel especificado. 

    Parâmetros:
        bot (discord.Client ou discord.ext.commands.Bot): Uma instância do bot do Discord que vai ser usada para acessar informações do cliente como avatar, nome e ID. 
        embed (discord.Embed): Uma instância do discord.Embed que vai ser usada como embed principal.
        timeout (float, optional): Um argumento opcional que é passado para a classe mãe View. É usado para especificar um timeout para a view, em segundos.
    """

    def __init__(
        self,
        *,
        bot: Bot,
        embed: Optional[Embed] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(timeout=timeout)
        if not embed:
            embed = self.get_default_embed
        self.bot, self.embed, self.timeout, self._creator_methods = (
            bot,
            embed,
            timeout,
            CreatorMethods(embed),
        )
        self.options_data = [
            {
                "label": kwargs.get("author_label", "Edite o Autor"),
                "description": kwargs.get(
                    "author_description", "Edita o nome e ícone do autor."
                ),
                "emoji": kwargs.get("author_emoji", "🔹"),
                "value": "author",
            },
            {
                "label": kwargs.get(
                    "message_label", "Edite a Mensagem (título e descrição)"
                ),
                "description": kwargs.get(
                    "message_description", "Edita o título e descrição da embed."
                ),
                "emoji": kwargs.get("message_emoji", "🔹"),
                "value": "message",
            },
            {
                "label": kwargs.get("thumbnail_label", "Edite a Thumbnail"),
                "description": kwargs.get(
                    "thumbnail_description", "Edita a thumbnail da embed."
                ),
                "emoji": kwargs.get("thumbnail_emoji", "🔹"),
                "value": "thumbnail",
            },
            {
                "label": kwargs.get("image_label", "Edite a Imagem"),
                "description": kwargs.get(
                    "image_description", "Edita a imagem da embed."
                ),
                "emoji": kwargs.get("image_emoji", "🔹"),
                "value": "image",
            },
            {
                "label": kwargs.get("footer_label", "Edite o Rodapé"),
                "description": kwargs.get(
                    "footer_description", "Edita o texto e o ícone do rodapé da embed."
                ),
                "emoji": kwargs.get("footer_emoji", "🔹"),
                "value": "footer",
            },
            {
                "label": kwargs.get("color_label", "Edite a Cor"),
                "description": kwargs.get(
                    "color_description", "Edita a cor da embed."
                ),
                "emoji": kwargs.get("color_emoji", "🔹"),
                "value": "color",
            },
            {
                "label": kwargs.get("addfield_label", "Adicione um campo"),
                "description": kwargs.get(
                    "addfield_description", "Adiciona um campo à embed."
                ),
                "emoji": kwargs.get("addfield_emoji", "🔹"),
                "value": "addfield",
            },
            {
                "label": kwargs.get("removefield_label", "Remova um campo"),
                "description": kwargs.get(
                    "removefield_description", "Remove um campo da embed."
                ),
                "emoji": kwargs.get("removefield_emoji", "🔹"),
                "value": "removefield",
            },
        ]

        self.children[0].options = [SelectOption(  # type: ignore
            **option) for option in self.options_data
        ]
        self.children[1].label, self.children[1].emoji, self.children[1].style = kwargs.get(  # type: ignore
            "send_label", 'Enviar'), kwargs.get("send_emoji", None), kwargs.get("send_style", ButtonStyle.blurple)
        self.children[2].label, self.children[2].emoji, self.children[2].style = kwargs.get(  # type: ignore
            "cancel_label", 'Cancelar'), kwargs.get("cancel_emoji", None), kwargs.get("cancel_style", ButtonStyle.red)  # type: ignore

    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any]) -> None:
        if isinstance(error, HTTPException) and error.code == 50035: # erro de url
            await interaction.followup.send('Por favor, insira um URL válido', ephemeral=True)

    async def update_embed(self, interaction: Interaction):
        """Essa função vai atualizar a embed inteira e editar a mensagem e view."""
        return await interaction.message.edit(embed=self.embed, view=self)  # type: ignore

    @property
    def get_default_embed(self) -> Embed:
        """
        Esse método de classe `get_default_embed` returna um objeto `discord.Embed` pré-configurado com título, descrição, cor, autor, thumbnail, imagem e rodapé já definidos com valores específicos.
        Ele pode ser usado como um modelo padrão para criar o Embed Builder.

        Retorna:
            embed (discord.Embed)
        """
        embed = Embed(title='Isso é um título',
                      description="Use o menu de seleção para editar minhas seções", colour=Colour.from_str('#070d2d'))
        embed.set_author(name='Bem-vindo ao Embed Builder.',
                         icon_url="https://i.imgur.com/8Zx1lLv.gif")
        embed.set_thumbnail(
            url="https://i.imgur.com/hARDXOC.png")
        embed.set_image(
            url="https://i.imgur.com/g1eBpIP.png")
        embed.set_footer(
            text='Isso é um rodapé', icon_url="https://i.imgur.com/8Zx1lLv.gif")
        return embed

    @select(placeholder="Edite uma seção")
    async def edit_select_callback(
        self, interaction: Interaction, select: Select
    ) -> None:
        """
        Esse método é uma função callback da interação `select`.
        Ele é invocado quando um usuário seleciona uma opção do menu de seleção. 
        O método usa o atributo `callbacks` da classe `CreatorMethods` para chamar a função callback apropriada baseada na seleção do usuário.

        Parâmetros:
            interaction (discord.Interaction): O objeto "interaction" representando a interação atual.
            select (discord.Select): O objeto "select" representando o menu de seleção.
        """
        await self._creator_methods.callbacks[select.values[0]](interaction)
        await self.update_embed(interaction)

    @button()
    async def send_callback(self, interaction: Interaction, button: Button) -> None:
        """
        Esse método é uma função callback para a intereração `button`. Ele é invocado quando o usuário clica no botão "Enviar".
        O método cria um objeto `ChannelSelectPrompt` e envia ele como uma mensagem ephemeral para o usuário. E então ele espera o usuário selecionar um chat.
        Se um chat é selecionado, o método envia a embed para o chat selecionado e então deleta a mensagem de interação original.

        Parâmetros:
            interaction (discord.Interaction): O objeto "interaction" representando a interação atual.
            button (discord.Button): O objeto "button" representando o botão "Enviar".
        """
        prompt = ChannelSelectPrompt(
            "Selecione um chat para enviar essa embed...", True, 1)
        await interaction.response.send_message(view=prompt, ephemeral=True)
        await prompt.wait()
        if prompt.values:
            if not isinstance(prompt.values[0], (StageChannel, ForumChannel, CategoryChannel)):
                await prompt.values[0].send(embed=self.embed)  # type: ignore
                await interaction.message.delete()  # type: ignore

    @button()
    async def cancel_callback(self, interaction: Interaction, button: Button) -> None:
        """
        Esse método é uma função callback para a interação `button`. Ele é invocado quando um usuário clica no botão "Cancelar".
        O método deleta a mensagem de interação original e finaliza a interação atual.

        Parâmetros:
            interaction (Interaction): O objeto "interaction" representando a interação atual.
            button (Button): O objeto "button" representando o botão "Cancelar".
        """
        await interaction.message.delete()  # type: ignore
        self.stop()
