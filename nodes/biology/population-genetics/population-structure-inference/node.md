---
tag: GH7ECN
kind: problem
slug: population-structure-inference
name: Population structure inference
aliases:
- genetic clustering of individuals
area: biology/population-genetics
level: core
summary: From genotypes of many individuals, find the ancestral populations and the share of each individual's genome that comes from each.
history:
  year: 2000
  people: [Jonathan K. Pritchard, Matthew Stephens, Peter Donnelly]
  note: "Pritchard, Stephens and Donnelly stated the problem as inference in a model with K unknown populations in Hardy-Weinberg equilibrium, with and without admixture, and solved it by Gibbs sampling in the program STRUCTURE."
prereqs: [allele-frequency, hardy-weinberg-principle, fixation-index]
see_also: [pritchard-stephens-donnelly-model, maximum-likelihood-admixture-estimation, genetic-principal-components, local-ancestry-inference, nonnegative-matrix-factorization, latent-dirichlet-allocation, gaussian-mixture-model, genome-wide-association-study]
sources:
  - paper: doi:10.1093/genetics/155.2.945
    title: Jonathan K. Pritchard, Matthew Stephens and Peter Donnelly, Inference of population structure using multilocus genotype data, Genetics 155(2), 2000
    locator: pp. 945-959 (the model without admixture, the admixture model, the Gibbs sampler and the choice of K)
  - paper: doi:10.1101/gr.094052.109
    title: David H. Alexander, John Novembre and Kenneth Lange, Fast model-based estimation of ancestry in unrelated individuals, Genome Research 19(9), 2009
    locator: pp. 1655-1664 (the likelihood of the admixture model and its maximization by block relaxation)
  - paper: doi:10.1093/genetics/164.4.1567
    title: Daniel Falush, Matthew Stephens and Jonathan K. Pritchard, Inference of population structure using multilocus genotype data, linked loci and correlated allele frequencies, Genetics 164(4), 2003
    locator: pp. 1567-1587 (the linkage model and the model of correlated allele frequencies)
  - paper: doi:10.1534/genetics.114.164350
    title: Anil Raj, Matthew Stephens and Jonathan K. Pritchard, fastSTRUCTURE, variational inference of population structure in large SNP data sets, Genetics 197(2), 2014
    locator: pp. 573-589 (variational Bayes for the admixture model)
---

Population structure inference takes the genotypes of many individuals at many loci and finds a small number $K$ of ancestral populations, each with its own allele frequencies, and for each individual the fraction of its genome that comes from each population. In the model-based form of Pritchard, Stephens and Donnelly (2000), the populations are in [Hardy-Weinberg](/hardy-weinberg-principle/) and linkage equilibrium, and the genotype of an individual at a locus is drawn from a mixture of the population frequencies with weights given by its ancestry. The likelihood is not concave and has many local optima, so the methods in use find a local optimum or a sample from the posterior: by Markov chain Monte Carlo, as in the [Pritchard-Stephens-Donnelly model](/pritchard-stephens-donnelly-model/), or by block relaxation, as in [maximum likelihood admixture estimation](/maximum-likelihood-admixture-estimation/).

## In plain words

You have DNA from many people, and you do not know where their ancestors lived. You guess that there were a few source groups, and that each group had its own mix of gene variants. Each person is then a blend of these groups, and the blend can differ from person to person.

The task is to find the groups and the blend of each person at the same time. You look for the groups and blends that make the observed DNA most likely. A person whose variants match one group well gets most of their ancestry from that group. A person whose variants look like a half-and-half mix gets a half-and-half blend. The answer is a guess that depends on how many groups you ask for, and the search can stop at a good answer that is not the best one.

## Definition

**Input.** Genotypes $g_{ij} \in \{0, 1, 2\}$ for individuals $i = 1, \ldots, n$ and biallelic loci $j = 1, \ldots, m$, counting copies of a chosen allele, and a number $K$ of populations.

**Unknowns.** Allele frequencies $f_{kj} \in [0, 1]$ of the chosen allele in population $k$ at locus $j$, and ancestry fractions $q_{ik} \ge 0$ with $\sum_k q_{ik} = 1$ for each individual.

**Admixture model.** Each of the two gene copies of individual $i$ at locus $j$ comes from population $k$ with probability $q_{ik}$, independently, and then carries the allele with probability $f_{kj}$. So, with $\phi_{ij} = \sum_k q_{ik} f_{kj}$,

$$P(g_{ij} \mid Q, F) = \binom{2}{g_{ij}} \phi_{ij}^{g_{ij}} (1 - \phi_{ij})^{2 - g_{ij}},$$

and loci and individuals are independent given $Q$ and $F$.

**Model without admixture.** Each individual belongs to one population $z_i$, so $q_i$ is a unit vector.

**The problem.** Find $Q$ and $F$ that maximize the log-likelihood

$$\ell(Q, F) = \sum_{i, j} \big[ g_{ij} \log \phi_{ij} + (2 - g_{ij}) \log(1 - \phi_{ij}) \big],$$

or, in the Bayesian form, describe the posterior of $Q$ and $F$ under priors on both. The answer is defined only up to a relabeling of the $K$ populations.

## Variants

