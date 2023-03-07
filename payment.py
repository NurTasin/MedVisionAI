import uuid
import order
from logger import *

class Payment:
    def __init__(self,id=None,ammount=0,sender=None,order=None,_time=None):
        self.id= ("TRX_"+uuid.uuid4()) if id is None else id
        self.ammount= ammount
        self.sender=sender
        self.order=order
        self._time=_time
    
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
    def linkTo(self,order:order.Order):
        self.order=order