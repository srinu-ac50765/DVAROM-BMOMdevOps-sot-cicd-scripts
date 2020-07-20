import datetime
import bmGitLabCommon
import bmJenkinsCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("triggerJenkinsReleasePipeline")
# Jenkins APIs seem to introduce a duplicate log handler. This will prevent duplicate log lines
logging.getLogger().handlers.clear() 
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

jenkinsToGitMap = bmGitLabCommon.getJenkinsToGitMap()
log.debug(jenkinsToGitMap)
envName = "TEST2"
x = [
"BMP_quickconnect-bs-service-test2-CONTINUOUS"
    ]
# for pipeline in x:
#     bmJenkinsCommon.triggerPipeline(pipeline)
for jenkinsPipeLineBase in jenkinsToGitMap.keys():    
    pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
#     if pipeline != "BMP_account-profile-service":    
#         bmJenkinsCommon.triggerPipeline(pipeline)   
    lastBuildNumber = bmJenkinsCommon.getLatestBuildNumberByLastStage(pipeline)
    jobLastStage = bmJenkinsCommon.getBuildLastStage(pipeline, lastBuildNumber)    
    if jobLastStage:
        log.info("%s lastBuildNumber:%s %s %s", pipeline, lastBuildNumber, jobLastStage['name'], jobLastStage['status'])
    else:
        log.info("%s lastBuildNumber:%s First Stage not started", pipeline, lastBuildNumber)
log.info("Done!!!")
