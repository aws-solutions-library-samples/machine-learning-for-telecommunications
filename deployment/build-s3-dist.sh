#!/bin/bash
#
# This assumes all of the OS-level configuration has been completed and git repo has already been cloned
#
# This script should be run from the repo's deployment directory
# cd deployment
# ./build-s3-dist.sh source-bucket-base-name trademarked-solution-name version-code
#
# Parameters:
#  - source-bucket-base-name: Name for the S3 bucket location where the template will source the Lambda
#    code from. The template will append '-[region_name]' to this bucket name.
#    For example: ./build-s3-dist.sh solutions my-solution v1.0.0 telecom
#    The template will then expect the source code to be located in the solutions-[region_name] bucket
#
#  - trademarked-solution-name: name of the solution for consistency
#
#  - version-code: version of the package (should follow semver)
#
#  - industry: the industry for the solution. Select 'telecom' for machine-learning-for-telecommunications.
#    Other choices are advertizing|healthcare|telecom

[ "$DEBUG" == 'true' ] && set -x
set -e

# Check to see if input has been provided:
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    echo "Please provide the base source bucket name, trademark approved solution name, version and industry where the lambda code will eventually reside."
    echo "For example: ./build-s3-dist.sh solutions trademarked-solution-name v1.0.0 telecom"
    exit 1
fi

# Get reference for all important folders
template_dir="$PWD"
template_dist_dir="$template_dir/global-s3-assets"
build_dist_dir="$template_dir/regional-s3-assets"
source_dir="$template_dir/../source"

echo "------------------------------------------------------------------------------"
echo "Rebuild distribution"
echo "------------------------------------------------------------------------------"
rm -rf $template_dist_dir
mkdir -p $template_dist_dir
rm -rf $build_dist_dir
mkdir -p $build_dist_dir

echo "------------------------------------------------------------------------------"
echo "Grab passed in parameters"
echo "------------------------------------------------------------------------------"
bucket_name="$1"
solution_name="$2"
version="$3"
industry="$4"

echo "------------------------------------------------------------------------------"
echo "Packaging Global Assets: CloudFormation Template"
echo "------------------------------------------------------------------------------"
printf "cp $template_dir/${solution_name}.template $template_dist_dir/${solution_name}.template\n"
cp $template_dir/${solution_name}.template $template_dist_dir/${solution_name}.template

# Replacing bucket name, solution name, version and industry in template
for replace in "s/%%BUCKET_NAME%%/${bucket_name}/g" \
        "s/%%SOLUTION_NAME%%/${solution_name}/g" \
        "s/%%VERSION%%/${version}/g" \
        "s/%%INDUSTRY%%/${industry}/g"; do
    printf "sed -i -e $replace ${template_dist_dir}/${solution_name}.template\n"
    sed -i -e "${replace}" ${template_dist_dir}/${solution_name}.template
done

echo "------------------------------------------------------------------------------"
echo "Packaging Region Assets: Source"
echo "------------------------------------------------------------------------------"
# Copying source/industry, and source/ml-custom-resource to build distribution directory
for dir in industry ml-custom-resource ; do
    printf "cp -r ../source/${dir} ${build_dist_dir}\n"
    cp -r ../source/${dir} ${build_dist_dir}
done

# Replacing version in notebooks
for replace in "s/%%VERSION%%/${version}/g"; do
    FILES="${build_dist_dir}/industry/${industry}/notebooks/"
    for filename in "${FILES}"*; do
        printf "sed -i -e $replace ${filename}\n"
        sed -i -e "${replace}" ${filename}
    done
done

printf 'cd ../source/ml-custom-resource/ && pip3 install -r ./requirements.txt -t .\n'
cd ../source/ml-custom-resource/ && pip3 install -r ./requirements.txt -t .

printf 'zip -r9 ml-custom-resource.zip *\n'
zip -r9 ml-custom-resource.zip *

echo 'mv ml-custom-resource.zip ${build_dist_dir}'
mv ml-custom-resource.zip ${build_dist_dir}

echo "------------------------------------------------------------------------------"
echo "[Packing] Solution Helper"
echo "------------------------------------------------------------------------------"
PY_PKG="local-solution-helper"
echo "------ Building local-solution-helper zip file"
echo "Building $PY_PKG zip file"
cd $build_dist_dir
# Build python resources using a virtual environment for containing all dependencies
echo "virtualenv --python $(which python3) env"
virtualenv --python $(which python3) $build_dist_dir/env/
echo "source env/bin/activate"
source env/bin/activate
echo "pip install $source_dir/$PY_PKG/. --target=$build_dist_dir/env/lib/python3.7/site-packages/ --upgrade --upgrade-strategy only-if-needed"
pip install $source_dir/$PY_PKG/.  --target=$build_dist_dir/env/lib/python3.7/site-packages/ --upgrade --upgrade-strategy only-if-needed
# fail build if pip install fails
instl_status=$?
if [ ${instl_status} != '0' ]; then
    echo "Error occurred in pip install solution helper. pip install Error Code: ${instl_status}"
    exit ${instl_status}
fi
cd $build_dist_dir/env/lib/python3.7/site-packages/
zip -q -r9 $build_dist_dir/$PY_PKG.zip .

cd $template_dir

echo "deactivate virtualenv and clean up build material in env"
deactivate
rm -r $build_dist_dir/env/

echo "------------------------------------------------------------------------------"
echo "S3 Packaging Complete"
echo "------------------------------------------------------------------------------"
