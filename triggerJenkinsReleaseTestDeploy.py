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
   
envName = "TEST1"   
# for jenkinsPipeLineBase in jenkinsToGitMap.keys():    
#     pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
#     buildInfo = bmJenkinsCommon.getProdBuildNumber(pipeline)

x = [
# "BMP_account-profile-service",
# "BMP_AccountTreatmentService",
# "BMP_datamapping-business-service",
# "BMP_DirecttvOMService",
# "BMP_order-dispatch-business-service",
# "BMP_DTVCorrectionService",
# "BMP_DTVTreatmentService",
# "BMP_gman-gbus-business-service",
# "BMP_isst-business-service",
# "BMP_kafka-adapter",
# "BMP_bmom-kafka-subscriber",
# "BMP_NotificationService",
# "BMP_OESService",
# "BMP_OrderManagementProcess",
# "BMP_ServiceDeliveryOrchestratorService",
# "BMP_TranslationLookupService",
# "BMP_UpdateEmailAccountService",
# "BMP_quickconnect-bs-service",
# "BMP_bmom-service-registry-service"


    ]

#for jenkinsPipeLineBase in jenkinsToGitMap.keys():   
for jenkinsPipeLineBase in x:     
    pipeline =  bmJenkinsCommon.getPipelineName(jenkinsPipeLineBase, envName)
    lastBuildNumber = bmJenkinsCommon.getLatestBuildNumberByLastStage(pipeline)
    if lastBuildNumber != -1:
        bmJenkinsCommon.deployTestStage(pipeline, lastBuildNumber)
log.info("Done!!!")            

# pipeline = bmJenkinsCommon.getPipelineName("BMP_account-profile-service", envName);
# # bmJenkinsCommon.triggerPipeline(pipeline);
# lastBuildNumber = bmJenkinsCommon.getLatestBuildNumberByLastStage(pipeline)
# log.info("lastBuildNumber:%s", lastBuildNumber)
# if lastBuildNumber != -1:
#     bmJenkinsCommon.deployTestStage(pipeline, lastBuildNumber)