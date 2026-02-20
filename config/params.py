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
    def __init__(self,debug_mode):

        #---------------------------------------------------
        '''
        Cargamos los parametros del modelo a memoria.
        '''
        #---------------------------------------------------

        ###############################################
        #               PARAMETROS -  GENERALES
        ###############################################

        self.etf = "SPY"
        self.exchange = ["SMART"]
        self.zone = pytz.timezone("America/New_York")

        ###############################################
        #               PARAMETROS -  DEL ENV
        ###############################################

        load_dotenv()
        self.name = os.getenv("NAMEIB")
        self.tele = os.getenv("TELEID")
        self.token = os.getenv("TOKENBOT")
        self.typeIB = os.getenv("TYPEIB")
        self.cuenta = os.getenv("CUENTA")
        self.strike_escenario =int( os.getenv("STRIKE"))
        self.strike_unidad = int(os.getenv("UNIDAD"))
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

        if debug_mode == False :
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
 
        # SELECCION DE STRIKES 
        self.rangos_strikes_2 = [[2, 2.6] ]
        self.rangos_strikes = [[0, 1] ]
        self.days_min_exp = 24  # DIAS para el exp minimo de busqueda
        self.days_max_exp = 39 
        self.except_days_min_exp = 28

        # PARAMETROS DE ASKBID DE ACCIONES
        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028
        self.max_askbid_venta_abs = 0.0255
        self.max_askbid_compra_abs = 0.0185
        self.max_askbid_venta_forzada = 0.04

        # PARAMETROS LIMITES DE OPEN ASKBID
        self.max_askbid_open = 0.03
        self.max_askbid_hora_open =  dt_time(9, 33)
        self.umbral_askbid=0.08

        # PARAMETROS DE COMPRA VENTA SLIPPAGE
        self.slippage=1.05

        #PARAMETROS DE TIEMPO DE RUTINA Y MUESTRAS
    
        self.fin_rutina = dt_time(15, 55)
        self.fd =  dt_time(15, 30)
        self.rutina = [dt_time(6, 50), dt_time(16, 0)]
        self.frecuencia_accion =[i for i in range(0, 60, 2)]
        
        #PARAMETROS DE VENTA 
        self.intentos=1
        self.tiempo_contulta=5

        #PARAMETROS DE PROTECCION
        self.proteccion_ask_bid=[[dt_time(9, 45,0), dt_time(9, 45,18)],[dt_time(10, 0,0), dt_time(10,0,18 )]]
        self.proteccion_compra=[ dt_time(9, 44,20), dt_time(9, 46,0) ]
        self.proteccion_compra_2=[ dt_time(9, 59,30), dt_time(10, 0,15) ]
        self.proteccion_compra_call_r1=[ dt_time(9, 44,0), dt_time(9, 46,0)  ]
        
        #########################################################
        ####################      CALL        ###################
        #########################################################
        # ==================================
        # =========== CALL PROTECCION ======  
        # ==================================
        self.umbral_no_perdida_c = 0.016
        
        self.perdida_maxima_c = 0.045
    
        self.perdida_maxima_c_abs = -0.017

        self.umbral_no_perdida_c_r2 = 0.016
        self.perdida_maxima_c_r2 = 0.05
        # ==================================
        # =========== CALL - R1 ============
        # ==================================
        
        self.dcall_r1 =  [0.11, 0.125]
        self.docall_r1 =[0.03, 0.035]
        self.timeCall_r1 = [dt_time(9, 47), dt_time(10, 00)]
        self.labelCall_r1 =0
        
        # VENTA
    
        # self.min_desicion_cr1  = 60
        self.sl_cr1 = -0.035  # STOP LOSS

        # self.target_cR1=0.04
        self.umbral_manifestacion_cR1 = 0.018 
        self.diamante_cr1 = [self.umbral_manifestacion_cR1,0.028 ,0.04  ] # DIAMANTE DE COMPRA
        self.resta_cr1  =  [ 0.01 ,0.005, 0.001]  # RETROCESO DEL DIAMANTE 



        # ==================================
        # =========== CALL - R1-E ==========  
        # ==================================
        
        self.dcall_r1_e = [-0.155, 0.077 ]
        self.docall_r1_e = [0.059, 0.065]
        self.timeCall_r1_e = [dt_time(10,14), dt_time(10, 18)]
        self.labelCall_r1_e =0
        
        # VENTA
        self.sl_cr1_e=-0.048  # STOP LOSS
        # min_desicion_cr1_e  = 60
        self.umbral_manifestacion_cR1_e= 0.018
        self.diamante_cr1_e = [self.umbral_manifestacion_cR1_e,0.027,0.0379, 0.07 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e = [0.015,0.01,0.005, 0.001 ] # RETROCESO DEL DIAMANTE 

        self.bloqueo_cr1_e_docall=0.15
        self.bloqueo_cr1_e_doput=0.06
        # bloqueo_cr1_e_dput= -0.05
        self.bloqueo_cr1_e_hora=dt_time(10,0)
        # ==================================
        # =========== CALL - R1-E2 ==========  
        # ==================================
        
        self.dcall_r1_e2 = [-0.07, 0.1 ]
        self.docall_r1_e2 =[0.057, 0.0631]
        self.timeCall_r1_e2 = [dt_time(10,26), dt_time(10, 40)]
        self.labelCall_r1_e2 =0
        
        # VENTA
        self.sl_cr1_e2=-0.04  # STOP LOSS
        # min_desicion_cr1_e2  = 60
        self.umbral_manifestacion_cR1_e2=  0.018
        self.diamante_cr1_e2 = [self.umbral_manifestacion_cR1_e2,0.027,0.0379, 0.07 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e2 = [0.015,0.01,0.005, 0.001 ] # RETROCESO DEL DIAMANTE 
    

        # ==================================
        # =======  CALL - R1 -INV ==========  
        # ==================================
        
        self.dcall_r1_i =[-0.37, 0]
        self.docall_r1_i = [0.08, 0.088]
        self.timeCall_r1_i = [dt_time(9, 34), dt_time(9,55)]
        self.labelCall_r1_i=1
        self.dcall_r1_i_dput=0.27
        
        # VENTA
        
        self.sl_cr1_i = -0.048  # STOP LOSS
   


        self.umbral_manifestacion_cr1_i =0.0198
        self.diamante_cr1_i = [self.umbral_manifestacion_cr1_i,0.0245,0.03   ] # DIAMANTE DE COMPRA
        self.resta_cr1_i=[0.015,0.01 ,0.001] # RETROCESO DEL DIAMANTE 

        

        # ==================================
        # =======  CALL - C       ==========  
        # ==================================
        
        self.dcall_r1_c =[-0.17,-0.1]
        self.docall_r1_c = [0.1, 0.11]
        self.timeCall_r1_c = [dt_time(11, 30), dt_time(12, 15)]
        self.labelCall_r1_c=0
        # VENTA
        self.sl_cr1_c =-0.04  # STOP LOSS
        # min_desicion_cr1_c   = 60
        self.umbral_manifestacion_cR1_c =0.018
        self.diamante_cr1_c = [self.umbral_manifestacion_cR1_c,0.028,0.0379, 0.07 ,0.10 ] # DIAMANTE DE COMPRA
        self.resta_cr1_c=[0.015,0.01 ,0.005,0.02, 0.001 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R2 ============
        # ==================================

        # COMPRA
        self.dcall_r2 =[0.25, 0.38]
        self.docall_r2 = [0.03, 0.0335]  
        self.timeCall_r2 =  [dt_time(9, 36,30), dt_time(9, 50)]
        self.labelCall_r2=0
        self.umbral_cr2=0.225
        # VENTA
        # self.umbral_manifestacion_cR2 =  0.05  # UMBRAL DE MANIFESTACION
        self.min_desicion_cR2   = 60
 
        
        self.target_min_desicion_cR2 =0.01
        self.sl_cr2 = -0.035  # STOP LOSS
        self.umbral_manifestacion_cR2=0.017
        self.diamante_cr2 = [self.umbral_manifestacion_cR2,0.0255 ,0.04 ,0.05] # DIAMANTE DE COMPRA
        self.resta_cr2=  [0.013,0.01,0.005,0.001] # RETROCESO DEL DIAMANTE 
        # self.target_cR2=0.11

        # ==================================
        # =========== CALL - R2-2 ============
        # ==================================

        # COMPRA
        self.dcall_r2_2 = [0.25, 0.35]
        self.docall_r2_2 = [0.03, 0.0335]  
        self.timeCall_r2_2= [dt_time(10, 0), dt_time(10, 45)]
        self.labelCall_r2_2=0
        self.umbral_cr2_2=0.225
        # VENTA
        # umbral_manifestacion_cR2 =  0.05  # UMBRAL DE MANIFESTACION
        self.min_desicion_cR2_2   = 60
        self.target_min_desicion_cR2_2 =0.01

        self.sl_cr2_2 = -0.035  # STOP LOSS
        self.umbral_manifestacion_cR2_2=0.02
        self.diamante_cr2_2 = [self.umbral_manifestacion_cR2_2 ,0.0255 ,0.04 ,0.05]# DIAMANTE DE COMPRA
        self.resta_cr2_2= [0.015,0.01,0.005,0.001] # RETROCESO DEL DIAMANTE 
        # target_cR2=0.11


        # ==================================
        # =========== CALL - R1-FAST =======
        # ==================================
        
        self.dcall_r1_fast = [-0.02 ,0.125]
        self.docall_r1_fast =  [0.04, 0.057]
        self.timeCall_r1_fast = [dt_time(9, 35), dt_time(9, 55)]
        self.labelCall_r1_fast =0
        
        # VENTA
        self.sl_cr1_fast =-0.045  # STOP LOSS
        # min_desicion_cr1_fast   = 60
        self.umbral_manifestacion_cR1_fast =0.02 
        self.diamante_cr1_fast  = [self.umbral_manifestacion_cR1_fast  , 0.028,0.04] # DIAMANTE DE COMPRA
        self.resta_cr1_fast  = [0.015,0.005,self.inf_n   ]# RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== CALL - R3 =======
        # ==================================
        
        self.dcall_r3 =  [ 0.2, 0.227]
        self.docall_r3 =  [0.03, 0.04]
        self.timeCall_r3 =  [dt_time(9, 38), dt_time(9, 45)]
        self.labelCall_r3=0
        
        # VENTA
        self.sl_cr3 =-0.046  # STOP LOSS
        
        self.umbral_manifestacion_cR3 =0.018
        self.diamante_cr3  = [  self.umbral_manifestacion_cR3,0.027, 0.031  ] # DIAMANTE DE COMPRA
        self.resta_cr3  = [  0.015,0.005,self.inf_n]# RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== CALL R1 F1 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f1 = [-0.22,-0.08]
        self.docall_r1_f1 = [0.095, 0.11]
        self.timeCall_r1_f1 = [dt_time(12, 30), dt_time(12, 31)]
        self.labelCall_r1_f1=0

        # VENTA
        self.sl_cr1_f1=-0.04  # STOP LOSS
    

        self.umbral_manifestacion_cR1_f1=0.018
        self.diamante_cr1_f1 = [
        self.umbral_manifestacion_cR1_f1 ,0.025,
    0.04
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f1 = [0.015 ,0.01,self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== CALL R1 F2 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f2 = [0.25, 0.35]
        self.docall_r1_f2 = [0.095, 0.11]
        self.timeCall_r1_f2 = [dt_time(12, 30), dt_time(12, 31)]
        self.labelcall_r1_f2=0

        # VENTA
        self.sl_cr1_f2=-0.04  # STOP LOSS
        # self.min_desicion_pr1_f2  = 60
        # self.target_pR1_f2 =0.04

        self.umbral_manifestacion_cR1_f2=0.018
        self.diamante_cr1_f2 = [
        self.umbral_manifestacion_cR1_f2,0.025, 0.03 ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f2 = [0.015,0.01,self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== CALL - R1-2 ============
        # ==================================
        
        self.dcall_r1_2 = [0 , 0.08]
        self.docall_r1_2 = [0.03, 0.035]
        self.timeCall_r1_2 = [dt_time(9, 34), dt_time(9, 40)]
        self.labelCall_r1_2 =0
        
        # VENTA
    
        # min_desicion_cr1  = 60
        self.sl_cr1_2 = -0.04  # STOP LOSS

        # target_cR1=0.04
        self.umbral_manifestacion_cR1_2 = 0.018
        self.diamante_cr1_2 = [self.umbral_manifestacion_cR1_2 ,0.028 ,0.0379 ,0.07,0.1 ] # DIAMANTE DE COMPRA
        self.resta_cr1_2  = [ 0.015,0.01,0.005,0.02 , 0.001] # RETROCESO DEL DIAMANTE 


        #########################################################
        ####################      PUT         ###################
        #########################################################

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.015
        
        self.perdida_maxima_p = 0.05
    
        self.perdida_maxima_p_abs = -0.017

        self.umbral_no_perdida_p_r2 = 0.016
        self.perdida_maxima_p_r2 = 0.04
   
        # ==================================
        # =======   PUT - R1-INV 2==========  
        # ==================================
        
        self.dput_r1_i_2 =[-0.35, -0.25]
        self.doput_r1_i_2 =  [0.03, 0.0385]
        self.timePut_r1_i_2 = [dt_time(9, 34), dt_time(9,40)]
        self.labelPut_r1_i_2=0
        
        # VENTA
        self.sl_pr1_i_2=-0.045  # STOP LOSS
        # min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_i_2=0.017
        self.diamante_pr1_i_2 = [self.umbral_manifestacion_pR1_i_2,0.025 ,0.04 ]# DIAMANTE DE COMPRA
        self.resta_pr1_i_2 =[0.015 ,0.005, 0.001 ] # RETROCESO DEL DIAMANTE 
        
        # ==================================
        # =======   PUT - R1-INV 3==========  
        # ==================================
        
        self.dput_r1_i_3 =[-0.025, 0.08]
        self.doput_r1_i_3 =[0.0645, 0.089]
        self.timePut_r1_i_3 = [dt_time(9,40), dt_time(10,5)]
        self.labelPut_r1_i_3=0
        
        # VENTA
        self.sl_pr1_i_3=-0.045  # STOP LOSS
        # min_desicion_pr1_i_3  = 60
        self.umbral_manifestacion_pR1_i_3=0.018
        self.diamante_pr1_i_3 = [self.umbral_manifestacion_pR1_i_3,0.025 ,0.0295]# DIAMANTE DE COMPRA
        self.resta_pr1_i_3 = [0.015 , 0.01,0.001 ]  # RETROCESO DEL DIAMANTE 
        

        # ==================================
        # =========== PUT R1-FAST================
        # ==================================
        # COMPRA
        
        self.dput_r1_fast = [ 0.0755, 0.155]
        self.doput_r1_fast = [0.0805, 0.0885]
        self.timePut_r1_fast = [dt_time(9, 40), dt_time(9, 55)]
        self.labelPut_r1_fast=1

        # VENTA
        self.sl_pr1_fast=-0.03  # STOP LOSS
        # min_desicion_pr1_fast  = 60
        self.umbral_manifestacion_pR1_fast=0.019
        self.diamante_pr1_fast = [self.umbral_manifestacion_pR1_fast,0.028 ,0.04,0.07,0.09]  # DIAMANTE DE COMPRA
        self.resta_pr1_fast =[0.012 ,0.012 ,0.012 ,0.005 ,self.inf_n ] # RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== PUT Label================
        # ==================================
        # COMPRA
        
        self.dput_r1_label =  [ 0.02, 0.1]
        self.doput_r1_label = [0.03, 0.04]
        self.timePut_r1_label = [dt_time(9, 40), dt_time(9, 55)]
        self.labelPut_r1_label=1

        # VENTA
        self.sl_pr1_label=-0.043  # STOP LOSS
        # min_desicion_pr1_label  = 60
        self.umbral_manifestacion_pR1_label=0.0165
        self.diamante_pr1_label= [self.umbral_manifestacion_pR1_label,0.025 ,0.04,0.07,0.088]# DIAMANTE DE COMPRA
        self.resta_pr1_label =[0.012,0.01  ,0.008  ,0.005  ,self.inf_n ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== PUT Label 2=========== 
        # ==================================
        # COMPRA
        
        self.dput_r1_label_2 = [ 0.02, 0.095]
        self.doput_r1_label_2 = [0.03, 0.04]
    
        self.timePut_r1_label_2 = [dt_time(10, 7), dt_time(10, 32)]
        self.labelPut_r1_label_2=1

        # VENTA
        self.sl_pr1_label_2=-0.043 # STOP LOSS
        # min_desicion_pr1_label  = 60
        self.umbral_manifestacion_pR1_label_2=0.018
        self.diamante_pr1_label_2= [self.umbral_manifestacion_pR1_label_2,0.025 ,0.04,0.07,0.088]  # DIAMANTE DE COMPRA
        self.resta_pr1_label_2 = [0.012,0.01  ,0.008  ,0.005  ,self.inf_n ]  # RETROCESO DEL DIAMANTE 



        # ==================================
        # =========== PUT R2 ===============
        # ==================================

        # COMPRA
        self.umbral_pr2=0.15
        self.dput_r2 = [0.21, 0.33]  
        self.doput_r2 = [0.055, 0.071]  
        self.timePut_r2 = [dt_time(9, 45), dt_time(9, 55)]
        self.labelPut_r2=1
  
        # VENTA
    
        # min_desicion_pr2 = 60  # MINUTOS ANTES DE MANIFESTACION
        self.sl_pr2 = -0.045  # STOP LOSS
        self.umbral_manifestacion_pR2=0.018
        self.diamante_pr2 = [
        self.umbral_manifestacion_pR2, 0.025 ]  # DIAMANTE DE COMPRA
        self.resta_pr2 = [0.01 ,0.001]   # RETROCESO DEL DIAMANTE
    
        
        # ==================================
        # =========== PUT R2E ===============
        # ==================================

        # COMPRA
        
        self.dput_r2_e = [0.385, 0.57]  
        self.doput_r2_e = [0.0355, 0.073]  
        self.timePut_r2_e = [dt_time(9, 50), dt_time(9, 55)]
        self.labelPut_r2_e=1
        
        # VENTA
        self.sl_pr2_e = -0.045 
        
        self.umbral_manifestacion_pR2_e=0.018
        self.diamante_pR2_e = [
        self.umbral_manifestacion_pR2_e,
        0.025 
        ]  # DIAMANTE DE COMPRA
        self.resta_pR2_e = [0.012 , 0.001 ] 

        


        # ==================================
        # =========== PUT R1 F =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f = [0.07, 0.2]
        self.doput_r1_f = [0.03, 0.06]
        self.timePut_r1_f = [dt_time(12, 50), dt_time(14, 10)]
        self.labelPut_r1_f=1

        # VENTA
        self.sl_pr1_f=-0.035  # STOP LOSS
        # min_desicion_pr1_f  = 60
        # self.target_pR1_f =0.04

        self.umbral_manifestacion_pR1_f=0.018
        self.diamante_pr1_f = [
        self.umbral_manifestacion_pR1_f,  0.023 ,0.04,0.07] # DIAMANTE DE COMPRA
        self.resta_pr1_f =[0.015      ,0.005 ,0.005  ,0.001     ]   # RETROCESO DEL DIAMANTE


        

        # ==================================
        # =========== PUT R3 ===============
        # ==================================
        # COMPRA
        
        self.dput_r3 =  [ 0.166, 0.21]
        self.doput_r3 = [0.04, 0.06] 
        self.timePut_r3 = [dt_time(9, 55), dt_time(10, 40)]
        self.labelPut_r3=1

        # VENTA
        
        self.sl_pr3 = -0.045   # STOP LOSS
        self.umbral_manifestacion_pR3=0.02 
        self.diamante_pr3  = [self.umbral_manifestacion_pR3 ,0.023, 0.0379 ,0.7,0.15] # DIAMANTE DE COMPRA
        self.resta_pr3  =  [0.015,0.01,0.012 ,0.02 ,self.inf_n]
    

        # ==================================
        # =======   PUT - R1-INV 4==========   
        # ==================================
        
        self.dput_r1_i_4 =[-0.036, -0.015]
        self.doput_r1_i_4 = [0.03, 0.0335]
        self.timePut_r1_i_4 = [dt_time(9,35), dt_time(9,58)]
        self.labelPut_r1_i_4=0
        
        # VENTA
        self.sl_pr1_i_4=-0.046  # STOP LOSS
        # min_desicion_pr1_i_3  = 60
        self.umbral_manifestacion_pR1_i_4=0.018
        self.diamante_pr1_i_4 = [self.umbral_manifestacion_pR1_i_4 ,0.023,0.04 ]# DIAMANTE DE COMPRA
        self.resta_pr1_i_4 =  [0.012 ,0.0045 ,0.001 ] # RETROCESO DEL DIAMANTE 
        
        # ==================================
        # =======   PUT - R1-INV 5==========  
        # ==================================
        
        self.dput_r1_i_5 =[-0.18, -0.129]
        self.doput_r1_i_5 = [0.03, 0.038]
        self.timePut_r1_i_5 = [dt_time(9,34), dt_time(9,55)]
        self.labelPut_r1_i_5=0
        
        # VENTA
        self.sl_pr1_i_5=-0.046  # STOP LOSS
        # min_desicion_pr1_i_3  = 60
        self.umbral_manifestacion_pR1_i_5=0.018
        self.diamante_pr1_i_5 = [self.umbral_manifestacion_pR1_i_5 ,0.025,0.0379,0.07,0.099]# DIAMANTE DE COMPRA
        self.resta_pr1_i_5 =  [0.012,0.01 , 0.001 ,0.005,self.inf_n] # RETROCESO DEL DIAMANTE 
        
    


        # ==================================
        # =========== PUT R2-FAST========== 
        # ==================================
        # COMPRA
        
        self.dput_r2_fast = [ 0.21, 0.43]
        self.doput_r2_fast = [0.055, 0.065]
        self.timePut_r2_fast = [dt_time(9, 34), dt_time(9, 35,30)]
        self.labelPut_r2_fast=1

        # VENTA
        self.sl_pr2_fast=-0.045  # STOP LOSS
        # min_desicion_pr2_fast  = 60
        self.umbral_manifestacion_pR2_fast=0.018
        self.diamante_pr2_fast = [self.umbral_manifestacion_pR2_fast, 0.025,0.04] # DIAMANTE DE COMPRA
        self.resta_pr2_fast = [0.01,0.005,0.001 ] # RETROCESO DEL DIAMANTE 


        #########################################################
        ####################      LABELS      ###################
        #########################################################
        
        self.omega=0.00000297000000
        self.alpha=0.027400000
        self.beta=0.90520000
        self.gamma=0.11470000
        self.days_year=252

