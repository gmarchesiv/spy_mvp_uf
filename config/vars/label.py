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
class varsLabel:
    def __init__(self,debug_mode ):

        #---------------------------------------------------
        '''
        Abriremos el archivo json Correspondientes (label.json)
        y en caso no exista la variable la genera ,finalmente 
        la carga en memoria.
        '''
        #---------------------------------------------------
        if debug_mode ==False:
            file_name = "/usr/src/app/data/label.json"

            if os.path.exists(file_name):
                # Leer el archivo JSON
                with open(file_name, "r") as json_file:
                    self.data = json.load(json_file)
                    printStamp(" - Lectura de archivo de variables - ")
            else:
                printStamp(" - No se encuentra archivo de variables - ")
                exit()
  
        else:
            self.data={}
        # print(self.data )
        ###############################################
        # LABEL
        ###############################################
        self.flag_minuto_label=self.data.get("flag_minuto_label", False)
        self.label = self.data.get("label", 0)
        self.retorno = self.data.get("retorno", 0)
        self.signo  = self.data.get("signo", 0)
        self.varianza  = self.data.get("varianza", 0)
        self.pico_etf=self.data.get("pico_etf", 608.48)
        self.d_pico  = self.data.get("d_pico", 0)   
        self.rsi=self.data.get("rsi",0)
        self.mu=self.data.get("mu", 0.000622019)
        self.mu_conteo=self.data.get("mu_conteo", 358123)


        # Listas

        self.retorno_lista = self.data.get("retorno_lista", [])
        self.ret_1H_back= self.data.get("ret_1H_back", [])
        self.ret_3H_back= self.data.get("ret_3H_back", [])
        self.ret_6H_back= self.data.get("ret_6H_back", [])
        self.ret_12H_back= self.data.get("ret_12H_back", [])
        self.ret_24H_back= self.data.get("ret_24H_back", [])
        self.ret_96H_back= self.data.get("ret_96H_back", [])
        self.etf_price_lista=self.data.get("etf_price_lista", [])
        

        # DEQUES
 
        self.retorno_lista =  deque(self.retorno_lista, maxlen=79)
        self.ret_1H_back= deque(self.ret_1H_back, maxlen=1)
        self.ret_3H_back= deque(self.ret_3H_back, maxlen=3)
        self.ret_6H_back= deque(self.ret_6H_back, maxlen=6)
        self.ret_12H_back= deque(self.ret_12H_back, maxlen=12)
        self.ret_24H_back= deque(self.ret_24H_back, maxlen=24)
        self.ret_96H_back= deque(self.ret_96H_back, maxlen=96)
        self.etf_price_lista=deque(self.etf_price_lista, maxlen=200)

  
        # print(self.ret_1H_back)