- **Without and with admixture.** The model without admixture is a mixture model with $K$ components, close to a [Gaussian mixture model](/gaussian-mixture-model/) with product-binomial components. The admixture model lets each individual have its own weights.
- **Linked loci.** Falush, Stephens and Pritchard (2003) let the population of origin change along a chromosome as a Markov chain, which joins this problem to [local ancestry inference](/local-ancestry-inference/).
- **Correlated frequencies.** The same paper lets the population frequencies come from a common ancestral frequency with drift, so that close populations can be split.
- **Choosing K.** $K$ is not part of the data. Pritchard and coauthors compare an approximate marginal likelihood over $K$. ADMIXTURE uses [cross-validation](/cross-validation/) on held-out genotypes. No choice of $K$ is right in a strict sense when the true history is continuous in space or time.
- **Without a model.** [Genetic principal components](/genetic-principal-components/) summarize the same data by the top eigenvectors of a genotype covariance matrix, with no populations or fractions.
- **Supervised.** When some individuals are known to come from given populations, their $q_i$ are fixed, and only the others are estimated.

## Examples

Take two loci and $K = 2$, with known frequencies $f_1 = (0.9, 0.1)$ and $f_2 = (0.1, 0.9)$ of the chosen allele.

- **An individual with genotypes (2, 0).** Under population 1 alone, the probability is $0.9^2 \cdot 0.9^2 = 0.6561$; under population 2 alone, $0.1^2 \cdot 0.1^2 = 0.0001$. With equal prior weights, the posterior probability of population 1 in the model without admixture is $0.6561 / 0.6562 \approx 0.99985$.
- **An individual with genotypes (1, 1).** Under either population alone the probability is $(2 \cdot 0.9 \cdot 0.1)^2 = 0.0324$. In the admixture model with $q = (0.5, 0.5)$, $\phi = 0.5$ at both loci, and the probability is $0.5 \cdot 0.5 = 0.25$. Here $\phi_2 = 1 - \phi_1$, so the likelihood is $4 [\phi_1 (1 - \phi_1)]^2$, which is largest at $\phi_1 = 0.5$, that is, at $q = (0.5, 0.5)$. The data fit a half-and-half individual much better than either pure population.
- **A non-identifiable case.** With one locus and $K = 2$, any $(Q, F)$ with the same values $\phi_i$ gives the same likelihood, so many different pairs of frequencies explain the data equally well. Many loci are needed to pin the populations down.

## Known algorithms

- **Gibbs sampling.** STRUCTURE samples the population of origin of each gene copy, the frequencies and the fractions in turn, under Dirichlet priors. See [Pritchard-Stephens-Donnelly model](/pritchard-stephens-donnelly-model/) and [Gibbs sampling](/gibbs-sampling/).
- **Block relaxation.** ADMIXTURE maximizes $\ell$ over $F$ with $Q$ fixed and over $Q$ with $F$ fixed in turn, with a quasi-Newton acceleration. See [maximum likelihood admixture estimation](/maximum-likelihood-admixture-estimation/).
- **Expectation maximization.** FRAPPE maximizes the same likelihood with [EM](/expectation-maximization/), treating the population of origin of each gene copy as missing data.
- **Variational Bayes.** fastSTRUCTURE (Raj, Stephens and Pritchard 2014) fits a factorized approximation of the posterior, which is much faster than sampling on large SNP data. See [variational inference](/variational-inference/).
- **Matrix factorization.** Since $E[g_{ij}] / 2 = \phi_{ij} = (Q F)_{ij}$, methods such as sNMF fit $Q$ and $F$ as a constrained [nonnegative matrix factorization](/nonnegative-matrix-factorization/) of the genotype matrix.
- **Principal components.** [Genetic principal components](/genetic-principal-components/) need no model and give a fast summary, often used before or beside the model-based methods.

All model-based methods reach a local optimum or a local mode. Users run them from several starts and compare the results.

## Bounds

- **No guarantee of the global optimum.** The log-likelihood is concave in $Q$ for fixed $F$ and in $F$ for fixed $Q$, but not jointly, and it has at least $K!$ equal optima from the relabelings. No polynomial-time algorithm is known that finds the global maximum.
- **Hardness of the related factorization.** Exact nonnegative matrix factorization, a close relative, is NP-hard in general (Vavasis 2009). This does not prove that the likelihood problem above is hard, but it shows that the matrix form gives no easy route.
- **Cost per iteration.** One Gibbs sweep, one EM step or one round of block relaxation costs $O(nmK)$ time, so the methods scale to hundreds of thousands of individuals and loci.
- **Data needed.** With $F_{ST}$ between populations small, many loci are needed to separate them. Patterson, Price and Reich (2006) give a threshold, of order $1/\sqrt{nm}$ for $F_{ST}$, below which the data show no structure in the eigenvalues; see [genetic principal components](/genetic-principal-components/).

## Reductions

- **To a topic model.** The admixture model is the same model as [latent Dirichlet allocation](/latent-dirichlet-allocation/), with individuals as documents, populations as topics and loci with alleles as words. Pritchard and coauthors published it in 2000, before LDA in 2003.
- **To matrix factorization.** The expected genotype matrix divided by 2 equals $Q F$ with $Q$ row-stochastic and $F$ in $[0, 1]$, so the problem is a constrained factorization with a binomial loss.
- **To principal components.** McVean (2009) showed that the principal components of genotype data reflect the mean coalescence times between pairs of samples, which ties the model-free summary to the genealogy.
- **To local ancestry.** When the loci are dense and linked, the per-locus population of origin forms a hidden Markov chain along each chromosome, and the problem becomes [local ancestry inference](/local-ancestry-inference/).

## Applications

- **Human history.** Ancestry fractions of individuals from many populations describe migration and admixture, for example in African, European and Native American samples.
- **Association studies.** Ancestry fractions or principal components enter a [genome-wide association study](/genome-wide-association-study/) as covariates, to correct for confounding by structure.
- **Conservation and ecology.** Clustering of animals or plants finds breeding units, hybrids and migrants.
- **Breeding.** Crop and livestock programs use the fractions to describe the ancestry of lines and to choose crosses.

## References
