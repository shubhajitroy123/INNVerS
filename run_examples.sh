#runs examples as a sanity check for the tool

#!/bin/sh

#sudo apt install git
#git clone https://github.com/iacs-csu-2020/INNVerS.git
#cd INNVerS

cd vnncomp_scripts
sudo chmod u+x install_tool.sh
sudo chmod u+x prepare_instance.sh
sudo chmod u+x run_instance.sh

./install_tool.sh v1

mkdir ../results

./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib ../results/result_acasxu_1_1.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib ../results/result_acasxu_1_2.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_1_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib ../results/result_acasxu_1_3.txt 60

./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib ../results/result_acasxu_2_1.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib ../results/result_acasxu_2_2.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_2_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib ../results/result_acasxu_2_3.txt 60

./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_1.vnnlib ../results/result_acasxu_3_1.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_2.vnnlib ../results/result_acasxu_3_2.txt 60
./prepare_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib
./run_instance.sh v1 acasxu ../examples/acasxu/ACASXU_run2a_1_3_batch_2000.onnx ../examples/acasxu/prop_3.vnnlib ../results/result_acasxu_3_3.txt 60

clear

echo -n "prop_1 of acasxu_1: "
cat ../results/result_acasxu_1_1.txt
echo " "
echo -n "prop_2 of acasxu_1: "
cat ../results/result_acasxu_1_2.txt
echo " "
echo -n "prop_3 of acasxu_1: "
cat ../results/result_acasxu_1_3.txt
echo " "

echo -n "prop_1 of acasxu_2: "
cat ../results/result_acasxu_2_1.txt
echo " "
echo -n "prop_2 of acasxu_2: "
cat ../results/result_acasxu_2_2.txt
echo " "
echo -n "prop_3 of acasxu_2: "
cat ../results/result_acasxu_2_3.txt
echo " "

echo -n "prop_1 of acasxu_3: "
cat ../results/result_acasxu_3_1.txt
echo " "
echo -n "prop_2 of acasxu_3: "
cat ../results/result_acasxu_3_2.txt
echo " "
echo -n "prop_3 of acasxu_3: "
cat ../results/result_acasxu_3_3.txt
echo " "

rm -rf ../results
