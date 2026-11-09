---
tag: JWD170
kind: algorithm
slug: random-restart-hill-climbing
name: Random-restart hill climbing
aliases:
- multi-start local search
- multistart hill climbing
- random restarts
- multistart method
area: optimization/metaheuristics
level: intro
summary: Run hill climbing from many random starts and keep the best result.
solves: [local-search-problem]
model: word-ram
complexity:
  vars: {R: the number of runs, H: the time of one run of hill climbing, s: the size of one solution}
  time: {worst: O(R H)}
  space: {extra: O(s)}
properties: {deterministic: false, recursive: false}
prereqs: [hill-climbing, local-optimum, geometric-distribution]
see_also: [iterated-local-search, grasp, stochastic-local-search, simulated-annealing, fitness-landscape, las-vegas-algorithm]
sources:
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Chapter 2 (restart as an escape mechanism) and Section 4.1, In Depth, Probabilistic Approximate Completeness and Convergence, from p. 155
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 4, Section 4.1 (random-restart hill climbing; the expected number of restarts is 1/p)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 7, Intelligent Multi-Start Methods, by R. Martí, R. Aceves, M. T. León, J. M. Moreno-Vega and A. Duarte, pp. 221 to 243
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C.4 (the geometric distribution and its mean)
  - paper: doi:10.1016/0020-0190(93)90029-9
    title: Michael Luby, Alistair Sinclair and David Zuckerman, Optimal speedup of Las Vegas algorithms, Information Processing Letters 47(4), 1993
    locator: pp. 173 to 180 (the universal restart schedule)
  - paper: "Shen Lin, Computer solutions of the traveling salesman problem, Bell System Technical Journal 44(10), 1965"
    locator: pp. 2245 to 2269 (3-opt from many random starting tours)
---

Random-restart hill climbing runs [hill climbing](/hill-climbing/) many times, each time from an independent random start, and returns the best [local optimum](/local-optimum/) that the runs reach. It is the simplest way to escape a bad local optimum: do not escape, start again somewhere else. Unlike most [metaheuristics](/metaheuristic/), it has a clean guarantee: if one run ends at a global optimum with probability $p$, then $R$ runs all miss it with probability exactly $(1-p)^R$. The catch is that $p$ is unknown and can be exponentially small.

## In plain words

Hill climbing walks downhill and stops in the first hollow it finds. Which hollow that is depends on where it starts. So start many times, from places picked at random, and keep the lowest hollow you find.

If one walk finds the lowest hollow with some fixed chance, then many walks all miss it only with a small chance, because each walk is a new try. Two walks with a fair chance each miss together only a quarter of the time. The problem is that you do not know that chance. On a field with many tiny hollows and one narrow deep one, almost every walk ends in the wrong place, and the restarts help little.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a [neighborhood](/neighborhood-structure/) $N$, a way to draw a random start from a distribution $D$ on $S$, and a number of runs $R \ge 1$. An optional target $\tau$ stops the search early. The output is a [local minimum](/local-optimum/) of $N$, the best of those that the runs reach. The aim is a global minimum, $f(x) = f^* = \min_S f$, but the algorithm can prove only local optimality.

## The algorithm

```pseudo id=main
RANDOM-RESTART(f, N, D, R, τ)            ▷ τ is an optional target value
L1  b ← none
L2  for r ← 1 to R do
L3      x0 ← a random start drawn from D, independent of all earlier draws
L4      x ← HILL-CLIMBING(x0, f, N)
L5      if b = none or f(x) < f(b) then b ← x
L6      if τ is given and f(b) ≤ τ then leave the loop
L7  return b
```

Each pass draws a new start (line L3), runs [hill climbing](/hill-climbing/) to a local minimum (line L4), and keeps the best end so far (line L5). Line L6 stops early when the best end is good enough, for example when $\tau$ is a known lower bound on $f$. The runs share nothing, so they can run in parallel.

## Example

Take the Max-Cut instance of the [hill climbing](/hill-climbing/) page: six vertices, ten weighted edges, total weight 22, and $f(x)$ the uncut weight of the split $x \in \{0,1\}^6$. Hill climbing uses best improvement with single flips. The global minimum is $f^* = 3$. Draw each start uniformly with a fixed seed (11 in the Python code below), and make four runs.

| run | start $x_0$ | end $x$ | $f(x)$ | best $f(b)$ |
|---|---|---|---|---|
| 1 | 111001 | 011001 | 6 | 6 |
| 2 | 001100 | 001110 | 7 | 6 |
| 3 | 011000 | 011001 | 6 | 6 |
| 4 | 000001 | 010101 | 3 | 3 |

Three runs end at local minima that are not global. The fourth ends at the optimum 010101.

On this instance we can compute $p$ exactly. Of the 64 starts, 44 lead hill climbing to a global minimum, so $p = 44/64 = 11/16$. The chance that all $R$ runs miss the optimum is $(5/16)^R$:

| $R$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $\Pr[\text{miss}] = (5/16)^R$ | 0.3125 | 0.0977 | 0.0305 | 0.0095 | 0.0030 |
| bound $e^{-pR}$ | 0.503 | 0.253 | 0.127 | 0.064 | 0.032 |

