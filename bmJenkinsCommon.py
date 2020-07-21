import jenkins
import os
import requests
import datetime

import warnings
import logging
import gitlab
import bmGitLabCommon
import json
from urllib.request import HTTPError
from gocd.api.response import Response

import requests
from jenkins import CRUMB_URL
from _overlapped import NULL

os.environ.setdefault("PYTHONHTTPSVERIFY", "0")
warnings.filterwarnings("ignore")
log=logging.getLogger("bmJenkinsCommon")


# logger_handler = logging.StreamHandler()  # Handler for the logger
# logger_handler.setFormatter(logging.Formatter('%(message)s'))
# logging.root.addHandler(logger_handler)
# logging.root.setLevel(logging.INFO)

# key is GOCD pipeline base, value is git project name
emailSet = set()
  
jenkinsUser = "ab83099"
jenkinsPasswd = "dfa376d5b79537b1032fc3a185bbd10a"
server = jenkins.Jenkins('https://ne1itcprhas70.ne1.savvis.net:8443/', username=jenkinsUser, password=jenkinsPasswd)
def getCrumb():
     crumbUrl = 'https://ne1itcprhas70.ne1.savvis.net:8443/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)';
     crumbResponse = requests.get(crumbUrl, auth=(jenkinsUser,jenkinsPasswd), verify=False)
       
     crumb=crumbResponse.text
     log.info("crumb:" + crumb)
     crumbKey,crumbValue = crumb.split(":")
     crumbHeader={}
     crumbHeader[crumbKey] =  crumbValue
     return crumbHeader
crumbHeader = getCrumb()
         
def triggerPipeline(pipeline):
          
    server = jenkins.Jenkins('https://ne1itcprhas70.ne1.savvis.net:8443/', username=jenkinsUser, password=jenkinsPasswd)
          
    # exception will be thrown if there is problem
    log.info("triggering %s", pipeline)
    response = server.build_job(pipeline) 
    
def deployTestStage(pipeline, buildNumber):    
    jobLastStage = getBuildLastStage(pipeline, buildNumber)    
    if not jobLastStage:
        log.error("%s/%s TEST-Deploy NOT READY - first stage not started yet", pipeline, buildNumber)            
    elif jobLastStage['name'] == 'TEST-ReleaseGate' and jobLastStage['status'] == 'PAUSED_PENDING_INPUT':
        getPendingUrl = "https://ne1itcprhas70.ne1.savvis.net:8443/job/BMP_OrderManagementProcess-test1-CONTINUOUS/7/wfapi/pendingInputActions"
        pendingInfoUrl = f"https://ne1itcprhas70.ne1.savvis.net:8443/job/{pipeline}/{buildNumber}/wfapi/pendingInputActions"
        log.debug("pendingInfoUrl:%s", pendingInfoUrl)
        jenkinsHeaders={}
        #crumbHeader = getCrumb()
        jenkinsHeaders.update(crumbHeader)        
        response = requests.get(pendingInfoUrl, auth=(jenkinsUser,jenkinsPasswd), headers=jenkinsHeaders, verify=False)
        log.debug("pendingInputActions response:%s", response.text)                
        data = response.json()
        if len(data) < 1:
            log.error("%s Failed: Cannot get pendingInfo", pipeline)
        else:
            proceedUrl = data[0]["proceedUrl"];
            url = f"https://ne1itcprhas70.ne1.savvis.net:8443{proceedUrl}"
            log.debug("URL to proceed:%s", url)
#             payload = "json=%7B%7D&proceed=Yes"
            payload = "json={}&proceed=Yes"
            jenkinsHeaders["Content-Type"] = "application/x-www-form-urlencoded"
            response = requests.post(url, data=payload, auth=(jenkinsUser,jenkinsPasswd), headers=jenkinsHeaders, verify=False)
            if not response.ok:
                log.error("%s/%s Failed to trigger TEST-Deploy: %s", pipeline, buildNumber, response.reason)
            else:
                log.info("%s/%s succeed", pipeline, buildNumber)
    else:
        log.error("%s/%s TEST-Deploy CANNOT BE TRIGGERED. Last stage: %s, status: %s", pipeline, buildNumber, jobLastStage['name'], jobLastStage['status'])
      
