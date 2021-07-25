FROM ubuntu:20.04

RUN echo "Starting..."
RUN apt-get update && apt-get install -y bc git # bc is used in vnncomp measurement scripts

# install tool from git repo

ARG TOOL_NAME=INNVerS
ARG REPO=https://github.com/iacs-csu-2020/INNVerS.git 
ARG COMMIT=12ff36a29c925bb58096c106af4b40836b4f68d4
ARG SCRIPTS_DIR=vnncomp_scripts

RUN git clone $REPO
RUN cd $TOOL_NAME && git checkout $COMMIT && cd ..
RUN chmod u+x /$TOOL_NAME/$SCRIPTS_DIR/prepare_instance.sh
RUN chmod u+x /$TOOL_NAME/$SCRIPTS_DIR/run_instance.sh

# install dependencies

FROM python:3.8
RUN pip3 install numpy ortools protobuf-compiler onnx==1.8.1 z3-solver

# run vnncomp

FROM ubuntu:20.04
COPY . /vnncomp2021

# run all categories to produce out.csv

ARG CATEGORIES="test"
RUN chmod u+x vnncomp2021/run_all_categories.sh
RUN vnncomp2021/run_all_categories.sh v1 /$TOOL_NAME/$SCRIPTS_DIR vnncomp2021 out.csv "$CATEGORIES"
