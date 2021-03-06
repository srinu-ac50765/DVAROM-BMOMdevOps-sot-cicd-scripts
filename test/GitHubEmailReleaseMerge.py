from common import bmGitHubCommon, emailLib
import logging
import warnings
#from utils import py
import sys
warnings.filterwarnings("ignore")

sendEmailFlag = True

#logging.basicConfig()
log=logging.getLogger("checkProjectMerge")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

sendEmailFlag = True
if len(sys.argv) > 1 and sys.argv[1] == "email":
    sendEmailFlag = True

if sendEmailFlag:
    email_handler = emailLib.BufferingSMTPHandler()
    logging.root.addHandler(email_handler)
    


mergedList=[]
unmergedList=[]  
 
projMap= bmGitHubCommon.getprojMap()
log.debug(projMap)
#fromBranch = "release/march20"
#toBranch = "release/april20"
fromBranch = "release/december20"
toBranch = "release/january21"
#fromBranch = "release/november20"
#toBranch = "release/december20"

aprilExclusiveList = ["bmp-bm-ui", "provisioning-order-business-service"]

for projName in projMap.keys():
    if projName.startswith('#'):
        continue
    if fromBranch == "release/april20" and projName in aprilExclusiveList:
        continue        
    #result=bmGitHubCommon.compareBranches(projName, "release/december19", "release/january20");     
    #result=bmGitHubCommon.compareBranches(projName, "release/january20", "release/february20"); 
    result= bmGitHubCommon.compareBranches(projName, fromBranch, toBranch);
    if result == 0:
        mergedList.append(projName)
    else:
        unmergedList.append(projName)

log.debug(str(("merged: ",mergedList)))
log.debug(str(("unmerged: ",unmergedList)))

emailList= bmGitHubCommon.getMissingCommitEmailList()

if emailList and sendEmailFlag:
    #emailList=["ning.li@centurylink.com"]
    msgPreamble = f"You made changes in the {fromBranch} branch, but did not merge the {fromBranch} to the {toBranch} branch. For projects owned by the Submit Order teams, you are responsible for submitting request to merge release branches. When multiple developers have missing commits for a project, the Merge Owner is responsible for merging. After merge is complete, please open STS ticket for deployment."
    subject = f"Missing Merges Notice ({fromBranch} to {toBranch})"
    #email_handler.sendEmail(subject, emailList, msgPreamble)    

    print("Email sent")
    
print(f"Email list: {emailList}")
print("Done!!!!!!!")