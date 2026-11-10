---
tag: NCX95D
kind: definition
slug: restricted-assignment
name: Restricted assignment
aliases:
- machine eligibility sets
- eligibility constraints
- P|M_j|Cmax
area: online-and-streaming/online-scheduling
level: intro
summary: Each job may run only on a given subset of machines, with the same time on each allowed machine. Online, the eligible set arrives with the job, and the best ratio is Theta(log m).
prereqs: [identical-machines, graham-three-field-notation]
see_also: [online-restricted-assignment-load-balancing, greedy-restricted-assignment, online-restricted-assignment-lower-bound, restricted-assignment-scheduling, unrelated-machines, power-of-two-choices, bipartite-matching, load-balancing-problem]
sources:
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    title: Azar, Naor and Rom 1995
    locator: the model of jobs with sets of allowed machines, the greedy upper bound and the deterministic and randomized lower bounds
  - paper: "Yossi Azar, On-line load balancing, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Azar 1998, survey chapter
    locator: the section on the restricted assignment model
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the restricted assignment model
---

In restricted assignment, each job may run only on some machines, and on each of them it takes the same time. It sits between [identical machines](/identical-machines/), where every machine is allowed, and [unrelated machines](/unrelated-machines/), where the times are arbitrary. Offline, the problem $P \mid M_j \mid C_{\max}$ is covered on the page on [restricted assignment scheduling](/restricted-assignment-scheduling/). Online, the set of allowed machines arrives with the job, and the competitive ratio grows with $m$: it is $\Theta(\log m)$, against $2 - \frac1m$ for identical machines.

## Definition

There are $m$ machines and a sequence $\sigma$ of $n$ jobs. Job $j$ has a size $p_j \ge 0$ and a nonempty set $M_j \subseteq \{1, \ldots, m\}$ of *eligible* (allowed) machines. A schedule assigns each job $j$ to one machine $i \in M_j$. The load of machine $i$ is $\ell_i = \sum_{j \text{ on } i} p_j$, and the cost is the makespan $\max_i \ell_i$. In the three-field notation the class is $P \mid M_j \mid C_{\max}$, and in the language of unrelated machines it is the case

$$p_{ij} = \begin{cases} p_j & \text{if } i \in M_j, \\ \infty & \text{otherwise.} \end{cases}$$

**The online version.** In $P \mid \mathrm{online\text{-}list}, M_j \mid C_{\max}$, job $j$ arrives with $p_j$ and $M_j$, and the algorithm must put it on a machine of $M_j$ before it sees job $j + 1$. The choice is final. This is [online restricted assignment](/online-restricted-assignment-load-balancing/); it is also called online load balancing with assignment restrictions. When all $p_j = 1$ it is the unit case.

**What the sets change.** With identical machines, the two bounds $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$ are within a factor of 2 of the optimum, and list scheduling compares its load with them. With eligibility sets, the average bound fails: $m$ unit jobs that may all run only on machine 1 have $\mathrm{OPT} = m$, while the average is $1$. The right lower bound is local. For every set $S$ of machines, the jobs with $M_j \subseteq S$ must fit on $S$, so

$$\mathrm{OPT} \ge \max_{S} \frac{1}{|S|} \sum_{j :\, M_j \subseteq S} p_j .$$

An online algorithm does not know which sets $S$ will become tight, and an adversary uses this to force a ratio of order $\log m$.

**Unit jobs offline.** When all $p_j = 1$, the offline optimum is the least $L$ such that a [bipartite](/bipartite-matching/) flow exists from jobs to machines with each job sending 1 unit to its eligible machines and each machine taking at most $L$ units. A [max-flow](/max-flow-problem/) computation for each candidate $L$ finds it in polynomial time. For general sizes the offline problem is NP-hard; see [restricted assignment scheduling](/restricted-assignment-scheduling/).

## Examples and non-examples

**A small instance.** Take $m = 2$ and two unit jobs, with $M_1 = \{1, 2\}$ and $M_2 = \{1\}$. If an online algorithm puts job 1 on machine 1, job 2 must also go to machine 1, and the makespan is $2$. The optimum puts job 1 on machine 2 and has makespan $1$. If the algorithm puts job 1 on machine 2 instead, the adversary gives $M_2 = \{2\}$. So every deterministic online algorithm has ratio at least $2$ on two machines, which is $\lceil \log_2 3 \rceil$. The [lower bound page](/online-restricted-assignment-lower-bound/) repeats this step in rounds and gets $\lceil \log_2(m + 1) \rceil$ for every $m$.

**Known online bounds.** These are proved on the linked pages.

| result | value | page |
|---|---|---|
| greedy (least load among eligible machines), any sizes | $\lceil \log_2 m \rceil + 1$ | [greedy restricted assignment](/greedy-restricted-assignment/) |
| every deterministic algorithm | at least $\lceil \log_2(m + 1) \rceil$ | [lower bound](/online-restricted-assignment-lower-bound/) |
| every randomized algorithm, oblivious adversary | at least $\ln m$ | [lower bound](/online-restricted-assignment-lower-bound/) |

**Two random choices.** If $M_j$ is a set of two machines chosen at random, and not by an adversary, greedy keeps the maximum load of $n = m$ unit jobs near $\log_2 \ln m$. This is the [power of two choices](/power-of-two-choices/), the same rule on random sets.

**Non-examples.**

- If job $j$ has different times on two allowed machines, the instance is [unrelated](/unrelated-machines/), not restricted assignment.
- Machines with speeds are [uniform machines](/uniform-machines/); a speed of zero is not a way to write $M_j$, because the time $p_j / 0$ is not defined.
- A job that may be split among its eligible machines is a fractional or preemptive variant, where a flow argument gives the optimum offline; the integral model above does not allow it.

## Related definitions

- [Online restricted assignment](/online-restricted-assignment-load-balancing/): the online problem and its bounds.
- [Greedy restricted assignment](/greedy-restricted-assignment/) and [its lower bound](/online-restricted-assignment-lower-bound/).
- [Restricted assignment scheduling](/restricted-assignment-scheduling/): the offline problem and its approximations.
- [Unrelated machines](/unrelated-machines/): the general environment.
- [Load balancing problem](/load-balancing-problem/) and [power of two choices](/power-of-two-choices/): the random versions.

## References
