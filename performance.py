import psutil

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