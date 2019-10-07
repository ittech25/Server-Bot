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
stopMarkup = {'keyboard': [['stop']]}
hide_keyboard = {'hide_keyboard': True}

#function to exit shell and change directory menu
def clearAll(chat_id):
    if chat_id in shellExecution:
        shellExecution.remove(chat_id)
    if chat_id in changeDirectory :
        changeDirectory .remove(chat_id)


#Function to change directory
def changeDir(message,chat_id):
    p = str(message)
    if os.path.isdir(p) == 1:
        os.chdir(p)
        bot.sendMessage(chat_id,"Directory is change into "+p ,reply_markup=hide_keyboard)
        clearAll(chat_id)
    else:
        bot.sendMessage(chat_id,"Dir is not available")


#Function to enter a shell command
def shellCommand(message,chat_id):
    p = Popen(message.lower() , shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if output != b'':
        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
    else:
        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)


#main class of bot
class ServerBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(ServerBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None


    def on_chat_message(self , msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        performanceResult = monitorPerformance(chat_id)
        print("User chat id :" +str(chat_id))
        if chat_id in adminchatid:
            if content_type == 'text':
                if msg['text'] == '/status' and chat_id not in shellExecution:
                    bot.sendMessage(chat_id, performanceResult, disable_web_page_preview=True)
                elif msg['text'] == 'stop':
                    clearAll(chat_id)
                    bot.sendMessage(chat_id, "Stop all operation" ,  reply_markup=hide_keyboard)
                elif msg['text'] == '/shell' and chat_id  not in shellExecution:
                    bot.sendMessage(chat_id, "Enter shell command" , reply_markup=stopMarkup)
                    shellExecution.append(chat_id)
                elif msg['text'] == '/changedir':
                    bot.sendMessage(chat_id,"Enter directory name " , reply_markup=stopMarkup)
                    changeDirectory .append(chat_id)
                elif chat_id in changeDirectory :
                    changeDir(msg['text'],chat_id)
                elif chat_id in shellExecution:
                    shellCommand(msg['text'],chat_id)     
        else:
            bot.sendMessage(chat_id, "This user dont have the permission")


TOKEN = telegrambot
bot = ServerBot(TOKEN)
bot.message_loop()
while 1:
    time.sleep(0.2)
