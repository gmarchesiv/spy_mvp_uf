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
class varsBroadcasting:
    def __init__(self,debug_mode ):
 
        #---------------------------------------------------
        '''
        Carga en memoria las variables y las guarda limpias 
        en su respectivo json (broadcasting.json).
        '''
        #---------------------------------------------------

        ###############################################
        # LECTURA DEL ARCHIVO DE VARIABLES
        ###############################################
 

        
        self.sell= False
        self.max_askbid_venta_abs = 0.0275
        self.sell_tipo = " "
        self.sell_regla = " "
        self.buy  = False
        self.buy_tipo  = " "
        self.buy_regla = " "
        self.user = " "
        

        self.aliniar = False
        self.call_close  = 0
        self.put_close  = 0
        self.call_open = 0
        self.put_open = 0
        self.flag_Call_R2 =False
        self.flag_Put_R2= False
        
 
        if debug_mode ==False:
            file_name = "/usr/src/app/data/broadcasting.json"
            with open(file_name, "r") as file:
                datos = json.load(file)
        
            
                datos["sell"] = self.sell
                datos["max_askbid_venta_abs"] = self.max_askbid_venta_abs

            with open(file_name, "w") as file:
                json.dump(datos, file, indent=4)
    

