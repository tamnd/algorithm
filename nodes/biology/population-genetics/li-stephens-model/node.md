---
tag: QN36N8
kind: model
slug: li-stephens-model
name: Li-Stephens haplotype copying model
aliases:
- Li and Stephens model
- product of approximate conditionals
area: biology/population-genetics
level: advanced
summary: An HMM that builds a new haplotype as a mosaic of known ones, with switches for recombination and errors for mutation.
history:
  year: 2003
  people: [Na Li, Matthew Stephens]
  note: "Li and Stephens proposed the copying model in 2003 as an approximation to the conditional distribution of a new haplotype under the coalescent with recombination, and used it to estimate recombination rates from samples of haplotypes."
prereqs: [hidden-markov-model, linkage-disequilibrium, kingman-coalescent]
see_also: [forward-backward-algorithm, forward-algorithm, viterbi-algorithm, ancestral-recombination-graph, haplotype-phasing, genotype-imputation, local-ancestry-inference, positional-burrows-wheeler-transform]
sources:
  - paper: doi:10.1093/genetics/165.4.2213
    title: Na Li and Matthew Stephens, Modeling linkage disequilibrium and identifying recombination hotspots using single-nucleotide polymorphism data, Genetics 165(4), 2003
    locator: pp. 2213-2233 (the copying model, its transition and emission probabilities, the choice of theta, the likelihood of a sample as a product of conditionals, and the estimates of recombination rates)
  - paper: doi:10.1086/319501
    title: Matthew Stephens, Nicholas J. Smith and Peter Donnelly, A new statistical method for haplotype reconstruction from population data, American Journal of Human Genetics 68(4), 2001
    locator: pp. 978-989 (the conditional distribution of a new haplotype given the others, without recombination, used in PHASE)
  - paper: doi:10.1093/bioinformatics/btu014
    title: Richard Durbin, Efficient haplotype matching and storage using the positional Burrows-Wheeler transform (PBWT), Bioinformatics 30(9), 2014
    locator: pp. 1266-1272 (fast matching of a new haplotype to a panel, used to choose copying states)
---

The Li-Stephens model gives a probability to a new haplotype $h$ given $K$ known haplotypes from the same population. It builds $h$ as a mosaic: along the sequence, $h$ copies one of the known haplotypes, switches to another at a rate set by the recombination rate, and at each site differs from the copied allele with a small probability set by the mutation rate. This is a [hidden Markov model](/hidden-markov-model/) whose hidden state is the haplotype being copied. Li and Stephens (2003) proposed it as a simple approximation to the conditional distribution of a new haplotype under the coalescent with recombination, which has no closed form. Its forward and backward passes cost $O(mK)$ time for $m$ sites, and it is the core of most methods for [haplotype phasing](/haplotype-phasing/), [genotype imputation](/genotype-imputation/) and [local ancestry inference](/local-ancestry-inference/).

## The machine

**Data.** Known haplotypes $h_1, \ldots, h_K$ and a new haplotype $h$, over $m$ biallelic sites in order along a chromosome. $\rho_j \ge 0$ is the scaled recombination rate $4 N_e r$ between sites $j$ and $j + 1$, times their distance, where $N_e$ is the effective population size and $r$ the recombination rate per generation per unit distance.

**Hidden state.** $X_j \in \{1, \ldots, K\}$ is the known haplotype that $h$ copies at site $j$.

**Start.** $X_1$ is uniform on $\{1, \ldots, K\}$.

**Transitions.** With $s_j = 1 - e^{-\rho_j / K}$,
$$P(X_{j+1} = y \mid X_j = x) = (1 - s_j)\,[x = y] + \frac{s_j}{K}.$$
So the chain keeps the same haplotype with probability $e^{-\rho_j / K} + (1 - e^{-\rho_j / K})/K$, and moves to each other one with probability $(1 - e^{-\rho_j / K})/K$. In words, a recombination event happens with probability $s_j$, and then the next haplotype to copy is uniform, which may be the same one.

**Emissions.** With a mutation parameter $\tilde\theta > 0$,
$$P(h_j = h_{X_j, j}) = \frac{K + \tilde\theta / 2}{K + \tilde\theta}, \qquad P(h_j \ne h_{X_j, j}) = \frac{\tilde\theta / 2}{K + \tilde\theta}.$$
Li and Stephens set $\tilde\theta = \big(\sum_{i=1}^{K-1} 1/i\big)^{-1}$, from Watterson's estimator of $\theta$ per site.

**Standing assumptions.** The known haplotypes are fixed and phased. Sites are biallelic. Switches and mismatches at different places are independent given the path. The model has no notion of the tree that relates the known haplotypes to each other.

**The forward algorithm.** The transition is a mix of "stay" and "jump to a uniform state", so the sum over the previous state takes $O(1)$ per state once the total is known. With $e_j(x) = P(h_j \mid X_j = x)$ and forward vectors scaled to sum to 1:

