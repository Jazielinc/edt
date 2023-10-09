#!/usr/bin/python

import os
import csv
import sys
import config
import psycopg2
import traceback
import logging
import logging.handlers
from pprint import pformat
from configparser import ConfigParser


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

def config(filename='./ext_db.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
    except:
        error_info = ''.join(traceback.format_exception(*sys.exc_info()))
        logger.error(error_info)

    return conn

def read_csv(path='./dummy_data.csv'):
    '''
    We expect to recive the data in order
    '''
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                yield row

    except:
        error_info = ''.join(traceback.format_exception(*sys.exc_info()))
        logger.error(error_info)

def insert_to_db(cursor, data=[]):
    try:
        if data:
            cursor = conn.cursor()
            sql = """INSERT INTO public.restaurants(
                id,
                rating,
                name,
                site,
                email,
                phone,
                street,
                city,
                state,
                lat, 
                lng
                )
             VALUES(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s);"""
            
            tmp_data = []

            for value_ in data:
                try:
                    tmp_data.append(int(value_))
                
                except:
                    tmp_data.append(value_)
            
            # tmp_data[-1] = "POINT({} {})".format(data[-1], data[-2])
            # del tmp_data[-2]

            cursor.execute(sql, tmp_data)
            conn.commit()

            count = cursor.rowcount
            if count:
                logger.info('Row inserted correctly!')
            
            else:
                logger.info('Row not inserted... check the code.')

        else:
            logger.info('No data to insert.')

    except:
        error_info = ''.join(traceback.format_exception(*sys.exc_info()))
        logger.error(error_info)


if __name__ == '__main__':
    count = 0
    conn = connect()
    
    for row in read_csv():
        if count == 0:
            pass

        else:
            logger.info('Processing data: {}'.format(pformat(row)))
            insert_to_db(conn, row)

        count += 1

    conn.close()
