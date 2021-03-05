from common import bmGitHubCommon
import logging
import warnings

warnings.filterwarnings("ignore")
log = logging.getLogger("createReleaseBranch")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

mergedList = []
unmergedList = []

projMap = bmGitHubCommon.getprojMap()
log.debug(projMap)
for projName in projMap.keys():
    if projName.startswith('#'):
        continue
    bmGitHubCommon.createBranch(projName, "release/march21", "release/april21")

log.info("Done!!!")
