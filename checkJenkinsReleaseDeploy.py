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

env="TEST1"
branchName="release/july20"

# env="TEST4"
# branchName="release/june20"


for jenkinsPipeLineBase in jenkinsToGitMap.keys():    
 
#     if (not jenkinsPipeLineBase == 'BMP_order-management-business-service'):
#         print(jenkinsPipeLineBase)
#         continue
    bmJenkinsCommon.checkProjectDeploy(jenkinsPipeLineBase, env, branchName)
print("Done!!!!!!!")