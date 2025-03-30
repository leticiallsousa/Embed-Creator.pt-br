from __future__ import annotations
from typing import Callable, Dict
from creator.input import ModalInput, SelectPrompt
from discord import Colour, Embed, HTTPException, Interaction, SelectOption, TextStyle
from discord.ui import TextInput

__all__ = ("CreatorMethods")

class CreatorMethods:
    """
    Essa classe contém todos os métodos para editar uma embed. Destina-se a ser herdado pela classe principal `EmbedCreator`.

    Atributos:
        embed (discord.Embed): O objeto da embed a ser editado.

    """

    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail,
            "image": self.edit_image,
            "footer": self.edit_footer,
            "color": self.edit_colour,
            "addfield": self.add_field,
            "removefield": self.remove_field,
        }


    async def edit_author(self, interaction: Interaction) -> None:
        """Esse método edita o autor da embed"""
        modal = ModalInput(title="Edite o autor da embed")
        modal.add_item(
            TextInput(
                label="Nome do autor",
                max_length=100,
                default=self.embed.author.name,
                placeholder="Nome do autor para ser mostrado na embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Url do ícone do autor",
                default=self.embed.author.icon_url,
                placeholder="Ícone do autor para ser mostrado na embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Url do autor",
                default=self.embed.author.url,
                placeholder="URL para definir como o link do autor da embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            self.embed.set_author(
                name=str(modal.children[0]),
                icon_url=str(modal.children[1]),
                url=str(modal.children[2]),
            )
        except HTTPException:
            self.embed.set_author(
                name=str(modal.children[0])
            )

    async def edit_message(self, interaction: Interaction) -> None:
        """Esse método edita a mensagem da embed (discord.Embed.title e discord.Embed.description)"""
        modal = ModalInput(title="Edite a mensagem da embed")
        modal.add_item(
            TextInput(
                label="Título da embed",
                max_length=255,
                default=self.embed.title,
                placeholder="Título para ser mostrado na embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Descrição da embed",
                default=self.embed.description,
                placeholder="Descrição para ser mostrada na embed",
                style=TextStyle.paragraph,
                required=False,
                max_length=2000,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.title, self.embed.description = str(modal.children[0]), str(
            modal.children[1]
        )

    async def edit_thumbnail(self, interaction: Interaction) -> None:
        """Esse método edita a thumbnail da embed"""
        modal = ModalInput(title="Edite a thumbnail da embed")
        modal.add_item(
            TextInput(
                label="Url da thumbnail",
                default=self.embed.thumbnail.url,
                placeholder="Thumbnail para ser mostrada na embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_thumbnail(url=str(modal.children[0]))

    async def edit_image(self, interaction: Interaction) -> None:
        """Esse método edita a imagem da embed"""
        modal = ModalInput(title="Edite a imagem da embed")
        modal.add_item(
            TextInput(
                label="Url da imagem",
                default=self.embed.image.url,
                placeholder="Imagem para ser mostrada na embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_image(url=str(modal.children[0]))

    async def edit_footer(self, interaction: Interaction) -> None:
        """Esse método edita o rodapé da embed (text, icon_url)"""
        modal = ModalInput(title="Edite o rodapé da embed")
        modal.add_item(
            TextInput(
                label="Texto do rodapé",
                max_length=255,
                required=False,
                default=self.embed.footer.text,
                placeholder="Texto para ser mostrado no rodapé da embed",
            )
        )
        modal.add_item(
            TextInput(
                label="Ícone do rodapé",
                required=False,
                default=self.embed.footer.icon_url,
                placeholder="Ícone para ser mostrado no rodapé da embed",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_footer(
            text=str(modal.children[0]), icon_url=str(modal.children[1])
        )

    async def edit_colour(self, interaction: Interaction) -> None:
        """Esse método edita a cor da embed"""
        modal = ModalInput(title="Edite a cor da embed")
        modal.add_item(
            TextInput(
                label="Cor da embed",
                placeholder="Cor para ser mostrada na embed (ex: #070d2d)",
                max_length=20
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            colour = Colour.from_str(str(modal.children[0]))
        except:
            await interaction.followup.send(
                "Por favor, informe um código HEX válido.", ephemeral=True
            )
        else:
            self.embed.color = colour

    async def add_field(self, interaction: Interaction) -> None:
        if len(self.embed.fields) >= 25:
            return await interaction.response.send_message(
                "Você não pode adicionar mais que 25 campos.", ephemeral=True
            )
        modal = ModalInput(title="Adicionar novo campo")
        modal.add_item(
            TextInput(
                label="Nome do campo",
                placeholder="Nome para ser mostrado no campo",
                max_length=255,
            )
        )
        modal.add_item(
            TextInput(label="Valor do campo", 
                      placeholder='Valor para ser mostrado no campo',
                      max_length=2000, 
                      style=TextStyle.paragraph)
        )
        modal.add_item(
            TextInput(
                label="Campos na mesma linha (True/False)",
                default="True",
                max_length=5,
                placeholder="Os campos ficarão na mesma linha? (True ou False)"),
            )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            inline = False
            if str(modal.children[2]).lower() == "true":
                inline = True
            elif str(modal.children[2]).lower() == "false":
                inline = False
            else:
                raise Exception("Resposta inválida.")
        except:
            await interaction.followup.send(
                "Por favor, informe uma opção válida em `campos na mesma linha`: ou True ou False.",
                ephemeral=True,
            )
        else:
            self.embed.add_field(
                name=str(modal.children[0]), value=str(modal.children[1]), inline=inline
            )

    async def remove_field(self, interaction: Interaction) -> None:
        if not self.embed.fields:
            return await interaction.response.send_message("Não há campos para serem removidos", ephemeral=True)
        field_options = list()
        for index, field in enumerate(self.embed.fields):
            field_options.append(
                SelectOption(
                    label=str(field.name)[0:30],
                    value=str(index),
                    emoji="\U0001f5d1"
                )
            )
        select = SelectPrompt(
            placeholder="Selecione um campo para a remoção...",
            options=field_options,
            max_values=len(field_options),
            ephemeral=True
        )
        await interaction.response.send_message(view=select, ephemeral=True)
        await select.wait()
        
        if vals := select.values:
            for value in vals:
                self.embed.remove_field(int(value))