---
tag: 4918P8
kind: concept
slug: mutation
name: Mutation
aliases:
- mutation operator
- bit-flip mutation
- Gaussian mutation
area: optimization/metaheuristics
level: intro
summary: A variation operator that changes one solution at random. Bit-flip mutation with rate p turns x into y with probability p^h (1-p)^(n-h), where h is the Hamming distance.
prereqs: [evolutionary-computation, binomial-distribution]
see_also: [crossover, genetic-algorithm, evolution-strategies, cma-es, premature-convergence, hamming-distance, local-search, cuckoo-search]
sources:
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992
    locator: Chapter 6 (mutation as a background operator that restores lost alleles)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Chapter 4, Representation, mutation, and recombination (bit-flip, creep, Gaussian, swap, insert and inversion mutation)
  - book: doi:10.1007/978-3-642-17339-4
    title: Thomas Jansen, Analyzing Evolutionary Algorithms, The Computer Science Perspective, Springer, 2013
    locator: Chapter 5 (methods for the analysis of the (1+1) EA with standard bit mutation)
  - paper: Carsten Witt, Tight bounds on the optimization time of a randomized search heuristic on linear functions, Combinatorics, Probability and Computing 22(2), 2013
    title: Tight bounds on the optimization time of a randomized search heuristic on linear functions
    locator: pages 294 to 318 (the mutation rate c/n and the bound (1 ± o(1)) (e^c / c) n ln n)
  - paper: Benjamin Doerr, Huu Phuoc Le, Régis Makhmara and Ta Duy Nguyen, Fast genetic algorithms, Proceedings of the Genetic and Evolutionary Computation Conference (GECCO), 2017
    title: Fast genetic algorithms
    locator: the analysis of the (1+1) EA on jump functions with static rates and with heavy-tailed rates
  - paper: Xin Yao, Yong Liu and Guangming Lin, Evolutionary programming made faster, IEEE Transactions on Evolutionary Computation 3(2), 1999
    title: Evolutionary programming made faster
    locator: pages 82 to 102 (Cauchy mutation in place of Gaussian mutation)
---

Mutation is a variation operator of [evolutionary computation](/evolutionary-computation/) that makes a child from one parent by a small random change. For bit strings, standard bit mutation flips each bit independently with a rate $p$, usually $p = 1/n$. For real vectors, Gaussian mutation adds a normal random vector. Mutation brings in values that are not in the population, and with $0 < p < 1$ it can reach every string in one step, which is the basis of the convergence proofs of [genetic algorithms](/genetic-algorithm/) with [elitism](/elitism/).

## In plain words

Take one solution and change it a little, at random. For a string of zeros and ones, go through the positions and flip each one with a small chance, for example one chance in the length of the string. On average one position changes, but sometimes none and sometimes two or three.

[Crossover](/crossover/) can only mix values that the parents already have. If all solutions in the group have a 0 in some place, no mix can make a 1 there. Mutation can. Small changes keep the child close to its parent, so mutation alone acts like a random [local search](/local-search/). The size of the change matters: too small and the search moves slowly, too large and the child keeps little of what made its parent good.

## The idea

**Standard bit mutation.** For $x \in \{0,1\}^n$, flip each bit independently with probability $p$. The child $y$ depends only on $x$, and for every $y$
$$\Pr[y \mid x] = p^{h} (1 - p)^{n - h}, \qquad h = H(x, y),$$
where $H$ is the [Hamming distance](/hamming-distance/). The number of flipped bits has the [binomial distribution](/binomial-distribution/) $B(n, p)$, with mean $n p$.

