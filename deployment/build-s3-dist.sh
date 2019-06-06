#!/bin/bash

# Check to see if input has been provided:
if [ -z "$4" ]; then
    printf "Please provide the base source bucket name where the lambda code will eventually reside and version number"
    printf "For example: ./build-s3-dist.sh solutions solutions-reference v1.0 telecom"
    exit 1
fi

# Build source
printf "Starting to build distribution"
printf "export deployment_dir=`pwd`"
export deployment_dir=`pwd`

printf "mkdir -p dist\n"
mkdir -p dist

# CloudFormation template creation
printf "cp -f *.template dist"
cp -f *.template dist

solution_name="machine-learning-for-all"
# industries - healthcare/telecom
industry="$4"

#Replacing BUCKET NAME and VERSION
for replace in "s/%%DIST_BUCKET_NAME%%/$1/g" "s/%%VERSION%%/$3/g" "s/%%INDUSTRY%%/${industry}/g" "s/%%SOLUTION_NAME%%/${solution_name}/g"; do
    printf "sed -i '' -e $replace dist/machine-learning-for-all.template\n"
    sed -i '' -e "${replace}" dist/machine-learning-for-all.template
done

# Copying source/industry ,ml-custom-resource
for dir in industry ml-custom-resource ; do
    printf "cp -r ../source/${dir} dist\n"
    cp -r ../source/"${dir}" dist
done

for replace in "s/%%VERSION%%/$3/g"; do
    FILES="dist/industry/${industry}/notebooks/"
    for filename in "${FILES}"*; do
        printf "sed -i '' -e $replace ${filename}\n"
        sed -i '' -e "${replace}" ${filename}
    done
done

printf 'cd ../source/ml-custom-resource/ && pip3 install -r ./requirements.txt -t .'
cd ../source/ml-custom-resource/ && pip3 install -r ./requirements.txt -t .

printf 'zip -r9 ml-custom-resource.zip *'
zip -r9 ml-custom-resource.zip *

printf 'mv ml-custom-resource.zip $deployment_dir/dist'
mv ml-custom-resource.zip $deployment_dir/dist



