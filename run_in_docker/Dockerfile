FROM ubuntu:18.04

RUN echo "Starting..."
RUN apt-get update && apt-get install -y bc git # bc is used in vnncomp measurement scripts

# install tool from git repo

ARG TOOL_NAME=INNVerS
ARG REPO=https://github.com/iacs-csu-2020/INNVerS.git 
ARG SCRIPTS_DIR=vnncomp_scripts

RUN git clone $REPO
RUN cd $TOOL_NAME && cd ..
RUN chmod u+x /$TOOL_NAME/$SCRIPTS_DIR/prepare_instance.sh
RUN chmod u+x /$TOOL_NAME/$SCRIPTS_DIR/run_instance.sh

# install dependencies

RUN apt-get update && apt-get install -y software-properties-common gcc && add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.7 python3-distutils python3-pip python3-apt
RUN pip3 install numpy ortools protobuf-compiler z3-solver
RUN pip3 install onnx==1.8.1

# run vnncomp

COPY . /vnncomp2021

# run all categories to produce out.csv

ARG CATEGORIES="test"
RUN chmod u+x vnncomp2021/run_all_categories.sh
RUN vnncomp2021/run_all_categories.sh v1 /$TOOL_NAME/$SCRIPTS_DIR vnncomp2021 out.csv "$CATEGORIES"