def getPipelineName(pipelineBase, envName): 
    envName = envName.lower()
    pipelineName = "";
    if "test4" == envName:
        pipelineName = "%s-CONTINUOUS" % (pipelineBase)
    else:
        pipelineName = "%s-%s-CONTINUOUS" % (pipelineBase, envName)
    return pipelineName          
      
def getBuildLastStage(pipeline, buildNumber):    
    buildStages = getBuildStages(pipeline, buildNumber)
      
    retVal = NULL
    if buildStages and len(buildStages) > 0:
        retVal = buildStages[-1]
    return retVal

def getBuildFirstStage(pipeline, buildNumber):    
    buildStages = getBuildStages(pipeline, buildNumber)
      
    retVal = NULL    
    if buildStages and len(buildStages) > 0:
        retVal = buildStages[0]
    return retVal

def getBuildStages(pipeline, buildNumber):    
    jenkinsHeaders={}
    #crumbHeader = getCrumb()
    jenkinsHeaders.update(crumbHeader)
  
    wfapiUrl = "https://ne1itcprhas70.ne1.savvis.net:8443/view/BMP/job/" + pipeline + "/" + str(buildNumber) + "/wfapi/"
    log.debug("wfapiUrl:%s", wfapiUrl)
      
    response = requests.get(wfapiUrl, auth=(jenkinsUser,jenkinsPasswd), headers=jenkinsHeaders, verify=False)
    if response.ok:
        log.debug("response:%s", response.text) 
        data = response.json()    
        return data['stages']
    else:
        log.error("request:%s   response:%s", wfapiUrl, response.text)
        return NULL
  
def getProdBuildNumber(pipeline):  

    buildNumber = getLatestBuildNumberByLastStage(pipeline, "PROD-ReleaseGate", "PAUSED_PENDING_INPUT")
    prodDeployNumber,prodBuildDt = getLatestBuildNumberByStage(pipeline, "PROD-Deploy", "")
     
    if buildNumber == -1:
        log.error("%s: NO BUILD AVAILABLE", pipeline)    
    else:
        if (prodDeployNumber == None or prodDeployNumber < buildNumber):
            log.info("%s/%s", pipeline, str(buildNumber))
        else:
            buildLastStage = getBuildLastStage(pipeline, prodDeployNumber)
            log.info("%s/%s. But build %s already in %s stage status:%s", pipeline, str(buildNumber), str(prodDeployNumber), buildLastStage['name'], buildLastStage['status'])
        
def getTestDeployBuildNumber(pipeline):   
    buildNumber = getLatestBuildNumberByLastStage(pipeline, "TEST-ReleaseGate", "PAUSED_PENDING_INPUT")
    if buildNumber == -1:
        log.error("%s: NO BUILD AVAILABLE", pipeline)
    else:
        log.info("%s/%s", pipeline, str(buildNumber))

def getLatestBuildNumberByStage(pipeline, stageName=None, stageStatus=None, checkLastStageOnly = False):
    allJobs = server.get_job_info(pipeline, 0, True)
    
    theBuildNumber = None
    theBuildStartedDate = None
    
    # the job list is ordered by time, latest one on top
    for build in allJobs["builds"]:  

        buildNumber = build["number"]      
        stages = getBuildStages(pipeline, buildNumber)
        stageMatch = False
        jenkinsBuildDt = None  
          
        if stages and len(stages) > 0:  
            if checkLastStageOnly:                
                lastStage = stages[-1] 
                stageMatch = (((not stageName) or lastStage['name'] == stageName) and (not stageStatus) or lastStage['status'] == stageStatus)    

            for stage in stages:             
                if stage['name'] == 'Build':
                    #log.debug("startTimeMillis:%s", stage['startTimeMillis'])
                    jenkinsBuildDt=stage['startTimeMillis']/1e3
                    log.debug("buildNumber:%s  jenkinsBuildDt:%s", buildNumber, jenkinsBuildDt)
                elif ((not stageMatch) and (not checkLastStageOnly)):                   
                    stageMatch = (((not stageName) or stage['name'] == stageName) and ((not stageStatus) or stage['status'] == stageStatus))   

            if (stageMatch):
                theBuildNumber = buildNumber
                theBuildStartedDate = jenkinsBuildDt
                break; 
             
        if stageMatch:                                                           
            break
            
    return (theBuildNumber, theBuildStartedDate)
    

