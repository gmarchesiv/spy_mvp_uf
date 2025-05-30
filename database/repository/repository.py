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
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(zone)
        new_data = register(start=datetime_now, user=name)
        session.add(new_data)
        session.commit()

    except:
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

    except:
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
    except:
        printStamp("Error al leer en Base de datos Wallet")
        session.close()


def writeDayTrade(app, vars, params):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(params.zone)
        new_data = dayTrade(
            date=datetime_now,
            etf=app.etfs[5]["symbol"],
            vix = float(app.etfs[6]["price"]),
            underlying=float(app.etfs[5]["price"]),
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
            label=int(vars.label),
            rentabilidad=vars.rentabilidad,
            pico=vars.pico,
            caida=vars.caida,
            rule=vars.regla,
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

    except:
        printStamp("Error al escribir en Base de datos transactions")
    finally:
        session.close()

def writeLabel(app, vars,params):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        datetime_now = datetime.now(params.zone)
        new_data = label(
            date=datetime_now,
            underlying = app.etfs[5]["price"],
            vix =app.etfs[6]['price'],
            
            mu =  float(vars.mu),
            mu_conteo = int(vars.mu_conteo),
            retorno = vars.retorno,
            signo = vars.signo,
            varianza = vars.varianza,
            garch=vars.garch,

            ret_1H_back= float(app.etfs[5]['price']/ vars.ret_1H_back[0] -1),
            ret_3H_back=float(app.etfs[5]['price']/ vars.ret_3H_back[0] -1),
            ret_6H_back= float(app.etfs[5]['price']/ vars.ret_6H_back[0] -1),
            ret_12H_back= float(app.etfs[5]['price']/ vars.ret_12H_back[0] -1),
            ret_24H_back= float(app.etfs[5]['price']/ vars.ret_24H_back[0] -1),
            ret_96H_back= float(app.etfs[5]['price']/ vars.ret_96H_back[0] -1),

            rsi_prom= vars.rsi,
            d_pico= float(vars.d_pico),

            label = int(vars.label)
        )

        session.add(new_data)
        session.commit()

    except:
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

    except:
        printStamp("Error al escribir en Base de datos routineFault")
    finally:
        session.close()
