from modules.exceptions.CustomExceptions import ConfigurationFileDoesNotExistsException, DirectoryDoesNotExistsException,FileDoesNotExistsException
from modules.utils import Utils
from modules.handlers.FirstFitDecreasingHandlers import backLogHandler, binsHandler, firstFitDecreasing, postProcessBins
from modules.logger.GeneralLogger import Logger
from datetime import datetime as dt
import xlwings as xw
import pandas as pd
import numpy as np
import warnings
import json
import sys
import re
import os


class FirstFitDecreasingProcess():
    def __init__(self,config_name):
        try:
            self.FirstFitDecreasingLogger = Logger(processName=__name__)
        except ConfigurationFileDoesNotExistsException:
            raise ConfigurationFileDoesNotExistsException
        except DirectoryDoesNotExistsException:
            raise DirectoryDoesNotExistsException

        configFile = None
        try:
            configFile = Utils.getConfigurationFile(config_name)
        except ConfigurationFileDoesNotExistsException:
            self.FirstFitDecreasingLogger.logger.error("It was not possible instantiate {0}. Configuration file {1} does not exists.".format(__name__,configFile))
            raise ConfigurationFileDoesNotExistsException
        
        try:
            with open(configFile,'r',encoding='utf-8') as fh:
                self.dictFileConfig = json.load(fh)
        except OSError:
            self.FirstFitDecreasingLogger.logger.error("It was not possible open {0} for reading.".format(configFile))
            self.FirstFitDecreasingLogger.logger.exception(sys.exc_info())
            raise OSError
    
    def _getDataHandlers(self):
        try:
            self.FirstFitDecreasingLogger.logger.info("Starting data handlers reading")
            self.dfBackLog, self.dfRoutesRestrictions = backLogHandler(pd.read_excel(self.dictFileConfig['sources']['BackLogOrdens']['path']))
            self.dfBinsRestrictions = binsHandler(pd.read_excel(self.dictFileConfig['sources']['TiposDeCaixa']['path'],sheet_name=self.dictFileConfig['sources']['TiposDeCaixa']['sheetName']))

        except DirectoryDoesNotExistsException:
            raise DirectoryDoesNotExistsException
        except KeyError:
            self.FirstFitDecreasingLogger.logger.error("Invalid Columns")
            raise KeyError
        self.FirstFitDecreasingLogger.logger.info("Data Handlers Completed")

    def _HeuristicProcess(self):
        try:
            self.FirstFitDecreasingLogger.logger.info("Starting FirstFitDecreasing")
            self.bins, self.dfLeftoverItems = firstFitDecreasing(self.dfBackLog, self.dfBinsRestrictions, self.dfRoutesRestrictions)
        except KeyError:
            self.FirstFitDecreasingLogger.logger.error(KeyError)
            raise KeyError
        self.FirstFitDecreasingLogger.logger.info("FirstFitDecreasing Completed")
        
    def _postProcessLoadData(self):
        try:
            self.FirstFitDecreasingLogger.logger.info("Starting _postProcessLoadData")
            dfResult = postProcessBins(self.bins, self.dfBackLog)
        except KeyError:
            self.FirstFitDecreasingLogger.logger.error(KeyError)
            raise KeyError
        self.FirstFitDecreasingLogger.logger.info("_postProcessLoadData Completed")

        try:
            self.FirstFitDecreasingLogger.logger.info("Starting Loading Process")
            dfResult.to_csv(self.dictFileConfig['outputs']['results']['path'], sep = ";", index=False)
            self.dfLeftoverItems.to_csv(self.dictFileConfig['outputs']['leftOver']['path'], sep = ";", index=False)
            self.dfBackLog.to_csv(self.dictFileConfig['outputs']['handledBacklog']['path'], sep = ";", index=False)
        except DirectoryDoesNotExistsException:
            raise DirectoryDoesNotExistsException
        except KeyError:
            self.FirstFitDecreasingLogger.logger.error(KeyError)
            raise KeyError
        self.FirstFitDecreasingLogger.logger.info("Completed")

    def main(self):
        self._getDataHandlers()
        self._HeuristicProcess()
        self._postProcessLoadData()

if __name__ == "__main__":
    FirstFitDecreasingProcess('FirstFitDecreasingConfig.json').main()