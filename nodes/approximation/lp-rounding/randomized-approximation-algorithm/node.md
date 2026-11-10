---
tag: FNKXS3
kind: concept
slug: randomized-approximation-algorithm
name: Randomized approximation algorithm
aliases:
- randomized approximation
- approximation ratio in expectation
area: approximation/lp-rounding
level: core
summary: An approximation algorithm using random choices whose expected solution cost is within a guaranteed factor of the optimum, or within it with high probability.
prereqs: [approximation-ratio, randomized-algorithm, linearity-of-expectation, markov-inequality]
see_also: [randomized-rounding, random-assignment-max-3-sat, method-of-conditional-expectations, monte-carlo-algorithm, las-vegas-algorithm, error-amplification, maximum-cut, pessimistic-estimators]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 5.1 (simple algorithms for MAX SAT and MAX CUT) and Section 5.2 (derandomization)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 13.4 (a randomized approximation algorithm for MAX 3-SAT)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 6 (the probabilistic method, large cuts, maximum satisfiability and derandomization by conditional expectations)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 5 (the probabilistic method, maximum satisfiability and the method of conditional probabilities)
---

A randomized approximation algorithm uses random choices and returns a feasible solution whose value is within a guaranteed factor of the optimum, either in expectation or with high probability. For a minimization problem it is a $\rho$-approximation in expectation if $\mathbb{E}[\text{ALG}(I)] \le \rho \cdot \text{OPT}(I)$ for every instance $I$, where the expectation is over the coins of the algorithm only and not over the input. For a maximization problem the condition is $\mathbb{E}[\text{ALG}(I)] \ge \alpha \cdot \text{OPT}(I)$. Two simple facts make the expected form useful: [Markov's inequality](/markov-inequality/) turns it into a constant probability of a slightly worse ratio, and independent repetition raises that probability to nearly 1. Many such algorithms can also be derandomized.

## In plain words

Some algorithms flip coins as they work, so their answer can change from run to run. For such an algorithm, the promise is about the average: over all coin flips, the answer is at most some factor worse than the best one. The promise holds for every input, not only for typical inputs.

An average promise is weaker than a promise for each run. But a bad run cannot happen too often, since it would pull the average down. So if you run the algorithm a few times and keep the best answer, you almost surely get one that is close to the promise. Often you can also replace the coins by careful fixed choices.

## The idea

**Ratios.** Let $\text{ALG}(I)$ be the value of the output on $I$, a random variable. The output is always feasible. The algorithm runs in polynomial time in the worst case, as a [Monte Carlo algorithm](/monte-carlo-algorithm/), or in expected polynomial time, as a [Las Vegas algorithm](/las-vegas-algorithm/).

- *In expectation:* $\mathbb{E}[\text{ALG}(I)] \le \rho \cdot \text{OPT}(I)$ (minimization) or $\mathbb{E}[\text{ALG}(I)] \ge \alpha \cdot \text{OPT}(I)$ (maximization) for all $I$.
- *With high probability:* $\Pr[\text{ALG}(I) \le \rho \cdot \text{OPT}(I)] \ge 1 - 1/n^{c}$ for a constant $c > 0$, where $n$ is the input size, and the same for maximization.

Since $\text{OPT}(I)$ is fixed for each $I$, the bound $\mathbb{E}[\text{ALG}] \le \rho \cdot \text{OPT}$ is the same as $\mathbb{E}[\text{ALG}/\text{OPT}] \le \rho$.

**From expectation to probability, minimization.** By Markov's inequality, for $\varepsilon > 0$,

$$\Pr[\text{ALG} > (1 + \varepsilon) \rho \cdot \text{OPT}] \le \frac{\mathbb{E}[\text{ALG}]}{(1 + \varepsilon) \rho \cdot \text{OPT}} \le \frac{1}{1 + \varepsilon}.$$

So one run gives $\text{ALG} \le (1 + \varepsilon) \rho \cdot \text{OPT}$ with probability at least $\varepsilon / (1 + \varepsilon)$. Run $t$ times and keep the best. All runs fail with probability at most $(1 + \varepsilon)^{-t} \le e^{-t \varepsilon / (1 + \varepsilon)}$, because $\ln(1 + \varepsilon) \ge \varepsilon / (1 + \varepsilon)$. So $t = \lceil \frac{1 + \varepsilon}{\varepsilon} \ln \frac{1}{\eta} \rceil$ runs give failure probability at most $\eta$; see [error amplification](/error-amplification/).

**From expectation to probability, maximization.** Each output is feasible, so $\text{ALG} \le \text{OPT}$. Let $p = \Pr[\text{ALG} \ge (\alpha - \varepsilon) \text{OPT}]$. Then

$$\alpha \cdot \text{OPT} \le \mathbb{E}[\text{ALG}] \le p \cdot \text{OPT} + (1 - p)(\alpha - \varepsilon) \text{OPT},$$

which gives $p \ge \varepsilon / (1 - \alpha + \varepsilon)$. The same repetition then works.

**Las Vegas from a lower bound.** If a bound $L \le \text{OPT}$ can be computed, for example $L = \text{LP}^*$, and $\mathbb{E}[\text{ALG}] \le \rho L$, then repeating until $\text{ALG} \le (1 + \varepsilon) \rho L$ gives that bound on every output, with at most $(1 + \varepsilon)/\varepsilon$ runs in expectation.

**Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) fixes the coins one at a time so that the conditional expectation never gets worse, and ends with a deterministic output at least as good as the expectation. When the conditional expectation is hard to compute, a [pessimistic estimator](/pessimistic-estimators/) takes its place. When the analysis uses only [pairwise or k-wise independence](/k-wise-independence/), a small sample space can be searched in full.

