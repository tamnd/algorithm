---
tag: V8W27B
kind: algorithm
slug: coalescent-simulation
name: Coalescent simulation
aliases:
- Hudson coalescent algorithm
- ms simulation
area: biology/population-genetics
level: core
summary: 'Simulate a neutral sample backward in time: draw exponential waiting times, merge random pairs of lineages, then drop mutations on the tree.'
model: real-ram
complexity:
  vars: {n: the number of sampled copies, s: the number of segregating sites}
  time: {worst: Θ(n + n s + s log s), average: Θ(n + n s + s log s), best: Θ(n + n s + s log s)}
  space: {extra: Θ(n + n s)}
properties: {deterministic: false, exact: true, online: false, recursive: false}
history:
  year: 1983
  people: [Richard R. Hudson]
  note: Hudson simulated samples backward in time under the coalescent in 1983, with recombination, and his program ms of 2002 made the method the standard tool.
prereqs: [kingman-coalescent, infinite-sites-model]
see_also: [ancestral-recombination-graph, sequentially-markov-coalescent, coalescent-theory, wright-fisher-model, site-frequency-spectrum, tajimas-d, gillespie-algorithm, poisson-distribution]
sources:
  - paper: doi:10.1016/0040-5809(83)90013-8
    title: Richard R. Hudson, Properties of a neutral allele model with intragenic recombination, Theoretical Population Biology 23(2), 1983
    locator: pp. 183-201 (samples simulated backward in time, with coalescence and recombination events of the ancestral lineages)
  - paper: doi:10.1093/bioinformatics/18.2.337
    title: Richard R. Hudson, Generating samples under a Wright-Fisher neutral model of genetic variation, Bioinformatics 18(2), 2002
    locator: pp. 337-338 (the program ms, its options for theta, a fixed number of segregating sites and recombination, and its time unit of 4N generations)
  - paper: doi:10.1016/0304-4149(82)90011-4
    title: J. F. C. Kingman, The coalescent, Stochastic Processes and their Applications 13(3), 1982
    locator: pp. 235-248 (the n-coalescent and its rates)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 3 (the coalescent) and Chapter 4 (mutations on the genealogy)
---

Coalescent simulation draws a sample of DNA sequences from a neutral population model by building the genealogy of the sample backward in time and then placing mutations on it, instead of simulating the whole population forward. The basic version, Hudson's algorithm, draws a [Kingman coalescent](/kingman-coalescent/) tree with exponential waiting times and random pairs of lineages to merge, and then puts a Poisson number of mutations on each branch under the [infinite sites model](/infinite-sites-model/). It costs time linear in the size of the sample and its data, not in the size of the population or the number of generations. It produces the null distributions of statistics such as [Tajima's D](/tajimas-d/), and with recombination it simulates the [ancestral recombination graph](/ancestral-recombination-graph/).

## In plain words

To see what neutral data from a population of a million individuals look like, you could simulate the million individuals for many generations and then pick a few of them. Almost all that work is wasted: only the ancestors of the few picked ones matter.

So start from the sample and go back in time. At each step, ask how long until two of the current lineages find a common parent; with many lineages this happens soon, with few it takes long. When it happens, pick two lineages at random and join them. Stop at the single common ancestor. Now the tree is done, and mutations fall on it like rain: a longer branch gets more of them, and everything below a branch carries its mutations.

## The problem

**Input.** A sample size $n \ge 1$, the population mutation rate $\theta = 4N\mu$ of the locus, and a source of random numbers. As an option, a fixed number $s$ of segregating sites instead of $\theta$.

**Output.** A random genealogy and a random sample from the neutral model: a rooted binary tree on the $n$ sampled copies with node ages, the positions of the segregating sites in $[0, 1)$, and the $n \times S$ matrix of alleles, 0 for ancestral and 1 for derived. The joint law of the output must be exactly the law of the model: the Kingman coalescent with time in units of $2N$ generations, and given the tree, mutations as a Poisson process of rate $\theta/2$ along the branches, each at a new uniform position.

The model assumes neutrality, a constant population size, random mating, no structure and no recombination inside the locus. The variants section lifts each of these.

## The algorithm

```pseudo id=main
HUDSON(n, θ)
L1  A ← the n sampled copies, each a node of age 0; t ← 0
L2  while |A| > 1 do
L3      k ← |A|; t ← t + an exponential time with rate k(k − 1)/2
L4      choose two distinct lineages i and j of A uniformly at random
L5      make a node u of age t with the children i and j; replace i and j in A by u
L6  for each branch from a node v to its parent p do
L7      draw M from a Poisson distribution with mean θ/2 · (age of p − age of v)
L8      add M sites at uniform positions in [0, 1), each with allele 1 in the copies below v
L9  sort the sites by position and return the tree and the matrix
```

