from gocd import Server
import datetime
import bmGitLabCommon
import bmGocdCommon

import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig()
logging.root.setLevel(logging.INFO)
log=logging.getLogger("checkProjectDeploy")

#bmGocdCommon.checkProjectDeploy("BMP_DirectoryListingBusinessService", "TEST1", "release/january20")        
bmGocdCommon.checkProjectDeploy("account-management-business-service", "TEST1", "release/march20")
#bmGocdCommon.checkProjectDeploy("BMP_AccountManagmentService", "TEST1", "release/january20")
