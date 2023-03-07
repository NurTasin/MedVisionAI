from logger import *


class User:
    def __init__(self,id,name,token):
        self.id=id
        self.name=name
        self.token=token
        self.order_history=[]
        self.prescriptions=[]
    def ConstructFromObj(self,obj):
        try:
            self.id=obj["id"]
            self.ammount=obj["ammount"]
            self.sender=obj["sender"]
            self.order=order.Order(linked=obj["order"]["linked"],id=obj["order"]["OrderID"])
            self._time=obj["_time"]
        except KeyError as a:
            ERROR(a)
    
    def ConvertToObj(self):
        return {
            "id":self.id,
            "ammount":self.ammount,
            "sender":self.sender,
            "order":{
                "linked":self.order.linked,
                "id":self.order.id
            },
            "_time":self._time
        }