Lines L1 to L5 build the tree. Each pass of the loop is one coalescence. Line L3 waits for it, and line L4 picks the pair, uniform among the $\binom{k}{2}$ pairs. Lines L6 to L8 add the mutations. The copies below a node are a bit mask in the implementation, built bottom-up in one pass, since a node is always made after its children.

With a fixed number $s$ of segregating sites (the option `-s` of ms), line L7 is replaced by drawing $s$ branches, each with probability proportional to its length. For a fixed tree, that is the law of the sites given $S = s$, because given their number the points of a Poisson process fall independently and uniformly on the tree. It is not the law of the whole sample given $S = s$, since the tree is not weighted by $P(S = s \mid \text{tree})$.

## Example

Take $n = 4$ and $\theta = 2$, and number the copies 1 to 4. Suppose the draws are these.

| step | $k$ | rate $\binom{k}{2}$ | waiting time | age $t$ | pair | new node |
|---|---|---|---|---|---|---|
| 1 | 4 | 6 | 0.10 | 0.10 | 1, 2 | 5 |
| 2 | 3 | 3 | 0.25 | 0.35 | 3, 4 | 6 |
| 3 | 2 | 1 | 0.85 | 1.20 | 5, 6 | 7 (root) |

The branch lengths are 0.10 above copies 1 and 2, 0.35 above copies 3 and 4, 1.10 above node 5 and 0.85 above node 6, a total of $L = 2.85$ (the mean is $2 a_4 = 11/3 = 3.67$). With $\theta = 2$, the mean number of mutations on a branch equals its length. Suppose line L7 gives one mutation above node 5, two above node 6, one above copy 3 and none elsewhere, and line L8 puts them at the positions 0.40, 0.12, 0.93 and 0.71. Sorted by position, the sites are 0.12 (copies 3, 4), 0.40 (copies 1, 2), 0.71 (copy 3) and 0.93 (copies 3, 4), and the sample is

| copy | 0.12 | 0.40 | 0.71 | 0.93 |
|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 1 | 1 |
| 4 | 1 | 0 | 0 | 1 |

So $S = 4$, against the mean $\theta a_4 = 11/3 = 3.67$. The sites 0.12 and 0.93 are on the same branch and have the same pattern; no pair of sites shows all four gametes, as the [four-gamete condition](/four-gamete-condition/) requires without recombination.

## Correctness

The Kingman coalescent of $n$ copies is a Markov chain on partitions of the sample: from a partition with $k$ blocks, each of the $\binom{k}{2}$ pairs of blocks merges at rate 1. In a continuous-time Markov chain with total rate $\lambda$ out of the current state, the time to the next jump is exponential with rate $\lambda$, and the jump goes to each target with probability its rate over $\lambda$, independently of the time. Here $\lambda = \binom{k}{2}$, and every pair has the same rate, so line L3 draws the right waiting time and line L4 the right pair. The node made in line L5 is the block of the merged pair. By induction on the number of merges, the tree after the loop has the law of the Kingman coalescent tree.

Given the tree, the mutations of the model are a Poisson process on the branches with rate $\theta/2$. A Poisson process restricted to disjoint pieces is a set of independent Poisson processes, and the number of points on a piece of length $l$ is Poisson with mean $\theta l / 2$. So line L7 draws the right counts, independently over the branches. Under the infinite sites model each mutation is at a new site, and every copy below the mutated branch, and no other copy, carries the derived allele, which is line L8. The positions are uniform and independent of the tree. So the output has the law of the model. The full proof is below.

## Complexity

- **Tree.** The loop runs $n - 1$ times. With an array of the active lineages and removal by swapping with the last entry, each pass takes $O(1)$ time, so the tree takes $\Theta(n)$ time and space.
- **Mutations.** Line L7 takes $O(1)$ expected time per branch for small means. The $s$ sites take $\Theta(s)$ to draw and $\Theta(s \log s)$ to sort, and the matrix has $n s$ entries. In total $\Theta(n + n s + s \log s)$ time. The expected number of sites is $\theta a_n$, which grows like $\theta \ln n$.
- **Space.** The tree and the matrix: $\Theta(n + n s)$. Storing, for each site, only the branch it is on instead of a column of the matrix takes $\Theta(n + s)$, which is what tree sequence formats do.
- **Against forward simulation.** A [Wright-Fisher](/wright-fisher-model/) simulation of $2N$ copies over the about $4N$ generations to the common ancestor of the sample costs $\Theta(N^2)$ time. The coalescent costs nothing for the copies that are not ancestors of the sample.

## Properties

