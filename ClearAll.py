from .. import loader, utils

class ClearAllMod(loader.Module):
    """Очищає всі повідомлення в чаті"""
    strings = {'name': 'ClearAll'}

    @loader.sudo
    async def clearallcmd(self, message):
        """Очищає всі повідомлення в чаті"""
        chat = message.chat
        if not chat:
            await message.edit("<b>Я не можу чистити лс!</b>")
            return

        confirmation_code = str(chat.id + message.sender_id)
        args = utils.get_args_raw(message)

        if args != confirmation_code:
            await message.edit(
                f"<b>Якщо ти впевнений у своїх діях, введи:</b>\n"
                f"<code>.clearall {confirmation_code}</code>"
            )
            return

        total_deleted = 0
        async for msg in message.client.iter_messages(chat, from_user="me"):
            await msg.delete()
            total_deleted += 1

        await message.client.delete_dialog(chat.id)
        await message.respond(f"<b>Видалено {total_deleted} повідомлень і закрито чат!</b>")