For a miss probability of at most $\delta = 0.01$, the exact value needs $R = 4$ runs. The simpler bound $R \ge \ln(1/\delta)/p$ asks for $R = 7$. The expected number of runs until the first success is $1/p = 16/11 \approx 1.45$.

## Correctness

Two claims. First, the algorithm returns a local minimum $b$ with $f(b)$ equal to the least value among the ends of the runs it made; this follows from the correctness of hill climbing and the invariant of line L5. Second, a probability bound: if each run ends in a good set $G = \{x : f(x) \le \tau\}$ with probability $p > 0$, then

$$\Pr[b \notin G] = (1 - p)^R \le e^{-pR},$$

so $R \ge \ln(1/\delta)/p$ runs suffice for a miss probability of at most $\delta$, and the expected number of runs until the first good end is $1/p$. The key step is that $b$ misses $G$ exactly when every run misses $G$, and the runs are independent. With a uniform start, a start that is already optimal stays there, so $p \ge |G|/|S| > 0$ and the miss probability tends to 0. Hoos and Stützle call an algorithm with this property *probabilistically approximately complete*. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

The time is the sum of the times of the runs: $O(R H)$, where $H$ is a bound on the time of one run of hill climbing. The bound $H$ itself can be exponential in the input size (see the [hill climbing](/hill-climbing/) page), but on many instances a run takes a few passes. The extra space is a constant number of solutions (the start, the current solution and the best one), so $O(s)$ for solutions of size $s$.

The number of runs that the guarantee needs depends on $p$:

- $R = \lceil \ln(1/\delta) / p \rceil$ runs give a miss probability of at most $\delta$.
- The expected number of runs to the first success is $1/p$, from the mean of the [geometric distribution](/geometric-distribution/).
- In the worst case $p$ can be as small as $1/|S|$, which for $n$-bit strings is $2^{-n}$. Then the bound is no better than enumeration of $S$.

## Properties

- **Randomized, with a proved success bound.** It is a Monte Carlo method for the global optimum: it can miss, with a probability that the bound controls once $p$ is known.
- **Probabilistically approximately complete.** On a finite set with a start distribution that gives each solution positive probability, the probability of a miss tends to 0 as $R$ grows.
- **Memoryless.** Run $r$ uses nothing from runs 1 to $r - 1$. This makes it simple and easy to run in parallel, but it also wastes what the earlier runs learned. [GRASP](/grasp/) and [iterated local search](/iterated-local-search/) use that information.
- **Its success depends on basin sizes.** The value $p$ is the share of the start distribution in the basins of attraction of the good solutions (see [fitness landscape](/fitness-landscape/)). On a landscape where the good basins are small, $p$ is small.

## Variants and improvements

- **Greedy randomized starts.** [GRASP](/grasp/) replaces the uniform start by a randomized greedy construction, which gives better starts and often a larger $p$.
- **Restart from a perturbed optimum.** [Iterated local search](/iterated-local-search/) restarts from a small change of the current local optimum, not from a random point. It keeps more of the structure of good solutions.
- **Restart schedules for Las Vegas algorithms.** When the run time of a [Las Vegas algorithm](/las-vegas-algorithm/) is random, Luby, Sinclair and Zuckerman (1993) gave a universal restart schedule whose expected time is within a logarithmic factor of the best fixed cutoff. It applies to randomized local search with a run-time cutoff.
- **Restarts inside other methods.** [WalkSAT](/walksat/) and [GSAT](/gsat/) restart after a fixed number of flips; [simulated annealing](/simulated-annealing/) and [tabu search](/tabu-search/) are often run with restarts.

## When to use it

Use random restarts as the first baseline for any local search, and when you need many independent runs on parallel machines. Use them when the start has a strong effect on the result and the basin of the good solutions is large. Do not expect much when the landscape has very many local optima and the good ones have tiny basins: then $p$ is small, and the number of runs grows like $1/p$. In that case use [iterated local search](/iterated-local-search/) or a method with memory, which start the next run near a good solution.

## Pitfalls

- **Reusing the seed.** If line L3 draws each start from a new generator with the same seed, all runs are the same run. Draw all starts from one generator, or from independent seeds.
- **A deterministic start.** If the start of line L3 comes from a deterministic construction, every run ends at the same local minimum. Each start must be random.
- **Keeping the last run, not the best.** Line L5 must compare with $f(b)$. Returning the end of the last run loses the best solution.
- **Misreading the bound.** The bound $(1 - p)^R$ needs the true $p$ of the instance. An estimate of $p$ from a few runs gives an estimate of the miss probability, not a bound.

## Implementations

## History

Restarting a local search from random starts is as old as local search itself; Lin (1965) ran his 3-opt procedure from many random tours of the traveling salesman problem and kept the best. Russell and Norvig (Section 4.1) give the expected number of restarts $1/p$. Hoos and Stützle (Section 4.1) give the notion of probabilistic approximate completeness, and Martí and coauthors survey multi-start methods in the Handbook of Metaheuristics.

## References
