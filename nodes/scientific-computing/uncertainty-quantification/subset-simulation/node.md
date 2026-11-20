---
tag: 2D3RV8
kind: algorithm
slug: subset-simulation
name: Subset simulation
aliases:
- SuS
- subset simulation by Markov chain Monte Carlo
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Writes a rare failure probability as a product of larger conditional probabilities of nested events, each sampled by MCMC.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of random inputs", N: "the number of samples per level", m: "the number of levels", C: "the cost of one evaluation of the limit state function"}
  time: {worst: O(m N (C + d))}
  space: {extra: O(N d)}
properties: {deterministic: false, intrusive: false, exact: false}
history:
  year: 2001
  people: [Siu-Kui Au, James L. Beck, Iason Papaioannou, Daniel Straub]
  note: Au and Beck introduced subset simulation with the modified Metropolis algorithm in 2001. Papaioannou, Betz, Zwirglmaier and Straub compared its MCMC samplers and gave adaptive proposals in 2015.
prereqs: [monte-carlo-integration, metropolis-hastings, conditional-probability]
see_also: [first-order-reliability-method, importance-sampling, cross-entropy-method, detailed-balance, random-walk-metropolis, sequential-monte-carlo, effective-sample-size, quantile]
sources:
  - paper: doi:10.1016/S0266-8920(01)00019-4
    title: Siu-Kui Au and James L. Beck, Estimation of small failure probabilities in high dimensions by subset simulation, Probabilistic Engineering Mechanics 16(4), 2001, 263-277
    locator: the product of conditional probabilities over nested failure sets, the component-wise modified Metropolis algorithm, and the coefficient of variation of the estimate with the correlation factor of the chains
  - paper: doi:10.1016/j.probengmech.2015.06.006
    title: Iason Papaioannou, Wolfgang Betz, Kilian Zwirglmaier and Daniel Straub, MCMC algorithms for subset simulation, Probabilistic Engineering Mechanics 41, 2015, 89-103
    locator: the comparison of MCMC samplers for subset simulation in standard normal space, and the adaptive scaling of the proposal spread toward a target acceptance rate
  - book: isbn:9781118398043
    title: Siu-Kui Au and Yu Wang, Engineering Risk Assessment with Subset Simulation, Wiley, 2014
    locator: the full treatment of the algorithm, the choice of the level probability, and the error estimate of the result
---

Subset simulation estimates a small probability $P_f = \mathbb{P}[g(U) \le 0]$, where $U$ is a standard normal vector and $g$ is a limit state function, much faster than plain [Monte Carlo](/monte-carlo-integration/). It writes the failure set $F$ as the last of a chain of nested sets $F_1 \supset F_2 \supset \cdots \supset F_m = F$, with $F_j = \{g \le b_j\}$, and uses

$$P_f = \mathbb{P}[F_1] \prod_{j=2}^{m} \mathbb{P}[F_j \mid F_{j-1}].$$

Each factor is about $p_0 = 0.1$, so a probability of $10^{-6}$ needs six factors that are each easy to estimate. The thresholds $b_j$ are chosen on the fly as sample quantiles. The samples conditional on $F_{j-1}$ come from Markov chains that start at the samples already in $F_{j-1}$ and stay in it, by a [Metropolis](/metropolis-hastings/) method that works one coordinate at a time. The method needs no gradient and no design point, it works in hundreds of dimensions, and it finds failure regions in several directions at once. Its result is random, with a small bias of order $1/N$.

## In plain words

A failure that happens once in a million runs is hard to see by random runs. So take it in steps. Run 1000 random cases and keep the 100 that came closest to failure. That defines a first "near failure" set, which holds about one case in ten. From each of the 100 kept cases, take small random walks that never leave the set, until you have 1000 cases spread over it. Again keep the 100 closest to failure. Each step moves the cases a factor of ten closer to the real failure set. When a step reaches it, count the failures and multiply the fractions of all steps.

## The problem

The input is a limit state function $g : \mathbb{R}^d \to \mathbb{R}$ of a standard normal vector $U$, with failure for $g(U) \le 0$. Physical inputs with other laws are first written as functions of $U$, for example by the inverse CDF of each marginal. The parameters are the number of samples per level $N$ and the level probability $p_0$, with $p_0 N$ an integer that divides $N$. The output is an estimate $\hat P_f$ of $\mathbb{P}[g(U) \le 0]$, the thresholds $b_1 > \cdots > b_m = 0$, and the number of calls to $g$. The interesting case is $P_f$ between about $10^{-3}$ and $10^{-9}$, and $g$ expensive.

