#!/bin/bash

FAILURE=1
SUCCESS=0

# Fail if any command fails
set -e
set -o pipefail

if [ "$1" == "test" ]; then
  echo "---=== TEST CLAUSE OR PLACEHOLDER ===---"
  echo "  Will not actually install anything."
  echo " "
  read -n1 -srp $'Press any key to continue...\n' _
  exit $SUCCESS

else
  echo "ERROR: Bad command or insufficient parameters!"
  echo " "
  exit $FAILURE
fi
