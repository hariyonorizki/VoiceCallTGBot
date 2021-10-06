#!/usr/bin/env python3
# Copyright (C) @HariyonoRizki2

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument
from plugins.controls import is_admin
from pyrogram import Client, filters
from utils import update, is_admin
from config import Config
from logger import LOGGER
import os

HOME_TEXT = "<b>Hai  [{}](tg://user?id={}) 🙋‍♂️\n\nAku Adalah Bot yang Berfungsi Untuk Memainkan dan Stream Video di Telegram Voice Chat.\nAku Bisa Stream Video YouTube, Telegram File bahkan YouTube Live.</b>"
admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton('Update Channel', url='https://t.me/kitgbotz'),
            InlineKeyboardButton('Source Code', url='https://github.com/HariyonoRizki2/VoiceCallTGBot')
        ],
        [
            InlineKeyboardButton('Bantuan', callback_data='help'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    buttons = [
        [
            InlineKeyboardButton('Update Channel', url='https://t.me/kitgbotz'),
            InlineKeyboardButton('Source Code', url='https://github.com/HariyonoRizki2/VoiceCallTGBot'),
        ]
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        Config.HELP,
        reply_markup=reply_markup
        )
@Client.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton('Repository', url='https://github.com/HariyonoRizki2/VoiceCallTGBot'),
            InlineKeyboardButton('Update Channel', url='https://t.me/kitgbotz'),
            
        ],
    ]
    await message.reply("<b>Source Code Bot Ini Publik, Dan Dapat Ditemukan di <a href=https://github.com/HariyonoRizki2/VoiceCallTGBot>VoiceCallTGBot.</a>\nKamu Dapat Membuat Botmu Sendiri dan gunakan di Grubmu.\n\nJangan Lupa Kasih Stars☀️ Ke Repo Ini Jika Kamu Menyukainya🙃.</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    await message.reply("Updating and restarting the bot.")
    await update()

@Client.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="Bot Logs"))
    if logs:
        await message.reply_media_group(logs)
        logs.clear()
    else:
        await message.reply("No log files found.")
