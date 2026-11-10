---
title: Greedy restricted assignment is (ceil(log2 m) + 1)-competitive
proves: [correctness]
status: full
---

**Feasibility.** Line L3 picks a machine of $M_t$, and line L4 assigns job $t$ to it, so every job runs on an eligible machine. Line L4 sets $a[t]$ once, and no later line changes it, so the assignment is final and online: the choice for job $t$ depends only on the loads, which depend only on jobs $1, \ldots, t - 1$. Line L5 keeps $\ell[i]$ equal to the total size of the jobs assigned to machine $i$ so far, so line L6 returns the makespan.

**Setup.** Fix $\sigma$ and the run of the algorithm, with any tie rule in line L3. Let $L^* = \mathrm{OPT}(\sigma)$. If $L^* = 0$, all sizes are $0$ and all loads stay $0$. So let $L^* > 0$. Fix an optimal assignment, and for each machine $j$ let $O_j$ be the set of jobs that it puts on $j$. Then $j \in M_t$ for each $t \in O_j$, and
$$\sum_{t \in O_j} p_t \le L^* \quad \text{for each } j, \qquad p_t \le L^* \text{ for each } t, \qquad W = \sum_t p_t \le m L^* .$$

**The stacks.** Let $s_t$ be the load of the machine chosen for job $t$ just before line L5, and $e_t = s_t + p_t$. On each machine, the jobs occupy the intervals $[s_t, e_t)$ of heights, one after the other, in order of arrival, and the final load $\ell_i$ is the top of the stack of machine $i$. For a height $y \ge 0$, the part of job $t$ above $y$ has size $\max\{0, e_t - \max\{s_t, y\}\}$. Define
$$V(y) = \sum_t \max\{0, e_t - \max\{s_t, y\}\} = \sum_i \max\{0, \ell_i - y\},$$
the total work above height $y$. Also define, for each machine $j$,
$$O_j(y) = \sum_{t \in O_j} \max\{0, e_t - \max\{s_t, y\}\}, \qquad B_j(x) = \max\{0, \min\{\ell_j - x, L^*\}\}.$$
$O_j(y)$ is the work above height $y$ of the jobs that the optimum puts on $j$, wherever greedy put them. $B_j(x)$ is the work of greedy on machine $j$ in the band of heights $[x, x + L^*]$. Since the sets $O_j$ partition the jobs, $\sum_j O_j(y) = V(y)$, and since the bands are consecutive, $\sum_j B_j(x) = V(x) - V(x + L^*)$.

**Lemma (band).** For every $x \ge 0$ and every machine $j$, $B_j(x) \ge O_j(x + L^*)$.

*Proof.* Let $y = x + L^*$, and let $K$ be the set of jobs $t \in O_j$ with $e_t > y$. Only these jobs contribute to $O_j(y)$. If $K$ is empty, $O_j(y) = 0 \le B_j(x)$. Otherwise let $t^* \in K$ have the largest start $s^* = s_{t^*}$ in $K$.

When job $t^*$ came, machine $j$ was eligible, because $t^* \in O_j$. Line L3 chose a machine of least load in $M_{t^*}$, and that load was $s^*$. So the load of machine $j$ at that time was at least $s^*$, and since loads never decrease, $\ell_j \ge s^*$.

*Case $s^* \ge y$.* Then $\ell_j \ge y = x + L^*$, so $B_j(x) = L^* \ge \sum_{t \in O_j} p_t \ge O_j(y)$.

*Case $s^* < y$.* Then every $t \in K$ has $s_t \le s^* < y$, so its part above $y$ is $e_t - y = s_t + p_t - y$. For $t \ne t^*$ this is at most $p_t$, and for $t^*$ it is $p_{t^*} + (s^* - y)$. So
$$O_j(y) \le \sum_{t \in K} p_t + (s^* - y) \le L^* + s^* - y = s^* - x .$$
Since $O_j(y) > 0$ when $K$ is not empty, $s^* > x$. Also $s^* - x < y - x = L^*$, and $\ell_j \ge s^*$. Hence $B_j(x) \ge \min\{s^* - x, L^*\} = s^* - x \ge O_j(y)$. $\square$

**Lemma (halving).** For every $x \ge 0$, $V(x + L^*) \le \frac12 V(x)$.

*Proof.* Sum the band lemma over all machines $j$: $V(x) - V(x + L^*) = \sum_j B_j(x) \ge \sum_j O_j(x + L^*) = V(x + L^*)$. $\square$

**Theorem.** $\max_i \ell_i \le (\lceil \log_2 m \rceil + 1) L^*$.

*Proof.* Let $b = \lceil \log_2 m \rceil$, so $2^b \ge m$. By the halving lemma $b$ times, starting at $x = 0$,
$$V(b L^*) \le \frac{V(0)}{2^b} = \frac{W}{2^b} \le \frac{m L^*}{2^b} \le L^* .$$
If some machine $i$ had $\ell_i > (b + 1) L^*$, then $V(b L^*) \ge \ell_i - b L^* > L^*$, a contradiction. $\blacksquare$

The argument holds for each prefix of $\sigma$ in place of $\sigma$, with the optimum of that prefix, so the bound holds at every moment.

**Theorem (unit jobs).** If all $p_t = 1$ and $L^* = 1$, then $\max_i \ell_i \le \lfloor \log_2 m \rfloor + 1$.

*Proof.* All loads are integers. For an integer $r \ge 1$, let $c_r$ be the number of machines with $\ell_i \ge r$, and let $T_r = \sum_{h \ge r} c_h$, the number of jobs that greedy placed at a height of at least $r - 1$. Then $V(r - 1) = T_r$. With $L^* = 1$ and $x = r - 1$, the band $B_j(r - 1)$ is $1$ if $\ell_j \ge r$ and $0$ otherwise, so $\sum_j B_j(r - 1) = c_r = T_r - T_{r+1}$, and the halving lemma gives $T_{r+1} \le T_r - T_{r+1}$, that is $T_{r+1} \le \frac12 T_r$.

Since $L^* = 1$, each machine gets at most one job in the optimum, so $T_1 = n \le m$. Let $k = \lfloor \log_2 m \rfloor$, so $m < 2^{k+1}$. If some machine had load at least $k + 2$, then $T_{k+2} \ge 1$, and $k + 1$ halvings give $T_1 \ge 2^{k+1} > m$, a contradiction. So every load is at most $k + 1$. $\blacksquare$

**Tightness.** The pair adversary of the [lower bound](/online-restricted-assignment-lower-bound/) gives unit jobs with $\mathrm{OPT} = 1$ on which every deterministic algorithm, greedy included, ends with load $\lfloor \log_2 m \rfloor + 1$. So the unit bound is exact, and the general bound is exact when $m$ is a power of two.
