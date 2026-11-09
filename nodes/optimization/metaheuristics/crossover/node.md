---
tag: WQV2ED
kind: concept
slug: crossover
name: Crossover
aliases:
- recombination
- one-point crossover
- uniform crossover
- two-point crossover
- order crossover
area: optimization/metaheuristics
level: intro
summary: A variation operator that builds children from parts of two or more parents. Each operator fits a coding, such as strings, permutations, real vectors or trees.
prereqs: [evolutionary-computation]
see_also: [mutation, genetic-algorithm, schema-theorem, building-block-hypothesis, genetic-programming, memetic-algorithm, differential-evolution, hamming-distance]
sources:
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992
    locator: Chapter 6 (the crossover operator and its effect on schemata)
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 1 (one-point crossover) and Chapter 5 (reordering operators, PMX and order crossover)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Chapter 4, Representation, mutation, and recombination (binary, integer, real-valued, permutation and tree codings)
  - paper: Gilbert Syswerda, Uniform crossover in genetic algorithms, Proceedings of the Third International Conference on Genetic Algorithms, Morgan Kaufmann, 1989
    title: Uniform crossover in genetic algorithms
    locator: pages 2 to 9
  - paper: Larry J. Eshelman, Richard A. Caruana and J. David Schaffer, Biases in the crossover landscape, Proceedings of the Third International Conference on Genetic Algorithms, Morgan Kaufmann, 1989
    title: Biases in the crossover landscape
    locator: pages 10 to 19 (positional and distributional bias)
  - paper: David E. Goldberg and Robert Lingle, Alleles, loci, and the traveling salesman problem, Proceedings of the First International Conference on Genetic Algorithms, 1985
    title: Alleles, loci, and the traveling salesman problem
    locator: pages 154 to 159 (partially mapped crossover)
---

Crossover, also called recombination, is a variation operator of [evolutionary computation](/evolutionary-computation/) that makes one or more children from parts of two or more parents. For bit strings, one-point crossover cuts both parents at the same random point and swaps the tails, and uniform crossover takes each position from a parent chosen by a fair coin. Other codings need their own operators, such as order crossover for permutations and subtree crossover for program trees. Crossover is the operator that sets the [genetic algorithm](/genetic-algorithm/) apart from mutation-only methods, but whether it helps depends on the problem.

## In plain words

Take two parent solutions. Make a child that has some parts from the first parent and the other parts from the second. If both parents are good for different reasons, the child can have both good parts.

For strings, you can cut both parents at the same place and join the start of one to the end of the other. You can also go through the positions one by one and toss a coin to choose the parent for each position. Where both parents agree, the child keeps their common value. For orderings, such as a route through cities, a simple cut and join can repeat a city and lose another, so special methods copy a part of one parent and fill the rest in the order of the other.

## The idea

Let $a, b \in \{0,1\}^l$ be two parents.

- **One-point crossover.** Draw a cut point $c$ uniformly from $\{1, \ldots, l - 1\}$. The children are $a_1 \ldots a_c \, b_{c+1} \ldots b_l$ and $b_1 \ldots b_c \, a_{c+1} \ldots a_l$.
- **Two-point and $m$-point crossover.** Draw $m$ distinct cut points and swap every second segment.
- **Uniform crossover.** Draw a mask $M \in \{0,1\}^l$ with independent fair bits. Child 1 takes position $i$ from $a$ if $M_i = 1$ and from $b$ otherwise, and child 2 takes the other gene.

**What is kept.** In all three operators, at each position $i$ the two children hold the two genes $a_i$ and $b_i$, in some order. So a position where $a_i = b_i$ keeps this value in both children, and each child lies between its parents: if $d$ is the [Hamming distance](/hamming-distance/) between the parents, each child differs from $a$ only at positions where $a$ and $b$ differ, so its distance to $a$ plus its distance to $b$ is exactly $d$. Under uniform crossover, child 1 is uniform over the $2^d$ strings that agree with both parents where they agree.

