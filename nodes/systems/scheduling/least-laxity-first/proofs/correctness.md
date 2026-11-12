---
title: LLF meets all deadlines of each feasible job set on one processor
proves: [correctness]
status: full
---

We work in the slot model of the page: integer release times $r_j$, works $c_j \ge 1$ and deadlines $d_j$, and a *slot schedule* that runs at most one job in each slot $[t, t + 1)$, runs job $j$ only in slots with $t \ge r_j$, and runs it for exactly $c_j$ slots. It is *feasible* if each job $j$ runs only in slots with $t + 1 \le d_j$. For a schedule $S$ and a slot $t$, let $e_j(t)$ be the work of $j$ not done in the slots before $t$.

**The loop.** Line L3 computes the jobs that may run in slot $t$, and line L5 picks one of them with the least laxity $d_j - t - e_j(t)$; lines L6 and L7 update the remaining work. The loop ends when all work is done, and it runs a job in each slot in which one is ready, so the loop stops after at most $\max_j r_j + \sum_j c_j$ slots.

**Theorem.** If a feasible slot schedule exists, the schedule of LLF, with any tie rule, is feasible.

*Proof.* Let $L$ be the LLF schedule. We show by induction on $t$: for each $t \ge 0$ there is a feasible schedule $S_t$ that agrees with $L$ in all slots before $t$. For $t = 0$, take any feasible schedule. Assume $S = S_t$ is given. Both schedules have run the same jobs before slot $t$, so $e_j(t)$ is the same in both.

*Case 1: $L$ idles in slot $t$.* No job is released and unfinished at $t$, so $S$ idles too. Let $S_{t+1} = S$.

*Case 2: $L$ runs $i$ and $S$ runs $i$.* Let $S_{t+1} = S$.

*Case 3: $L$ runs $i$ and $S$ idles in slot $t$.* Job $i$ has $e_i(t) \ge 1$, so $S$ runs $i$ in some slot $t' > t$ with $t' + 1 \le d_i$. Move this unit of $i$ from slot $t'$ to slot $t$. Job $i$ is released by $t$, and it ends no later than before. Let $S_{t+1}$ be the result.

*Case 4: $L$ runs $i$ and $S$ runs $j \ne i$.* Write $e_i = e_i(t) \ge 1$ and $e_j = e_j(t) \ge 1$. Line L5 picked $i$, so

$$d_i - t - e_i \le d_j - t - e_j. \qquad (*)$$

In $S$, job $i$ runs in exactly $e_i$ slots from $t + 1$ on, all before $d_i$. We claim that one of them, $t'$, has $t' + 1 \le d_j$.

- If $d_i \le d_j$, each of these slots has $t' + 1 \le d_i \le d_j$, and there is at least one.
- If $d_i > d_j$, at most $d_i - d_j$ of the slots lie in $[d_j, d_i)$, so at least $e_i - (d_i - d_j)$ of them have $t' + 1 \le d_j$. By $(*)$, $e_i - (d_i - d_j) \ge e_j \ge 1$.

Swap the contents of slots $t$ and $t'$ in $S$. Job $i$ now runs in slot $t$, where it is released, and it does not end later. Job $j$ now runs in slot $t' > t \ge r_j$, with $t' + 1 \le d_j$; its other slots do not move, so it still ends by $d_j$. All other jobs keep their slots. Let $S_{t+1}$ be the result.

In each case $S_{t+1}$ is feasible and agrees with $L$ in all slots before $t + 1$. Let $T$ be the number of slots of $L$. Then $S_T$ agrees with $L$ on all slots in which $L$ runs a job, and both run all the work, so $S_T$ runs nothing after $T$, and $S_T = L$. So $L$ is feasible. $\blacksquare$

The test `meets_deadlines` compares each finish time from line L7 with its deadline. For a feasible input it returns true by the theorem; if it returns false, the input has no feasible slot schedule, because LLF would have found one.

**Remark.** Case 4 with $d_i \le d_j$ is the exchange step of the optimality proof for [EDF](/edf-optimality/). The laxity rule needs the second bullet, which uses $(*)$.
