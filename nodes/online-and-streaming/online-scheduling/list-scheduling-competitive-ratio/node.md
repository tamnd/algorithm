---
tag: NHZFX8
kind: theorem
slug: list-scheduling-competitive-ratio
name: List scheduling is (2 - 1/m)-competitive
aliases:
- Graham's bound
- Graham's online bound
- competitive ratio of list scheduling
area: online-and-streaming/online-scheduling
level: intro
summary: "Graham's bound in the online view: list scheduling on m identical machines is strictly (2 - 1/m)-competitive for makespan over a list, the ratio is exact, and it is optimal for m = 2 and m = 3."
prereqs: [list-scheduling, identical-machines, competitive-ratio]
see_also: [list-scheduling-bound, list-scheduling, online-makespan-minimization, online-makespan-lower-bound, identical-machines, graham-three-field-notation, lpt-bound, makespan-lower-bounds]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the bound 2 - 1/m for list schedules and the examples that reach it
  - paper: "Ulrich Faigle, Walter Kern and Gyorgy Turan, On the performance of on-line algorithms for partition problems, Acta Cybernetica 9(2), 1989"
    title: Faigle, Kern and Turan 1989
    locator: the lower bounds for deterministic online makespan, which show that list scheduling is optimal for m = 2 and m = 3
  - paper: "Jiri Sgall, On-line scheduling, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Sgall 1998, survey chapter
    locator: the section on scheduling jobs one by one on identical machines, the analysis of list scheduling
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the greedy algorithm on identical machines
---

Graham's bound says that list scheduling, the rule "put each job on a machine of least load", has makespan at most $2 - \frac1m$ times the optimum on $m$ identical machines. The [offline page](/list-scheduling-bound/) states it as an approximation ratio. This page states it as a [competitive ratio](/competitive-ratio/) for $P \mid \mathrm{online\text{-}list} \mid C_{\max}$, the problem of [online makespan minimization](/online-makespan-minimization/), and draws the online consequences: the bound holds after every prefix of the list, it does not use the size of the current job, it is exact even with an additive constant, and for $m = 2$ and $m = 3$ no deterministic online algorithm does better.

## Statement

**Notation.** The input is a list $\sigma = (p_1, p_2, \ldots, p_n)$ of job sizes, shown one at a time, on $m$ identical machines. List scheduling (LS) gives job $t$ to a machine of least current load, ties broken in any way, before it sees job $t + 1$. $\mathrm{LS}(\sigma)$ is its makespan and $\mathrm{OPT}(\sigma)$ the optimal offline makespan of the same jobs. An online algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$ with a constant $b$, and strictly $c$-competitive if $b = 0$.

**Theorem (Graham 1966).** For every $m \ge 1$:

1. LS is strictly $(2 - \frac1m)$-competitive for $P \mid \mathrm{online\text{-}list} \mid C_{\max}$. More precisely, for every list and every prefix $\sigma_t = (p_1, \ldots, p_t)$,
$$\mathrm{LS}(\sigma_t) \le \frac1m \sum_{j \le t} p_j + \Big(1 - \frac1m\Big) \max_{j \le t} p_j \le \Big(2 - \frac1m\Big) \mathrm{OPT}(\sigma_t).$$
2. The ratio is exact: for each $c < 2 - \frac1m$ and each constant $b$, some list has $\mathrm{LS}(\sigma) > c \cdot \mathrm{OPT}(\sigma) + b$.

Both parts are proved on this page. The optimality of LS for $m = 2$ and $m = 3$ is proved on the [lower bound page](/online-makespan-lower-bound/).

## In plain words

Each job goes to the machine that has the least work so far. Take the machine that ends last and look at its last job. When that job came, its machine had the least work, so every machine had at least that much work, and the optimum must also do all that work. The last job itself is no longer than the longest job, which the optimum must also run. Add the two parts and the online schedule is less than twice the optimum. The bound holds at every moment, so the rule never needs to know when the list ends. A long list of small jobs followed by one big job shows that the bound cannot be improved for this rule.

## Proof

**Part 1.** Fix a prefix $\sigma_t$ and the schedule that LS has built for it. Let machine $i$ have the largest load, so $\mathrm{LS}(\sigma_t) = \ell_i$. If no job is on machine $i$, then $\ell_i = 0$ and there is nothing to prove. Otherwise let job $k \le t$ be the last job that LS put on machine $i$, and let $L$ be the load of machine $i$ just before job $k$ came. Then $\ell_i = L + p_k$, because no later job went to machine $i$.

