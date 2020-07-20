import bmGitLabCommon
import logging
import warnings
#from utils import py
import emailLib
import datetime
import sys
warnings.filterwarnings("ignore")

sendEmailFlag = False

#logging.basicConfig()
log=logging.getLogger("checkProjectChange")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

sendEmailFlag = False
if len(sys.argv) > 1 and sys.argv[1] == "email":
    sendEmailFlag = True

if sendEmailFlag:
    email_handler = emailLib.BufferingSMTPHandler()
    logging.root.addHandler(email_handler)
    

#branch="release/release/february20"
#date = datetime.datetime.strptime("2020-01-29T11:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%f%z')
#result=bmGitLabCommon.getBranchCommitInfo("tom-orchestrator-business-service", "release/february20", releaseDate)
 
projMap=bmGitLabCommon.getprojMap()
projToKubeMap = bmGitLabCommon.getProjConfigBaseMap()
log.debug(projMap)

branch1="release/june20"
branch2="release/july20"
projList = projMap.keys()
#projList = ["bmp-bm-ui"]
log.info("Compare branches: %s %s", branch1, branch2)
totalCount = 0;
changedCount = 0;
for projName in projList:
    if projName.startswith('#'):
        continue
    #result=bmGitLabCommon.compareBranches(projName, "release/december19", "release/january20");     
    #result=bmGitLabCommon.compareBranches(projName, "release/january20", "release/february20"); 
    result=bmGitLabCommon.compareBranchesLastCommit(projName, branch1, branch2);  
    # those special projects are those that don't have config properties 
    if (projName == "bmp-ordermanagement-gui"):
        kubeBase = "bmp-ordermanagement-gui"
    # bm-ui is deployed in bmcm, we can change it separately
    elif projName == "bmp-bm-ui":
        continue 
    elif projName == "bmp-martens-orders-service":
        kubeBase = "bmp-martens-orders-service"
    else:
        kubeBase = bmGitLabCommon.getProjConfigBaseMap()[projName]

    """
    if result == 0:
        #log.info("%s: no change", projName)
        log.info("%s: no change", gocdBase)
        
    else:
        #log.info("%s: changed", projName)
        log.info("%s: changed", gocdBase)
    """
    if result > 0:
        log.info(kubeBase)
        changedCount = changedCount + 1

log.info("\r\n\r\nTotal count: %s Changed count: %s", totalCount, changedCount)
log.info("Done!!!!!!!")