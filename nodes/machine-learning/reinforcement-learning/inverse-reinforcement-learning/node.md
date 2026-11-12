---
tag: 5XWNRJ
kind: problem
slug: inverse-reinforcement-learning
name: Inverse reinforcement learning
aliases:
- IRL
- inverse optimal control
area: machine-learning/reinforcement-learning
level: advanced
summary: "Find a reward function for which observed expert behavior is optimal or most likely. The answer is never unique: the zero reward explains every policy, so methods add a criterion."
prereqs: [markov-decision-process, reward-function, imitation-learning]
see_also: [maximum-entropy-rl, linear-programming-for-mdps, linear-programming-problem, potential-based-reward-shaping, log-sum-exp-trick, dagger, offline-reinforcement-learning, policy-iteration]
sources:
  - paper: "Andrew Y. Ng and Stuart Russell, Algorithms for inverse reinforcement learning, Proceedings of the 17th International Conference on Machine Learning (ICML), 2000, pages 663 to 670"
    locator: Section 3 (finite state spaces, Theorem 3 on the set of rewards for which a policy is optimal, the degenerate zero reward, and the linear program), Section 4 (linear function approximation), Section 5 (IRL from sampled trajectories)
  - paper: doi:10.1145/1015330.1015430
    title: "Pieter Abbeel and Andrew Y. Ng, Apprenticeship learning via inverse reinforcement learning, Proceedings of the 21st International Conference on Machine Learning (ICML), 2004"
    locator: feature expectations, the max-margin and projection algorithms, and their iteration and sample bounds
  - paper: "Brian D. Ziebart, Andrew Maas, J. Andrew Bagnell and Anind K. Dey, Maximum entropy inverse reinforcement learning, Proceedings of the Twenty-Third AAAI Conference on Artificial Intelligence, 2008, pages 1433 to 1438"
    locator: the maximum entropy distribution over paths, Algorithm 1 (the backward pass and the forward pass for the expected state visitation frequencies), and the gradient as the difference of feature counts
  - paper: doi:10.1145/1143844.1143936
    title: "Nathan D. Ratliff, J. Andrew Bagnell and Martin A. Zinkevich, Maximum margin planning, Proceedings of the 23rd International Conference on Machine Learning (ICML), 2006"
    locator: IRL as structured prediction with a loss-augmented margin
  - paper: "Deepak Ramachandran and Eyal Amir, Bayesian inverse reinforcement learning, Proceedings of the 20th International Joint Conference on Artificial Intelligence (IJCAI), 2007, pages 2586 to 2591"
    locator: a posterior over rewards, sampled by a Markov chain
  - paper: "Rudolf E. Kalman, When is a linear control system optimal?, Journal of Basic Engineering 86(1), 1964, pages 51 to 60"
    locator: the inverse optimal control problem for linear systems with quadratic cost
  - paper: "Haoyang Cao, Samuel N. Cohen and Lukasz Szpruch, Identifiability in inverse reinforcement learning, Advances in Neural Information Processing Systems 34 (NeurIPS 2021), arXiv:2106.03498"
    locator: with entropy regularization, the policy determines the reward up to a potential-based shaping term
---

Inverse reinforcement learning (IRL) turns reinforcement learning around. Reinforcement learning gets a [reward](/reward-function/) and finds a good policy; IRL gets the behavior of an expert in a [Markov decision process](/markov-decision-process/) without a reward and finds a reward that explains it, usually one for which the expert's policy is optimal. The reward is then a compact description of the task: it can be reused in other environments, inspected, or optimized to obtain a policy, which makes IRL one route to [imitation learning](/imitation-learning/). The problem is ill-posed, because many rewards explain the same behavior, including the zero reward, so every method adds a criterion that picks one.

## In plain words

You watch someone act and ask: what are they trying to achieve? If a driver always slows near schools and never takes the toll road, you guess that safety counts a lot and money counts a little. IRL makes this guess precise.

Many guesses explain the same actions. "They want nothing at all" explains every action, because then every action is as good as any other. So IRL methods prefer guesses that make the observed actions clearly better than the others, or that make the observed paths as likely as possible.

## Definition

**Input.** A Markov decision process without its reward, $M \setminus R = (S, A, P, \gamma)$, usually with known dynamics $P$, and the expert's behavior, in one of these forms:

- the expert's policy $\pi_E$, or
- demonstrations: $m$ trajectories of $\pi_E$.

Rewards are often restricted to a class, for example $R(s) = \theta^\top \phi(s)$ for given features $\phi : S \to \mathbb{R}^k$.

**Output.** A reward function $R$.

