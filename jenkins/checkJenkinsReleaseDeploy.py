import bmJenkinsCommon
import datetime
import bmGitLabCommon

import warnings
import logging
import sys
import emailLib
warnings.filterwarnings("ignore")

log=logging.getLogger("checkJenkinsReleaseDeploy")
# Jenkins APIs seem to introduce a duplicate log handler. This will prevent duplicate log lines
logging.getLogger().handlers.clear() 

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

jenkinsToGitMap = bmGitLabCommon.getJenkinsToGitMap()
log.debug(jenkinsToGitMap)

# env="TEST2"
# branchName="release/august20"

env="TEST1"
branchName="release/july20"


for jenkinsPipeLineBase in jenkinsToGitMap.keys():    
    pipeline =  bmJenkinsCommon.checkProjectDeploy(jenkinsPipeLineBase, env, branchName, True)
print("Done!!!!!!!")