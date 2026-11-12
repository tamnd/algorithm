---
tag: WJ898F
kind: algorithm
slug: double-dqn
name: Double DQN
aliases:
- DDQN
- deep double Q-learning
area: machine-learning/reinforcement-learning
level: advanced
summary: "DQN with the target y = r + gamma Q(s', argmax_a' Q(s', a'; theta); theta-minus): the online network selects the next action and the target network evaluates it, which reduces overestimation."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the number of environment steps, B: the minibatch size, W: the cost of one forward and backward pass of the network, N: the replay capacity}
  time: {worst: "O(T B W)"}
  space: {extra: "O(N)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2016
  people: [Hado van Hasselt, Arthur Guez, David Silver]
  note: "Van Hasselt, Guez and Silver combined the double estimator of double Q-learning with the target network of DQN at AAAI 2016."
prereqs: [dqn, double-q-learning]
see_also: [dueling-network, prioritized-experience-replay, q-learning, td-error, deadly-triad, td3]
sources:
  - paper: "Hado van Hasselt, Arthur Guez and David Silver, Deep reinforcement learning with double Q-learning, Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence (AAAI), 2016, pages 2094 to 2100, arXiv:1509.06461"
    locator: the section on Double DQN (the target with online selection and target evaluation), Theorem 1 (the lower bound on the overestimation of the maximum) and the Atari experiments
  - paper: "Hado van Hasselt, Double Q-learning, Advances in Neural Information Processing Systems 23 (NIPS 2010), pages 2613 to 2621"
    locator: the double estimator and the double Q-learning algorithm
  - paper: doi:10.1038/nature14236
    title: "Volodymyr Mnih and others, Human-level control through deep reinforcement learning, Nature 518(7540), 2015, pages 529 to 533"
    locator: the DQN algorithm and the target network that Double DQN reuses
  - paper: "Sebastian Thrun and Anton Schwartz, Issues in using function approximation for reinforcement learning, Proceedings of the 1993 Connectionist Models Summer School, 1993"
    locator: the systematic overestimation caused by the maximum over approximate values
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.7 (maximization bias and double learning)
---

Double DQN (van Hasselt, Guez and Silver, 2016) is [DQN](/dqn/) with one line changed. DQN's target $r + \gamma \max_{a'} Q(s', a'; \theta^-)$ uses the target network both to choose the next action and to value it, so the noise in its estimates pushes the target up. Double DQN chooses the action with the online network and values it with the target network:

$$y = r + \gamma\, Q\big(s', \arg\max_{a'} Q(s', a'; \theta);\ \theta^-\big).$$

This is the double estimator of [double Q-learning](/double-q-learning/), with the target network as the second estimator, so it costs no extra network. On the Atari games of DQN it gave lower, more accurate value estimates and better scores on many games.

## In plain words

DQN asks: of all the actions in the next situation, which looks best, and how good does it look? It answers both questions with the same estimates. When the estimates are noisy, the action that looks best is often the one whose estimate happens to be too high, so the answer to the second question is too high on average. These high answers then feed into the next targets.

Double DQN answers the two questions with two different sets of estimates. The current network picks the action that looks best. The older, frozen copy of the network says how good that action is. If the two sets of errors are not the same, the action that the current network likes for a lucky error gets an honest value from the frozen copy.

## The problem

