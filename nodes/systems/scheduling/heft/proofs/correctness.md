---
title: HEFT computes longest-path ranks and always returns a valid schedule
proves: [correctness]
status: full
---

HEFT is a heuristic, so its correctness has three parts: line L1 computes the ranks that the method defines, the order of line L2 lets every task be placed after its predecessors, and the schedule of lines L3 to L9 respects every constraint. The last section shows that the schedule need not be optimal.

**Setting.** The task graph $G$ is acyclic, with tasks $1, \ldots, n$ and processors $1, \ldots, q$. Times $w_{i,p} \ge 0$ and transfer costs $c_{i,j} \ge 0$. A schedule gives each task $i$ a processor $\pi(i)$ and a start $s_i \ge 0$, with finish $f_i = s_i + w_{i,\pi(i)}$. It is *valid* if (a) for each edge $(j, i)$, $s_i \ge f_j + \delta_{j,i}$, where $\delta_{j,i} = 0$ if $\pi(j) = \pi(i)$ and $c_{j,i}$ otherwise, and (b) two tasks on the same processor run in disjoint intervals $[s, f)$.

**Lemma 1 (ranks).** Line L1 sets $\operatorname{rank}(i)$ to the largest length of a path from $i$ to an exit task, where the length of a path $i = v_0 \to v_1 \to \cdots \to v_r$ is $\sum_{x=0}^{r} \bar w_{v_x} + \sum_{x=1}^{r} c_{v_{x-1}, v_x}$.

*Proof.* By induction along the reverse topological order. When line L1 handles $i$, every successor $j$ has its final rank. A path from $i$ to an exit task is either $i$ alone, if $i$ is an exit task, or the edge $(i, j)$ followed by a path from $j$. The longest such path through $j$ has length $\bar w_i + c_{i,j} + \operatorname{rank}(j)$ by the induction hypothesis, and line L1 takes the maximum over $j$. $\square$

**Lemma 2 (order).** For every edge $(i, j)$, task $i$ comes before task $j$ in the order $\lambda$ of line L2.

*Proof.* By line L1, $\operatorname{rank}(i) \ge \bar w_i + c_{i,j} + \operatorname{rank}(j) \ge \operatorname{rank}(j)$, since all costs are nonnegative. If $\operatorname{rank}(i) > \operatorname{rank}(j)$, the sort by decreasing rank puts $i$ first. If the ranks are equal, the tie is broken by the topological order, in which $i$ comes before $j$. $\square$

**Lemma 3 (gap search).** Let the tasks already on processor $p$ occupy the intervals $[a_1, b_1), \ldots, [a_k, b_k)$, sorted, with $b_l \le a_{l+1}$. Line L6, done as the scan "set $x \leftarrow$ ready; for $l = 1, \ldots, k$: if $x + w \le a_l$, stop; else $x \leftarrow \max(x, b_l)$", returns the least *free* $x \ge$ ready, where $y$ is free if, for every $l$, $y + w \le a_l$ or $y \ge b_l$. For $w > 0$, $y$ is free exactly when $[y, y + w)$ meets no busy interval. For $w = 0$, $y$ is free when it is not strictly inside a busy interval, and the empty interval $[y, y)$ meets nothing in any case.

*Proof.* Before step $l$ the scan keeps two facts: $x \ge \max(\text{ready}, b_{l-1})$ (with $b_0 = 0$), and no $y$ with ready $\le y < x$ is free. Both hold at the start. At step $l$, if $x + w \le a_l$, then $x + w \le a_{l'}$ for every $l' \ge l$, and $x \ge b_{l-1} \ge b_{l'}$ for every $l' < l$, so $x$ is free, and by the second fact it is the least free time. Otherwise $x + w > a_l$. Every $y$ with $x \le y < b_l$ has $y + w > a_l$ and $y < b_l$, so it is not free. So the new value $x = \max(x, b_l)$ keeps both facts. If the scan does not stop, then at the end $x \ge b_k \ge b_l$ for every $l$, so $x$ is free, and it is the least free time by the second fact. $\square$

**Theorem 1 (validity).** HEFT places every task exactly once and returns a valid schedule.

*Proof.* Line L3 takes each task once, and line L8 places it, since line L6 always returns a start by Lemma 3. We show by induction on the steps of line L3 that the placed tasks always form a valid partial schedule, that is, (a) holds for every edge between two placed tasks and (b) holds for every pair of placed tasks.

When task $i$ is handled, all its predecessors are placed by Lemma 2, so line L5 reads only finish times that are set. Line L8 picks a processor $p^*$ with start $s_i = \mathrm{EST}[p^*] \ge \mathrm{ready}$ for $p^*$, which is at least $f_j + \delta_{j,i}$ for each predecessor $j$, with $\delta_{j,i}$ for the processor $p^*$. So (a) holds for every edge into $i$. Successors of $i$ are not placed yet by Lemma 2, so no other edge involves $i$. By Lemma 3, $[s_i, s_i + w_{i,p^*})$ meets none of the intervals already on $p^*$, so (b) holds. Placed tasks never move, so the old constraints still hold. After the last step every task is placed and the schedule is valid. $\square$

**Theorem 2 (the greedy choice).** Given the placement of the tasks before $i$ in $\lambda$, line L8 gives $i$ the least finish time over all processors $p$ and all starts $y \ge$ ready on $p$ that are free in the sense of Lemma 3. When $w_{i,p} > 0$, these starts are exactly the starts on $p$ that keep the partial schedule valid.

*Proof.* On processor $p$, a start $y$ keeps (a) for the edges into $i$ exactly when $y \ge$ ready, as computed by line L5, and for $w_{i,p} > 0$ it keeps (b) exactly when $y$ is free. By Lemma 3 the least such start is $\mathrm{EST}[p]$, so the least finish on $p$ is $\mathrm{EFT}[p]$, and line L8 takes the least of these over $p$. $\square$

**Not optimal.** Theorem 2 is greedy: it does not look at later tasks. Take two processors and three tasks: $t_1$ with times $(4, 3)$, $t_2$ with $(2, 6)$, $t_3$ with $(1, 7)$, edges $t_1 \to t_2$ with cost $2$ and $t_1 \to t_3$ with cost $6$. The ranks are $3.5 + \max(2 + 4, 6 + 4) = 13.5$, $4$ and $4$, so $\lambda = t_1, t_2, t_3$. Line L8 puts $t_1$ on $P_2$, finish $3 < 4$. Then $t_2$ finishes at $\min(3 + 2 + 2,\ 3 + 6) = 7$ on $P_1$, and $t_3$ at $\min(\max(3 + 6, 7) + 1,\ 3 + 7) = 10$, on $P_1$ by the lowest index. The schedule that runs all three tasks on $P_1$ has no transfers and finishes at $4 + 2 + 1 = 7$. No schedule finishes earlier. If $t_1$ runs on $P_2$, it ends at $3$ or later, and $t_2$ ends at $3 + 6 = 9$ or later on $P_2$ and at $3 + 2 + 2 = 7$ or later on $P_1$. If $t_1$ runs on $P_1$, it ends at $4$ or later; then $t_2$ on $P_2$ ends at $4 + 2 + 6 = 12$ or later, $t_3$ on $P_2$ ends at $4 + 6 + 7 = 17$ or later, and with both on $P_1$ that processor has $7$ units of work. So HEFT returns $10$ where $7$ is optimal. $\blacksquare$
