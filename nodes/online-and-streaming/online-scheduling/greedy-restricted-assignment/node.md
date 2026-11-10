---
tag: FJFX7X
kind: algorithm
slug: greedy-restricted-assignment
name: Greedy restricted assignment
aliases:
- greedy online restricted assignment
- greedy load balancing with assignment restrictions
- least loaded eligible machine
area: online-and-streaming/online-scheduling
level: advanced
summary: "Assign each job to the eligible machine of least load. This is strictly (ceil(log2 m) + 1)-competitive for online restricted assignment, and no deterministic algorithm is better by more than 1."
solves: [online-restricted-assignment-load-balancing]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines, s: the total size of the eligible sets}
  time: {worst: Θ(s + m)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1992
  people: [Yossi Azar, Joseph Naor, Raphael Rom]
  note: "Azar, Naor and Rom analyzed the greedy rule for online assignment with restricted sets at SODA 1992, and the journal version appeared in 1995."
prereqs: [online-restricted-assignment-load-balancing, restricted-assignment, greedy-algorithm]
see_also: [online-restricted-assignment-lower-bound, restricted-assignment, online-restricted-assignment-load-balancing, list-scheduling, list-scheduling-competitive-ratio, unrelated-machines, power-of-two-choices, load-balancing-problem]
sources:
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    title: Azar, Naor and Rom 1995
    locator: the analysis of the greedy algorithm for assignment with restricted sets and its bound of about log2 m
  - paper: "Yossi Azar, On-line load balancing, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Azar 1998, survey chapter
    locator: the section on the restricted assignment model, the greedy upper bound
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the greedy algorithm for restricted assignment
  - paper: "Fu-Hong Liu, Hsiang-Hsuan Liu and Prudence W. H. Wong, Greedy is optimal for online restricted assignment and smart grid scheduling for unit size jobs, WAOA 2019"
    title: Liu, Liu and Wong 2019
    locator: the result that greedy is an optimal deterministic online algorithm for restricted assignment with unit jobs
---

Greedy restricted assignment puts each arriving job on the machine of least load among the machines that may run it. It is the rule of [list scheduling](/list-scheduling/), applied to [restricted assignment](/restricted-assignment/), where each job has a set of eligible machines. For [online restricted assignment](/online-restricted-assignment-load-balancing/) it is strictly $(\lceil \log_2 m \rceil + 1)$-competitive, for every order of the jobs and every rule for ties. Since no deterministic online algorithm is better than $\lceil \log_2 (m + 1) \rceil$ ([lower bound](/online-restricted-assignment-lower-bound/)), greedy is optimal up to an additive $1$, and exactly optimal on unit jobs.

## In plain words

Each task can go only to some workers. When a task comes, look at the workers who may take it, and give it to the one with the least work so far. Never move a task later. This rule can be fooled: a clever opponent can make the busiest worker a little busier in each of a few rounds. But each round needs twice as many workers as the next one, so the number of rounds is small. The result is that the busiest worker never has more than a few times the work of the best plan, where "a few" grows like the number of times you can halve the number of workers.

## The problem

There are $m$ machines and a request sequence $\sigma$ of $n$ jobs. Job $t$ has a size $p_t \ge 0$ and a nonempty set $M_t \subseteq \{1, \ldots, m\}$ of eligible machines. When job $t$ comes, it must go to a machine of $M_t$ before job $t + 1$ is seen, and it stays there. The cost $\mathrm{ALG}(\sigma)$ is the largest load, and $\mathrm{OPT}(\sigma)$ is the least largest load of any assignment that respects the sets. An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, and strictly so if $b = 0$. This is the problem $P \mid \mathrm{online\text{-}list}, M_j \mid C_{\max}$.

## The algorithm

```pseudo id=main
GREEDY-RESTRICTED-ASSIGNMENT(m, σ)
L1  for i ← 1 to m do ℓ[i] ← 0
L2  for each job t = (p_t, M_t) of σ, in order of arrival do
L3      i ← a machine of M_t with the least ℓ[i]       ▷ ties: the lowest index
L4      a[t] ← i                                       ▷ final, never changed
L5      ℓ[i] ← ℓ[i] + p_t
L6  return a and max_i ℓ[i]
```

The algorithm keeps only the vector of loads. It does not need $\mathrm{OPT}$, the number of jobs, or any parameter. On eligible machines a job has the same size, so the machine of least load is also the machine where the job ends first.

## Example

Take $m = 3$ and five jobs. Ties go to the lowest index.

| job $t$ | $p_t$ | $M_t$ | loads before | line L3 picks | loads after |
|---|---|---|---|---|---|
| 1 | 2 | $\{1, 2, 3\}$ | (0, 0, 0) | 1 | (2, 0, 0) |
| 2 | 2 | $\{1, 2\}$ | (2, 0, 0) | 2 | (2, 2, 0) |
| 3 | 1 | $\{2, 3\}$ | (2, 2, 0) | 3 | (2, 2, 1) |
| 4 | 3 | $\{1\}$ | (2, 2, 1) | 1 | (5, 2, 1) |
| 5 | 2 | $\{3\}$ | (5, 2, 1) | 3 | (5, 2, 3) |

Greedy ends with makespan $5$. The optimum is $4$: jobs 1 and 2 on machine 2, job 4 on machine 1, jobs 3 and 5 on machine 3 give loads $(3, 4, 3)$, and no assignment is below $4$, because the total size is $10 > 3 \cdot 3$ and the loads are integers. Greedy lost because job 1 went to machine 1, which job 4 needed later. The ratio $\frac54$ is well below the bound $\lceil \log_2 3 \rceil + 1 = 3$; the [pair adversary](/online-restricted-assignment-load-balancing/) shows how an adversary gets close to the bound.

## Correctness

**Theorem (Azar, Naor and Rom).** For every $m \ge 1$ and every sequence $\sigma$, with any rule for ties in line L3,
$$\mathrm{ALG}(\sigma) \le \big(\lceil \log_2 m \rceil + 1\big) \cdot \mathrm{OPT}(\sigma).$$
If all jobs have size $1$ and $\mathrm{OPT}(\sigma) = 1$, then $\mathrm{ALG}(\sigma) \le \lfloor \log_2 m \rfloor + 1$.

The proof views the greedy schedule as stacks of intervals, one stack per machine, and lets $V(x)$ be the total amount of work above height $x$. Scale so that $\mathrm{OPT} = L^*$. A band lemma shows that for each machine $j$, the work of greedy in the band $[x, x + L^*]$ on machine $j$ is at least the work above height $x + L^*$ of the jobs that the optimum puts on $j$. The reason is the choice in line L3: when such a job was placed high, machine $j$ was eligible and at least as loaded. Summing over $j$ gives $V(x + L^*) \le \frac12 V(x)$. Since $V(0) \le m L^*$, after $\lceil \log_2 m \rceil$ halvings at most $L^*$ of work is left above height $\lceil \log_2 m \rceil L^*$, so no machine ends above $(\lceil \log_2 m \rceil + 1) L^*$. The full proof, and the proof of the unit case, are in the proof file.

## Complexity

Line L1 takes $\Theta(m)$ time. Line L3 scans $M_t$, in $\Theta(|M_t|)$ time, and lines L4 and L5 take $O(1)$. The total time is $\Theta(m + s)$ with $s = \sum_t |M_t| \ge n$, which is the size of the input. The algorithm stores the $m$ loads, so the extra space is $\Theta(m)$, besides the output.

If the sets are long intervals of machine indices, a segment tree over the loads finds the least load in a range in $O(\log m)$ time per job instead of $\Theta(|M_t|)$.

## Properties

- **Online and final.** Each decision uses only the jobs seen so far, and no job moves later.
- **Strict guarantee at every moment.** The theorem applies to each prefix of $\sigma$, so the bound holds whenever the sequence stops.
- **Deterministic.** With a fixed tie rule, the output is a function of $\sigma$. The bound holds for every tie rule.
- **Contains list scheduling.** If every $M_t$ is the set of all machines, greedy is [list scheduling](/list-scheduling/), and then the better bound $2 - \frac1m$ holds ([Graham's bound](/list-scheduling-competitive-ratio/)).
- **Near optimal.** The [lower bound](/online-restricted-assignment-lower-bound/) $\lceil \log_2 (m + 1) \rceil$ for every deterministic algorithm differs from the bound of greedy by at most $1$, and the two are equal when $m$ is a power of two.

## Variants and improvements

- **Unrelated machines.** Greedy that picks the machine where the job ends first is only $m$-competitive on [unrelated machines](/unrelated-machines/). The exponential-function algorithm of Aspnes, Azar, Fiat, Plotkin and Waarts is $O(\log m)$ there.
- **Random sets.** If each set is $d \ge 2$ machines chosen at random, the same rule gives a maximum load near $\frac{\ln \ln m}{\ln d}$ for $m$ unit jobs: the [power of two choices](/power-of-two-choices/).
- **Temporary jobs.** If jobs also leave, greedy is not enough; the Robin Hood algorithm reaches $O(\sqrt m)$, the optimal order for that model.
- **Reassignment.** If the algorithm may move a few jobs later, constant ratios become possible.
- **Unit jobs.** Liu, Liu and Wong (2019) show that greedy is an optimal deterministic online algorithm for unit jobs (cited).

## When to use it

Use greedy when jobs must be placed at once on servers or machines that can serve only some of them, and when no information about the future is available. It needs no parameter and no estimate of $\mathrm{OPT}$, and it is within one of the best possible deterministic ratio. Expect a $\log m$ loss only against an adversary that chooses the sets; with random or well-mixed sets it usually does far better. If jobs leave, or if their sizes differ between machines, use an algorithm for that model instead.

## Pitfalls

- **The global least load.** The machine of least load overall may not be in $M_t$. Line L3 must take the minimum over $M_t$ only, or the assignment breaks the constraints.
- **Hoping for a constant ratio.** No deterministic online algorithm, and no randomized one, has a ratio that does not grow with $m$. A ratio near $\log_2 m$ in a test is not a bug of the implementation.
- **Ties matter for the output, not for the bound.** Different tie rules give different schedules, and an adversary can exploit a fixed rule, but the theorem holds for each rule.
- **Comparing with the average load.** The average $\frac1m \sum_t p_t$ is not a lower bound of the right size for $\mathrm{OPT}$ here: all jobs may be eligible on one machine only. Tests must compare with the true optimum.

## Implementations

## History

Azar, Naor and Rom presented the analysis at SODA 1992 and in the Journal of Algorithms in 1995, with the motivation of mobile users that can reach only nearby base stations. They proved that greedy is within one of $\log_2 m$ and that no online algorithm does much better, deterministic or randomized. Aspnes, Azar, Fiat, Plotkin and Waarts (1997) extended the $O(\log m)$ bound to unrelated machines with a different algorithm. Liu, Liu and Wong (2019) showed that greedy is exactly optimal for unit jobs.

## References
