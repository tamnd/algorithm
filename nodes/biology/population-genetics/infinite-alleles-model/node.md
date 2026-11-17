---
tag: AWDSAS
kind: model
slug: infinite-alleles-model
name: Infinite alleles model
aliases:
- Kimura-Crow model
area: biology/population-genetics
level: core
summary: "A mutation model in which every mutation creates an allele never seen before, so alleles are labels and only their counts matter."
history:
  year: 1964
  people: [Motoo Kimura, James F. Crow]
  note: "Kimura and Crow introduced the model in 1964 to find how many alleles a finite population can keep. Ewens (1972) found the distribution of the allele counts in a sample."
prereqs: [wright-fisher-model, genetic-drift]
see_also: [ewens-sampling-formula, infinite-sites-model, kingman-coalescent, moran-model, genetic-drift, effective-population-size, dirichlet-process, random-permutation]
sources:
  - paper: "Motoo Kimura and James F. Crow, The number of alleles that can be maintained in a finite population, Genetics 49(4), 1964"
    title: Kimura and Crow 1964
    locator: pp. 725-738 (the model, the equilibrium homozygosity and the effective number of alleles 4Nu + 1)
  - paper: "Warren J. Ewens, The sampling theory of selectively neutral alleles, Theoretical Population Biology 3(1), 1972"
    title: Ewens 1972
    locator: the distribution of the allele counts in a sample under this model
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.6 (infinitely many alleles models, p. 111) and Section 3.6.4 (the Moran model with infinitely many alleles, p. 117)
---

The infinite alleles model is a model of mutation in which each mutation makes an allele that is new to the population. So two gene copies carry the same allele only if no mutation has happened on either line since their common ancestor, and an allele is only a label. Kimura and Crow used it on a [Wright-Fisher](/wright-fisher-model/) population to find how much variation [genetic drift](/genetic-drift/) and mutation keep in balance. It is the model behind the [Ewens sampling formula](/ewens-sampling-formula/).

## The machine

**The state.** A population of $2N$ gene copies (for example $N$ diploids) in discrete generations. Each copy carries an allele label. The state is the partition of the $2N$ copies into allele classes; the names of the labels do not matter.

**The step.** Each copy of the next generation picks a parent copy uniformly and independently, as in the Wright-Fisher model. Then it mutates with probability $u$, independently of the others. A copy that mutates gets a label that no copy has had before. A copy that does not mutate keeps the label of its parent. The scaled mutation rate is

$$\theta = 4Nu,$$

twice the expected number of new mutations per generation.

**A simulation.**

```pseudo id=main
INFINITE-ALLELES(2N, u, T)
L1  labels ← 2N copies of allele 0; fresh ← 1
L2  for t ← 1 to T do
L3      for each new copy, pick a parent copy uniformly among the 2N copies
L4      with probability u give it the label fresh and add 1 to fresh, else copy the label of its parent
L5      replace the population by the new copies
L6  return the allele classes of the labels
```

Each generation costs $O(N)$ random draws, so $T$ generations take $O(NT)$ time. The implementation also has the exact homozygosity recursion and the Hoppe urn, which draws a sample from the stationary distribution directly.

**A trace.** With seed 7, $2N = 20$ and $u = 0.05$ ($\theta = 2$), the sizes of the allele classes are $(19, 1)$ after 1 and 5 generations, $(13, 4, 2, 1)$ after 10, $(11, 5, 1, 1, 1, 1)$ after 20 and $(8, 5, 3, 2, 1, 1)$ after 40. The original allele is still the most common one, but it has lost more than half its copies.

## What it counts

- The number of distinct alleles in the population or in a sample of $n$ copies.
- The allele counts: how many alleles have exactly $j$ copies, for each $j$.
- The homozygosity $F$: the probability that two distinct copies carry the same allele. Its inverse $1/F$ is the effective number of alleles.
- Identity by descent: two copies have the same allele exactly when no mutation has happened on their two lines back to their common ancestor.

## Relation to other models

