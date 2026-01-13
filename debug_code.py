###################################################
################### LIBRERIAS  ####################
###################################################
 
import pandas as pd
import multiprocessing
import time
import asyncio
from datetime import datetime
import os
# config/
from config.IB.connection import test_ibkr_connection, ibkr_connection, load_app_vars
from config.IB.wallet import wallet_config 
from config.params import parameters
from config.vars.rutina import varsRutina
from config.vars.broadcasting import varsBroadcasting
from config.vars.app import varsApps
from config.vars.label import varsLabel

# DataBase
from database.repository.repository import writeRegister

# funtions/
from functions.broadcasting import *
from functions.clean import clean_broadcasting, clean_vars
from functions.events import countdown, isTradingDay
from functions.labels import generar_label
from functions.logs import *
from functions.notifications import sendError, sendStart
from functions.saveVars import saveVars

# rules/
from rules.buy import buyOptions
from rules.routine import (
    data_option_open,
    calculations,
    data_option_open,
    data_susciption,
    registration,
    registro_strike,
    saveTransaction 
)
 
 
# database/
from database.repository.repository import *
from rules.sell import sellOptions

class App:
    def __init__(self):
        # options es un diccionario:
        #  claves: 0, 1, 2
        #  valor: diccionario con contract y symbol
        self.options = {
            0: {"contract": None, "symbol": None},
            1: {"contract": None, "symbol": None},
            2: {"contract": None, "symbol": None},
        }


def debug_code(archivos):
    
    
    
    # ================================
    #  - Variables y Parametros -
    # ================================

    # VARIABLES
    vars = varsRutina(debug_mode=True)

    varsBc = varsBroadcasting(debug_mode=True)

    varsLb=varsLabel(debug_mode=True)

    varsApp=varsApps(debug_mode=True)

    # PARAMETROS
    params = parameters(debug_mode=True)

    app = App()
    

    file="C:/Users/Usuario/Desktop/modelos/alpha_spy_options/dataset_2s"
    
    vars.archivo=os.path.basename(archivos)
    printStamp(f" - Archivo :{vars.archivo}- ")
    
    df=pd.read_csv(archivos)

    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%Y-%m-%d")

    # Verificamos el mes
    if (df["FECHA"].dt.month == 1).any() and (df["FECHA"].dt.year == 2026).any():
        pass
    
        
    else:
        return  

    df["HORA"] = pd.to_datetime(df["HORA"], format="%H:%M:%S").dt.time
    df["MINUTO_HORA"] = pd.to_datetime(df["HORA"], format="%H:%M:%S").dt.minute

    df["RENT"] = None
    df["REGLA"] = ""
    df["TIPO"] = ""

    vars.df=df.copy()

    
    for i in range(df.shape[0]):
        vars.i=i

        if int(df["HORA"][i].second ) == 0:
            vars.minutos += 1
            vars.n_minutos += 1
            vars.minutos_trade += 1


        if  i ==0 or df["FECHA"][i] != df["FECHA"][i-1]  :
            clean_vars(vars,varsApp)

        
        vars.cask = df["CASK"][i]
        vars.cbid = df["CBID"][i]
        vars.pask = df["PASK"][i]
        vars.pbid = df["PBID"][i]

        vars.askbid_call = df["ASKBID_CALL"][i]
        vars.askbid_put = df["ASKBID_PUT"][i]
        vars.dcall = df["DCALL"][i]
        vars.dput = df["DPUT"][i]
        vars.docall = df["DOCALL"][i]
        vars.doput = df["DOPUT"][i]
        varsLb.label= df["LABEL"][i]

        if vars.askbid_call >0 and params.umbral_askbid>vars.askbid_call:
            vars.askbid_call_prom.append(vars.askbid_call)

        if vars.askbid_put >0 and params.umbral_askbid>vars.askbid_put:
            vars.askbid_put_prom.append(vars.askbid_put)

     
        if vars.rule:
            if vars.dcall >= params.umbral_cr2:
                vars.flag_Call_R2 = True
            if vars.dput >= params.umbral_pr2:
                vars.flag_Put_R2 = True
    
            vars.rule = False
 
        # ================================
        #  -VENTA-
        # ================================
        if vars.call or vars.put:
            sellOptions(app,varsBc,varsLb,vars,params,debug_mode=True)
        # ================================
        #  -COMPRA-
        # ================================
        if vars.compra:
            buyOptions(app,varsBc,varsLb,vars,params, debug_mode=True)
        pass
        vars.label_ant=varsLb.label

    df_aux = pd.DataFrame()
    df_aux["FECHA_C"] = vars.df["FECHA"]
    df_aux["HORA_C"] = vars.df["HORA"]
    # df_aux["FECHA_V"] = vars.df["FECHA"]
    df_aux["HORA_V"] = vars.df["HORA"]
    df_aux["REGLA"] = vars.df["REGLA"]
    df_aux["TIPO"] = vars.df["REGLA"]
    df_aux["TIPO R"] = vars.df["TIPO"]

    df_aux["RENTABILIDAD"] = vars.df["RENT"]

    df_aux_3 = df_aux.copy()
    df_aux_3 = df_aux_3[(df_aux_3["REGLA"] == "PUT") | (df_aux_3["REGLA"] == "CALL")]
    df_aux_3.reset_index(drop=True, inplace=True)

    df_aux = df_aux[df_aux["REGLA"] != ""]
 
    df_aux = df_aux[df_aux["REGLA"] != "PUT"]
    df_aux = df_aux[df_aux["REGLA"] != "CALL"]
    df_aux.reset_index(drop=True, inplace=True)

    df_aux["FECHA_C"] = df_aux_3["FECHA_C"]
    df_aux["HORA_C"] = df_aux_3["HORA_C"]
    df_aux["TIPO"] = df_aux_3["TIPO"]
    df_aux["TIPO R"] = df_aux_3["TIPO R"]

    nombre_archivo = vars.archivo 
    solo_nombre = nombre_archivo.split(".")[0]
    writer = pd.ExcelWriter( f"resultados_test/{solo_nombre}.xlsx", engine="xlsxwriter") 
    # if vars.archivo =="07-2025.csv":
    #     vars.df.to_excel(writer, sheet_name="DATA", index=True)
    df_aux.to_excel(writer, sheet_name="Resultados", index=True)
 
    writer.close()
    
    return
         


if __name__ == "__main__":
    # ###########################
    # #### INICIO DEL CODIGO ####
    # ###########################
 

    file= "C:/Users/Usuario/Desktop/modelos/alpha_spy_options/dataset_2s/" 
    
    printStamp(f" - Carpeta de Origen : {file} - ")
    archivos = [
    os.path.join(file, f)
    for f in os.listdir(file)
    if os.path.isfile(os.path.join(file, f))
]
    # print(archivos)
 
    pool = multiprocessing.Pool()
    pool.map(debug_code, archivos)
    pool.close()
    pool.join()
   