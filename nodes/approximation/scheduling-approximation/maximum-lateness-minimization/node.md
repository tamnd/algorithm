---
tag: BNQ857
kind: problem
slug: maximum-lateness-minimization
name: Minimizing maximum lateness
aliases:
- 1||Lmax
- max lateness
- 1|r_j|Lmax
- head-body-tail problem
- one-machine sequencing with delivery times
area: approximation/scheduling-approximation
level: core
summary: Schedule jobs with due dates to minimize the largest lateness max_j (C_j - d_j). EDD solves one machine without release dates; with release dates the problem is strongly NP-hard.
prereqs: [lateness-and-tardiness, scheduling-notation, earliest-due-date-first]
see_also: [earliest-due-date-first, lawler-algorithm, minimizing-maximum-lateness, scheduling-with-release-dates, scheduling-with-release-times-and-deadlines, three-partition, ptas, preemptive-scheduling]
sources:
  - paper: "James R. Jackson, Scheduling a production line to minimize maximum tardiness, Research Report 43, Management Science Research Project, University of California, Los Angeles, 1955"
    locator: the whole report (the EDD rule for 1||Lmax)
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1), 1974"
    locator: pages 177 to 185 (preemptive EDD for 1|r_j,pmtn|Lmax)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (strong NP-hardness of 1|r_j|Lmax)
  - paper: "Chris N. Potts, Analysis of a heuristic for one machine sequencing with release dates and delivery times, Operations Research 28(6), 1980"
    locator: pages 1436 to 1441 (the bound 2 for Schrage's rule and the 3/2 heuristic)
  - paper: "Leslie A. Hall and David B. Shmoys, Jackson's rule for single-machine scheduling, making a good heuristic better, Mathematics of Operations Research 17(1), 1992"
    locator: pages 22 to 35 (the 4/3 algorithm and the PTAS in delivery form)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.1 (1|r_j|Lmax with negative due dates, a 2-approximation)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A5.1, problem SS1 (sequencing with release times and deadlines)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the maximum lateness with and without release dates
---

Minimizing maximum lateness asks for a schedule whose worst [lateness](/lateness-and-tardiness/) $L_{\max} = \max_j (C_j - d_j)$ is as small as possible. On one machine with all jobs available at time 0, written $1 \| L_{\max}$, the [EDD rule](/earliest-due-date-first/) is optimal, and [Lawler's algorithm](/lawler-algorithm/) adds precedence constraints. With release dates, $1 \mid r_j \mid L_{\max}$ is strongly NP-hard, but it becomes easy again with preemption. Because $L_{\max}$ can be zero or negative, approximation results are stated for an equivalent form with delivery times, where Schrage's rule gives a factor 2 and a PTAS exists.

## In plain words

Each job has a due date. When a job finishes, its lateness is how much after the due date it finished; it is negative if the job finished early. You want the worst lateness to be small, so that no single customer waits too long past their date.

If all jobs are ready at the start, do them in the order of their due dates. If jobs become ready at different times, it gets hard: sometimes it is best to leave the machine idle and wait for an urgent job. If you may stop a job and continue it later, it is easy again: always work on the ready job with the nearest due date.

## Definition

**Input.** $n$ jobs. Job $j$ has a processing time $p_j \ge 0$, a release date $r_j \ge 0$ (zero when the problem has no release dates) and a due date $d_j \in \mathbb{R}$.

**Output.** A schedule on one machine: each job $j$ runs in one piece $[S_j, C_j)$ with $C_j = S_j + p_j$ and $S_j \ge r_j$, and no two pieces overlap. In the preemptive version $1 \mid r_j, pmtn \mid L_{\max}$, a job may run in several pieces that add up to $p_j$, none of them before $r_j$, and $C_j$ is the end of its last piece.

**Goal.**

$$\min \; L_{\max} = \max_{1 \le j \le n} (C_j - d_j).$$

**Delivery time form.** Let $K \ge \max_j d_j$ and $q_j = K - d_j \ge 0$. Job $j$ is delivered $q_j$ time units after it completes, and the goal is to minimize the time of the last delivery, $\max_j (C_j + q_j) = L_{\max} + K$. The two problems have the same optimal schedules. In this form the problem is also called the head-body-tail problem, with head $r_j$, body $p_j$ and tail $q_j$. The time reversal $r_j \leftrightarrow q_j$ maps an instance to an instance with the same optimum.

## Variants

- **$1 \| L_{\max}$.** No release dates. Solved by EDD in $O(n \log n)$ time. Also $1 \| T_{\max}$, since $T_{\max} = \max(0, L_{\max})$.
- **$1 \mid prec \mid L_{\max}$ and $1 \mid prec \mid f_{\max}$.** Precedence constraints and any nondecreasing costs. Solved by [Lawler's algorithm](/lawler-algorithm/) in $O(n^2)$ time.
- **$1 \mid r_j \mid L_{\max}$.** Release dates, no preemption. Strongly NP-hard.
- **$1 \mid r_j, pmtn \mid L_{\max}$.** Release dates with preemption. Solved by preemptive EDD.
- **Decision version.** "Is $L_{\max} \le 0$?" asks whether every job can run inside its window $[r_j, d_j]$. This is [sequencing with release times and deadlines](/scheduling-with-release-times-and-deadlines/), problem SS1 of Garey and Johnson.
- **Parallel machines.** $P \| L_{\max}$ contains $P \| C_{\max}$ (take all $d_j = 0$), so it is NP-hard, and strongly NP-hard when $m$ is part of the input. $P \mid r_j, pmtn \mid L_{\max}$ is solvable in polynomial time: Horn (1974) tests with a max flow whether all jobs can meet given deadlines, and a search on $L$ with the deadlines $d_j + L$ finds the optimum.

## Examples

**Without release dates.** Take $p = (3, 2, 1, 4, 2)$ and $d = (5, 4, 9, 10, 3)$. EDD gives the order $4, 1, 0, 2, 3$ with completion times $2, 4, 7, 8, 12$ and lateness values $-1, 0, 2, -1, 2$. So $L_{\max} = 2$, and this is optimal. The order $0, 1, 2, 3, 4$ has $L_{\max} = 9$.

**With release dates.** Take five jobs

| job | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_j$ | 4 | 2 | 2 | 1 | 2 |
| $r_j$ | 0 | 1 | 1 | 2 | 3 |
| $d_j$ | 10 | 2 | 8 | 9 | 7 |

- Run the available job with the earliest due date whenever the machine is free (Schrage's rule, below). At time 0 only job 0 is released, so it runs in $[0, 4)$. Then job 1 runs in $[4, 6)$ with lateness 4, and jobs 4, 2 and 3 follow. $L_{\max} = 4$.
- The best non-preemptive schedule leaves the machine idle in $[0, 1)$ and runs $1, 2, 3, 4, 0$, with completion times $3, 5, 6, 8, 12$. $L_{\max} = 2$, set by job 0. A search over all 120 orders confirms the value 2.
- With preemption, job 0 runs in $[0, 1)$, job 1 interrupts it and runs in $[1, 3)$, then jobs 4, 2 and 3 run in $[3, 5)$, $[5, 7)$ and $[7, 8)$, and job 0 completes in $[8, 11)$. $L_{\max} = 1$.

So the three values are $4 > 2 > 1$. Waiting helps the non-preemptive schedule, and preemption helps more.

**A family where Schrage's rule is near a factor 2.** In the delivery form take job 0 with $r = 0$, $p = K$, $q = 0$ and job 1 with $r = 1$, $p = 1$, $q = K$. Schrage's rule starts job 0 at time 0, because it is the only released job, so job 1 completes at $K + 1$ and the value is $2K + 1$. Waiting for job 1 gives $\max(2 + K, K + 2) = K + 2$. The ratio $(2K + 1)/(K + 2)$ tends to 2.

## Known algorithms

- **[EDD](/earliest-due-date-first/)** for $1 \| L_{\max}$, $O(n \log n)$, exact (Jackson 1955). The [greedy page](/minimizing-maximum-lateness/) gives the exchange proof.
- **[Lawler's algorithm](/lawler-algorithm/)** for $1 \mid prec \mid f_{\max}$, $O(n^2)$, exact (Lawler 1973).
- **Preemptive EDD** for $1 \mid r_j, pmtn \mid L_{\max}$, $O(n \log n)$, exact (Horn 1974).
- **Schrage's rule** for $1 \mid r_j \mid L_{\max}$ in delivery form, $O(n \log n)$, factor 2.
- **Potts (1980)**, factor $3/2$ in $O(n^2 \log n)$ time: run Schrage's rule up to $n$ times, each time forcing the job that interferes with the critical job to come after it.
- **Hall and Shmoys (1992)**, factor $4/3$, and a PTAS in delivery form.
- **Branch and bound.** Carlier (1982) gives a branch and bound method that branches on the job found in the analysis of Schrage's rule. It solves large instances fast in practice.

**Preemptive EDD is exact.** At each moment it runs the released, unfinished job with the earliest due date. Take integer data; rational data can be scaled. Then preemptive EDD changes jobs only at integer times, and we may look at an optimal preemptive schedule $\sigma$ slot by slot, with unit slots $[t, t+1)$.

1. Let $[t, t+1)$ be the first slot where $\sigma$ and preemptive EDD differ, and let $j$ be the job that EDD runs there. The two schedules agree before $t$, so in $\sigma$ the job $j$ is released and unfinished at $t$, and $\sigma$ runs in this slot either nothing or a job $k$ with $d_k \ge d_j$.
2. Swap the contents of the slot $[t, t+1)$ and of the last slot of $j$ in $\sigma$, which is later than $t$. Job $j$ completes no later than before.
3. Job $k$, if there is one, now completes at most at $\max(C_k(\sigma), C_j(\sigma))$. Its new lateness is at most $\max(L_k(\sigma), C_j(\sigma) - d_k)$, and $C_j(\sigma) - d_k \le C_j(\sigma) - d_j \le L_{\max}(\sigma)$. No other job moves.
4. So the new schedule is optimal and agrees with EDD on a longer prefix. After finitely many swaps it is the preemptive EDD schedule, which is therefore optimal.

**Schrage's rule.** This is the non-preemptive version of the same idea, in delivery form: whenever the machine is free, start the released job with the largest $q_j$, which is the earliest due date.

```pseudo id=main
SCHRAGE(p[1 .. n], r[1 .. n], q[1 .. n])
L1  t ← 0, H ← empty max-heap keyed by q
L2  while some job is not scheduled do
L3      insert into H every job j with r[j] ≤ t that is not in H and not scheduled
L4      if H is empty then t ← the least release date of an unscheduled job, and go to L2
L5      j ← extract from H the job with the largest q[j]
L6      S[j] ← t, t ← t + p[j], C[j] ← t
L7  return S and max over j of (C[j] + q[j])
```

**Schrage's rule is a 2-approximation.** For any set $A$ of jobs, every schedule must start some job of $A$ at time $\min_{j \in A} r_j$ or later, run all of $A$, and deliver the last job of $A$ at least $\min_{j \in A} q_j$ after that. So

$$\mathrm{OPT} \ge h(A) = \min_{j \in A} r_j + \sum_{j \in A} p_j + \min_{j \in A} q_j, \qquad \mathrm{OPT} \ge r_j + p_j + q_j \ge p_j .$$

Let $c$ be a job with $C_c + q_c$ equal to the value of Schrage's schedule. Let $[t_0, C_c]$ be the longest interval that ends at $C_c$ and in which the machine is never idle, and let $B$ be the jobs that run in it. Each job of $B$ has $r_j \ge t_0$: the rule leaves the machine idle only when no unscheduled job is released, so a job released before $t_0$ ran before $t_0$. So $C_c = t_0 + p(B) \le \min_B r + p(B)$.

- If every job of $B$ has $q_j \ge q_c$, then $\min_B q = q_c$ and $C_c + q_c \le \min_B r + p(B) + \min_B q = h(B) \le \mathrm{OPT}$, and the schedule is optimal.
- Otherwise let $a$ be the last job of $B$ before $c$ with $q_a < q_c$, and let $B'$ be the jobs after $a$ up to and including $c$. Each job of $B'$ has $q_j \ge q_c$. Each job of $B'$ is released after $S_a$: at time $S_a$ line L5 chose $a$, so no released job with a larger $q$ was waiting. Thus $C_c = S_a + p_a + p(B') < \min_{B'} r + p_a + p(B')$, and
$$C_c + q_c < h(B') + p_a \le \mathrm{OPT} + \mathrm{OPT}.$$

So the value is less than $\mathrm{OPT} + \max_j p_j \le 2\,\mathrm{OPT}$. The job $a$ is the interference job that Potts and Carlier branch on. The tests of this page check $\mathrm{OPT} \le$ Schrage $\le \mathrm{OPT} + \max_j p_j$ on random instances against a search over all orders. With all $r_j = 0$ the rule is EDD and is exact.

## Bounds

- **Exact.** $1 \| L_{\max}$ and $1 \mid r_j, pmtn \mid L_{\max}$ take $O(n \log n)$ time, the cost of sorting the due dates. $1 \mid prec \mid f_{\max}$ takes $O(n^2)$.
- **Hardness.** $1 \mid r_j \mid L_{\max}$ is strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977), so it has no pseudo-polynomial algorithm and, in delivery form, no [FPTAS](/fptas/) unless P = NP. See [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).
- **No ratio for $L_{\max}$ itself.** Deciding whether the optimum is at most 0 is strongly NP-complete. An algorithm with any finite ratio $\alpha$ for $L_{\max}$ would return a value $\le \alpha \cdot 0 = 0$ exactly when the optimum is at most 0, and so would decide this question. So no polynomial algorithm has a finite [approximation ratio](/approximation-ratio/) for $L_{\max}$ unless P = NP. This is why the results above are for the delivery form, where all values are at least $\max_j p_j \ge 0$. Williamson and Shmoys get the same effect by assuming $d_j < 0$ for all $j$, so that $\mathrm{OPT} > 0$.
- **Approximation in delivery form.** The best results are a [PTAS](/ptas/) (Hall and Shmoys 1992). Strong NP-hardness rules out an FPTAS.

## Reductions

- **From 3-partition.** Let $a_1, \ldots, a_{3m}$ with $\sum_i a_i = mB$ be an instance of [3-partition](/three-partition/). Make one job with $p = a_i$, $r = 0$ and $d = mB + m - 1$ for each number, and $m - 1$ separator jobs with $p = 1$, $r = iB + i - 1$ and $d = iB + i$ for $i = 1, \ldots, m - 1$. The separators have no slack, so they fix $m$ gaps of length exactly $B$, and the number jobs fit in the gaps with $L_{\max} \le 0$ exactly when the numbers split into $m$ triples of sum $B$. The numbers are polynomial in the input size, so the hardness is strong.
- **To the delivery form and back.** $q_j = K - d_j$ with $K = \max_j d_j$, and back with $d_j = K - q_j$. Both take $O(n)$ time and keep all schedules and their order of quality.
- **Special cases.** $C_{\max}$ is $L_{\max}$ with all $d_j = 0$. With release dates, $1 \mid r_j \mid C_{\max}$ is easy: run the jobs in order of release dates. See [scheduling with release dates](/scheduling-with-release-dates/).
- **A building block.** The one-machine problem with heads and tails is the relaxation that branch and bound methods for the [job shop](/job-shop-scheduling/) solve for each machine.

## Applications

- **Customer due dates.** Shops that promise dates to customers want no customer to wait long past the promise.
- **Real-time systems.** The test "can all deadlines be met?" is $L_{\max} \le 0$. The [earliest deadline first](/earliest-deadline-first/) policy of real-time systems is preemptive EDD.
- **Job shop bounds.** Heads and tails come from the machines before and after a job. The one-machine bound is the main bound in exact job shop solvers.

## References
