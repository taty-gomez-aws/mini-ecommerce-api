pipeline {
    agent any

    environment {
        IMAGE_NAME = "mini-ecommerce-api"
        IMAGE_TAG  = "${BUILD_NUMBER}"
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
    }

    post {
        always {
            sh 'docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true'
        }
        success {
            echo '✅ Build y tests superados correctamente'
        }
        failure {
            echo '❌ El build o los tests han fallado'
        }
    }
}