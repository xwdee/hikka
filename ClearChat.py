from .. import loader, utils

class ClearChatMod(loader.Module):
    """Видаляє всі повідомлення в чаті"""

    strings = {"name": "ClearChat"}

    @loader.sudo
    async def delallcmd(self, message):
        """Видаляє всі повідомлення в чаті"""
        chat = message.chat
        if chat:
            await self.delete_all(chat, message)
        else:
            await message.edit("<b>В лс не чищу!</b>")

    async def delete_all(self, chat, message):
        all_msgs = (await message.client.get_messages(chat)).total
        await message.edit(f"<b>{all_msgs} повідомлень буде видалено!</b>")
        async for msg in message.client.iter_messages(chat):
            await msg.delete()
        await message.delete()
