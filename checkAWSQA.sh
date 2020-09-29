#!/bin/bash

if python3 remote_checker.py
then
echo "AWSQA environment is good"
else
echo "AWSQA environment is NOT good"
fi
