from gocd import Server
import datetime

import warnings
import logging
import gitlab
import bmGitLabCommon
import json
from urllib.request import HTTPError
from gocd.api.response import Response

import requests


warnings.filterwarnings("ignore")

log=logging.getLogger("bmGocdCommon")

# key is GOCD pipeline base, value is git project name
gocdToGitMap = {}
emailSet = set()

def init():
    
    lineList = [line.rstrip('\n') for line in open("ConfigInfo.txt", "r")]

    for line in lineList:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue        
        projName, projId, gocdPipelineBase = line.split(",")
        gocdToGitMap[gocdPipelineBase]=projName
       
# deployStageName, for example TEST1-DeployStage
def getGOCDLastBuildDate(pipelineName, deployStageName):
    server = Server('https://ne1itcprhas72.ne1.savvis.net:8154', user='bmpapp', password='FM59wYtos4WceVHT2nLaxRQh')
    #pipeline = server.pipeline('BMP_OrderDecompositionService_K8S_TEST4_DEPLOY')
    pipeline = server.pipeline(pipelineName)    
    
    response = pipeline.history()
    log.debug("GOCD response:%s", response.body)
    pipelineHistory=response.body    
    #buildTimeStamp = (datetime.datetime.now() - datetime.timedelta(days=100*365)).timestamp
    buildTimeStamp = 0.0
    
    for instance in pipelineHistory["pipelines"]:
        log.debug("pipeline label:%s", instance["label"])        
        lastDeployedFlag = False
        # starting on version 3.7, the dictionary will maintain the insertion order. 
        firstStage=instance["stages"][0];        
        for stage in instance["stages"]:                       
            if stage["name"] == deployStageName:
                if "result" in stage and stage["result"] == "Passed":
                    lastDeployedFlag = True                
                break
            else:
                continue
        if lastDeployedFlag == True:
            if firstStage["name"] == "buildStage":
                buildTimeStamp=firstStage["jobs"][0]["scheduled_date"]/1e3
            else:
                log.debug("%s first stage is %s", pipelineName, firstStage["name"])
                buildTimeStamp=firstStage["jobs"][0]["scheduled_date"]/1e3
            break
    return buildTimeStamp

def checkProjectDeploy(gocdPipelineBase, envName, branchName):
    gocdPipeline="%s_K8S_%s_DEPLOY" % (gocdPipelineBase, envName);
    deployStage="%s-DeployStage" % (envName) 
    log.debug("gocdPipeline:%s deployStage:%s", gocdPipeline, deployStage)    
    
    #gocdLastBuildDt = bmGocdCommon.getGOCDLastBuildDate("BMP_OrderDecompositionService_K8S_TEST1_DEPLOY")    
    gocdLastBuildDt = getGOCDLastBuildDate(gocdPipeline, deployStage)
    #log.debug("gocdLastBuildDt timestamp: %s", gocdLastBuildDt);
    #log.debug("gocdLastBuildDt local time: %s", datetime.datetime.fromtimestamp(gocdLastBuildDt))
    #log.debug("gocdLastBuildDt zulu time: %s", datetime.datetime.utcfromtimestamp(gocdLastBuildDt))

    #branchName="release/january20";
    #projectName="order-decomposition-business-service";
    gitProject=bmGitLabCommon.getGocdToGitMap()[gocdPipelineBase]
    log.debug("gitProject:%s", gitProject)
    '''
        retDict={}
    retDict["lastCommitTimstamp"]=commitTimestamp
    retDict["lastCommit"] = branch.commit
    return retDict
    '''
    gitLastCommitInfo=bmGitLabCommon.getBranchLastCommitInfo(gitProject, branchName)
    gitLastCommitDt=gitLastCommitInfo["lastCommitTimstamp"]
    #log.debug("gitLastCommitDt timestamp:%s", gitLastCommitDt)
    #log.debug("gitLastCommitDt local time:%s", datetime.datetime.fromtimestamp(gitLastCommitDt))
    #log.debug("gitLastCommitDt zulu time:%s", datetime.datetime.utcfromtimestamp(gitLastCommitDt))
    if gocdLastBuildDt > gitLastCommitDt:
        log.debug("%s OK", gocdPipeline)
        log.debug("    GOCD last build time (UTC):%s, GIT last commit time(UTC):%s", datetime.datetime.utcfromtimestamp(gocdLastBuildDt), datetime.datetime.utcfromtimestamp(gitLastCommitDt))
    else:
        log.info("%s", gocdPipeline)
        log.info("    GOCD last build time (UTC):%s, GIT last commit time(UTC):%s", datetime.datetime.utcfromtimestamp(gocdLastBuildDt), datetime.datetime.utcfromtimestamp(gitLastCommitDt))
        log.info("    %s", bmGitLabCommon.getCommitInfoString(gitLastCommitInfo["lastCommit"]));
        emailSet.add(gitLastCommitInfo["lastCommit"]["author_email"])
        
