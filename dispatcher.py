import ftpHandler
import downloader

import multiprocessing as mp
import time
import sys
import re
import traceback


StartFile = 1
EndFile = 365
NUM_OF_PROCESS = 200

def downloadPerFolder(workQueue, endQueue):
    pattern = re.compile("\.Z$")
    ftps = ftpHandler.connectFTP_TLS()
    while True:
        time.sleep(1)
        fileDir = workQueue.get()
        try:
            fileList = ftps.nlst(fileDir)
            startTime = time.time()
            for filename in fileList:
                if(pattern.search(filename)==None):
                    continue
                print('Downloading '+filename)
                downloader.downloadFile(filename, ftps)
            deltaTime = time.time() - startTime
            print(fileDir + ' Done in ' + str(deltaTime) + ' seconds')
            endQueue.get()
        except (KeyboardInterrupt, SystemError):
            raise
        except:
            workQueue.put(fileDir)
            print ("Unexpected error: ")

            print(str(sys.exc_info()[0]))
            print(str(sys.exc_info()[1]))
            print(str(sys.exc_info()[2]))
            print(traceback.format_exc())

            print('some error on ' + fileDir)


    # ftps.storbinary('STOR gnss/products/ionex/2020/256/esrg2560.20i.Z', )
    # print(ftps.retrbinary('RETR gnss/products/ionex/2020/256/esrg2560.20i.Z', callback_nop))

    # filename = "gnss/products/ionex/2020/256/esrg2560.20i.Z"

def printMpQueue(mpQueue):
    normalQueue = []
    while(mpQueue.empty() is False):
        normalQueue.append(mpQueue.get())
    print(normalQueue)
    while(normalQueue):
        mpQueue.put(normalQueue.pop(0))
for year in range(2016, 2018):
    # baseDir = 'gnss/products/ionex/2018/'
    baseDir = 'gnss/products/ionex/' + str(year) + '/'
    # input filename to mp.Queue
    workQueue = mp.Queue()
    endQueue = mp.Queue()
    for i in range (StartFile, EndFile+1):
        workQueue.put(baseDir + "{:03d}".format(i))
        endQueue.put(1)

    processes = []
    for i in range (1, NUM_OF_PROCESS+1):
        process = mp.Process(target=downloadPerFolder, args=(workQueue, endQueue,))
        processes.append(process)
        process.start()
    while True:
        time.sleep(10)
        printMpQueue(workQueue)
        # printMpQueue(endQueue) # why this thing break the thing?
        print('endqueue size: ' + str(endQueue.qsize()))
        if(endQueue.empty() is True):
            break
    for process in processes:
        process.terminate()
