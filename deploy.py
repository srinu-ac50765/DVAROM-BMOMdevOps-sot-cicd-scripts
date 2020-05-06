from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("deploy")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

#bmGocdCommon.getLastRunInfo("BMP_MartensOrdersService", "TEST4")        
#bmGocdCommon.checkProjectDeploy("BMP_AccountManagmentService", "TEST1", "release/january20")
#bmGocdCommon.runStage("BMP_MartensOrdersService", "TEST4", 30, "TEST4-DeployStage")
bmGocdCommon.bypassSonar("BMP_QuickconnecService", "TEST4");
#bmGocdCommon.runStage("BMP_BillingOrderOrchestratorService", "TEST4", 76, "imageStage");

log.info("Done!!!")
