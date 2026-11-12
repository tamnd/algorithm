---
tag: 2AB190
kind: theorem
slug: rate-monotonic-optimality
name: Optimality of rate-monotonic priorities
aliases:
- critical instant theorem
- optimality of the rate-monotonic priority assignment
area: systems/scheduling
level: advanced
summary: "For periodic or sporadic tasks with deadlines equal to periods on one processor, if any fixed priority order meets all deadlines, the rate-monotonic order does too."
prereqs: [rate-monotonic-scheduling, exchange-argument]
see_also: [rate-monotonic-scheduling, deadline-monotonic-scheduling, response-time-analysis, liu-layland-utilization-bound, fixed-priority-scheduling, edf-optimality, sporadic-task-model]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the theorem on the critical instant of a task, and the theorem that the rate-monotonic priority assignment is optimal among fixed priority assignments
  - paper: "Joseph Y.-T. Leung and Jennifer Whitehead, On the complexity of fixed-priority scheduling of periodic, real-time tasks, Performance Evaluation 2(4) (1982), 237-250"
    locator: the optimality of the deadline-monotonic priority assignment for deadlines at most the periods
  - paper: "Mathai Joseph and Paritosh Pandya, Finding response times in a real-time system, The Computer Journal 29(5) (1986), 390-395"
    locator: the response time as the least solution of the recurrence
  - paper: "John P. Lehoczky, Fixed priority scheduling of periodic task sets with arbitrary deadlines, Proceedings of the 11th IEEE Real-Time Systems Symposium, 1990"
    locator: the busy period analysis for deadlines after the periods, where the first job is not always the worst
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (the optimality of rate monotonic and deadline monotonic priorities)
---

The optimality theorem for [rate-monotonic scheduling](/rate-monotonic-scheduling/) says that, on one preemptive processor, if some fixed priority order meets all deadlines of a set of periodic or sporadic tasks with deadlines equal to periods, then the rate-monotonic order (shortest period first) meets them too. Its proof rests on the critical instant theorem: a task meets its worst response time when it releases a job together with all tasks of higher priority. Both are due to Liu and Layland (1973). The same proof shows that the deadline-monotonic order is optimal when each deadline is at most the period.

## Statement

Let $\tau = \{\tau_1, \ldots, \tau_n\}$ be a set of independent tasks $\tau_i = (C_i, T_i, D_i)$ with $D_i \le T_i$, on one processor with preemption at any time and no overheads. The tasks are [sporadic](/sporadic-task-model/): releases of $\tau_i$ are at least $T_i$ apart, and each job needs at most $C_i$. Synchronous periodic tasks are a special case. A *fixed priority order* is a total order of the tasks; at each time the processor runs the pending job of the task that is first in the order, and jobs of one task run in release order. Write $hp(k)$ for the set of tasks before $\tau_k$, and let

$$W_k(t) = C_k + \sum_{j \in hp(k)} \left\lceil \frac{t}{T_j} \right\rceil C_j, \qquad R_k = \min\{ t > 0 : W_k(t) \le t \}$$

($R_k = \infty$ if no such $t$ exists).

**Theorem 1 (critical instant).** Fix a priority order. If $R_k \le T_k$, then each job of $\tau_k$, in each legal release pattern, ends at most $R_k$ after its release. In the synchronous pattern (all tasks release at 0 and then every $T_j$, with execution time $C_j$), the first job of $\tau_k$ ends exactly at $R_k$. If $R_k = \infty$, the first job of $\tau_k$ in the synchronous pattern never ends.

So $\tau_k$ meets all its deadlines under the order if and only if $R_k \le D_k$.

**Theorem 2 (optimality).** If some fixed priority order meets all deadlines of $\tau$, then each *deadline-monotonic* order (by $D_i$, smallest first, ties in any way) meets them. For implicit deadlines ($D_i = T_i$) this is the *rate-monotonic* order.

## In plain words

Think of the worst moment for a task: the moment when it starts a new job and, at the same time, every more important task starts a new job too. Then all the important work comes at once, and later releases add more. The first part of the theorem says that no other moment is worse. So it is enough to check this one moment for each task.

The second part says how to rank the tasks. Suppose some ranking works. If two neighbors in the ranking are in the wrong order, the one with the later deadline above the one with the earlier deadline, swapping them keeps every deadline. Repeat the swaps until the ranking is sorted by deadline. When each deadline equals the period, sorted by deadline is sorted by period, which is the rate-monotonic ranking.