**Goal.** Either (a) $\pi_E$ is optimal for $R$, or (b) the demonstrations are most likely under a model of near-optimal behavior for $R$, or (c) a policy that is optimal for $R$ does as well as the expert under the true reward. Goal (a) has a precise answer for finite MDPs (Ng and Russell, 2000, Theorem 3). For a state reward $R \in \mathbb{R}^{|S|}$ and a deterministic policy $\pi$ with transition matrix $P_\pi$, $\pi$ is optimal if and only if

$$\big(P_\pi(s) - P_a(s)\big)\,(I - \gamma P_\pi)^{-1} R \;\ge\; 0 \qquad \text{for every state } s \text{ and action } a,$$

where $P_a(s)$ is the row of next-state probabilities of action $a$ in $s$. The left side is $\frac{1}{\gamma}\big(Q^\pi(s, \pi(s)) - Q^\pi(s, a)\big)$. So the set of rewards that explain $\pi$ is a polyhedral cone. It always contains $R = 0$ and every constant reward, which make every policy optimal.

## Variants

- **Policy known or only sampled.** With the full policy, the test above applies directly; with $m$ trajectories, feature expectations $\hat\mu_E = \frac{1}{m}\sum_i \sum_t \gamma^t \phi(s^i_t)$ replace it.
- **Max-margin IRL** (Ng and Russell, 2000): maximize how much better the expert's action is than the second best, with a penalty on $\|R\|_1$. Maximum margin planning (Ratliff, Bagnell and Zinkevich, 2006) treats IRL as [structured prediction](/structured-prediction/).
- **Apprenticeship learning** (Abbeel and Ng, 2004): the goal is a policy, not the reward; find any policy whose feature expectations match the expert's.
- **Maximum entropy IRL** (Ziebart and others, 2008): a probabilistic model of the expert, with paths more likely when their total reward is higher.
- **Bayesian IRL** (Ramachandran and Amir, 2007): a posterior over rewards.
- **Unknown dynamics and deep rewards:** guided cost learning, adversarial IRL and [GAIL](/imitation-learning/) learn with samples instead of a known $P$.
- **Inverse optimal control** for continuous control (Kalman, 1964), where the question is which quadratic costs make a linear feedback law optimal.

## Examples

**Two states.** Let $S = \{1, 2\}$ and two deterministic actions, *stay* and *switch*. The expert switches in state 1 and stays in state 2. Then $V^\pi(2) = R_2/(1-\gamma)$ and $V^\pi(1) = R_1 + \gamma R_2/(1-\gamma)$, and both conditions of the test reduce to $V^\pi(2) - V^\pi(1) = R_2 - R_1 \ge 0$. Every reward with $R_2 \ge R_1$ explains the expert, including $R = 0$. Ng and Russell's linear program maximizes the sum of the margins minus $\lambda\|R\|_1$, with $|R_i| \le 1$: here $2(R_2 - R_1) - \lambda(|R_1| + |R_2|)$. For $0 \le \lambda < 2$ it chooses $R = (-1, 1)$; for $\lambda > 2$ the penalty wins and it chooses $R = 0$.

**Maximum entropy on a grid.** The implementation uses a $3 \times 3$ grid with moves up, down, left, right and stay, start $(0, 0)$, horizon 5, and three features: being at the goal $(2, 2)$, being in water at $(1, 1)$ or $(1, 2)$, and the column divided by 2. With true weights $\theta^* = (2, -1.5, 0.3)$, the expected feature counts over the 5 states of a path are $(0.038, 0.090, 0.955)$; with $\theta = 0$ (a uniform random walk) they are $(0.010, 0.347, 0.819)$. From the exact counts of $\theta^*$, the algorithm below recovers $\theta^*$ to $10^{-6}$. From 300 sampled paths, it returns $\theta = (1.654, -1.541, 0.297)$ and matches the sample's feature counts to $10^{-8}$; the weight of the goal is the least certain, because only 2.7% of the paths reach it in time.

## Known algorithms

