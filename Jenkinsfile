pipeline {
    agent any

    environment {
        IMAGE_NAME = "mini-ecommerce-api"
        AWS_REGION = 'us-east-1'
        ECR_REPO   = '784230179950.dkr.ecr.us-east-1.amazonaws.com/mini-ecommerce-api'
        IMAGE_TAG  = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} pytest'
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}
                '''
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}:latest

                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true'
        }
        success {
            echo '✅ Build, tests y push a ECR completados correctamente'
        }
        failure {
            echo '❌ El pipeline ha fallado'
        }
    }
}