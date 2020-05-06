from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("deployReleaseStage")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

gocdToGitMap=bmGitLabCommon.getGocdToGitMap()

#env="TEST2"
#branchName="release/february20"

env="TEST4"

for gocdPipeLineBase in gocdToGitMap.keys():       
    bmGocdCommon.deployTestStage(gocdPipeLineBase, env);    
    #result=bmGitLabCommon.compareBranches(projName, "release/november19", "release/december19")

#log.info(bmGocdCommon.getEmailList())
log.info("Done!!!")