from common import bmKubeCommon

import warnings
import logging

warnings.filterwarnings("ignore")
log=logging.getLogger("checkKubeImages")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

# This list includes all the submit services. Not only the incremental list. So comment it out
#kubeDeployList = sorted(bmGitLabCommon.getProjConfigBaseMap().values())
kubeDeployList =  [
"bmp-account-profile-service",
"bmp-account-treatment-business-service",
"bmp-billing-order-orchestrator-business-service",
"bmp-datamapping-business-service",
"bmp-directory-listing-business-service",
"bmp-directtv-om-service",
"bmp-dispatch-business-service",
"bmp-dtvoptout-business-service",
"bmp-dtv-treatment-business-service",
"bmp-ffwf-business-service",
"bmp-gman-gbus-business-service",
"bmp-isst-business-service",
"bmp-jeopardy-business-service",
"bmp-notification-business-service",
"bmp-oes-business-service",
"bmp-order-decomposition-business-service",
"bmp-order-management-business-service",
"bmp-order-management-process",
"bmp-order-status-update-business-service",
"bmp-provisioning-order-business-service",
"bmp-rules-mapping-service",
"bmp-service-delivery-orchestrator-business-service",
"bmp-service-registry-business-service",
"bmp-tom-orchestrator-business-service",
"bmp-update-email-account-business-service",
"cybersecurity-business-service",
"bmp-qconnect-service",
"bmp-armor-business-service",
"bmp-bmom-service-registry-business-service"
]

# generate the image files using command (or enhance the script to call it here)
# prod: in prod namespace
# kubectl get deployments -o wide | awk  '{print $7 "\t",  $8}'
# test: in test namespace, for example test1
# kubectl get deployments -o wide | awk  '{print $7 "\t",  $8}' | grep test1
# generate the image files using command (or enhance the script to call it here)
# prod: in prod namespace
# kubectl get deployments -o wide | awk  '\''{print $7 "\t",  $8}'\''
# test: in test namespace, for example test1
# kubectl get deployments -o wide | awk  '\''{print $7 "\t",  $8}'\'' | grep test1
# Replace -test1 and app= with empty string in TEST env
#TEST1 CMD
#kubectl get deployments -o wide | awk  '{print $8 "\t",  $7}' | grep test1 > c:/Users/AC60906/git/prodrelease/sot-cicd-scripts/bm/test1-image
#TEST2 CMD
#kubectl get deployments -o wide | awk  '{print $8 "\t",  $7}' | grep test2 > c:/Users/AC60906/git/prodrelease/sot-cicd-scripts/bm/test2-image
#TEST4 CMD
#kubectl get deployments -o wide | awk  '{print $8 "\t",  $7}' | grep test4 > c:/Users/AC60906/git/prodrelease/sot-cicd-scripts/bm/test4-image
#PROD CMD
#kubectl get deployments -o wide | awk  '{print $8 "\t",  $7}' > c:/Users/AC60906/git/prodrelease/sot-cicd-scripts/bm/prod-image
#PET1
#kubectl get deployments -o wide | awk  '{print $8 "\t",  $7}' | grep bmpet1 > c:/Users/AC60906/git/prodrelease/sot-cicd-scripts/bm/pet1-image-20
bmKubeCommon.compareImages("c:/bm/test1-image", "c:/bm/prod-image", kubeDeployList)
#checkPodsDate("c:/bm/test1-pod", 126000, kubeDeployList)    
log.info("Done!!!")