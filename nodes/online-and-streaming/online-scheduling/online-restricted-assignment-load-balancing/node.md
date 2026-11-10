---
tag: TBNYZG
kind: problem
slug: online-restricted-assignment-load-balancing
name: Online restricted assignment load balancing
aliases:
- online load balancing with restricted assignment
- online restricted assignment
- P|online-list, M_j|Cmax
area: online-and-streaming/online-scheduling
level: advanced
summary: "Online makespan minimization where each job can run only on its eligible machines. The optimal ratio is Theta(log m) for deterministic and for randomized algorithms."
prereqs: [restricted-assignment, online-makespan-minimization]
see_also: [restricted-assignment, greedy-restricted-assignment, online-restricted-assignment-lower-bound, unrelated-machines, online-makespan-minimization, power-of-two-choices, load-balancing-problem, bipartite-matching]
sources:
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    title: Azar, Naor and Rom 1995
    locator: the model, the greedy upper bound of about log2 m, the deterministic lower bound of about log2 m and the randomized lower bound ln m
  - paper: "Yossi Azar, On-line load balancing, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Azar 1998, survey chapter
    locator: the sections on restricted assignment, on temporary tasks, and on the Robin Hood algorithm
  - paper: "Fu-Hong Liu, Hsiang-Hsuan Liu and Prudence W. H. Wong, Greedy is optimal for online restricted assignment and smart grid scheduling for unit size jobs, WAOA 2019"
    title: Liu, Liu and Wong 2019
    locator: the result that greedy is an optimal deterministic online algorithm for restricted assignment with unit jobs
  - paper: "Yossi Azar, Andrei Z. Broder and Anna R. Karlin, On-line load balancing, Theoretical Computer Science 130(1), 1994"
    title: Azar, Broder and Karlin 1994
    locator: the lower bound of order sqrt(m) for restricted assignment with temporary tasks of unknown duration
  - paper: "James Aspnes, Yossi Azar, Amos Fiat, Serge Plotkin and Orli Waarts, On-line routing of virtual circuits with applications to load balancing and machine scheduling, Journal of the ACM 44(3), 1997"
    title: Aspnes, Azar, Fiat, Plotkin and Waarts 1997
    locator: the O(log m) algorithm for unrelated machines, which contains restricted assignment
---

Online restricted assignment is [online makespan minimization](/online-makespan-minimization/) with [eligibility sets](/restricted-assignment/): each job comes with a size and a set of machines that may run it, and the algorithm must choose one of these machines at once. On identical machines without sets, the best ratio is a constant below 2. With sets, it grows like $\log m$, and this is true for deterministic algorithms and for randomized ones. The [greedy algorithm](/greedy-restricted-assignment/) reaches $\lceil \log_2 m \rceil + 1$, and the [lower bound](/online-restricted-assignment-lower-bound/) shows that $\lceil \log_2(m + 1) \rceil$ is needed.

## In plain words

Tasks arrive one at a time, and each task can only go to some of the workers, for example the workers who have the right tool. You must pick one of the allowed workers before you see the next task. The goal is that no worker gets too much work. The trouble is that you do not know which workers will be the only choice for later tasks. A clever opponent sees where you put each task and then sends tasks that only your busy workers can take. Each round of this trick halves the number of workers in play and adds one task to the busiest one, so the damage grows with the number of rounds, which is about the number of times the workers can be halved.

## Definition

**Input.** A number $m$ of machines, and a request sequence $\sigma$ of jobs. Job $t$ has a size $p_t \ge 0$ and a nonempty set $M_t \subseteq \{1, \ldots, m\}$ of eligible machines. The number $n$ of jobs is not known in advance.

**Online rule.** When job $t$ is shown, the algorithm assigns it to a machine $a_t \in M_t$, using only the jobs up to $t$. The choice is final.

**Cost.** $\mathrm{ALG}(\sigma) = \max_i \sum_{t :\, a_t = i} p_t$. $\mathrm{OPT}(\sigma)$ is the least makespan over all assignments with $a_t \in M_t$ for all $t$.

**Measure.** An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$; strictly so if $b = 0$. A randomized algorithm is measured by $\mathbb{E}[\mathrm{ALG}(\sigma)]$ against an [oblivious adversary](/oblivious-adversary/), who fixes $\sigma$ without seeing the coin flips.

## Variants

