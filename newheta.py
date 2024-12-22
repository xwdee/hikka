import aiohttp
import asyncio
from bs4 import BeautifulSoup
from difflib import get_close_matches
from telethon.tl.types import DocumentAttributeFilename
from .. import loader, utils
import os
import re

@loader.tds
class RecursiveFileDownloaderMod(loader.Module):
    """Придумал: @artm1r  && Создал: ChatGPT
    Модуль для быстрого поиска и скачивания файлов с сайта heta.dan.tatar с поддержкой кэша и исправления опечаток"""
    strings = {"name": "NewHeta"}

    BASE_URL = "https://heta.dan.tatar/"
    MAX_DEPTH = 3  # Максимальная глубина рекурсии
    MODULES_PER_PAGE = 15  # Количество модулей на одной странице
    folder_cache = {}  # Кэш для хранения структуры папок и файлов

    async def client_ready(self, client, db):
        self.client = client

    async def updatecachecmd(self, message):
        """Использование: .updatecache — Обновление кэша всех папок и файлов"""
        await message.edit("<b>Обновление списка папок и модулей...</b>")
        try:
            self.folder_cache = await self.build_folder_cache(self.BASE_URL, depth=0)
            await message.edit("<b>Кэш успешно обновлен!</b>")
        except Exception as e:
            await message.edit(f"<b>Ошибка при обновлении кэша: {str(e)}</b>")

    async def build_folder_cache(self, url, depth):
        """Рекурсивный обход сайта для обновления кэша всех папок и файлов"""
        folder_cache = {}

        if depth > self.MAX_DEPTH:  # Ограничиваем глубину рекурсии
            return folder_cache

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return folder_cache

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    tasks = []
                    for link in soup.find_all('a'):
                        href = link.get('href')

                        if not href or href in ['/', '../']:  # Игнорируем корневые и предыдущие ссылки
                            continue

                        # Если это .py файл
                        if href.endswith('.py'):
                            file_url = os.path.join(url, href)
                            filename = href.split("/")[-1]
                            author = url.split('/')[-2]  # Получаем имя автора (главная папка)

                            if filename not in folder_cache:
                                folder_cache[filename] = {"urls": [file_url], "author": author}
                            else:
                                folder_cache[filename]["urls"].append(file_url)

                        # Если это папка, идем внутрь
                        if href.endswith('/'):
                            new_url = os.path.join(url, href)
                            tasks.append(self.build_folder_cache(new_url, depth + 1))

                    # Запускаем параллельно все задачи по обходу папок
                    results = await asyncio.gather(*tasks)

                    # Объединяем результаты
                    for result in results:
                        folder_cache.update(result)

            return folder_cache
        except Exception as e:
            print(f"Ошибка при построении кэша: {str(e)}")
            return folder_cache

    async def modulecmd(self, message):
        """Использование: .module <имя файла> — Поиск и отправка модуля"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите имя модуля для поиска.</b>")
            return

        if not self.folder_cache:
            await message.edit("<b>Кэш пуст. Пожалуйста, выполните команду .updatecache для обновления кэша.</b>")
            return

        # Попробуем найти точное совпадение
        if args in self.folder_cache:
            file_urls = self.folder_cache[args]["urls"]
            await self.send_files(message, args, file_urls)
        else:
            # Попробуем найти похожие имена файлов (исправление опечаток)
            close_matches = get_close_matches(args, self.folder_cache.keys(), n=3, cutoff=0.6)
            if close_matches:
                file_urls = self.folder_cache[close_matches[0]]["urls"]
                await self.send_files(message, close_matches[0], file_urls, match_info=close_matches[0])
            else:
                await message.edit(f"<b>Модуль с именем '{args}' не найден.</b>")

    async def send_files(self, message, filename, file_urls, match_info=None):
        """Отправка файлов в чат с указанием пути и правильным расширением"""
        match_text = f"Найдено ближайшее совпадение: {match_info}\n" if match_info else ""
        
        for file_url in file_urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(file_url) as response:
                        if response.status == 200:
                            file_content = await response.read()
                            file_name = file_url.split('/')[-1]

                            # Проверка расширения .py
                            if not file_name.endswith(".py"):
                                file_name += ".py"

                            # Отправляем файл с указанием правильного имени и расширения
                            await self.client.send_file(
                                entity=message.peer_id,
                                file=bytes(file_content),
                                caption=f"<b>NewHeta</b>\n{match_text}\nПуть: {file_url}",
                                reply_to=message.id,
                                force_document=True,
                                attributes=[DocumentAttributeFilename(file_name)]  # Указание правильного имени файла
                            )
                        else:
                            await message.edit(f"<b>Не удалось загрузить файл по ссылке: {file_url}</b>")
            except Exception as e:
                await message.edit(f"<b>Ошибка при загрузке файла: {str(e)}</b>")

    async def folderscmd(self, message):
        """Использование: .folders <имя папки> — Получение списка файлов из указанной папки"""
        args = utils.get_args_raw(message)

        if not args:
            # Если аргументы не указаны, покажем список главных папок
            main_folders = set(url.split('/')[3] for url_list in self.folder_cache.values() for url in url_list["urls"])
            folders_list = "\n".join(f"📁 {folder}" for folder in sorted(main_folders))
            await message.edit(f"<b>Главные папки:</b>\n\n{folders_list}")
        else:
            # Поиск файлов в указанной папке
            folder_name = args.strip()
            matching_files = {
                filename: data for filename, data in self.folder_cache.items()
                if any(f"/{folder_name}/" in url for url in data["urls"])
            }

            if matching_files:
                files_list = "\n".join(f"📄 {filename}" for filename in sorted(matching_files.keys()))
                await message.edit(f"<b>Модули в папке '{folder_name}':</b>\n\n{files_list}")
            else:
                await message.edit(f"<b>Папка '{folder_name}' не найдена или пуста.</b>")

    async def listcmd(self, message):
        """Использование: .list <номер страницы> — Просмотр списка модулей по страницам"""
        args = utils.get_args_raw(message)
        page = int(args) if args.isdigit() else 1

        if not self.folder_cache:
            await message.edit("<b>Кэш пуст. Пожалуйста, выполните команду .updatecache для обновления кэша.</b>")
            return

        modules = sorted(self.folder_cache.items())  # Сортировка модулей по алфавиту
        total_pages = (len(modules) + self.MODULES_PER_PAGE - 1) // self.MODULES_PER_PAGE

        if page > total_pages or page < 1:
            await message.edit(f"<b>Страницы {page} не существует. Всего страниц: {total_pages}</b>")
            return

        start_idx = (page - 1) * self.MODULES_PER_PAGE
        end_idx = start_idx + self.MODULES_PER_PAGE
        modules_on_page = modules[start_idx:end_idx]

        list_message = f"<b>Список модулей (страница {page}/{total_pages}):</b>\n\n"
        for filename, data in modules_on_page:
            author = data["author"]
            list_message += f"📄 <b>{filename}</b> (Автор: {author})\n"

        sent_message = await message.edit(list_message)

        # Удаление сообщения через минуту
        await asyncio.sleep(60)
        await sent_message.delete()