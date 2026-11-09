---
tag: MH6JW4
kind: algorithm
slug: estimation-of-distribution-algorithm
name: Estimation of distribution algorithm
aliases:
- EDA
- probabilistic model-building GA
- UMDA
- univariate marginal distribution algorithm
- compact genetic algorithm
area: optimization/metaheuristics
level: research
summary: Replace crossover and mutation by sampling from a probabilistic model learned from the selected solutions. UMDA and the compact GA use independent bits.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {g: the number of generations, l: the number of samples per generation, n: the number of bits, c: the cost of one value of the objective}
  time: {worst: O(g l (n + c + log l))}
  space: {extra: O(l n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true, comparison-based: true}
history:
  year: 1996
  people: [Heinz Mühlenbein, Gerhard Paaß, Shumeet Baluja]
  note: Baluja proposed PBIL in 1994, Mühlenbein and Paaß proposed UMDA in 1996, and Harik, Lobo and Goldberg the compact GA in 1999.
prereqs: [genetic-algorithm, black-box-optimization]
see_also: [cross-entropy-method, cma-es, schema-theorem, building-block-hypothesis, bayesian-network, premature-convergence, genetic-algorithm, black-box-optimization]
sources:
  - paper: "Heinz Mühlenbein and Gerhard Paaß, From recombination of genes to the estimation of distributions I. Binary parameters, Parallel Problem Solving from Nature PPSN IV, LNCS 1141, 1996"
    title: Heinz Mühlenbein and Gerhard Paaß, From recombination of genes to the estimation of distributions I. Binary parameters
    locator: pages 178 to 187 (the univariate marginal distribution algorithm)
  - paper: doi:10.1109/4235.797971
    title: Georges R. Harik, Fernando G. Lobo and David E. Goldberg, The compact genetic algorithm, IEEE Transactions on Evolutionary Computation 3(4), 1999
    locator: pages 287 to 297 (the algorithm with the update 1/K and its relation to a GA with population size K)
  - book: doi:10.1007/978-1-4615-1539-5
    title: Pedro Larrañaga and Jose A. Lozano (editors), Estimation of Distribution Algorithms, a New Tool for Evolutionary Computation, Kluwer, 2002
    locator: Chapter 3 (a review of EDAs with univariate, bivariate and multivariate models)
  - paper: doi:10.1016/j.swevo.2011.08.003
    title: Mark Hauschild and Martin Pelikan, An introduction and survey of estimation of distribution algorithms, Swarm and Evolutionary Computation 1(3), 2011
    locator: pages 111 to 128 (the general loop, the classes of models, and deceptive traps)
  - paper: "Dirk Sudholt and Carsten Witt, On the choice of the update strength in estimation-of-distribution algorithms and ant colony optimization, Algorithmica 81, 2019"
    title: Dirk Sudholt and Carsten Witt, On the choice of the update strength in estimation-of-distribution algorithms and ant colony optimization
    locator: the upper bound O(K sqrt(n)) for the compact GA on OneMax and the lower bound from genetic drift
---

An estimation of distribution algorithm (EDA) is an evolutionary method that keeps a probability model of good solutions instead of a set of solutions. Each generation it samples solutions from the model, selects the best, and fits the model to the selected ones. Sampling from the model takes the place of the crossover and mutation of a [genetic algorithm](/genetic-algorithm/). The simplest EDAs on bit strings treat the bits as independent: the univariate marginal distribution algorithm (UMDA) of Mühlenbein and Paaß sets the probability of a 1 at each position to its frequency among the selected strings, and the compact GA (cGA) of Harik, Lobo and Goldberg moves each probability by a fixed amount after a comparison of two samples. Richer EDAs learn a [Bayesian network](/bayesian-network/) and can capture interactions between bits. Without a lower and upper bound on the probabilities, a probability that reaches 0 or 1 is fixed forever, and random drift alone can fix it at the wrong value. There is no general guarantee of finding the optimum, and univariate EDAs fail on deceptive functions where the bits must change together.

## In plain words

Think of a long form with yes or no questions, and a score for each filled form. Instead of keeping a pile of good forms, keep one number per question: how likely the answer yes is.

Each round, fill in many forms at random using those numbers, score them, and keep the best half. Then set each number to how often the kept forms said yes to that question. Good answers become more likely, round by round.

This works when each answer helps on its own. It fails when answers only help in groups, because the numbers treat every question alone. And if a number reaches always or never, it can not change again, so most versions keep it a little away from the ends.

## The problem

The input is a score $S : \{0, 1\}^n \to \mathbb{R}$ to maximize that we can only evaluate, the number $\lambda$ of samples per generation, the number $\mu < \lambda$ of selected samples, and a number of generations. The goal is a string with a high score, ideally a global maximum. This is [global optimization](/global-optimization/) over bit strings in the [black-box](/black-box-optimization/) setting. EDAs also exist for real vectors, with Gaussian models, and for permutations.

## The algorithm

The UMDA with truncation selection and margins. The model is a vector $p \in [0, 1]^n$, and a sample has independent bits with $P(x_j = 1) = p_j$.

```pseudo id=main
UMDA(S, n, λ, μ, G)
L1  p ← (1/2, …, 1/2)
L2  for generation ← 1 to G do
L3      sample x₁, …, x_λ independently from p
L4      keep the μ samples with the highest S; update best
L5      p_j ← (number of kept samples with bit j = 1) / μ, for each j
L6      p_j ← min(1 − 1/n, max(1/n, p_j))              ▷ margins
L7  return best
```

Line L5 is the [maximum likelihood](/maximum-likelihood-estimation/) fit of independent bits to the selected strings, the same update as the [cross-entropy method](/cross-entropy-method/) with no smoothing. Line L6 keeps every $p_j$ in $[1/n, 1 - 1/n]$, so that a bit fixed at the wrong value can still flip with probability at least $1/n$, as with the mutation of a genetic algorithm. Without line L6 the algorithm is the original UMDA.

The **compact GA** keeps the same model but samples only two strings $x, y$ per step. If $S(x) \ge S(y)$, it moves $p_j$ by $1/K$ toward $x_j$ at each position where $x_j \ne y_j$, and then applies the same margins. Harik, Lobo and Goldberg showed that with the step $1/K$, it behaves like a genetic algorithm with uniform crossover and a population of size $K$.

## Example

**One generation by hand.** Take OneMax, $S(x) = \sum_j x_j$, with $n = 4$, $\lambda = 6$ and $\mu = 3$. Say the samples are $1011$, $0100$, $1110$, $0011$, $1000$ and $1101$, with the scores $3, 1, 3, 2, 1, 3$. The three kept strings are $1011$, $1110$ and $1101$. The frequencies of 1 are $(3/3, 2/3, 2/3, 2/3)$. Line L6 clamps them to $[1/4, 3/4]$, which gives $p = (0.75, 0.667, 0.667, 0.667)$. Without margins, $p_1 = 1$, and every later sample would have $x_1 = 1$.

**OneMax with $n = 50$.** UMDA with $\lambda = 2\mu$, at most 300 generations, 20 runs (seeds 0 to 19). A run is a success if some sample is the string of all ones. The number of evaluations counts all samples up to and including the generation of the first success.

| $\mu$ | without margins: successes | mean evaluations | with margins: successes | mean evaluations |
|---|---|---|---|---|
| 5 | 0 | | 20 | 510 |
| 10 | 1 | 220 | 20 | 473 |
| 20 | 17 | 435 | 20 | 520 |
| 40 | 20 | 804 | 20 | 856 |

Without margins and with a small $\mu$, some $p_j$ reach 0 before the selection has pushed them up, and the run can never succeed. With margins every run succeeded, but the small populations needed more generations.

The compact GA on the same function, with at most 200000 steps, found the optimum in all 20 runs (seeds 0 to 19) for each $K$, with the mean number of evaluations 672 for $K = 4$ (216 to 1648), 382 for $K = 10$ (166 to 706), 500 for $K = 30$ (380 to 610) and 1271 for $K = 100$ (1064 to 1410).

**Genetic drift.** With a constant score, selection ignores the bits. In one UMDA run without margins, with $n = 200$, $\lambda = 20$, $\mu = 10$ and seed 0, the number of fixed positions ($p_j \in \{0, 1\}$) was 47 after 5 generations, 102 after 10, 163 after 20, 198 after 40 and all 200 after 80. Of these, 108 were fixed at 1. By Claim 3 of the proof, each position is fixed at 1 with probability exactly $1/2$.

**A deceptive function.** Split $n = 30$ bits into 6 blocks of 5, and let a block with $u$ ones score 5 if $u = 5$ and $4 - u$ otherwise. The optimum is all ones, with score 30, but within a block, fewer ones score more except at $u = 5$. UMDA with margins, $\lambda = 2\mu$ and 100 generations found the optimum in 0 of 10 runs (seeds 0 to 9) for $\mu = 50$ and for $\mu = 200$, and in every run all 30 probabilities ended below $1/2$. The model with independent bits sees only the pull toward 0. An EDA that learns which bits belong together, such as BOA or ECGA, is needed.

## Correctness

The proofs are below.

1. **Valid model.** Every $p_j$ is a multiple of $1/\mu$ clamped to $[1/n, 1 - 1/n]$, or a multiple of $1/\mu$ in $[0, 1]$ without margins.
2. **Absorption without margins.** If $p_j \in \{0, 1\}$, then $p_j$ never changes again.
3. **Genetic drift.** If the score is constant and there are no margins, each $p_j$ is a martingale that is fixed at 0 or 1 with probability 1, and it is fixed at 1 with probability exactly $p_j$ at the start.
4. **With margins, every string has a chance.** Each sample equals any given string with probability at least $n^{-n}$. So the probability that the optimum has not been sampled after $t$ samples is at most $(1 - n^{-n})^t$, which goes to 0. This is a guarantee in the limit only.
5. **Invariance.** With the same random numbers, the runs on $S$ and on $g \circ S$, for $g$ strictly increasing, are identical.

For OneMax there are sharp results. Sudholt and Witt proved that the compact GA with $K \ge c\sqrt n \log n$, for a large enough constant $c$, optimizes OneMax in $O(K \sqrt n)$ expected steps, which is $O(n \log n)$ for $K = \Theta(\sqrt n \log n)$. They also showed that with a smaller $K$, drift as in Claim 3 drives many probabilities to the lower margin, and the running time grows. Similar bounds are known for UMDA. On functions where good values need several bits to change together, such as the traps above, no such bound exists for univariate EDAs, and the measurement shows them failing.

## Complexity

A generation samples $\lambda$ strings of $n$ bits, evaluates them, sorts the scores in $O(\lambda \log \lambda)$, and counts frequencies in $O(\mu n)$. So $G$ generations cost $O(G \lambda (n + c + \log \lambda))$, where $c$ is the cost of one score. The space is $O(\lambda n)$ for one generation of samples, or $O(n)$ for the compact GA, which keeps only $p$ and two samples. EDAs with a Bayesian network spend much more time learning the structure of the model, often $O(n^2 \lambda)$ or more per generation.

## Properties

- **Comparison-based.** Only the order of the scores is used (Claim 5).
- **Small memory.** The compact GA stores $n$ numbers instead of a population, which was its original purpose.
- **Explicit model.** After a run, $p$ or the learned network says which values and which groups of variables matter, which can be useful in itself.
- **Univariate models ignore interactions.** UMDA and the compact GA are invariant under any permutation of the positions, but they cannot represent a dependence between bits.
- **Drift.** A small $\mu$ or a small $K$ makes the model follow random noise. Margins, larger populations and smaller steps reduce the effect.

## Variants and improvements

- **PBIL.** Baluja's population-based incremental learning moves $p$ toward the best sample with a learning rate, $p \leftarrow (1 - \alpha) p + \alpha x_{\text{best}}$. It is close to the [cross-entropy method](/cross-entropy-method/) with smoothing.
- **Bivariate models.** MIMIC learns a chain of dependencies between pairs of bits, and the algorithm of Baluja and Davies a tree.
- **Multivariate models.** ECGA (Harik, 1999) groups the bits into blocks with a joint distribution each. BOA (Pelikan, Goldberg and Cantú-Paz, 1999) learns a Bayesian network, and hBOA adds a hierarchy. These solve the concatenated traps above with a population that grows polynomially in $n$, as the authors report.
- **Continuous EDAs.** Fit a Gaussian, or a mixture, to the selected points. [CMA-ES](/cma-es/) can be seen as a refined continuous EDA with evolution paths, and the [cross-entropy method](/cross-entropy-method/) as a basic one.
- **Permutations.** Models such as the Mallows model or edge histograms for tours.

## When to use it

Use a univariate EDA when the variables affect the score mostly on their own, and the compact GA when memory is very small. Use a multivariate EDA such as BOA when the problem is known to have groups of interacting variables, the building blocks of the [building block hypothesis](/building-block-hypothesis/), and the evaluations are cheap enough for large populations. When the structure is unknown and evaluations are expensive, test a simpler method, such as a [genetic algorithm](/genetic-algorithm/) or a local search with restarts, with the same budget.

## Pitfalls

- **No margins.** A probability at 0 or 1 never changes again (Claim 2), and drift can put it there even on an easy function, as the table for $\mu = 5$ shows.
- **Populations that are too small.** Drift fixes probabilities at random values within a number of generations of the order of $\mu$, as the drift example shows for $\mu = 10$. The population must be large enough that selection moves each probability faster than drift does.
- **Deceptive and interacting variables.** A univariate model is pulled the wrong way on traps. Learn the dependencies or use a different method.
- **Ties.** On plateaus, the rule that breaks ties in the selection decides the update. Break ties at random.
- **The cost of learning.** Learning a Bayesian network each generation can cost far more than the evaluations of a cheap function.

## Implementations

## History

Shumeet Baluja proposed population-based incremental learning in 1994, and Heinz Mühlenbein and Gerhard Paaß proposed UMDA in 1996 under the name estimation of distributions. Harik, Lobo and Goldberg published the compact GA in 1999. Bivariate models followed with MIMIC (De Bonet, Isbell and Viola, 1997), and multivariate models with ECGA and BOA in 1999. Larrañaga and Lozano edited the first book on EDAs in 2002. Rigorous running time analyses of UMDA and the compact GA on OneMax and other simple functions appeared from the mid 2000s, with sharp bounds and the role of genetic drift established in the late 2010s.

## References
