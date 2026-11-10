---
tag: AG0VAT
kind: problem
slug: restricted-assignment-scheduling
name: Scheduling with machine eligibility restrictions
aliases:
- P|M_j|Cmax
- restricted assignment
- restricted assignment makespan
- scheduling with processing set restrictions
area: approximation/scheduling-approximation
level: advanced
summary: Each job may run only on a given subset of machines.
prereqs: [unrelated-machine-scheduling, makespan-minimization, scheduling-notation]
see_also: [lenstra-shmoys-tardos, unrelated-makespan-inapproximability, configuration-lp, online-restricted-assignment-load-balancing, bipartite-matching, local-search, uniform-machine-scheduling, scheduling-makespan-inapproximability]
sources:
  - paper: doi:10.1007/BF01585745
    title: "J. K. Lenstra, D. B. Shmoys and É. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990"
    locator: the 2-approximation and the 3/2 hardness, whose instances are restricted assignment instances
  - paper: "T. Ebenlendr, M. Krčál and J. Sgall, Graph balancing: a special case of scheduling unrelated parallel machines, Proceedings of the 19th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2008, pages 483 to 490; journal version in Algorithmica 68(1), 2014"
    locator: the 1.75-approximation for graph balancing and the 3/2 hardness for graph balancing with two job sizes
  - paper: "O. Svensson, Santa Claus schedules jobs on unrelated machines, SIAM Journal on Computing 41(5), 2012"
    locator: the estimate 33/17 of the optimum by the configuration linear program
  - paper: "K. Jansen and L. Rohwedder, On the configuration-LP of the restricted assignment problem, Proceedings of the 28th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2017"
    locator: the improved estimate 11/6
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    locator: the greedy online algorithm with ratio about log m and the matching lower bound
---

Scheduling with machine eligibility restrictions, also called the restricted assignment problem and written $P \mid M_j \mid C_{\max}$, is [makespan minimization](/makespan-minimization/) where each job $j$ has one processing time $p_j$ and a set $M_j$ of machines that may run it. It is the special case of [unrelated machines](/unrelated-machine-scheduling/) with $p_{ij} \in \{p_j, \infty\}$. The [3/2 hardness](/unrelated-makespan-inapproximability/) holds already for it, and the [rounding of Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) gives ratio 2, but the problem has a structure that general unrelated machines lack: the [configuration LP](/configuration-lp/) is known to estimate its optimum within a factor below 2.

## In plain words

Each task has a fixed length, but only some workers have the tools or the license to do it. You must give each task to one of its allowed workers so that the last worker finishes as early as possible.

If all workers could do all tasks, simple rules would be very good. The limits change this: a worker who is the only one able to do some task may be overloaded, and nobody knows a fast method that is always much better than twice the best plan. Strong results show that the best plan can at least be estimated more closely.

## Definition

**Input.** An integer $m \ge 1$ and $n$ jobs. Job $j$ has a time $p_j \ge 0$ and a nonempty set $M_j \subseteq \{1, \ldots, m\}$ of allowed machines.

**Output.** An assignment $\sigma$ with $\sigma(j) \in M_j$ for each $j$. Machine $i$ has the load $L_i = \sum_{j : \sigma(j) = i} p_j$.

**Goal.** Minimize $C_{\max} = \max_i L_i$. The least value is $\mathrm{OPT}$.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. An *estimation algorithm* with factor $\rho$ returns a number $v$ with $\mathrm{OPT}/\rho \le v \le \mathrm{OPT}$, but not necessarily a schedule of makespan $\rho v$. All ratios here are absolute and worst case.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$, $M_j$ | the time of job $j$ and its set of allowed machines |
| $L_i$, $C_{\max}$ | the load of machine $i$, and $\max_i L_i$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Graph balancing.** Each job has $|M_j| \le 2$, so the jobs are the edges of a graph on the machines, and each edge must be oriented toward one of its ends. Ebenlendr, Krčál and Sgall (2008) gave a 1.75-approximation, and Jansen and Rohwedder (2019) showed that the configuration LP estimates the optimum within a factor slightly below 1.75. The $3/2$ hardness holds even here.
- **Two job sizes.** All times are in $\{1, \varepsilon\}$ for a small $\varepsilon$. Chakrabarty, Khanna and Li (2015) gave a polynomial algorithm with ratio $2 - \delta$ for a small constant $\delta > 0$, the first algorithm below 2 for a nontrivial case with arbitrary sets.
- **Unit times.** With $p_j = 1$, "is $\mathrm{OPT} \le T$?" asks whether each machine can take at most $T$ jobs, which is a flow problem, so the problem is polynomial. With $T = 1$ it is [bipartite matching](/bipartite-matching/).
- **Nested sets.** If any two sets $M_j$ are either disjoint or one contains the other, much better ratios are possible; Ou, Leung and Li (2008) gave a PTAS for the case where all sets have the form $\{1, \ldots, a_j\}$.
- **Online.** Jobs arrive one by one. Greedy is about $\log_2 m$ competitive, and no online algorithm does better than order $\log m$ (Azar, Naor and Rom 1995). See [online restricted assignment](/online-restricted-assignment-load-balancing/).
- **Max-min version.** Maximize the smallest load. This is the restricted Santa Claus problem. Svensson adapted to makespan a local search that Asadpour, Feige and Saberi had used for it.

