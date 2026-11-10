pipeline {
    agent any

    environment {
        PYTHON = 'python'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }

        stage('Prepare Environment') {
            steps {
                bat 'python --version'
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install pytest selenium'
            }
        }

        stage('Run UI Tests') {
            steps {
                bat 'python -m pytest lab10/test_ui.py -v'
            }
        }

        stage('Artifacts') {
            steps {
                archiveArtifacts artifacts: 'lab10/index.html, lab10/test_ui.py', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo '====================================================='
            echo '[SUCCESS] Jenkins CI Pipeline completed successfully!'
            echo 'All Lab 10 UI tests passed without errors.'
            echo '====================================================='
        }
        failure {
            echo '====================================================='
            echo '[FAILURE] Jenkins CI Pipeline failed.'
            echo '====================================================='
        }
    }
}