The setting is that of [DQN](/dqn/): [reinforcement learning control](/rl-control/) in an unknown MDP with a finite action set and the discounted criterion, with a parametric $Q(s, a; \theta)$. The specific defect it addresses is the *overestimation* of DQN's targets: if the estimates $Q(s', a; \theta^-)$ equal the true values plus zero-mean errors, then $\mathbb{E}[\max_{a'} Q(s', a'; \theta^-)] \ge \max_{a'} Q^{\text{true}}(s', a')$, and the inequality is strict in general. The argument is the maximization bias of [double Q-learning](/double-q-learning/); this page does not repeat it.

## The algorithm

The notation is that of [DQN](/dqn/). Only lines L6 and L7 differ from DQN.

```pseudo id=main
DOUBLE-DQN(env, T, N, B, C, γ, η)
L1  D ← empty buffer of capacity N; θ ← random; θ⁻ ← θ
L2  for t ← 1 to T do
L3      a ← random action with probability ε_t, else argmax_a Q(s, a; θ)
L4      do a, observe r, s′, done; store (s, a, r, s′, done) in D
L5      draw a minibatch (s_j, a_j, r_j, s′_j, done_j), j = 1..B, uniformly from D
L6      a*_j ← argmax_a′ Q(s′_j, a′; θ)                     ▷ select with the online network
L7      y_j ← r_j if done_j, else r_j + γ Q(s′_j, a*_j; θ⁻)  ▷ evaluate with the target network
L8      θ ← θ − η ∇_θ (1/B) Σ_j h(y_j − Q(s_j, a_j; θ))     ▷ y_j is a constant
L9      if t mod C = 0 then θ⁻ ← θ
L10     s ← s′, or a new start state if done
```

Line L6 needs one more forward pass of the online network per sample, on $s'_j$. Both $a^*_j$ and $y_j$ are constants for the gradient of line L8. The paper also tuned three DQN settings for its main results (a longer sync period, a smaller final $\epsilon$ in training and a smaller $\epsilon$ in evaluation) and used one bias shared by all action values in the output layer; the algorithm is the same.

**Comparison with double Q-learning.** Tabular double Q-learning keeps two tables $Q^A$ and $Q^B$, updates one of them at random in each step, and uses the other to evaluate. Double DQN does not train two networks symmetrically: $\theta^-$ is an old copy of $\theta$, not an independent estimate. It is the smallest change to DQN that decouples selection from evaluation.

## Example

**A fixed table.** At $s'$ there are three actions, the online network gives $Q(s', \cdot; \theta) = (1, 3, 2)$ and the target network $Q(s', \cdot; \theta^-) = (2, 1, 4)$. With $r = \tfrac12$ and $\gamma = \tfrac{9}{10}$:

| target | chosen action | value used | $y$ |
|---|---|---|---|
| DQN | $\arg\max(2, 1, 4) = 3$rd | 4 | $\tfrac12 + \tfrac{9}{10} \cdot 4 = 4.1$ |
| Double DQN | $\arg\max(1, 3, 2) = 2$nd | 1 | $\tfrac12 + \tfrac{9}{10} \cdot 1 = 1.4$ |

The two targets agree whenever the two networks rank the same action first; in particular they are equal when $\theta^- = \theta$.

**The bias, exactly.** Let all $m$ actions at $s'$ have true value 0, and let each network add independent noise $\pm 1$ with probability $\tfrac12$ each, with $r = 0$, $\gamma = 1$. Averaging over all $2^{2m}$ noise patterns gives

| $m$ | DQN target, mean | Double DQN target, mean |
|---|---|---|
| 2 | $1/2$ | 0 |
| 3 | $3/4$ | 0 |
| 4 | $7/8$ | 0 |

The DQN mean is $1 - 2^{1-m}$: the maximum of $m$ signs is $-1$ only when all are $-1$. The Double DQN mean is 0, because the chosen index depends only on the online noise, and the target noise at any fixed index has mean 0. With standard normal noise and $m = 10$, 4000 seeded trials give a mean of 1.554 for the DQN target (the exact mean of the maximum of 10 standard normals is about 1.539) and 0.005 for the Double DQN target.

**A full run.** On the 6-state chain of the [DQN](/dqn/) page, with the same network and settings (3000 steps, $C = 50$), seeds 0 and 1 of the implementation reach the optimal policy, with $Q(s, \text{right})$ within 0.02 of $0.9^{5-s}$.

## Correctness

Like DQN, Double DQN has no convergence guarantee with function approximation. The proved facts (full proofs below) are:

1. **No upward bias from independent evaluation.** If, given the online network, the target network's errors at $s'$ have mean zero, then $\mathbb{E}[y \mid \theta] = r + \gamma\, Q^{\text{true}}(s', a^*) \le r + \gamma \max_{a'} Q^{\text{true}}(s', a')$. The Double DQN target may underestimate, but on average it does not overestimate.
2. **The overestimation of the maximum has a floor** (van Hasselt, Guez and Silver, Theorem 1). If the true values at $s$ are all equal to $V^*(s)$, the estimates have errors $e_a$ with $\sum_a e_a = 0$ and $\frac{1}{m}\sum_a e_a^2 = c > 0$, with $m \ge 2$ actions, then $\max_a Q(s, a) \ge V^*(s) + \sqrt{c/(m-1)}$, and the bound is tight. Under the same conditions, the lower bound on the absolute error of the double estimate is zero.
3. **Reduction.** If $\theta^- = \theta$, the Double DQN target equals the DQN target.

## Complexity

The same as [DQN](/dqn/) up to a constant: line L6 adds one forward pass per sample, so $T$ steps cost $O(T B W)$ arithmetic operations in the worst case, with $W$ the cost of one forward and backward pass. Memory is the buffer of $N$ transitions and two networks. No bound on the number of steps to a good policy is known; the Atari budgets are observed.

## Properties

- **Off-policy, model-free, value-based**, as DQN.
- **Less overestimation, not none.** $\theta^-$ is a delayed copy of $\theta$, so their errors are correlated; the decoupling is partial.
- **Can underestimate.** The value of the action chosen by the online network can be below the true maximum.
- **No extra parameters.** It reuses the target network of DQN.

## Variants and improvements

- **Clipped double Q-learning.** [TD3](/td3/) trains two critics and uses the minimum of the two in the target, a stronger guard against overestimation for continuous actions.
- **Double DQN with [prioritized replay](/prioritized-experience-replay/) and [dueling heads](/dueling-network/).** These combine directly; Algorithm 1 of the prioritized replay paper is Double DQN.
- **Averaged and ensemble targets.** Averaging several old target networks, or an ensemble, reduces the variance of the target and with it the overestimation.

## When to use it

Use Double DQN in place of DQN whenever DQN is used: the change is one line and one forward pass. It matters most when many actions have similar values and the estimates are noisy, which is when the maximum is biased most. If the problem has continuous actions, use [TD3](/td3/) or [soft actor-critic](/soft-actor-critic/) instead.

## Pitfalls

- **Swapping the roles.** Selecting with $\theta^-$ and evaluating with $\theta$ in lines L6 and L7 also decouples the two, but the evaluated values then move with every gradient step, and the target is no longer fixed between syncs. Select with $\theta$, evaluate with $\theta^-$.
- **Using the maximum of the online network as the value.** $\max_{a'} Q(s', a'; \theta)$ is the DQN target without a target network, not Double DQN. Line L7 must read $Q(s', a^*; \theta^-)$.
- **Expecting independence.** Right after a sync, $\theta^- = \theta$ and the targets equal the DQN targets. The decoupling grows as the online network moves away from its copy.
- **Ties in the argmax.** With exact ties, pick a fixed rule (the first index), or the target becomes random.

## Implementations

## History

Thrun and Schwartz (1993) showed that the maximum over approximate values overestimates. Van Hasselt (2010) proposed the double estimator and double Q-learning for the tabular case. Van Hasselt, Guez and Silver (2016) applied the idea to DQN with the target network as the second estimator, proved the lower bound on the overestimation of the maximum, and showed on Atari that DQN's value estimates were far too high on several games and that Double DQN reduced them and improved the scores.

## References
