---
title: An exchange proof that SRPT minimizes the total completion time
proves: [statement]
status: full
---

**Model.** There is one machine of speed 1 and a finite set of jobs. Job $j$ has release time $r_j \ge 0$ and processing time $p_j > 0$. A *schedule* is a finite set of disjoint time intervals, the *pieces*, each assigned to one job $j$ and contained in $[r_j, \infty)$, such that the pieces of job $j$ have total length $p_j$. The completion time $C_j$ is the right end of the last piece of $j$. We write $q_k(S, t)$ for the work of job $k$ that schedule $S$ has not done by time $t$.

**Theorem.** For each schedule $S$, $\sum_j C_j(\text{SRPT}) \le \sum_j C_j(S)$. Since $\sum_j F_j = \sum_j C_j - \sum_j r_j$, the same holds for the total flow time.

## The events

Let $e_0 < e_1 < \dots < e_K$ be the distinct values in $\{0\} \cup \{r_j\} \cup \{C_j(\text{SRPT})\}$. Let $T_i = [e_i, e_{i+1})$ for $i < K$. SRPT changes its decision only at a release or at a completion, so on each $T_i$ SRPT either idles all the time or runs one job $j$ all the time. In the second case $j$ does not complete before $e_{i+1}$, so

$$L_i = e_{i+1} - e_i \le q_j(\text{SRPT}, e_i). \qquad (1)$$

No job is released in the open interval $(e_i, e_{i+1})$, because each release time is an event. After $e_K$, all jobs are complete under SRPT.

## The induction

**Claim.** For each $i \le K$, there is a schedule $S_i$ with $\sum_j C_j(S_i) \le \sum_j C_j(S)$ that is equal to SRPT on $[0, e_i)$: at each time in $[0, e_i)$, both run the same job or both idle.

For $i = 0$, take $S_0 = S$. For $i = K$, the schedule $S_K$ does in $[0, e_K)$ exactly the work of SRPT, which is all the work. So $S_K$ has no piece after $e_K$, it is equal to SRPT, and $\sum_j C_j(\text{SRPT}) = \sum_j C_j(S_K) \le \sum_j C_j(S)$. This proves the theorem. It remains to go from $i$ to $i + 1$.

Let $S = S_i$. Because $S$ and SRPT are equal on $[0, e_i)$, they have the same remaining work at $e_i$. Write $q_k = q_k(S, e_i) = q_k(\text{SRPT}, e_i)$.

**Case 1: SRPT idles on $T_i$.** Then each job with $r_k \le e_i$ has $q_k = 0$, and no job is released in $(e_i, e_{i+1})$. So $S$ has no job to run on $T_i$ and idles there too. Take $S_{i+1} = S$.

**Case 2: SRPT runs job $j$ on $T_i$.** Let $k \ne j$ be a job that $S$ runs at some time in $T_i$. Then $r_k \le e_i$, because no release falls inside $T_i$ after $e_i$, and $q_k > 0$. SRPT chose $j$ at $e_i$ among the released, unfinished jobs, so

$$q_j \le q_k. \qquad (2)$$

**The exchange of $j$ and $k$.** Let $U$ be the set of times $t \ge e_i$ at which $S$ runs $j$ or $k$. It is a finite union of intervals of total length $q_j + q_k$. Define $S'$ equal to $S$ outside $U$. On $U$, in time order, $S'$ gives the first $q_j$ units of length to $j$ and the rest to $k$. Both jobs are released by $e_i$, so $S'$ is a schedule.

- The part of $U$ before $C_j(S)$ has length at least $q_j$, because $S$ does all remaining work of $j$ inside $U$ by that time. So $C_j(S') \le C_j(S)$. In the same way, the part of $U$ before $C_k(S)$ has length at least $q_k$, and $q_k \ge q_j$ by (2), so $C_j(S') \le C_k(S)$. Hence $C_j(S') \le \min(C_j(S), C_k(S))$.
- The last piece of $U$ goes to $k$, so $C_k(S') = \max(C_j(S), C_k(S))$.
- The other jobs keep their pieces and their completion times.

So $C_j(S') + C_k(S') \le C_j(S) + C_k(S)$, and the sum of all completion times does not increase.

The part of $U$ inside $T_i$ has length at most $L_i \le q_j$ by (1). It comes first in time order, so $S'$ gives all of it to $j$. Thus $S'$ does not run $k$ in $T_i$, it runs $j$ wherever $S$ ran $j$ or $k$ in $T_i$, and it does not change $[0, e_i)$ or the pieces of other jobs in $T_i$.

**Repeat.** Each exchange removes one job other than $j$ from $T_i$ and adds none. After at most $n - 1$ exchanges, we have a schedule $S''$ that equals SRPT on $[0, e_i)$, does not increase the sum, and runs only $j$ in $T_i$ or idles.

**Fill the idle time.** Let $I \subseteq T_i$ be the idle part of $S''$ in $T_i$, of length $\delta$. Job $j$ runs for $L_i - \delta$ in $T_i$, so its work after $e_{i+1}$ is $q_j - (L_i - \delta) \ge \delta$ by (1). Move the first $\delta$ units of this later work of $j$ into $I$. This is allowed because $r_j \le e_i$. The completion time of $j$ does not increase, and no other job changes. The result $S_{i+1}$ runs $j$ on all of $T_i$, so it equals SRPT on $[0, e_{i+1})$, and $\sum_j C_j(S_{i+1}) \le \sum_j C_j(S)$.

Each step keeps the number of pieces finite, so each $S_i$ is a schedule in the sense of the model. This proves the claim and the theorem. $\blacksquare$
