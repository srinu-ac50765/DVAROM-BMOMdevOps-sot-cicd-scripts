import git
import datetime
import logging
import bmGitLabCommon

log=logging.getLogger("checkProperties")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

#class PropertiesChecker:
class checkProperties:
    def __init__(self, repoDir, srcEnv, targetEnv, cutoffDate = "1900-01-01 01:01:01 +0000"):
        self.repoDir = repoDir
        self.srcEnv = srcEnv
        self.targetEnv = targetEnv
        self.git = git.Git(repoDir) 
        self.cutoffDate = datetime.datetime.strptime(cutoffDate, '%Y-%m-%d %H:%M:%S %z')
        
    def getFileName(self, env, serviceName):
        env = env.lower()
        serviceName = serviceName.lower()
        fileName = ""
        if env != "prod":
            fileName = f"{env}/{serviceName}-{env}.properties"
        else:
            fileName = f"{env}/{serviceName}.properties"
        return fileName;
    
    def compareDates(self, service):
        srcFileName = self.getFileName(self.srcEnv, service)
        targetFileName = self.getFileName(self.targetEnv, service)
                
        # %ci  commit date in ISO 8601-like format
        srcLastCommitDateStr = self.git.log('-1', '--pretty=%ci', srcFileName)       
        srcLastCommitDate = datetime.datetime.strptime(srcLastCommitDateStr, '%Y-%m-%d %H:%M:%S %z')
        
        targetCommitDateStr = self.git.log('-1', '--pretty=%ci', targetFileName)        
        targetLastCommitDate = datetime.datetime.strptime(targetCommitDateStr, '%Y-%m-%d %H:%M:%S %z')
        
        retCode = 0
        if srcLastCommitDate > self.cutoffDate: 
            if srcLastCommitDate > targetLastCommitDate:
                errorInfo = f"{service}: {self.srcEnv} is updated after {self.targetEnv}"
                log.error(errorInfo)
                log.error("    %s:%s  %s:%s", self.srcEnv, srcLastCommitDateStr, self.targetEnv, targetCommitDateStr)
                retCode = 1
            else:
                log.info("%s: %s:%s %s:%s", service, self.srcEnv, srcLastCommitDateStr, self.targetEnv, targetCommitDateStr)
                retCode = 0
        else:
            log.debug("%s %s:%s %s:%s - source updated before start date", service, self.srcEnv, srcLastCommitDateStr, self.targetEnv, targetCommitDateStr)
            retCode = 0
            
    def compareContents(self, service):
        srcFileName = self.getFileName(self.srcEnv, service)
        targetFileName = self.getFileName(self.targetEnv, service)  
        srcMap = self.readConfigFile(self.repoDir + "/" + srcFileName)
        targetMap = self.readConfigFile(self.repoDir + "/" + targetFileName) 
        srcSet = set(srcMap.keys())
        targetSet = set(targetMap.keys())
        srcNotInTarget =  srcSet.difference(targetSet);
        retVal = 0
        if srcNotInTarget:
            log.error("    %s: %s in %s but not in %s", service, srcNotInTarget, self.srcEnv, self.targetEnv)
            retVal = 1
        return retVal
        
        

    def readConfigFile(self, fileName):
        pMap = {}
        lineList = [line.rstrip('\n') for line in open(fileName, "r")]
    
        for line in lineList:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue            
            sepIdx = line.find("=")
            
            if sepIdx < 0:
                log.error("    %s: %s not contain =", fileName, line)
                continue
            else:
                propertyName = line[0:sepIdx]
                propertyValue = line[sepIdx:]
            propertyName = propertyName.strip()
            propertyValue = propertyValue.strip()
            pMap[propertyName]=propertyValue
        return pMap
    def diffServiceProperties(self, service):        
        retCode = self.compareDates(service) 
        retCode = self.compareContents(service) 
                            
    def diffReleaseProperties(self):
        for service in bmGitLabCommon.projConfigBaseMap.values():
            self.diffServiceProperties(service)         
                
        
x = checkProperties("c:/users/nxli/git/bmom/bmp-config-repo", "test2", "prod", "2020-05-05 01:01:01 +0000") 
#x = checkProperties("c:/users/nxli/git/bm/tmp/bmp-config-repo", "test1", "prod", "2020-02-28 01:01:01 +0000")
#x.diffServiceProperties("bmp-bmom-service-registry-business-service") 
#x.diffServiceProperties("bmp-martens-orders-service")
#x.diffServiceProperties("bmp-billing-order-orchestrator-business-service")    
x.diffReleaseProperties() 
log.info("Done!!!!!!!!!!!!")