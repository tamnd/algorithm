---
tag: N7DJXC
kind: problem
slug: scheduling-with-release-dates
name: Scheduling with release dates
aliases:
- release times
- 1|r_j|Cmax
- scheduling with ready times
area: approximation/scheduling-approximation
level: advanced
summary: Jobs may not start before their release dates. Makespan stays easy on one machine, but most other objectives become strongly NP-hard; this page maps the versions and their approximations.
prereqs: [scheduling-notation, release-time, list-scheduling]
see_also: [maximum-lateness-minimization, weighted-completion-time-scheduling, flow-time-minimization, scheduling-with-release-times-and-deadlines, srpt, preemptive-scheduling, makespan-minimization, online-algorithm]
sources:
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (strong NP-hardness of 1|r_j|L_max, 1|r_j|sum C_j and 1|r_j|sum U_j)
  - paper: "Leslie A. Hall and David B. Shmoys, Jackson's rule for single-machine scheduling: making a good heuristic better, Mathematics of Operations Research 17(1), 1992"
    locator: pages 22 to 35 (the 4/3 bound and a PTAS for 1|r_j|L_max in the delivery form)
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1), 1974"
    locator: pages 177 to 185 (preemptive EDD with release dates)
  - paper: "Bo Chen and Arjen P. A. Vestjens, Scheduling on identical machines: how good is LPT in an on-line setting?, Operations Research Letters 21(4), 1997"
    locator: pages 165 to 169 (online makespan with release dates, ratio 3/2)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.1 (maximum lateness with release dates) and Section 4.1 (total completion time with release dates)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), and Chapter 5, Parallel Machine Models (Deterministic)
---

Scheduling with release dates is the family of scheduling problems in which each job $j$ has a [release date](/release-time/) $r_j$ and may not start before it. In the [three-field notation](/scheduling-notation/) the field $r_j$ marks this, as in $1 \mid r_j \mid C_{\max}$. The machine may then have to wait, so idle time can be part of a good schedule. For the [makespan](/makespan/) on one machine, release dates are harmless: running the jobs in order of release date is optimal. For almost every other objective they turn an easy problem into a strongly NP-hard one, and the usual answers are an exact preemptive algorithm, a conversion to a non-preemptive schedule, and an approximation scheme. This page proves the makespan results for one and for $m$ machines and maps the other versions to their own pages.

## In plain words

Work arrives over time, and you cannot start a task before it arrives. If you only care when the last task is done, start whatever has arrived whenever the machine is free; on one machine nothing does better. If you care about each task, for example how long each one waits, the choice of what to run next becomes hard. A short task may arrive one minute after you started a long one, and you cannot know in general whether to wait for it.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$ and release dates $r_j \ge 0$, and $m \ge 1$ identical machines. Other versions add due dates $d_j$, weights $w_j$, delivery times $q_j$ or precedence constraints.

**Output.** A start time $S_j \ge r_j$ and a machine for each job, such that no machine runs two jobs at once. Without preemption, job $j$ runs in $[S_j, S_j + p_j)$, so $C_j = S_j + p_j$.

**Goal.** For the version on this page, minimize the makespan $C_{\max} = \max_j C_j$. The other objectives are in the table of variants.

## Variants

| objective | one machine, no preemption | one machine, preemption | see |
|---|---|---|---|
| $C_{\max}$ | ERD, $O(n \log n)$ | the same | this page |
| $L_{\max}$ | strongly NP-hard; factor 2 in the delivery form, PTAS | preemptive EDD, $O(n \log n)$ (Horn 1974) | [maximum lateness](/maximum-lateness-minimization/) |
| $\sum C_j$ | strongly NP-hard; factor 2, $e/(e-1)$, PTAS | SRPT, $O(n \log n)$ | [weighted completion time](/weighted-completion-time-scheduling/) |
| $\sum w_j C_j$ | strongly NP-hard; PTAS | strongly NP-hard | [weighted completion time](/weighted-completion-time-scheduling/) |
| $\sum F_j = \sum (C_j - r_j)$ | strongly NP-hard; no ratio $n^{1/2 - \varepsilon}$ | SRPT, $O(n \log n)$ | [flow time](/flow-time-minimization/) |
| $\sum U_j$ | strongly NP-hard; no finite ratio | polynomial (Lawler 1990) | [tardy jobs](/minimizing-tardy-jobs/) |
| "all jobs on time?" | strongly NP-complete | polynomial, by EDD | [release times and deadlines](/scheduling-with-release-times-and-deadlines/) |

