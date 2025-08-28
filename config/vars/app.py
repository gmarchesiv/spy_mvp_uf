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
class varsApps:
    def __init__(self):
        
        #---------------------------------------------------
        '''
        Abriremos el archivo json Correspondientes (app.json)
        y en caso no exista la variable la genera ,finalmente 
        la carga en memoria.
        '''
        #---------------------------------------------------

        file_name = "/usr/src/app/data/app.json"

        if os.path.exists(file_name):
            # Leer el archivo JSON
            with open(file_name, "r") as json_file:
                self.data = json.load(json_file)
                printStamp(" - Lectura de archivo de variables - ")
        else:
            printStamp(" - No se encuentra archivo de variables - ")
            exit()
        ###############################################
        # VARIABLES DE APP
        ###############################################

        self.cash = self.data.get("cash", 0)
        self.statusIB = self.data.get("statusIB", False)
        self.execution_details = self.data.get("execution_details", {})
        self.commissions = self.data.get("commissions", {})
        self.sendError = self.data.get("sendError", False)
        self.Error = self.data.get("Error", False)
        self.Error_buy = self.data.get("Error_buy", False)
        self.flag_bloqueo_tiempo= self.data.get("flag_bloqueo_tiempo", False)
       