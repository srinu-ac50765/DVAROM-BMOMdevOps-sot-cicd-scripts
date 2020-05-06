import bmGitLabCommon
import logging
import warnings
import sys
import emailLib

warnings.filterwarnings("ignore")
#logging.basicConfig()

log=logging.getLogger("checkProjectMerge")

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
    


#result=bmGitLabCommon.compareBranches("billing-order-orchestrator-business-service", "release/november19", "release/december19")
#result=bmGitLabCommon.compareBranches("order-decomposition-business-service", "release/november19", "release/december19")
#result=bmGitLabCommon.compareBranches("bill-estimates-business-service", "release/december19", "release/january20")
#result=bmGitLabCommon.compareBranches("notification-business-service", "release/february20", "release/march20")
#result=bmGitLabCommon.compareBranches("account-management-business-service", "release/february20", "release/march20")
result=bmGitLabCommon.compareBranches("jeopardy-business-service", "release/march20", "release/april20")
#result=bmGitLabCommon.compareBranches("billing-order-orchestrator-business-service", "release/december19", "release/november19")
if result == 0:
    log.debug("merged")
else:
    log.debug("unmerged")

emailList=bmGitLabCommon.getMissingCommitEmailList()
log.info("Email list: %s", emailList)

#email_handler.sendEmail("Missing Merges Notice", "ning.li@centurylink.com")