- With $p = 1/n$, one bit flips on average. No bit flips with probability $(1 - 1/n)^n$, which tends to $1/e \approx 0.368$, and exactly one bit flips with probability $(1 - 1/n)^{n-1} \ge 1/e$.
- A specific bit, and no other, flips with probability $\frac{1}{n}(1 - \frac{1}{n})^{n-1} \ge \frac{1}{en}$. This bound is the main step in the analysis of the $(1+1)$ EA by fitness levels.
- If $0 < p < 1$, every $y$ has $\Pr[y \mid x] \ge \min(p, 1 - p)^n > 0$. So one mutation can reach any string. This makes the population process of a genetic algorithm an irreducible Markov chain, and with [elitism](/elitism/) it gives convergence to an optimum with probability 1.

**The rate.** On linear functions, the $(1+1)$ EA with rate $p = c/n$ for a constant $c > 0$ needs $(1 \pm o(1)) \frac{e^c}{c} n \ln n$ iterations in expectation, as Witt (2013) proved. This is smallest at $c = 1$, which supports the usual choice $p = 1/n$ for this class. For other functions other rates are better. Doerr, Le, Makhmara and Nguyen (2017) showed that on jump functions, where the algorithm must flip $m$ given bits at once, the best static rate is about $m/n$. So $1/n$ is a default, not a law.

**Real vectors.** Gaussian mutation sets $y = x + \sigma z$ with $z \sim N(0, I)$. The step size $\sigma$ decides the scale of the search. [Evolution strategies](/evolution-strategies/) adapt it during the run, for example by the 1/5 success rule or by self-adaptation, and [CMA-ES](/cma-es/) adapts a full covariance matrix. Mutations with heavy tails, such as Cauchy or Lévy steps, make rare long jumps. Yao, Liu and Lin (1999) used Cauchy mutation in evolutionary programming. The Lévy flight of [cuckoo search](/cuckoo-search/) is a mutation of this kind.

**Permutations.** A swap mutation exchanges two random elements, an insertion mutation moves one element to a new position, and an inversion mutation reverses a random segment. On a tour of the [traveling salesman problem](/traveling-salesman-problem/), an inversion is a random [2-opt](/two-opt/) move.

**Trees.** Subtree mutation in [genetic programming](/genetic-programming/) replaces a random subtree by a new random tree.

## Examples

**The full distribution on 3 bits.** Mutate $x = 010$ with $p = 0.2$. The child is $x$ with probability $0.8^3 = 0.512$. Each of the 3 strings at distance 1 has probability $0.2 \cdot 0.8^2 = 0.128$, each of the 3 at distance 2 has $0.2^2 \cdot 0.8 = 0.032$, and $101$ at distance 3 has $0.2^3 = 0.008$. The sum is $0.512 + 3(0.128) + 3(0.032) + 0.008 = 1$.

**Rate $1/n$ for $n = 100$.** No bit flips with probability $0.99^{100} \approx 0.366$, exactly one bit with probability $0.99^{99} \approx 0.370$, and two or more with probability about $0.264$. So about a third of the children are copies of the parent, which costs evaluations in a run. Some programs resample until at least one bit flips.

**Restoring a lost value.** Let every string of a population have a 0 in position 4. Selection and crossover keep this 0 in every child. Bit mutation with $p = 1/n$ puts a 1 there with probability $1/n$ per child. Without mutation, no string with a 1 in position 4 can ever appear.

**Swap mutation.** On the tour $1\,2\,3\,4\,5\,6$, swapping the elements in positions 2 and 5 gives $1\,5\,3\,4\,2\,6$. The result is again a permutation.

## Where it is used

- In the [genetic algorithm](/genetic-algorithm/), as bit-flip mutation after crossover.
- In [evolution strategies](/evolution-strategies/) and [CMA-ES](/cma-es/), as the main operator, with adapted Gaussian steps.
- In the $(1+1)$ EA and its relatives, which use mutation only and are the main objects of runtime analysis.
- In [genetic programming](/genetic-programming/), as subtree and point mutation.
- In the operators of several metaphor-based methods, such as the Lévy steps of [cuckoo search](/cuckoo-search/) and the pitch adjustment of [harmony search](/harmony-search/).

## References
