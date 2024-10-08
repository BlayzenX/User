# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Lost UserBot - Mustafa Usta


""" Birkaç küçük komutu içeren UserBot modülü. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import io
import sys
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("misc")

# ████████████████████████████████ #

ASKSHUTDOWN2 = "n"
ASKSHUTDOWN1 = "n"

@register(outgoing=True, disable_edited=True)
async def txt(msg):
    global ASKSHUTDOWN2 
    if ASKSHUTDOWN2 == "y":
        message = msg.raw_text
        user_id = msg.sender.id
        if (message == "y" or message == "Y") and user_id == msg.sender.id:
            await msg.client.send_file(msg.chat_id, 'https://www.winhistory.de/more/winstart/mp3/winxpshutdown.mp3', caption=LANG['GOODBYE_MFRS'], voice_note=True)
            await msg.delete()

            if BOTLOG:
                await msg.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                            "Bot kapatıldı.")
            try:
                await bot.disconnect()
            except:
                pass
        else: 
            ASKSHUTDOWN = False
            ASKSHUTDOWN2 = "n"
            return await msg.edit("**Kapatma İşlemi Durduruldu!**")
    else:
        return True

@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    """ .shutdown komutu botu kapatır. """
    global ASKSHUTDOWN2 
    ASKSHUTDOWN2 = "y"
    await event.edit("**Dikkat Bu İşlem Geri Döndürülemez**\n**Userbot'u Kapatmak İçin** `Y` **Yazın.**")



@register(outgoing=True, pattern="^.resend")
async def resend(event):
    await event.delete()
    m = await event.get_reply_message()
    if not m:
        event.edit(LANG['REPLY_TO_FILE'])
        return
    await event.respond(m)

@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ .random komutu, eşya listesinden rastgele bir eşya seçer. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            LANG['NEED_MUCH_DATA_FOR_RANDOM']
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(f"**{LANG['QUERY']}: **\n`" + items.text[8:] + f"`\n**{LANG['RESULT']}: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ .sleep komutu Lost'nın birkaç saniye uyumasına olanak sağlar. """
    if " " not in time.pattern_match.group(1):
        await time.reply(LANG['SLEEP_DESC'])
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit(LANG['SLEEPING'])
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Botu" + str(counter) + "saniye uykuya bıraktın.",
            )
        await sleep(counter)
        await time.edit(LANG['GOODMORNIN_YALL'])


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit(LANG['RESTARTING'])
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot yeniden başlatıldı.")

    try:
        await bot.disconnect()
    except:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ .support komutu destek grubumuzu verir. """
    await wannahelp.edit(LANG['SUPPORT_GROUP'])


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit(LANG['CREATOR'])


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit(LANG['CREATOR'])


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ .repo komutunun tek yaptığı şey GitHub repomuzun bağlantısını vermek. """
    await wannasee.edit(LANG['REPO'])

@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Çözülmüş mesaj için userbot loglarını kontrol et!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Çözülen mesaj`")

CmdHelp('misc').add_command(
    'random', '<eşya1> <eşya2> ... <eşyaN>', 'Eşya listesinden rastgele bir eşya seçer', 'random Lost uniborg userge'
).add_command(
    'sleep', '<süre>', 'Lost de bir insan, o da yoruluyor. Ara sıra biraz uyumasına izin ver.', 'sleep 30'
).add_command(
    'shutdown', None, 'Nostaljik bir şekilde botunuzu kapatın.'
).add_command(
    'repo', None, 'Lost botunun GitHub\'daki reposuna giden bir bağlantı.'
).add_command(
    'readme', None, 'Lost botunun GitHub\'daki README.md dosyasına giden bir bağlantı.'
).add_command(
    'creator', None, 'Bu güzel botu kimlerin oluşturduğunu öğren :-)'
).add_command(
    'repeat', '<sayı> <metin>', 'Bir metni belli bir sayıda tekrar eder. Spam komutu ile karıştırma!'
).add_command(
    'restart', None, 'Botu yeniden başlatır.'
).add_command(
    'resend', None, 'Bir medyayı yeniden gönderir.'
).add_command(
    'resend', None, 'Bir medyayı yeniden gönderir.'
).add_command(
    'raw', '<yanıt>', 'Yanıt verilen mesaj hakkında bilgi verir.'
).add()