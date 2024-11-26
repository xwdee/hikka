from .. import loader, utils

class DelmeMod(loader.Module):
    """Удаляет все сообщения в группе"""
    strings = {'name': 'ClearAll'}

    @loader.sudo
    async def delmecmd(self, message):
        """Удаляет все сообщения в группе"""
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id + message.sender_id):
                await message.edit(f"<b>Если ты точно хочешь удалить все сообщения в группе, то напиши:</b>\n<code>.delme {message.chat.id + message.sender_id}</code>")
                return
            await delete_all_messages(chat, message, True)
        else:
            await message.edit("<b>В лс не чищу!</b>")

async def delete_all_messages(chat, message, now):
    if now:
        all_messages = await message.client.get_messages(chat)
        all_message_count = len(all_messages)
        await message.edit(f"<b>Будет удалено {all_message_count} сообщений!</b>")
    else:
        await message.delete()

    async for msg in message.client.iter_messages(chat):
        if msg.sender_id != message.sender_id:
            await msg.delete()
    await message.delete() if now else "хули мусара хули мусара хули, едем так как ехали даже в хуй не дули"