**Hardness applies too.** The reductions that prove hardness of approximation are deterministic. A randomized polynomial-time algorithm that beats such a bound with probability at least $2/3$ on every instance would put NP in BPP, so the bounds hold for randomized algorithms under that assumption.

## Examples

- **Random cut.** Put each vertex on a side by a fair coin. Each edge is cut with probability $\frac12$, so $\mathbb{E}[\text{cut}] = m/2 \ge \frac12 \text{OPT}$ for [maximum cut](/maximum-cut/) on a graph with $m$ edges. This is a $\frac12$-approximation in expectation, and conditional expectations make it deterministic.
- **MAX-3SAT.** A [uniform random assignment](/random-assignment-max-3-sat/) satisfies each clause with exactly three distinct literals with probability $\frac78$, so $\mathbb{E}[\text{ALG}] = 7m/8 \ge \frac78 \text{OPT}$. The number satisfied is an integer, so a run below $7m/8$ satisfies at most $7m/8 - 1/8$ clauses. With $p$ the probability of at least $7m/8$, $7m/8 \le p m + (1 - p)(7m/8 - 1/8)$, so $p \ge 1/(m + 1)$. Repeating until $7m/8$ clauses are satisfied is a Las Vegas algorithm with at most $m + 1$ runs in expectation.
- **Set cover.** [LP rounding for set cover](/lp-rounding-set-cover/) gives cost $O(\log n) \cdot \text{LP}^*$ in expectation.
- **Routing.** [Randomized rounding](/randomized-rounding/) for congestion gives the ratio $O(\log m / \log \log m)$ with high probability, from a Chernoff bound and a union bound.
- **MAX-SAT.** [LP rounding for MAX-SAT](/max-sat-lp-rounding/) gives $1 - 1/e$ in expectation, and the better of it and a fair random assignment gives $\frac34$.
- **Semidefinite rounding.** The random hyperplane rounding for maximum cut gives about $0.878$ of the optimum in expectation; see [semidefinite programming](/semidefinite-programming/).

## Where it is used

- **LP rounding.** Most rounding methods are randomized: [randomized rounding](/randomized-rounding/), [dependent rounding](/dependent-rounding/), [swap rounding](/swap-rounding/), and the clustering steps of [facility location](/shmoys-tardos-aardal-facility-location/).
- **The probabilistic method.** The bound $\mathbb{E}[\text{ALG}] \ge \alpha \cdot \text{OPT}$ also proves that a solution of that value exists; see [the probabilistic method](/probabilistic-method/).
- **Deterministic algorithms.** Many deterministic approximation algorithms are derandomized forms of randomized ones, for example the derandomized [MAX-3SAT](/random-assignment-max-3-sat/) algorithm.
- **Approximate counting.** A randomized approximation scheme for a counting problem returns a value within a factor $1 \pm \varepsilon$ of the count with probability at least $\frac34$; the median of independent runs raises this probability.

## References
