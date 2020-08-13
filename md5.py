import threading, queue
import hashlib
import sys
from time import sleep

q = queue.Queue()
dowork = True
file_hash = hashlib.md5()
if not len(sys.argv) > 1:
    print ("You must provide an input file")
    sys.exit(1)

def filereader():
    global dowork
    global q
    try:
        with open(sys.argv[1], "rb") as f:
            while chunk := f.read(8192000):
                #print ("put to q ")
                q.put(chunk)
                #todo check if q is full
                while q.qsize() >  100:
                    sleep(0.2)
                    #print ("Sleep")
            
            dowork = False

    except KeyboardInterrupt:
        sys.exit(1)
    except:
        print("An exception occurred reading the provided " )
        sys.exit(1)
        
def hashthread():
    global dowork
    global q
    try:
        while (q.empty()):
            #print ("waiting for q to fill")
            sleep(0.1)
            continue
        while dowork:
            #print ("getting q")
            chunk = q.get()
            if chunk:
                #print ("getting q 1")
                file_hash.update(chunk)
        #TODO: read last chunks from q
        while q.qsize() > 0:
            #print ("last chunks " + str(q.qsize()))
            chunk = q.get()
            file_hash.update(chunk)
            
        q.task_done()
    except KeyboardInterrupt:
        raise

    
    
t1 = threading.Thread(target=hashthread)
t2 = threading.Thread(target=filereader)    
t1.start()
t2.start()
t1.join()
t2.join()

print(file_hash.hexdigest())  # to get a printable str instead of bytes

