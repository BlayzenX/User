# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
from random import choice

AFKSTR = [
    "Şu an acele işim var, daha sonra mesaj atsan olmaz mı? Zaten yine geleceğim.",
    "Aradığınız kişi şu anda telefona cevap veremiyor. Sinyal sesinden sonra kendi tarifeniz üzerinden mesajınızı bırakabilirsiniz. Mesaj ücreti 49 kuruştur. \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Birkaç dakika içinde geleceğim. Fakat gelmezsem...\ndaha fazla bekle.",
    "Şu an burada değilim, muhtemelen başka bir yerdeyim.",
    "Güller kırmızı\nMenekşeler mavi\nBana bir mesaj bırak\nVe sana döneceğim.",
    "Bazen hayattaki en iyi şeyler beklemeye değer…\nHemen dönerim.",
    "Hemen dönerim,\nama eğer geri dönmezsem,\ndaha sonra dönerim.",
    "Henüz anlamadıysan,\nburada değilim.",
    "Merhaba, uzak mesajıma hoş geldiniz, bugün sizi nasıl görmezden gelebilirim?",
    "7 deniz ve 7 ülkeden uzaktayım,\n7 su ve 7 kıta,\n7 dağ ve 7 tepe,\n7 ovala ve 7 höyük,\n7 havuz ve 7 göl,\n7 bahar ve 7 çayır,\n7 şehir ve 7 mahalle,\n7 blok ve 7 ev...\n\nMesajların bile bana ulaşamayacağı bir yer!",
    "Şu anda klavyeden uzaktayım, ama ekranınızda yeterince yüksek sesle çığlık atarsanız, sizi duyabilirim.",
    "Şu yönde ilerliyorum\n---->",
    "Şu yönde ilerliyorum\n<----",
    "Lütfen mesaj bırakın ve beni zaten olduğumdan daha önemli hissettirin.",
    "Sahibim burada değil, bu yüzden bana yazmayı bırak.",
    "Burada olsaydım,\nSana nerede olduğumu söylerdim.\n\nAma ben değilim,\ngeri döndüğümde bana sor...",
    "Uzaklardayım!\nNe zaman dönerim bilmiyorum !\nUmarım birkaç dakika sonra!",
    "Sahibim şuan da müsait değil. Adınızı, numarınızı ve adresinizi verirseniz ona iletibilirm ve böylelikle geri döndüğü zaman.",
    "Üzgünüm, sahibim burada değil.\nO gelene kadar benimle konuşabilirsiniz.\nSahibim size sonra döner.",
    "Bahse girerim bir mesaj bekliyordun!",
    "Hayat çok kısa, yapacak çok şey var...\nOnlardan birini yapıyorum...",
    "Şu an burada değilim....\nama öyleysem ...\n\nbu harika olmaz mıydı?",
]

UNAPPROVED_MSG = ("`Hey! Bu bir bot. Endişelenme.\n\n`"
                  "`Sahibim sana PM atma izni vermedi. `"
                  "`Lütfen sahibimin aktif olmasını bekleyin, o genellikle PM'leri onaylar.\n\n`"
                  "`Bildiğim kadarıyla o kafayı yemiş insanlara PM izni vermiyor.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Girilen telefon numarası geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()
try:
    bot.start()
    idim = bot.get_me().id
    asenabl = requests.get('https://gitlab.com/Quiec/asen/-/raw/master/asen.json').json()
    if idim in asenabl:
        bot.disconnect()
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`Tanrı Türk'ü Korusun. 🐺 Asena çalışıyor.`", "afk": str(choice(AFKSTR)), "kickme": "Güle Güle ben gidiyorum 🤠", "pm": UNAPPROVED_MSG}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            PLUGIN_MESAJLAR[mesaj] = dmsj

    if PLUGIN_CHANNEL_ID != None:
        print("Pluginler Yükleniyor")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Plugin_Channel_Id'iniz geçersiz. Pluginler kalıcı olmuyacak.`")
            DOGRU = 0

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if DOGRU == 0:
                break
            dosyaa = plugin.file.name
            print(dosyaa)
            if not os.path.exists(os.getcwd() + "/userbot/modules/" + dosyaa):
                dosya = bot.download_media(plugin, os.getcwd() + "/userbot/modules/")
            else:
                print("Bu Plugin Zaten Yüklü " + dosyaa)
                dosya = dosyaa
                break
            try:
                spec = importlib.util.spec_from_file_location(dosya, dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                bot.send_message(KanalId, f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")
                plugin.delete()

                if os.path.exists("/userbot/modules/" + dosya):
                  os.remove(os.getcwd() + "/userbot/modules/" + dosya)
                continue
            
            ndosya = dosya.replace(".py", "")
            CMD_HELP[ndosya] = "Bu Plugin Dışarıdan Yüklenmiştir"
            bot.send_message(KanalId, f"`Plugin Yüklendi\n\Dosya: {dosya}`")
        if KanalId != "me":
            bot.send_message(KanalId, f"`Pluginler Yüklendi`")
    else:
        bot.send_message("me", f"`Lütfen pluginlerin kalıcı olması için PLUGIN_CHANNEL_ID'i ayarlayın.`")

except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz çalışıyor! Herhangi bir sohbete .alive yazarak Test edin."
          " Yardıma ihtiyacınız varsa, Destek grubumuza gelin t.me/AsenaSupport")
LOGS.info("Bot sürümünüz Asena v1.4")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
