# ====================
#  - Librerias -
# ====================
import os
from sqlalchemy import (
    DateTime,
    create_engine,
    Column,
    Integer,
    Float,
    Date,
    Boolean,
    String,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base

# Obtener el directorio actual del script

db_path = "dataBase.db"

# Definir la clase base para las clases de modelo
Base = declarative_base()


class register(Base):
    __tablename__ = "register"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    user = Column(String)


class wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    TotalCashValue = Column(Float)
    SettledCash = Column(Float)
    NetLiquidation = Column(Float)
    UnrealizedPnL = Column(Float)
    AvailableFunds = Column(Float)


class transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    action = Column(String)
    tiker = Column(String)
    symbol = Column(String)
    type = Column(String)
    price = Column(Float)
    shares = Column(Float)
    commission = Column(Float)
    cash = Column(Float)
    regla = Column(String)


class dayTrade(Base):
    __tablename__ = "dayTrade"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    etf = Column(String)
    underlying = Column(Float)
    vix = Column(Float)
    cStrike = Column(Float)
    pStrike = Column(Float)
    exp = Column(String)
    cask = Column(Float)
    cbid = Column(Float)
    pask = Column(Float)
    pbid = Column(Float)
    cask_Size = Column(Integer)
    cbid_Size = Column(Integer)
    pask_Size = Column(Integer)
    pbid_Size = Column(Integer)
    cAskBid = Column(Float)
    pAskBid = Column(Float)
    dCall = Column(Float)
    dPut = Column(Float)
    doCall = Column(Float)
    doPut = Column(Float)
    label= Column(Integer)
    rentabilidad = Column(Float)
    pico = Column(Float)
    caida = Column(Float)
    rule = Column(String)
    cAskBid_prom = Column(Float)
    pAskBid_prom = Column(Float)

    cStrike_2= Column(Float)
    pStrike_2= Column(Float)
    exp_2= Column(Float)
    cask_2= Column(Float)
    cbid_2= Column(Float)
    pask_2= Column(Float)
    pbid_2= Column(Float)

    cAskBid_2= Column(Float)
    pAskBid_2= Column(Float)
    dCall_2= Column(Float)
    dPut_2= Column(Float)
    doCall_2= Column(Float)
    doPut_2= Column(Float)
    
    cStrike_3= Column(Float)
    pStrike_3= Column(Float)
    exp_3= Column(Float)
    cask_3= Column(Float)
    cbid_3= Column(Float)
    pask_3= Column(Float)
    pbid_3= Column(Float)

    cAskBid_3= Column(Float)
    pAskBid_3= Column(Float)
    dCall_3= Column(Float)
    dPut_3= Column(Float)
    doCall_3= Column(Float)
    doPut_3= Column(Float)
    

class label(Base):
    __tablename__ = "label"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    underlying = Column(Float)
    vix = Column(Float)

    mu = Column(Float)
    mu_conteo = Column(Integer)
    retorno = Column(Float)
    signo = Column(Integer)
    varianza = Column(Float)
    garch=Column(Float)


    ret_1H_back=Column(Float)
    ret_3H_back=Column(Float)
    ret_6H_back=Column(Float)
    ret_12H_back=Column(Float)
    ret_24H_back=Column(Float)
    ret_96H_back=Column(Float)

    rsi_prom=Column(Float)
    d_pico=Column(Float)

    label = Column(Integer)
     

class routineFault(Base):
    __tablename__ = "routineFault"
    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    typeFault = Column(String)
    code = Column(Float)
    idIB = Column(Float)
    message = Column(String)

 

# Crear la conexión a la base de datos
engine = create_engine(f"sqlite:///{db_path}")

# Crear la tabla en la base de datos
Base.metadata.create_all(engine)
