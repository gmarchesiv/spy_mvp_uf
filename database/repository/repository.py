# ====================
#  - Librerias -
# ====================

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from database.model.model import *
import time
from datetime import datetime
import pytz

from functions.logs import printStamp

engine = create_engine("sqlite:////usr/src/app/dataBase.db", echo=False)


def writeRegister(name, zone):
    
    #---------------------------------------------------
    '''
    Registro de sesion en la DB.
    '''
    #---------------------------------------------------

    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(zone)
        new_data = register(start=datetime_now, user=name)
        session.add(new_data)
        session.commit()

    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al escribir en Base de datos register")
    finally:
        session.close()


def writeRoutineFault(Fault, codeIB, id, msg):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        timezone_NY = pytz.timezone("America/New_York")
        datetime_now = datetime.now(timezone_NY)
        new_data = routineFault(
            date=datetime_now, typeFault=Fault, code=codeIB, idIB=id, message=msg
        )

        session.add(new_data)
        session.commit()

    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al escribir en Base de datos routineFault")
    finally:
        session.close()


def writeWallet(app):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        timezone_NY = pytz.timezone("America/New_York")
        datetime_now = datetime.now(timezone_NY)

        new_data = wallet(
            TotalCashValue=app.wallet["TotalCashValue"],
            SettledCash=app.wallet["SettledCash"],
            NetLiquidation=app.wallet["NetLiquidation"],
            UnrealizedPnL=app.wallet["UnrealizedPnL"],
            AvailableFunds=app.wallet["AvailableFunds"],
            date=datetime_now,
        )

        session.add(new_data)
        session.commit()
    except Exception as e:
        print(f"Error al escribir en Base de datos Wallet: {e}")
    finally:
        session.close()


def readWallet():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        data = session.query(wallet).order_by(desc(wallet.id)).first()

        session.close()
        if data == None:
            return None
        return data.__dict__
    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al leer en Base de datos Wallet")
        session.close()


def writeDayTrade(app, vars,varsLb, params):
    #---------------------------------------------------
    '''
    Registra del dia en la DB.
    '''
    #---------------------------------------------------
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(params.zone)
        new_data = dayTrade(
            date=datetime_now,
            etf=app.etfs[10]["symbol"],
            vix = float(app.etfs[11]["price"]),
            underlying=float(app.etfs[10]["price"]),
            cStrike=app.options[1]["strike"],
            pStrike=app.options[2]["strike"],
            exp=app.options[1]["expirations"],
            cask=vars.cask,
            cbid=vars.cbid,
            pask=vars.pask,
            pbid=vars.pbid,
            cask_Size=app.options[1]["ASK_SIZE"],
            cbid_Size=app.options[1]["BID_SIZE"],
            pask_Size=app.options[2]["ASK_SIZE"],
            pbid_Size=app.options[2]["BID_SIZE"],
            cAskBid=vars.askbid_call,
            pAskBid=vars.askbid_put,
            dCall=vars.dcall,
            dPut=vars.dput,
            doCall=vars.docall,
            doPut=vars.doput,
            label=int(varsLb.label),
            rentabilidad=vars.rentabilidad,
            pico=vars.pico,
            caida=vars.caida,
            rule=vars.regla,
            cAskBid_prom = vars.promedio_call,
            pAskBid_prom = vars.promedio_put,


            cStrike_2=app.options[3]["strike"],
            pStrike_2=app.options[4]["strike"],
            exp_2=vars.exp_2,
            cask_2=vars.cask_2,
            cbid_2=vars.cbid_2,
            pask_2=vars.pask_2,
            pbid_2=vars.pbid_2,
 
            cAskBid_2=vars.askbid_call_2,
            pAskBid_2=vars.askbid_put_2,
            dCall_2=vars.dcall_2,
            dPut_2=vars.dput_2,
            doCall_2=vars.docall_2,
            doPut_2=vars.doput_2,
            
            # cStrike_3=app.options[5]["strike"],
            # pStrike_3=app.options[6]["strike"],
            # exp_3=vars.exp_3,
            # cask_3=vars.cask_3,
            # cbid_3=vars.cbid_3,
            # pask_3=vars.pask_3,
            # pbid_3=vars.pbid_3,
 
            # cAskBid_3=vars.askbid_call_3,
            # pAskBid_3=vars.askbid_put_3,
            # dCall_3=vars.dcall_3,
            # dPut_3=vars.dput_3,
            # doCall_3=vars.docall_3,
            # doPut_3=vars.doput_3

        )

        session.add(new_data)
        session.commit()

    except Exception as e:
        printStamp(f"Error al escribir en Base de datos dayTrade: {e}")
    finally:
        session.close()


def writeTransactions(app, id, vars):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        new_transaction = transactions(
            date=vars.trade_hour,
            action=app.execution_details[id]["action"],
            tiker=app.execution_details[id]["tiker"],
            type=app.execution_details[id]["type"],
            symbol=app.execution_details[id]["symbol"],
            price=app.execution_details[id]["price"],
            shares=app.execution_details[id]["shares"],
            commission=app.execution_details[id]["commission"],
            cash=float(app.cash),
            regla=vars.regla_ant,
        )

        session.add(new_transaction)
        session.commit()

    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al escribir en Base de datos transactions")
    finally:
        session.close()

def writeLabel(app, varsLb,params):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(params.zone)
        new_data = label(
            date=datetime_now,
            underlying = app.etfs[10]["price"],
            vix =app.etfs[11]['price'],
            
            mu =  float(varsLb.mu),
            mu_conteo = int(varsLb.mu_conteo),
            retorno = varsLb.retorno,
            signo = varsLb.signo,
            varianza = varsLb.varianza,
            garch=varsLb.garch,
            
            ret_1H_back= float(app.etfs[10]['price']/ varsLb.ret_1H_back[0] -1)*100,
            ret_3H_back=float(app.etfs[10]['price']/ varsLb.ret_3H_back[0] -1)*100,
            ret_6H_back= float(app.etfs[10]['price']/ varsLb.ret_6H_back[0] -1)*100,
            ret_12H_back= float(app.etfs[10]['price']/ varsLb.ret_12H_back[0] -1)*100,
            ret_24H_back= float(app.etfs[10]['price']/ varsLb.ret_24H_back[0] -1)*100,
            ret_96H_back= float(app.etfs[10]['price']/ varsLb.ret_96H_back[0] -1)*100,

            rsi_prom= varsLb.rsi,
            d_pico= float(varsLb.d_pico),

            label = int(varsLb.label)
        )

        session.add(new_data)
        session.commit()

    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al escribir en Base de datos transactions")
    finally:
        session.close()

def writeRoutineFault(Fault, codeIB, id, msg):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        timezone_NY = pytz.timezone("America/New_York")
        datetime_now = datetime.now(timezone_NY)
        new_data = routineFault(
            date=datetime_now, typeFault=Fault, code=codeIB, idIB=id, message=msg
        )

        session.add(new_data)
        session.commit()

    except Exception as e:
        print(type(e).__name__, ":", e)
        printStamp("Error al escribir en Base de datos routineFault")
    finally:
        session.close()
