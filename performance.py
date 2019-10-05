import psutil
import operator
from datetime import datetime

def sortedProcs(pids):
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.4:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("Process is not available")
    sortedProcs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedProcs:
        pidsreply += proc[0]  +  "\n"
    return pidsreply
    

def monitorPerformance(chat_id):
    memory = psutil.virtual_memory()
    bootTime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    cpuPercent = psutil.cpu_percent()
    serverOnline = "Server Online : %.1f Hours" % (((now - bootTime).total_seconds()) / 3600)
    memTotal = "Server RAM Memory : %.2f GB " % (memory.total / 1000000000)
    memAvail = "Available RAM : %.2f MB" % (memory.available / 1000000)
    memUse = "RAM used : " + str(memory.percent) + " %"
    cpuUse = "CPU usage : "+ str(cpuPercent) + "%"
    allPid = psutil.pids()
    sortedProcsResult = sortedProcs(allPid)
    
    reply = serverOnline  + "\n" + \
            cpuUse + "\n" + \
            memTotal + "\n" + \
            memAvail + "\n" + \
            memUse + "\n\n Running Services: \n" + \
            sortedProcsResult
    
    return reply
    # bot.sendMessage(chat_id, reply, disable_web_page_preview=True)