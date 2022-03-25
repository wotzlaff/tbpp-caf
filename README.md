# Combinatorial Arcflow Model for the Temporal Bin Packing Problem with Fire-Ups

This repository contains compact models for the Temporal Bin Packing Problem with Fire-Ups.
The problem was introduced in [[1]](#1).
Some improvements for the compact models were proposed in [[2]](#2), [[3]](#3), [[4]](#4).

The method in this repository implements the model of a combinatorial flow-based formulation. A description of the details will be published soon [[5]](#5).

## Examples

Results for the benchmark instances can be computed using the script `solve_benchmarks.py` specifying a subset of instances (`a1`, `a2`, `b1`, `b2`) and a problem setting (`without_fu` or `with_fu`).

## Installation

The file `environment.yml` contains a description of all required packages.
You can create a clean Anaconda environment from this file using

```
conda env create
```

and activate it using

```
conda activate grb
```

Afterwards, use

```
python -m pip install -e .
```

to setup a link to the `tbpp_caf` package such that it can be loaded easily.

## Data of Benchmark Instances

The data for the benchmark instances can be found [here](https://github.com/sibirbil/TemporalBinPacking).
After cloning this repository move the instance directory to `data/set1` or create a symbolic link.

## References

<a id="1">[1]</a>
Aydın, N., Muter, İ., & Birbil, Ş. İ. (2020). Multi-objective temporal bin packing problem: An application in cloud computing. Computers & Operations Research, 121, 104959. <https://doi.org/10.1016/j.cor.2020.104959>

<a id="2">[2]</a>
Martinovic, J., Strasdat, N., & Selch, M. (2021). Compact integer linear programming formulations for the temporal bin packing problem with fire-ups. Computers & Operations Research, 105288. <https://doi.org/10.1016/j.cor.2021.105288>

<a id="3">[3]</a>
Martinovic, J., Strasdat, N., Valério de Carvalho, J., & Furini, F. (2021). Variable and constraint reduction techniques for the temporal bin packing problem with fire-ups. Optimization Letters, 1-26. <https://doi.org/10.1007/s11590-021-01825-x>

<a id="4">[4]</a>
Martinovic, J. & Strasdat, N. (2022). Theoretical Insights and a New Class of Valid Inequalities for the Temporal Bin Packing Problem with Fire-Ups. Preprint MATH-NM-01-2022 (available online: <http://www.optimization-online.org/DB_HTML/2022/02/8791.html>)

<a id="5">[5]</a>
Martinovic, J., Strasdat, N., Valério de Carvalho, J., & Furini, F. (2022). A Combinatorial Flow-based Formulation for Temporal Bin Packing Problems. TBP