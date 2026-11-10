---
title: The slot rounding costs at most the LP and loads each machine to at most T plus one job
proves: [correctness]
status: full
---

**Setting.** The machines are $i = 1, \ldots, m$ and the jobs are $j = 1, \ldots, n$, with times $p_{ij} \ge 0$, costs $c_{ij} \ge 0$ and a target $T > 0$. Let $x$ be a feasible solution of the LP of line L1: $\sum_i x_{ij} = 1$ for each job $j$, $\sum_j p_{ij} x_{ij} \le T$ for each machine $i$, $x \ge 0$, and $x_{ij} = 0$ whenever $p_{ij} > T$. Let $X_i = \sum_j x_{ij}$ and $k_i = \lceil X_i \rceil$.

**Pouring.** On machine $i$, list the jobs with $x_{ij} > 0$ as $j_1, j_2, \ldots, j_q$ with $p_{i j_1} \ge p_{i j_2} \ge \cdots \ge p_{i j_q}$, as in line L5. Put the share of $j_t$ on the interval $I_t = [a_{t-1}, a_t)$ of the real line, where $a_0 = 0$ and $a_t = a_{t-1} + x_{i j_t}$, so $a_q = X_i$. Slot $(i, s)$ for $s = 1, \ldots, k_i$ is the interval $[s - 1, s)$. Line L6 puts the amount $z_{j_t, (i,s)} = |I_t \cap [s - 1, s)|$ of job $j_t$ into slot $(i, s)$, and joins $j_t$ to $(i, s)$ when this amount is positive. Set $z = 0$ on all other job-slot pairs.

**Lemma 1 ($z$ is a fractional matching).** For each job $j$, $\sum_{\text{slots } u} z_{j u} = 1$. For each slot $u = (i, s)$, $\sum_j z_{j u} \le 1$, with equality when $s < k_i$. Moreover $\sum_{u} \sum_j c_{u j} z_{j u} = \sum_{i, j} c_{ij} x_{ij}$, where $c_{u j} = c_{ij}$ for a slot $u$ of machine $i$.

*Proof.* The intervals $I_1, \ldots, I_q$ of machine $i$ are disjoint and their union is $[0, X_i)$, which lies inside $[0, k_i)$, the union of the slots of $i$. So the share $x_{ij}$ of job $j$ on machine $i$, which is the length of its interval, is the sum of the lengths of its parts in the slots of $i$. Summing over the machines gives $\sum_u z_{j u} = \sum_i x_{ij} = 1$. A slot $[s - 1, s)$ receives the length of $[s - 1, s) \cap [0, X_i)$, which is at most 1, and it is exactly 1 when $s \le k_i - 1 < X_i$, that is, when $s < k_i$. The cost identity follows because job $j$ in a slot of machine $i$ costs $c_{ij}$ per unit and its parts on machine $i$ add up to $x_{ij}$. $\square$

**Lemma 2 (cost).** Line L7 finds a matching that covers every job, and its cost is at most $\sum_{i, j} c_{ij} x_{ij}$.

*Proof.* Let $B$ be the bipartite graph of line L6, with jobs on one side, slots on the other, and an edge where $z_{ju} > 0$. Consider the polytope $Q = \{ w \ge 0 : \sum_u w_{ju} = 1 \text{ for each job } j, \ \sum_j w_{ju} \le 1 \text{ for each slot } u \}$ on the edges of $B$. Its constraint matrix is the incidence matrix of a bipartite graph, which is totally unimodular, and the right sides are integers, so each vertex of $Q$ is integral. An integral point of $Q$ is a matching of $B$ that covers every job. By Lemma 1, $z \in Q$, so $Q$ is nonempty and bounded, and the linear function $w \mapsto \sum c_{u j} w_{ju}$ attains its minimum over $Q$ at a vertex. That vertex is a matching covering every job, with cost at most the cost of $z$, which is $\sum c_{ij} x_{ij}$ by Lemma 1. A minimum cost matching that covers every job, as found by line L7, costs no more than this vertex. $\square$

