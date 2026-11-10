---
tag: 05ZP6A
kind: problem
slug: online-max-stretch
name: Online maximum stretch minimization
aliases:
- online max-stretch
- online maximum slowdown
area: online-and-streaming/online-scheduling
level: research
summary: Online scheduling that minimizes the largest stretch over all jobs.
prereqs: [stretch, online-flow-time-minimization, earliest-deadline-first]
see_also: [srpt, edf-optimality, flow-time, deadline, competitive-ratio, non-clairvoyant-flow-time-minimization, scheduling-metrics]
sources:
  - paper: "Michael A. Bender, Soumen Chakrabarti and S. Muthukrishnan, Flow and stretch metrics for scheduling continuous job streams, SODA 1998"
    locator: pages 270 to 279 (the Omega(Delta^(1/3)) lower bound, the O(sqrt Delta)-competitive online algorithm, and the offline algorithm)
  - paper: doi:10.4086/toc.2012.v008a007
    title: Chandra Chekuri, Sungjin Im and Benjamin Moseley, Online scheduling to minimize maximum response time and maximum delay factor, Theory of Computing 8, 2012
    locator: pages 165 to 195, Section 1 (the history of max stretch, the lower bound when Delta is not known, and the result with extra speed)
  - paper: "Michael A. Bender, S. Muthukrishnan and Rajmohan Rajaraman, Improved algorithms for stretch scheduling, SODA 2002"
    locator: pages 762 to 771 (a simpler O(sqrt Delta)-competitive online algorithm for the maximum stretch)
  - book: isbn:9781584883975
    title: Joseph Y-T. Leung (ed.), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004
    locator: Chapter 15, Kirk Pruhs, Jiří Sgall and Eric Torng, Online Scheduling (stretch objectives)
---

Online maximum stretch minimization is the problem of scheduling jobs that arrive over time on one machine, so that the largest [stretch](/stretch/) $\max_j (C_j - r_j)/p_j$ is small. The job sizes are known at release, and [preemption](/preemptive-scheduling/) is allowed. Offline, the problem is a [deadline](/deadline/) problem that [earliest deadline first](/earliest-deadline-first/) solves after a search over the target. Online, the best [competitive ratio](/competitive-ratio/) depends on the ratio $\Delta$ of the largest to the smallest job size: it is $\Omega(\Delta^{1/3})$ and $O(\sqrt{\Delta})$ (Bender, Chakrabarti and Muthukrishnan 1998), and the exact order is open.

## In plain words

Jobs of very different sizes arrive at a server. The stretch of a job is the time it spent in the system divided by its size. The goal is that no job has a large stretch: each job, short or long, should wait in proportion to its size.

Two simple rules fail. Serving jobs in arrival order makes a short job wait behind a long one, so the short job gets a huge stretch. Always serving the shortest job can starve a long job while short jobs keep coming. The good schedule is a balance, and it depends on the jobs that come later. An online rule does not know them, so it must hedge. The theory shows that the price of not knowing the future grows with the ratio between the largest and the smallest job.

## Definition

**Input.** A sequence $\sigma$ of $n$ jobs, revealed online. Job $j$ has release time $r_j \ge 0$ and processing time $p_j > 0$, both known at time $r_j$ (the [clairvoyant](/clairvoyant-scheduling/) model). Let $\Delta = \max_j p_j / \min_j p_j$.

**Output.** A preemptive schedule on one machine of speed 1, built online.

**Objective.** Minimize $\max_j S_j$, where $S_j = (C_j - r_j)/p_j$.

**Notation.** ALG$(\sigma)$ and OPT$(\sigma)$ are the maximum stretch of the online schedule and of the best offline preemptive schedule. An algorithm is $c$-competitive if ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. The ratio $c$ may depend on $\Delta$. Some results assume that the algorithm knows $\Delta$ in advance.

## Variants

- **Known or unknown $\Delta$.** The $O(\sqrt{\Delta})$ algorithms use the value of $\Delta$ or an estimate of it. When $\Delta$ is not known in advance, Chekuri, Im and Moseley show a stronger lower bound, of the form $\Delta^{0.4}/2$.
- **Extra speed.** With a machine of speed $1 + \varepsilon$ against OPT at speed 1, shortest job first is $O(1/\varepsilon)$-competitive for the maximum stretch, as noted by Chekuri, Im and Moseley.
- **Maximum weighted flow time.** The maximum of $w_j F_j$ for general weights. Stretch is the case $w_j = 1/p_j$; the delay factor of a job with a deadline is a related case.
- **Total stretch.** The sum of the stretches, where [SRPT](/srpt/) is 2-competitive. See [stretch](/stretch/).
- **Parallel machines and broadcast.** The same objective on $m$ machines, or in broadcast scheduling, where one transmission serves many requests.

