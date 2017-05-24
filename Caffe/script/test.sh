#!/bin/bash
LOG=log/test-`date +%Y-%m-%d-%H-%M-%S`.log
CAFFE=/media/silverlining/FAF2924BF2920BCF/TT100K/code/caffe/build/tools/caffe
$CAFFE test --model=../model/model.prototxt --weights=../model/snapshots/TT100K_iter_50000.caffemodel --gpu=0  2>&1 | tee $LOG
