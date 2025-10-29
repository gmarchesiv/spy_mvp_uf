# ====================
#  - Librerías -
# ====================

from datetime import datetime  # Importa la clase datetime desde el módulo datetime
import pytz  # Importa el módulo pytz para manejar zonas horarias

# ====================
#  - Funciones -
# ====================


# Función para imprimir con marca de tiempo de Nueva York
def printStamp(msg):

    #---------------------------------------------------
    '''
    Genera un log con la hora de New York.
    '''
    #---------------------------------------------------

    zone = pytz.timezone("America/New_York")
    # Obtiene la marca de tiempo actual en Nueva York
    timestamp = datetime.now(zone).strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-4] + "]"
    # Imprime la marca de tiempo y el mensaje proporcionado
    print(timestamp, msg)

def readIBData(app, vars,varsLb):

    #---------------------------------------------------
    '''
    Genera un Log de lo que esta pasando alli mismo.
    '''
    #---------------------------------------------------



    vars.promedio_call = sum(vars.askbid_call_prom) / len(vars.askbid_call_prom) if len(vars.askbid_call_prom)!=0 else 0
    vars.promedio_put = sum(vars.askbid_put_prom) / len(vars.askbid_put_prom) if len(vars.askbid_put_prom)!=0 else 0

    print("===============================================")
 
    printStamp(f"{app.etfs[5]['symbol']} : $ {app.etfs[5]['price']}")
    printStamp(f"{app.etfs[6]['symbol']} :   {app.etfs[6]['price']}")
    printStamp(f"LABEL:   {varsLb.label}")

    print("-----------------------------------------------")

    printStamp(f"{app.options[1]['symbol']}")
    printStamp(f"ASK :{vars.cask } | DCALL :{round(vars.dcall*100,2)}%")
    printStamp(f"BID :{vars.cbid} | DOCALL :{round(vars.docall*100,2)}%")
    printStamp(f"ASK/BID-CALL : {round(vars.askbid_call*100,2)}%")
    printStamp(f"A/B-CALL_PROM: {round(vars.promedio_call*100,2)}%")
    print("-----------------------------------------------")

    printStamp(f"{app.options[2]['symbol']}")
    printStamp(f"ASK :{vars.pask} | DPUT :{round(vars.dput*100,2)}%")
    printStamp(f"BID :{vars.pbid} | DOPUT :{round(vars.doput*100,2)}%")
    printStamp(f"ASK/BID-PUT : {round(vars.askbid_put*100,2)}%")
    printStamp(f"A/B-PUT_PROM: {round(vars.promedio_put*100,2)}%")
    

 
def read_rentabilidad(vars):
    print("===============================================")
    printStamp(f"Rentabilidad: {round(vars.rentabilidad*100,2)}%")
 
def read_buy(vars):
    print("===============================================")
    printStamp(f"-COMPRA EXITOSA -")
    printStamp(f"STATUS: {vars.status} ")
    printStamp(f"REGLA: {vars.regla} ")
    printStamp(f"TIPO: {vars.tipo} ")
    printStamp(f"CONTRATOS: {vars.quantity} ")
 
def read_sell(vars,tipo):
    print("===============================================")
    printStamp(f"-VENTA EXITOSA -")
    if tipo == "C":
        tipo_name="CALL"
    elif tipo == "P":
        tipo_name="PUT"
    printStamp(f"TIPO: {tipo_name} ")
    printStamp(f"REGLA: {vars.regla} ")
    printStamp(f"STATUS: {vars.status} ")
    printStamp(f"CONTRATOS: {vars.quantity} ")
    
   
 

def readIBData_action(app, vars, tipo, regla):
    print("===============================================")
    for cash in app.wallet:
        printStamp(f"{cash}  : {app.wallet[cash]} $ ")
    print("===============================================")
    print("-----------------------------------------------")
    if tipo == "C":
        tipo_name = "CALL"
    else:
        tipo_name = "PUT"
    if vars.compra == True:
        printStamp(f"-COMPRA - {tipo_name} : {regla}")
    else:
        printStamp(f"-VENTA - {tipo_name} : {regla}")

 
    if tipo == "C":
        print("-----------------------------------------------")

        cask = app.options[1]["ASK"]
        cbid = app.options[1]["BID"]
    

        printStamp(f"{app.options[1]['symbol']}")
        printStamp(f"ASK :{cask } | DCALL :{round((cbid / vars.call_close - 1)*100,2)}%")
        printStamp(f"BID :{cbid} | DOCALL :{round((cbid / vars.call_open - 1)*100,2)}%")
        printStamp(f"ASK/BID_CALL : {round((cask / cbid - 1)*100,2)}%")

    else:
        print("-----------------------------------------------")
    
        pask = app.options[2]["ASK"]
        pbid = app.options[2]["BID"]
        printStamp(f"{app.options[2]['symbol']}")
        printStamp(f"ASK :{pask} | DPUT :{round((pbid / vars.put_close - 1)*100,2)}%")
        printStamp(f"BID :{pbid} | DOPUT :{round((pbid / vars.put_open - 1)*100,2)}%")
        printStamp(f"ASK/BID_PUT : {round((pask / pbid - 1)*100,2)}%")