## Examples

All examples are on one machine, with a long job $(0, \Delta)$ and $k$ unit jobs released at times $1, 2, \dots, k$, written as (release, size). The values are exact optimal maximum stretches, from the deadline test below.

| $\Delta$ | $k$ | SRPT | FIFO | OPT |
|---|---|---|---|---|
| 4 | 8 | 3 | 4 | 3 |
| 4 | 40 | 11 | 4 | 4 |
| 16 | 64 | 5 | 16 | 5 |

- With $\Delta = 4$ and $k = 40$, SRPT runs each unit job on arrival and finishes the long job at time 44, so its stretch is $44/4 = 11$. FIFO runs the long job first; each unit job then waits 3 units and has stretch 4, which is optimal.
- With $\Delta = 16$ and $k = 64$, FIFO makes the first unit job wait until time 16, for stretch 16. SRPT gives the long job stretch $(64 + 16)/16 = 5$, which is optimal.

So FIFO is good on one input and SRPT on the other. An online algorithm sees the same start in both inputs, a long job and then unit jobs, and it must choose how much of the long job to run before it knows $k$.

## Known algorithms

**Offline: a search over the target.** The maximum stretch is at most $s$ if and only if each job meets the deadline $d_j(s) = r_j + s p_j$. With preemption, EDF meets all deadlines whenever some schedule does ([EDF optimality](/edf-optimality/)). A set of deadlines is feasible on one machine if and only if, for each release time $a$ and each deadline $b > a$, the jobs with $r_j \ge a$ and $d_j(s) \le b$ have total size at most $b - a$. Each violated pair gives a linear inequality in $s$, so the optimal $s$ is one of polynomially many critical values, and a binary search over them with the EDF test finds it. This is the method of the table above. It needs all jobs in advance.

**Online: EDF with estimated deadlines.** The online algorithm of Bender, Chakrabarti and Muthukrishnan uses the offline method on the jobs seen so far: at each arrival it computes the optimal maximum stretch of the known jobs, sets deadlines from this estimate with a slack factor that depends on $\Delta$, and runs EDF. They show that it is $O(\sqrt{\Delta})$-competitive. Bender, Muthukrishnan and Rajaraman gave a simpler algorithm with the same ratio. These results are cited here, and this description is only a sketch of the idea; the exact rules are in the papers.

**Simple rules.** Neither SRPT nor FIFO is good in general. With only the jobs $(0, \Delta)$ and $(1, 1)$, FIFO gives the unit job stretch $\Delta$, while running the unit job at once gives maximum stretch $(\Delta + 1)/\Delta$. So the FIFO ratio grows linearly in $\Delta$. SRPT can starve a long job, as in the first example.

## Bounds

| bound | model | value | source |
|---|---|---|---|
| lower | deterministic online, one machine, preemptive | $\Omega(\Delta^{1/3})$ | Bender, Chakrabarti and Muthukrishnan 1998 |
| upper | deterministic online, one machine, preemptive | $O(\sqrt{\Delta})$ | Bender, Chakrabarti and Muthukrishnan 1998 |
| lower | deterministic online, $\Delta$ not known in advance | about $\Delta^{0.4}/2$ | Chekuri, Im and Moseley 2012 |
| upper | speed $1 + \varepsilon$, shortest job first | $O(1/\varepsilon)$ | noted by Chekuri, Im and Moseley 2012 |
| exact | offline, one machine, preemptive | polynomial time | Bender, Chakrabarti and Muthukrishnan 1998 |

All bounds are cited here and not proved. *Sketch of the idea of the lower bound:* the adversary releases a long job and then a stream of short jobs. If the algorithm works on the long job, a short job waits and its stretch grows. If it serves the short jobs, the adversary continues the stream until the long job has a large stretch, while OPT, which knows the length of the stream, chose the right balance from the start. Balancing the two cases gives the exponent $1/3$. The gap between $\Delta^{1/3}$ and $\Delta^{1/2}$ is open.

## Reductions

- **To deadline scheduling.** For a fixed target $s$, the problem is feasibility with deadlines $r_j + s p_j$, solved by EDF. The online difficulty is that $s$ is not known.
- **From maximum flow time.** With all $p_j$ equal, the stretch is the flow time divided by a constant, and FIFO is optimal on one machine.
- **To maximum weighted flow time.** Stretch is the weight $1/p_j$, so algorithms for the maximum weighted flow time apply.

## Applications

The maximum stretch is a fairness measure for servers that handle requests of very different sizes, such as web and file servers, database servers and data broadcast systems. A low maximum stretch means that no request, small or large, waits much longer than its size justifies.

## References
