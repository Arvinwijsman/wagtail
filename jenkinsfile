node {
   stage('Preparation') {
        git branch: 'develop', url: 'https://github.com/Arvinwijsman/wagtail.git'
        sh label: 'Setup wagtail environment', returnStdout: true, script: '''
        #!/bin/bash
        export WORKSPACE=`pwd`
        rm -rf /env
        /usr/local/bin/python3.7 -m virtualenv env
        env/bin/pip install --upgrade setuptools
        env/bin/pip install -e .[\'testing\']
        '''                 
   }
   stage('Tests') {
        sh label: 'Unit tests', returnStdout: true, script: 'env/bin/pytest -sv wagtail/asv_tests/unit'
   }
}
