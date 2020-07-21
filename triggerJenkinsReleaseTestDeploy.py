import bmJenkinsCommon
import bmGitLabCommon
import logging
import warnings
#from utils import py
import emailLib
import datetime
import sys
warnings.filterwarnings("ignore")

#logging.basicConfig()
log=logging.getLogger("cutJenkinsProdVersion")
# Jenkins APIs seem to introduce a duplicate log handler. This will prevent duplicate log lines
logging.getLogger().handlers.clear() 
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

jenkinsToGitMap = bmGitLabCommon.getJenkinsToGitMap()
log.debug(jenkinsToGitMap)
   
envName = "TEST1"   


for jenkinsPipeLineBase in jenkinsToGitMap.keys():       
    pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
    lastBuildNumber = bmJenkinsCommon.getLatestBuildNumberByLastStage(pipeline)
    if lastBuildNumber != -1:
        bmJenkinsCommon.deployTestStage(pipeline, lastBuildNumber)
log.info("Done!!!")            