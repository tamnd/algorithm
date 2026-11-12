---
title: The iteration finds the least fixed point, which is the worst-case response time
proves: [correctness]
status: full
---

Fix a task $\tau_i$ and a blocking term $B \ge 0$, and let $F(t) = C_i + B + \sum_{j < i} \lceil t / T_j \rceil C_j$ for $t > 0$. Let $R^* = \min\{t > 0 : F(t) \le t\}$, or $R^* = \infty$ if there is no such $t$. The minimum exists when the set is not empty. Let $s$ be the infimum of the set. Since $F(t) \ge C_i > 0$, the set has no points below $C_i$, so $s > 0$. The function $F$ is non-decreasing and constant on each interval $(a, b]$ between two neighboring multiples of the periods, so there is a $\delta > 0$ with $F$ constant on $(s, s + \delta]$; this constant is at most each point of the set in that interval, so it is at most $s$. Then $F(s) \le s$, and $s$ is in the set. At this least element, $F(R^*) = R^*$: if $F(R^*) < R^*$, then each $t$ with $F(R^*) \le t < R^*$ has $F(t) \le F(R^*) \le t$, which contradicts the choice of $R^*$.

**Lemma 1.** Let $r_0 = C_i + B$ and $r_{m+1} = F(r_m)$ (lines L1, L3 and L6). Then $r_0 \le r_1 \le r_2 \le \cdots$, and $r_m \le R^*$ for each $m$.

*Proof.* $F$ is non-decreasing, and $F(t) \ge C_i + B$ for each $t > 0$. So $r_1 = F(r_0) \ge r_0$, and if $r_m \ge r_{m-1}$ then $r_{m+1} = F(r_m) \ge F(r_{m-1}) = r_m$. Next, $R^* \ge F(R^*) \ge C_i + B = r_0$, and if $r_m \le R^*$ then $r_{m+1} = F(r_m) \le F(R^*) \le R^*$. If $R^* = \infty$, the second claim is empty. $\square$

**Lemma 2 (termination).** The loop stops after at most $1 + \sum_{j < i} \lceil D_i / T_j \rceil$ rounds.

*Proof.* While the loop runs, $r_m \le D_i$, by line L4. If $r_{m+1} > r_m$, then some count $\lceil r_m / T_j \rceil$ is larger than $\lceil r_{m-1} / T_j \rceil$, by the form of $F$, and no count decreases by Lemma 1. Each count is at most $\lceil D_i / T_j \rceil$. If $r_{m+1} = r_m$, line L5 returns. $\square$

**Lemma 3 (the result).** If the call returns $R$, then $R = R^*$. If it returns MISS, then $R^* > D_i$.

*Proof.* Line L5 returns $R = r_m$ with $F(r_m) = r_m$. So $r_m$ is in the set that defines $R^*$, and $R^* \le r_m$. With Lemma 1, $r_m = R^*$. Line L4 returns MISS when $r_{m+1} > D_i$. By Lemma 1, $R^* \ge r_{m+1} > D_i$. $\square$

**Theorem.** Let $D_k \le T_k$ for each $k$, with no blocking and no jitter. Then `response_time_analysis` returns $R_i^*$ for each task with $R_i^* \le D_i$ and `None` for the other tasks, and `schedulable` returns true if and only if the priority order meets all deadlines in each legal release pattern.

*Proof.* With $B = 0$, $R^*$ is the value $R_i$ of the [critical instant theorem](/rate-monotonic-optimality/). If $R_i \le D_i$, then $R_i \le T_i$, and by that theorem each job of $\tau_i$ ends at most $R_i$ after its release, and the synchronous release reaches $R_i$. If $R_i > D_i$, the first job of $\tau_i$ in the synchronous release ends after its deadline. Lemma 3 shows that the call returns $R_i$ in the first case and MISS (`None`) in the second. $\blacksquare$

**Blocking.** Assume that a protocol guarantees that a job of $\tau_i$ is delayed by jobs of lower priority for at most $B$ in total, and only while jobs of $\tau_i$ or of higher priority are pending. In the proof of the critical instant theorem, the work in the busy window then grows by at most $B$, and the same argument gives the bound $R^*$ for $F$ with $B$. The bound is not always reached, so the test is sufficient.
