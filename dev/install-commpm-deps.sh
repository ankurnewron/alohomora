#!/usr/bin/env bash

set -ex

function retry-with-backoff() {
    for BACKOFF in 0 1 2; do
        sleep $BACKOFF
        if "$@"; then
            return 0
        fi
    done
    return 1
}

while :
do
  case "$1" in
    # Install skinny dependencies
    --skinny)
      SKINNY="true"
      shift
      ;;
    # Install ML dependencies
    --ml)
      ML="true"
      shift
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Error: unknown option: $1" >&2
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

# Cleanup apt repository to make room for tests.
sudo apt clean
df -h

python --version
pip install --upgrade pip wheel
pip --version

if [[ "$SKINNY" == "true" ]]; then
  MLFLOW_SKINNY=true pip install . --upgrade
else
  pip install .[extras] --upgrade
fi
export MLFLOW_HOME=$(pwd)

req_files=""
# Install Python test dependencies only if we're running Python tests
if [[ "$SKINNY" == "true" ]]; then
  req_files+=" -r requirements/skinny-test-requirements.txt"
else
  req_files+=" -r requirements/test-requirements.txt"
fi
if [[ "$ML" == "true" ]]; then
  req_files+=" -r requirements/extra-ml-requirements.txt"
fi

if [[ ! -z $req_files ]]; then
  retry-with-backoff pip install $req_files
fi

# Install `mlflow-test-plugin` without dependencies
pip install --no-dependencies tests/resources/mlflow-test-plugin
pip install git+https://github.com/djokester/alohomora
# Print current environment info
python dev/show_package_release_dates.py
which mlflow
echo $MLFLOW_HOME

# Print mlflow version
mlflow --version

# Turn off trace output & exit-on-errors
set +ex