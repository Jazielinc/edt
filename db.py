#!/usr/bin/python

import os
import logging
import logging.handlers

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgres://jazielroot:yYWNzHgCLgCfyFVe16TRRo6elcjSawgp@dpg-ckg278eafg7c73d9qal0-a/edt_db"

CONTROLLED_LEVELV_NUM = 29

logging.addLevelName(CONTROLLED_LEVELV_NUM, "CONTROLLED")


def controlled(self, message, *args, **kws):
    if self.isEnabledFor(CONTROLLED_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(CONTROLLED_LEVELV_NUM, message, args, **kws)

def start_logging(loggerPath, loggerName, loggerLevel):
    """
        Funcion para generar el archivo de logueo en la ruta pasada.
        Entrada:
            loggerPath: la ruta en donde se va a crear el archivo.
            loggerName: nombre del archivo de log, sin la extencion.
            loggerLevel: el nivel de logueo(debug, info, error)
        Salida:
            El objeto de logger que apunta al archivo.
    """
    # Setup local logger
    if not logging.getLogger(loggerName).handlers:
        # set logging level
        # level=logging.DEBUG
        level = int(logging.getLevelName(loggerLevel.upper()))
        # Create log file path
        logfile="%s/%s.log"%(loggerPath,loggerName)
        if not os.path.exists(logfile):
            with open(logfile, 'w') as f:
                pass
        # Create log file handler
        handler = logging.handlers.WatchedFileHandler(logfile)
        # Do not propagate to father
        logging.getLogger(loggerName).propagate=False
        # Set logging level
        logging.getLogger(loggerName).setLevel(level)
        # Set logging format
        handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d [%(process)d] [%(levelname)s] %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
        #
        logging.Logger.controlled = controlled
        # logging.getLogger(loggerName).controlled = controlled
        # Set logger handler
        logging.getLogger(loggerName).addHandler(handler)
    return logging.getLogger(loggerName)

# -------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------

logger = start_logging('./', 'edt_log', 'info')

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try: 
        yield db

    finally:
        db.close()