from common import bmGitHubCommon, bmJenkinsCommon
import logging
import warnings
import configparser
from urllib.parse import quote

warnings.filterwarnings("ignore")
# logging.basicConfig()
log = logging.getLogger("checkProjectChange")

logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

projMap = bmGitHubCommon.getprojMap()
projToJenkinsMap = bmGitHubCommon.getProjToJenkinsMap()
log.debug(projMap)
config = configparser.ConfigParser()
config.read('prod.properties')
branch1 = config.get('GeneralSection', 'branch1')
branch2 = config.get('GeneralSection', 'branch2')
jenkins_unified_url = config.get('GeneralSection', 'jenkins_unified_url')
currentReleaseBranch = config.get('GeneralSection', 'currentReleaseBranch')
projList = projMap.keys()
log.info("Compare branches: %s %s", branch1, branch2)
totalCount = 0
changedCount = 0
for projName in projList:
    if projName.startswith('#'):
        continue
    result = bmGitHubCommon.compareBranchesLastCommit(projName, branch1, branch2)
    #result = bmGitHubCommon.compareBranches(projName, branch1, branch2)
    jenkinsBase = projToJenkinsMap[projName]
    totalCount = totalCount + 1
    if result > 0:
        jenkins_url = jenkins_unified_url.replace('<ServiceName>', projName.split('/')[1])
        log.info(jenkins_url + quote(quote(currentReleaseBranch, safe=''), safe=''))
        #buildInfo = bmJenkinsCommon.getProdBuildNumberForUnified(jenkins_url)
        changedCount = changedCount + 1

log.info("\r\n\r\nTotal count: %s Changed count: %s", totalCount, changedCount)
log.info("Done!!!!!!!")
