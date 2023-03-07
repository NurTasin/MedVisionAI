import colorama

def log__(type,msg):
    if type=="err":
        print(colorama.Fore.RED+"[ERROR] "+colorama.Fore.RESET+str(msg))
    if type=="info":
        print(colorama.Fore.BLUE+"[INFO] "+colorama.Fore.RESET+str(msg))
    if type=="log":
        print(colorama.Fore.YELLOW+"[LOG] "+colorama.Fore.RESET+str(msg))

def INFO(msg):
    log__("info",msg)

def ERROR(msg):
    log__("err",msg)

def LOG(msg):
    log__("log",msg)