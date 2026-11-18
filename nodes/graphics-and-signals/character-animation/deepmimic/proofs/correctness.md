---
title: The DeepMimic imitation reward lies in [0, 1] with its maximum on the reference, and RSI and early termination do what they state
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
This file is about the reward and the episode rules of the toy, which follow the paper.
It does not prove anything about the learning: PPO with neural network policies has no convergence guarantee for this problem, and the toy has no learner.

## The reward

The imitation reward is
$r^I = 0.65\, r^p + 0.1\, r^v + 0.15\, r^e + 0.1\, r^c$
with $r^p = \exp(-2 \sum_j \|\hat q_j \ominus q_j\|^2)$, $r^v = \exp(-0.1 \sum_j \|\hat{\dot q}_j - \dot q_j\|^2)$, $r^e = \exp(-40 \sum_e \|\hat p_e - p_e\|^2)$ and $r^c = \exp(-10 \|\hat p_c - p_c\|^2)$, where a hat marks the reference, $\ominus$ is the rotation angle between two joint orientations, the $p_e$ are the end effector positions and $p_c$ is the center of mass.
With a task reward $r^G \in [0, 1]$, the reward is $r = 0.7\, r^I + 0.3\, r^G$.

**Theorem 1.** $0 < r^I \le 1$, and $r^I = 1$ if and only if every pose difference, velocity difference, end effector difference and center of mass difference is zero.
With a task, $0 < r \le 1$, and $r = 1$ if and only if $r^I = 1$ and $r^G = 1$.

*Proof.*
Each term is $\exp(-k x)$ with $k > 0$ and $x \ge 0$, so it lies in $(0, 1]$ and equals 1 exactly when $x = 0$.
The weights $0.65, 0.1, 0.15, 0.1$ are positive and sum to 1, so $r^I$ is a convex combination of numbers in $(0, 1]$; it is in $(0, 1]$, and it is 1 exactly when all four terms are 1.
The same argument with the weights $0.7$ and $0.3$ gives the claim for $r$. $\blacksquare$

**Lemma 1.** If the state equals the reference pose and velocity at the current time, then $r^I = 1$.

*Proof.*
The end effectors and the center of mass are functions of the pose, so their differences are also zero, and Theorem 1 applies. $\square$

## Reference state initialization

The reference is periodic with period $T$.
RSI draws a phase $t_0$ uniformly from $[0, T)$ and starts in the reference state $(\hat q(t_0), \hat{\dot q}(t_0))$ at time $t_0$; the fixed start uses $t_0 = 0$.

**Theorem 2.** Every RSI start state lies on the reference motion, and its reward, measured before the first action, is 1.
For any phase interval $I \subset [0, T)$, the probability that the start phase is in $I$ is $|I| / T$.

*Proof.*
The start state is the reference state at $t_0$ by definition, and Lemma 1 gives the reward.
The phase is uniform on $[0, T)$. $\blacksquare$

So every part of the clip, also the late parts that a policy reaches only after it learns the early parts, appears as a start state with a positive probability.
That this speeds up learning is a measurement in the paper, not a theorem.

## Early termination

The episode has $K$ control steps with rewards $r_0, \dots, r_{K-1}$ and the discount $\gamma \in (0, 1)$.
With early termination, the episode ends at the first step $k^*$ at which the character is in a fallen state, and the toy sets $r_k = 0$ for $k \ge k^*$.

**Theorem 3.** With early termination, the return is $\sum_{k < k^*} \gamma^k r_k$, so no state at or after the fall adds to it.
Every return lies in $[0, (1 - \gamma^K)/(1 - \gamma)]$.

*Proof.*
The rewards from $k^*$ on are zero.
Each reward is in $[0, 1]$ by Theorem 1, so the return is between 0 and $\sum_{k < K} \gamma^k$. $\blacksquare$

Without early termination, a fallen state can still earn a positive reward, because every term of $r^I$ is positive (Theorem 1).
The test measures this on the toy: a rod with no torque falls, and without termination it earns a larger return than with termination, and the difference comes only from the steps at and after the fall.
