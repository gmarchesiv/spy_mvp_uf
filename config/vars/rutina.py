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
class varsRutina:
    def __init__(self,debug_mode ):

        #---------------------------------------------------
        '''
        Abriremos el archivo json Correspondientes 
        (vars.json) y en caso no exista la variable la genera,
        finalmente la carga en memoria.
        '''
        #---------------------------------------------------
        if debug_mode ==False:
            file_name = "/usr/src/app/data/vars.json"

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
        ###############################################
        # VARIABLES DE TIEMPO
        ###############################################
        self.minutos = self.data.get("minutos", 0)
        self.n_minutos = self.data.get("n_minutos", 0)
        self.minutos_trade = self.data.get("minutos_trade", 0)

        ###############################################
        # VARIABLES DE PRECIO
        ###############################################
        self.call_close = self.data.get("call_close", 0)
        self.put_close = self.data.get("put_close", 0)
        self.call_open = self.data.get("call_open", 0)
        self.put_open = self.data.get("put_open", 0)

        ###############################################
        # VARIABLES DE FLAGS
        ###############################################
        self.call = self.data.get("call", False)
        self.put = self.data.get("put", False)
        self.compra = self.data.get("compra", True)
        self.manifesto = self.data.get("manifesto", False)
        self.flag_Call_R2 = self.data.get("flag_Call_R2", False)
        self.flag_Put_R2 = self.data.get("flag_Put_R2", False)

        self.flag_Call_reset_r1=self.data.get("flag_Call_reset_r1", False)
        self.flag_Call_reset_r3=self.data.get("flag_Call_reset_r3", False)
        self.flag_Call_reset_r1_e =self.data.get("flag_Call_reset_r1_e", False)
        self.flag_Call_reset_r1_e2 =self.data.get("flag_Call_reset_r1_e2", False)

        self.flag_Put_reset_r2_e=self.data.get("flag_Put_reset_r2_e", False)
        self.flag_Put_reset_r1=self.data.get("flag_Put_reset_r1", False)
        self.flag_Put_reset_r1_c =self.data.get("flag_Put_reset_r1_c", False)
        self.flag_Put_reset_r1_c2 =self.data.get("flag_Put_reset_r1_c2", False)
        self.flag_Put_reset_r1_fast=self.data.get("flag_Put_reset_r1_fast", False)
        self.flag_Put_reset_r1_i =self.data.get("flag_Put_reset_r1_i", False)
        self.flag_Put_reset_f2 =self.data.get("flag_Put_reset_f2", False)
        self.flag_Put_reset_r3 =self.data.get("flag_Put_reset_r3", False)

        self.flag_Call_reset_r3_2 =self.data.get("flag_Call_reset_r3_2", False)
        self.flag_Put_reset_r1_label =self.data.get("flag_Put_reset_r1_label", False)
        self.flag_cambio_R1_label =self.data.get("flag_cambio_R1_label", False)
  
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
        self.min_extras = self.data.get("min_extras", 0)
        self.min_desicion = self.data.get("min_desicion", 0)
        self.ugs_n = self.data.get("ugs_n", 0)
        self.ugs_n_ant = self.data.get("ugs_n_ant", 0)
        self.pico = self.data.get("pico", 0)
        self.tipo = self.data.get("tipo", "")
        self.hora_inicio = self.data.get("hora_inicio", "")
        ###############################################
        # VARIABLES DE TRADING
        ###############################################
        self.label_ant = self.data.get("label_ant", 0)
        self.vix= self.data.get("vix", 0)
        self.dcall = self.data.get("dcall", 0)
        self.dput = self.data.get("dput", 0)
        self.doput_ant = self.data.get("doput_ant", 0)
 
        self.docall = self.data.get("docall", 0)
        self.doput = self.data.get("doput", 0)
        self.askbid_call = self.data.get("askbid_call", 0)
        self.askbid_put = self.data.get("askbid_put", 0)
        self.askbid_call_prom = self.data.get("askbid_call_prom ", [])
        self.askbid_put_prom  = self.data.get("askbid_put_prom ",[])
        
        self.quantity = self.data.get("quantity", 0)
        self.rentabilidad = self.data.get("rentabilidad", 0)
        self.rentabilidad_ant = self.data.get("rentabilidad_ant", 0)
        self.priceBuy = self.data.get("priceBuy", 0)
        self.real_priceBuy= self.data.get("real_priceBuy", 0)
        self.caida = self.data.get("caida", 0)
        self.regla = self.data.get("regla", "")
        self.trades = self.data.get("trades", [])
        self.fecha = self.data.get("fecha", "")
        self.strikes = self.data.get("strikes", {})
        self.strike_c = self.data.get("strike_c", 0)
        self.strike_p = self.data.get("strike_p", 0)
        self.dif_exp = self.data.get("dif_exp", 0)
        self.dic_strike = self.data.get("dic_strike", 0)
        self.exp = self.data.get("exp", "")
        self.rentabilidad_final = 0
        self.dic_exp_strike = self.data.get("dic_exp_strike", {})
        self.rule = self.data.get("rule", True)
        self.cask = 0
        self.cbid = 0
        self.pask = 0
        self.pbid = 0
        self.regla_ant = ""
        self.trade_hour = ""
        self.accion_mensaje = self.data.get("accion_mensaje", 0)
        self.bloqueo = self.data.get("bloqueo", True)
        self.exchange = self.data.get("exchange", "CBOE")
        self.status = self.data.get("status", "ON")
  

        self.promedio_call=self.data.get("promedio_call",0)
        self.promedio_put=self.data.get("promedio_put",0)   

        self.askbid_call_prom=deque(self.askbid_call_prom, maxlen=90)
        self.askbid_put_prom=deque(self.askbid_put_prom, maxlen=90)