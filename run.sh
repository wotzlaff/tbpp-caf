#!/bin/bash

for set in a1 b1 a2 b2
do
  for method in caf_relax colgen_ip
  do
    for gamma in 0 1
    do
      python examples/solve_benchmarks.py $set $method $gamma
    done
  done
done