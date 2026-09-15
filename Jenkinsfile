pipeline {
    agent any

    environment {
	    IMAGE_NAME       = "mini-ecommerce-api"
	    AWS_REGION       = 'us-east-1'
	    ECR_REPO         = '784230179950.dkr.ecr.us-east-1.amazonaws.com/mini-ecommerce-api'
	    IMAGE_TAG        = "${env.GIT_COMMIT.take(7)}"
	    PROD_INSTANCE_ID = 'i-0e1263811a49efb09'
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

        stage('Approve Deploy') {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    input message: '¿Desplegar esta imagen a producción?', ok: 'Deploy'
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    COMMAND_ID=$(aws ssm send-command \
                    --instance-ids "$PROD_INSTANCE_ID" \
                    --document-name "AWS-RunShellScript" \
                    --parameters commands=["aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}","docker pull ${ECR_REPO}:${IMAGE_TAG}","docker stop ${IMAGE_NAME} || true","docker rm ${IMAGE_NAME} || true","docker run -d --name ${IMAGE_NAME} -p 8000:8000 ${ECR_REPO}:${IMAGE_TAG}"] \
                    --region "$AWS_REGION" \
                    --query "Command.CommandId" --output text)

                    aws ssm wait command-executed \
                    --command-id "$COMMAND_ID" \
                    --instance-id "$PROD_INSTANCE_ID" \
                    --region "$AWS_REGION"

                    aws ssm get-command-invocation \
                    --command-id "$COMMAND_ID" \
                    --instance-id "$PROD_INSTANCE_ID" \
                    --region "$AWS_REGION"
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                docker rmi ${ECR_REPO}:${IMAGE_TAG} || true
                docker rmi ${ECR_REPO}:latest || true
            '''
        }
        success {
            echo '✅ Pipeline completo: build, tests, push a ECR y deploy a producción exitosos'
        }
        failure {
            echo '❌ El pipeline ha fallado'
        }
    }
}