On $m$ identical machines, $P \mid r_j \mid C_{\max}$ is strongly NP-hard already without release dates, ERD list scheduling below has ratio less than 2, and a PTAS exists for $P \mid r_j, q_j \mid C_{\max}$ (Hall and Shmoys 1989). In the online version, where a job becomes known at $r_j$, see [online algorithms](/online-algorithm/).

**Delivery times.** In $1 \mid r_j, q_j \mid C_{\max}$, job $j$ also needs $q_j$ units of delivery after it completes, which takes no machine time, and the goal is $\max_j (C_j + q_j)$. With $d_j = K - q_j$ for a large constant $K$, this is $1 \mid r_j \mid L_{\max}$ plus $K$. Reversing time swaps the roles of $r_j$ and $q_j$. The approximation results for $L_{\max}$ use this form, because $L_{\max}$ itself can be 0 or negative.

## Examples

**One machine.** Take four jobs, numbered from 0:

| job | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $p_j$ | 2 | 3 | 1 | 2 |
| $r_j$ | 4 | 0 | 1 | 9 |

ERD runs job 1 in $[0, 3]$, job 2 in $[3, 4]$, job 0 in $[4, 6]$, waits, and runs job 3 in $[9, 11]$. So $C_{\max} = 11$. No schedule does better: job 3 is released at 9 and needs 2 units, so every schedule ends at 11 or later.

**Two machines.** Take three jobs, all released at 0, with $p = (1, 1, 2)$ in this list order. ERD list scheduling puts the two unit jobs on the two machines, and then the long job on a machine that is free at time 1, so $C_{\max} = 3$. The optimum is 2: the long job alone on one machine. With $m(m-1)$ unit jobs followed by one job of length $m$, ERD gives $2m - 1$ and the optimum is $m$, so the ratio of ERD can be $2 - 1/m$.

**An objective that changes everything.** With the same four jobs and $\sum C_j$ as the objective, the order matters inside the busy period, and a long job that is released early can block short jobs that come soon after. The [weighted completion time page](/weighted-completion-time-scheduling/) has a five-job example in which the optimal schedule leaves the only job released at time 0 for the end.

## Known algorithms

**ERD list scheduling.** Take the jobs by release date. Put each one on the machine that becomes free first, and start it as soon as both the machine and the job are ready.

```pseudo id=main
ERD-SCHEDULE(p[1 .. n], r[1 .. n], m)
L1  sort the jobs so that r[j1] ≤ r[j2] ≤ ... ≤ r[jn]
L2  F ← a min-heap of the m machines, each free at time 0
L3  for k ← 1 to n do
L4      remove from F the machine i that is free first, at time t
L5      S[jk] ← max(t, r[jk]), run jk on i, insert i into F, free at S[jk] + p[jk]
L6  return the start times S and Cmax = max over j of S[j] + p[j]
```

The sort takes $O(n \log n)$ time and each heap operation $O(\log m)$, so the total is $O(n \log n)$ time and $O(n + m)$ space. The rule is also an online algorithm: it starts a job only after its release date and uses no later information, apart from the order among jobs with the same release date.

**Theorem 1.** On one machine, ERD is optimal for $1 \mid r_j \mid C_{\max}$, and $\mathrm{OPT} = \max_j \bigl( r_j + p(\{k : r_k \ge r_j\}) \bigr)$.

*Proof.* Lower bound: in any schedule, all jobs with $r_k \ge r_j$ run after time $r_j$ on the single machine, so the schedule ends at $r_j + p(\{k : r_k \ge r_j\})$ or later. Upper bound: let $j_i$ be the job after the last idle time of the ERD schedule, or $j_1$ if there is none. Then the machine is busy from $r_{j_i}$ to the end with the jobs $j_i, \ldots, j_n$, which all have $r \ge r_{j_i}$. So $C_{\max} = r_{j_i} + p(\{j_i, \ldots, j_n\}) \le r_{j_i} + p(\{k : r_k \ge r_{j_i}\})$, which is at most the lower bound. ∎

**Theorem 2.** On $m$ identical machines, ERD list scheduling has $C_{\max} \le 2\,\mathrm{OPT} - p_\ell / m$, where $\ell$ is a job that completes last. So the ratio is less than 2.

*Proof.* First we show that no machine is idle at any time in $[r_\ell, S_\ell)$. If $S_\ell > r_\ell$, then $S_\ell = t$, the time at line L4 for $\ell$, and every machine is busy up to its free time, which is at least $t$, except for idle gaps. An idle gap on a machine ends when a job $k$ starts at $r_k$. That job $k$ came before $\ell$ in the sorted order, so the gap ends at $r_k \le r_\ell$. So all $m$ machines run other jobs during $[r_\ell, S_\ell)$, and $m(S_\ell - r_\ell) \le \sum_j p_j - p_\ell$. Every schedule has $\mathrm{OPT} \ge r_\ell + p_\ell$, because $\ell$ cannot start before $r_\ell$, and $\mathrm{OPT} \ge \sum_j p_j / m$, because the machines share the work. Hence

