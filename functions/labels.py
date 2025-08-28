


import math
from collections import deque
import pandas_ta as ta 
import pandas as pd   
import joblib
from sklearn.cluster import KMeans
import asyncio
from database.repository.repository import writeLabel
from functions.saveJson import saveLabel      

def generar_label(params, varsLb,app):
   
    #---------------------------------------------------
    '''
    Generamos todas las variables involucradas en la
    preddicon del Label para finalmente generar
    el Label.
    '''
    #---------------------------------------------------

    generar_garch(params, varsLb,app)
    
    generar_rsi(params, varsLb,app)
  
    generar_d_pico(params, varsLb,app)
  
    clusterizar(params, varsLb,app)

    generar_hour_back(params, varsLb,app)
    
    pass



def generar_garch(params, varsLb,app):


    varsLb.varianza=params.omega+(params.alpha+params.gamma*varsLb.signo)*  math.pow(varsLb.retorno-varsLb.mu, 2) +params.beta*varsLb.varianza
    
    varsLb.garch=round(100* math.sqrt(  params.days_year*varsLb.varianza),4)
   
    
    varsLb.signo=0 if (varsLb.retorno-varsLb.mu)>0 else 1
 
    varsLb.retorno_lista.append(app.etfs[5]['price'])
 
    varsLb.retorno=app.etfs[5]['price'] / varsLb.retorno_lista[0] -1
    

    varsLb.mu= ((varsLb.mu*varsLb.mu_conteo) + varsLb.retorno)/(varsLb.mu_conteo+1)
    varsLb.mu_conteo=varsLb.mu_conteo+1

 

def generar_hour_back(params, varsLb,app):
    varsLb.ret_1H_back.append(app.etfs[5]['price'])
    varsLb.ret_3H_back.append(app.etfs[5]['price'])
    varsLb.ret_6H_back.append(app.etfs[5]['price'])
    varsLb.ret_12H_back.append(app.etfs[5]['price'])
    varsLb.ret_24H_back.append(app.etfs[5]['price'])
    varsLb.ret_96H_back.append(app.etfs[5]['price'])
    pass

def generar_rsi(params, varsLb,app):
    varsLb.etf_price_lista.append(app.etfs[5]['price'])
   
    if len(varsLb.etf_price_lista)<4:
        varsLb.rsi=0

    else:
        df=pd.DataFrame({"price":varsLb.etf_price_lista})
        df["rsi"]=ta.rsi(df["price"])
        df["rsi_prom_3"]=df["rsi"]*0.5+df["rsi"].shift(1)*0.25+df["rsi"].shift(2)*0.25
 
        varsLb.rsi=float(df["rsi_prom_3"].iloc[-1])
    pass

def generar_d_pico(params, varsLb,app):
    if app.etfs[5]['price'] > varsLb.pico_etf:
        varsLb.pico_etf=app.etfs[5]['price']

    varsLb.d_pico=app.etfs[5]['price']/varsLb.pico_etf -1

    pass


def clusterizar(params, varsLb,app):
    
    
    scaler = joblib.load('/usr/src/app/functions/scaler.joblib')
    km = joblib.load('/usr/src/app/functions/model.joblib')

    df=pd.DataFrame(

        {
            "VIX_CLOSE":[app.etfs[6]['price']],
            "SPY_GARCH":[varsLb.garch],
            "ret_1H_back":[(app.etfs[5]['price']/ varsLb.ret_1H_back[0] -1)*100],
            "ret_3H_back":[(app.etfs[5]['price']/ varsLb.ret_3H_back[0] -1)*100],
            "ret_6H_back":[(app.etfs[5]['price']/ varsLb.ret_6H_back[0] -1)*100],
            "ret_12H_back":[(app.etfs[5]['price']/ varsLb.ret_12H_back[0] -1)*100],
            "ret_24H_back":[(app.etfs[5]['price']/ varsLb.ret_24H_back[0] -1)*100],
            "ret_96H_back":[(app.etfs[5]['price']/ varsLb.ret_96H_back[0] -1)*100],
            "rsi_prom_3":[varsLb.rsi],
            "D_PICO":[varsLb.d_pico]
        }
    )
 
    X = df.copy()
    df_final = X.copy()
    # Usar en nuevos datos
    X_s = scaler.transform(X)
    labels = km.predict(X_s)
    df_final["LABELS"] = labels
    df_final.reset_index(drop=True,inplace=True)
    varsLb.label=df_final["LABELS"][0]
 
    writeLabel(app, varsLb,params)

    asyncio.run(saveLabel(varsLb))
    