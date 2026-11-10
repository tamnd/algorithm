---
tag: KQ1676
kind: definition
slug: unrelated-machines
name: Unrelated machines
aliases:
- R environment
- unrelated parallel machines
area: online-and-streaming/online-scheduling
level: intro
summary: "Machines where each job has its own processing time on each machine. Online, greedy is only m-competitive, and the best ratio is Theta(log m)."
prereqs: [uniform-machines, identical-machines, graham-three-field-notation]
see_also: [uniform-machines, identical-machines, restricted-assignment, unrelated-machine-scheduling, lenstra-shmoys-tardos, online-restricted-assignment-load-balancing, online-restricted-assignment-lower-bound, greedy-restricted-assignment]
sources:
  - paper: "James Aspnes, Yossi Azar, Amos Fiat, Serge Plotkin and Orli Waarts, On-line routing of virtual circuits with applications to load balancing and machine scheduling, Journal of the ACM 44(3), 1997"
    title: Aspnes, Azar, Fiat, Plotkin and Waarts 1997
    locator: the section on unrelated machines (the exponential-function algorithm with a doubling guess, O(log m) competitive)
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    title: Azar, Naor and Rom 1995
    locator: the lower bounds for restricted assignment, which hold for unrelated machines as a special case
  - paper: "Yossi Azar, On-line load balancing, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Azar 1998, survey chapter
    locator: the sections on the unrelated machines model and on the greedy algorithm
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the unrelated machines model
---

Unrelated machines are the machine environment $R$ of the [three-field notation](/graham-three-field-notation/): job $j$ takes time $p_{ij}$ on machine $i$, and the numbers $p_{ij}$ need not follow any pattern. Offline, $R \mid\mid C_{\max}$ has the 2-approximation of [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/); see [unrelated machine scheduling](/unrelated-machine-scheduling/). Online, the natural greedy rule is $m$-competitive and no better, the best possible ratio is $\Theta(\log m)$, and the lower bound comes from the special case of [restricted assignment](/restricted-assignment/).

## Definition

There are $m$ machines and a sequence $\sigma$ of $n$ jobs. Job $j$ has a vector $(p_{1j}, \ldots, p_{mj})$ with $p_{ij} \in [0, \infty]$: the time that job $j$ takes on machine $i$, where $p_{ij} = \infty$ means that machine $i$ cannot run job $j$. If $A_i$ is the set of jobs on machine $i$, the load of machine $i$ is $\ell_i = \sum_{j \in A_i} p_{ij}$, and the makespan is $\max_i \ell_i$.

The environment contains the other parallel ones:

| environment | times | page |
|---|---|---|
| identical, $P$ | $p_{ij} = p_j$ | [identical machines](/identical-machines/) |
| uniform, $Q$ | $p_{ij} = p_j / s_i$ | [uniform machines](/uniform-machines/) |
| restricted assignment, $P \mid M_j$ | $p_{ij} \in \{p_j, \infty\}$ | [restricted assignment](/restricted-assignment/) |
| unrelated, $R$ | any $p_{ij}$ | this page |

So every online lower bound for one of the first three is also a lower bound for $R$, and every online upper bound for $R$ holds for the first three.

**What changes online.** In $R \mid \mathrm{online\text{-}list} \mid C_{\max}$, the algorithm sees the whole vector of job $j$ and must choose its machine before it sees job $j + 1$. Two lower bounds that work on $P$ fail here. The bound $\mathrm{OPT} \ge \max_j p_j$ becomes $\mathrm{OPT} \ge \max_j \min_i p_{ij}$, and the average bound $\mathrm{OPT} \ge \frac1m \sum_j \min_i p_{ij}$ can be far below $\mathrm{OPT}$. The algorithm cannot compute $\mathrm{OPT}$ of the jobs seen so far in polynomial time either, so online algorithms for $R$ keep a guess of $\mathrm{OPT}$ and double it when it is too small.

**The greedy rule.** Greedy gives job $j$ to a machine $i$ with the least $\ell_i + p_{ij}$, the machine where it ends first.

**Claim.** Greedy is strictly $m$-competitive on unrelated machines.