```pseudo id=main
LS-FORWARD(h_1..h_K, h, rho, theta)
L1  alpha(x) ← e_1(x) / K for each x
L2  c_1 ← sum of alpha; divide alpha by c_1
L3  for j = 2 to m do
L4      s ← 1 - exp(-rho_{j-1} / K); jump ← s / K
L5      alpha(x) ← ((1 - s) alpha(x) + jump) e_j(x) for each x     ▷ uses sum of alpha = 1
L6      c_j ← sum of alpha
L7      divide alpha by c_j
L8  return log P(h | h_1..h_K) = sum of log c_j
```

The same structure gives the backward pass, the posterior copying probabilities and the most likely path in $O(mK)$ time each.

**A step by hand.** Take $h_1 = 001$, $h_2 = 111$, $h = 011$, $K = 2$, $\tilde\theta = 1$, and $\rho_1 = \rho_2 = 2 \ln 2$, so $s = 1/2$. A match has probability $5/6$ and a mismatch $1/6$; the chain stays with probability $3/4$ and switches with probability $1/4$. Without scaling, the forward values are $(5/12, 1/12)$ at site 1 and $\big((5/12 \cdot 3/4 + 1/12 \cdot 1/4) \cdot 1/6,\ (5/12 \cdot 1/4 + 1/12 \cdot 3/4) \cdot 5/6\big) = (1/18, 5/36)$ at site 2. Both haplotypes carry 1 at site 3, so $P(h) = (1/18 + 5/36) \cdot 5/6 = 35/216 \approx 0.162$. The posterior probability that $h$ copies $h_2$ at site 2 is $5/7$.

## What it counts

- **The conditional probability.** $\hat\pi(h \mid h_1, \ldots, h_K)$, the probability of the new haplotype given the known ones, is the output of the forward algorithm.
- **A likelihood for a sample.** For a sample $h_1, \ldots, h_n$, Li and Stephens multiply a probability for $h_1$ by the conditionals $\hat\pi(h_k \mid h_1, \ldots, h_{k-1})$ for $k = 2, \ldots, n$. This is not a true joint probability: it depends on the order of the haplotypes, and they average it over several random orders. As a function of the $\rho_j$, it gives estimates of recombination rates and of hotspots.
- **The copying path.** The posterior of $X_j$ tells which known haplotype is closest to $h$ near site $j$. Summed by population, this gives the local ancestry of $h$, and summed by donor it gives the "painting" of a genome by donors.
- **Missing alleles.** For a site where $h$ is missing, the posterior predictive allele is $\sum_x P(X_j = x \mid h)\, P(\text{allele} \mid X_j = x)$, which is the basis of imputation.

## Relation to other models

- **Coalescent with recombination.** The true conditional distribution of a new haplotype comes from the [ancestral recombination graph](/ancestral-recombination-graph/), and has no closed form. The copying model keeps the main features: the new haplotype tends to look like an existing one, more so when $K$ is large, and less so when $\theta$ is large. Recombination makes the closest haplotype change along the sequence. The rate of change falls like $\rho / K$, because with more known haplotypes the new lineage joins their tree sooner, so recombination has less time to act.
- **The model without recombination.** With all $\rho_j = 0$, the path never switches, and the model is a mixture over which known haplotype is copied, close to the conditional of Stephens, Smith and Donnelly (2001) used in PHASE.
- **Hidden Markov models.** It is an HMM with $K$ states and a transition matrix of rank-one-plus-identity form, so the [forward algorithm](/forward-algorithm/), the [forward-backward algorithm](/forward-backward-algorithm/) and the [Viterbi algorithm](/viterbi-algorithm/) all run in $O(mK)$ instead of $O(mK^2)$.
- **Admixture HMMs.** The linkage model of Falush and coauthors and HAPMIX switch among a few ancestral populations instead of among haplotypes, or among haplotypes grouped by population. See [local ancestry inference](/local-ancestry-inference/).
- **Matching structures.** The [positional Burrows-Wheeler transform](/positional-burrows-wheeler-transform/) finds the known haplotypes with the longest exact matches to $h$, which methods use to keep only a few states per region.

## Known results in the model

- **Linear time.** One forward pass, one backward pass, the posterior and the most likely path each take $O(mK)$ time, as shown in the proof for this page. A sample of $n$ haplotypes, each conditioned on the others, takes $O(mn^2)$ time.
- **The limits of $\rho$.** With all $\rho_j = 0$, $P(h) = \frac{1}{K} \sum_x \prod_j e_j(x)$. As all $\rho_j \to \infty$, the sites are independent and $P(h) = \prod_j \frac{1}{K} \sum_x e_j(x)$.
- **Bias of the rate estimates.** Li and Stephens found that the recombination rates estimated from the product of conditionals are biased, and gave a modified conditional that reduces the bias in simulations.
- **Hotspots.** Applied to SNP data in human genes, the model detected local peaks of recombination rate that match hotspots found by sperm typing.
- **Phasing and imputation.** Methods such as PHASE, IMPUTE, SHAPEIT, Beagle and Eagle use this model, or a close variant, as the conditional distribution of a haplotype given a reference panel or the other haplotypes in the sample. For large panels they restrict the states to a few haplotypes chosen by matching.

## References
