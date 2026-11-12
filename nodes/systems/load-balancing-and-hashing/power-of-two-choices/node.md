---
tag: FH6PZB
kind: algorithm
slug: power-of-two-choices
name: Power of two choices
aliases:
- two-choice balancing
- d-choice load balancing
- balanced allocations
- join the shortest of d queues
area: systems/load-balancing-and-hashing
level: core
summary: "Sample two servers (or d) at random and send the job to the less loaded one. The maximum load of n jobs on n servers drops from about ln n / ln ln n to ln ln n / ln 2 + O(1)."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {d: the number of choices per job, n: the number of servers}
  time: {worst: O(d)}
  space: {extra: O(n)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1994
  people: [Yossi Azar, Andrei Z. Broder, Anna R. Karlin, Eli Upfal, Michael Mitzenmacher]
  note: Azar, Broder, Karlin and Upfal proved the ln ln n / ln d bound at STOC 1994 (SIAM J. Comput. 1999); Mitzenmacher analyzed the queueing version in his 1996 thesis (IEEE TPDS 2001).
prereqs: [random-load-balancing, balls-into-bins-max-load]
see_also: [power-of-d-choices-theorem, least-connections, cuckoo-hashing, peak-ewma, load-balancer, balls-into-bins, bounded-load-consistent-hashing, load-skew]
sources:
  - paper: doi:10.1137/S0097539795288490
    title: Yossi Azar, Andrei Z. Broder, Anna R. Karlin and Eli Upfal, Balanced allocations, SIAM Journal on Computing 29(1), 1999
    locator: pp. 180 to 200, the greedy d-choice process and its maximum load ln ln n / ln d + O(1) (conference version STOC 1994)
  - paper: doi:10.1109/71.963420
    title: Michael Mitzenmacher, The power of two choices in randomized load balancing, IEEE Transactions on Parallel and Distributed Systems 12(10), 2001
    locator: pp. 1094 to 1104, the supermarket model, the fixed point lambda^((d^i - 1)/(d - 1)) and the expected time in the system
  - paper: "Berthold Vöcking, How asymmetry helps load balancing, Journal of the ACM 50(4), 2003"
    locator: pp. 568 to 589, the Always-Go-Left rule and the bound ln ln n / (d ln phi_d) + O(1)
  - paper: doi:10.1137/S009753970444435X
    title: Petra Berenbrink, Artur Czumaj, Angelika Steger and Berthold Vöcking, Balanced allocations, the heavily loaded case, SIAM Journal on Computing 35(6), 2006
    locator: pp. 1350 to 1385, the gap ln ln n / ln d + O(1) for any number m of balls
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 17, Section 17.1 (the power of two choices)
---

The power of two choices is a randomized [load balancing](/load-balancing-problem/) rule: for each arriving job, sample $d \ge 2$ servers uniformly at random and send the job to the one with the least load. With $n$ jobs on $n$ servers, the busiest server then holds $\ln\ln n/\ln d + O(1)$ jobs with high probability, against $(1 + o(1))\ln n/\ln\ln n$ for one random choice ([Azar, Broder, Karlin and Upfal](/power-of-d-choices-theorem/)). The second choice gives an exponential improvement, and each further choice only a constant factor. The rule needs no central state, only $d$ load probes per job, so load balancers and schedulers use it widely.

## In plain words

You stand in a supermarket with many checkout lines. If you pick a line at random, some lines get long by bad luck. If you look at two random lines and join the shorter one, long lines become very rare: a line can only grow when both lines you looked at were already long, and that is much less likely than one long line.

Looking at two lines is enough for most of the gain. Looking at three or four helps a little more. Looking at all of them is the best, but it costs a look at every line for every customer.

## The problem

There are $n$ servers (bins) and a stream of jobs (balls). Each server has a load, the number of jobs it holds now. Each job must go to one server when it arrives, without knowledge of the future jobs. The goal is a small maximum load, or a small time in the system when jobs also finish. This is the online, dynamic form of the [load balancing problem](/load-balancing-problem/). The analysis assumes that the samples are independent and uniform and that the probed loads are current.

## The algorithm

```pseudo id=main
TWO-CHOICE-PLACE(load, d)                  ▷ load[0 .. n − 1] holds the current loads
L1  best ← RANDOM(0, n − 1)
L2  for r ← 2 to d do
L3      b ← RANDOM(0, n − 1)               ▷ independent and uniform
L4      if load[b] < load[best] then best ← b
L5  load[best] ← load[best] + 1
L6  return best
```

The samples are drawn with replacement, as in the analysis of Azar et al., so two samples can be the same bin. A tie goes to the bin sampled first; the bound holds for any rule of ties. In a server pool the load is the number of open requests, and it falls by 1 when a request completes. With $d = 1$ the procedure is [random load balancing](/random-load-balancing/), and with $d = n$ and no repeats it is join the shortest queue, which is [least connections](/least-connections/).

## Example

Four servers, six jobs, $d = 2$. The samples of each job are fixed in advance.

| job | samples | loads of the samples | chosen | loads after |
| --- | --- | --- | --- | --- |
| 1 | 0, 1 | 0, 0 | 0 (tie) | 1 0 0 0 |
| 2 | 0, 2 | 1, 0 | 2 | 1 0 1 0 |
| 3 | 1, 2 | 0, 1 | 1 | 1 1 1 0 |
| 4 | 3, 3 | 0, 0 | 3 | 1 1 1 1 |
| 5 | 0, 3 | 1, 1 | 0 (tie) | 2 1 1 1 |
| 6 | 2, 1 | 1, 1 | 2 (tie) | 2 1 2 1 |

The final maximum is 2. With one choice, the first sample of each job gives the loads $3, 1, 1, 1$ from the samples 0, 0, 1, 3, 0, 2, and a maximum of 3.

**Maximum load for $m = n$.** Seeded runs (Python `random.Random(5)`; 200, 50, 10 and 3 runs for the four sizes), as the mean and the range of the maximum:

| $n$ | $d = 1$ | $d = 2$ | $d = 3$ | $d = 4$ | Always-Go-Left, $d = 2$ | $\ln\ln n/\ln 2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $10^3$ | 5.53 (4 to 8) | 3.00 (3) | 2.40 (2 to 3) | 2.04 (2 to 3) | 2.98 (2 to 3) | 2.79 |
| $10^4$ | 6.58 (6 to 8) | 3.08 (3 to 4) | 3 | 2.22 (2 to 3) | 3 | 3.20 |
| $10^5$ | 7.70 (7 to 10) | 3.40 (3 to 4) | 3 | 3 | 3 | 3.53 |
| $10^6$ | 8.67 (8 to 9) | 4 | 3 | 3 | 3 | 3.79 |

**More jobs than servers.** With $n = 1000$ servers and $m = 50n$ or $100n$ jobs (seed 6), two choices keep the maximum at most 3 above the mean $m/n$. One choice puts the maximum about 34 above the mean at $m = 100n$, since its excess grows like $\sqrt{2(m/n)\ln n}$ ([maximum load of balls into bins](/balls-into-bins-max-load/)).

## Correctness

The rule is correct when it places each job on a least loaded sampled server. By a [loop invariant](/loop-invariant/) of line L2, after each round $best$ is the first sampled bin of least load (Lemma 1 of the proof). The key fact of the analysis follows at once: if $\nu_i$ servers have load at least $i$, a new job lands on such a server with probability exactly $(\nu_i/n)^d$, because all $d$ samples must hit them (Lemma 2). For one choice it is $\nu_i/n$. This squaring at each level is what turns the bound $\ln n/\ln\ln n$ into $\ln\ln n/\ln d$. The full proofs, and the fixed point of the supermarket model below, are in the proof file.

## Complexity

- **Time per job.** $O(d)$: $d$ random numbers and $d - 1$ comparisons of loads, in the [word RAM](/word-ram/). In a real system the cost is $d$ load probes, which may be messages.
- **Space.** $O(n)$ for the loads, or none at all if each server reports its own load when probed.
- **Maximum load, $m = n$.** $\ln\ln n/\ln d + O(1)$ with probability $1 - o(1/n)$, and at least $\ln\ln n/\ln d - O(1)$ with the same probability ([power of d choices theorem](/power-of-d-choices-theorem/)). This is a bound with high probability, over the random samples, for any order of ties.
- **Maximum load, any $m$.** $m/n + \ln\ln n/\ln d + O(1)$ with high probability (Berenbrink, Czumaj, Steger and Vöcking). The gap to the mean does not grow with $m$. With one choice it grows like $\sqrt{m\ln n/n}$.
- **Supermarket model.** Jobs arrive as a Poisson stream of rate $\lambda n$, $\lambda < 1$, and each server works at rate 1 with exponential service times. As $n \to \infty$, the fraction of queues with at least $i$ jobs tends at equilibrium to $s_i = \lambda^{(d^i - 1)/(d-1)}$, against $\lambda^i$ for one choice (Mitzenmacher). By Little's law the expected time in the system is $T_d(\lambda) = \sum_{i \ge 1} \lambda^{(d^i - d)/(d-1)}$.

| $\lambda$ | $T_1 = 1/(1-\lambda)$ | $T_2$ | $T_3$ |
| --- | --- | --- | --- |
| 0.5 | 2 | 1.266 | 1.125 |
| 0.9 | 10 | 2.614 | 2.028 |
| 0.99 | 100 | 5.432 | 3.858 |

A seeded simulation of 100 servers at $\lambda = 0.9$ with $d = 2$ (seed 7, 200000 events after 20000 events of warm-up) gives the fractions 0.899, 0.729, 0.481, 0.215 and 0.046 for $i = 1, \ldots, 5$, against the limit values 0.9, 0.729, 0.478, 0.206 and 0.038.

## Properties

- **Online.** Each job is placed when it arrives, from the current loads only.
- **Randomized.** The bound holds with high probability over the samples, for every arrival sequence of equal jobs. It does not hold against an adversary who sees the samples.
- **Stateless dispatcher.** The dispatcher keeps no table; it needs only the loads of the $d$ sampled servers.
- **Robust to ties.** Any tie rule keeps the bound. A fixed asymmetric tie rule improves it (Always-Go-Left).

## Variants and improvements

- **More choices.** $d$ choices give $\ln\ln n/\ln d + O(1)$. Going from $d = 2$ to $d = 3$ divides the leading term by $\ln 3/\ln 2 = 1.58$ only.
- **Always-Go-Left.** Split the servers into $d$ groups of equal size, sample one server in each group, and break a tie toward the leftmost group. Vöcking proved the maximum load $\ln\ln n/(d\ln\phi_d) + O(1)$, where $\phi_d$ is the growth rate of the $d$-step Fibonacci numbers ($\phi_2 = 1.618$, so $d\ln\phi_d = 0.962$ against $\ln 2 = 0.693$).
- **Weighted jobs and servers of different speed.** Compare load divided by speed, as in [weighted random load balancing](/weighted-random-load-balancing/). The bounds then depend on the weight distribution.
- **Two choices in hashing.** In two-choice hashing each key goes to the shorter of two buckets, so the longest chain is $O(\log\log n)$. [Cuckoo hashing](/cuckoo-hashing/) also uses two candidate cells per key, but each cell holds one key and an insert may move older keys to their other cell; its question is whether all keys fit, with a load threshold of $1/2$ for two tables ([cuckoo hashing load threshold](/cuckoo-hashing-load-threshold/)). The two-choice rule never moves a placed job, and bins have no capacity.
- **Two choices on a hash ring.** Hash each key with two hash functions and store it on the less loaded of the two servers, as in [bounded-load consistent hashing](/bounded-load-consistent-hashing/) and related schemes.
- **Sampling with latency.** Production balancers compare a latency estimate instead of a count, as in [peak EWMA](/peak-ewma/).

## When to use it

Use two choices when a dispatcher can probe the load of a server cheaply but cannot keep a global view of all servers, for example with many independent dispatchers or a very large pool. It is close to [least connections](/least-connections/) in quality at a cost of two probes instead of $n$, and it is far better than [random load balancing](/random-load-balancing/) or a plain hash. Use [round robin](/round-robin-load-balancing/) when jobs are equal and one dispatcher sees all of them, since round robin then gives exact balance. Use a hash scheme such as [consistent hashing](/consistent-hashing/) when a key must always go to the same server, since two choices sends equal keys to different servers.

## Pitfalls

- **Stale loads.** If many dispatchers act on old load reports, they all pick the same lightly loaded server, and it becomes the busiest. The analysis assumes the loads are current. Count the jobs sent but not yet reported, or use fewer choices when the information is old.
- **Sampling the same server twice.** Sampling with replacement wastes a probe with probability $1/n$. This does not change the bound, but for very small pools sample without replacement.
- **Ties toward one side by accident.** A tie rule that always picks the lower index, with samples that are not uniform, puts extra load on low indices. Break ties by the order of the samples, or use the deliberate Always-Go-Left grouping.
- **Comparing loads of servers of different speed.** A fast server with 4 jobs may be less loaded than a slow server with 2. Compare load divided by capacity.
- **Expecting balance for one key.** The rule balances counts of jobs. It does not keep a session or a cache key on one server.

## Implementations

The Python file has the d-choice rule, Always-Go-Left, and a simulation of the supermarket model by uniformization: each event is an arrival with probability $\lambda/(\lambda + 1)$, else a service at a uniform server.

## History

Azar, Broder, Karlin and Upfal introduced the greedy $d$-choice process and proved the bound $\ln\ln n/\ln d + O(1)$ at STOC 1994; the journal version appeared in 1999. Mitzenmacher studied the dynamic version with queues in his 1996 Berkeley thesis, titled "The power of two choices in randomized load balancing", and proved the fixed point of the supermarket model with the method of differential equations. Vöcking showed in 2003 that asymmetric tie breaking improves the constant. Berenbrink, Czumaj, Steger and Vöcking proved in 2006 that the gap does not grow with the number of balls.

## References
