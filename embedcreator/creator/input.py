from __future__ import annotations
from typing import List, Optional
from discord.ui import ChannelSelect, Modal, Select, View, select
from discord import Interaction, SelectOption, ChannelType
from contextlib import suppress

__all__ = ("ModalInput", "SelectPrompt", "ChannelSelectPrompt")

class ModalInput(Modal):
    """
    Essa classe é uma subclasse da classe `Modal` que deve ser usada como uma classe base para a criação de modals que requerem uma entrada do usuário.

    Parâmetros:
        title (str): O título do modal.
        timeout (float, optional): Um argumento opcional que é passado para a classe mãe Modal. Ele é usado para especificar um timeout para o mosal, em segundos.
        custom_id (str, optional): Um argumento opcional que é passado para a classe mãe Moda. Ele é usado para especificar um ID personalizado para o modal.
        ephemeral (bool, optional): Um indicador booleano de que o modal será ou não enviado como uma mensagem ephemeral.
    """
    def __init__(
        self,
        *,
        title: str,
        timeout: Optional[float] = None,
        custom_id: str = "modal_input",
        ephemeral: bool = False,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.ephemeral = ephemeral

    async def on_submit(self, interaction: Interaction) -> None:
        with suppress(Exception):
            await interaction.response.defer(ephemeral=self.ephemeral)


class SelectPrompt(View):
    """
    Essa classe é uma subclasse da classe `View` que deve ser usada como uma classe base para a criação de um prompt de seleção.

    Parâmetros:
        placeholder (str): O texto placeholder que vai ser exibido no prompt de seleção.
        options (List[SelectOption]): Uma lista de instâncias de `SelectOption` que vão ser exibidas como opções no prompt de seleção.
        max_values (int, optional): O número máximo de seleções que podem ser selecionadas pelo usuário. Por padrão é 1.
        ephemeral (bool, optional): Um indicador booleano de que o prompt selecionado será ou não enviado como uma mensagem ephemeral. Por padrão é False.
    """
    def __init__(
        self, placeholder: str, options: List[SelectOption], max_values: int = 1, ephemeral: bool = False
    ) -> None:
        super().__init__()
        self.children[0].placeholder, self.children[0].max_values, self.children[0].options = placeholder, max_values, options  # type: ignore
        self.values = None
        self.ephemeral = ephemeral

    @select()
    async def select_callback(self, interaction: Interaction, select: Select):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = select.values
        self.stop()

class ChannelSelectPrompt(View):
    """
    Essa classe é uma subclasse da classe `View` que deve ser usada como uma classe base para a criação de um prompt de seleção de chat.

    Parâmetros:
        placeholder (str): O texto placeholer que vai ser exibido no prompt de seleção de chat.
        ephemeral (bool, optional): Um indicador booleano de que o prompt de seleção será ou não enviado como uma mensagem ephemeral. Por padrão é False.
        max_values (int, optional): O número máximo de opções que podem ser selecionadas pelo usuário. Por padrão é 1.
    """
    def __init__(
        self, placeholder: str, ephemeral: bool = False, max_values: int = 1
    ) -> None:
        super().__init__()
        self.values = None
        self.ephemeral = ephemeral
        self.children[0].placeholder, self.children[0].max_values = placeholder, max_values# type: ignore

    @select(cls=ChannelSelect, channel_types=[ChannelType.text, ChannelType.private_thread, ChannelType.public_thread, ChannelType.news])
    async def callback(self, interaction: Interaction, select: ChannelSelect):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = [interaction.guild.get_channel(i.id) for i in select.values] # type: ignore
        self.stop()
        