**Disruption of a schema.** A schema $H$ is a pattern such as 1**0*, with fixed positions and wildcards. Its order $o(H)$ is the number of fixed positions, and its defining length $\delta(H)$ is the distance from the first to the last fixed position. Let $a \in H$. Under one-point crossover, the cut falls strictly between two fixed positions of $H$ for exactly $\delta(H)$ of the $l - 1$ cut points. For any other cut, child 1 or child 2 gets all the fixed positions from $a$. So the probability that crossover can disrupt $H$ is at most $\delta(H)/(l - 1)$, which is the crossover factor of the [schema theorem](/schema-theorem/). Short schemata survive one-point crossover well, whatever their order. Under uniform crossover, the probability that child 1 takes all $o(H)$ fixed genes from $a$ is $2^{-o(H)}$, whatever the distance between them. Eshelman, Caruana and Schaffer (1989) called these two effects positional bias and distributional bias.

**Other codings.**

- **Permutations.** For tours of the [traveling salesman problem](/traveling-salesman-problem/), a child must again be a permutation. Order crossover (OX) copies a segment of parent $a$ and fills the free positions with the missing elements in the order in which they appear in $b$. Partially mapped crossover (PMX) and cycle crossover keep other properties of the parents, such as absolute positions.
- **Real vectors.** Arithmetic crossover takes $\lambda a + (1 - \lambda) b$. Blend crossover draws each component uniformly from an interval around $[\min(a_i, b_i), \max(a_i, b_i)]$. The recombination of [differential evolution](/differential-evolution/) mixes a target vector with a mutant vector coordinate by coordinate, which is a uniform crossover with a biased coin.
- **Trees.** Subtree crossover in [genetic programming](/genetic-programming/) picks a node in each parent and swaps the subtrees below them.

**Does crossover help?** It can, and it can also hurt. The [building block hypothesis](/building-block-hypothesis/) says that crossover joins good short parts into better strings, but this hypothesis is disputed. Proved results exist for specific functions: on some functions, an algorithm with crossover is provably faster in expectation than the same algorithm without it, and on others the reverse holds.

## Examples

**One-point crossover.** The parents 11000 and 10011 with the cut $c = 2$ give 11|011 and 10|000, that is 11011 and 10000. Position 1 holds 1 in both parents, so both children have 1 there. The parents differ in positions 2, 4 and 5, so $d = 3$. The child 11011 differs from 11000 in positions 4 and 5 and from 10011 in position 2, and $2 + 1 = 3 = d$.

**Uniform crossover.** The parents 11000 and 10011 with the mask 10110 give child 1 = 1, 0, 0, 0, 1, that is 10001, and child 2 = 1, 1, 0, 1, 0, that is 11010. With a random mask, child 1 is one of the $2^3 = 8$ strings 1?0?? with free positions 2, 4 and 5, each with probability $1/8$.

**Disruption.** Take $l = 5$ and $H = $ 1***1, with $\delta(H) = 4$ and $o(H) = 2$. Every one of the 4 cut points falls between positions 1 and 5, so one-point crossover can break this schema at every cut. The schema 11*** has $\delta = 1$, and only the cut $c = 1$ can break it. Under uniform crossover, both schemata keep all genes of parent $a$ in child 1 with probability $2^{-2} = 1/4$.

**Order crossover.** Let $a = 1\,2\,3\,4\,5\,6\,7\,8$ and $b = 3\,7\,5\,1\,6\,8\,2\,4$, and copy positions 3 to 5 of $a$, that is $3\,4\,5$. Read $b$ from position 6 onward and wrap around: $8\,2\,4\,3\,7\,5\,1\,6$. Drop 3, 4 and 5 to get $8\,2\,7\,1\,6$, and write these into positions 6, 7, 8, 1 and 2. The child is $1\,6\,3\,4\,5\,8\,2\,7$, which is again a permutation.

## Where it is used

- In the [genetic algorithm](/genetic-algorithm/), with one-point, two-point or uniform crossover on strings.
- In [genetic programming](/genetic-programming/), with subtree crossover.
- In [memetic algorithms](/memetic-algorithm/) for routing and scheduling, with permutation crossovers followed by a [local search](/local-search/).
- In [differential evolution](/differential-evolution/) and in [evolution strategies](/evolution-strategies/), where recombination averages or mixes the parents.
- In multi-objective algorithms such as [NSGA-II](/nsga-ii/), with simulated binary crossover on real vectors.

## References
