import bmGitLabCommon
import logging
import warnings
warnings.filterwarnings("ignore")

log=logging.getLogger("createBranch")
logger_handler = logging.StreamHandler()  # Handler for the logger
logger_handler.setFormatter(logging.Formatter('%(message)s'))
logging.root.addHandler(logger_handler)
logging.root.setLevel(logging.INFO)

#result=bmGitLabCommon.compareBranches("billing-order-orchestrator-business-service", "release/november19", "release/december19")
#result=bmGitLabCommon.compareBranches("order-decomposition-business-service", "release/november19", "release/december19")

result=bmGitLabCommon.createBranch("bmp-martens-orders-service", "release/april20", "release/may20")

log.info("Done!!!")