## The algorithm

```pseudo id=main
SUBSET-SIMULATION(g, d, N, p0)
L1  draw N independent standard normal samples u_i; evaluate g(u_i)
L2  repeat for j = 1, 2, ...
L3      b ← the (p0 N)-th smallest value of g(u_i)
L4      if b ≤ 0
L5          return P ≈ p0^(j-1) · #{i : g(u_i) ≤ 0} / N
L6      record the factor p0 and the threshold b_j = b
L7      from each of the p0 N samples with g ≤ b, run a modified Metropolis chain of length 1/p0 inside {g ≤ b}
L8      the N chain states are the samples of level j + 1
```

Line L1 is plain Monte Carlo. Line L3 picks the threshold as a sample quantile, so that exactly $p_0 N$ samples lie in $F_j = \{g \le b\}$. If the threshold is already at or below 0 (line L4), at least $p_0 N$ samples fail, the last factor is the plain fraction of failures, and line L5 multiplies the factors. Otherwise line L6 records the factor $p_0$. Line L7 is the conditional sampling step. Each seed is the first state of a chain of $1/p_0$ states. One step of the modified Metropolis method of Au and Beck changes each coordinate $u_k$ independently: it proposes $\xi_k = u_k + \text{Uniform}(-w, w)$ and accepts it with probability $\min(1, \varphi(\xi_k)/\varphi(u_k))$, where $\varphi$ is the standard normal density. Then it evaluates $g$ at the candidate and moves only if the candidate lies in $F_j$. The chain keeps the standard normal law conditioned on $F_j$ invariant, so its states are (dependent) samples of the next level. Line L8 replaces the samples; the reference code also stops with an error after a fixed number of levels.

## Example

**One run.** Let $g(u) = 3 - u_1$ in two dimensions, $N = 1000$, $p_0 = 0.1$, and seed 7. The exact value is $\Phi(-3) = 1.350 \times 10^{-3}$.

| level $j$ | threshold $b_j$ | factor | estimate so far |
|---|---|---|---|
| 1 | 1.666 | 0.1 | 0.1 |
| 2 | 0.570 | 0.1 | 0.01 |
| 3 | 0 | 0.193 | $1.93 \times 10^{-3}$ |

The run used 2692 calls of $g$, fewer than $1000 + 2 \cdot 900$, because a step that rejects every coordinate does not call $g$. One run has a large error; the next table shows the spread.

**Many runs.** Each row repeats the method 40 times, with seeds 0 to 39, $N = 1000$, $p_0 = 0.1$ and $w = 1$. The coefficient of variation (c.o.v.) is the standard deviation over the mean. The last column is the c.o.v. that plain Monte Carlo would have with the same mean number of calls, $\sqrt{(1 - P_f)/(P_f n)}$.

| limit state | $d$ | exact $P_f$ | mean estimate | c.o.v. | mean calls | Monte Carlo c.o.v. |
|---|---|---|---|---|---|---|
| $3 - (u_1 + \cdots + u_d)/\sqrt{d}$ | 20 | $1.350 \times 10^{-3}$ | $1.458 \times 10^{-3}$ | 0.27 | 2868 | 0.51 |
| $4.5 - u_1$ | 20 | $3.398 \times 10^{-6}$ | $3.486 \times 10^{-6}$ | 0.79 | 5500 | 7.3 |
| $3 - \lvert u_1 \rvert$ | 10 | $2.700 \times 10^{-3}$ | $2.725 \times 10^{-3}$ | 0.21 | 2800 | 0.36 |

At $P_f = 3.4 \times 10^{-6}$, Monte Carlo with 5500 runs would usually see no failure at all. The third limit state has two design points, at $u_1 = 3$ and $u_1 = -3$. Subset simulation finds both and gets $2 \Phi(-3)$; the [first-order reliability method](/first-order-reliability-method/) finds one and returns $\Phi(-3)$, half the answer.

## Correctness

Three statements are exact. First, the product formula: if $F_m \subset F_{m-1} \subset \cdots \subset F_1$, then $\mathbb{P}[F_m] = \mathbb{P}[F_1] \prod_j \mathbb{P}[F_j \mid F_{j-1}]$, by the definition of [conditional probability](/conditional-probability/), since $F_j \cap F_{j-1} = F_j$. Second, the modified Metropolis step satisfies [detailed balance](/detailed-balance/) for the standard normal law restricted to $F_j$, so that law is a [stationary distribution](/stationary-distribution/) of the chain. A chain started from a sample of the conditional law therefore stays in that law at every step; the test file checks this for the truncated normal law. Third, the algorithm stops, because the number of levels is bounded.

