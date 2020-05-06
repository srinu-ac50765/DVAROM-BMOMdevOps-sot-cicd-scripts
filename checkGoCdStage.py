from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging
import sys
import emailLib
warnings.filterwarnings("ignore")

log=logging.getLogger("checkGoCdStage")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

pipelineList = ["BMP_BillingOrderOrchestratorService/87",
"BMP_DataMappingService/23",
"BMP_DirectoryListingBusinessService/19",
"BMP_DtvOptoutBusinessService/30",
"BMP_EmailProvisioningService/15",
"BMP_FFWFService/31",
"BMP_GmanGbusService/13",
"BMP_IsstBusinessService/22",
"BMP_JeopardyService/46",
"BMP_NotificationService/27",
"BMP_OESBusinessService/18",
"BMP_OrderDecompositionService/104",
"BMP_OrderManagementService/120",
"BMP_OrderStatusUpdateBusinessService/25",
"BMP_ProvisioningOrderService/35",
"BMP_QuickconnecService/25",
"BMP_RulesMappingService/11",
"BMP_ServiceRegistryService/19",
"BMP_TomOrchestratorServiceService/58",
"BMP_TranslationLookupService/13",
"BMP_UpdateEmailAccountService/17",
"BMP_CamundaMonitoringAppService/11",
"BMP_OrderManagementProcessService/230",
"BMP_AccountTreatmentService/25",
"BMP_AccountProfileService/15",
"BMP_DtvCorrectionBusinessService/21",
"BMP_DirectTvOmService/38",
"BMP_cybersecuritybusinessservice/22",
"BMP_MartensOrdersService/2",
"BMP_ServiceDeliveryService/36",
"BMP_DtvTreatmentBusinessService/13",
"BMP_QCServices/8",
"BMP_BM_UI/51"
]
    
#pipelineList=bmGitLabCommon.getGocdToGitMap().keys()
#env="TEST1"
#stageName="TEST1-DeployStage"
env = "TEST1"
stageName="PROD-DeployStage"
for pipeline in pipelineList:
    instanceNumber = -1
    if pipeline.find("/") > 0:
        gocdPipelineBase,instanceString = pipeline.split("/")
        instanceNumber = int(instanceString)
    else:
        gocdPipelineBase = pipeline        
    bmGocdCommon.checkStageStatus(gocdPipelineBase, env, stageName, instanceNumber)    
        
'''
gocdPipelineBase="BMP_BillingOrderOrchestratorService";
env="TEST1"
#stageName="PROD-DeployStage"
stageName="TEST1-DeployStage"
instanceNumber=88
bmGocdCommon.checkStageStatus(gocdPipelineBase, env, stageName, instanceNumber)
'''


print("Done!!!!!!!")