import gitlab
import warnings
import logging
import datetime
import json

warnings.filterwarnings("ignore")
log=logging.getLogger("bmGitLabCommon")
# key is GIT project name, value is GIT project id
projMap = {}
projToGocdMap = {}
gocdToGitMap = {}
projConfigBaseMap = {}
gitMissingCommitEmailSet = set()

def init():
    
    lineList = [line.rstrip('\n') for line in open("ConfigInfo.txt", "r")]

    for line in lineList:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        projName, projId, gocdPipelineBase,configBase = line.split(",")
        projName = projName.strip()
        projId = projId.strip()
        gocdPipelineBase = gocdPipelineBase.strip()
        configBase = configBase.strip()
        
        
        projMap[projName] = projId
        projToGocdMap[projName] = gocdPipelineBase
        gocdToGitMap[gocdPipelineBase]=projName            
        if configBase != "skip":
            projConfigBaseMap[projName] = configBase

def getprojMap():
    return projMap;

def getProjToGocdMap():
    return projToGocdMap;

def getGocdToGitMap():
    return gocdToGitMap;

def getMissingCommitEmailList():
    return gitMissingCommitEmailSet;


def compareBranches(projectName, fromBranchName, targetBranchName):
    projectId=projMap[projectName]
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    project = gl.projects.get(projectId)
    log.debug("compareBranches %s from:%s to:%s", project.name, fromBranchName, targetBranchName)    
    try:
        fromBranch = project.branches.get(fromBranchName)
    except:
        raise Exception(projectName, " Invalid from branch " + fromBranchName)
        
    try:
        targetBranch = project.branches.get(targetBranchName)
    except:
        raise Exception(project.name, " Invalid target branch " + targetBranchName)        

    #result = project.repository_compare(oldBranch, newBranch)
    result = project.repository_compare(targetBranchName, fromBranchName)
    # get the commits
    retVal = -1;
    if len(result['diffs']) == 0:
        retVal = 0
    else:
        log.info("\r\n%s from:%s to:%s", project.name, fromBranchName, targetBranchName) 
        
        firstCommit = result['commits'][0];
        for commit in result['commits']:            
            log.info(getCommitInfoString(commit))    
            gitMissingCommitEmailSet.add(commit["author_email"]) 
        log.info("==================================================")
        log.info("Merge Owner:%s", firstCommit["author_email"])   
        retVal = 1 
    return retVal
        
def getCommitInfoString(commit):
    #log.info("  commitId:%s  author:%s  date:%s msg:%s", commit["short_id"], commit["author_name"], commit["authored_date"], commit["title"])
    commitInfoString="   commitId:%s  author_email:%s  date:%s msg:%s" % (commit["short_id"], commit["author_email"], commit["authored_date"], commit["title"])
    return commitInfoString
def getBranchLastCommitInfo(projectName, branchName):
    projectId=projMap[projectName]
    #projectId=1305
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    project = gl.projects.get(projectId)
    log.debug("getGitLastUpdateDate projectId:%s project:%s branch:%s", projectId, projectName, branchName)    
    try:
        branch = project.branches.get(branchName)
    except:
        raise Exception(project.name, " Invalid branch " + branchName)                 
    
    lastCommitDt=branch.commit["created_at"]
    
    #lastCommitDt example "2019-12-17T17:53:41.000Z";        
    lastCommitDtObj = datetime.datetime.strptime(lastCommitDt, '%Y-%m-%dT%H:%M:%S.%f%z')
    commitTimestamp=datetime.datetime.timestamp(lastCommitDtObj);
    lastCommitInfo={}
    lastCommitInfo["lastCommitTimstamp"]=commitTimestamp
    lastCommitInfo["lastCommit"] = branch.commit
    return lastCommitInfo

