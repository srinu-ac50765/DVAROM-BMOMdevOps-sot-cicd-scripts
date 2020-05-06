from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("triggerProjectPipeline")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

bmGocdCommon.triggerPipeline("BMP_MartensOrdersService", "TEST1")   
#bmGocdCommon.triggerPipeline("cybersecurity-business-service", "TEST2")      
#bmGocdCommon.checkProjectDeploy("BMP_AccountManagmentService", "TEST1", "release/january20")
log.info("Done!!!")
