#!/bin/bash
LOG=log/train-`date +%Y-%m-%d-%H-%M-%S`.log
CAFFE=/media/silverlining/FAF2924BF2920BCF/TT100K/code/caffe/build/tools/caffe
$CAFFE train --solver=../model/solver.prototxt --gpu=0 2>&1 | tee $LOG
