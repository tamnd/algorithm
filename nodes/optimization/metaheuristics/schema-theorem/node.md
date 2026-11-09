---
tag: MGN8A0
kind: theorem
slug: schema-theorem
name: Schema theorem
aliases:
- fundamental theorem of genetic algorithms
- Holland's schema theorem
area: optimization/metaheuristics
level: advanced
summary: A lower bound on the expected number of instances of a schema after one generation of roulette selection, one-point crossover and bit mutation. It says nothing about many generations.
prereqs: [genetic-algorithm, roulette-wheel-selection, crossover, mutation]
see_also: [building-block-hypothesis, linearity-of-expectation, evolutionary-computation, no-free-lunch-theorem, walsh-hadamard-transform, fitness-landscape]
sources:
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992 (first edition 1975)
    locator: Chapter 6, Reproductive plans and genetic operators (the effect of selection, crossover and mutation on schemata) and Chapter 7 (the robustness of genetic plans)
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 2, Genetic algorithms revisited, mathematical foundations (the schema theorem and the building block hypothesis)
  - book: isbn:9780262133166
    title: Melanie Mitchell, An Introduction to Genetic Algorithms, MIT Press, 1996
    locator: Chapter 4, Theoretical foundations of genetic algorithms (schemas, the two-armed bandit argument, Royal Road functions, and the critiques)
  - paper: Lee Altenberg, The schema theorem and Price's theorem, in L. D. Whitley and M. D. Vose (editors), Foundations of Genetic Algorithms 3, Morgan Kaufmann, 1995
    title: The schema theorem and Price's theorem
    locator: pages 23 to 49 (the schema theorem as a case of Price's covariance theorem, and why it does not explain performance)
  - paper: John J. Grefenstette and James E. Baker, How genetic algorithms work, a critical look at implicit parallelism, Proceedings of the Third International Conference on Genetic Algorithms, Morgan Kaufmann, 1989
    title: How genetic algorithms work, a critical look at implicit parallelism
    locator: pages 20 to 27
  - paper: Stephanie Forrest and Melanie Mitchell, Relative building-block fitness and the building-block hypothesis, in L. D. Whitley (editor), Foundations of Genetic Algorithms 2, Morgan Kaufmann, 1993
    title: Relative building-block fitness and the building-block hypothesis
    locator: pages 109 to 126 (the Royal Road functions)
  - book: Michael D. Vose, The Simple Genetic Algorithm, Foundations and Theory, MIT Press, 1999
    title: The Simple Genetic Algorithm, Foundations and Theory
    locator: the infinite population model, in which the expected next population is a quadratic map of the current one
  - paper: Chris Stephens and Henri Waelbroeck, Schemata evolution and building blocks, Evolutionary Computation 7(2), 1999
    title: Schemata evolution and building blocks
    locator: pages 109 to 124 (an exact schema equation that includes the gains from crossover)
---

The schema theorem, from Holland's 1975 book, bounds from below the expected number of strings that match a pattern, called a schema, after one generation of a [genetic algorithm](/genetic-algorithm/) with [roulette wheel selection](/roulette-wheel-selection/), one-point [crossover](/crossover/) and bitwise [mutation](/mutation/). The bound is the current number times the ratio of the schema's mean fitness to the population's mean fitness, times the probabilities that crossover and mutation do not destroy the schema. It is an inequality about one generation and an expectation. It does not imply that good schemata grow exponentially over many generations, and it does not explain why or when a genetic algorithm works well.

## Statement

**Setting.** A population $P(t)$ is a multiset of $N$ strings in $\{0,1\}^l$, $l \ge 2$, with fitness $f(x) \ge 0$ and $F(t) = \sum_{x \in P(t)} f(x) > 0$. Let $\bar f(t) = F(t)/N$. One generation makes $P(t+1)$ as $N$ children. Each child is made in this way, and every two children form a pair:

1. Draw two parents $a$ and $b$ independently from $P(t)$, each by roulette: string $x$ with probability $f(x)/F(t)$.
2. With probability $p_c$, draw a cut $c$ uniformly from $\{1, \ldots, l - 1\}$ and form the children $a_1 \ldots a_c b_{c+1} \ldots b_l$ and $b_1 \ldots b_c a_{c+1} \ldots a_l$. Otherwise the children are copies of $a$ and $b$.
3. Flip each bit of each child independently with probability $p_m$.

A **schema** is a word $H \in \{0, 1, *\}^l$. A string $x$ is an instance of $H$, written $x \in H$, if $x_i = H_i$ at every position $i$ with $H_i \ne *$. These positions are the fixed positions of $H$. The **order** $o(H)$ is the number of fixed positions, and the **defining length** $\delta(H)$ is the distance between the first and the last fixed position, with $\delta(H) = 0$ if $o(H) \le 1$. Let $m(H, t)$ be the number of instances of $H$ in $P(t)$, counted with multiplicity, and if $m(H, t) > 0$ let $f(H, t)$ be their mean fitness.

**Theorem (Holland).** For every schema $H$ with $m(H, t) > 0$,
$$\mathrm{E}\big[m(H, t+1) \mid P(t)\big] \;\ge\; m(H, t) \, \frac{f(H, t)}{\bar f(t)} \left(1 - p_c \frac{\delta(H)}{l - 1}\right) (1 - p_m)^{o(H)}.$$
Hence also
$$\mathrm{E}\big[m(H, t+1) \mid P(t)\big] \;\ge\; m(H, t) \, \frac{f(H, t)}{\bar f(t)} \left(1 - p_c \frac{\delta(H)}{l - 1} - o(H) \, p_m\right).$$
The second form is the one in Goldberg's book. If $m(H, t) = 0$, the right side is 0 and the statement holds trivially.

## In plain words

A schema is a pattern with fixed values in some places and "any value" in the others, such as "starts with 1". The theorem looks at one round of a genetic algorithm and asks how many strings will fit the pattern after the round, on average.

Selection pushes the number up when the strings that fit the pattern score above the group average. Crossover can break the pattern, but only when the cut falls between its fixed places, so a pattern whose fixed places are close together is rarely broken. Mutation can break the pattern by changing a fixed place, so a pattern with few fixed places is rarely broken. The theorem puts these three effects in one formula. It ignores the ways in which a round can create new strings that fit the pattern, so it gives a lower bound, not the exact number.

## Proof

Fix $P(t)$ and $H$ with $m = m(H, t) > 0$. All probabilities below are conditional on $P(t)$. Let
$$p_H = \Pr[a \in H] = \sum_{x \in P(t),\, x \in H} \frac{f(x)}{F(t)} = \frac{m \, f(H, t)}{N \bar f(t)},$$
where the sum runs over the strings of $P(t)$ with multiplicity. The parent $b$ has the same law as $a$, and the two are independent.

**Step 1, all children have the same law.** The first child of a pair is $a_{1..c} b_{c+1..l}$ and the second is $b_{1..c} a_{c+1..l}$. Since $a$ and $b$ are independent with the same law, the pair $(b, a)$ has the same law as $(a, b)$. So the second child has the same law as the first, and all $N$ children have the same law. By [linearity of expectation](/linearity-of-expectation/),
$$\mathrm{E}[m(H, t+1)] = N \Pr[\text{child} \in H],$$
where "child" is the first child of a pair after mutation.

**Step 2, crossover.** Let $z$ be the first child before mutation. Let $i_1$ and $i_2$ be the first and last fixed positions of $H$, so $\delta(H) = i_2 - i_1$. We show
$$\Pr[z \in H] \ge p_H \left(1 - p_c \frac{\delta(H)}{l - 1}\right).$$
With probability $1 - p_c$ there is no crossover and $z = a$, so $z \in H$ with probability $p_H$. With probability $p_c$ the cut $c$ is uniform on $\{1, \ldots, l - 1\}$. If $c \ge i_2$, all fixed positions of $z$ come from $a$, so $z \in H$ exactly when $a$ matches $H$ on them, with probability $p_H$. If $c < i_1$, all fixed positions of $z$ come from $b$, again with probability $p_H$. The remaining cuts $c \in \{i_1, \ldots, i_2 - 1\}$ number exactly $\delta(H)$, and for them $\Pr[z \in H \mid c] \ge 0$. So
$$\Pr[z \in H] \ge (1 - p_c) p_H + p_c \frac{(l - 1) - \delta(H)}{l - 1} p_H = p_H \left(1 - p_c \frac{\delta(H)}{l - 1}\right).$$

**Step 3, mutation.** The child is in $H$ if $z \in H$ and none of the $o(H)$ fixed bits flips. The flips are independent of $z$, so
$$\Pr[\text{child} \in H] \ge \Pr[z \in H] \, (1 - p_m)^{o(H)}.$$

**Step 4, the first form.** By Steps 1 to 3,
$$\mathrm{E}[m(H, t+1)] \ge N p_H \left(1 - p_c \frac{\delta(H)}{l - 1}\right)(1 - p_m)^{o(H)} = m \frac{f(H, t)}{\bar f(t)} \left(1 - p_c \frac{\delta(H)}{l - 1}\right)(1 - p_m)^{o(H)}.$$

**Step 5, the second form.** Let $u = p_c \delta(H)/(l - 1) \in [0, 1]$ and $v = o(H) p_m \ge 0$. By Bernoulli's inequality, $(1 - p_m)^{o(H)} \ge 1 - v$. If $1 - v \ge 0$, then $(1 - u)(1 - p_m)^{o(H)} \ge (1 - u)(1 - v) = 1 - u - v + uv \ge 1 - u - v$. If $1 - v < 0$, then $1 - u - v < 0 \le (1 - u)(1 - p_m)^{o(H)}$. In both cases the factor of the first form is at least $1 - u - v$, and $m f(H, t)/\bar f(t) \ge 0$. $\blacksquare$

The proof drops two kinds of terms: the cuts inside the defining length that still give an instance, because the other parent matches the rest of $H$, and the strings outside $H$ that become instances by crossover or mutation. These are the gains. The bound counts only losses.

## Consequences

**What it says.** In one generation, a schema whose instances have mean fitness above the population mean, whose defining length is short relative to $l$ and whose order is low, is expected to gain instances, as long as the selection factor $f(H, t)/\bar f(t)$ is larger than the losses. For example, with $p_c = 0.6$, $p_m = 0.01$, $l = 20$ and a schema with $\delta(H) = 2$ and $o(H) = 3$, the loss factor is at least $1 - 0.6 \cdot 2/19 - 0.03 \approx 0.907$, so the expected count grows if $f(H, t)/\bar f(t) > 1.103$.

**What it does not imply.**

- **No exponential growth over many generations.** The bound is about one step and depends on $f(H, t)$ and $\bar f(t)$, which change from one generation to the next. As instances of a good schema spread, $\bar f(t)$ approaches $f(H, t)$, and the ratio tends to 1. The expectation of a product of random ratios is not the product of their expectations, so the one-step bound cannot simply be iterated. The common phrase "short, low-order, above-average schemata receive exponentially increasing trials" is not a consequence of the theorem.
- **No statement about finding good strings.** The theorem says that instances of $H$ are not lost faster than a given rate. It does not say that the genetic algorithm finds an optimum, or how fast, and the [no free lunch theorem](/no-free-lunch-theorem/) shows that no such statement holds for all functions.
- **No statement about combining schemata.** The theorem has no term for the creation of new good schemata by crossover. The claim that a genetic algorithm works by joining short good schemata is the separate [building block hypothesis](/building-block-hypothesis/), which the theorem does not prove.
- **Fitness of a schema is measured in the population.** The value $f(H, t)$ is the mean over the instances present in $P(t)$, weighted by their copies, not the mean over all $2^{l - o(H)}$ instances of $H$. In a small population it says little about the schema as a whole.
- **It holds for any subset of this kind, so it does not single out schemata.** Altenberg (1995) showed that the theorem is a case of Price's theorem from population genetics, and that a bound of the same form holds for any set of strings whose disruption can be bounded. Since it holds for every schema at once and does not use the structure of $f$, it cannot tell which schemata matter for performance. Altenberg argued that performance depends on the covariance between the fitness of parents and the fitness of their children, which the schema theorem does not measure.
- **Implicit parallelism.** Holland and Goldberg argued that a population of $N$ strings processes about $N^3$ schemata usefully at once. Grefenstette and Baker (1989) and the discussion in Mitchell (1996, Chapter 4) show that this argument does not give a speed advantage: the observed fitness of a schema in a small sample is a poor estimate of its true mean, and the claim relies on the theorem's one-step bound.

**Exact versions.** The full expected next population of this generation is a quadratic function of the current proportions, which Vose's infinite population model describes exactly. Stephens and Waelbroeck (1999) gave an exact schema equation that includes the gain terms. Both confirm that the one-step bound can be far from the actual expectation, as the next section shows.

## Tightness

**Equality without disruption.** If $p_c \delta(H) = 0$ and $p_m o(H) = 0$, for example with no crossover and no mutation, both forms hold with equality: $\mathrm{E}[m(H, t+1)] = m(H, t) f(H, t)/\bar f(t)$. This is the selection step alone, whose expected copy count is exact.

**Strict in general.** With crossover inside the defining length and $p_m < 1$, the bound is strict whenever $m(H, t) > 0$: both parents are instances of $H$ with probability $p_H^2 > 0$, and then every cut gives an instance. So the first form is never an equality when $p_c \delta(H) > 0$. The gap can be large, as the exact computation below shows.

**A computed example.** Take the population 01101, 11000, 01000, 10011 with $f(x) = x^2$, so $\bar f = 292.5$. The table gives the exact expectation, computed by summing over all parent pairs, cuts and mutations with exact rational arithmetic, and the first form of the bound.

| schema | $m$ | $f(H)$ | $\delta$ | $o$ | exact $\mathrm{E}$, $p_c = 1$, $p_m = 0.001$ | bound | exact $\mathrm{E}$, $p_c = 0.6$, $p_m = 0.01$ | bound |
|---|---|---|---|---|---|---|---|---|
| 1**** | 2 | 468.5 | 0 | 1 | 3.2010 | 3.2002 | 3.1794 | 3.1714 |
| *1*** | 2 | 372.5 | 0 | 1 | 2.7643 | 2.7630 | 2.7505 | 2.7382 |
| 11*** | 1 | 576 | 1 | 2 | 2.0285 | 1.4740 | 1.9856 | 1.6405 |
| 1***1 | 1 | 361 | 4 | 2 | 1.4503 | 0 | 1.3599 | 0.4839 |
| 1*0** | 2 | 468.5 | 2 | 2 | 2.9668 | 1.5985 | 3.0086 | 2.1978 |

For 1***1 with $p_c = 1$, every cut falls inside the defining length, so the bound is 0, but the expected count is 1.45. For order-1 schemata, crossover cannot disrupt and the bound is within 0.1 percent of the exact value at $p_m = 0.001$.

**The selection factor is sharp.** The factor $f(H, t)/\bar f(t)$ cannot be replaced by a larger one: with $p_c = p_m = 0$ the bound is an equality.

## History

Holland introduced schemata and the analysis of their expected growth under his reproductive plans in *Adaptation in Natural and Artificial Systems* (1975), together with the argument from the two-armed bandit that a genetic plan allocates trials to schemata in a near-optimal way. Goldberg's 1989 book gave the form with $1 - p_c \delta(H)/(l-1) - o(H) p_m$, called it the fundamental theorem of genetic algorithms, and stated the building block hypothesis next to it. From the late 1980s the explanatory value of the theorem was questioned: Grefenstette and Baker (1989) criticized implicit parallelism, Forrest and Mitchell (1993) found that the Royal Road functions did not behave as the building block view predicts, and Altenberg (1995) related the theorem to Price's theorem and showed what it leaves out. Exact models by Vose and by Stephens and Waelbroeck (1999) and the runtime analysis of evolutionary algorithms have since replaced the theorem as the main tools of genetic algorithm theory.

## References
