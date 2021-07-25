#!/bin/sh

#checking arguments
if [ "$1" != v1 ]; then
	echo "Expected first argument (version string) 'v1', got '$1'."
	exit 1
fi

echo "Installing INNVerS"

#installing tool
apt update &&
apt install -y python3 python3-pip && #Python 3.7 or higher
#apt install -y psmisc && #for killall, used in prepare_instance.sh
pip3 install numpy && #Numpy
pip3 install ortools && #Google OR-Tools for MILP optimization
pip3 install protobuf-compiler && #prerequisite for ONNX
pip3 install onnx==1.8.1 && #ONNX for .onnx file processing
pip3 install z3-solver #z3 Theorem Prover for .vnnlib file processing