## Examples

**A small instance.** Take $m = 3$ and six jobs:

| job | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| time $p_j$ | 3 | 2 | 2 | 1 | 1 | 1 |
| allowed machines $M_j$ | 1, 2 | 1 | 2, 3 | 3 | 1, 3 | 2 |

The total time is 10, so $\mathrm{OPT} \ge \lceil 10/3 \rceil = 4$. The assignment machine 1 gets jobs 2 and 5, machine 2 gets jobs 1 and 6, and machine 3 gets jobs 3 and 4 has loads 3, 4 and 3, so $\mathrm{OPT} = 4$.

Greedy in the order 1 to 6, with each job on an allowed machine of least load and ties to the lowest number, puts job 1 on machine 1 and then job 2 on machine 1 too, since it is the only choice. Machine 1 ends at 5, so greedy has makespan 5. The forced job 2 should have been foreseen.

## Known algorithms

| algorithm | ratio $\rho$ | kind | time |
|---|---|---|---|
| greedy, online | $\lceil \log_2 m \rceil + 1$ | schedule | $O(nm)$ |
| [Lenstra, Shmoys and Tardos 1990](/lenstra-shmoys-tardos/) | 2, and $2 - 1/m$ with the rounding of Shchepin and Vakhania (2005) | schedule | polynomial |
| Ebenlendr, Krčál and Sgall 2008, graph balancing | 1.75 | schedule | polynomial |
| Chakrabarty, Khanna and Li 2015, sizes 1 and $\varepsilon$ | $2 - \delta$ | schedule | polynomial |
| Svensson 2012, configuration LP | $33/17 \approx 1.941$ | estimate | polynomial for each fixed accuracy |
| Jansen and Rohwedder 2017, configuration LP | $11/6 \approx 1.833$ | estimate | polynomial for each fixed accuracy |
| flow, unit times | exact | schedule | polynomial |

The estimates use the [configuration LP](/configuration-lp/). For a guess $T$, it has a variable $y_{iC}$ for each machine $i$ and each set $C$ of jobs allowed on $i$ with total time at most $T$, and it asks that each machine choose one set fractionally and each job be covered once. It can be solved approximately in polynomial time with the ellipsoid method. Svensson's proof shows that if the program is feasible for $T$, then a schedule of makespan $33T/17$ exists. The proof is a [local search](/local-search/) inspired by Haxell's method for hypergraph matching; it is not known to end in polynomial time, so it bounds $\mathrm{OPT}$ but does not find the schedule. Finding a schedule with a ratio below 2 in polynomial time is open, and Jansen and Rohwedder (2017) gave a quasi-polynomial algorithm with ratio $11/6 + \varepsilon$.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \max_j p_j$ and $\mathrm{OPT} \ge \frac1m \sum_j p_j$, as for identical machines. More precisely, for each set $S$ of machines, the jobs with $M_j \subseteq S$ must run on $S$, so $\mathrm{OPT} \ge \frac{1}{|S|} \sum_{j : M_j \subseteq S} p_j$.
- **No ratio below 3/2.** The reduction from three-dimensional matching in [the 3/2 hardness theorem](/unrelated-makespan-inapproximability/) builds restricted assignment instances with times 1 and 2. Ebenlendr, Krčál and Sgall showed that the same bound holds for graph balancing with times 1 and 2.
- **Gap of the configuration LP.** For restricted assignment it is at most $11/6$ (Jansen and Rohwedder 2017). For general unrelated machines it is 2 (Verschae and Wiese 2014), so the restricted case is easier for this program.
- **Strong NP-hardness.** The case $M_j = \{1, \ldots, m\}$ for all $j$ is $P \mid\mid C_{\max}$.

## Reductions

**To unrelated machines.** Set $p_{ij} = p_j$ for $i \in M_j$ and $p_{ij} = \infty$ otherwise. Every algorithm for [unrelated machines](/unrelated-machine-scheduling/) applies.

**From three-dimensional matching.** The instance of the $3/2$ hardness proof has one machine for each triple, an element job of time 1 for each element of two of the three sets, and dummy jobs of time 2, and each job is allowed only on the machines of the triples that contain its element.

**Unit times to flow.** Build a network with a source, a node for each job, a node for each machine and a sink. Give the arcs from the source to the jobs capacity 1, the arcs from job $j$ to the machines of $M_j$ capacity 1, and the arcs from the machines to the sink capacity $T$. A schedule of makespan at most $T$ exists if and only if the maximum flow is $n$.

## Applications

- Assigning jobs to a cluster where some jobs need special hardware, a licensed program or data that is stored on only some servers.
- Assigning calls or tickets to agents who speak the right language or have the right training.
- Load balancing of clients that can reach only some servers, which is the setting of the online problem.

## References
