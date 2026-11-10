---
title: SRPT follows its rule and minimizes the total flow time on one machine
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The jobs are $(r_j, p_j)$ with $r_j \ge 0$ and $p_j > 0$, on one machine of speed 1. A schedule is a finite set of pieces $[a, b)$, each assigned to one released job, with disjoint pieces and $p_j$ units of work for job $j$.

## Part 1. The loop computes the SRPT schedule

**Invariant (H).** At the test of line L2, the heap $H$ holds exactly the jobs with $r_j \le t$ (in the sorted order, the first $i$ jobs) that are not complete, each with its remaining work at time $t$. The schedule built so far covers $[0, t)$ and follows the SRPT rule there.

At the start, $t = 0$, $i = 0$ and $H$ is empty, so (H) is true. Assume (H) at the test. If $H$ is empty, no released job is waiting, so SRPT idles until the next release, and line L3 moves $t$ to it. Line L4 then inserts each job with $r_j \le t$, so $H$ holds all released unfinished jobs. Line L5 removes the job $j$ with the least remaining work $q$, which is the job that SRPT runs at time $t$. Let $\mathit{next}$ be the next release after the jobs in $H$ (line L6). No job arrives in $(t, \mathit{next})$, so the set of waiting jobs changes there only when $j$ completes. While $j$ runs, its remaining work drops and the others stay the same, so $j$ keeps the least remaining work. Hence SRPT runs $j$ on $[t, \min(t + q, \mathit{next}))$.

- If $t + q \le \mathit{next}$, line L7 completes $j$ at $t + q$ and moves $t$ there. The heap holds the other waiting jobs with unchanged remaining work.
- Else line L8 puts $j$ back with remaining work $q - (\mathit{next} - t)$ and moves $t$ to $\mathit{next}$. The next pass of line L4 inserts the new jobs, and line L5 picks the least remaining work again, so a new job preempts $j$ exactly when its work is smaller.

In both cases (H) holds again.

**Termination.** Each pass either completes a job at line L7, or reaches line L8 and moves $t$ to a release, after which line L4 of the next pass inserts at least one job. There are $n$ completions and $n$ insertions, so the loop runs at most $2n$ times. When it stops, $i = n$ and $H$ is empty, so each job is complete. $\square$

## Part 2. SRPT minimizes the total flow time

Fix any schedule $S$ on one machine of speed 1, online or not. At time $t$, let $R_S(t)$ be the multiset of the remaining work of the jobs with $r_j \le t$, where a complete job counts as $0$. Its size $m(t)$ is the number of released jobs, the same in every schedule. For $1 \le k \le m(t)$, let $P_k(S, t)$ be the sum of the $k$ smallest elements of $R_S(t)$.

**Lemma.** For each $t$ and each $k \le m(t)$, $P_k(\text{SRPT}, t) \le P_k(S, t)$.

*Proof.* Two facts about a multiset $A$ of non-negative numbers and the sums $P_k(A)$ of its $k$ smallest elements:

1. If one element of $A$ drops by $\delta \ge 0$ (and stays $\ge 0$), then $P_k$ drops by at most $\delta$. Take the $k$ smallest elements of the new multiset. The same elements of the old multiset have a sum of at most the new $P_k$ plus $\delta$, so the old $P_k$ is at most the new $P_k$ plus $\delta$.
2. If an element $x$ is added, then $P_k(A \cup \{x\}) = \min(P_k(A), P_{k-1}(A) + x)$, with $P_0 = 0$ and $P_k(A) = +\infty$ for $k > |A|$. The $k$ smallest elements of $A \cup \{x\}$ either omit $x$, or contain $x$ and the $k - 1$ smallest of $A$. This formula is non-decreasing in $P_k(A)$ and in $P_{k-1}(A)$.

Let $e_1 < e_2 < \dots$ be the distinct release times. Before $e_1$, both multisets are empty. At a release time, add the new jobs one at a time. By fact 2, the inequality for each $k$ before the release gives it for each $k$ after the release, because both schedules add the same values $p_j$.

Now take an interval $[e_i, e_{i+1})$ with no release inside, and fix $k$. Let $D(t) = P_k(\text{SRPT}, t) - P_k(S, t)$. It is continuous on the interval, because the remaining work of each job is continuous in $t$ between releases, and $D(e_i) \le 0$. Assume $D(t') > 0$ for some $t'$ in the interval, and let $t_0$ be the last time in $[e_i, t']$ with $D(t_0) \le 0$. On $(t_0, t']$, $P_k(\text{SRPT}, t) > P_k(S, t) \ge 0$. So SRPT has fewer than $k$ zero elements, and at least one released job is unfinished. SRPT then runs the unfinished job with the least remaining work, which is among its $k$ smallest elements, and it stays the least positive element while it runs. So on each subinterval $[u, v]$ of $(t_0, t']$, $P_k(\text{SRPT})$ drops by exactly $v - u$. In $S$, at most one job runs at a time at speed 1, so by fact 1, $P_k(S)$ drops by at most $v - u$. Hence $D$ does not increase on $(t_0, t']$, and by continuity $D(t') \le D(t_0) \le 0$. This is a contradiction, so $D \le 0$ on the whole interval. $\square$

**Theorem.** At each time $t$, the number $N(t)$ of released, unfinished jobs satisfies $N_{\text{SRPT}}(t) \le N_S(t)$. So $\sum_j F_j(\text{SRPT}) \le \sum_j F_j(S)$, and $\sum_j C_j(\text{SRPT}) \le \sum_j C_j(S)$.

*Proof.* The number of complete jobs at time $t$ is the number $z$ of zeros in $R(t)$, and it is the largest $k$ with $P_k = 0$. If $P_k(S, t) = 0$, then the lemma gives $P_k(\text{SRPT}, t) = 0$. So SRPT has at least as many complete jobs as $S$, and $N_{\text{SRPT}}(t) = m(t) - z_{\text{SRPT}}(t) \le m(t) - z_S(t) = N_S(t)$. The total flow time is $\int_0^\infty N(t) \, dt$ (see [flow time](/flow-time/)), so it is at most the one of $S$. The total completion time differs from the total flow time by $\sum_j r_j$, which does not depend on the schedule. $\blacksquare$

The theorem shows more than optimality of the sum: for each $k$, the $k$-th completion of SRPT is no later than the $k$-th completion of any other schedule. A second proof, by an exchange argument, is on the [SRPT optimality](/srpt-optimality/) page.
