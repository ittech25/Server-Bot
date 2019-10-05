from tokens import *
from subprocess import Popen, PIPE, STDOUT,call
import collections
import time
import telepot
import subprocess
import os
from performance import monitorPerformance

shellExecution = []
changeDirectory = []
stopmarkup = {'keyboard': [['Stop']]}
hide_keyboard = {'hide_keyboard': True}

def clearAll(chat_id):
    if chat_id in shellExecution:
        shellExecution.remove(chat_id)
    if chat_id in changeDirectory :
        changeDirectory .remove(chat_id)


class ServerBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(ServerBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None


    def on_chat_message(self , msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print("Chat id admin :" +str(chat_id))
        if chat_id in adminchatid:
            performanceResult = monitorPerformance(chat_id)
            if content_type == 'text':
                if msg['text'] == '/stats' and chat_id not in shellExecution:
                    bot.sendMessage(chat_id, performanceResult, disable_web_page_preview=True)
                elif msg['text'] == 'Stop':
                    clearAll(chat_id)
                    bot.sendMessage(chat_id, "hentikan semua operasi" ,  reply_markup=hide_keyboard)
                elif msg['text'] == '/shell' and chat_id  not in shellExecution:
                    bot.sendMessage(chat_id, "masukan perintah atau command " , reply_markup=stopmarkup)
                    shellExecution.append(chat_id)
                elif msg['text'] == '/changeDirectory ':
                    bot.sendMessage(chat_id,"masukan nama direktori" , reply_markup=stopmarkup)
                    changeDirectory .append(chat_id)
                elif chat_id in changeDirectory :
                    p = str(msg['text'])
                    if os.path.isdir(p) == 1:
                        os.chdir (p)
                        bot.sendMessage(chat_id,"direktori telah diganti ke"+p ,reply_markup=hide_keyboard)
                        clearAll(chat_id)
                    else:
                        bot.sendMessage(chat_id,"tidak ada direktori")
                elif chat_id in shellExecution:
                    p = Popen(msg['text'] , shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output != b'':
                        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
                    else:
                        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)
                elif msg['text'] == '/reboot':
                    p = subprocess.Popen(['reboot'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    out,err = p.communicate()
                    bot.sendMessage(chat_id,"server akan di reboot")
                elif msg['text'] == '/shutdown':
                    p = subprocess.Popen(['shutdown','now'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    matikan = p.communicate()
                    bot.sendMessage(chat_id,"server akan segera dimatikan")
        else:
            bot.sendMessage(chat_id, "user ini bukan admin")



TOKEN = telegrambot
bot = ServerBot(TOKEN)
bot.message_loop()
while 1:
    time.sleep(0.2)