- **Linear programming** (Ng and Russell, 2000). Maximize $\sum_s \min_{a \ne \pi(s)} \big(P_\pi(s) - P_a(s)\big)(I - \gamma P_\pi)^{-1} R - \lambda \|R\|_1$ subject to the test above and $|R(s)| \le R_{\max}$. This is a [linear program](/linear-programming-problem/) after the usual change of variables for the minimum and the absolute values. With features, the same idea applies to sampled policies, by repeatedly adding the best response to the current reward.
- **Apprenticeship learning** (Abbeel and Ng, 2004). Alternate: find $w$ with $\|w\|_2 \le 1$ that maximizes the gap $w^\top(\hat\mu_E - \mu(\pi_j))$ against the policies found so far; solve the MDP for the reward $w^\top \phi$; stop when the gap is below $\epsilon$. A mixture of the policies found then matches the expert's feature expectations.
- **Maximum entropy IRL** (Ziebart and others, 2008). On a deterministic MDP with horizon $T$, each action sequence $\zeta$ has probability $\exp(\theta^\top f_\zeta)/Z(\theta)$, where $f_\zeta$ is the sum of the features along it. The log likelihood of the demonstrations is concave in $\theta$, and its gradient is the expert's feature count minus the expected one. A soft backward pass (log-sum-exp in place of max, see the [log-sum-exp trick](/log-sum-exp-trick/)) and a forward pass compute the expected count in $O(T |S| |A|)$ time:

```pseudo id=main
MAXENT-IRL(deterministic MDP, features φ, demonstrations ζ_1..ζ_m, horizon T, step η)
L1  f̃ ← (1/m) Σ_i Σ_t φ(s^i_t)                     (the expert's feature count)
L2  θ ← 0
L3  repeat
L4      V_T(s) ← θᵀφ(s);  V_t(s) ← θᵀφ(s) + log Σ_a exp V_{t+1}(next(s, a)), for t = T − 1 down to 1
L5      π_t(a | s) ← exp(V_{t+1}(next(s, a)) − V_t(s) + θᵀφ(s))
L6      D_1 ← the start state;  D_{t+1}(s′) ← Σ of D_t(s) π_t(a | s) over s, a with next(s, a) = s′
L7      θ ← θ + η (f̃ − Σ_t Σ_s D_t(s) φ(s))
L8  until the gradient is near 0
L9  return θ
```

  The soft values of line L4 are the same as in [maximum entropy reinforcement learning](/maximum-entropy-rl/). With stochastic dynamics, the usual version uses the causal entropy (Ziebart, Bagnell and Dey, 2010) and the same two passes.
- **Bayesian IRL** samples rewards from a posterior with a random walk Markov chain; each step solves the MDP.
- **Sample-based methods** without known dynamics (guided cost learning, adversarial IRL) alternate between a reward update and a policy update by reinforcement learning.

## Bounds

- **Non-identifiability.** For any reward $R$ and any potential $\Phi$, the shaped reward $R + \gamma \Phi(s') - \Phi(s)$ has the same optimal policies ([potential-based reward shaping](/potential-based-reward-shaping/)); scaling $R$ by $c > 0$ and adding a constant also keep them. So no method can recover more than such an equivalence class from optimal behavior. Under maximum entropy behavior with known dynamics, the policy determines the reward up to a potential-based shaping term (Cao, Cohen and Szpruch, 2021).
- **Concavity.** The maximum entropy log likelihood is concave in $\theta$, so gradient ascent finds the global maximum, and at the maximum the expected feature counts equal the expert's (the moment matching property of exponential families).
- **Apprenticeship guarantees.** If the true reward is $w^{*\top}\phi$ with $\|w^*\|_2 \le 1$, a policy whose feature expectations are within $\epsilon$ of the expert's in the 2-norm loses at most $\epsilon$. Abbeel and Ng (2004) show that their algorithms reach this in a number of iterations polynomial in $k$, $1/\epsilon$ and $1/(1-\gamma)$, and that the number of demonstrations needed grows with $\log k$.
- **Cost.** Every method above solves the forward problem (an MDP) inside its loop, so IRL is at least as costly as planning in the MDP for each reward it tries.

## Reductions

- **IRL to linear programming:** the optimality test is linear in $R$, so the set of consistent rewards and the max-margin choice are linear programs; compare the [linear program for MDPs](/linear-programming-for-mdps/).
- **Imitation to IRL plus planning:** apprenticeship learning and maximum entropy IRL give policies by planning for the learned reward.
- **IRL plus reinforcement learning to occupancy matching:** Ho and Ermon (2016) show that maximum entropy IRL followed by reinforcement learning is the same as finding the policy whose state-action occupancy measure is closest to the expert's under a regularizer chosen by the reward class; GAIL is the case of a Jensen-Shannon distance.
- **IRL to structured prediction:** maximum margin planning treats each path as a structured output.

## Applications

Predicting routes and destinations of drivers (Ziebart and others, 2008, on taxi data), helicopter aerobatics learned from a pilot (Abbeel, Coates and Ng), pedestrian and robot navigation that follows social norms, modeling animal and human decisions in neuroscience and economics, and learning reward models for robots from demonstrations.

## References
