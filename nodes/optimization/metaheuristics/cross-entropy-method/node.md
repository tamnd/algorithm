---
tag: HK9SF5
kind: algorithm
slug: cross-entropy-method
name: Cross-entropy method
aliases:
- CE method
- CEM
area: optimization/metaheuristics
level: advanced
summary: Iteratively fit a sampling distribution to the elite samples, by maximum likelihood with smoothing. It can settle on a solution that is not optimal.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of iterations, m: the number of samples per iteration, n: the length of a solution, c: the cost of one value of the objective}
  time: {worst: O(k m (n + c + log m))}
  space: {extra: O(m n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true, comparison-based: true}
history:
  year: 1997
  people: [Reuven Rubinstein]
  note: Rubinstein introduced the method for the estimation of rare-event probabilities in 1997 and adapted it to combinatorial optimization in 1999.
prereqs: [black-box-optimization, maximum-likelihood-estimation]
see_also: [estimation-of-distribution-algorithm, cma-es, importance-sampling, cross-entropy-loss, maximum-cut, premature-convergence, simulated-annealing, genetic-algorithm]
sources:
  - paper: doi:10.1023/A:1010091220143
    title: Reuven Rubinstein, The cross-entropy method for combinatorial and continuous optimization, Methodology and Computing in Applied Probability 1(2), 1999
    locator: pages 127 to 190 (the algorithm for optimization, max-cut and the traveling salesman problem)
  - paper: doi:10.1007/s10479-005-5724-z
    title: Pieter-Tjerk de Boer, Dirk P. Kroese, Shie Mannor and Reuven Y. Rubinstein, A tutorial on the cross-entropy method, Annals of Operations Research 134, 2005
    locator: pages 19 to 67 (the elite update as maximum likelihood, smoothing, and the max-cut example)
  - book: doi:10.1007/978-1-4757-4321-0
    title: Reuven Y. Rubinstein and Dirk P. Kroese, The Cross-Entropy Method, a Unified Approach to Combinatorial Optimization, Monte-Carlo Simulation and Machine Learning, Springer, 2004
    locator: Chapters 2 and 4 (rare events and optimization) and the chapter on convergence
  - paper: "Andre Costa, Owen Dafydd Jones and Dirk Kroese, Convergence properties of the cross-entropy method for discrete optimization, Operations Research Letters 35(5), 2007"
    title: Andre Costa, Owen Dafydd Jones and Dirk Kroese, Convergence properties of the cross-entropy method for discrete optimization
    locator: pages 573 to 580 (convergence to a degenerate distribution with constant smoothing)
---

The cross-entropy (CE) method is a randomized method for optimization that keeps a probability distribution over the solutions instead of a set of solutions. Each iteration draws samples from the distribution, keeps the best fraction of them, the *elite*, and fits the distribution to the elite by [maximum likelihood](/maximum-likelihood-estimation/), often mixed with the old distribution by a *smoothing* factor. Rubinstein introduced it in 1997 to estimate the probabilities of rare events by [importance sampling](/importance-sampling/), where the update minimizes a [cross-entropy](/cross-entropy-loss/), or equivalently a Kullback-Leibler divergence, and he adapted it to optimization in 1999. The distribution usually becomes concentrated on a single solution. That solution need not be optimal, and with a constant smoothing factor there is no guarantee that the method samples the optimum.

## In plain words

Imagine guessing a password where you are told how good each guess is. Start with no idea: each letter is a coin flip. Make many guesses, look at the best few, and count how often each letter appears in them. Use those counts as the new odds for the next round of guesses.

Round by round, the odds move toward what the good guesses have in common. In the end, every letter is almost certain, and all guesses are the same.

This works well when good guesses share parts of the best answer. But the odds can lock in a wrong letter early, and once a choice is certain, it can never change again. Moving the odds only part of the way each round makes this less likely.

## The problem

The input is a set $\mathcal{X}$ of solutions, a score $S : \mathcal{X} \to \mathbb{R}$ to maximize, a family of distributions $f(\cdot\,; v)$ on $\mathcal{X}$ with a start parameter $v_0$, the number $m$ of samples per iteration, the elite fraction $\rho$ and the smoothing factor $\alpha \in (0, 1]$. The goal is a solution with a high score, ideally a global maximum, in the [global optimization](/global-optimization/) and [black-box](/black-box-optimization/) setting. For $\mathcal{X} = \{0, 1\}^n$ the usual family is independent bits with $P(x_j = 1) = p_j$. For $\mathcal{X} = \mathbb{R}^n$ it is a Gaussian, often with a diagonal covariance.

## The algorithm

```pseudo id=main
CROSS-ENTROPY(S, f(·; v), v₀, m, ρ, α, K)
L1  v ← v₀; best ← none
L2  for t ← 1 to K do
L3      draw X₁, …, X_m independently from f(·; v)
L4      E ← the ⌈ρm⌉ samples with the highest S; update best
L5      w ← argmax_u Σ_{X ∈ E} ln f(X; u)          ▷ maximum likelihood on E
L6      v ← α w + (1 − α) v                        ▷ smoothing
L7  return best
```

For independent bits, line L5 gives $w_j = $ the fraction of elite samples with $x_j = 1$. For a Gaussian with a diagonal covariance, it gives the sample mean and the sample standard deviation of each coordinate over the elite. The score of the worst elite sample, $\gamma_t$, is the level of iteration $t$. Common values are $\rho$ between 0.01 and 0.1, $m$ a multiple of the number of parameters, and $\alpha$ between 0.3 and 0.9.

## Example

**Max-cut on 16 vertices.** The weighted graph has 16 vertices and 68 edges with integer weights from 1 to 5, drawn with seed 7, and a total weight of 206. The [maximum cut](/maximum-cut/), found by checking all $2^{15}$ cuts with vertex 16 fixed on side 0, has weight 140. A solution $x \in \{0, 1\}^{16}$ puts vertex $j$ on side $x_j$, with $x_{16} = 0$ fixed so that a cut and its mirror are not both counted, and $S(x)$ is the weight of the cut. Start with $p_j = 1/2$ for $j \le 15$, and use $\rho = 0.1$.

With $m = 200$, $\alpha = 0.7$ and seed 0, the level was $\gamma_1 = 118$, $\gamma_2 = 121$, $\gamma_3 = 123$, $\gamma_5 = 131$ and $\gamma_{10} = 139$. By iteration 10 every $p_j$ was within $0.01$ of 0 or 1, and from then on almost every sample was the same cut of weight 139. The distribution had become concentrated on a cut that is one short of the optimum, and the run never found 140.

Over 20 runs (seeds 0 to 19) of 60 iterations each, the number of runs that found the maximum cut of 140, and the number whose final $p$ was a 0/1 vector for a worse cut, were:

| $\alpha$ | $m = 50$: found 140 | $m = 50$: stuck on a worse cut | $m = 200$: found 140 | $m = 200$: stuck on a worse cut |
|---|---|---|---|---|
| 1.0 | 5 | 15 | 10 | 12 |
| 0.7 | 9 | 11 | 12 | 8 |
| 0.3 | 11 | 0 | 18 | 0 |

With $\alpha = 0.3$ no run had yet reached a 0/1 vector for a worse cut after 60 iterations, but the remaining runs had not found 140 either.

**A continuous function.** On Rastrigin's function $20 + \sum_{i=1}^{2} (x_i^2 - 10 \cos 2\pi x_i)$, with a diagonal Gaussian starting at mean $(3, 3)$ and standard deviations $(5, 5)$, $\rho = 0.1$ and 100 iterations, the best value was below $10^{-6}$ in 6 of 20 runs (seeds 0 to 19) with $m = 50$ and $\alpha = 1$, in 10 of 20 with $m = 50$ and $\alpha = 0.7$, and in 20 of 20 with $m = 500$ for both values of $\alpha$. In the run with seed 19 of each of the four settings, both standard deviations were below $10^{-9}$ at the end: the Gaussian collapses to a point, whether or not that point is the global minimum.

## Correctness

The proofs are below.

1. **The update is maximum likelihood, and so a cross-entropy minimization.** Line L5 maximizes the likelihood of the elite. Equivalently, it minimizes the Kullback-Leibler divergence from the uniform distribution on the elite to $f(\cdot\,; u)$. For independent bits, $w_j$ is the elite frequency of $x_j = 1$. For a Gaussian, $w$ is the elite mean and the elite standard deviation.
2. **The parameters stay valid.** For bits, every $p_j$ stays in $[0, 1]$. For a Gaussian, every standard deviation stays $\ge 0$.
3. **Absorption.** For bits, if some $p_j$ becomes 0 or 1, it never changes again. For a Gaussian, if a standard deviation becomes 0, it stays 0.
4. **Invariance.** With the same random numbers, the runs on $S$ and on $g \circ S$, with $g$ strictly increasing, are identical.

Claim 3 is the reason for the failures above: a bit that is fixed at the wrong value cannot be corrected. Costa, Jones and Kroese proved that for independent bits with a constant smoothing factor $\alpha$, the vector $p_t$ converges with probability 1 to a 0/1 vector, so the method always ends with a single solution, which need not be optimal. They also give conditions on the smoothing factor under which the optimum is sampled with high probability. There is no bound on the number of iterations, and no guarantee for the Gaussian version.

## Complexity

One iteration draws $m$ samples of length $n$, evaluates $S$ $m$ times, sorts the scores in $O(m \log m)$, and fits the parameters in $O(\lceil \rho m \rceil n)$. So $K$ iterations cost $O(K m (n + c + \log m))$, where $c$ is the cost of one score. Only the scores of the current samples are stored, so the space is $O(m n)$. The number of iterations needed has no general bound.

## Properties

- **Comparison-based.** Only the order of the scores is used to pick the elite (Claim 4).
- **A model instead of a population.** The state is the parameter $v$, not a set of solutions. With bits, the method is close to the univariate [estimation of distribution algorithms](/estimation-of-distribution-algorithm/), such as PBIL.
- **Converges to a single point.** With independent bits and constant smoothing, the distribution becomes degenerate with probability 1 (Costa, Jones and Kroese).
- **Simple and parallel.** The $m$ samples of an iteration are independent.
- **Also an estimator.** The same iteration with importance sampling estimates the probability of a rare event $P(S(X) \ge \gamma)$.

## Variants and improvements

- **Rare-event estimation.** The original method raises the level $\gamma_t$ step by step until it reaches a given $\gamma$, and then uses $f(\cdot\,; v)$ as the [importance sampling](/importance-sampling/) density, with likelihood ratios in the update.
- **Smoothing schedules.** A smaller $\alpha$, or $\alpha$ that decreases over time, keeps the parameters away from 0 and 1 for longer.
- **Noise injection.** For the Gaussian, add a decreasing amount to the variances after each update, so that the distribution does not collapse too early.
- **Richer families.** Mixtures of Gaussians, a full covariance, or for permutations, Markov chains on the next city of a tour, as for the [traveling salesman problem](/traveling-salesman-problem/).
- **Related methods.** [CMA-ES](/cma-es/) also fits a Gaussian to weighted elite steps, but it keeps evolution paths and adapts the step size separately. [Estimation of distribution algorithms](/estimation-of-distribution-algorithm/) use the same loop with many kinds of models.
- **Use in reinforcement learning.** The CE method is a common simple baseline for optimizing the parameters of a policy.

## When to use it

Use the CE method when a natural parametric family over the solutions exists and the score is cheap enough for many samples per iteration: combinatorial problems such as [max-cut](/maximum-cut/), assignment and routing, noisy problems, and the tuning of parameters. It is also a good tool for rare-event estimation. For continuous problems, [CMA-ES](/cma-es/) is usually more efficient. For problems where the good solutions do not share simple features that the family can describe, the fit to the elite gives little help.

## Pitfalls

- **Degenerate convergence.** With $\alpha = 1$ and a small sample, bits lock in early, as the table shows. Use smoothing, a larger $m$, or restarts.
- **An elite that is too small.** With $\lceil \rho m \rceil$ of 1 or 2, the fit follows single samples and the variances collapse at once.
- **Collapsing variances.** For the Gaussian, the standard deviation shrinks every iteration even far from a minimum. Inject noise or stop and restart when it is small.
- **Ties in the score.** On a plateau, the choice of the elite among equal scores decides the update. Break ties at random, or include all ties.
- **Symmetric solutions.** In max-cut, a cut and its mirror have the same score, and the elite mixes both, which pulls every $p_j$ toward $1/2$. Fix one vertex, as in the example.

## Implementations

## History

Reuven Rubinstein introduced the cross-entropy method in 1997 as an adaptive importance sampling method for the probabilities of rare events in networks, and in 1999 showed that the same iteration solves combinatorial optimization problems such as max-cut and the traveling salesman problem. Rubinstein and Kroese wrote a book on it in 2004, and de Boer, Kroese, Mannor and Rubinstein wrote a widely used tutorial in 2005. Costa, Jones and Kroese analyzed its convergence for discrete problems in 2007.

## References
