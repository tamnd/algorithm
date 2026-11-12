---
title: The invariants of Monte Carlo ES, and why its stable points are optimal policies
proves: [correctness, termination]
status: full
---

We use the notation of the page. The MDP is finite and episodic: with $\gamma = 1$, every policy ends each episode with probability 1. We write $q_\pi$ and $v_\pi$ for the values of a policy $\pi$. The convergence of MC ES to a stable point is not proved here; it is open in general (see the page).

**Termination.** Under the assumption, the episode of line L4 ends with probability 1, so it has a finite length $T$. Lines L5 to L10 then run $T$ times, each in $O(A)$ time. The loop of line L2 runs $n$ times. So the algorithm stops with probability 1. The implementation also stops with an error if an episode passes a given length, so it always stops. $\square$

**Lemma 1 (first visits).** In each episode, lines L6 to L9 update each pair $(s, a)$ of the episode exactly once, with the return $G_{t_0}$ after its first visit $t_0$.

*Proof.* The loop of line L6 runs $t$ from $T - 1$ down to 0. Before line L7 at time $t$, $G = G_{t+1}$: this holds at $t = T - 1$, since $G = 0 = G_T$, and line L7 turns $G_{t+1}$ into $\gamma G_{t+1} + R_{t+1} = G_t$. Line L8 skips time $t$ exactly when $(S_t, A_t)$ occurs at an earlier time, so the only time that is not skipped for a pair is its first visit $t_0$, and there $G = G_{t_0}$. $\square$

**Lemma 2 (sample averages).** After each episode, for each pair with $N(s, a) = m > 0$, $Q(s, a)$ is the mean of the $m$ first-visit returns of $(s, a)$ observed so far.

*Proof.* By Lemma 1, each update of $(s, a)$ adds one new first-visit return $g$. If $Q$ is the mean $\bar g_{m-1}$ of the first $m - 1$ returns (with $\bar g_0 = 0$ and $m - 1 = 0$ at the start), line L9 sets $Q = \bar g_{m-1} + (g - \bar g_{m-1})/m = ((m-1)\bar g_{m-1} + g)/m$, the mean of the $m$ returns. $\square$

**Lemma 3 (greedy policy).** After each episode, for every state $s$ at which some pair was updated, $\pi(s)$ maximizes $Q(s, \cdot)$.

*Proof.* $Q(s, \cdot)$ changes only in line L9, and only for the state $S_t$ of that line. Line L10 runs right after it for the same state and sets $\pi(S_t)$ to a maximizer. So after each step of the loop, $\pi(s)$ maximizes $Q(s, \cdot)$ at every state that has been updated. $\square$

**Theorem 1 (stable points are optimal).** Let $\pi$ be a deterministic policy with $\pi(s) \in \arg\max_a q_\pi(s, a)$ for every state $s$. Then $\pi$ is optimal. So if MC ES reaches a point where $Q = q_\pi$ and $\pi$ is greedy in $Q$, then $\pi$ is optimal.

*Proof.* For each state, $v_\pi(s) = q_\pi(s, \pi(s)) = \max_a q_\pi(s, a) = \max_a \big(r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\, v_\pi(s')\big)$, with $v_\pi = 0$ at the terminal state. So $v_\pi$ solves the Bellman optimality equation. That equation has exactly one solution, $v_*$: for $\gamma < 1$ because its operator is a $\gamma$-contraction in the max norm, and for $\gamma = 1$ under the assumption that every policy ends episodes with probability 1 (Bertsekas and Tsitsiklis, Neuro-Dynamic Programming, the results on stochastic shortest path problems). So $v_\pi = v_*$, and $\pi$ is optimal. $\square$

**Theorem 2 (the ε-greedy step improves).** Let $\varepsilon \in (0, 1]$, let $\pi$ be ε-soft ($\pi(a \mid s) \ge \varepsilon / |A(s)|$ for all $a$), and let $\pi'$ be ε-greedy in $q_\pi$: $\pi'(a \mid s) = \varepsilon / |A(s)|$ plus $1 - \varepsilon$ for one maximizing action. Then $v_{\pi'} \ge v_\pi$ in every state.

*Proof.* Fix $s$ and write $k = |A(s)|$ and $q(a) = q_\pi(s, a)$. If $\varepsilon = 1$, then $\pi = \pi'$, the uniform policy, and there is nothing to prove. Else the numbers $w(a) = (\pi(a \mid s) - \varepsilon/k)/(1 - \varepsilon)$ are nonnegative because $\pi$ is ε-soft, and they sum to $(1 - \varepsilon)/(1 - \varepsilon) = 1$. A weighted mean is at most the maximum, so

$$\sum_a \pi'(a \mid s)\, q(a) = \frac{\varepsilon}{k}\sum_a q(a) + (1 - \varepsilon)\max_a q(a) \ge \frac{\varepsilon}{k}\sum_a q(a) + (1-\varepsilon)\sum_a w(a)\, q(a) = \sum_a \pi(a \mid s)\, q(a) = v_\pi(s).$$

This is the hypothesis of the policy improvement theorem, which gives $v_{\pi'} \ge v_\pi$. $\square$

**Corollary.** If an ε-soft policy $\pi$ is ε-greedy in its own values $q_\pi$, then no ε-soft policy is better. Sutton and Barto (Section 5.4) prove this by moving the requirement of ε-softness into the environment: in the new environment, with probability $\varepsilon$ the action is replaced by a uniform one, and the best policies of the new environment are exactly the best ε-soft policies of the old one. Equality in the chain of Theorem 2 then says that $v_\pi$ solves the Bellman optimality equation of the new environment, so it is optimal there by the argument of Theorem 1. $\blacksquare$
