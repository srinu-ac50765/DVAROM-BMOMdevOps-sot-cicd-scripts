import warnings
import logging
import datetime
import json
import base64
from github import Github
from pprint import pprint

warnings.filterwarnings("ignore")
log=logging.getLogger("bmGitLabCommon")
# key is GIT project name, value is GIT project id
projMap = {}
projToJenkinsMap = {}
jenkinsToGitMap = {}
projConfigBaseMap = {}
gitMissingCommitEmailSet = set()

def init():
    
    lineList = [line.rstrip('\n') for line in open("NewConfigInfo.txt", "r")]

    for line in lineList:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        log.debug(line)
        projName, configBase,jenkinsPipelineBase = line.split(",")
        projName = projName.strip()
        jenkinsPipelineBase = jenkinsPipelineBase.strip()
        configBase = configBase.strip()
       
        projMap[projName] = projName
        projToJenkinsMap[projName] = jenkinsPipelineBase
        jenkinsToGitMap[jenkinsPipelineBase]=projName          
        if configBase != "skip":
            projConfigBaseMap[projName] = configBase

def getprojMap():
    return projMap;

def getProjToJenkinsMap():
    return projToJenkinsMap;

def getJenkinsToGitMap():
    return jenkinsToGitMap;

def getMissingCommitEmailList():
    return gitMissingCommitEmailSet;

def getProjConfigBaseMap():
    return projConfigBaseMap;

def compareBranches(projectName, fromBranchName, targetBranchName):
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    log.debug("Saritha compareBranches %s", projectName) 
    project = gh.get_repo(projectName)
    log.debug("compareBranches %s from:%s to:%s", project.name, fromBranchName, targetBranchName)    
    try:
        fromBranch = project.get_branch(fromBranchName)
    except:
        raise Exception(projectName, " Invalid from branch " + fromBranchName)
        
    try:
        targetBranch = project.get_branch(targetBranchName)
    except:
        raise Exception(project.name, " Invalid target branch " + targetBranchName)        

    #result = project.repository_compare(oldBranch, newBranch)

    result = project.compare(targetBranchName, fromBranchName)._rawData
    # get the commits
    print(result) 
    retVal = -1;
    if result["total_commits"] == 0:
        retVal = 0
    else:
        log.info("\r\n%s from:%s to:%s", project.name, fromBranchName, targetBranchName) 
      
        firstCommit = result['commits'][0];
        for commit in result['commits']:  
            print(commit)          
            log.info(getCommitInfoString(commit))    
            gitMissingCommitEmailSet.add(commit["commit"]["author"]["email"]) 
        log.info("==================================================")
        log.info("Merge Owner:%s", firstCommit["commit"]["author"]["email"])   
        retVal = 1 
    return retVal
        
def getCommitInfoString(commit):
    #log.info("  commitId:%s  author:%s  date:%s msg:%s", commit["short_id"], commit["author_name"], commit["authored_date"], commit["title"])
    #commitInfoString="   commitId:%s  author_email:%s  date:%s msg:%s" % (commit["short_id"], commit["author_email"], commit["authored_date"], commit["title"])
    #print(commit)
    commitInfoString="   commitId:%s  author_email:%s  date:%s msg:%s" % (commit["sha"][0:7], commit["commit"]["author"]["email"], commit["commit"]["author"]["date"], commit["commit"]["message"].replace('\n\n',' '))
    #print(commitInfoString)
    return commitInfoString
def getBranchLastCommitInfo(projectName, branchName):
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    project = gh.get_repo(projectName)
    log.debug("getGitLastUpdateDate project:%s branch:%s", projectName, branchName)    
    try:
        branch = project.get_branch(branchName)
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
    print("List all the GitHub Repositories...")
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    count = 0    
    for repo in gh.get_user().get_repos():
        count=count+1
        print(repo)
        
    print("total project count", count)  
    
def createBranch(projectName, refBranchName, newBranchName):
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    project = gh.get_repo(projectName)     
    try:
        project.get_branch(fromBranchName)
        log.info("    %s %s already exist", projectName, newBranchName)
        return 0
    except:   
        log.info("createBranch %s from:%s to:%s", project.name, refBranchName, newBranchName)       
        try:        
            project.create_git_ref('refs/heads/{newBranchName}'.format(**locals()),project.get_branch(refBranchName).commit.sha)                            
        except:
            raise Exception(project.name, " error creating " + newBranchName + " from " + refBranchName)

def getBranchCommitInfo(projectName, branchName, releaseDate):
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    project = gh.get_repo(projectName)
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
    gh = Github(base_url="https://github.com/CenturyLink", login_or_token="142eeb26666a4067fd9df2efea676e98d20d78b8")
    gh = Github("142eeb26666a4067fd9df2efea676e98d20d78b8")
    project = gh.get_repo(projectName)
    log.debug("compareBranchesLastCommit %s %s %s", project.name, branch1Name, branch2Name)    
    branch1CommitId = ""
    branch2CommitId = ""
    try:
        branch1 = project.get_branch(branch1Name)
        #print(branch1.commit.__getattribute__("sha"))
        branch1CommitId = branch1.commit.__getattribute__("sha")
    except:
        log.info("New project %s", project.name)       
        try: 
            branch1CommitId = 0;                                   
        except:
            raise Exception(projectName, " Invalid from branch " + branch1Name)
        
    try:
        branch2 = project.get_branch(branch2Name)
        branch2CommitId = branch2.commit.__getattribute__("sha")
    except:
        raise Exception(project.name, " Invalid target branch " + branch2Name)    
    
    if branch1CommitId == branch2CommitId:
        return 0;
    else:
        return 1;    
                    
init()
#compareBranches("CenturyLink/BMOM-bbtcs-business-service" "release/december20", "release/january21")
#compareBranches("CenturyLink/BMOM-KafkaAdapter","release/november20","release/december20")

getAllProjects()