def getAllProjects():
    print("This will take a few minutes ...")
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    projects = gl.projects.list(all=True)
    
    allProjIdMap={}
    for project in projects:
        #print(project['id'])
        #print(project)
        allProjIdMap[project.name]=project.id
        print(project.id, ":", project.name)
        json_string = json.dumps(project._attrs)
        (json_string)
    
    print("total project count", len(projects))  
     
def createBranch(projectName, refBranchName, newBranchName):
    projectId=projMap[projectName]
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    project = gl.projects.get(projectId)
     
    try:
        project.branches.get(newBranchName)
        log.info("    %s %s already exist", projectName, newBranchName)
        return 0
    except:   
        log.info("createBranch %s from:%s to:%s", project.name, refBranchName, newBranchName)       
        try:        
            project.branches.create({"branch": newBranchName,
                                 "ref": refBranchName})
        except:
            raise Exception(project.name, " error creating " + newBranchName + " from " + refBranchName)

def getBranchCommitInfo(projectName, branchName, releaseDate):
    projectId=projMap[projectName]
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    project = gl.projects.get(projectId)
    log.debug("getBranchCommitInfo %s branch:%s date:%s", project.name, branchName, releaseDate)    
    commits = project.commits.list(all=True,
                               query_parameters={'ref_name': branchName})
    beforeReleaseCommitCount = 0;
    afterReleaseCommitCount = 0
    beforeReleaseAuthor = set()
    afterReleaseAuthor = set()
    
    for commit in commits:      
        commitInfo = commit.attributes;  
        #xyz = getCommitInfoString(commitInfo)
        # commitInfoString="   commitId:%s  author_email:%s  date:%s msg:%s" % (commit["short_id"], commit["author_email"], commit["authored_date"], commit["title"])
        commitDateString = commitInfo["authored_date"]
        commitDate = datetime.datetime.strptime(commitDateString, '%Y-%m-%dT%H:%M:%S.%f%z')
        if commitDate > releaseDate: 
            afterReleaseCommitCount = afterReleaseCommitCount + 1;
            afterReleaseAuthor.add(commitInfo["author_name"])
        else: 
            beforeReleaseCommitCount = beforeReleaseCommitCount + 1
            beforeReleaseAuthor.add(commitInfo["author_name"])
    
    
    if afterReleaseAuthor:
        summary = f"{projectName}:{beforeReleaseCommitCount}:{afterReleaseCommitCount}:{beforeReleaseAuthor}:{afterReleaseAuthor}"        
    else:
        summary = f"{projectName}:{beforeReleaseCommitCount}:{afterReleaseCommitCount}:{beforeReleaseAuthor}"
            
    #summary = f"{projectName}:{afterReleaseCommitCount}:{afterReleaseAuthor}"    
    log.info(summary)    
    retMap = {}
    retMap["beforeCount"] =  beforeReleaseCommitCount;
    retMap["afterCount"] =  afterReleaseCommitCount;
    return retMap;

def compareBranchesLastCommit(projectName, branch1Name, branch2Name):
    projectId=projMap[projectName]
    gl = gitlab.Gitlab('https://ne1itcprhas62.ne1.savvis.net', private_token='sRKyruzyTU3cbd9TWypc', ssl_verify=False)
    project = gl.projects.get(projectId)
    log.debug("compareBranchesLastCommit %s %s %s", project.name, branch1Name, branch2Name)    
    branch1CommitId = ""
    branch2CommitId = ""
    try:
        branch1 = project.branches.get(branch1Name)
        branch1CommitId = branch1.attributes["commit"]["id"]
    except:
        raise Exception(projectName, " Invalid from branch " + branch1Name)
        
    try:
        branch2 = project.branches.get(branch2Name)
        branch2CommitId = branch2.attributes["commit"]["id"]
    except:
        raise Exception(project.name, " Invalid target branch " + branch2Name)    
    
    if branch1CommitId == branch2CommitId:
        return 0;
    else:
        return 1;    
                    
init()

#getAllProjects()
