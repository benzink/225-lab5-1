pipeline {
    agent any 

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/benzink'  //<-- change to your MiamiID
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/benzink/225-lab5-1.git' //<-- your repo URL
        KUBECONFIG = credentials('benzink-225') //<-- your Kubernetes credentials ID
    }

    stages {
        stage('Code Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                script {
                    def kubeConfig = readFile(KUBECONFIG)
                    sh "kubectl delete --all deployments --namespace=default || true"
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        stage('Generate Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "sleep 15"
                    sh "kubectl exec ${appPod} -- python3 data-gen.py"
                }
            }
        }

        stage("Run Acceptance Tests") {
            steps {
                script {
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run qa-tests'
                }
            }
        }

        stage('Remove Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 data-clear.py"
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "✅ Build Completed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        unstable {
            slackSend color: "warning", message: "⚠️ Build Unstable: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            slackSend color: "danger", message: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
