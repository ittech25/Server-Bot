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
        print("User chat id :" +str(chat_id))
        if chat_id in adminchatid:
            performanceResult = monitorPerformance(chat_id)
            if content_type == 'text':
                if msg['text'] == '/status' and chat_id not in shellExecution:
                    bot.sendMessage(chat_id, performanceResult, disable_web_page_preview=True)
                elif msg['text'] == 'stop':
                    clearAll(chat_id)
                    bot.sendMessage(chat_id, "Stop all operation" ,  reply_markup=hide_keyboard)
                elif msg['text'] == '/shell' and chat_id  not in shellExecution:
                    bot.sendMessage(chat_id, "Enter shell command" , reply_markup=stopmarkup)
                    shellExecution.append(chat_id)
                elif msg['text'] == '/chdir':
                    bot.sendMessage(chat_id,"Enter direcotry name " , reply_markup=stopmarkup)
                    changeDirectory .append(chat_id)
                elif chat_id in changeDirectory :
                    p = str(msg['text'])
                    if os.path.isdir(p) == 1:
                        os.chdir (p)
                        bot.sendMessage(chat_id,"Directory is change into "+p ,reply_markup=hide_keyboard)
                        clearAll(chat_id)
                    else:
                        bot.sendMessage(chat_id,"Dir is not available")
                elif chat_id in shellExecution:
                    p = Popen(msg['text'].lower() , shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output != b'':
                        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
                    else:
                        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)
        else:
            bot.sendMessage(chat_id, "This user dont have the permission")



TOKEN = telegrambot
bot = ServerBot(TOKEN)
bot.message_loop()
while 1:
    time.sleep(0.2)
