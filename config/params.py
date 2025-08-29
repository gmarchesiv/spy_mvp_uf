# ====================
#  - Librerias -
# ====================
import json
import os
import pytz
from dotenv import load_dotenv
from datetime import time as dt_time
from functions.logs import printStamp


###############################################
#                  PARAMETROS
###############################################
class parameters:
    def __init__(self ):
        ###############################################
        #               PARAMETROS -  GENERALES
        ###############################################

        self.etf = "SPY"
        self.exchange = ["CBOE"]
        self.zone = pytz.timezone("America/New_York")
        self.fin_rutina = dt_time(15, 55)

        ###############################################
        #               PARAMETROS -  DEL ENV
        ###############################################

        load_dotenv()

        self.name = os.getenv("NAMEIB")
        self.tele = os.getenv("TELEID")
        self.token = os.getenv("TOKENBOT")
        self.typeIB = os.getenv("TYPEIB")
        self.cuenta = os.getenv("CUENTA")

        ###############################################
        #               PARAMETROS -  conexión IBKR
        ###############################################

        self.ip = "ibkr"  # IP de conexion de contenedores
        self.port = 8888  #  Puerto de conexion con datos IBKR
        self.time_connection = 180  # Tiempo para probar la conexion (Segundos)
        self.client = 124  # Numero de Cliente del modelo

        ###############################################
        #               PARAMETROS -  BoradCasting
        ###############################################

        file_name = "/usr/src/app/data/grupo.json"

        if os.path.exists(file_name):
            # Leer el archivo JSON
            with open(file_name, "r") as json_file:
                self.data = json.load(json_file)
                printStamp(" - Lectura de archivo de Grupos - ")
        else:
            printStamp(" - No se encuentra archivo de Grupos - ")
            exit()
        self.users = self.data["red"]

        ###############################################
        #               PARAMETROS -  RUTINA
        ###############################################

        # PARAMETROS NO DEFINIDOS
        self.inf = 999
        self.inf_n = -9
 

        self.rangos_strikes = [[2, 2.5] ]
        # self.rangos_strikes = [[2, 2.3], [2.15, 2.55], [2.4, 3]]
        self.diff_days_exp = 30
        self.days_max = [30, 45]



        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028

        self.max_askbid_venta_abs = 0.0275
        self.max_askbid_compra_abs = 0.0185

        self.umbral_askbid=0.08
        # self.askbid_len_lista=91

        self.max_askbid_venta_forzada = 0.04

        self.slippage=1.075
        self.fd =  dt_time(15, 30)

        self.rutina = [dt_time(7, 0), dt_time(16, 0)]
        self.frecuencia_muestra =[i for i in range(0, 60, 2)]
        self.frecuencia_accion = [i for i in range(0, 60, 2)]
 
        self.intentos=1
        self.tiempo_contulta=5

        self.proteccion_ask_bid=[[dt_time(9, 45,0), dt_time(9, 45,18)],[dt_time(10, 0,0), dt_time(10,0,18 )]]


        self.proteccion_compra=[ dt_time(9, 44,0), dt_time(9, 45,30) ]
        self.proteccion_compra_2=[ dt_time(9, 59,0), dt_time(10, 0,15) ]
        self.proteccion_compra_call_r1=[ dt_time(9, 44,0), dt_time(9, 45,30)  ]
        #########################################################
        ####################      CALL        ###################
        #########################################################
        # ==================================
        # =========== CALL PROTECCION ======  
        # ==================================
        self.umbral_no_perdida_c = 0.016
        self.perdida_maxima_c = 0.045
        self.perdida_maxima_c_abs = -0.021
    
        # ==================================
        # =========== CALL - R1 ============
        # ==================================
        
        self.dcall_r1 = [0.125, 0.18]
        self.docall_r1 = [0.036, 0.0595]
        self.timecall_r1 = [ dt_time(9, 45,30) , dt_time(9, 55)]
        self.labelcall_r1 =0
        
        # VENTA
        self.sl_cr1=-0.03  # STOP LOSS
        # self.min_desicion_cr1  = 60
        self.umbral_manifestacion_cR1=0.023
        self.diamante_cr1 = [self.umbral_manifestacion_cR1 ,0.039  ] # DIAMANTE DE COMPRA
        self.resta_cr1 = [0.0295,self.inf_n ] # RETROCESO DEL DIAMANTE 
        # ==================================
        # =========== CALL - R3 =======
        # ==================================
        
        self.dcall_r3 =  [ 0.18, 0.25]
        self.docall_r3 =   [0.035, 0.0595]
        self.timecall_r3 =  [dt_time(9, 35), dt_time(10, 5)]
        self.labelcall_r3=0
        
        # VENTA
        self.sl_cr3 =-0.037  # STOP LOSS
        
        self.umbral_manifestacion_cR3 =0.023
        self.diamante_cr3  = [  self.umbral_manifestacion_cR3,0.03, 0.037    ] # DIAMANTE DE COMPRA
        self.resta_cr3  = [  0.0295,0.01,self.inf_n]# RETROCESO DEL DIAMANTE 
        # ==================================
        # =========== CALL - R1-E ========== 
        # ==================================
        
        self.dcall_r1_e = [-0.17, 0]
        self.docall_r1_e = [0.105, 0.113]
        self.timecall_r1_e = [dt_time(10, 25), dt_time(11, 15)]
        self.labelcall_r1_e =0
        
        # VENTA
        self.sl_cr1_e=-0.042  # STOP LOSS
        # self.min_desicion_cr1_e  = 60
        self.umbral_manifestacion_cR1_e=0.023
        self.diamante_cr1_e = [self.umbral_manifestacion_cR1_e ,0.039] # DIAMANTE DE COMPRA
        self.resta_cr1_e = [0.043, 0.005 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R1-E2 ========== 
        # ==================================
        
        self.dcall_r1_e2 = [0, 0.2]
        self.docall_r1_e2 = [0.103, 0.115]
        self.timecall_r1_e2 = [dt_time(10, 10), dt_time(11, 5)]
        self.labelcall_r1_e2 =0
        
        # VENTA
        self.sl_cr1_e2=-0.035  # STOP LOSS
        # self.min_desicion_cr1_e2  = 60
        self.umbral_manifestacion_cR1_e2=0.017
        self.diamante_cr1_e2 = [self.umbral_manifestacion_cR1_e2,0.019 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e2 = [0.005  ,self.inf_n ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R1-FAST =======
        # ==================================
        
        self.dcall_r1_fast =  [0, 0.05]
        self.docall_r1_fast =  [0.106, 0.115]
        self.timecall_r1_fast = [dt_time(9, 35), dt_time(10, 0)]
        self.labelcall_r1_fast =0
        
        # VENTA
        self.sl_cr1_fast =-0.03  # STOP LOSS
        # self.min_desicion_cr1_fast   = 60
        self.umbral_manifestacion_cR1_fast =0.029
        self.diamante_cr1_fast  = [self.umbral_manifestacion_cR1_fast  ] # DIAMANTE DE COMPRA
        self.resta_cr1_fast  = [0.005] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =======  CALL - R1 -INV ==========  
        # ==================================
        
        self.dcall_r1_i =[-0.31, 0]
        self.docall_r1_i =  [0.106, 0.111]
        self.timecall_r1_i = [dt_time(9, 35), dt_time(9, 46)]
        self.labelcall_r1_i=1
        
        # VENTA
        self.sl_cr1_i =-0.04  # STOP LOSS
        # self.min_desicion_cr1_i  = 60
        self.umbral_manifestacion_cR1_i =0.023
        self.diamante_cr1_i = [self.umbral_manifestacion_cR1_i ,0.0379, 0.079,0.11,0.15 ] # DIAMANTE DE COMPRA
        self.resta_cr1_i = [0.0295,0.01, 0.02 ,0.015,self.inf_n] # RETROCESO DEL DIAMANTE 
        

        # ==================================
        # =======  CALL - C       ==========  
        # ==================================
        
        self.dcall_r1_c =[-0.14, 0]
        self.docall_r1_c = [0.05, 0.0842]
        self.timecall_r1_c = [dt_time(11, 35), dt_time(11, 50)]
        self.labelcall_r1_c=0
        # VENTA
        self.sl_cr1_c =-0.04  # STOP LOSS
        # self.min_desicion_cr1_c   = 60
        self.umbral_manifestacion_cR1_c =0.0285
        self.diamante_cr1_c = [self.umbral_manifestacion_cR1_c,0.0379, 0.08 ] # DIAMANTE DE COMPRA
        self.resta_cr1_c= [0.0295,0.01,self.inf_n] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R2 ============
        # ==================================

        # COMPRA
        self.dcall_r2 = [0.3, 0.61]
        self.docall_r2 = [0.042, 0.057]  
        self.timecall_r2 = [dt_time(9, 35), dt_time(10, 40)]
        self.labelcall_r2=0
        self.umbral_cr2=0.25
        

        # VENTA
        self.sl_cr2 =-0.04  # STOP LOSS
        # self.min_desicion_cr2  = 60
        self.umbral_manifestacion_cR2 =0.023
        self.diamante_cr2 = [self.umbral_manifestacion_cR2,0.0379 ]  # DIAMANTE DE COMPRA
        self.resta_cr2= [0.0295,0.0001 ] # RETROCESO DEL DIAMANTE 
        # target_cr2 =0.0379
        
        # retroceso_cr2=0.05 

        # ==================================
        # =========== CALL R1 F =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f = [0.02, 0.13]
        self.docall_r1_f = [0.095, 0.11]
        self.timecall_r1_f = [dt_time(12, 30), dt_time(12, 33)]
        self.labelcall_r1_f=0

        # VENTA
        self.sl_cr1_f=-0.03  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        # target_pR1_f =0.04

        self.umbral_manifestacion_cR1_f=0.0285
        self.diamante_cr1_f = [
        self.umbral_manifestacion_cR1_f,
        0.04
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f = [0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE



        # ==================================
        # =========== CALL R1 F2 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f2 = [0.158, 0.335]
        self.docall_r1_f2 = [0.1, 0.11]
        self.timecall_r1_f2 = [dt_time(12, 0), dt_time(14, 0)]
        self.labelcall_r1_f2=0

        # VENTA
        self.sl_cr1_f2=-0.03  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        # target_pR1_f =0.04

        self.umbral_manifestacion_cR1_f2=0.0285
        self.diamante_cr1_f2 = [
        self.umbral_manifestacion_cR1_f2,
        0.038
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f2 = [0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== CALL R1 F3 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f3 = [-0.17, -0.02]
        self.docall_r1_f3 = [0.09, 0.1]
        self.timecall_r1_f3 = [dt_time(12, 0), dt_time(14, 0)]
        self.labelcall_r1_f3=0

        # VENTA
        self.sl_cr1_f3=-0.03  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        # target_pR1_f =0.04

        self.umbral_manifestacion_cR1_f3=0.0285
        self.diamante_cr1_f3 = [
        self.umbral_manifestacion_cR1_f3,
        0.038
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f3 = [0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE

        #######################
        #########################################################
        ####################      PUT         ###################
        #########################################################

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.016
        self.perdida_maxima_p = 0.045
        self.perdida_maxima_p_abs = -0.021

        # ==================================
        # =========== PUT R1================
        # ==================================
        # COMPRA
        
        self.dput_r1 = [0.09, 0.15]
        self.doput_r1 = [0.059, 0.065]
        self.timePut_r1 = [dt_time(9, 50), dt_time(10, 5)]
        self.labelPut_r1=1

        # VENTA
        self.sl_pr1=-0.03  # STOP LOSS
        # self.min_desicion_pr1  = 60
        self.umbral_manifestacion_pR1=0.029
        self.diamante_pr1 = [self.umbral_manifestacion_pR1, 0.036,0.079 ,0.109] # DIAMANTE DE COMPRA
        self.resta_pr1 = [0.0295,0.01, 0.02,self.inf_n ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =======   PUT - R1-INV ==========  
        # ==================================
        
        self.dput_r1_i =[-0.06, 0.02]
        self.doput_r1_i = [0.11, 0.115]
        self.timePut_r1_i = [dt_time(9, 40), dt_time(10,5)]
        self.labelPut_r1_i=0
        
        # VENTA
        self.sl_pr1_i=-0.04  # STOP LOSS
        # self.min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_i=0.029
        self.diamante_pr1_i = [self.umbral_manifestacion_pR1_i, 0.0379,0.079 ,0.11,0.15] # DIAMANTE DE COMPRA
        self.resta_pr1_i =[0.0295,0.01, 0.02,0.015,self.inf_n ]# RETROCESO DEL DIAMANTE 

        # ==================================
        # =======   PUT - R1-C ==========  
        # ==================================
        
        self.dput_r1_c =[-0.135, -0.02]
        self.doput_r1_c = [0.105, 0.112]
        self.timePut_r1_c = [dt_time(10, 25), dt_time(11,10)]
        self.labelPut_r1_c=0
        
        # VENTA
        self.sl_pr1_c=-0.03  # STOP LOSS
        # self.min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_c=0.023
        self.diamante_pr1_c = [self.umbral_manifestacion_pR1_c, 0.0379 ] # DIAMANTE DE COMPRA
        self.resta_pr1_c =[0.0295,self.inf_n ]# RETROCESO DEL DIAMANTE 

        # ==================================
        # =======   PUT - R1-C2 ==========  
        # ==================================
        
        self.dput_r1_c2 =[0.05, 0.12]
        self.doput_r1_c2 = [0.095, 0.112]
        self.timePut_r1_c2 = [dt_time(10, 30), dt_time(11,10)]
        self.labelPut_r1_c2=0
        
        # VENTA
        self.sl_pr1_c2=-0.03  # STOP LOSS
        # self.min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_c2=0.023
        self.diamante_pr1_c2 = [self.umbral_manifestacion_pR1_c2, 0.0298 ] # DIAMANTE DE COMPRA
        self.resta_pr1_c2 =[0.0295,self.inf_n ]# RETROCESO DEL DIAMANTE 

        # # ==================================
        # # =========== PUT R1 C =============  COMENTADA
        # # ==================================
        # # COMPRA
        
        # self.dput_r1_c = [self.inf_n, 0.2]
        # self.doput_r1_c = [0.13, 0.145]
        # self.timePut_r1_c = [dt_time(11, 0), dt_time(13,15)]
        

        # # VENTA
        # self.sl_pr1_c=-0.05  # STOP LOSS
        # # self.min_desicion_pr1_c  = 60
        # self.umbral_manifestacion_pR1_c=0.0379
        # self.diamante_pr1_c = [self.umbral_manifestacion_pR1_c, 0.079 ] # DIAMANTE DE COMPRA
        # self.resta_pr1_c = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =======   PUT - R1-E    ==========  COMENTADA
        # ==================================
        
        self.dput_r1_e =[0.15, 0.33]
        self.doput_r1_e = [0.13, 0.14]
        self.timePut_r1_e = [dt_time(10, 15), dt_time(11,0)]
        self.labelPut_r1_e=1
        
        # VENTA
        self.sl_pr1_e=-0.05  # STOP LOSS
        # self.min_desicion_pr1_e  = 60
        self.umbral_manifestacion_pR1_e=0.0379
        self.diamante_pr1_e = [self.umbral_manifestacion_pR1_e, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1_e = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== PUT R1-FAST=========== # COMENTADA
        # ==================================
        # COMPRA
        
        self.dput_r1_fast = [0, 0.15]
        self.doput_r1_fast = [0.08, 0.115]
        self.timePut_r1_fast = [dt_time(9, 45), dt_time(10, 5)]
        self.labelPut_r1_fast=1

        # VENTA
        self.sl_pr1_fast=-0.045  # STOP LOSS
        # self.min_desicion_pr1_fast  = 60
        self.umbral_manifestacion_pR1_fast=0.02 
        self.diamante_pr1_fast = [self.umbral_manifestacion_pR1_fast, 0.089 ] # DIAMANTE DE COMPRA
        self.resta_pr1_fast = [0.01, self.inf_n ] # RETROCESO DEL DIAMANTE 

        
        
        # ==================================
        # =========== PUT R2 ===============
        # ==================================

        # COMPRA
        self.umbral_pr2=0.2
        self.dput_r2 = [0.27, 0.40]  
        self.doput_r2 = [0.057, 0.065]  
        self.timePut_r2 = [dt_time(9, 45), dt_time(10, 0)]
        self.labelPut_r2=1

        # VENTA
        self.sl_pr2 = -0.035
        self.umbral_manifestacion_pR2=0.0285
        self.diamante_pr2 = [ self.umbral_manifestacion_pR2,   0.035 ]  # DIAMANTE DE COMPRA
        self.resta_pr2 =[0.003, self.inf_n ]  # RETROCESO DEL DIAMANTE
        
        # ==================================
        # =========== PUT R2E ===============
        # ==================================

        # COMPRA
        
        self.dput_r2_e = [0.45, 0.7]  
        self.doput_r2_e = [0.04, 0.075]  
        self.timePut_r2_e = [dt_time(9, 35), dt_time(10, 5)]
        self.labelPut_r2_e=1
        
        # VENTA
        
        self.sl_pr2_e = -0.035  # STOP LOSS
        

        self.umbral_manifestacion_pR2_e=0.019

        self.diamante_pr2_e = [ self.umbral_manifestacion_pR2_e ] # DIAMANTE DE COMPRA
        self.resta_pr2_e = [self.inf_n ] # RETROCESO DEL DIAMANTE  


        # ==================================
        # =========== PUT R1 F =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f = [-0.05, 0.08]
        self.doput_r1_f = [0.07, 0.115]
        self.timePut_r1_f = [dt_time(14, 0), dt_time(14, 10)]
        self.labelPut_r1_f=1

        # VENTA
        self.sl_pr1_f=-0.042  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        # target_pR1_f =0.04

        self.umbral_manifestacion_pR1_f=0.0285
        self.diamante_pr1_f = [
        self.umbral_manifestacion_pR1_f,
        0.04
        ]  # DIAMANTE DE COMPRA
        self.resta_pr1_f = [0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== PUT R1 F2 =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f2 = [0, 0.2]
        self.doput_r1_f2 = [0.075, 0.081]
        self.timePut_r1_f2 = [dt_time(12, 30), dt_time(15, 5)]
        self.labelPut_r1_f2=1

        # VENTA
        self.sl_pr1_f2=-0.025  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        # target_pR1_f =0.04

        self.umbral_manifestacion_pR1_f2=0.023
        self.diamante_pr1_f2 = [
        self.umbral_manifestacion_pR1_f2 ,0.029
        ]  # DIAMANTE DE COMPRA
        self.resta_pr1_f2 = [ 0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== PUT R3 ===============
        # ==================================
        # COMPRA
        
        self.dput_r3 = [ 0.2, 0.25]
        self.doput_r3 = [0.055, 0.065]
        self.timePut_r3 = [dt_time(9, 40), dt_time(9, 55)]
        self.labelPut_r3=1

        # VENTA
        
        self.sl_pr3 = -0.035   # STOP LOSS
        self.umbral_manifestacion_pR3=0.023
        self.diamante_pr3  = [self.umbral_manifestacion_pR3 ,0.034 ] # DIAMANTE DE COMPRA
        self.resta_pr3  = [ 0.0295, self.inf_n]
   
        #########################################################
        ####################      LABELS      ###################
        #########################################################
       
     

        self.omega=0.00000233

        self.alpha=0.00280000

        self.beta=0.89020000

        self.gamma=0.17930000

        self.days_year=252

