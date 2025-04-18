#!/bin/bash
NOW=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_DIR="logs/execucoes_oraculo"
mkdir -p $LOG_DIR
PYTHONPATH=. python omega_executor/oraculo_executor.py | tee "$LOG_DIR/exec_$NOW.log"
