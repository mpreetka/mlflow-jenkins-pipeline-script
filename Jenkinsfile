def nodeLabel = 'mlops'
#import groovy.json.*
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
        stage('MLFlow model retraining') {
            agent {
                kubernetes {
                    cloud 'amr_service'
                    inheritFrom nodeLabel
                    yaml """
                    apiVersion: v1
                    kind: Pod
                    metadata:
                        labels:
                        worker: ${nodeLabel}
                    spec:
                        containers:
                        - name: jnlp
                          image: gar-registry.caas.intel.com/cifordi/jenkins-inbound-agent:jdk8
                          args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
                          
                        - name: python
                          image: gar-registry.caas.intel.com/cifordi/python:latest
                          command:
                          - cat
                          tty: true
                    """
    
                }
            }
            steps {
                container("python") {
                        echo "Get python version"
                        sh "python -V"
                        sh "python hello.py"
                }
            }
        }
        
        stage("get MLflow models") {
            agent any 
            steps {
                script {
                    // preview has to be added for 1.11.0
                    def mlflow_models_string = sh(script: "curl -X GET https://mlflow.malina.intel.com/api/2.0/mlflow/registered-models/list -k", returnStdout:true).trim()
                    def new_models = [:]
                    def all_models = []
                    new_models = get_new_models(mlflow_models_string)
                    all_models = new_models.keySet()
                    println("mlflow_models_string")
                    println(mlflow_models_string)
                }
            }
        }
    }
}
@NonCPS
def get_new_models(String mlflow_models_string) {
    def jsonSlurper = new JsonSlurper()
    def mlflow_models = jsonSlurper.parseText(mlflow_models_string).registered_models
    mlflow_models_string = null
    jsonSlurper = null
    def now = new Date()
    def now_seconds = now.getTime()
    def staging_models = [:]
    for (int i=0; i<mlflow_models.size(); i++) {
      
        def these_models = mlflow_models[i].latest_versions
        for (int j=0; these_models && j<these_models.size(); j++) {
            println(these_models[j])
            if (these_models[j].current_stage == "Staging") {
                //println(staging_model.getClass())
                staging_models[these_models[j].name] = [version: these_models[j].version, run_id: these_models[j].run_id]
                break
                //staging_model = null
            }
        }
        these_models = null
    }
    return staging_models
}