- **[Wright-Fisher model](/wright-fisher-model/) and [Moran model](/moran-model/).** The infinite alleles model is a mutation rule on top of a model of reproduction. On the Moran model many results are exact (Ewens 2004, Section 3.6.4); on the Wright-Fisher model they hold to first order in $u$ and $1/N$.
- **$K$-allele models.** With $K$ alleles and mutation to each of the others at equal rates, a mutation can make an allele that already exists. As $K \to \infty$, this model tends to the infinite alleles model.
- **[Infinite sites model](/infinite-sites-model/).** Each mutation hits a new site of a long DNA sequence. If the sequence is the allele, the infinite sites model gives an infinite alleles model, but it also keeps the information of which mutations two alleles share.
- **[Kingman coalescent](/kingman-coalescent/).** Run back in time, the genealogy of a sample is the coalescent. Mutations fall on its branches at rate $\theta/2$ per lineage, and each mutation cuts the lineages below it off as a new allele. This gives the [Ewens sampling formula](/ewens-sampling-formula/).
- **The Chinese restaurant process and the [Dirichlet process](/dirichlet-process/).** The Hoppe urn that draws a sample under this model is the Chinese restaurant process with parameter $\theta$, and the allele frequencies in a large population follow the Poisson-Dirichlet law. For $\theta = 1$, the allele counts of a sample of $n$ have the law of the cycle lengths of a uniform [random permutation](/random-permutation/).

## Known results in the model

**The homozygosity recursion.** Let $F_t$ be the probability that two distinct copies of generation $t$ carry the same allele. Then

$$F_{t+1} = (1 - u)^2\Big(\frac{1}{2N} + \Big(1 - \frac{1}{2N}\Big)F_t\Big).$$

*Proof.* Two distinct copies of generation $t + 1$ have the same parent copy with probability $1/(2N)$, and two distinct parent copies otherwise, which carry the same allele with probability $F_t$. They carry the same allele after the step exactly when this holds and neither copy mutates, which has probability $(1 - u)^2$; a mutation always gives a new label. $\square$

**The equilibrium homozygosity.** The recursion is linear with the factor $(1 - u)^2(1 - 1/(2N)) < 1$, so $F_t$ tends to its unique fixed point

$$F^* = \frac{(1 - u)^2}{2N - (2N - 1)(1 - u)^2} \approx \frac{1}{1 + 4Nu} = \frac{1}{1 + \theta}.$$

The approximation drops terms of order $u^2$ and $u/N$. It is good when $u$ is small: for $N = 50$ and $u = 0.001$ ($\theta = 0.2$), $F^* = 0.833125$ against $1/(1 + \theta) = 0.833333$. It is poor when $u$ is not small: for $2N = 20$ and $u = 0.05$ ($\theta = 2$), $F^* = 0.316389$ against $0.333333$, 5 percent off. The approach to $F^*$ is geometric with rate about $2u + 1/(2N)$ per generation. The implementation checks the recursion against 10000 simulated populations.

The same value comes from the genealogy: going back, the two lines merge at rate $1/(2N)$ and one of them mutates at rate $2u$ per generation, so the chance that they merge first is about $(1/(2N))/(1/(2N) + 2u) = 1/(1 + \theta)$.

**The effective number of alleles (Kimura and Crow 1964).** The number $n_e = 1/F^* \approx 1 + 4Nu$ is the number of equally common alleles that would give the same homozygosity. The true number of alleles present is larger, because most of them are rare. For $\theta = 2$ there are about 3 alleles in this sense, while the trace above has 6 after 40 generations.

**Samples.** In the limit of large $N$ with $\theta$ fixed, the allele counts of a sample of $n$ copies have the [Ewens sampling formula](/ewens-sampling-formula/) as their law. A sample can be drawn with the Hoppe urn: copy $k + 1$ is a new allele with probability $\theta/(\theta + k)$, and otherwise a copy of one of the first $k$ copies, chosen uniformly. The number of alleles $K_n$ in the sample has

$$\mathbb E[K_n] = \sum_{i=0}^{n-1} \frac{\theta}{\theta + i} \approx \theta \ln n.$$

With $\theta = 1$ this is $4.50$ for $n = 50$ and $5.19$ for $n = 100$: doubling the sample adds less than one allele on average. The implementation compares the Hoppe urn with the exact formula by a chi-squared test.

**Without mutation.** With $u = 0$ the recursion gives $1 - F_t = (1 - 1/(2N))^t(1 - F_0)$: drift alone removes all variation, and one allele fixes.

**A test of neutrality.** Given the number of alleles in a sample, the law of the allele counts does not depend on $\theta$. Watterson (1977) used this to test neutrality: a sample with too even counts suggests balancing selection, and one with too many rare alleles suggests a recent expansion or weak purifying selection.

## References