def getEmailList():
    return emailSet

def triggerPipeline(gocdPipelineBase, envName):
    gocdPipeline="%s_K8S_%s_DEPLOY" % (gocdPipelineBase, envName);
    server = Server('https://ne1itcprhas72.ne1.savvis.net:8154', user='bmpapp', password='FM59wYtos4WceVHT2nLaxRQh')
    #pipeline = server.pipeline('BMP_OrderDecompositionService_K8S_TEST4_DEPLOY')
    log.info("trigger %s", gocdPipeline)
    pipeline = server.pipeline(gocdPipeline)     
    headers={"Accept":"application/vnd.go.cd.v1+json", "Content-Type":"application/json", "X-GoCD-Confirm": "true"}
    #headers={"Accept":"application/vnd.go.cd.v1+json", "Content-Type":"application/json"}
    response = pipeline._request('/schedule', 202, {}, headers)    
    if response.is_ok == True:
        return 0
    else:
        log.error(" %s Error:%s .HTTP_STATUS:%s", gocdPipeline, response.payload['message'], response.status_code)
        return -1
    
def startDeployStage(gocdPipelineBase, envName, prevStageName, prevStagePassStatus, stageName, stagePassStatus):
    gocdPipeline="%s_K8S_%s_DEPLOY" % (gocdPipelineBase, envName);   
    server = Server('https://ne1itcprhas72.ne1.savvis.net:8154', user='bmpapp', password='FM59wYtos4WceVHT2nLaxRQh')
    #pipeline = server.pipeline('BMP_OrderDecompositionService_K8S_TEST4_DEPLOY')
    log.info("trigger %s", gocdPipeline)
    pipeline = server.pipeline(gocdPipeline)   
    pipelineHistory = pipeline.history();
    if (pipelineHistory.status_code == 404):    
        log.error("    %s pipeline not found", gocdPipeline)
        return -1
    pipelineInstances = pipelineHistory['pipelines']
    if not pipelineInstances:
        log.error("    >>>>>%s pipeline not triggered", gocdPipeline)
        return -1
    # last instance  
    instance=pipelineInstances[0];

    last_run = instance['counter']
    
    #testEnvStage = "TEST4-DeployStage"
    #devsiStage =  "DEVSI4-DeployStage"    
    #testEnvStageDone = False  
    #devsiStageDone = False
    stageMatch = False
    prevStageMatch = False
    stageStatus = ""
    prevStageStatus = ""

    for stage in instance["stages"]:                       
        if stage["name"] == stageName:
                if "result" in stage:
                    stageStatus = stage["result"]
                    
                    if stageStatus == "Passed":
                        if stagePassStatus:
                            stageMatch = True
                    elif not stagePassStatus:                      
                        stageMatch = True
                else:                
                    # if the stage has not run, there will be no stage["result']
                    stageMatch = not stagePassStatus
        elif stage["name"] == prevStageName:
                if "result" in stage:
                    prevStageStatus = stage["result"]
                    
                    if prevStageStatus == "Passed":
                        if prevStagePassStatus:
                            prevStageMatch = True
                    elif not prevStagePassStatus:
                        prevStageMatch = True
                                       
    log.debug("%s lastrun:%s", gocdPipeline, last_run)
    if stageMatch and prevStageMatch:
        log.info(    "%s ready for deploy. Instance:%s. %s:%s. %s:%s", gocdPipeline, last_run, prevStageName, prevStageStatus, stageName, stageStatus) 
        runStage(gocdPipelineBase, envName, last_run, stageName)
    else:
        log.info("    !!!!!!!!!!!!%s not ready. Instance:%s. %s:%s. %s:%s", gocdPipeline, last_run, prevStageName, prevStageStatus, stageName, stageStatus)

