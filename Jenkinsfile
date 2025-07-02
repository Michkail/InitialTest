pipeline {
  agent any

  environment {
    IMAGE = "orchest-investment"
    TAG = "local"
  }

  stages {
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE:$TAG .'
      }
    }

    stage('Apply to Kubernetes') {
      steps {
        sh 'kubectl apply -f k8s/'
      }
    }

    stage('Restart Deployment') {
      steps {
        sh 'kubectl rollout restart deployment investment-web'
      }
    }
  }
}
