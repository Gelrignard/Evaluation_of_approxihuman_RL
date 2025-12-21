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

### 2.1 Train PPO in F1TENTH

The trained policy is an end-to-end PPO in F1TENTH using stable-baseline 3 for a day (approx. 10M steps). The agent converged to a smooth, collision-free policy on the source track (though a bit slow).

https://github.com/user-attachments/assets/cb88c2c9-e6d3-4675-95f4-64f63d28e35e

### 2.2 Direct Migration

Pre-Alignment: Without precise action scaling, the agent exhibited drastic, high-frequency steering oscillations immediately upon initialization.

https://github.com/user-attachments/assets/ea1fbe72-4025-4c83-a375-a1bc11965fd2

To enable transfer, the physical parameters, observation (LIDAR, Pos, state, etc.) and action spaces (throttle, steering) of the target simulator were manually aligned to match the source training environment.

### 2.3 Migration After Alignment

Post-Alignment: Even after aligning the observation vectors and action scalars, the policy failed to generalize.


https://github.com/user-attachments/assets/00bb4832-31a0-4385-825b-e710dacc4f69

The potential reasons are:
* The internal physics engines differ significantly (e.g., friction coefficients, tire slip models).
* The PPO policy overfitted to the specific dynamics of the F1TENTH Gym.

## 3. Experiment 3: Direct End-to-End training




### 3.1 Methodology Details

### 3.2 Most-Recent Result


https://github.com/user-attachments/assets/aeb527b2-4fdc-46f7-a43e-9b6c83bb5600

## 4. Conclusion and Future Prospects
The key result

TCDriver Reproduction: Achieved a 30% success rate (7/23 tracks). Though this method depicts better generalizability than other methods, it still identified overfitting issues in the original baseline, not genralizing well on all conditions.

Sim-to-Sim Transfer: The policy transfer from high speed gym to high-fidelity rendered simulators proved infeasible due to simulation gaps.

End-to-End Visual Training: Direct training in rendered simulators is currently bottlenecked by simulation speed (real-time training), preventing convergence within feasible timeframes.



