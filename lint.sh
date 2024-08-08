#!/bin/bash

set -e

cd "$(dirname $0)"

ruff --ignore=E501 .
