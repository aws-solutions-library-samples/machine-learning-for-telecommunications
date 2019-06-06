#!/bin/bash -xe
# Custom Script to Replace Params in  Notebooks
set -e
CP_SAMPLES=true
CP_DATA=true
EXTRACT_CSV=false
s3region="<%s3region%>"
SRC_NOTEBOOK_DIR="<%SRC_NOTEBOOK_DIR%>"
SRC_DATA_DIR="<%SRC_DATA_DIR%>"
DESTINATION_DATA_DIR="<%DESTINATION_DATA_DIR%>"

CDR_START_PARQ_FILE="<%CDRStartFile%>"
CDR_STOP_PARQ_FILE="<%CDRStopFile%>"
CDR_START_SAMPLE_PARQ_FILE="<%CDRStartSampleFile%>"
CDR_STOP_SAMPLE_PARQ_FILE="<%CDRStopSampleFile%>"
Sagedir=/home/ec2-user/SageMaker
industry=telecom

notebooks=("Ml-Telecom-NaiveBayes.ipynb" "Ml-Telecom-PCA-KMeans.ipynb" "Ml-Telecom-RandomCutForest.ipynb" "Ml-Telecom-RandomForestClassifier.ipynb" "Ml-Telecom-TimeSeries-RandomForestClassifier-DeepAR.ipynb")

download_files(){

    for notebook in "${notebooks[@]}"
        do
          printf "aws s3 cp s3://${SRC_NOTEBOOK_DIR}/${notebook} ${Sagedir}/${industry}\n"
          aws s3 cp s3://"${SRC_NOTEBOOK_DIR}"/"${notebook}" ${Sagedir}/${industry}
        done
}

replace_param(){
        cd ${Sagedir}
        CDR_START_PRQ=$(echo ${DESTINATION_DATA_DIR}/cdr-start|sed 's#/#\\/#g')
        CDR_STOP_PRQ=$(echo ${DESTINATION_DATA_DIR}/cdr-stop|sed 's#/#\\/#g')
        CDR_START_SAMPLE_PRQ=$(echo ${DESTINATION_DATA_DIR}/cdr-start-sample|sed 's#/#\\/#g')
        CDR_STOP_SAMPLE_PRQ=$(echo ${DESTINATION_DATA_DIR}/cdr-stop-sample|sed 's#/#\\/#g')

        for notebook in "${notebooks[@]}"
            do
                sed -i "s/${CDR_START_PARQ_FILE}/${CDR_START_PRQ}/g" ${industry}/"${notebook}"
                sed -i "s/${CDR_STOP_PARQ_FILE}/${CDR_STOP_PRQ}/g" ${industry}/"${notebook}"
                sed -i "s/${CDR_START_SAMPLE_PARQ_FILE}/${CDR_START_SAMPLE_PRQ}/g" ${industry}/"${notebook}"
                sed -i "s/${CDR_STOP_SAMPLE_PARQ_FILE}/${CDR_STOP_SAMPLE_PRQ}/g" ${industry}/"${notebook}"
            done

}

if [ ${CP_SAMPLES} = true ]; then
    sudo -u ec2-user mkdir -p ${Sagedir}/${industry}
    mkdir -p ${Sagedir}/${industry}
    download_files
    chmod -R 755 ${Sagedir}/${industry}
    chown -R ec2-user:ec2-user ${Sagedir}/${industry}/.
        #Replacing placeholders in Notebook
    if [ ${CP_DATA} = true ]; then
        replace_param
    fi
fi