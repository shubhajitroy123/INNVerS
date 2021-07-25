This directory contains the files necessary to test the INNVerS scripts using the run_in_docker.sh script provided by vnncomp-2021. To run the script, docker must be installed as a prerequisite. Check their [website](https://www.docker.com/) for details on how to install and get docker running. To run the script, type the following command in terminal:

```shell
chmod u+x run_in_docker.sh
./run_in_docker.sh
```

By default, it runs the "test" category benchmarks. To run the "acasxu" category benchmarks, type the command:

```shell
./run_in_docker.sh acasxu
```

An output file out.csv should be produced, which will store the results for the docker tests.
