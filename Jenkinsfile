pipeline{
    agent any
    stages{
        stage("Code"){
            steps{
                git url:"https://github.com/Mohammed-Khubaib/AHP" , branch:"main"
                echo "Code is now cloned from GitHub 😀"
            }    
        }
        stage("Build"){
            steps{
                sh "docker build -t ahp ."
                echo "Build is completed 👍"
            }
        }
        stage("Push"){
            steps{
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker tag ahp:latest ${env.dockerHubUser}/ahp:latest"
                    sh "docker push ${env.dockerHubUser}/ahp:latest"
                    echo "Image is pushed to Docker Hub 😁"
                }
            }
        }
        stage("Deploy"){
            steps{
                sh "docker-compose down && docker-compose up -d"
                echo "Deployment is completed 🤲"
            }
        }
    }
}