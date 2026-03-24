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
        inf = 9999
        inf_n = -9
 
        # SELECCION DE STRIKES 
        self.rangos_strikes = [[2, 2.6] ]
        self.days_min_exp = 31  # DIAS para el exp minimo de busqueda
        self.days_max_exp = 39 
        self.except_days_min_exp = 26

        # PARAMETROS DE ASKBID DE ACCIONES
        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028
        self.max_askbid_venta_abs = 0.0255
        self.max_askbid_compra_abs = 0.0185
        self.max_askbid_venta_forzada = 0.04
        self.max_askbid_compra_alt = 0.02

        # PARAMETROS LIMITES DE OPEN ASKBID
        self.max_askbid_open = 0.03
        self.max_askbid_hora_open =  dt_time(9, 33)
        self.umbral_askbid=0.08

        # PARAMETROS DE COMPRA VENTA SLIPPAGE
        self.slippage=1.045

        #PARAMETROS DE TIEMPO DE RUTINA Y MUESTRAS
        self.fin_rutina = dt_time(15, 55)
        self.fd =  dt_time(15, 45)
        self.rutina = [dt_time(6, 50), dt_time(16, 0)]
        self.frecuencia_accion =[i for i in range(0, 60, 2)]
        
        #PARAMETROS DE VENTA 
        self.intentos=1
        self.tiempo_contulta=5

        #PARAMETROS DE PROTECCION
        self.proteccion_ask_bid=[[dt_time(9, 45,0), dt_time(9, 45,18)],[dt_time(10, 0,0), dt_time(10,0,18 )]]
        self.proteccion_compra=[ dt_time(9, 44,30), dt_time(9, 45,30) ]
        self.proteccion_compra_2=[ dt_time(9, 59,20), dt_time(10, 0,15) ]
        self.proteccion_compra_call_r1=[ dt_time(9, 44,0), dt_time(9, 45,12)  ]

 
        # ==================================
        # =========== CALL PROTECCION ======  
        # ==================================
    
        self.umbral_no_perdida_c = 0.016
        self.perdida_maxima_c = 0.05
        self.perdida_maxima_c_dinamico_r2 = 0.043
        self.perdida_maxima_c_abs = -0.021
        
      
 

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.016
        self.perdida_maxima_p = 0.05
        self.perdida_maxima_p_abs = -0.021
        self.perdida_maxima_p_dinamico_r2 = 0.043

 


   
        #########################################################
        ####################      LABELS      ###################
        #########################################################
       
     

        self.omega=0.00000233

        self.alpha=0.00280000

        self.beta=0.89020000

        self.gamma=0.17930000

        self.days_year=252



        #########################################################
        ####################      CALL        ###################
        #########################################################
 
 
        #########################################################
        self.C_r1={
            "REGLA":"R1",
            "TIPO":"CALL",
            "D":[0.06, 0.137],
            "DO":[0.0265, 0.031],
            "DPUT":[-0.25, -0.0965],
            "TIME":[ dt_time(9, 35) , dt_time(9, 47)],
            "LABEL":0,

            "SL":-0.045,
            "DIAMANTE":[0.02 ,0.025,0.03,0.06  ],
            "RESTA":[0.008 ,0.005, 0.003, 0.001],
            
            "NMT":inf,
            "TARGET_NMT":inf
            } 
        #########################################################
        self.C_r1_2={
            "REGLA":"R1-2",
            "TIPO":"CALL",
            "D":[-0.052 , 0.046 ],
            "DO":[0.03, 0.04],
            "DPUT":[-0.14, 0.04],
            "TIME":[ dt_time(9, 47) , dt_time(9, 50,30)],
            "LABEL":0,

            "SL":-0.035 ,
            "DIAMANTE":[ 0.02,0.028,0.04 ],
            "RESTA":[  0.015,0.005 ,0.001 ] ,


            "NMT":inf,
            "TARGET_NMT":inf
            } 
            
        #########################################################
        self.C_r3={
            "REGLA":"R3",
            "TIPO":"CALL",
            "D":[ 0.18, 0.252],
            "DO": [0.031, 0.05],
            "DPUT":[-0.33, -0.135],
            "TIME": [dt_time(9, 35), dt_time(9, 42)],
            "LABEL":0,

            "SL":-0.037,
            # "DIAMANTE":[0.0165 ,0.025,0.035,0.05] ,
            # "RESTA": [0.015, 0.005,0.003,0.001],
            "DIAMANTE":[0.018 ,0.036,0.05] ,
            "RESTA": [0.015, 0.005,0.001],


            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_r3_2={
            "REGLA":"R3-2",
            "TIPO":"CALL",
            "D":[ 0.19, 0.43],
            "DO": [0.0425, 0.05],
            "DPUT":[-0.46, -0.135],
            "TIME":  [dt_time(10, 16,40), dt_time(10, 40)],
            "LABEL":0,

            "SL":-0.04,
                "DIAMANTE":[0.0165 ,0.025,0.035,0.05] ,
            "RESTA": [0.015, 0.005,0.003,0.001],
            # "DIAMANTE":[0.0165,0.026,0.036] ,
            # "RESTA": [0.015,0.005,0.001],

            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_r1_e={
            "REGLA":"R1-E",
            "TIPO":"CALL",
            "D":[-0.12,0.015],
            "DO": [0.085, 0.092],
            "DPUT":[-0.1, 0.075],
            "TIME":[dt_time(10, 24), dt_time(11, 5)],
            "LABEL":0,
            

            "SL":-0.04,
            "DIAMANTE":[0.02,0.03,0.04,0.06,0.07 ],
            "RESTA":[0.015,0.01,0.005, 0.003, 0.001],
            # "DIAMANTE":[0.027,0.05 ,0.07  ],
            # "RESTA": [0.013,0.01 , 0.001],

            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################  
        self.C_fast={
            "REGLA":"FAST",
            "TIPO":"CALL",
            "D":[-0.025, 0.09],
            "DO":[0.05, 0.052],
            "DPUT":[ -0.16,0.05],
            "TIME":[dt_time(9, 38,30), dt_time(9, 44 )],
            "LABEL":0,

            "SL":-0.042,
            "DIAMANTE":[0.017,0.025, 0.03 ,0.04] ,
            "RESTA":[   0.01,0.005,0.003,0.001 ] ,
            # "DIAMANTE":[0.02,0.025, 0.03 ,0.04] ,
            # "RESTA":[ 0.005,0.01,0.005,0.001 ] ,

            "NMT":inf,
            "TARGET_NMT":inf
            }



        #########################################################
        self.C_inv_1={
            "REGLA":"INV-1",
            "TIPO":"CALL",
            "D":[-0.164, -0.05],
            "DO":[0.054, 0.059],
            "DPUT":[0.04, 0.28],
            "TIME":[dt_time(9, 33), dt_time(9, 39)],
            "LABEL":1,


            "SL":-0.05,
            "DIAMANTE":[ 0.023,0.05,0.08] ,
            "RESTA":[ 0.01,0.005,0.001],

            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_inv_2={
            "REGLA":"INV-2",
            "TIPO":"CALL",
            "D":[-0.36, -0.20],
            "DO":[0.03, 0.038] ,
            "DPUT":[0.01, 0.46],
            "TIME":[dt_time(9, 35), dt_time(9, 50)],
            "LABEL":1,


            "SL":-0.04,
            "DIAMANTE":[ 0.023,0.05,0.08] ,
            "RESTA":[ 0.01,0.005,0.001],
            # "DIAMANTE":[0.029,0.04,0.06 ] ,
            # "RESTA": [0.015,0.005,0.001 ],


            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_r1_c={
            "REGLA":"R1-C",
            "TIPO":"CALL",
            "D":[-0.2, 0.095],
            "DO":[0.0325, 0.035] ,
            "DPUT":[-0.084, 0.045] ,
            "TIME": [dt_time(11, 30), dt_time(12, 15)],
            "LABEL":0,

            

            "SL":-0.046,
            "DIAMANTE":[0.02,0.027,0.06,0.08],
            "RESTA":   [0.016,0.01 ,0.005,0.001],


            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_r2={
            "REGLA":"R2",
            "TIPO":"CALL",
            "D":[0.3, 0.435],
            "DO":[0.042, 0.05]  ,
            "DPUT":[-0.46, -0.21],
            "TIME":[dt_time(9, 36), dt_time(9,56)],
            "LABEL":0,
            "UMBRAL_R2":0.25,      

            "SL":-0.04,
            # "DIAMANTE":[0.02,0.025, 0.03 ,0.04] ,
            # "RESTA":[   0.01,0.005,0.003,0.001 ] ,
            "DIAMANTE":[0.02,0.027,0.038],
            "RESTA":[0.018,0.005,0.001] ,

            

            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTADA
        self.C_r2_2={
            "REGLA":"R2-2",
            "TIPO":"CALL",
            "D":[0.3, 0.435],
            "DO":[0.044, 0.048] ,
            "TIME": [dt_time(10, 16), dt_time(10, 40)],
            "LABEL":0,

            "SL":-0.04,
            "DIAMANTE":[0.02,0.027,0.038] ,
            "RESTA":[0.018,0.005,0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }


        #########################################################
        self.C_f1={
            "REGLA":"F1",
            "TIPO":"CALL",
            "D":[-0.06, 0.15],
            "DO": [0.0325, 0.036],
            "DPUT":[-0.25, -0.03],
            "TIME":[dt_time(13, 30), dt_time(14, 0)],
            "LABEL":0,

            "SL":-0.045,
            # "DIAMANTE":[0.015, 0.02,0.03],
            # "RESTA":   [0.01 ,0.005,0.001]   ,
            "DIAMANTE":[0.015,0.02 ] ,
            "RESTA":[0.01 , 0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTADA
        self.C_f2={
            "REGLA":"F2",
            "TIPO":"CALL",
            "D":[0.05, 0.16],
            "DO":[0.07, 0.09],
            "DPUT":[-0.2, 0.06],
            "TIME":[dt_time(13, 13), dt_time(14, 50)],
            "LABEL":0,

            "SL":-0.04,
            "DIAMANTE":[0.018,0.024] ,
            "RESTA":[0.015, 0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTADA
        self.C_f3={
            "REGLA":"F3",
            "TIPO":"CALL",
            "D":[0.05, 0.15],
            "DO":[0.033, 0.04],
            "TIME":[dt_time(14, 0), dt_time(14, 8)],
            "LABEL":0,

            "SL":-0.03,
            "DIAMANTE":[0.0165,0.027,0.034 ] ,
            "RESTA":[0.015,0.01,0.001]  ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTADA
        self.C_f4={
            "REGLA":"F4",
            "TIPO":"CALL",
            "D":[-0.21, -0.07],
            "DO": [0.03, 0.035],
            "TIME":[dt_time(12, 9), dt_time(12, 15)],
            "LABEL":0,

            "SL":-0.03,
            "DIAMANTE":[0.02,0.027,0.0375 ] ,
            "RESTA":[0.015,0.01,0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }


        #########################################################
        self.C_label_1={
            "REGLA":"LABEL-1",
             "TIPO":"CALL",
            "D":[ -0.1, -0.01],
            "DO":[-0.21, 0.15],
            "DPUT":[0, 0.09],

            "TIME":[dt_time(9, 50), dt_time(10, 40,5)],
            "TIME-FIN":dt_time(10, 45),
            "LABEL":0,

            "UMBRAL_COMPRA":[0.002,0.005],

            "SL":-0.05,
            "DIAMANTE":[0.014,0.025 ,0.03,0.04],
            "RESTA":[0.014,0.005  , 0.003  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.C_label_2={
            "REGLA":"LABEL-2",
            "TIPO":"CALL",
            "D":[ -0.25, -0.14],
            "DO":[-0.375, 0.02],
            "DPUT":[0.07, 0.28],

            "TIME":[dt_time(11,5), dt_time(11, 45,5)],
            "TIME-FIN":dt_time(11, 50),
            "LABEL":0,

            "UMBRAL_COMPRA":[0.002,0.005],

            "SL":-0.05,
            "DIAMANTE":[0.013,0.025 ,0.03,0.04],
            "RESTA":[0.01 ,0.005  , 0.003  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }




        #########################################################
        ####################      PUT         ###################
        #########################################################
        #########################################################
        self.P_r1={
            "REGLA":"R1",
            "TIPO":"PUT",
            "D": [0.04, 0.137],
            "DO":[0.0365, 0.06 ],
            "DCALL": [-0.13, -0.02],
            "TIME":[dt_time(9, 50), dt_time(9, 56)],
            "LABEL":1,

            "SL":-0.035,
            "DIAMANTE":[0.02, 0.03,0.045,0.07 ] ,
            "RESTA": [0.017, 0.01,0.005 , 0.001],


            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.P_inv_1={
            "REGLA":"INV-1",
            "TIPO":"PUT",
            "D":[-0.18, -0.073],
            "DO":[0.047, 0.05],
            "DCALL": [0, 0.16],
            "TIME": [dt_time(9, 34), dt_time(9,38)],
            "LABEL":0,

            "SL":-0.05,
            "DIAMANTE":[0.016,0.0255,0.034,0.04,0.045] ,
            "RESTA":   [0.015,0.01,0.005,0.003,0.001],
            # "DIAMANTE":[0.016,0.026,0.034,0.07,0.11] ,
            # "RESTA":[0.015,0.01,0.005,0.005,0.001],

            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.P_inv_2={
            "REGLA":"INV-2",
            "TIPO":"PUT",
            "D":[-0.022, 0.01],
            "DO":[0.03, 0.039],
            "DCALL": [-0.11, 0.08],
            "TIME":[dt_time(9, 34,30), dt_time(9,38,30)],
            "LABEL":0,


            "SL":-0.045,
            "DIAMANTE":[0.02 ,0.023,0.03 ,0.04],
            "RESTA":[0.012 ,0.005 ,0.003,0.001  ],
            

            "NMT":inf,
            "TARGET_NMT":inf
            }


        #########################################################
        self.P_inv_3={
            "REGLA":"INV-3",
            "TIPO":"PUT",
            "D":[-0.055, 0.085],
            "DO":[0.045, 0.055],
            "DCALL": [-0.112, 0.02],
            "TIME":[dt_time(9, 43,30), dt_time(9,46,30)],
            "LABEL":0,

            "SL":-0.045,
            "DIAMANTE":[0.016,0.026,0.034,0.04,0.05] ,
            "RESTA":   [0.015,0.01,0.005,0.003,0.001],
            # "DIAMANTE":[0.02 ,0.04,0.06,0.08 ],
            # "RESTA":[0.012 ,0.01 ,0.005,0.001 ],

            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################
        self.P_inv_4={
            "REGLA":"INV-4",
            "TIPO":"PUT",
            "D":[-0.055,0],
            "DO":[0.045, 0.055],
            "DCALL": [-0.03, 0.08],
            "TIME":[dt_time(9, 49,30), dt_time(10,8)],
            "LABEL":0,

            "SL":-0.04 ,
            "DIAMANTE":[0.016 ,0.02,0.028   ],
            "RESTA":[0.01 ,0.005 , 0.001 ],

            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################

        self.P_r2={
            "REGLA":"R2",
            "TIPO":"PUT",
            "D":[0.28, 0.40]  ,
            "DO":[0.057, 0.065]   ,
            "DCALL": [-0.32, -0.17],
            "TIME":[dt_time(9, 46), dt_time(9, 55)],
            "LABEL":1,
            "UMBRAL_R2":0.2,  

            "SL":-0.035,
            "DIAMANTE":[0.02, 0.026,0.035 ],
            "RESTA":[0.015,0.01,0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.P_r2_e={
            "REGLA":"R2-E",
            "TIPO":"PUT",
            "D":[0.427, 0.53]  ,
            "DO":[0.04, 0.055]   ,
            "DCALL": [-0.48, -0.23],
            "TIME":[dt_time(9, 34,45), dt_time(10, 2)],
            "LABEL":1,


            "SL":-0.035,
            "DIAMANTE":[0.019] ,
            "RESTA":[inf_n] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
            
        #########################################################
        self.P_r3={
            "REGLA":"R3",
            "TIPO":"PUT",
            "D":[ 0.175, 0.2],
            "DO": [0.03, 0.036],
            "DCALL": [-0.21, -0.09],
            "TIME":[dt_time(9, 34), dt_time(9, 41)],
            "LABEL":1,


            "SL":-0.04,
            "DIAMANTE":[0.018,0.03,0.05,0.07 ],
            "RESTA":[0.012,0.01,0.005,0.003],
            # "DIAMANTE":[0.018,0.03,0.06,0.07 , 0.08],
            # "RESTA":[0.012,0.015,0.01,0.005,0.001],



            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################
        self.P_label_1={
            "REGLA":"LABEL-1",
            "TIPO":"PUT",
            "D":[ 0.04, 0.145],
            "DO":[0.03, 0.0385],
            "DCALL": [-0.2, -0.02],
            "TIME":[dt_time(10,2), dt_time(10, 22)],
            "LABEL":1,

            "SL":-0.043,
            # "DIAMANTE":[0.0165,0.025 ,0.04,0.07,0.088],
            # "RESTA":[0.012,0.01  ,0.008  ,0.005  ,inf_n ] ,

            "DIAMANTE":[0.0165,0.025 ,0.04,0.06 ],
            "RESTA":[0.012,0.01  ,0.005  ,0.001    ] ,

            #  "SL":-0.1,
            # "DIAMANTE":[0.08,0.1] ,
            # "RESTA": [0.01 ,0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }


        #########################################################
        self.P_label_2={
            "REGLA":"LABEL-2",
            "TIPO":"PUT",
            "D":[ -0.035, 0.24],
            "DO":[0.043, 0.11],
            "DCALL":[ -0.3, -0.12],
            "UMBRAL_COMPRA":[0.002,0.005],
            "TIME":[dt_time(9, 40), dt_time(10, 30,5)],
            "TIME-FIN":dt_time(10, 35),
            "LABEL":1,

            "SL":-0.045,
            "DIAMANTE":[ 0.02 ,0.024 ,0.03 ,0.04 ],
            "RESTA":[ 0.01 , 0.005 , 0.003 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################
        self.P_label_3={
            "REGLA":"LABEL-3",
            "TIPO":"PUT",
            "D":[ -0.05, 0.41],
            "DO":[0.11, 0.34],
            "DCALL":[-0.38 , 0.01], 
            "UMBRAL_COMPRA":[0.002,0.005],
            "TIME":[dt_time(9, 45), dt_time(10, 45,5)],
            "TIME-FIN":dt_time(10, 50),
            "LABEL":1,

            "SL":-0.05,
            "DIAMANTE":[ 0.02 ,0.024 ,0.03 ,0.04 ],
            "RESTA":[ 0.01 , 0.005 , 0.003 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################
        self.P_label_4={
            "REGLA":"LABEL-4",
            "TIPO":"PUT",
            "D":[ -0.35, 0.12],
            "DO":[0.06, 0.22],
            "DCALL":[-0.15 , 0.46], 
            "UMBRAL_COMPRA":[0.002,0.005],
            "TIME":[dt_time(11, 15), dt_time(11, 50,5)],
            "TIME-FIN":dt_time(11, 55),
            "LABEL":1,

            "SL":-0.05,
            "DIAMANTE":[ 0.02 ,0.024 ,0.03 ,0.04 ],
            "RESTA":[ 0.01 , 0.005 , 0.003 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }

        #########################################################
        self.P_f1={
            "REGLA":"F1",
            "TIPO":"PUT",
            "D":[ -0.025, 0.124],
            "DO":[0.05, 0.065],
            "DCALL": [-0.18, -0.08],
            "TIME":[dt_time(14, 32), dt_time(14, 42)],
            # "LABEL":1,

            "SL":-0.05,
            "DIAMANTE":[0.019,0.03 ,0.04 ],
            "RESTA":[0.01 ,0.005  ,0.001 ] ,

            #  "SL":-0.1,
            # "DIAMANTE":[0.08,0.1] ,
            # "RESTA": [0.01 ,0.001],

            "NMT":inf,
            "TARGET_NMT":inf
            }
