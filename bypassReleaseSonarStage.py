from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("bypassReleaseSonarStage")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

gocdToGitMap=bmGitLabCommon.getGocdToGitMap()
#gocdToGitMap={"BMP_TomOrchestratorServiceService":"xyz"}

#env="TEST2"
#branchName="release/february20"

env="TEST4"

for gocdPipeLineBase in gocdToGitMap.keys():       
    bmGocdCommon.bypassSonarStage(gocdPipeLineBase, env);    
    #result=bmGitLabCommon.compareBranches(projName, "release/november19", "release/december19")

#log.info(bmGocdCommon.getEmailList())
log.info("Done!!!")