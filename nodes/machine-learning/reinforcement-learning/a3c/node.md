---
tag: VZH9DA
kind: algorithm
slug: a3c
name: Asynchronous advantage actor-critic
aliases:
- A3C
area: machine-learning/reinforcement-learning
level: advanced
summary: "Parallel actor-learners, each with its own environment, compute n-step advantage actor-critic gradients from a copy of shared parameters and add them back without locks."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of environment steps of all workers, W: the cost of one evaluation of the actor and the critic with their gradients, N: the number of workers, n: the maximum segment length t_max, d: the number of parameters}
  time: {worst: "O(T W)"}
  space: {extra: "O(N (n + d))"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2016
  people: [Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy P. Lillicrap, Tim Harley, David Silver, Koray Kavukcuoglu]
  note: "Mnih et al. trained Atari agents with 16 CPU threads in about half the time that DQN needed on a GPU, without experience replay, by running asynchronous actor-learners in parallel."
prereqs: [a2c, stochastic-gradient-descent]
see_also: [actor-critic, dqn, n-step-td, v-trace, generalized-advantage-estimation, experience-replay, ppo, advantage-function]
sources:
  - paper: "Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy P. Lillicrap, Tim Harley, David Silver and Koray Kavukcuoglu, Asynchronous methods for deep reinforcement learning, Proceedings of the 33rd International Conference on Machine Learning, PMLR 48, 2016, pages 1928 to 1937, arXiv:1602.01783"
    locator: Section 4 (the asynchronous framework and A3C), the supplementary pseudocode of the A3C actor-learner thread, the shared RMSProp, and the Atari, MuJoCo and Labyrinth experiments
  - paper: "Feng Niu, Benjamin Recht, Christopher Re and Stephen J. Wright, Hogwild!, a lock-free approach to parallelizing stochastic gradient descent, Advances in Neural Information Processing Systems 24, 2011, pages 693 to 701, arXiv:1106.5730"
    locator: the lock-free update scheme and its convergence analysis for sparse problems
  - url: https://openai.com/index/openai-baselines-acktr-a2c/
    title: "OpenAI, OpenAI Baselines: ACKTR and A2C, blog post, August 2017"
    locator: the report that the synchronous version A2C performs as well as A3C
  - paper: "Lasse Espeholt, Hubert Soyer, Remi Munos, Karen Simonyan, Volodymyr Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, Shane Legg and Koray Kavukcuoglu, IMPALA, scalable distributed deep-RL with importance weighted actor-learner architectures, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, pages 1407 to 1416, arXiv:1802.01561"
    locator: the comparison with A3C and the V-trace correction for the lag between actors and learner
---

Asynchronous advantage actor-critic (A3C) runs several actor-learners in parallel, usually as CPU threads. Each worker has its own copy of the environment. In a loop, it copies the shared parameters $\theta$ and $w$, runs its copy of the policy for up to $t_{\max}$ steps or to the end of the episode, computes $n$-step returns and advantage actor-critic gradients for that segment, and adds the gradients to the shared parameters without a lock, in the "Hogwild" style of Niu et al. (2011). Because other workers write in between, a gradient can be *stale*: it was computed at older parameters than the ones it is added to. The workers explore different parts of the environment at the same time, which decorrelates the updates, so A3C needs no [experience replay](/experience-replay/). Mnih et al. (2016) introduced it, and it beat [DQN](/dqn/) on Atari while training on one multi-core CPU. The synchronous version [A2C](/a2c/), which waits for all workers, later turned out to do as well.

## In plain words

Many players learn the same game together, each on their own board. They share one notebook of advice. Each player copies the advice, plays a few moves, works out which moves went better or worse than expected, and writes corrections into the shared notebook. Nobody waits for anyone else, and nobody locks the notebook. So a player sometimes writes a correction that is based on an older version of the advice, because others wrote in the meantime. That small delay does little harm when the corrections are small, and the players see many different situations at once, which makes learning steady without storing old games.

## The problem

The setting is [reinforcement learning control](/rl-control/) with a simulator that can run many independent copies of an MDP, and a machine with many cores that share memory. The aim is to learn a stochastic policy $\pi_\theta$ and a value function $V_w$ with the n-step advantage actor-critic, using all cores, without a GPU and without a replay memory.

## The algorithm

Every worker runs the loop below on the same shared $\theta$ and $w$, with its own environment, its own step counter $t$ and its own local copies $\theta'$, $w'$. Notation: $\eta$ is the step size, $\beta$ the entropy weight, $c$ the weight of the critic, $H$ the entropy, and $T_{\max}$ the total budget of steps of all workers.

```pseudo id=main
A3C-WORKER(shared θ, w; t_max, γ, η, β, c)
L1  repeat
L2      θ′ ← θ; w′ ← w                                 ▷ read the shared parameters, no lock
L3      dθ ← 0; dw ← 0; t_start ← t
L4      repeat A_t ~ π_θ′(· | S_t); observe R_{t+1}, S_{t+1}; t ← t + 1 until the episode ends or t − t_start = t_max
L5      G ← 0 if the episode ended, else V_w′(S_t)
L6      for i ← t − 1 down to t_start: G ← R_{i+1} + γ G
L7          dθ ← dθ + (G − V_w′(S_i)) ∇ log π_θ′(A_i | S_i) + β ∇ H(π_θ′(· | S_i))
L8          dw ← dw + (G − V_w′(S_i)) ∇ V_w′(S_i)
L9      θ ← θ + η dθ; w ← w + η c dw                    ▷ write to the shared parameters, no lock
L10 until the shared step counter exceeds T_max
```

Line L2 takes a snapshot of the shared parameters. Lines L4 to L8 are the [n-step advantage actor-critic](/a2c/) on one segment, computed with the snapshot only: the step $t - 1$ gets a one-step return, the step $t_{\text{start}}$ a return of up to $t_{\max}$ steps, and the return is 0 after the end of an episode. If the episode ended, the next segment starts a new one. Line L9 adds the summed gradient to the shared parameters. Between lines L2 and L9 of one worker, the other workers can execute their line L9 any number of times, so the gradient is applied to parameters that may differ from $\theta'$. Mnih et al. used $t_{\max} = 5$, $\beta = 0.01$, 16 threads, and RMSProp whose squared-gradient statistics are shared between the threads.

**Simulating the asynchrony.** The implementation below runs the workers in one process and takes a *schedule*, a sequence of worker indices. The first time a worker appears it executes lines L2 to L8, the next time line L9. The schedule $0, 0, 1, 1, 2, 2, \ldots$ gives zero delay; the schedule $0, 1, 2, 0, 1, 2$ makes all three gradients of a round stale.

## Example

Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page with $\gamma = \tfrac12$ and the start state 0.

**One segment.** With $\theta' = 0$ (uniform policy), $w' = 0$, $\beta = 0$, suppose a worker sees state 0, action 0, reward 1, then state 1, action 1, reward 3, and the episode ends. Line L5 sets $G = 0$; line L6 gives $G = 3$ and then $G = 1 + \tfrac12 \cdot 3 = \tfrac52$. The summed gradients are $d\theta_0 = \tfrac52 (\tfrac12, -\tfrac12) = (\tfrac54, -\tfrac54)$, $d\theta_1 = 3 (-\tfrac12, \tfrac12) = (-\tfrac32, \tfrac32)$ and $dw = (\tfrac52, 3)$. Unlike [REINFORCE](/reinforce/), there is no factor $\gamma^t$ on the second step.

**Three schedules.** Let $g(\theta, \sigma)$ be the update of lines L3 to L8 for the segment $\sigma$ at parameters $\theta$, and $\theta_0$ the shared parameters at the start.

| schedule | shared parameters after the writes |
|---|---|
| $0, 0, 1, 1$ (zero delay) | $\theta_2 = \theta_1 + \eta g(\theta_1, \sigma_1)$ with $\theta_1 = \theta_0 + \eta g(\theta_0, \sigma_0)$ |
| $0, 1, 0, 1$ (both stale) | $\theta_0 + \eta g(\theta_0, \sigma_0) + \eta g(\theta_0, \sigma_1)$ |
| $0, 1, 1, 1, 1, 0$ (worker 0 two writes behind) | $\theta'' + \eta g(\theta_0, \sigma_0)$ with $\theta' = \theta_0 + \eta g(\theta_0, \sigma_1)$ and $\theta'' = \theta' + \eta g(\theta', \sigma_2)$ |

Zero delay is a sequence of single-copy [A2C](/a2c/) steps. A round in which all workers read before any writes is one synchronous A2C step on the union of the segments. With random interleavings of 4 workers, $t_{\max} = 5$, $\eta = 0.1$ and $\beta = 0.01$, the implementation reaches $\pi(0 \mid 0) > 0.99$ and $\pi(1 \mid 1) > 0.99$ after 600 segments (seed 3), the optimal policy.

## Correctness

A3C has no convergence guarantee with nonlinear networks, and none is claimed. The proved facts are about the update rule; see the correctness proof.

1. **Each worker computes an A2C gradient.** Given its snapshot $(\theta', w')$ and its segment, lines L3 to L8 compute the summed n-step advantage actor-critic gradient, so with an exact critic the n-step targets are unbiased estimates of $Q^{\pi_{\theta'}}$ (the [A2C](/a2c/) analysis).
2. **Zero delay is sequential A2C.** If every worker writes before the next worker reads, then each write uses the current shared parameters, and A3C is a sequence of single-segment A2C steps.
3. **A fully stale round is one batched A2C step.** If all workers read the same parameters before any of them writes, then the result is $\theta_0 + \eta \sum_i g(\theta_0, \sigma_i)$, one synchronous step on the batch of all segments. Additions commute, so the order of the writes does not matter.
4. **Staleness is a small perturbation.** If the expected update is $L$-Lipschitz in the parameters, each write is at most $\tau$ writes behind its read, and every write has norm at most $\eta M$, then the expected stale update differs from the expected fresh update by at most $L \tau \eta M$. For small steps, A3C is a gradient method with a perturbation of order $\eta$.

Hogwild's convergence theorem (Niu et al., 2011) needs sparse gradients that rarely touch the same coordinates, which a dense network does not have; A3C relies on small steps and on experiment, not on that theorem.

## Complexity

Each environment step costs one forward pass of the actor and the critic, and each segment step one backward pass in lines L7 and L8, so $T$ steps of all workers cost $O(T W)$ arithmetic in the worst case. A read or a write of the shared parameters costs $O(d)$ once per segment, which is at most $O(t_{\max} W)$. Each of the $N$ workers stores a segment of up to $t_{\max}$ steps and its own copy of the parameters: $O(N(t_{\max} + d))$ memory. The wall-clock time is about $T W / N$ on $N$ cores, since the workers never wait for each other.

## Properties

- **On-policy, up to staleness.** Each segment comes from the worker's snapshot, which is slightly older than the shared parameters when its gradient is applied.
- **No replay memory.** Parallel workers in different states give decorrelated updates.
- **Nondeterministic.** With real threads, the interleaving depends on timing, so two runs with the same seed differ. A2C removes this.
- **Lock-free.** Workers never wait, so cores are used fully; with real hardware, races can even lose parts of a write, which the method tolerates.
- **Randomized.** Action selection, the environments and the interleaving are random.

## Variants and improvements

- **Synchronous A2C.** Wait for all workers and average their gradients ([A2C](/a2c/)); this is deterministic and uses a GPU well.
- **Other asynchronous learners.** The same paper gives asynchronous one-step Q-learning, one-step Sarsa and n-step Q-learning; A3C was the best of them.
- **GA3C.** A GPU version that queues the requests of many CPU workers into batches.
- **IMPALA.** Decouples acting from learning: many actors send trajectories to one learner, and [V-trace](/v-trace/) corrects for the policy lag (Espeholt et al., 2018).
- **Better advantages.** [Generalized advantage estimation](/generalized-advantage-estimation/) replaces the plain n-step advantage.

## When to use it

A3C fits a machine with many CPU cores, no GPU, and a cheap simulator. On a GPU, or when reproducibility matters, use [A2C](/a2c/) or [PPO](/ppo/). For large distributed setups with many actors, IMPALA-style architectures with off-policy corrections scale better. With expensive samples, off-policy methods with replay ([DQN](/dqn/), [soft actor-critic](/soft-actor-critic/)) use the data better.

## Pitfalls

- **Too many workers or too large a step.** The staleness grows with the number of workers, and so does the perturbation in item 4 of Correctness. Scale the step size down when adding workers.
- **Per-thread optimizer statistics.** Mnih et al. found that RMSProp with statistics shared across threads is more robust than separate statistics.
- **Correlated workers.** Workers with the same seed or the same start explore the same states; seed and start them differently.
- **The end of an episode.** Line L5 must bootstrap from 0 only at a real end, not at a time limit.
- **Reading torn parameters.** With real threads, a read can mix values from before and after another worker's write. This is part of the design, but it makes bugs hard to reproduce; debug with a fixed schedule, as in the implementation below.

## Implementations

## History

Niu, Recht, Re and Wright (2011) showed that stochastic gradient descent can run on many cores that update shared memory without locks, and still converge when the gradients are sparse. Mnih et al. (2016) applied this lock-free scheme to reinforcement learning: asynchronous one-step and n-step Q-learning, Sarsa, and the asynchronous advantage actor-critic. Running different workers in different parts of the environment replaced the experience replay of [DQN](/dqn/), and A3C set new results on Atari with 16 CPU threads, and also learned continuous control and navigation in 3D mazes. In 2017, OpenAI and others reported that the synchronous version, [A2C](/a2c/), does as well, and later systems such as IMPALA kept the parallel actors but added off-policy corrections.

## References
