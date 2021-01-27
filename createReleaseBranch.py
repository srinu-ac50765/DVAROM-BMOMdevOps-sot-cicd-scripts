import bmGitLabCommon
import bmGitHubCommon
import logging
import warnings
warnings.filterwarnings("ignore")
log=logging.getLogger("createReleaseBranch")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

mergedList=[]
unmergedList=[]  
 
projMap=bmGitHubCommon.getprojMap()
log.debug(projMap)
for projName in projMap.keys():
    if projName.startswith('#'):
        continue
    #bmGitLabCommon.createBranch(projName, "release/april20", "release/may20")    
    #bmGitLabCommon.createBranch(projName, "release/december20", "release/january21")
    bmGitHubCommon.createBranch(projName, "release/january21", "release/february21")

log.info("Done!!!")