## Proof

Fix a priority order and a task $\tau_k$. Tasks after $\tau_k$ never run while a job of $\tau_k$ or of $hp(k)$ is pending, so we can ignore them. A job is *pending* at time $t$ if it is released by $t$ and has work left. The schedule up to any time has finitely many pieces.

**Lemma 1 (the synchronous case).** In the synchronous pattern, the first job of $\tau_k$ ends at $R_k$, or never if $R_k = \infty$.

*Proof.* Let $f$ be the finish time of the first job $J$ of $\tau_k$ ($f = \infty$ if it never ends). At each time in $[0, f)$, $J$ is pending, so the processor runs $J$ or a job of $hp(k)$; a later job of $\tau_k$ waits for $J$.

Take $0 < t < f$ and assume $W_k(t) \le t$. In $[0, t)$ the processor is busy and runs only $J$ and jobs of $hp(k)$ released before $t$; their total work is $W_k(t)$, since task $\tau_j$ releases $\lceil t / T_j \rceil$ jobs in $[0, t)$. The processor does $t \ge W_k(t)$ units of this work in $[0, t)$, so all of it is done by $t$, and $J$ ends by $t < f$. This is a contradiction, so $W_k(t) > t$ for each $t \in (0, f)$. If $f = \infty$, then $R_k = \infty$.

If $f < \infty$, in the last piece before $f$ the processor runs $J$, so no job of $hp(k)$ is pending then. Each job of $hp(k)$ released before $f$ is thus done by $f$. In $[0, f)$ the processor does exactly the work of $J$ and of these jobs, without idling, so $W_k(f) = f$. Hence $f = R_k$. $\square$

**Lemma 2 (any pattern).** Assume $R_k \le T_k$. In each legal release pattern, each job of $\tau_k$ ends at most $R_k$ after its release.

*Proof.* By induction over the jobs of $\tau_k$ in release order. Let $J$ be a job of $\tau_k$ released at $r$ and ending at $f_J$, and assume the claim for the earlier jobs of $\tau_k$. Each earlier job is released at most at $r - T_k$, so it ends by $r - T_k + R_k \le r$. So from $r$ on, $J$ waits only for jobs of $hp(k)$.

Let $t_0$ be the latest time $s \le r$ such that no job of $hp(k)$ released before $s$ is pending at $s$. The time $s = 0$ has this property, and the schedule has finitely many pieces, so $t_0$ exists. By the choice of $t_0$, at each time in $(t_0, r]$ a job of $hp(k)$ is pending, so the processor runs jobs of $hp(k)$ in $[t_0, r)$. At each time in $[r, f_J)$, $J$ is pending, so the processor runs $J$ or jobs of $hp(k)$. No job of $hp(k)$ released before $t_0$ is pending at $t_0$. So in $[t_0, f_J)$ the processor is busy all the time and runs only $J$ and jobs of $hp(k)$ released at or after $t_0$.

