from datetime import datetime
from pathlib import Path
import logging
import shlex
import subprocess
import json
import time

def setupLoger(name, file):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log

def setupDataLoggers():
    def setupLoger(name, file):
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(file, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        log.addHandler(fh)

        return log
    loggers = []
    dt = datetime.now().strftime("%m_%d_%H")
    Path("./logs/%s" % dt).mkdir(parents=True, exist_ok=True)
    loggers.append(setupLoger('reward', './logs/{0}/reward.log'.format(dt)))
    loggers.append(setupLoger('action', './logs/{0}/action.log'.format(dt)))
    loggers.append(setupLoger('time', './logs/{0}/time.log'.format(dt)))
    loggers.append(setupLoger('state', './logs/{0}/state.log'.format(dt)))

    return loggers