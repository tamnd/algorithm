---
title: Sorted-Balance is feasible and has makespan at most (3/2 - 1/(2m)) OPT
proves: [correctness]
status: full
---

We use the pseudocode of the page. After line L1, the sizes are $p_1 \ge p_2 \ge \cdots \ge p_n \ge 0$, and $m \ge 1$ is the number of machines. $\mathrm{OPT}$ is the optimal makespan and $\mathrm{ALG} = \max_i T_i$ at line L7. The proofs below are full.

**Lemma 1 (feasibility).** At line L7, the sets $A(1), \ldots, A(m)$ are a partition of $\{1, \ldots, n\}$, and $T_i = \sum_{j \in A(i)} p_j$ for each $i$.

*Proof.* Line L2 makes every set empty and every load $0$. Each round of line L3 adds job $j$ to exactly one set at line L5 and adds $p_j$ to the load of the same machine at line L6. So after round $j$, the sets partition $\{1, \ldots, j\}$ and each load is the sum of its set. $\square$

**Lemma 2 (the pair bound).** If $n \ge m + 1$, then $\mathrm{OPT} \ge 2 p_{m+1}$.

*Proof.* The jobs $1, \ldots, m + 1$ are on $m$ machines in an optimal schedule, so two of them, say $j$ and $k$, share a machine. Its load is at least $p_j + p_k \ge 2 p_{m+1}$, because $j, k \le m + 1$ and the sizes are sorted. $\square$

**Theorem.** $\mathrm{ALG} \le \left(\frac32 - \frac1{2m}\right)\mathrm{OPT}$.

*Proof.* If $n = 0$, both sides are $0$. Otherwise let $i$ be a machine with $T_i = \mathrm{ALG}$ at line L7, let $l$ be the last job that line L5 put on $i$, and let $s$ be the load of $i$ just before job $l$. Then $\mathrm{ALG} = s + p_l$.

*Case $s = 0$.* Then $\mathrm{ALG} = p_l \le \max_j p_j \le \mathrm{OPT}$, by the largest job bound of [makespan lower bounds](/makespan-lower-bounds/).

*Case $s > 0$.* Line L4 chose $i$ with the smallest load, so before job $l$ every machine had load at least $s > 0$, and so every machine had at least one of the jobs $1, \ldots, l - 1$. Hence $l - 1 \ge m$, so $l \ge m + 1$, $n \ge m + 1$, and $p_l \le p_{m+1}$ by the order. Lemma 2 gives $p_l \le \mathrm{OPT}/2$.

The smallest of the $m$ loads before job $l$ is at most their mean, and these loads add up to $\sum_{k < l} p_k \le \sum_k p_k - p_l$. So

$$\mathrm{ALG} = s + p_l \le \frac1m \sum_{k} p_k + \Big(1 - \frac1m\Big) p_l \le \mathrm{OPT} + \Big(1 - \frac1m\Big)\frac{\mathrm{OPT}}{2} = \Big(\frac32 - \frac1{2m}\Big)\mathrm{OPT},$$

where the middle step uses the average load bound $\frac1m \sum_k p_k \le \mathrm{OPT}$.

In both cases the bound holds, since $\frac32 - \frac1{2m} \ge 1$. $\blacksquare$

**The analysis is not tight.** Sorted-Balance is the [LPT](/longest-processing-time-first/) rule, so the stronger bound $\mathrm{ALG} \le (\frac43 - \frac1{3m})\,\mathrm{OPT}$ of [the LPT bound](/lpt-bound/) also holds. For $m = 2$ the bound above is $\frac54$, while the worst case is $\frac76$, reached by $p = (3, 3, 2, 2, 2)$: the algorithm gives loads $7$ and $5$, and the optimum is $6$.
