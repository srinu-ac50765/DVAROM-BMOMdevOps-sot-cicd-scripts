1. Set up ConfigInfo.txt. This is required in order to run any of our scripts.
2. Check release merge: checkReleaseMerge.py
3. Check whether latest code is deployed in GOCD: checkReleaseDeploy.py
4. Check commits before and after a release: checkReleaseCommit.py
5. Cut a branch: createReleaseBranch.py
6. Trigger GOCD pipeline: triggerReleaseDeploy.py
7. Bypass SONAR stage: bypassReleaseSonarStage.py.
	If sonar stage is already passed, the script will not do anything
8. Run TESTX-DeployStage: deployReleaseStage.py
9. checkProjectChange: compare two branches' last commit. Can be used for determining candidates for incremental deployment.
10. checkProperties: check whether there is GIT change after given date on a source branch(test1), if yes, 
      compare the property names of source with destination branch.

Most of the above scripts have corresponding scripts that operator on a single project level. A project level script contains
key word "Project" in its name.