When job $k$ came, LS chose machine $i$ because its load $L$ was the least. So each of the $m$ machines had load at least $L$, and the jobs before $k$ have total size at least $mL$:
$$L \le \frac1m \sum_{j < k} p_j \le \frac1m \Big(\sum_{j \le t} p_j - p_k\Big).$$
So
$$\mathrm{LS}(\sigma_t) = L + p_k \le \frac1m \sum_{j \le t} p_j + \Big(1 - \frac1m\Big) p_k .$$
Every schedule of $\sigma_t$ has some machine with load at least the average, and some machine that runs the largest job, so $\mathrm{OPT}(\sigma_t) \ge \frac1m \sum_{j \le t} p_j$ and $\mathrm{OPT}(\sigma_t) \ge \max_{j \le t} p_j \ge p_k$ (see [makespan lower bounds](/makespan-lower-bounds/)). Put these into the last line:
$$\mathrm{LS}(\sigma_t) \le \mathrm{OPT}(\sigma_t) + \Big(1 - \frac1m\Big) \mathrm{OPT}(\sigma_t) = \Big(2 - \frac1m\Big) \mathrm{OPT}(\sigma_t).$$
The argument uses nothing about the jobs after $t$, so it holds for each prefix, with $b = 0$.

**Part 2.** Let $\sigma^{(m)}$ be the list of $m(m - 1)$ jobs of size $1$, followed by one job of size $m$. LS spreads the unit jobs evenly: after $m(m - 1)$ of them every machine has load $m - 1$, because each unit job goes to a machine of least load and the least load rises by one only after all machines have reached it. The last job then goes to a machine of load $m - 1$, and $\mathrm{LS}(\sigma^{(m)}) = 2m - 1$. The optimum puts the big job alone on one machine and $m$ unit jobs on each of the other $m - 1$ machines, so $\mathrm{OPT}(\sigma^{(m)}) = m$, and it cannot be less because of the job of size $m$. The ratio is $\frac{2m - 1}{m} = 2 - \frac1m$.

For an additive constant $b$, multiply all sizes by $\lambda > 0$. LS makes the same choices, so $\mathrm{LS} = \lambda(2m - 1)$ and $\mathrm{OPT} = \lambda m$. If $c < 2 - \frac1m$, then $\lambda(2m - 1) > c \lambda m + b$ for all large $\lambda$. $\square$

**The tight list for $m = 3$.** Six unit jobs, then a job of size 3:

| job | size | loads before | machine | loads after |
|---|---|---|---|---|
| 1 to 3 | 1 each | (0, 0, 0) | 1, 2, 3 | (1, 1, 1) |
| 4 to 6 | 1 each | (1, 1, 1) | 1, 2, 3 | (2, 2, 2) |
| 7 | 3 | (2, 2, 2) | 1 | (5, 2, 2) |

$\mathrm{LS} = 5$, while $\{3\}, \{1, 1, 1\}, \{1, 1, 1\}$ gives $\mathrm{OPT} = 3$: the ratio is $\frac53$.

## Consequences

- **LS is an online algorithm with a guarantee at every moment.** Because Part 1 holds for every prefix, the bound does not depend on when the list stops, and the algorithm needs no knowledge of $n$.
- **The size of the current job is not used.** LS picks the machine before it reads $p_t$, so the bound holds when the size of each job is revealed only after its assignment, as long as the loads are known.
- **Optimal for two and three machines.** Every deterministic online algorithm has ratio at least $\frac32$ for $m = 2$ and at least $\frac53$ for $m = 3$ ([lower bound page](/online-makespan-lower-bound/)). These equal $2 - \frac1m$, so LS is the best deterministic algorithm for $m \le 3$.
- **Not optimal for $m \ge 4$.** Better deterministic algorithms keep some machines lightly loaded for large jobs; for large $m$ the best known ratio is about $1.9201$. Randomization also helps: for $m = 2$ the best randomized ratio is $\frac43$. These results are cited on the [problem page](/online-makespan-minimization/).
- **Sorted lists.** If the list is sorted by non-increasing size, LS is LPT and the bound improves to $\frac43 - \frac1{3m}$ ([LPT bound](/lpt-bound/)), but a sorted list is a promise about the future, so this is a semi-online result.

## Tightness

Part 2 shows that $2 - \frac1m$ is the exact competitive ratio of LS, strict or not. The tight list is not adaptive: LS is deterministic, so the adversary knows its choices in advance, and a fixed list is enough. Other tight lists exist. For example, $m$ unit jobs followed by a job of size $2$ give $\mathrm{LS} = 3$ and $\mathrm{OPT} = 2$, a ratio of $\frac32$. If the adversary stops this list as soon as an algorithm puts two unit jobs on one machine, it forces a ratio of at least $\frac32$ on every deterministic algorithm, and it is the first step of the lower bound proofs.

## History

Graham (1966) proved the bound for list schedules in a study of multiprocessing anomalies, together with the case of precedence constraints, before competitive analysis existed. Later surveys of online algorithms count it as the first competitive analysis, because list scheduling makes each decision without knowledge of later jobs. Faigle, Kern and Turán (1989) showed that no deterministic online algorithm beats $2 - \frac1m$ for $m = 2$ and $m = 3$, and Galambos and Woeginger (1993) gave the first algorithm better than LS for every $m \ge 4$.

## References
