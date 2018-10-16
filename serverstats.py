from tokens import *
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import operator
import collections
# import sys
import time
# import threading
# import random
import telepot

shellexecution = []

stopmarkup = {'keyboard': [['Stop']]}
hide_keyboard = {'hide_keyboard': True}

class BotPcr(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(BotPcr, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

    def on_chat_message(self , msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print("Chat id admin :" +str(chat_id))
        if chat_id in adminchatid:
            if content_type == 'text':
                if msg['text'] == '/stats' and chat_id not in shellexecution:
                    memory = psutil.virtual_memory()
                    boottime = datetime.fromtimestamp(psutil.boot_time())
                    now = datetime.now()
                    cpu_percent = psutil.cpu_percent() *10
                    timedif = "Server online salama : %.1f jam" % (((now - boottime).total_seconds()) / 3600)
                    memtotal = "Total memory ram : %.2f GB " % (memory.total / 1000000000)
                    memavail = "Memory ram yang tersedia : %.2f GB" % (memory.available / 1000000000)
                    memuseperc = "Memory ram yang dipakai : " + str(memory.percent) + " %"
                    cpu_used = "Ultilisasi cpu sebanyak : "+ str(cpu_percent) + "%"
                    pids = psutil.pids()
                    pidsreply = ''
                    procs = {}
                    for pid in pids:
                        p = psutil.Process(pid)
                        try:
                            pmem = p.memory_percent()
                            if pmem > 0.5:
                                if p.name() in procs:
                                    procs[p.name()] += pmem
                                else:
                                    procs[p.name()] = pmem
                        except:
                            print("Do Nothing")
                    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
                    for proc in sortedprocs:
                        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
                    reply = timedif  + "\n" + \
                            cpu_used + "\n" + \
                            memtotal + "\n" + \
                            memavail + "\n" + \
                            memuseperc + "\n\nService yang sedang berjalan : \n" + \
                            pidsreply
                    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)




TOKEN = telegrambot
bot = BotPcr(TOKEN)
bot.message_loop()

while 1:
    time.sleep(10)
