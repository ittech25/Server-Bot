from tokens import *
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT,call
import operator
import collections
import time
import telepot
import subprocess
import os

shellexecution = []

stopmarkup = {'keyboard': [['Stop']]}
hide_keyboard = {'hide_keyboard': True}

def clearsemua(chat_id):
    if chat_id in shellexecution:
        shellexecution.remove(chat_id)


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
                    #memangka = "Memory ram yang dipakai : %.2f GB" % (memory.used / 1000000000)
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
                        pidsreply += proc[0]  +  "\n"
                    reply = timedif  + "\n" + \
                            cpu_used + "\n" + \
                            memtotal + "\n" + \
                            memavail + "\n" + \
                            memuseperc + "\n\nService yang sedang berjalan : \n" + \
                            pidsreply
                    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)
                elif msg['text'] == 'Stop':
                    clearsemua(chat_id)
                    bot.sendMessage(chat_id, "hentikan operasi shell" ,  reply_markup=hide_keyboard)
                elif msg['text'] == '/shell' and chat_id  not in shellexecution:
                    bot.sendMessage(chat_id, "masukan perintah atau command " , reply_markup=stopmarkup)
                    shellexecution.append(chat_id)
                elif chat_id in shellexecution:
                    p = Popen(msg['text'] , shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output != b'':
                        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
                    else:
                        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)
                elif msg['text'] == '/mail':
                    while True:
                        if os.stat("mail").st_size == 0:
                            pass
                        else:
                            p = subprocess.Popen(['tail', '/home/tronic/serverbot/mail'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                            out, err = p.communicate()
                            bot.sendMessage(chat_id,out)
                            open('mail','w').close()
        else:
            bot.sendMessage(chat_id, "user ini bukan admin")



TOKEN = telegrambot
bot = BotPcr(TOKEN)
bot.message_loop()

while 1:
    time.sleep(1)
