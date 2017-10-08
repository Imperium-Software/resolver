#!/bin/bash

electron SATSolver/interface > SATSolver/interface/log & 
python3 SATSolver/main.py
