---
tag: 6CBPCS
kind: concept
slug: coalescent-theory
name: Coalescent theory
aliases:
- coalescence
- gene genealogy theory
area: biology/phylogenetics
level: advanced
summary: The study of the genealogy of sampled gene copies traced backward in time, as lineages merge one pair at a time until one common ancestor is left.
prereqs: [phylogenetic-tree, rooted-and-unrooted-trees, poisson-distribution]
see_also: [kingman-coalescent, multispecies-coalescent, incomplete-lineage-sorting, ancestral-recombination-graph, yule-model, birth-death-process, molecular-clock]
sources:
  - paper: doi:10.1016/0304-4149(82)90011-4
    title: J. F. C. Kingman, The coalescent, Stochastic Processes and their Applications 13(3), 1982
    locator: pp. 235-248 (the coalescent as the limit of the genealogy of a sample, with pair merge rate 1 on the scaled time axis)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 3 (the coalescent) and Chapter 4 (neutral mutations and genetic polymorphism)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 26 (coalescent trees) and Chapter 28 (coalescents and species trees)
  - paper: doi:10.1016/0040-5809(75)90020-9
    title: G. A. Watterson, On the number of segregating sites in genetical models without recombination, Theoretical Population Biology 7(2), 1975
    locator: pp. 256-276 (the mean and variance of the number of segregating sites, and the estimator S divided by a_n)
---

Coalescent theory studies the genealogy of a sample of gene copies from a population, traced backward in time from the present. Going back, the ancestral lines of the copies, called lineages, merge in pairs (they *coalesce*) until one lineage is left: the most recent common ancestor (MRCA) of the sample. Under neutral evolution the genealogy does not depend on the mutations, so a model can first draw a random [rooted tree](/rooted-and-unrooted-trees/) and then put mutations on its branches as a [Poisson](/poisson-distribution/) process. The basic model is the [Kingman coalescent](/kingman-coalescent/); other models add changes of population size, population structure, recombination and species boundaries.

## In plain words

Take a few copies of one gene from people alive today. Each copy came from a parent copy one generation back, and that one from a grandparent copy, and so on. Follow these lines back in time. Sometimes two lines reach the same ancestor copy. From then on they are one line. In the end all lines meet in one ancestor.

The times of these meetings are random. In a large population two lines take a long time to meet, because there are many possible parents. When many lines are left, some pair meets soon, because there are many pairs. So the tree has short branches near the present and a long wait at the top, when only two lines are left.

The genealogy is never seen. The data are the mutations that fell on its branches. Coalescent theory links the two.

## The idea

**The population model and the time scale.** Take a Wright-Fisher population of $N$ diploid individuals, so $2N$ gene copies, with no selection and no recombination in the gene. Each copy in a generation picks its parent copy uniformly from the $2N$ copies of the generation before. Two copies pick the same parent with probability $1/(2N)$, so the number of generations back to their common ancestor is geometric with mean $2N$. Measure time in units of $2N$ generations. Then, as $N \to \infty$, this time tends to an exponential random variable with mean 1. For a haploid population of $N$ copies the unit is $N$ generations. Each page here states its unit, because books use both.

**Many lineages.** With $k$ lineages there are $\binom{k}{2}$ pairs. In one generation some pair merges with probability about $\binom{k}{2}/(2N)$, and two merges in one generation have a probability of order $k^4/N^2$. Over the $2N$ generations of one time unit, the expected number of such double events is of order $k^4/N$, which tends to zero. So, in the limit, the waiting time while $k$ lineages remain is exponential with rate $\binom{k}{2}$, and each merge joins one uniformly chosen pair. Kingman proved that the genealogy of a sample converges to this process. The process is the [Kingman coalescent](/kingman-coalescent/), and its page has the proofs of the results below.

**Genealogy first, mutations second.** Under neutrality, the number of offspring of a copy does not depend on its allele. So the genealogy has the same distribution whatever the alleles are. Mutations then fall on each branch at rate $\theta/2$ per unit of time, where $\theta = 4N\mu$ for a diploid population with mutation rate $\mu$ per copy per generation. The number of mutations on a branch of length $t$ is Poisson with mean $\theta t/2$. This order of work, a random tree first and then mutations, makes simulation fast: a sample needs about $n$ steps, not a forward simulation of the whole population.

