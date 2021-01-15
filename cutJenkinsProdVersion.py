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
   
envName = "TEST4"
branch = "release/december20"
lastBranch = "release/november20"

totalCount = 0;
changedCount = 0;
for jenkinsPipeLineBase, gitProjName in jenkinsToGitMap.items(): 
    totalCount = totalCount + 1
    needDeploy = bmGitLabCommon.compareBranchesLastCommit(gitProjName, lastBranch, branch);
    jenkinsPipeLineBase = jenkinsPipeLineBase.replace("_build_","_Test4_")
    #print(gitProjName)
    if needDeploy:        
        pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
        #if not pipeline == "BMP_AccountTreatmentService-test1-CONTINUOUS":
#         if not pipeline == "BMP_billing-order-orchestrator-business-service-test1-CONTINUOUS":
#             continue
            
        buildInfo = bmJenkinsCommon.getProdBuildNumber(pipeline)
        changedCount = changedCount + 1
        
log.info("\r\n\r\nTotal count: %s Changed count: %s", totalCount, changedCount)      
log.info("Done!")           
            