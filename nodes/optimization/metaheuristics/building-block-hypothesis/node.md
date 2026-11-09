---
tag: 5V7KBH
kind: concept
slug: building-block-hypothesis
name: Building block hypothesis
aliases:
- BBH
- building blocks
area: optimization/metaheuristics
level: advanced
summary: The claim that a genetic algorithm works by joining short, low-order, fit schemata into better strings. It is not a theorem, and experiments and analyses since 1993 have questioned it.
prereqs: [schema-theorem]
see_also: [genetic-algorithm, crossover, estimation-of-distribution-algorithm, fitness-landscape, hill-climbing, no-free-lunch-theorem]
sources:
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 2, Section on the building block hypothesis, and the discussion of deception
  - book: isbn:9780262133166
    title: Melanie Mitchell, An Introduction to Genetic Algorithms, MIT Press, 1996
    locator: Chapter 4, Theoretical foundations of genetic algorithms (Royal Road functions, hitchhiking, and the comparison with hill climbing)
  - paper: Stephanie Forrest and Melanie Mitchell, Relative building-block fitness and the building-block hypothesis, in L. D. Whitley (editor), Foundations of Genetic Algorithms 2, Morgan Kaufmann, 1993
    title: Relative building-block fitness and the building-block hypothesis
    locator: pages 109 to 126 (the Royal Road functions R1 and R2 and the results of the genetic algorithm on them)
  - paper: Melanie Mitchell, John H. Holland and Stephanie Forrest, When will a genetic algorithm outperform hill climbing, Advances in Neural Information Processing Systems 6, 1994
    title: When will a genetic algorithm outperform hill climbing
    locator: pages 51 to 58 (random mutation hill climbing on Royal Road functions and the idealized genetic algorithm)
  - paper: Lee Altenberg, The schema theorem and Price's theorem, in L. D. Whitley and M. D. Vose (editors), Foundations of Genetic Algorithms 3, Morgan Kaufmann, 1995
    title: The schema theorem and Price's theorem
    locator: pages 23 to 49 (why the schema theorem does not support the building block hypothesis)
  - paper: Thomas Jansen and Ingo Wegener, The analysis of evolutionary algorithms, a proof that crossover really can help, Algorithmica 34(1), 2002
    title: The analysis of evolutionary algorithms, a proof that crossover really can help
    locator: pages 47 to 66 (the jump functions)
  - paper: Thomas Jansen and Ingo Wegener, Real royal road functions, where crossover provably is essential, Discrete Applied Mathematics 149, 2005
    title: Real royal road functions, where crossover provably is essential
    locator: pages 111 to 125
  - paper: doi:10.1016/S0304-3975(01)00182-7
    title: Stefan Droste, Thomas Jansen and Ingo Wegener, On the analysis of the (1+1) evolutionary algorithm, Theoretical Computer Science 276(1-2), 2002
    locator: pages 51 to 81 (the bound Θ(n^m + n log n) on jump functions)
---

The building block hypothesis, stated by Goldberg in 1989, says that a [genetic algorithm](/genetic-algorithm/) works by finding short, low-order schemata of high fitness, called building blocks, and joining them by [crossover](/crossover/) into better and better strings. It was offered next to the [schema theorem](/schema-theorem/) as the explanation of why genetic algorithms work, but the theorem does not prove it. Experiments on the Royal Road functions (Forrest and Mitchell 1993), the analysis of Altenberg (1995) and the discussion in Mitchell's book (1996) showed that it fails as a general explanation. Proved results now show that crossover helps on some functions and not on others.

## In plain words

Think of a good solution as a set of good small parts. One string may have a good first part, and another string may have a good last part. If you cut both and join the right pieces, you get a string with both good parts. The hypothesis says that this is how a genetic algorithm makes progress: it finds good small parts, keeps them through selection, and puts them together through crossover.

The idea is easy to like, but it is a guess, not a proof. Tests on functions built to reward exactly this kind of joining showed that a genetic algorithm often did worse than a simple method that only changes one string at random. On other functions, careful proofs show that crossover does help. So the picture is true for some problems and false for others.

## The idea

A **schema** is a pattern in $\{0, 1, *\}^l$, such as 11******. Its order is the number of fixed positions and its defining length is the distance between the first and the last fixed position. The [schema theorem](/schema-theorem/) gives, for one generation, a lower bound on the expected number of instances of a schema. The bound is close to the selection term $m(H, t) f(H, t)/\bar f(t)$ when the schema is short and of low order, so these are the schemata that selection can increase without much loss.

**The hypothesis.** Goldberg stated it as follows: short, low-order, highly fit schemata are sampled, recombined and resampled to form strings of potentially higher fitness. A genetic algorithm then works by assembling building blocks, much as one builds a structure from bricks.

