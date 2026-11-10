---
tag: 02ZTAT
kind: concept
slug: stretch
name: Stretch
aliases:
- slowdown
- normalized flow time
area: online-and-streaming/online-scheduling
level: advanced
summary: The flow time of a job divided by its processing time; how much slower the job ran than on an idle machine.
prereqs: [flow-time]
see_also: [online-max-stretch, srpt, online-flow-time-minimization, earliest-deadline-first, edf-optimality, flow-time-minimization, scheduling-metrics, deadline]
sources:
  - paper: "Michael A. Bender, Soumen Chakrabarti and S. Muthukrishnan, Flow and stretch metrics for scheduling continuous job streams, SODA 1998"
    locator: pages 270 to 279 (the stretch metric, the offline algorithm for the maximum stretch, the online lower bound and the O(sqrt Delta) algorithm)
  - paper: "S. Muthukrishnan, Rajmohan Rajaraman, Anthony Shaheen and Johannes Gehrke, Online scheduling to minimize average stretch, FOCS 1999"
    locator: SRPT is 2-competitive for the total stretch on one machine (main theorem for one machine)
  - book: isbn:9781584883975
    title: Joseph Y-T. Leung (ed.), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004
    locator: Chapter 15, Kirk Pruhs, Jiří Sgall and Eric Torng, Online Scheduling (stretch and weighted flow time)
  - paper: doi:10.4086/toc.2012.v008a007
    title: Chandra Chekuri, Sungjin Im and Benjamin Moseley, Online scheduling to minimize maximum response time and maximum delay factor, Theory of Computing 8, 2012
    locator: pages 165 to 195, Section 1 (the history of the max stretch results)
---

The stretch of a job is its [flow time](/flow-time/) divided by its processing time: $S_j = F_j / p_j = (C_j - r_j)/p_j$. It says how many times longer the job stayed in the system than it would on an idle machine of speed 1. The total stretch is the weighted flow time with weight $w_j = 1/p_j$, and the maximum stretch is a fairness measure that treats short and long jobs alike. Bender, Chakrabarti and Muthukrishnan introduced the term in 1998 for servers with mixed job sizes.

## In plain words

A user who asks for a small web page expects a fast answer. A user who asks for a large file accepts a longer wait. The flow time treats a wait of ten seconds the same in both cases. The stretch does not: it divides the wait by the size of the job.

A stretch of one means that the job ran at once, with no wait. A stretch of three means that the job took three times as long as on an idle machine. The total stretch adds these numbers over all jobs. The maximum stretch looks at the worst job, so a schedule with a small maximum stretch is fair to every job. A scheduler that always serves the shortest job first keeps the stretch of short jobs small, but it can starve a long job.

## The idea

Use the notation of [flow time](/flow-time/): job $j$ has release time $r_j$, processing time $p_j > 0$ and completion time $C_j$, and $F_j = C_j - r_j$. The stretch is

$$S_j = \frac{F_j}{p_j}.$$

On one machine of speed 1, $F_j \ge p_j$, so $S_j \ge 1$. The two objectives are the total stretch $\sum_j S_j$ and the maximum stretch $\max_j S_j$. Let $\Delta = \max_j p_j / \min_j p_j$ be the ratio of the largest to the smallest processing time. Many bounds for stretch depend on $\Delta$ (some papers write $P$ for it).

**Stretch as a weighted flow time.** The total stretch is $\sum_j w_j F_j$ with $w_j = 1/p_j$. So each result for weighted flow time applies to it. The weights here are tied to the sizes in a special way: a short job has a large weight and needs little work. Because of this, the shortest remaining work first rule ([SRPT](/srpt/)) does well for total stretch, while it can be bad for general weights. On one machine, SRPT is 2-competitive for the total stretch (Muthukrishnan, Rajaraman, Shaheen and Gehrke 1999). This result is cited here and not proved.

**Maximum stretch as a deadline problem.** Fix a target $s \ge 1$. Then $S_j \le s$ if and only if $C_j \le r_j + s p_j$. So a preemptive schedule on one machine with maximum stretch at most $s$ exists if and only if the jobs can meet the [deadlines](/deadline/) $d_j(s) = r_j + s p_j$. With preemption, the [earliest deadline first](/earliest-deadline-first/) rule meets all deadlines whenever any schedule does ([EDF optimality](/edf-optimality/)). So the offline problem reduces to a search for the smallest feasible $s$. The feasibility test is the interval condition: for each set $J$ of jobs,

$$\sum_{j \in J} p_j \le \max_{k \in J} d_k(s) - \min_{j \in J} r_j.$$

Each side is a simple function of $s$, so the smallest feasible $s$ is the largest of finitely many critical values, and binary search over them finds it. Bender, Chakrabarti and Muthukrishnan gave a polynomial algorithm of this kind.

**Online, the problem is hard.** An online algorithm does not know $s$, so it cannot set the deadlines. For the maximum stretch, no online algorithm is better than $\Omega(\Delta^{1/3})$-competitive, and an $O(\sqrt{\Delta})$-competitive online algorithm exists (Bender, Chakrabarti and Muthukrishnan 1998). See [online max stretch](/online-max-stretch/).

## Examples

Take the three jobs of the [flow time](/flow-time/) page: $(r_1, p_1) = (0, 4)$, $(r_2, p_2) = (1, 1)$ and $(r_3, p_3) = (2, 2)$.

| schedule | $F_1, F_2, F_3$ | $S_1, S_2, S_3$ | $\sum S_j$ | $\max S_j$ |
|---|---|---|---|---|
| FIFO, no preemption | 4, 4, 5 | 1, 4, 5/2 | 15/2 | 4 |
| SRPT | 7, 1, 2 | 7/4, 1, 1 | 15/4 | 7/4 |

FIFO makes the short job 2 wait 3 units behind job 1, so its stretch is 4. SRPT gives the small jobs stretch 1, and the long job 1 pays with stretch $7/4$.

The value $7/4$ is the optimal maximum stretch. The set $J = \{1, 2, 3\}$ has total work $7$ and earliest release $0$, so the condition $7 \le \max(4s, 1 + s, 2 + 2s)$ forces $4s \ge 7$ for $s \ge 1$. With $s = 7/4$, the deadlines are $d_1 = 7$, $d_2 = 11/4$ and $d_3 = 11/2$, and EDF meets them with the SRPT schedule above. The optimal maximum flow time is 5, which FIFO reaches. So the schedule that is best for the maximum flow time (FIFO, $\max S_j = 4$) is not the schedule that is best for the maximum stretch.

## Where it is used

- **Web and file servers.** The size of a request is often known (the size of the file), and users accept waits in proportion to the size. Stretch is then a better measure of user experience than flow time. This was the motivation of Bender, Chakrabarti and Muthukrishnan.
- **Database and broadcast scheduling.** Stretch, also called slowdown, is common in the study of query and data broadcast schedulers.
- **Online scheduling theory.** [Online max stretch](/online-max-stretch/) is a standard example of a problem where the ratio depends on $\Delta$ and not on $n$. The total stretch is a case of [online flow time minimization](/online-flow-time-minimization/) with weights.
- **Fairness.** The maximum stretch is between the maximum flow time, which favors long jobs, and the total flow time, which favors short jobs. See also [scheduling metrics](/scheduling-metrics/).

## References
