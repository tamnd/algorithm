---
title: The cells of a stable Bloom filter record the decay since the last set
proves: [correctness, invariant, termination]
status: full
---

Write $C_t$ for the array after step $t$, and $V_t$ for the set of $P$ cells chosen at line L3 of step $t$. Each step does $K$ checks, $P$ decrements and $K$ sets, so it ends.

**Lemma 1 (invariant (D)).** For each $t \ge 0$ and each cell $j$, let $\tau = \max\{ s \le t : j \in H(x_s) \}$, if it exists. Then $C_t[j] = \max(0, \mathrm{Max} - |\{s : \tau < s \le t,\ j \in V_s\}|)$, and $C_t[j] = 0$ if $\tau$ does not exist.

*Proof.* By induction on $t$. At $t = 0$ all cells are 0 by line L1, and no element has arrived. Consider step $t + 1$ and cell $j$. If $j \in H(x_{t+1})$, then $\tau = t + 1$, there are no later decrements, and line L4 sets $C_{t+1}[j] = \mathrm{Max}$, after line L3. Otherwise $\tau$ is unchanged. If $j \in V_{t+1}$, the count of decrements grows by 1, and line L3 lowers the cell by 1 if it is above 0, which is the change of $\max(0, \mathrm{Max} - D)$ when $D$ grows by 1; and if $\tau$ does not exist the cell stays 0. If $j \notin V_{t+1}$, nothing changes. $\square$

**Theorem 1 (what is reported).** PROCESS$(x_t)$ returns true exactly when every $j \in H(x_t)$ was set at some step $\tau_j < t$ and had fewer than Max decrements in the steps $\tau_j + 1, \ldots, t - 1$, where $\tau_j$ is the last such step.

*Proof.* Line L2 reads $C_{t-1}$ before the decrements and sets of step $t$. By Lemma 1, $C_{t-1}[j] > 0$ exactly when $\tau_j \le t - 1$ exists and fewer than Max of the steps $\tau_j + 1, \ldots, t - 1$ chose $j$. $\square$

**Corollary 1.** If $x_t = x_{t-1}$, PROCESS$(x_t)$ returns true. More generally, if $x_t = x_s$ with $s < t$, and no cell of $x_t$ was chosen Max times in the steps $s + 1, \ldots, t - 1$, then PROCESS$(x_t)$ returns true.

*Proof.* Each $j \in H(x_t)$ was set at step $s$, so its last set $\tau_j$ satisfies $s \le \tau_j < t$, and it had at most as many decrements after $\tau_j$ as after $s$. For $s = t - 1$ there are no steps in between. Theorem 1 gives the claim. $\blacksquare$
