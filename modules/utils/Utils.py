
import os
from pathlib import Path
from modules.exceptions.CustomExceptions import ConfigurationFileDoesNotExistsException, DirectoryDoesNotExistsException,FileDoesNotExistsException

import argparse

def getInputDirectory() -> Path:
    inputDir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'inputs'))
    if not isDirectoryExists(directoryName=inputDir):
        raise DirectoryDoesNotExistsException("The inputs directory does not exists.")
    return inputDir

def getOutputDirectory() -> Path:
    inputDir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'outputs'))
    if not isDirectoryExists(directoryName=inputDir):
        raise DirectoryDoesNotExistsException("The output directory does not exists.")
    return inputDir

def getConfigurationFile(configFileName: str) -> Path:
    configDir = None
    try:
        configDir = getConfigurationDirectory()
    except DirectoryDoesNotExistsException:
        raise DirectoryDoesNotExistsException
    
    configFile = Path(os.path.join(configDir,configFileName))
    if not isFileExists(fileName=configFile):
        raise ConfigurationFileDoesNotExistsException("Configuration file {} does not exists.".format(configFile))
    return configFile

def isDirectoryExists(directoryName: Path) -> bool:
    return directoryName.exists()

def isFileExists(fileName: Path) -> bool:
    return fileName.exists()

def getLogDirectory() -> Path:
    logDir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'logs'))
    if not isDirectoryExists(directoryName=logDir):
        raise DirectoryDoesNotExistsException("The logs directory does not exists.")
    return logDir

def getConfigurationDirectory() -> Path:
    configDir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'configs'))

    if not isDirectoryExists(directoryName=configDir):
        raise DirectoryDoesNotExistsException("The configs directory does not exists.")
    return configDir