# AI-IoT Assisted Predictive Congestion Control Protocol

This project implements a research-style congestion control protocol that predicts network congestion before packet loss occurs.

## Key Features

- Machine Learning based congestion prediction
- IoT telemetry integration
- Adaptive congestion window control
- Network simulation with real-time metrics
- Research-grade visualization

## Architecture

Prediction Layer
- ML model predicts congestion probability
- Uses RTT trend, packet loss, throughput

Control Layer
- Adjusts TCP congestion window (cwnd)
- Increase / Maintain / Decrease policy

## Metrics Visualized

- Congestion Window (cwnd)
- RTT
- Queue Load
- Throughput
- Sender Rate
- Congestion Probability
- Phase Diagram

## Technologies

Python  
Scikit-Learn  
Matplotlib  
Network Simulation  
