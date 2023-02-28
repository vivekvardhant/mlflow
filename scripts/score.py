import argparse
import json
import logging
import logging.config
import os
import os.path as op
import pickle
import sys
import tarfile

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="data folder path")
parser.add_argument('--model_path',nargs='?')
parser.add_argument('--data_path',nargs='?')
parser.add_argument('--res_path' ,nargs='?')
parser.add_argument('--log_level',nargs='?')
parser.add_argument('--log_path',nargs='?')
parser.add_argument('--no_console_log',nargs='?')
args = parser.parse_args()

if args.log_level == None:
    log_level = "DEBUG"
else:
    log_level = args.log_level

if args.log_path == None:
    log_file = None
else:
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','logs',"score.log")

if args.no_console_log == None:
    no_console_log = True
else:
    no_console_log = args.no_console_log

LOGGING_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(message)s"},
    },
    "root": {"level": "DEBUG"},
}

def configure_logger(
    logger=None, cfg=None, log_file=None, console=True, log_level="DEBUG"
):
    if not cfg:
        logging.config.dictConfig(LOGGING_DEFAULT_CONFIG)
    else:
        logging.config.dictConfig(cfg)

    logger = logger or logging.getLogger()

    if log_file or console:
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(getattr(logging, log_level))
            logger.addHandler(fh)

        if console:
            sh = logging.StreamHandler()
            sh.setLevel(getattr(logging, log_level))
            logger.addHandler(sh)

    return logger

HERE = op.dirname(op.abspath(__file__))

if args.model_path == None:
    path = op.join(HERE, '..', 'artifacts')
    with open(path + '/model_pickle','rb') as f:
        final_model = pickle.load(f)
else:
    with open(args.model_path,'rb') as f:
        final_model = pickle.load(f)

if args.res_path == None:
    path3 = op.join(HERE, '..', 'artifacts')
else:
    path3 = args.res_path

if args.data_path == None:
    path2 = op.join(HERE, '..', 'data','processed')
else:
    path2 = args.data_path

X_test_prepared = pd.read_csv(path2 + '/X_test.csv')
y_test = pd.read_csv(path2 + '/y_test.csv')

X_test_prepared = X_test_prepared.iloc[:,1:]
y_test = y_test.iloc[:,1:]

logger = configure_logger(log_file=log_file, console=no_console_log, log_level=log_level)


final_predictions = final_model.predict(X_test_prepared)
final_mse = mean_squared_error(y_test, final_predictions)
logger.info(f"MSE calculated")
final_rmse = np.sqrt(final_mse)
logger.info(f"RMSE calculated")
results = {'Mean Square Error':final_mse, 'Root mean square error':final_rmse}

with open(path3 + '/results.txt', 'w') as convert_file:
     convert_file.write(json.dumps(results))
logger.info(f"Results are stored in the artifacts folder")

#logs added