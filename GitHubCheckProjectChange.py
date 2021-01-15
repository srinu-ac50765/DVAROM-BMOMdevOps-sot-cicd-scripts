import bmGitHubCommon
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
#result=bmGitHubCommon.getBranchCommitInfo("tom-orchestrator-business-service", "release/february20", releaseDate)
 
projMap=bmGitHubCommon.getprojMap()
projToJenkinsMap = bmGitHubCommon.getProjToJenkinsMap();
log.debug(projMap)

branch1="release/november20"
branch2="release/december20"
projList = projMap.keys()
#projList = ["bmp-bm-ui"]
log.info("Compare branches: %s %s", branch1, branch2)
totalCount = 0;
changedCount = 0;
for projName in projList:
    if projName.startswith('#'):
        continue
    #result=bmGitHubCommon.compareBranches(projName, "release/december19", "release/january20");     
    #result=bmGitHubCommon.compareBranches(projName, "release/january20", "release/february20"); 
    result=bmGitHubCommon.compareBranchesLastCommit(projName, branch1, branch2);
    jenkinsBase = projToJenkinsMap[projName]
    totalCount = totalCount + 1
    """
    if result == 0:
        #log.info("%s: no change", projName)
        log.info("%s: no change", gocdBase)
        
    else:
        #log.info("%s: changed", projName)
        log.info("%s: changed", gocdBase)
    """
    if result > 0:
        log.info(jenkinsBase)
        #log.info(projName)
        changedCount = changedCount + 1

"""
if sendEmailFlag:
    #emailList=["ning.li@centurylink.com"]
    msgPreamble = f"You made changes in the {fromBranch} branch, but did not merge {fromBranch} to the {toBranch} branch. For projects owned by the Submit Order teams, you are responsible for submitting request to merge release branches. After merge is complete, please open STS ticket for deployment."
    subject = f"Missing Merges Notice ({fromBranch} to {toBranch})"
    email_handler.sendEmail(subject, emailList, msgPreamble)    

    print("Email sent")
    
print(f"Email list: {emailList}")
"""
log.info("\r\n\r\nTotal count: %s Changed count: %s", totalCount, changedCount)
log.info("Done!!!!!!!")