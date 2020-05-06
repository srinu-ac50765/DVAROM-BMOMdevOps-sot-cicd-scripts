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
log=logging.getLogger("checkReleaseCommit")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

sendEmailFlag = False
if len(sys.argv) > 1 and sys.argv[1] == "email":
    sendEmailFlag = True

sendEmailFlag = False

if sendEmailFlag:
    email_handler = emailLib.BufferingSMTPHandler()
    logging.root.addHandler(email_handler)
    

#branch="release/release/february20"
#date = datetime.datetime.strptime("2020-01-29T11:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%f%z')
#result=bmGitLabCommon.getBranchCommitInfo("tom-orchestrator-business-service", "release/february20", releaseDate)
 
projMap=bmGitLabCommon.getprojMap()
log.debug(projMap)

branch="release/april20"
#branch="release/march20"
#branch="release/february20"
date = datetime.datetime.strptime("2020-04-17T23:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%f%z')

#branch="release/january20"
#date = datetime.datetime.strptime("2020-01-17T23:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%f%z')

log.info("Release branch: %s Release date: %s", branch, date)
beforeCountTotal = 0;
afterCountTotal = 0;
for projName in projMap.keys():
    if projName.startswith('#'):
        continue
    #result=bmGitLabCommon.compareBranches(projName, "release/december19", "release/january20");     
    #result=bmGitLabCommon.compareBranches(projName, "release/january20", "release/february20"); 
    result=bmGitLabCommon.getBranchCommitInfo(projName, branch, date);
    beforeCountTotal = beforeCountTotal + result["beforeCount"] 
    afterCountTotal = afterCountTotal + result["afterCount"]
    log.info("beforeTotal: %s   afterTotal: %s", beforeCountTotal, afterCountTotal)

"""
if sendEmailFlag:
    #emailList=["ning.li@centurylink.com"]
    msgPreamble = f"You made changes in the {fromBranch} branch, but did not merge {fromBranch} to the {toBranch} branch. For projects owned by the Submit Order teams, you are responsible for submitting request to merge release branches. After merge is complete, please open STS ticket for deployment."
    subject = f"Missing Merges Notice ({fromBranch} to {toBranch})"
    email_handler.sendEmail(subject, emailList, msgPreamble)    

    print("Email sent")
    
print(f"Email list: {emailList}")
"""
print("Done!!!!!!!")