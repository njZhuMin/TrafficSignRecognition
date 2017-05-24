#!/usr/bin/env sh
set -e

./build/tools/caffe.bin test --model=examples/mnist/lenet_train_test.prototxt --weights=examples/mnist/lenet_iter_10000.caffemodel -gpu 0 $@