The estimate is not exactly unbiased, because the thresholds are random and depend on the same samples. Au and Beck showed that the bias is of order $1/N$ and the c.o.v. of order $1/\sqrt{N}$. For fixed thresholds, the c.o.v. of level $j$ is $\delta_j^2 = \frac{1 - p_j}{p_j N}(1 + \gamma_j)$, where $\gamma_j \ge 0$ measures the correlation of the states of a chain. With $m$ levels the total c.o.v. is roughly $\sqrt{\sum_j \delta_j^2}$, which grows like $\sqrt{|\ln P_f|}$, while the c.o.v. of Monte Carlo grows like $1/\sqrt{P_f}$. The chains are also not proved to explore every part of $F_j$: if a part of the failure set is not reached by any seed of an earlier level, the estimate misses it.

## Complexity

In the [real RAM](/real-ram/) model, each level costs at most $N$ calls of $g$ and $O(N d)$ work for the proposals and the sort, so the total is $O(m N (C + d))$ with $m \approx \ln P_f / \ln p_0 + 1$ levels. The extra space is $O(N d)$ for the samples of one level. For $P_f = 10^{-6}$ and $N = 1000$, the cost is about 5500 calls, against $10^8$ for Monte Carlo at a c.o.v. of 0.1.

## Properties

- **Randomized.** The estimate is random; repeated runs give its spread.
- **Cost grows like $\lvert \ln P_f \rvert$.** Each factor of $1/p_0$ in rarity adds one level.
- **No gradients.** It uses only values of $g$.
- **Works in high dimension.** The component-wise proposal keeps the acceptance rate from falling to 0 as $d$ grows.
- **Global.** It finds several failure regions, if the first level samples them all.
- **Small bias.** Of order $1/N$, from the adaptive thresholds.

## Variants and improvements

- **Adaptive proposals.** Papaioannou and coauthors tune the spread $w$ of each level toward an acceptance rate near 0.44, and use conditional sampling with a correlated normal proposal in standard normal space, which needs no rejection per coordinate.
- **Other level probabilities.** $p_0$ between 0.1 and 0.3 works well; a smaller $p_0$ gives fewer levels but a larger error per level.
- **Error estimate from one run.** Estimate $\gamma_j$ from the correlation of the chain states and combine the $\delta_j$, as Au and Beck did.
- **Subset simulation for design.** The samples of each level are samples of the inputs given near failure, so they also give conditional means, sensitivity and the failure probability as a function of a threshold, at no extra cost.
- **Related methods.** The [cross-entropy method](/cross-entropy-method/) adapts an [importance sampling](/importance-sampling/) density with a similar sequence of quantile levels. Multilevel splitting and [sequential Monte Carlo](/sequential-monte-carlo/) use the same nested structure with resampling.

## When to use it

Use subset simulation when $P_f$ is small, $d$ is large or the limit state is strongly nonlinear, there are no gradients, or the failure set may have several parts. It needs a few thousand calls of $g$ per run, more than [FORM](/first-order-reliability-method/) but far fewer than Monte Carlo. If $g$ is smooth with one design point, FORM with a second-order correction is cheaper. If each call of $g$ is very expensive, fit a surrogate first and run subset simulation on it.

## Pitfalls

- **Correlated chains.** A proposal that is too narrow or too wide makes $\gamma_j$ large and the error large, as in the $4.5 - u_1$ row. Monitor the acceptance rate.
- **Missed failure regions.** If no seed of level $j$ lies near a part of $F$, later levels do not find it. Use a larger $N$ when there may be separated regions.
- **One run is not enough.** The c.o.v. of one run can be 0.3 or more. Report an error estimate.
- **Bad input map.** The method assumes independent standard normal inputs. Map other laws to that space first, or the modified Metropolis step samples the wrong law.
- **Ties in $g$.** A limit state with flat regions makes the quantile ill defined. Break ties, or use a level set with a little noise.

## Implementations

## History

Au and Beck introduced subset simulation in 2001 for small failure probabilities of structures with many random inputs, and gave the modified Metropolis algorithm, which works one coordinate at a time because the plain Metropolis method rejects almost every move in high dimensions. The method became a standard tool of structural reliability. Papaioannou, Betz, Zwirglmaier and Straub compared MCMC samplers for it in 2015 and gave adaptive proposals. Au and Wang wrote a book on the method in 2014.

## References
