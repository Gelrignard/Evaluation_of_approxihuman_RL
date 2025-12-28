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

Youtube Link: 
[https://youtu.be/QI4dagA5XG4](https://youtu.be/QI4dagA5XG4)


| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Track** | Austin | BrandsHatch | IMS | MexicoCity | Sakhir | SaoPaulo | YasMarine |
| **LapTime (s)** | 181 | 153 | 124 | 148 | 192 | 155 | 223 |
| **Mean Velocity (m/s)** | 3.05 | 2.56 | 3.24 | 2.91 | 2.82 | 2.78 | 2.37 |

### 1.2 Key Failure Analysis:

The primary failure mode is oscillation with low speed.

In a condition that the car is at an angle relative to the track centerline, the agent fails to steer effectively and oscillates at low speeds. Instead, the steering output fluctuates rapidly between left/right limits, causing the vehicle to stall.

This shows that the policy lacks the ability to using steering to recover in this condition.

The video below illustrates the agent failing to correct its heading, resulting in the oscillation loop:

https://github.com/user-attachments/assets/edc9d5fb-a75b-4e77-a498-da88256b01a0

Youtube Link: 
[https://youtu.be/1RZKaoyIHcE](https://youtu.be/1RZKaoyIHcE)

## 2. Experiment 2: Sim-to-Sim Transfer 

### 2.1 Train PPO in F1TENTH

The trained policy is an end-to-end PPO in F1TENTH using stable-baseline 3 for two days. The agent converged to a smooth, collision-free policy on the source track (though a bit slow).

https://github.com/user-attachments/assets/cb88c2c9-e6d3-4675-95f4-64f63d28e35e

Youtube Link: 
[https://youtu.be/7TR5dYTiEbI](https://youtu.be/7TR5dYTiEbI)

### 2.2 Direct Migration

Pre-Alignment: Without precise action scaling, the agent exhibited drastic, high-frequency steering oscillations immediately upon initialization.

https://github.com/user-attachments/assets/ea1fbe72-4025-4c83-a375-a1bc11965fd2

To enable transfer, the physical parameters, observation (LIDAR, Pos, state, etc.) and action spaces (throttle, steering) of the target simulator were manually aligned to match the source training environment.

Youtube Link: 
[https://youtu.be/-Bidc7pVoOM](https://youtu.be/-Bidc7pVoOM)

### 2.3 Migration After Alignment

Post-Alignment: Even after aligning the observation vectors and action scalars, the policy failed to generalize.

https://github.com/user-attachments/assets/00bb4832-31a0-4385-825b-e710dacc4f69

Youtube Link: 
[https://youtu.be/j6FQdK1cLrM](https://youtu.be/j6FQdK1cLrM)

The potential reasons are:
* The internal physics engines differ significantly (e.g., friction coefficients, tire slip models).
* The PPO policy overfitted to the specific dynamics of the F1TENTH Gym.

## 3. Experiment 3: Direct End-to-End training

### 3.1 Methodology Details
Training was conducted using an end-to-end PPO implementation directly in the rendered environment. Through some unsuccessful intermediate training runtimes, the current reward function is training with progress and can avoid "Zero-Throttle Convergence" problem (where the agent learns to stand still to avoid collision penalties) through:
* Smaller penalty on collision
* Modify the reset: start with throttle
* A reward for accumulated distance covered and speed (moving forward)
* Tracking the central line

The latest runtime is run for less than a week (10M steps) 

### 3.2 Most-Recent Result
This training did not converge to a smooth driving policy.

https://github.com/user-attachments/assets/aeb527b2-4fdc-46f7-a43e-9b6c83bb5600

Youtube Link: 
[https://youtu.be/KQ0D8JEPjgc](https://youtu.be/KQ0D8JEPjgc)

The agent developed a "Pulsing" control strategy. It outputs throttle in short bursts (approx. 2 Hz frequency) and random steering when no throttle. While this strategy avoids high-speed crashes, it fails to complete a lap efficiently. The agent need more timesteps to learn for better racing strategy.

## 4. Conclusion and Future Prospects
### 4.1 Key Results
1. TCDriver Reproduction: Achieved a 30% success rate (7/23 tracks). Though this method depicts better generalizability than other methods, it still  failed to validate "zero-shot generalization" and identified overfitting issues in the original baseline.

2. Sim-to-Sim Transfer: The policy transfer from high speed gym to high-fidelity rendered simulators proved infeasible due to simulation gaps.

3. End-to-End Visual Training: Direct training in rendered simulators is currently bottlenecked by simulation speed (real-time training), preventing convergence within feasible timeframes.

### 4.2 Proposed Improvements
Based on the limitations identified above, my future research should move away from pure end-to-end RL and focus on *structured learning paradigms* (like TC-Driver) for faster training.

Besides, from car motion during trainning, we can notice a significant difference from PPO learning (initializing from initial state randomly) and human learning (from sense to actual input). My future work should focus on human study and building learning algotithm structure that better mimic human learning patterns in car racing.







