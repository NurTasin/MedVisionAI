import requests as req
import os

class LCD:
    def __init__(self,ip:str) -> None:
        if not ip.startswith("http://"):
            ip="http://"+ip
        
        if ip.endswith("/"):
            ip=ip[::-1]
        self._ip=ip
        self._paired=False
        self._msg=(None,None)
    
    @property
    def ip(self):
        return self._ip
    
    @ip.setter
    def ip(self,val):
        self._ip=val
    
    @property
    def paired(self):
        return self._paired
    
    @property
    def screenBuff(self):
        return self._msg
    
    def pair(self):
        res=req.post(self.ip,data={
            "id":os.getenv("USER")
        })
        if res.status_code==200:
            self._paired=True
            return True
        else:
            print(f"LCD @ {self.ip} says `{res.text}`")
            self._paired=False
            return False
    
    def unpair(self):
        res=req.post(self.ip+"/disconnect",data={
            "id":os.getenv("USER")
        })
        if res.status_code==200:
            self._paired=False
            self._msg=(None,None)
            return True
        else:
            print(f"LCD @ {self.ip} says `{res.text}`")
            return False
    
    def print(self,line1="",line2=""):
        res=req.post(self.ip+"/print",data={
            "message1":str(line1),
            "message2":str(line2),
            "id":os.getenv("USER")
        })
        if res.status_code==200:
            self._msg=(str(line1),str(line2))
            return True
        else:
            print(f"LCD @ {self.ip}  says `{res.text}`")
            return False
    
    def scroll(self,line1="",line2=""):
        res=req.post(self.ip+"/scroll",data={
            "message1":line1,
            "message2":line2,
            "id":os.getenv("USER")
        })
        if res.status_code==200:
            self._msg=(line1,line2)
            return True
        else:
            print(res.text)
            return False
    
    def printFormatted(self,string):
        m1=""
        m2=""
        if len(string)>16:
            m1=string[0:16]
            m2=string[16::]
            return self.print(m1,m2)
        else:
            return self.print(string,"")
    
    def scrollFormatted(self,string1,scroll_1,string2,scroll_2):
        res=req.post(self.ip+"/scroll2",data={
            "message1":string1,
            "message2":string2,
            "scroll_1":"1" if scroll_1 else "0",
            "scroll_2":"1" if scroll_2 else "0",
            "id":os.getenv("USER")
        })
        if res.status_code == 200:
            self._msg=(string1,string2)
            return True
        else:
            print(f"[LCD] @ {self.ip} says `{res.text}`")
            return False

if __name__=="__main__":
    Display=LCD(str(input("IP: ")))
    while True:
        cmd=input("[LCD]$ ")
        if cmd.startswith("pair"):
            Display.pair()
        elif cmd.lower().startswith("print "):
            if cmd[len("print ")::].strip()=="":
                Display.print("","")
            elif "#$#" in cmd[len("print ")::]:
                splitted=cmd[len("print ")::].split("#$#")
                Display.print(splitted[0],splitted[1])
            else:
                Display.print(cmd[len("print ")::],"")
        elif cmd.lower().startswith("printf "):
            Display.printFormatted(cmd[len("printf ")::])
        elif cmd.lower().startswith("scroll "):
            if cmd[len("scroll ")::].strip()=="":
                Display.scroll("","")
            if "#$#" in cmd[len("scroll ")::]:
                splitted=cmd[len("scroll ")::].split("#$#")
                Display.scroll(splitted[0],splitted[1])
            else:
                Display.scroll(cmd[len("scroll ")::],"")
        elif cmd.lower().startswith("unpair"):
            Display.unpair()
        elif cmd.lower().startswith("exit"):
            break