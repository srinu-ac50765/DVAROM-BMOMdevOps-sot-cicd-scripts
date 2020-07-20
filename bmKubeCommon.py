import bmGitLabCommon
import logging
import warnings
import datetime

warnings.filterwarnings("ignore")

log=logging.getLogger("kubeCheckImages")
# 
# logger_handler = logging.StreamHandler()  # Handler for the logger
# logger_handler.setFormatter(logging.Formatter('%(message)s'))
# logging.root.addHandler(logger_handler)
# logging.root.setLevel(logging.INFO)

# podsFile is the output of kubectl get pods
# kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | awk '$2 <= "'$(date -d 'yesterday' -Ins --utc | sed 's/+0000/Z/')'" { print $1 }'
def checkPodsDate(podsFile, withinMinutes, kubeDeployList):
    imageMap = {}
    lineList = [line.rstrip('\n') for line in open(podsFile, "r")]    
    uncheckedList = kubeDeployList.copy()
    for line in lineList:  
        line = line.strip()
        if not line:
            continue
        # skip the test pipelines which we don't own
        if line.find('-test-') > -1:
             continue
        log.debug(line)
        pod, status, restarts, podStartTime =  line.split()
        
        # do we need to check the pod
        sotService = False
        for kubeDeploy in kubeDeployList:      
            if pod.find("bmp-kafka-adapter-invoker-service") > -1 and kubeDeploy == "bmp-kafka-adapter":
                continue 
            if pod.find(kubeDeploy) > -1:
                sotService = True
                if kubeDeploy in uncheckedList:
                    uncheckedList.remove(kubeDeploy)
                break
        if not sotService:
            continue
        
        if status != "Running":
            log.error("%s not running. status=%s", pod, status)
        elif int(restarts) > 0:
            log.warn("%s restarted %s times", pod, restarts)
        else:
            # for example, 2020-07-11T01:02:37Z. It's UTC            
            #startTime = datetime.datetime.strptime(podStartTime, "%y-%m-%dT%H:%M:%SZ")            
            startTime = datetime.datetime.strptime(podStartTime, "%Y-%m-%dT%H:%M:%SZ")
            refTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=withinMinutes)
            # log.debug("pod startTime:%s  refTime:%s", startTime, refTime)
            if startTime < refTime:
                log.error("%s not just deployed:%s", pod, podStartTime)
            else:
                log.debug("%s ok", pod)
    if uncheckedList:
        log.error("PODS NOT FOUND: %s", uncheckedList)

# For prod a file is the output of kubectl get deployments -o wide | awk  '\''{print $7 "\t",  $8}'\''
# for dev/test, remove the env name in addition 
def compareImages (file1Path, file2Path, kubeDeployList):
    #kubeDeployList = sorted(bmGitLabCommon.getProjConfigBaseMap().values())    
    
    imageMap1 = getImageMap(file1Path)
    imageMap2 = getImageMap(file2Path)
    
    for deploy in kubeDeployList:
        deploy = stripEnvSuffix(deploy)
        if not imageMap1.get(deploy, ""):        
            log.error("%s NOT in %s", deploy, file1Path)
            continue
        elif not imageMap2.get(deploy, ""):          
            log.error("%s NOT in %s", deploy, file2Path)
            continue
        else:
            if imageMap1[deploy] == imageMap2[deploy]:
               log.debug("%s OK: %s", deploy, imageMap1[deploy]) 
            else:
                log.error("%s error: %s-%s  %s-%s", deploy, file1Path, imageMap1[deploy], file2Path, imageMap2[deploy])

def getImageMap(fileName):
    imageMap = {}
    lineList = [line.rstrip('\n') for line in open(fileName, "r")]
    
    for line in lineList:
        line = line.strip()
        if not line:
            continue
        kubeDeploy,image = line.split()
        # if this if for dev/test, remove the environment
        kubeDeploy = stripEnvSuffix(kubeDeploy)            
        imageMap[kubeDeploy] = image
    return imageMap

def stripEnvSuffix(name):
        nameLower = name.lower()
        envTokens = ["-dev", "-test", "-bmpet"]
        for envToken in envTokens:            
            if nameLower.find(envToken) != -1:
                idx = name.rfind("-")
                name = name[0:idx:];
                break
        return name
    
# kubeDeployList = sorted(bmGitLabCommon.getProjConfigBaseMap().values())    
# #compareImages("c:/bm/bmpet1", "c:/bm/prod", kubeDeployList)
# checkPodsDate("c:/bm/test1-pod", 126000, kubeDeployList)    