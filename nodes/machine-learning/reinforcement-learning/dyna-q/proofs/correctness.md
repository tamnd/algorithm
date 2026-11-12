---
title: Dyna-Q converges to Q* in a deterministic environment
proves: [correctness, termination]
status: full
---

We use the notation of the page. The environment is a finite MDP with deterministic transitions: taking $a$ in $s$ always gives the reward $r(s, a)$, the next state $\delta(s, a)$ and the flag $\tau(s, a)$, which says whether the next state is terminal. Let $0 \le \gamma < 1$ and $0 < \alpha \le 1$. For a table $Q$ define

$$(\mathcal{T}Q)(s, a) = r(s, a) + [\tau(s, a) = 0]\,\gamma \max_{b} Q(\delta(s, a), b),$$

and let $\lVert Q \rVert = \max_{s, a}|Q(s, a)|$. For two tables, $|(\mathcal{T}Q)(s, a) - (\mathcal{T}Q')(s, a)| \le \gamma \max_b |Q(\delta(s, a), b) - Q'(\delta(s, a), b)| \le \gamma\lVert Q - Q' \rVert$, so $\mathcal{T}$ is a $\gamma$-contraction and has a unique fixed point $Q^*$ ([Bellman contraction](/bellman-contraction/)). $Q^*$ is the optimal action-value function, and a policy that is greedy for $Q^*$ is optimal.

**Termination.** Line L2 repeats a given number of times, line L8 repeats $n$ times, and every other line does a bounded amount of work. So the algorithm stops.

**Lemma 1 (the model is exact).** Every entry $\mathrm{Model}(s, a) = (\rho, s', t)$ written in line L7 satisfies $\rho = r(s, a)$, $s' = \delta(s, a)$ and $t = \tau(s, a)$.

*Proof.* Line L7 stores the outcome that the environment returned in line L5 for the pair $(s, a)$. The environment is deterministic, so this outcome is $(r(s, a), \delta(s, a), \tau(s, a))$. $\square$

**Lemma 2 (one update).** Every update in line L6 or line L11 is, for some pair $(s, a)$,

$$Q_{\text{new}}(s, a) = (1 - \alpha)Q(s, a) + \alpha(\mathcal{T}Q)(s, a),$$

with all other entries unchanged. Let $e = \lVert Q - Q^* \rVert$ before the update. Then after it, $|Q_{\text{new}}(s, a) - Q^*(s, a)| \le (1 - \alpha)|Q(s, a) - Q^*(s, a)| + \alpha\gamma e \le e$, and $\lVert Q_{\text{new}} - Q^* \rVert \le e$.

*Proof.* In line L6 the target is the observed outcome, and in line L11 it is the model entry, which is the same by Lemma 1. In both cases the target is $(\mathcal{T}Q)(s, a)$, with the reward alone when the next state is terminal. Since $Q^* = \mathcal{T}Q^*$,

$$Q_{\text{new}}(s, a) - Q^*(s, a) = (1 - \alpha)(Q(s, a) - Q^*(s, a)) + \alpha((\mathcal{T}Q)(s, a) - (\mathcal{T}Q^*)(s, a)),$$

and the contraction gives the first bound. Because $1 - \alpha + \alpha\gamma \le 1$, the right side is at most $e$. The other entries do not change, so the largest error does not grow. $\square$

**Lemma 3 (one round).** Let $\mathcal{P}$ be the set of all pairs. Suppose that from time $t$ on, the agent updates only pairs of $\mathcal{P}$, and that between $t$ and a later time $t'$ every pair is updated at least once. Then $e_{t'} \le (1 - \alpha(1 - \gamma))e_t$.

*Proof.* By Lemma 2 the largest error never increases, so $e_u \le e_t$ for every $u \ge t$. Take a pair $(s, a)$ and its last update before $t'$, at time $u$. Lemma 2 gives, just after it, $|Q(s, a) - Q^*(s, a)| \le (1 - \alpha)|Q_u(s, a) - Q^*(s, a)| + \alpha\gamma e_u \le (1 - \alpha)e_t + \alpha\gamma e_t$. The entry does not change between $u$ and $t'$. This holds for every pair, which gives the bound. $\square$

**Theorem.** In a deterministic environment with $\gamma < 1$, $0 < \alpha \le 1$ and $n \ge 1$, suppose that every pair $(s, a)$ is tried at least once in line L5. Then, as the number of real steps grows, $Q \to Q^*$ with probability 1, and after finitely many steps every greedy policy for $Q$ is optimal.

*Proof.* Let $t_0$ be the step at which the last untried pair is tried. After $t_0$ the model holds every pair, and each planning step in line L9 picks a state uniformly from the seen states and an action uniformly from those tried in it, so it picks each fixed pair with probability at least $1/(|S||A|)$, independently of the past. With probability 1, every pair is therefore picked infinitely often, so the time after $t_0$ splits into infinitely many rounds in which every pair is updated at least once. By Lemma 3 the largest error falls by the factor $1 - \alpha(1 - \gamma) < 1$ in each round, so $\lVert Q - Q^* \rVert \to 0$.

For the policy, let $g > 0$ be the smallest gap $Q^*(s, a^*) - Q^*(s, a)$ over all states and all actions $a$ that are not optimal in $s$, where $a^*$ is optimal. If no such action exists every policy is optimal. Once $\lVert Q - Q^* \rVert < g/2$, every action that maximizes $Q(s, \cdot)$ maximizes $Q^*(s, \cdot)$, so the greedy policy is optimal. $\blacksquare$

**Remarks.** With $n = 0$ the same argument works for Q-learning on a deterministic environment, provided that the ε-greedy policy tries every pair infinitely often. The role of the planning steps is to make the rounds short in real steps: one real step brings $n$ updates. In a stochastic environment Lemma 1 fails, because the model keeps only the last outcome, and then the theorem does not hold.