Assume that $f_J - r > R_k$, and let $t' = t_0 + R_k$. Then $t' \le r + R_k < f_J$. In a window $[t_0, t')$ of length $R_k$, task $\tau_j$ releases at most $\lceil R_k / T_j \rceil$ jobs, because its releases are at least $T_j$ apart. Each needs at most $C_j$.

- If $t' > r$: in $[t_0, t')$ the processor does $R_k$ units of work of $J$ and of the jobs of $hp(k)$ released in $[t_0, t')$. $J$ is not done at $t'$, so the total work of these jobs is more than $R_k$. It is at most $W_k(R_k)$, so $W_k(R_k) > R_k$.
- If $t' \le r$: in $[t_0, t')$ the processor does $R_k$ units of work of jobs of $hp(k)$ released in $[t_0, t')$, and at $t'$ one of these jobs is still pending, by the choice of $t_0$. So their total work is more than $R_k$, and again $W_k(R_k) \ge C_k + (\text{that work}) > R_k$.

Both cases contradict $W_k(R_k) \le R_k$. So $f_J - r \le R_k$. $\square$

*Proof of Theorem 1.* Lemma 2 gives the bound, and Lemma 1 shows that the synchronous pattern reaches it. If $R_k \le D_k \le T_k$, each job of $\tau_k$ meets its deadline. If $R_k > D_k$, the first job of $\tau_k$ in the synchronous pattern, which is a legal pattern, ends after $D_k$ by Lemma 1. $\blacksquare$

*Proof of Theorem 2.* By Theorem 1, an order meets all deadlines if and only if $R_i \le D_i$ for each $i$, where $R_i$ depends only on the set $hp(i)$. Take an order that meets all deadlines. If it is not deadline-monotonic, it has two neighbors $\tau_a$ directly before $\tau_b$ with $D_a > D_b$. Swap them, and let $R'$ be the new values.

- For each task other than $\tau_a$ and $\tau_b$, the set of tasks before it is the same, so $R'_i = R_i \le D_i$.
- The task $\tau_b$ loses $\tau_a$ from its set, so $W'_b \le W_b$ at each $t$, and $R'_b \le R_b \le D_b$.
- The task $\tau_a$ gains $\tau_b$. Let $P$ be the set of tasks before $\tau_a$ in the old order. Since $R_b \le D_b < D_a \le T_a$ and $R_b \le D_b \le T_b$, both $\lceil R_b / T_a \rceil$ and $\lceil R_b / T_b \rceil$ are 1. So
$$W'_a(R_b) = C_a + C_b + \sum_{j \in P} \left\lceil \frac{R_b}{T_j} \right\rceil C_j = W_b(R_b) \le R_b,$$
and $R'_a \le R_b \le D_b < D_a$.

So the new order meets all deadlines, and it has one pair fewer in the wrong order by deadline. After finitely many swaps, as in bubble sort, the order is deadline-monotonic. Two deadline-monotonic orders differ only among tasks with equal deadlines, and the same swap, with $D_a = D_b$, moves from one to the other. For $D_i = T_i$, the deadline-monotonic orders are the rate-monotonic orders. $\blacksquare$

## Consequences

- **Exact test.** A fixed-priority task set is schedulable if and only if $R_k \le D_k$ for each $k$; [response-time analysis](/response-time-analysis/) computes $R_k$ by a fixed-point iteration from $R = C_k$. A simulation of the synchronous release up to the first completion of each task gives the same answer.
- **Sporadic equals synchronous.** A sporadic task set with $D_i \le T_i$ is schedulable under a fixed order exactly when the synchronous periodic set with the same parameters is.
- **Deadline-monotonic optimality.** For $D_i \le T_i$, the [deadline-monotonic](/deadline-monotonic-scheduling/) order is optimal among fixed priorities (Leung and Whitehead 1982).
- **The utilization bound.** The [Liu-Layland bound](/liu-layland-utilization-bound/) is proved for the rate-monotonic order; by Theorem 2 it then holds for the best fixed order too.
- **The worst case is known.** A fixed-priority analysis needs no search over release patterns on one processor.

## Tightness

- **Fixed versus dynamic priorities.** Theorem 2 compares fixed orders only. For $\tau_1 = (2, 5)$ and $\tau_2 = (4, 7)$ with implicit deadlines, both fixed orders miss a deadline, but [earliest deadline first](/earliest-deadline-first/), which is [optimal on one processor](/edf-optimality/), meets all.
- **Rate-monotonic with shorter deadlines.** For $(C, T, D) = (2, 10, 2)$ and $(1, 5, 5)$, the rate-monotonic order puts the second task first, and the first task ends at 3, after its deadline 2. The deadline-monotonic order meets both deadlines.
- **Deadlines after the periods.** The assumption $R_k \le T_k$ is needed: with $D_i > T_i$, several jobs of one task can be pending at once, the first job is not always the worst, and the deadline-monotonic order is not always optimal. For $(2, 4, 6)$ and $(4, 8, 7)$, deadline-monotonic priorities make the second task end at 8, after 7, but the other order meets all deadlines. Audsley's algorithm finds an order in this case.
- **Fixed offsets.** If the offsets are fixed and the synchronous release never happens, Theorem 1 gives only an upper bound, and the exact test must look at the actual releases.
- **Many processors.** Under global fixed priorities on several processors, the synchronous release is not always the worst case.

## History

Liu and Layland (1973) proved the critical instant theorem and the optimality of the rate-monotonic order for implicit deadlines. Leung and Whitehead (1982) extended the optimality to the deadline-monotonic order for deadlines at most the periods. Joseph and Pandya (1986) gave the response time as the least solution of the recurrence, which turned the critical instant into an exact test. Lehoczky (1990) treated deadlines after the periods, where the critical instant needs a busy period with several jobs of the task.

## References
