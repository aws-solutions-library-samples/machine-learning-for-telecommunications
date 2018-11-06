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

ACTIVITIES_PARQ_FILE="<%ActivitiesFile%>"
IMPRESSIONS_PARQ_FILE="<%ImpressionsFile%>"
Sagedir=/home/ec2-user/SageMaker
industry=advertising

download_files(){
    wget https://"${s3region}"/"${SRC_NOTEBOOK_DIR}"/Ml_Workflow_for_advertising_SageMaker.ipynb -P ${Sagedir}/${industry}
    wget https://"${s3region}"/"${SRC_NOTEBOOK_DIR}"/Ml_Workflow_for_advertising_SiteID_Sagemaker.ipynb -P ${Sagedir}/${industry}
}
replace_param(){
        cd ${Sagedir}
        ACT_PRQ=$(echo ${DESTINATION_DATA_DIR}/activity|sed 's#/#\\/#g')
        IMP_PRQ=$(echo ${DESTINATION_DATA_DIR}/impressions|sed 's#/#\\/#g')
        sed -i "s/${ACTIVITIES_PARQ_FILE}/${ACT_PRQ}/g" ${industry}/Ml_Workflow_for_advertising_SageMaker.ipynb
        sed -i "s/${IMPRESSIONS_PARQ_FILE}/${IMP_PRQ}/g" ${industry}/Ml_Workflow_for_advertising_SageMaker.ipynb
        sed -i "s/${ACTIVITIES_PARQ_FILE}/${ACT_PRQ}/g" ${industry}/Ml_Workflow_for_advertising_SiteID_Sagemaker.ipynb
        sed -i "s/${IMPRESSIONS_PARQ_FILE}/${IMP_PRQ}/g" ${industry}/Ml_Workflow_for_advertising_SiteID_Sagemaker.ipynb
}

extract_data(){
        aws s3 cp s3://${SRC_DATA_DIR}/activity/generated_activities.csv.gz /tmp/
        aws s3 cp s3://${SRC_DATA_DIR}/impressions/generated_impressions.csv.gz /tmp/
        #wget https://${s3region}/${SRC_DATA_DIR}/activity/generated_activities.csv.gz -P /tmp/
        #wget https://${s3region}/${SRC_DATA_DIR}/impressions/generated_impressions.csv.gz -P /tmp/
        gunzip -d /tmp/generated_activities.csv.gz
        gunzip -d /tmp/generated_impressions.csv.gz
        aws s3 cp /tmp/generated_activities.csv s3://${SRC_DATA_DIR}/activity/
        aws s3 cp /tmp/generated_impressions.csv s3://${SRC_DATA_DIR}/impressions/
}

clean(){
        aws s3 rm s3://${SRC_DATA_DIR}/activity/generated_activities.csv.gz
        aws s3 rm s3://${SRC_DATA_DIR}/impressions/generated_impressions.csv.gz
        rm -rf /tmp/generated*.csv
}


if [ ${CP_SAMPLES} = true ]; then
    sudo -u ec2-user mkdir -p ${Sagedir}/${industry}
    mkdir -p ${Sagedir}/${industry}
    download_files
    chmod -R 755 ${Sagedir}/advertising
    chown -R ec2-user:ec2-user ${Sagedir}/${industry}/.
    #Replacing placeholders in Notebook
    if [ ${CP_DATA} = true ]; then
        replace_param
    fi
    if [ ${EXTRACT_CSV} = true ];then
        #Extracting synthetic-data gz files
        extract_data
        #Delete gz files
        clean
    fi
fi