**Lemma 3 (order of the slots).** For machine $i$ and slot $s$, let $p^{\max}_s$ and $p^{\min}_s$ be the largest and the smallest $p_{ij}$ over the jobs $j$ joined to slot $(i, s)$. Then $p^{\max}_{s+1} \le p^{\min}_s$ for $1 \le s < k_i$, and $p^{\max}_1 \le T$.

*Proof.* Let $j_t$ be a job joined to slot $s + 1$ and $j_{t'}$ a job joined to slot $s$. Then $I_t$ meets $[s, s + 1)$ and $I_{t'}$ meets $[s - 1, s)$. If $t < t'$, then $I_t$ lies to the left of $I_{t'}$, so each point of $I_t$ is less than each point of $I_{t'}$; but $I_t$ has a point at least $s$ and $I_{t'}$ has a point less than $s$, a contradiction. So $t \ge t'$, and the order of line L5 gives $p_{i j_t} \le p_{i j_{t'}}$. Taking the largest $p_{ij_t}$ over the jobs in slot $s + 1$ and the smallest $p_{i j_{t'}}$ over the jobs in slot $s$ gives the first claim. Each joined job has $x_{ij} > 0$, so $p_{ij} \le T$ by the filter in the LP, which gives the second claim. $\square$

**Lemma 4 (load).** In the assignment $\sigma$ of line L8, each machine $i$ has load at most $T + p^{\max}_1 \le T + \max \{ p_{ij} : x_{ij} > 0 \} \le 2T$.

*Proof.* The matching gives machine $i$ at most one job in each of its slots, and the job in slot $s$ has time at most $p^{\max}_s$. So, by Lemma 3,

$$\text{load}_i \le \sum_{s=1}^{k_i} p^{\max}_s \le p^{\max}_1 + \sum_{s=1}^{k_i - 1} p^{\max}_{s+1} \le p^{\max}_1 + \sum_{s=1}^{k_i - 1} p^{\min}_s.$$

For $s < k_i$, slot $s$ is full by Lemma 1, and each job in it has time at least $p^{\min}_s$, so $p^{\min}_s = p^{\min}_s \sum_j z_{j,(i,s)} \le \sum_j p_{ij} z_{j,(i,s)}$. Summing over $s < k_i$ and then adding the nonnegative terms of slot $k_i$,

$$\sum_{s=1}^{k_i - 1} p^{\min}_s \le \sum_{s=1}^{k_i} \sum_j p_{ij} z_{j,(i,s)} = \sum_j p_{ij} x_{ij} \le T,$$

where the equality uses Lemma 1 on machine $i$ and the last step is the load row of the LP. With $p^{\max}_1 \le T$ from Lemma 3, the load is at most $2T$. $\square$

**Theorem.** If the LP with target $T$ is feasible, SHMOYS-TARDOS-GAP returns an assignment of every job with cost at most the LP value and with each load at most $T + \max_j \{ p_{ij} : x_{ij} > 0 \} \le 2T$. The LP value is at most the cost $C$ of each assignment with all loads at most $T$, so the cost is at most $C$.

*Proof.* Line L1 gives an optimal $x$, and Lemmas 2 and 4 bound the cost and the loads of the result of lines L7 and L8. Each assignment $\sigma^*$ with loads at most $T$ gives a feasible LP point $x_{ij} = [\sigma^*(j) = i]$: each job has total 1, each machine has load at most $T$, and no job is on a machine with $p_{ij} > T$, since its load would then exceed $T$. So the LP value is at most the cost of $\sigma^*$. If the LP is infeasible, no assignment has loads at most $T$, and line L2 reports this correctly. $\blacksquare$

**Remark (tightness of the analysis).** Take $k \ge 2$ machines, a long job with $p_{i0} = k$ on every machine, and for each machine $i$ a set of $k - 1$ unit jobs with time 1 on $i$ and time greater than $k$ elsewhere. With $T = k$, the point that puts $1/k$ of the long job and all its own unit jobs on each machine is feasible, with each load $k - 1 + 1 = k$. Each integral assignment puts the long job on some machine with its $k - 1$ unit jobs, a load of $2k - 1 = (2 - 1/k) T$. So no rounding of this LP can guarantee loads below $(2 - 1/k) T$.
