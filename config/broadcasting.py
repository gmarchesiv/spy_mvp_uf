# ====================
#  - Librerias -
# ====================
import json
import os
from functions.logs import printStamp
from collections import deque

###############################################
#                  VARIABLES
###############################################
class broadcasting:
    def __init__(self):
        ###############################################
        # LECTURA DEL ARCHIVO DE VARIABLES
        ###############################################
 

        
        self.sell= False
        self.max_askbid_venta_abs = 0.0275
        # self.sell_tipo = self.data.get("sell_tipo", "")
        # self.sell_regla = self.data.get("sell_regla", "")
        # self.buy  = self.data.get("buy", False)
        # self.buy_tipo  = self.data.get("buy_tipo", "")
        # self.buy_regla = self.data.get("buy_regla", "")
        # self.user = self.data.get("user", "")
        

        # self.aliniar = self.data.get("aliniar", False)
        # self.call_close  = self.data.get("call_close", 0)
        # self.put_close  = self.data.get("put_close",0)
        # self.call_open = self.data.get("call_open", 0)
        # self.put_open = self.data.get("put_open",0)
        # self.flag_Call_R2 = self.data.get("flag_Call_R2", False)
        # self.flag_Put_R2= self.data.get("flag_Put_R2", False)
        
 
 

