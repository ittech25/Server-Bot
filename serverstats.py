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
chdir = []
stopmarkup = {'keyboard': [['Stop']]}
hide_keyboard = {'hide_keyboard': True}

def clearsemua(chat_id):
    if chat_id in shellexecution:
        shellexecution.remove(chat_id)
    if chat_id in chdir:
        chdir.remove(chat_id)
#function ini digunakan untuk melakukan monitoring performa layanan menggunakan library psutil
#this function is made for monitor performance and service in server
def monitor_performance(chat_id):
    memory = psutil.virtual_memory()
    bootTime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    cpuPercent = psutil.cpu_percent()
    serverOnline = "Server online salama : %.1f jam" % (((now - bootTime).total_seconds()) / 3600)
    memTotal = "Total memory ram : %.2f GB " % (memory.total / 1000000000)
    memAvail = "Memory ram yang tersedia : %.2f MB" % (memory.available / 1000000)
    memUse = "Memory ram yang dipakai : " + str(memory.percent) + " %"
    cpuUse = "Ultilisasi cpu sebanyak : "+ str(cpuPercent) + "%"
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
    sortedProcs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedProcs:
        pidsreply += proc[0]  +  "\n"
    reply = serverOnline  + "\n" + \
            cpuUse + "\n" + \
            memTotal + "\n" + \
            memAvail + "\n" + \
            memUse + "\n\nService yang sedang berjalan : \n" + \
            pidsreply
    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)
#this function is not used
def forwardEmail():
    if os.stat("/var/mail/root").st_size == 0:
        pass
    else:
        for adminchatid2 in adminchatid:
            p = subprocess.Popen(['tail', '/var/mail/root'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            bot.sendMessage(adminchatid2,out)
        open('/var/mail/root','w').close()


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
                    monitor_performance(chat_id)
                elif msg['text'] == 'Stop':
                    clearsemua(chat_id)
                    bot.sendMessage(chat_id, "hentikan semua operasi" ,  reply_markup=hide_keyboard)
                elif msg['text'] == '/shell' and chat_id  not in shellexecution:
                    bot.sendMessage(chat_id, "masukan perintah atau command " , reply_markup=stopmarkup)
                    shellexecution.append(chat_id)
                elif msg['text'] == '/chdir':
                    bot.sendMessage(chat_id,"masukan nama direktori" , reply_markup=stopmarkup)
                    chdir.append(chat_id)
                elif chat_id in chdir:
                    p = str(msg['text'])
                    if os.path.isdir(p) == 1:
                        os.chdir(p)
                        bot.sendMessage(chat_id,"direktori telah diganti ke"+p ,reply_markup=hide_keyboard)
                        clearsemua(chat_id)
                    else:
                        bot.sendMessage(chat_id,"tidak ada direktori")
                elif chat_id in shellexecution:
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
bot = BotPcr(TOKEN)
bot.message_loop()
while 1:
    time.sleep(0.2)
