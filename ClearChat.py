from .. import loader, utils

class ClearAllMod(loader.Module):
    """Удаляет все сообщения в группе"""
    strings = {'name': 'ClearChat'}

    @loader.sudo
    async def clearallcmd(self, message):
        """Удаляет все сообщения в группе"""
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id + message.sender_id):
                await message.edit(f"<b>Для продолжения, напиши следующее</b>\n<code>clearall {message.chat.id + message.sender_id}</code>")
                return
            await delete_all_messages(chat, message, True)
        else:
            await message.edit("<b>В лс не чищу!</b>")

async def delete_all_messages(chat, message, now):
    if now:
        all_messages = await message.client.get_messages(chat)
        await message.edit(f"<b>Начался процес очистки....</b>")
    else:
        await message.delete()

    async for msg in message.client.iter_messages(chat):
        try:
            await msg.delete()
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    await message.delete() if now else None
