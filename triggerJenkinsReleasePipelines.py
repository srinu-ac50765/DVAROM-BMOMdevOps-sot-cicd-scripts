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
envName = "TEST4"

for jenkinsPipeLineBase in jenkinsToGitMap.keys():    
    pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
    bmJenkinsCommon.triggerPipeline(pipeline)
#     Need to wait for a while, otherwise the new build number probably not reflected
#     lastBuildNumber = bmJenkinsCommon.getLatestBuildNumberByLastStage(pipeline)
#     jobLastStage = bmJenkinsCommon.getBuildLastStage(pipeline, lastBuildNumber)    
#     if jobLastStage:
#         log.info("%s lastBuildNumber:%s %s %s", pipeline, lastBuildNumber, jobLastStage['name'], jobLastStage['status'])
#     else:
#         log.info("%s lastBuildNumber:%s First Stage not started", pipeline, lastBuildNumber)
log.info("Done!!!")