**What the schema theorem gives and does not give.** The theorem bounds the loss of instances by crossover. It has no term for the gain when crossover joins two different schemata in one child, which is the process that the hypothesis needs. So the hypothesis is an extra claim.

**Critiques.**

- **Royal Road functions.** Forrest and Mitchell (1993) built functions that reward exactly the joining of blocks. On $R_1$, a string of 64 bits is cut into 8 blocks of 8 bits, and each block that is all ones adds 8 to the fitness. If the hypothesis were the whole story, a genetic algorithm should do very well here. It did not: random mutation hill climbing, which flips one random bit and keeps the result if it is not worse, needed far fewer evaluations on average (Mitchell, Holland and Forrest 1994; Mitchell 1996, Chapter 4).
- **Hitchhiking.** Once a string with a good block takes over, the bits at the other positions of that string spread with it, whether they are good or not. This reduces the diversity at the positions of other blocks and slows the discovery of those blocks. It is one reason for the results on Royal Road functions.
- **The schema theorem is not specific.** Altenberg (1995) showed that the schema theorem is a case of Price's theorem from population genetics. A bound of the same form holds for any set of strings whose disruption can be bounded, so it does not single out short schemata as the units of search. What matters for progress is the covariance between the fitness of parents and that of their children, and the theorem does not address it.
- **Deception.** A function is deceptive when low-order schemata with high mean fitness point away from the optimum. On such functions, joining good low-order schemata leads to the wrong string. Goldberg himself used deceptive functions to show when a genetic algorithm can fail.

**Results that support a weaker form.** Rigorous runtime analysis gives cases where crossover provably helps.

- **Jump functions.** On $\mathrm{Jump}_m$, a string must jump over a gap of $m$ bits. A mutation-only $(1+1)$ EA needs $\Theta(n^m)$ expected evaluations (Droste, Jansen and Wegener 2002). Jansen and Wegener (2002) proved that a genetic algorithm with uniform crossover, used with a small probability, needs far fewer, because crossover can join two strings whose zeros are in different places.
- **Real royal roads.** Jansen and Wegener also gave functions on which every mutation-only algorithm of a given kind needs exponential time, but a genetic algorithm with crossover needs polynomial time.

On other functions crossover slows the search or makes no difference. So the honest form of the hypothesis is a statement about some functions, not an explanation of genetic algorithms in general.

**Linkage learning.** If good blocks exist but their positions are not adjacent, one-point crossover breaks them. The messy genetic algorithm, linkage learning methods and [estimation of distribution algorithms](/estimation-of-distribution-algorithm/) such as the Bayesian optimization algorithm try to learn which positions belong together and to recombine whole blocks. They are the main design idea that came out of the hypothesis.

## Examples

**Royal Road $R_1$.** Let $x \in \{0,1\}^{64}$ and let $s_i$ be the schema with ones in positions $8i - 7$ to $8i$ and $*$ elsewhere, for $i = 1, \ldots, 8$. Then
$$R_1(x) = \sum_{i=1}^{8} 8 \cdot [x \in s_i].$$
The string with blocks 1 and 3 complete has fitness 16. Crossover of a string with block 1 and a string with block 3, with a cut between the blocks, gives such a string in one step. This is the joining that the hypothesis describes. The optimum is $1^{64}$ with fitness 64.

**A deceptive trap.** For a block of $k = 4$ bits with $u$ ones, let $\mathrm{trap}(u) = 4$ if $u = 4$ and $3 - u$ otherwise. So the values for $u = 0, 1, 2, 3, 4$ are $3, 2, 1, 0, 4$. Over all 8 strings of the schema 0***, the number of ones is $0, 1, 1, 1, 2, 2, 2, 3$, and the mean value is $(3 + 3 \cdot 2 + 3 \cdot 1 + 0)/8 = 1.5$. Over the 8 strings of 1***, the number of ones is $1, 2, 2, 2, 3, 3, 3, 4$, and the mean value is $(2 + 3 \cdot 1 + 3 \cdot 0 + 4)/8 = 1.125$. So the order-1 schema 0*** looks better, but the optimum 1111 lies in 1***. A function made of several such blocks misleads the joining of low-order schemata.

**One cut, two blocks.** With $l = 8$, the parents 11110000 and 00001111 have one good block each under $R$ with two blocks of 4 bits. One-point crossover with the cut after position 4 gives 11111111 and 00000000. For the other 6 cuts, neither child is $1^8$. So the joining needs the right cut, which has probability $1/7$ here.

## Where it is used

- As the motivation for the design of competent genetic algorithms, which learn the linkage between positions.
- As the motivation for [estimation of distribution algorithms](/estimation-of-distribution-algorithm/) that model the dependence between variables.
- In the design of test functions such as Royal Road functions, trap functions and hierarchical functions, which test whether a method can join blocks.
- In the runtime analysis of crossover, which replaces the hypothesis by proved statements for specific functions.

## References
