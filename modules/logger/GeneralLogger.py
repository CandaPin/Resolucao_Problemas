import logging
import logging.config
import json
import datetime
# import path
from modules.exceptions.CustomExceptions import ConfigurationFileDoesNotExistsException, DirectoryDoesNotExistsException
from modules.utils import Utils

class Logger(object):

    # def __init__(self,processName: str,loggingConfiguration: path.Path = None):
    def __init__(self,processName,loggingConfiguration=None):
        configFile = None
        try:
            if loggingConfiguration is None:
                configFile = Utils.getConfigurationFile("logging.json")
            else:
                configFile = Utils.getConfigurationFile(loggingConfiguration)
        except ConfigurationFileDoesNotExistsException:
            raise ConfigurationFileDoesNotExistsException
        dictFileConfig = dict()
        with open(configFile,'r') as fh:
            dictFileConfig = json.load(fh)
        
        logDir = None
        try:
            logDir = Utils.getLogDirectory()
        except DirectoryDoesNotExistsException:
            raise DirectoryDoesNotExistsException

        logging.config.dictConfig(dictFileConfig)
        self.logger = logging.getLogger(processName)
    