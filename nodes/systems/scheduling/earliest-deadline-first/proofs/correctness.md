---
title: EDF runs the earliest deadline, and the utilization and processor demand tests are exact
proves: [correctness]
status: full
---

We use the notation of the page. A job is *pending* at time $t$ if it is released by $t$ and has work left.

**Lemma 1 (the loop).** In each run of line L8, in the interval $[t, t + \delta)$, the job $j$ has the earliest deadline among the pending jobs, by the tie rule of the heap.

*Proof.* Line L5 moves each job with $r \le t$ into $Q$, and line L9 removes a job only when its work is 0, so $Q$ holds exactly the pending jobs at $t$. Line L6 takes the top of $Q$. By line L7, $t + \delta$ is at most the next release, so no job becomes pending inside the interval. The other jobs in $Q$ do not run, so their keys and their membership do not change. Each round either ends a job or reaches a release, so the loop stops after at most $2k$ rounds. $\square$

So the loop builds the EDF schedule. The rest of the proof is about the tests. Let $h$ be the demand bound function of the page, for sporadic tasks $(C_i, T_i, D_i)$ with any deadlines.

**Lemma 2 (necessity).** If $h(t) > t$ for some $t > 0$, then no schedule meets all deadlines of the synchronous release pattern.

*Proof.* In the synchronous pattern, task $\tau_i$ releases jobs at $0, T_i, 2T_i, \ldots$, and the jobs with deadline at most $t$ are those with $k T_i + D_i \le t$, so there are $\max(0, \lfloor (t - D_i)/T_i \rfloor + 1)$ of them, each with work $C_i$. All of them are released at or after 0 and must end by $t$, so a schedule that meets all deadlines does $h(t)$ units of work in $[0, t]$. One processor does at most $t$ units in that interval. $\square$

**Lemma 3 (sufficiency).** If $h(t) \le t$ for each $t > 0$, then EDF meets all deadlines for each legal release pattern: the releases of $\tau_i$ are at least $T_i$ apart, and each job of $\tau_i$ needs at most $C_i$.

*Proof.* Assume that EDF misses a deadline, and let $d$ be the deadline of a job $J$ that is pending at $d$. The EDF schedule is a finite list of pieces up to $d$. Let $t_0$ be the end of the last piece before $d$ in which the processor is idle or runs a job with a deadline after $d$; if there is no such piece, let $t_0 = 0$.

In $[t_0, d)$ the processor is busy all the time and runs only jobs with deadlines at most $d$. No job with a deadline at most $d$ and a release before $t_0$ is pending at $t_0$. If $t_0 = 0$, this is clear. If the processor is idle just before $t_0$, no job is pending then. If it runs a job with a deadline after $d$ just before $t_0$, a pending job with a deadline at most $d$ would have a higher priority by Lemma 1. So each job that runs in $[t_0, d)$ has its release in $[t_0, d)$ and its deadline at most $d$. The same is true for $J$: it is pending at each time from its release to $d$, so a release before $t_0$ is not possible. The work of these jobs is more than $d - t_0$: the processor does $d - t_0$ units of their work, and $J$ still has work left.

Fix a task $\tau_i$. Its jobs with release at least $t_0$ and deadline at most $d$ have releases in $[t_0, d - D_i]$, at least $T_i$ apart, so there are at most $\max(0, \lfloor (d - t_0 - D_i)/T_i \rfloor + 1)$ of them, each with work at most $C_i$. The sum over the tasks gives a total work of at most $h(d - t_0)$. Thus $h(d - t_0) > d - t_0$, with $d - t_0 > 0$. This contradicts the assumption. $\square$

**Theorem 1 (processor demand criterion).** A sporadic or synchronous periodic task system is feasible on one preemptive processor if and only if $h(t) \le t$ for each $t > 0$, and then EDF meets all deadlines.

*Proof.* Lemmas 2 and 3. $\blacksquare$

**Corollary (implicit deadlines).** If $D_i = T_i$ for each $i$, EDF meets all deadlines if and only if $U \le 1$.

*Proof.* For $t > 0$, $h(t) = \sum_i \lfloor t / T_i \rfloor C_i \le \sum_i (t / T_i) C_i = tU$. If $U \le 1$, then $h(t) \le t$, and Theorem 1 applies. If $U > 1$ and the periods are integers, then $h(H) = \sum_i (H / T_i) C_i = HU > H$, and Lemma 2 applies. For real periods, $h(t) \ge tU - \sum_i C_i > t$ for each large $t$. $\blacksquare$

**Theorem 2 (the points to check).** Let $D_i \le T_i$ for each $i$, with integer periods, and let $U \le 1$. If $h(t) > t$ for some $t > 0$, then there is an absolute deadline $t' = k T_i + D_i$ with $h(t') > t'$ and $t' \le L$, where $L = H$ if $U = 1$ and $L = \min(H, L_a)$ if $U < 1$.

*Proof.* For $t \ge 0$ and $D_i \le T_i$, $\lfloor (t - D_i)/T_i \rfloor + 1 \ge \lfloor -1 \rfloor + 1 = 0$, so the maximum with 0 has no effect. Then $H / T_i$ is an integer, and $h(t + H) = h(t) + \sum_i (H / T_i) C_i = h(t) + HU$. So $h(t + H) - (t + H) = h(t) - t - H(1 - U) \le h(t) - t$. If $t > H$ violates the test, then $t - H > 0$ does too. By repetition, the least violating $t$ is at most $H$. (The least one exists, because $h$ is a step function that changes only at absolute deadlines.)

If $U < 1$, each violating $t$ satisfies

$$t < h(t) \le \sum_i \left(\frac{t - D_i}{T_i} + 1\right) C_i = tU + \sum_i (T_i - D_i)\, U_i,$$

so $t(1 - U) < \sum_i (T_i - D_i) U_i$ and $t < L_a$.

Let $t$ be the least violating value. Then $t \le L$. The function $h$ is constant between two absolute deadlines and 0 before the first one. Let $t'$ be the largest absolute deadline at most $t$; it exists, because $h(t) > 0$. Then $h(t') = h(t) > t \ge t'$. $\blacksquare$

The function `processor_demand_test` returns false when $U > 1$, which is correct by Lemma 2 at $t = H$. Otherwise it checks $h(t') \le t'$ at each absolute deadline $t' \le L$, which is correct by Theorem 2.