def runStage(gocdPipelineBase, envName, pipelineCount, stageName):    
    gocdPipeline="%s_K8S_%s_DEPLOY" % (gocdPipelineBase, envName); 
    
    gocdUrl="https://ne1itcprhas72.ne1.savvis.net:8154/go/run/%s/%s/%s" % (gocdPipeline, pipelineCount, stageName)
    log.info("    run %s", gocdUrl)
    
    gocdHeaders={"Accept":"application/vnd.go.cd.v1+json", "Content-Type":"application/json", "X-GoCD-Confirm": "true", "Confirm": "true"}    
    resp = requests.post(gocdUrl, data={}, auth=("bmpapp", "FM59wYtos4WceVHT2nLaxRQh"), headers=gocdHeaders, verify=False);

    if resp.ok == True and gocdUrl == resp.url:
        return 0
    else:
        log.error("Failed!!!!!!!!!!!!!")
        return -1
    

def bypassSonarStage(gocdPipelineBase, envName):
    startDeployStage(gocdPipelineBase, envName, "sonarQubeStage", False, "imageStage", False)
    
def deployTestStage(gocdPipelineBase, envName):
    testDeployStage = f"{envName}-DeployStage"
    devsiDeployStage = testDeployStage.replace("TEST", "DEVSI")
    startDeployStage(gocdPipelineBase, envName, devsiDeployStage, True, testDeployStage, False)  
    
def checkStageStatus(gocdPipelineBase, envName, stageName, instanceNumber):
    gocdPipeline="%s_K8S_%s_DEPLOY" % (gocdPipelineBase, envName);   
    server = Server('https://ne1itcprhas72.ne1.savvis.net:8154', user='bmpapp', password='FM59wYtos4WceVHT2nLaxRQh')
    #pipeline = server.pipeline('BMP_OrderDecompositionService_K8S_TEST4_DEPLOY')
    log.info("check %s", gocdPipeline)
    pipeline = server.pipeline(gocdPipeline)   
    pipelineHistory = pipeline.history();
    if (pipelineHistory.status_code == 404):    
        log.error("    %s pipeline not found", gocdPipeline)
        return -1
    pipelineInstances = pipelineHistory['pipelines']
    if not pipelineInstances:
        log.error("    >>>>>%s pipeline not triggered", gocdPipeline)
        return -1
    # last instance
    
    for instance in pipelineInstances:
        

        instanceCounter = instance['counter']
        
        if instanceNumber > instanceCounter:
            log.error("    >>>>>instance:%s not found. last:%s", instanceNumber, instanceCounter)
            break        
    
        if instanceNumber == -1 or instanceNumber == instanceCounter:    
            stageStatus = ""
        
            for stage in instance["stages"]:                       
                if stage["name"] == stageName:
                        if "result" in stage:                            
                            stageStatus = stage["result"]
                            
                            if stageStatus == "Passed":
                                log.debug("    passed!!!!!!")
                            else:
                                log.error("    status:" + stageStatus)
                        else:                
                            # if the stage has not run, there will be no stage["result']
                            stageStatus = "NotFound"
                            log.error("    >>>>>Stage not run yet")
                        break

            if not stageStatus:
                log.error("    >>>>>Stage not found")    
                
            break                               
    