- **Unit jobs**, $p_t = 1$: the case of the lower bounds. On unit jobs with $\mathrm{OPT} = 1$, greedy has makespan at most $\lfloor \log_2 m \rfloor + 1 = \lceil \log_2 (m + 1) \rceil$, the deterministic lower bound ([greedy restricted assignment](/greedy-restricted-assignment/)). Liu, Liu and Wong (2019) show that greedy is optimal for unit jobs in general (cited).
- **Temporary tasks**: jobs also leave, at times not known in advance, and the load is measured at each moment. Then the optimal deterministic ratio is $\Theta(\sqrt m)$; the lower bound is due to Azar, Broder and Karlin (1994), and the Robin Hood algorithm reaches $O(\sqrt m)$ (cited).
- **Random sets**: if each $M_t$ is a random set of $d \ge 2$ machines, greedy gives a maximum load near $\frac{\ln \ln m}{\ln d}$ for $m$ unit jobs. This is the [power of two choices](/power-of-two-choices/).
- **Reassignment**: if the algorithm may move a few earlier jobs, constant ratios become possible.
- **Unrelated machines**: the general case [$R \mid \mathrm{online\text{-}list} \mid C_{\max}$](/unrelated-machines/), still $\Theta(\log m)$.

## Examples

**The pair adversary on four machines.** Run [greedy](/greedy-restricted-assignment/), with ties to the lowest index, against the adversary of the [lower bound](/online-restricted-assignment-lower-bound/). All jobs have size $1$.

| job | eligible set | greedy loads before | greedy picks | loads after |
|---|---|---|---|---|
| 1 | $\{1, 2\}$ | (0, 0, 0, 0) | 1 | (1, 0, 0, 0) |
| 2 | $\{3, 4\}$ | (1, 0, 0, 0) | 3 | (1, 0, 1, 0) |
| 3 | $\{1, 3\}$ | (1, 0, 1, 0) | 1 | (2, 0, 1, 0) |
| 4 | $\{1\}$ | (2, 0, 1, 0) | 1 | (3, 0, 1, 0) |

In each round the adversary pairs the machines that greedy chose in the round before. Greedy ends with load $3$, while the assignment $1 \to 2$, $2 \to 4$, $3 \to 3$, $4 \to 1$ has every load equal to $1$. The ratio is $3 = \lceil \log_2 5 \rceil$. The same adversary works against every deterministic rule, since it only uses the rule's choices.

## Known algorithms

| algorithm | ratio | source |
|---|---|---|
| [greedy](/greedy-restricted-assignment/): least load among the eligible machines | $\lceil \log_2 m \rceil + 1$; makespan $\lfloor \log_2 m \rfloor + 1$ on unit jobs with $\mathrm{OPT} = 1$ | Azar, Naor and Rom 1995, proved on the [algorithm page](/greedy-restricted-assignment/) |
| exponential-function algorithm for unrelated machines | $O(\log m)$ | Aspnes, Azar, Fiat, Plotkin and Waarts 1997, cited |

Greedy is the simplest algorithm with the right order of growth, and for unit jobs it is exactly optimal among deterministic algorithms (Liu, Liu and Wong 2019, cited).

## Bounds

| class of algorithms | lower bound | upper bound | status |
|---|---|---|---|
| deterministic | $\lceil \log_2 (m + 1) \rceil$ | $\lceil \log_2 m \rceil + 1$ | both proved on this site |
| randomized, oblivious adversary | $\ln m$ | $\lceil \log_2 m \rceil + 1$ | both proved on this site |

So the optimal ratio is $\Theta(\log m)$ in both classes. The lower bounds are on the [lower bound page](/online-restricted-assignment-lower-bound/), and the upper bound is on the [greedy page](/greedy-restricted-assignment/). Randomization can gain at most a constant factor: since $\ln m = (\ln 2) \log_2 m \approx 0.69 \log_2 m$, the gain is asymptotically at most a factor $\frac1{\ln 2} \approx 1.44$.

For deterministic algorithms the two bounds are equal when $m$ is a power of two: for $m = 2^k$ both are $k + 1$. Otherwise they differ by $1$, since $\lceil \log_2 (m + 1) \rceil = \lfloor \log_2 m \rfloor + 1$. On the instances of the lower bound, unit jobs with $\mathrm{OPT} = 1$, greedy reaches $\lfloor \log_2 m \rfloor + 1$, so there the bounds meet for every $m$.

## Reductions

- **Contains identical machines.** With $M_t = \{1, \ldots, m\}$ for all $t$, the problem is $P \mid \mathrm{online\text{-}list} \mid C_{\max}$.
- **Contained in unrelated machines.** Put $p_{it} = p_t$ for $i \in M_t$ and $p_{it} = \infty$ otherwise; then every lower bound here holds for [unrelated machines](/unrelated-machines/).
- **Unit jobs and matching.** For unit jobs, an assignment with maximum load $L$ is a [bipartite](/bipartite-matching/) $b$-matching that covers each job, with capacity $L$ at each machine, so the offline optimum is a flow computation.

## Applications

- Assigning mobile users to base stations within reach, the motivation of Azar, Naor and Rom.
- Sending requests to servers that hold a copy of the data, where the copies define the eligible set.
- Placing virtual circuits or tasks in networks where only some resources can serve each request, the setting of Aspnes et al.

## References