**What follows.** With $n$ sampled copies, the expected time to the MRCA is $2(1 - 1/n)$ units. The last wait, with two lineages, has mean 1, so it is on average more than half of the depth of the tree. A larger sample adds many short branches near the present and almost no depth. The expected sum of all branch lengths is $2 a_n$ with $a_n = \sum_{i=1}^{n-1} 1/i$, so the expected number $S$ of mutated sites (segregating sites, under the infinite-sites model) is $\theta a_n$. This gives Watterson's estimator $\hat\theta_W = S / a_n$.

**The effective size.** Real populations do not follow the Wright-Fisher rules. Many other models give the same limit with $N$ replaced by an *effective population size* $N_e$. The formulas above then hold with $N_e$, and the estimates of $\theta$ from data are estimates of $4 N_e \mu$.

**Extensions.** Each one changes the rates of the process, not the backward view:

| model | what changes |
|---|---|
| changing population size | the merge rate at time $t$ is $\binom{k}{2} N(0)/N(t)$ |
| structured populations | lineages merge only inside a deme, and move between demes at the migration rates |
| recombination | a lineage can split into two going back; the graph is the [ancestral recombination graph](/ancestral-recombination-graph/) |
| several species | the coalescent runs inside each branch of a species tree: the [multispecies coalescent](/multispecies-coalescent/) |
| high variance in offspring numbers | more than two lineages can merge at one time (coalescents with multiple mergers) |

**Difference from forward models of trees.** The [Yule model](/yule-model/) and the [birth-death process](/birth-death-process/) grow a tree of species forward in time. The coalescent builds a tree of gene copies inside one population, backward in time. The Kingman coalescent and the Yule model give the same distribution of labeled tree shapes, but their branch lengths differ. With $k$ lineages, the coalescent waits at rate $\binom{k}{2}$ and the Yule model at rate $k\lambda$. So a coalescent tree spends a much larger part of its depth in its last two lineages.

## Examples

**Two copies.** In a diploid population with $N = 10{,}000$, two copies have an expected time to their common ancestor of $2N = 20{,}000$ generations. The probability that they have not yet coalesced after $2N$ generations is $e^{-1} \approx 0.368$.

**Ten copies.** For $n = 10$, the expected time to the MRCA is $2(1 - 1/10) = 1.8$ units, or $36{,}000$ generations when $N = 10{,}000$. The last wait, with two lineages, has mean 1 unit, which is $1/1.8 \approx 55.6\%$ of the expected depth. The expected sum of branch lengths is $2 a_{10} = 2 \cdot \tfrac{7129}{2520} \approx 5.658$ units.

**Watterson's estimator.** A sample of $n = 10$ sequences of $10{,}000$ sites has $S = 20$ segregating sites. Then $a_{10} = 1 + \tfrac12 + \cdots + \tfrac19 = \tfrac{7129}{2520} \approx 2.829$ and $\hat\theta_W = 20 / 2.829 \approx 7.07$ for the region, or about $7.07 \times 10^{-4}$ per site. With $\mu = 10^{-8}$ per site per generation, $N_e = \theta/(4\mu) \approx 17{,}700$. The estimate is noisy: at $\theta = 7.07$ the standard deviation of $S$ is $\sqrt{\theta a_n + \theta^2 b_n} \approx 9.85$, with $b_n = \sum_{i=1}^{n-1} 1/i^2$, so $S$ alone gives a wide interval.

**Gene trees inside a species tree.** Two species split $T$ coalescent units ago. One copy from each species cannot coalesce before the split, so their genealogy is older than the split. The expected extra age is 1 unit in the ancestral population. This simple fact is the start of the [multispecies coalescent](/multispecies-coalescent/) and of [incomplete lineage sorting](/incomplete-lineage-sorting/).

## Where it is used

- **Estimating population parameters.** The values of $\theta$, of $N_e$ and of growth rates come from the number and frequencies of segregating sites, with likelihoods computed over random genealogies.
- **Tests of neutrality.** Tests such as Tajima's D compare two estimators of $\theta$ that agree in expectation under the neutral coalescent, so a large difference points to selection or to a change of population size.
- **Simulation.** Coalescent simulators make samples of DNA sequences in time proportional to the sample, not to the population. They are the null model of many population genetics studies.
- **Species trees.** The [multispecies coalescent](/multispecies-coalescent/) explains why gene trees disagree with the species tree, and it is the model behind [species tree estimation](/species-tree-estimation/) methods such as [ASTRAL](/astral/).
- **Recombination and mapping.** The [ancestral recombination graph](/ancestral-recombination-graph/) extends the coalescent along a chromosome, and it is used for association mapping and for scans of selection.
- **Dating.** Coalescent times in units of $2N_e$ generations, together with a [molecular clock](/molecular-clock/), give the ages of common ancestors of genes.

## References