def getLatestBuildNumberByLastStage(pipeline, lastStageName=None, lastStageStatus=None):    
    allJobs = server.get_job_info(pipeline, 0, True)
    retVal = -1
    for build in allJobs["builds"]:  

        buildNumber = build["number"] 
        if lastStageName == None and lastStageStatus == None:
            log.debug("build number:%s for pipeline %s", buildNumber, pipeline)
            retVal = buildNumber            
            break     
        
        jobLastStage = getBuildLastStage(pipeline, buildNumber)
        if not jobLastStage:
            log.debug("%s/%s not ready - first stage not started", pipeline, buildNumber)            
        elif jobLastStage['name'] == lastStageName and ((not lastStageStatus) or jobLastStage['status'] == lastStageStatus):
            retVal = buildNumber
            log.debug("build number:%s for pipeline %s, lastStageName:%s, lastStageStatus:%s", str(buildNumber), pipeline, lastStageName, lastStageStatus)             
            break
        else:            
            log.debug("%s/%s not ready - %s - %s", pipeline, buildNumber, jobLastStage['name'], jobLastStage['status'])
    if retVal == -1:
        log.debug("BUILD NOT FOUND for pipeline %s, lastStageName:%s, lastStageStatus:%s", pipeline, lastStageName, lastStageStatus)
    return retVal


def checkProjectDeploy(pipelineBase, envName, branchName):
    pipeline = getPipelineName(pipelineBase, envName)
    deployStage="TEST-Deploy"
    log.debug("jenkinsPipeline:%s deployStage:%s", pipeline, deployStage)  
    buildNumber = None
    

    buildNumber, jenkinsBuildDt = getLatestBuildNumberByStage(pipeline, "TEST-Deploy", "SUCCESS")
    
    if buildNumber == None:
        log.error("%s doesn't have a qualified build", pipeline)
        return -1
    elif jenkinsBuildDt == None:
        log.error("%s doesn't have build", pipeline)
        return -1
                 
    gitProject=bmGitLabCommon.getJenkinsToGitMap()[pipelineBase]
    log.debug("gitProject:%s", gitProject)

    gitLastCommitInfo=bmGitLabCommon.getBranchLastCommitInfo(gitProject, branchName)
    gitLastCommitDt=gitLastCommitInfo["lastCommitTimstamp"]
    log.debug("gitLastCommitDt:%s", gitLastCommitDt)
    #log.debug("gitLastCommitDt timestamp:%s", gitLastCommitDt)
    #log.debug("gitLastCommitDt local time:%s", datetime.datetime.fromtimestamp(gitLastCommitDt))
    #log.debug("gitLastCommitDt zulu time:%s", datetime.datetime.utcfromtimestamp(gitLastCommitDt))
    if jenkinsBuildDt > gitLastCommitDt:
        log.debug("%s OK", pipeline)
        log.debug("    JENKINS last build time (UTC):%s, GIT last commit time(UTC):%s", datetime.datetime.utcfromtimestamp(jenkinsBuildDt), datetime.datetime.utcfromtimestamp(gitLastCommitDt))
    else:
        log.info("%s", pipeline)
        log.info("    JENKINS last build time (UTC):%s, GIT last commit time(UTC):%s", datetime.datetime.utcfromtimestamp(jenkinsBuildDt), datetime.datetime.utcfromtimestamp(gitLastCommitDt))
        log.info("    %s", bmGitLabCommon.getCommitInfoString(gitLastCommitInfo["lastCommit"]));
        emailSet.add(gitLastCommitInfo["lastCommit"]["author_email"])   
 