$$C_{\max} = S_\ell + p_\ell \le (r_\ell + p_\ell) + \frac{\sum_j p_j}{m} - \frac{p_\ell}{m} \le 2\,\mathrm{OPT} - \frac{p_\ell}{m}. \qquad ∎$$

Without release dates this is Graham's bound $2 - 1/m$ for [list scheduling](/list-scheduling/), since then $r_\ell = 0$ and the same steps give $C_{\max} \le \sum_j p_j / m + (1 - 1/m)\,p_\ell$. The two-machine example above shows that ERD can be as bad as $2 - 1/m$. With release dates we prove only the bound "less than 2" here. The tests did not find an instance worse than $2 - 1/m$.

The tests of this page compare ERD with a search over all orders on one machine, and with a search over all assignments of jobs to 2 or 3 machines, on seeded random instances with up to 7 jobs. They also check the tight family.

**Other algorithms.**

- **Maximum lateness.** Schrage's rule, preemptive EDD, and the factor 2 in the delivery form; see [maximum lateness](/maximum-lateness-minimization/).
- **Total completion time.** SRPT with preemption, and the factor 2 conversion without it; see [weighted completion time](/weighted-completion-time-scheduling/) and [SRPT](/srpt/).
- **Online makespan.** Chen and Vestjens (1997) show that "when a machine is idle, start the longest released job" has competitive ratio $3/2$ for $P \mid r_j \mid C_{\max}$ online. See [competitive ratio](/competitive-ratio/).
- **Preemption.** With preemption, release dates are often easy: preemptive EDD for $L_{\max}$, SRPT for $\sum C_j$ and $\sum F_j$. See [preemptive scheduling](/preemptive-scheduling/).

## Bounds

- **Exact.** $O(n \log n)$ for $1 \mid r_j \mid C_{\max}$ and for the preemptive one-machine versions of $L_{\max}$, $\sum C_j$ and $\sum F_j$.
- **Strong NP-hardness.** $1 \mid r_j \mid L_{\max}$, $1 \mid r_j \mid \sum C_j$ and $1 \mid r_j \mid \sum U_j$ are strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977), so they have no [FPTAS](/fptas/) unless P = NP. The proof for $L_{\max}$ is a reduction from [3-partition](/three-partition/) on the [maximum lateness page](/maximum-lateness-minimization/).
- **Approximation.** A factor less than 2 for $P \mid r_j \mid C_{\max}$ by ERD, and PTASs for the makespan with release dates and delivery times on one and on $m$ machines.
- **No ratio.** For $1 \mid r_j \mid \sum U_j$ and for $L_{\max}$ in the usual form, the optimum can be 0, and deciding whether it is 0 is NP-hard, so no finite ratio is possible unless P = NP.

## Reductions

- **Release dates and deadlines.** "Can all jobs meet their deadlines?" with release dates is [sequencing with release times and deadlines](/scheduling-with-release-times-and-deadlines/). It is the decision version of $1 \mid r_j \mid L_{\max}$ with the question $L_{\max} \le 0$.
- **Delivery times and due dates.** $1 \mid r_j, q_j \mid C_{\max}$ and $1 \mid r_j \mid L_{\max}$ are the same problem with $d_j = K - q_j$.
- **Time reversal.** A schedule for release dates $r_j$ and delivery times $q_j$, read backwards, is a schedule for release dates $q_j$ and delivery times $r_j$ with the same value.
- **Completion time and flow time.** With release dates, $\sum_j C_j = \sum_j F_j + \sum_j r_j$. Exact algorithms transfer, approximation ratios do not.

## Applications

- **Arrivals over time.** Orders, jobs on a server, and patients in a clinic all arrive over time, and none can be served before it arrives.
- **Heads and tails in shop scheduling.** In branch and bound for [job shop scheduling](/job-shop-scheduling/), each machine gives a problem $1 \mid r_j, q_j \mid C_{\max}$, where $r_j$ is the work before an operation and $q_j$ the work after it. Its preemptive optimum and Schrage's rule give the bounds.
- **Online scheduling.** Release dates are the arrival times of online jobs, so the offline problems here give the optimum that [competitive ratios](/competitive-ratio/) compare with.

## References
