#!/usr/bin/env python3
# Copyright (C) @HariyonoRizki2

from utils import get_buttons, is_admin, get_playlist_str, shuffle_playlist, import_play_list
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from logger import LOGGER
import json
import os

admin_filter=filters.create(is_admin)   


@Client.on_message(filters.command(["export", f"export@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def export_play_list(client, message: Message):
    if not Config.playlist:
        await message.reply_text("Playlist Kosong")
        return
    file=f"{message.chat.id}_{message.message_id}.json"
    with open(file, 'w+') as outfile:
        json.dump(Config.playlist, outfile, indent=4)
    await client.send_document(chat_id=message.chat.id, document=file, file_name="PlayList.json", caption=f"Playlist\n\nNomor Urut Lagu: <code>{len(Config.playlist)}</code>\n\nJoin [KITGBOTZ](https://t.me/kitgbotz)")
    try:
        os.remove(file)
    except:
        pass

@Client.on_message(filters.command(["import", f"import@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def import_playlist(client, m: Message):
    if m.reply_to_message is not None and m.reply_to_message.document:
        if m.reply_to_message.document.file_name != "PlayList.json":
            k=await m.reply("Playlist Invalid. Gunakan @GetPlayListBot untuk Mendapatkan File Playlist. Atau Export Playlistmu Sebelumnya Menggunakan /export.")
            return
        myplaylist=await m.reply_to_message.download()
        status=await m.reply("Mencoba Mendapatkan Detail dari Playlist.")
        n=await import_play_list(myplaylist)
        if not n:
            await status.edit("Terjadi Error saat Export Playlist.")
            return
        if Config.SHUFFLE:
            await shuffle_playlist()
        pl=await get_playlist_str()
        if m.chat.type == "private":
            await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())        
        elif not Config.LOG_GROUP and m.chat.type == "supergroup":
            await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        else:
            await status.delete()
    else:
        await m.reply("Playlist Tidak ada Isinya. Gunakan @GetPlayListBot  atau cari playlist di @DumpPlaylist untuk mendapatkan file playlist.")
