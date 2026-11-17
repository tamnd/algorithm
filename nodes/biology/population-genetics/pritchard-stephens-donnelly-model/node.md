---
tag: M3YDR9
kind: model
slug: pritchard-stephens-donnelly-model
name: Pritchard-Stephens-Donnelly admixture model
aliases:
- STRUCTURE model
area: biology/population-genetics
level: core
summary: A Bayesian model where each individual has ancestry proportions over K populations with their own allele frequencies, fitted by Gibbs sampling.
history:
  year: 2000
  people: [Jonathan K. Pritchard, Matthew Stephens, Peter Donnelly]
  note: "Pritchard, Stephens and Donnelly gave the model without admixture and the admixture model, with Dirichlet priors and a Gibbs sampler, in the program STRUCTURE in 2000. Falush, Stephens and Pritchard added linked loci and correlated allele frequencies in 2003."
prereqs: [population-structure-inference, gibbs-sampling, hardy-weinberg-principle]
see_also: [maximum-likelihood-admixture-estimation, latent-dirichlet-allocation, dirichlet-process, local-ancestry-inference, genetic-principal-components, fixation-index, bayesian-inference, expectation-maximization]
sources:
  - paper: doi:10.1093/genetics/155.2.945
    title: Jonathan K. Pritchard, Matthew Stephens and Peter Donnelly, Inference of population structure using multilocus genotype data, Genetics 155(2), 2000
    locator: pp. 945-959 (the model without admixture and its Algorithm 1, the admixture model and its Algorithm 2, the priors, and the estimate of Pr(X | K))
  - paper: doi:10.1093/genetics/164.4.1567
    title: Daniel Falush, Matthew Stephens and Jonathan K. Pritchard, Inference of population structure using multilocus genotype data, linked loci and correlated allele frequencies, Genetics 164(4), 2003
    locator: pp. 1567-1587 (the linkage model as a Markov chain along the chromosome, and the F model of correlated frequencies)
  - paper: "David M. Blei, Andrew Y. Ng and Michael I. Jordan, Latent Dirichlet allocation, Journal of Machine Learning Research 3, 2003"
    title: Blei, Ng and Jordan 2003
    locator: pp. 993-1022 (the same generative model for documents and topics)
  - paper: doi:10.1534/genetics.106.065317
    title: John P. Huelsenbeck and Peter Andolfatto, Inference of population structure under a Dirichlet process model, Genetics 175(4), 2007
    locator: pp. 1787-1802 (a prior on the partition of individuals with no fixed K)
---

The Pritchard-Stephens-Donnelly model is the Bayesian model of [population structure](/population-structure-inference/) behind the program STRUCTURE. It assumes $K$ populations, each with its own allele frequencies at each locus and in [Hardy-Weinberg](/hardy-weinberg-principle/) and linkage equilibrium. In the model without admixture, each individual comes from one population. In the admixture model, each individual has a vector of ancestry fractions $q_i$, and each of its gene copies comes from a population drawn from $q_i$. The allele frequencies and the fractions have Dirichlet priors, so all full conditional distributions are Dirichlet or categorical, and the posterior is explored by [Gibbs sampling](/gibbs-sampling/).

## The machine

**Data.** Individuals $i = 1, \ldots, n$, diploid, at loci $l = 1, \ldots, L$. Locus $l$ has $J_l$ alleles. The data are the alleles $x_i^{(l, a)}$ for the two gene copies $a = 1, 2$.

**Parameters.**

- $P$: for each population $k$ and locus $l$, a frequency vector $p_{kl} = (p_{kl1}, \ldots, p_{klJ_l})$ on the simplex.
- $Q$: for each individual, ancestry fractions $q_i = (q_{i1}, \ldots, q_{iK})$ on the simplex (admixture model only).
- $Z$: the population of origin, $z_i$ for the whole individual (no admixture) or $z_i^{(l, a)}$ for each gene copy (admixture).
- $\alpha > 0$: the concentration of the prior on $q_i$.

**Generative process of the admixture model.**

1. For each $k$ and $l$, draw $p_{kl} \sim \text{Dirichlet}(\lambda, \ldots, \lambda)$, with $\lambda = 1$ by default.
2. Draw $\alpha$ from a uniform prior on $(0, 10]$.
3. For each individual, draw $q_i \sim \text{Dirichlet}(\alpha, \ldots, \alpha)$.
4. For each gene copy, draw $z_i^{(l, a)} = k$ with probability $q_{ik}$, then draw $x_i^{(l, a)} = j$ with probability $p_{klj}$, all independently.

**The model without admixture.** Step 3 is replaced by $z_i$ uniform on $\{1, \ldots, K\}$, and every copy of individual $i$ comes from $p_{z_i l}$.

**Standing assumptions.** The populations are in Hardy-Weinberg equilibrium and the loci are in linkage equilibrium within each population, so all copies are independent given $Z$ and $P$. The individuals are unrelated. $K$ is fixed and chosen by the user. Allele frequencies of different populations are independent a priori.

**Gibbs sampler of the admixture model** (Pritchard and coauthors, Algorithm 2). Repeat:

