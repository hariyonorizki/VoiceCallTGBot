#!/usr/bin/env python3
# Copyright (C) @HariyonoRizki2

from utils import get_playlist_str, get_admins, is_admin, restart_playout, skip, pause, resume, volume, get_buttons, is_admin
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from logger import LOGGER

admin_filter=filters.create(is_admin)   

@Client.on_message(filters.command(["player", f"player@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT) | filters.private))
async def player(client, message):
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('playlist') is not None:
            await Config.msg['playlist'].delete()
        Config.msg['playlist'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=await get_buttons()
        )

@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def skip_track(_, m: Message):
    if not Config.playlist:
        await m.reply("Playlist Kosong.\nLive Streaming.")
        return
    if len(m.command) == 1:
        await skip()
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    Config.playlist.pop(i)
                    await m.reply(f"Berhasil Menghapus dari Playlist- {i}. **{Config.playlist[i][1]}**")
                else:
                    await m.reply(f"Kamu Tidak Dapat Melawati Dua lagu Awal- {i}")
        except (ValueError, TypeError):
            await m.reply_text("Invalid input")
    pl=await get_playlist_str()
    if m.chat.type == "private":
        await m.reply_text(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        await m.reply_text(pl, disable_web_page_preview=True, reply_markup=await get_buttons())

@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def pause_playing(_, m: Message):
    if Config.PAUSE:
        return await m.reply("Telah Terjeda")
    if not Config.CALL_STATUS:
        return await m.reply("Tidak Memutar Apapun.")
    await m.reply("Voice Call Terjeda")
    await pause()
    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def resume_playing(_, m: Message):
    if not Config.PAUSE:
        return await m.reply("Tidak ada Yang Terjeda untuk Dilanjutkan")
    if not Config.CALL_STATUS:
        return await m.reply("Tidak Memutar Apapun.")
    await m.reply("Voice Call Dilanjutkan")
    await resume()
    


@Client.on_message(filters.command(['volume', f"volume@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        return await m.reply("Tidak Memutar Apapun.")
    if len(m.command) < 2:
        await m.reply_text('kamu lupa menyetel volume (1-200).')
        return
    await m.reply_text(f"Volume diatur menjadi {m.command[1]}")
    await volume(int(m.command[1]))
    

@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & (filters.chat(Config.CHAT) | filters.private))
async def replay_playout(client, m: Message):
    if not Config.CALL_STATUS:
        return await m.reply("Tidak Memutar Apapun.")
    await m.reply_text(f"Mengulang Dari Awal")
    await restart_playout()
