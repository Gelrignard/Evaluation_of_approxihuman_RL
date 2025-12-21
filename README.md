# Evaluation of Using RL Strategies as Approximate Human in Autonomous Racing

Author: Enlin Gu

Course: Independent Study (Fall 2025)

This study implemented and evaluated three Reinforcement Learning strategy in robot racing simulators as approximate human for future studies. The approaches evaluated are: sim-to-sim transfer, direct end-to-end training and reproduction of the TC-Driver paper.

## 1. Experiment 1: TC-Driver Reproduction (on ALL F1TENTH Race Tracks)

Reproduce the paper TC-Drievr on the full suite of F1TENTH benchmark tracks. This paper is introduced a structured SAC strategy and shows generalizability compared to existing methods.

### 1.1 Experiment Results

The success rate of the TC-Driver paper on all F1TENTH tracks are: success on 7 out of 23 tracks. Though the paper highlights generalizability, the result shows that it does not generalize that well. The policy struggles to adapt to track geometries not present in their training and demostartion set.

The recordings of successful tracks are below.

https://github.com/user-attachments/assets/f9509a3e-0195-4181-958b-dcc5d8346d25

### 1.2 Key Failure Analysis:

The primary failure mode is oscillation with low speed. In a condition that the car is at an angle relative to the track centerline, the agent fails to steer effectively and oscillates at low speeds. This shows that the policy lacks the ability to using steering to recover in this condition.

The video below illustrates the agent failing to correct its heading, resulting in the oscillation loop.

https://github.com/user-attachments/assets/edc9d5fb-a75b-4e77-a498-da88256b01a0

## 2. Experiment 2: Sim-to-Sim Transfer 


## 3. Experiment 3: Direct End-to-End training

## 4. Conclusion and Future Prospects