- **Exact for its model.** The output has exactly the law of the Kingman coalescent with infinite-sites mutations, not an approximation of it. The coalescent is itself the large-population limit of the Wright-Fisher and Moran models.
- **Separation of genealogy and mutation.** Under neutrality, mutations do not change the genealogy, so the tree can be drawn first. This is the reason the method works, and it fails for selected sites.
- **Tree shape and times are independent.** The pairs of line L4 do not depend on the times of line L3. The shape of the tree is the random-joining (Yule-Harding) shape. If the two sides of the root are put in random order, the number of copies on the first side is uniform on $1, \ldots, n - 1$.
- **Reproducible.** With a seeded generator, the draws are made in a fixed order, so the same seed gives the same sample.
- **Expected values to check against.** $E[T_{\text{MRCA}}] = 2(1 - 1/n)$, which is $1.8$ for $n = 10$; $E[L] = 2 a_n = 5.657937$ for $n = 10$; $E[S] = \theta a_n$; $E[\xi_i] = \theta / i$; for $n = 2$, $S$ is geometric with $P(S = k) = (1/(1 + \theta)) (\theta/(1 + \theta))^k$. The tests check all of them.

## Variants and improvements

- **Recombination.** Hudson's 1983 algorithm adds recombination events: a lineage that carries ancestral material over a stretch of sequence splits at rate $\rho/2$ times the length of that stretch, with $\rho = 4Nr$. The result is the [ancestral recombination graph](/ancestral-recombination-graph/), with one tree per stretch of sequence. Its cost grows quickly with $\rho$, because many lineages carry no material that reaches the sample in some regions.
- **Along the sequence.** The [sequentially Markov coalescent](/sequentially-markov-coalescent/) approximates the recombination process by building the local trees from left to right, each from the one before, which is much faster for long sequences.
- **Changing population size.** If the size is $N(t) = N_0 \lambda(t)$, $k$ lineages merge at rate $\binom{k}{2}/\lambda(t)$. The waiting time is then drawn by inverting the integrated rate $\int \binom{k}{2}/\lambda(s)\, ds$, which has a closed form for piecewise constant and exponential $\lambda$.
- **Structure and migration.** With several subpopulations, the state is the number of lineages in each, lineages move between them at the migration rates, and only lineages in the same subpopulation merge. The next event is drawn as in the [Gillespie algorithm](/gillespie-algorithm/), from the total rate of all coalescence and migration events.
- **Finite sites.** Instead of the infinite sites rule, evolve a sequence down the tree under a [substitution model](/substitution-model/) such as [Jukes-Cantor](/jukes-cantor-model/). Then repeat hits and back mutations occur.
- **Modern programs.** ms (Hudson 2002) is the reference program. msprime records the output as a tree sequence and simulates whole chromosomes with recombination for large samples. Programs for selected sites (a sweep, for example) condition the coalescent on a trajectory of the selected allele, or simulate forward in time.

## When to use it

Use it to get the distribution of a statistic under a neutral model when no formula is known, for example the null distribution of [Tajima's D](/tajimas-d/) with recombination, the expected [site frequency spectrum](/site-frequency-spectrum/) under a demographic history, or test data with a known genealogy for inference methods. It is also the simulator in approximate Bayesian computation for population genetics. For models with selection at many sites, or with complex ecology, use forward simulation instead.

## Pitfalls

- **Time units.** This page and most textbooks use units of $2N$ generations, with $\theta = 4N\mu$ and $\theta/2$ per branch. ms uses units of $4N$ generations, so its times and its tree lengths are half of these; the mutation parameter $\theta$ is the same. Mixing the two conventions gives errors by a factor of 2.
- **Haploid and diploid.** For a haploid population of $N$ copies, time is in units of $N$ generations and $\theta = 2N\mu$. The $n$ of the algorithm is the number of sequences, not of individuals.
- **Choosing the pair.** The pair must be uniform among all pairs. A common mistake is to join the first lineage with a random other one, or to join two neighbors in a list, which gives a wrong tree shape with the right times.
- **Fixed $s$ is not a fixed $\theta$.** Samples given $S = s$ are not samples with $\theta = s / a_n$: the conditioning changes the law of the tree length, and the null distribution of a statistic can differ from the one with $\theta$ fixed, most of all in the tails.
- **Random numbers.** Simulation studies run millions of replicates; a generator with a short period or bad seeding across parallel jobs makes replicates dependent.

## Implementations

## History

Kingman described the coalescent in 1982, and Hudson's 1983 paper on intragenic recombination simulated samples backward in time with coalescence and recombination events, the first coalescent simulation. Hudson's 1990 review in Oxford Surveys in Evolutionary Biology explained the method of drawing a genealogy and then placing mutations on it, and his program ms (2002) became the standard simulator for many years. Later programs simulate recombination along whole chromosomes, such as MaCS with the sequentially Markov approximation and msprime with exact recombination and tree sequences.

## References
