


import math
from collections import deque
import pandas_ta as ta 
import pandas as pd  
import joblib

from database.repository.repository import writeLabel      

def generar_label(params, vars,app):
   
    generar_garch(params, vars,app)
   
    generar_hour_back(params, vars,app)
    
    generar_rsi(params, vars,app)
  
    generar_d_pico(params, vars,app)
 



    clusterizar(params, vars,app)
    
    pass



def generar_garch(params, vars,app):
    vars.varianza=params.omega+(params.alpha+params.gamma*vars.signo)*  math.pow(vars.retorno-params.mu, 2) +params.beta*vars.varianza
    
    vars.garch=round(100* math.sqrt(  params.days_year*vars.varianza),4)
   
    
    vars.signo=1 if (vars.retorno-params.mu)>0 else 0
 
    vars.retorno_lista.append(app.etfs[5]['price'])
 
    vars.retorno=app.etfs[5]['price'] / vars.retorno_lista[0] -1
    

 

def generar_hour_back(params, vars,app):
    vars.ret_1H_back.append(app.etfs[5]['price'])
    vars.ret_3H_back.append(app.etfs[5]['price'])
    vars.ret_6H_back.append(app.etfs[5]['price'])
    vars.ret_12H_back.append(app.etfs[5]['price'])
    vars.ret_24H_back.append(app.etfs[5]['price'])
    vars.ret_96H_back.append(app.etfs[5]['price'])
    pass

def generar_rsi(params, vars,app):
    vars.etf_price_lista.append(app.etfs[5]['price'])
    print()
    if len(vars.etf_price_lista)<4:
        vars.rsi=0

    else:
        df=pd.DataFrame({"price":vars.etf_price_lista})
        df["rsi"]=ta.rsi(df["price"])
        df["rsi_prom_3"]=df["rsi"]*0.5+df["rsi"].shift(1)*0.25+df["rsi"].shift(2)*0.25
 
        vars.rsi=float(df["rsi_prom_3"].iloc[-1])
    pass

def generar_d_pico(params, vars,app):
    if app.etfs[5]['price'] > vars.pico_etf:
        vars.pico_etf=app.etfs[5]['price']

    vars.d_pico=app.etfs[5]['price']/vars.pico_etf -1

    pass


def clusterizar(params, vars,app):
    scaler = joblib.load('/usr/src/app/functions/scaler.joblib')
    km = joblib.load('/usr/src/app/functions/model.joblib')

    df=pd.DataFrame(

        {
            "VIX_CLOSE":[app.etfs[6]['price']],
            "QQQ_GARCH":[vars.garch],
            "ret_1H_back":[(app.etfs[5]['price']/ vars.ret_1H_back[0] -1)],
            "ret_3H_back":[(app.etfs[5]['price']/ vars.ret_3H_back[0] -1)],
            "ret_6H_back":[(app.etfs[5]['price']/ vars.ret_6H_back[0] -1)],
            "ret_12H_back":[(app.etfs[5]['price']/ vars.ret_12H_back[0] -1)],
            "ret_24H_back":[(app.etfs[5]['price']/ vars.ret_24H_back[0] -1)],
            "ret_96H_back":[(app.etfs[5]['price']/ vars.ret_96H_back[0] -1)],
            "rsi_prom_3":[vars.rsi],
            "D_PICO":[vars.d_pico]
        }
    )
 
    X = df.copy()
    df_final = X.copy()
    # Usar en nuevos datos
    X_s = scaler.transform(X)
    labels = km.predict(X_s)
    df_final["LABELS"] = labels
    df_final.reset_index(drop=True,inplace=True)
    vars.label=df_final["LABELS"][0]
 
    writeLabel(app, vars,params)