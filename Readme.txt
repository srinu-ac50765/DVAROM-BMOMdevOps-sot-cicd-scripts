Core scripts:
bmGitLabCommon.py - GitLab related functions
bmGocdCommon.py - GoCD related functions
bmJenkinsCommon.py - Jenkins related functions
KubeCheckImage.py - Kubernetes related functions
All the other files are just simple scripts that invoke the above functions

1. Set up ConfigInfo.txt. This is required in order to run any of our scripts.
2. Check release merge: checkReleaseMerge.py
3. Check whether latest code is deployed in GOCD: checkReleaseDeploy.py
4. Check commits before and after a release: checkReleaseCommit.py
5. Cut a branch: createReleaseBranch.py
6. Trigger GOCD pipeline: triggerReleaseDeploy.py
7. Bypass SONAR stage in GoCD pipelines: bypassReleaseSonarStage.py.
	If sonar stage is already passed, the script will not do anything
8. Run TESTX-DeployStage in GoCD pipelines: deployReleaseStage.py
9. checkProjectChange: compare two branches' last commit. The output is the a service list for incremental production deployment.
10. checkProperties: check whether there is GIT change after given date on a source directory(test1), if yes, 
     compare the property names of source with destination directory.
11. Cut Jenkins pipeline and versions: cutJenkinsProdVersion.
12. Check whether latest code is deployed in Jenkins: checkJenkinsReleaseDeploy
13. Batch trigger Jenkins pipelines: triggerJenkinsReleasePipelines.py
    This can be used to deploy a new environment
14. Batch trigger Proceed in Jenkins Test-ReleaseGate stage: JenkinsReleaseTestDeploy
15. check Jenkins pipelines status: checkJenkinsReleaseStatus  
16. check kubenetes images in two enviroment: checkKubeImage
17. check kubenetes pod deployment: checkKubeDeploy

Most of the above scripts have corresponding scripts that operator on a single project level. A project level script contains
key word "Project" in its name.