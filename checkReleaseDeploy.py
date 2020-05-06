from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging
import sys
import emailLib
warnings.filterwarnings("ignore")

log=logging.getLogger("checkReleaseDeploy")

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
    

gocdToGitMap=bmGitLabCommon.getGocdToGitMap()

env="TEST2"
branchName="release/may20"

#env="TEST2"
#branchName="release/february20"

#env="TEST1"
#branchName="release/january20"

for gocdPipeLineBase in gocdToGitMap.keys():       
    bmGocdCommon.checkProjectDeploy(gocdPipeLineBase, env, branchName);    
    #result=bmGitLabCommon.compareBranches(projName, "release/november19", "release/december19")

emailList = bmGocdCommon.getEmailList()
if sendEmailFlag:
    #emailList=["ning.li@centurylink.com"]
    msgPreamble = f"You committed a change to the {branchName} branch but did not deploy it to {env}. For projects owned by the Submit Order teams, you are responsible for creating STS ticket after committing to a release branch."
    subject = f"Missing Deployment Notice ({branchName} to {env})"
    email_handler.sendEmail(subject, emailList, msgPreamble)    

    print("Email sent")
    
print(f"Email list: {emailList}")
print("Done!!!!!!!")