1. Draw $p_{kl} \sim \text{Dirichlet}(\lambda + n_{kl1}, \ldots, \lambda + n_{klJ_l})$, where $n_{klj}$ is the number of copies with $z = k$ and allele $j$ at locus $l$.
2. Draw $q_i \sim \text{Dirichlet}(\alpha + m_{i1}, \ldots, \alpha + m_{iK})$, where $m_{ik}$ is the number of copies of individual $i$ with $z = k$.
3. For each copy, draw $z_i^{(l, a)} = k$ with probability proportional to $q_{ik} \, p_{kl x_i^{(l, a)}}$.
4. Update $\alpha$ with a Metropolis-Hastings step.

Steps 1 and 2 use the conjugacy of the Dirichlet prior with categorical counts. Each sweep costs $O(nLK)$ time.

**A step by hand.** Let $q_i = (0.7, 0.3)$, and let a copy carry an allele with frequency $0.2$ in population 1 and $0.8$ in population 2. Then step 3 gives population 1 with probability $0.7 \cdot 0.2 / (0.7 \cdot 0.2 + 0.3 \cdot 0.8) = 0.14 / 0.38 \approx 0.368$. If, after this step, the individual has $m_i = (30, 10)$ copies from the two populations and $\alpha = 1$, step 2 draws $q_i \sim \text{Dirichlet}(31, 11)$, with mean $(31/42, 11/42) \approx (0.738, 0.262)$.

## What it counts

- **The likelihood.** Given $P$ and $Q$, the probability of the data is $\prod_{i, l, a} \sum_k q_{ik} \, p_{kl x_i^{(l, a)}}$. For biallelic loci this is the likelihood of the admixture model in [population structure inference](/population-structure-inference/), up to the binomial coefficients.
- **The posterior.** The model assigns a posterior distribution to $Q$, $P$ and $Z$. The posterior mean of $q_i$ is the usual estimate of the ancestry of individual $i$. In the model without admixture, the posterior of $z_i$ gives the probability that individual $i$ belongs to each population.
- **The evidence for K.** Pritchard and coauthors estimate $\log \Pr(X \mid K)$ from the chain. With $D = -2 \log \Pr(X \mid P, Q)$ over the sampled states, mean $\hat\mu$ and variance $\hat\sigma^2$, the estimate is $-\hat\mu / 2 - \hat\sigma^2 / 8$, which is exact if $D$ is normal under the posterior. The authors call it an ad hoc guide, not a test.
- **Migrants.** With prior population labels, a variant of the model gives the posterior probability that an individual, a parent or a grandparent is a migrant from another population.

## Relation to other models

- **Maximum likelihood.** ADMIXTURE and FRAPPE maximize the same likelihood over $P$ and $Q$ with no priors. See [maximum likelihood admixture estimation](/maximum-likelihood-admixture-estimation/) and [expectation maximization](/expectation-maximization/).
- **Latent Dirichlet allocation.** The admixture model is the generative model of [latent Dirichlet allocation](/latent-dirichlet-allocation/): an individual is a document, a population is a topic, and an allele at a locus is a word. The two were published independently, in 2000 and 2003.
- **Dirichlet process.** Huelsenbeck and Andolfatto (2007) replaced the fixed $K$ of the model without admixture by a [Dirichlet process](/dirichlet-process/) prior on the partition of individuals, so that the number of populations is inferred.
- **Linkage model.** Falush and coauthors (2003) let $z_i^{(l, a)}$ change along each chromosome as a Markov chain with a switch rate per unit of genetic distance. The model is then a [hidden Markov model](/hidden-markov-model/) along the genome, as in [local ancestry inference](/local-ancestry-inference/).
- **Correlated frequencies.** In the F model of the same paper, $p_{kl} \sim \text{Dirichlet}\big(p_{Al} (1 - F_k) / F_k\big)$ around an ancestral frequency vector $p_{Al}$, where $F_k$ plays the role of the [fixation index](/fixation-index/) of population $k$.
- **Principal components.** [Genetic principal components](/genetic-principal-components/) summarize the same genotype matrix with no model, and often place admixed individuals between the clusters on a line, in agreement with their fractions.

## Known results in the model

- **Conjugate full conditionals.** With Dirichlet priors and categorical data, the conditional of $P$ given $Z$ and of $Q$ given $Z$ are Dirichlet, and the conditional of each $z$ is categorical. So each step of the sampler above draws exactly from a full conditional, and the chain has the posterior as its stationary distribution.
- **Label switching.** The posterior is unchanged by any of the $K!$ relabelings of the populations, so it has at least $K!$ symmetric modes. A chain usually stays near one of them, and results from several runs must be aligned before they are compared.
- **Non-identifiable fractions.** With few loci, many pairs $(Q, P)$ give the same likelihood, and the posterior is wide. More loci shrink it.
- **Limits of the evidence estimate.** The estimate of $\Pr(X \mid K)$ often keeps rising with $K$. Evanno, Regnaut and Goudet (2005) proposed a guide based on the second difference of the estimate across successive values of $K$, divided by its spread over runs.
- **Sensitivity to the design.** Uneven sample sizes across groups, close relatives and continuous spatial variation all change the clusters that the model finds. The model fits discrete groups even when the true structure is a cline.

## References