*Proof.* Let $M$ be the maximum load before job $j$, and let $k$ be a machine with the least $p_{kj}$. Greedy picks $i$ with $\ell_i + p_{ij} \le \ell_k + p_{kj} \le M + p_{kj}$, so the maximum load grows by at most $\min_k p_{kj}$. Summing over the jobs, $\mathrm{ALG} \le \sum_j \min_k p_{kj}$. If $o(j)$ is the machine of job $j$ in an optimal schedule, then $\sum_j \min_k p_{kj} \le \sum_j p_{o(j) j}$, which is the sum of the $m$ optimal loads, at most $m \cdot \mathrm{OPT}$. $\square$

## Examples and non-examples

**Greedy reaches $m$.** Fix $m$ and a small $\varepsilon > 0$. Job $k$, for $k = 1, \ldots, m - 1$, can run on machine $k$ in time $1$ and on machine $k + 1$ in time $k(1 - \varepsilon)$; the last job $m$ can run only on machine $m$, in time $1$. All other times are $\infty$. For $m = 3$:

| job | time on $M_1$ | time on $M_2$ | time on $M_3$ | greedy compares | greedy loads after |
|---|---|---|---|---|---|
| 1 | $1$ | $1 - \varepsilon$ | $\infty$ | $1$ and $1 - \varepsilon$ | $(0, 1 - \varepsilon, 0)$ |
| 2 | $\infty$ | $1$ | $2 - 2\varepsilon$ | $2 - \varepsilon$ and $2 - 2\varepsilon$ | $(0, 1 - \varepsilon, 2 - 2\varepsilon)$ |
| 3 | $\infty$ | $\infty$ | $1$ | only $M_3$ | $(0, 1 - \varepsilon, 3 - 2\varepsilon)$ |

Each job goes to the next machine because there it ends a little earlier, and the loads pile up on machine $m$. Greedy ends at $m - (m - 1)\varepsilon$, while job $k$ on machine $k$ gives $\mathrm{OPT} = 1$. As $\varepsilon \to 0$ the ratio tends to $m$, so the claim above is tight. With $\varepsilon = \frac1{100}$ the ratios for $m = 2, 3, 4, 5, 6$ are $1.99$, $2.98$, $3.97$, $4.96$ and $5.95$.

**The best online ratio is $\Theta(\log m)$.** Aspnes, Azar, Fiat, Plotkin and Waarts (1997) keep a guess $\Lambda$ of $\mathrm{OPT}$ and give job $j$ to the machine that least increases $\sum_i a^{\ell_i / \Lambda}$ for a constant $a > 1$, doubling $\Lambda$ when the loads get too high. This is $O(\log m)$-competitive. The matching lower bound is the [restricted assignment lower bound](/online-restricted-assignment-lower-bound/): already with $p_{ij} \in \{1, \infty\}$, no deterministic algorithm is better than $\lceil \log_2(m + 1) \rceil$, and no randomized algorithm against an oblivious adversary is better than $\ln m$. Both results are cited here; the lower bounds are proved on their own page.

**Non-examples.**

- A job that needs two machines at once is not in the model: each job runs on exactly one machine.
- Times that depend on the order of the jobs on a machine, as with setup times, are not unrelated machines; the load is a sum of numbers that depend only on the pair (machine, job).
- Uniform machines with speeds are unrelated machines, but not the other way: the table $p_{1,1} = 1$, $p_{2,1} = 2$, $p_{1,2} = 2$, $p_{2,2} = 1$ fits no speeds; see [uniform machines](/uniform-machines/).

## Related definitions

- [Unrelated machine scheduling](/unrelated-machine-scheduling/) and [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/): the offline problem and its LP rounding.
- [Restricted assignment](/restricted-assignment/), with [greedy restricted assignment](/greedy-restricted-assignment/) and [online restricted assignment](/online-restricted-assignment-load-balancing/): the special case that gives the lower bound.
- [Uniform machines](/uniform-machines/) and [identical machines](/identical-machines/): the special cases with constant ratios.
- [Doubling trick](/doubling-trick/): how online algorithms guess $\mathrm{OPT}$.

## References
