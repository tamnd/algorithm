---
tag: Q16CFN
kind: model
slug: felsenstein-81-model
name: Felsenstein 1981 model
aliases:
- F81
- equal-input model
area: biology/phylogenetics
level: core
summary: JC69 with unequal base frequencies. Each change to base j has rate mu pi_j, so P(t) mixes the start base with a fresh draw from pi, and P_ij(t) has a closed form.
history:
  year: 1981
  people: [Joseph Felsenstein]
  note: Felsenstein used this model in the paper that brought maximum likelihood and the pruning algorithm to trees built from DNA sequences.
prereqs: [jukes-cantor-model]
see_also: [substitution-model, kimura-two-parameter-model, hky-model, gtr-model, phylogenetic-likelihood, felsenstein-pruning, maximum-likelihood-phylogeny, stationary-distribution]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17 (1981)
    locator: pp. 368 to 376 (the model with rates proportional to the base frequencies, its transition probabilities, and the pruning computation of the likelihood)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Section 1.2 (the F81 model among the models with unequal base frequencies)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 13, Models of DNA evolution
---

The Felsenstein 1981 model, F81, is the [JC69 model](/jukes-cantor-model/) with unequal base frequencies. The rate of change from base $i$ to base $j \ne i$ is $\mu \pi_j$: it depends only on the target base, through its stationary frequency $\pi_j$. The model has a simple picture. Events happen at rate $\mu$, and at each event the site draws a new base from $\pi$, which may be the same base as before. So after a time $t$ the site either has seen no event and keeps its base, or it is a fresh draw from $\pi$. Felsenstein used this model in his 1981 paper on maximum likelihood trees from DNA, the same paper that gave the [pruning algorithm](/felsenstein-pruning/).

## The machine

**States and rates.** The states are A, C, G and T, with frequencies $\pi = (\pi_A, \pi_C, \pi_G, \pi_T)$, all positive and summing to 1. The [rate matrix](/substitution-model/) has

$$Q_{ij} = \mu \pi_j \quad (i \ne j), \qquad Q_{ii} = -\mu (1 - \pi_i).$$

In matrix form, $Q = \mu (\mathbf{1} \pi - I)$, where $\mathbf{1} \pi$ is the matrix whose rows all equal $\pi$.

**Stationary and reversible.** Each column $j$ of $\pi Q$ is $\mu \pi_j \sum_{i \ne j} \pi_i - \mu \pi_j (1 - \pi_j) = 0$, so $\pi$ is stationary. Detailed balance holds because $\pi_i Q_{ij} = \mu \pi_i \pi_j = \pi_j Q_{ji}$.

**Scaling.** The expected substitution rate at stationarity is $\sum_i \pi_i \mu (1 - \pi_i) = \mu B$, with

$$B = 1 - \sum_i \pi_i^2.$$

Programs set $\mu = 1/B$, so that the branch length $t$ is in expected substitutions per site.

**Transition probabilities.** The matrix $E = \mathbf{1} \pi$ satisfies $E^2 = E$, because each row of $E$ times $\mathbf 1$ is 1. So $e^{\mu t E} = I + (e^{\mu t} - 1) E$, and with $Q = \mu (E - I)$,

$$P(t) = e^{-\mu t} I + \left(1 - e^{-\mu t}\right) \mathbf{1} \pi, \qquad P_{ij}(t) = e^{-\mu t} \delta_{ij} + \left(1 - e^{-\mu t}\right) \pi_j.$$

This is the event picture in a formula: $e^{-\mu t}$ is the probability of no event, and after at least one event the base is a draw from $\pi$. The eigenvalues of $Q$ are $0$ and $-\mu$ (three times).

## What it counts

**Expected differences.** For two sequences at distance $d$ under the scaled model, the probability that a site differs is

$$p(d) = \sum_i \pi_i \left(1 - P_{ii}(d)\right) = \sum_i \pi_i (1 - \pi_i) \left(1 - e^{-d/B}\right) = B \left(1 - e^{-d/B}\right).$$

**The F81 distance.** Inverting $p(d)$ at the observed proportion $\hat p$ gives

$$\hat d = -B \ln\left(1 - \frac{\hat p}{B}\right),$$

with $B$ computed from the base frequencies, usually the observed frequencies in the two sequences. The upper limit of $\hat p$ is $B$, the probability that two independent draws from $\pi$ differ. With $\pi$ uniform, $B = 3/4$ and the formula is the JC69 distance.

**Cheap likelihood steps.** A vector $v$ multiplied by $P(t)$ needs only one dot product: $(P(t) v)_i = e^{-\mu t} v_i + (1 - e^{-\mu t}) \sum_j \pi_j v_j$. So one step of [pruning](/felsenstein-pruning/) costs $O(k)$ per node and site instead of $O(k^2)$ for a general model on $k$ states.

## Relation to other models

- **JC69 is the case of equal frequencies.** With $\pi_j = 1/4$, $B = 3/4$, $\mu = 4/3$, and $Q_{ij} = 1/3$, which is [JC69](/jukes-cantor-model/).
- **HKY85 adds the transition and transversion rates.** [HKY85](/hky-model/) multiplies the rates of transitions by $\kappa$. F81 is HKY85 with $\kappa = 1$, and [K80](/kimura-two-parameter-model/) is HKY85 with equal frequencies. So the nesting is JC69 $\subset$ F81 $\subset$ HKY85, next to JC69 $\subset$ K80 $\subset$ HKY85.
- **[GTR](/gtr-model/)** with all six exchangeabilities equal is F81. Every GTR matrix has the form $Q_{ij} = r_{ij} \pi_j$, and F81 is the case $r_{ij} = \mu$.
- **Other alphabets.** The same form on 20 amino acids is the equal-input model of protein evolution, and on two states it is the binary model with unequal frequencies.

## Known results in the model

**A worked matrix.** Take $\pi = (0.1, 0.2, 0.3, 0.4)$ in the order A, C, G, T. Then $B = 1 - (0.01 + 0.04 + 0.09 + 0.16) = 0.7$ and $\mu = 1/0.7$. The rate matrix is

| | A | C | G | T |
|---|---|---|---|---|
| A | $-1.285714$ | $0.285714$ | $0.428571$ | $0.571429$ |
| C | $0.142857$ | $-1.142857$ | $0.428571$ | $0.571429$ |
| G | $0.142857$ | $0.285714$ | $-1$ | $0.571429$ |
| T | $0.142857$ | $0.285714$ | $0.428571$ | $-0.857143$ |

The eigenvalues are $0$ and $-1/0.7 = -1.428571$ (three times). At $t = 0.2$, $e^{-0.2/0.7} = 0.751477$, and

| | A | C | G | T |
|---|---|---|---|---|
| A | $0.776330$ | $0.049705$ | $0.074557$ | $0.099409$ |
| C | $0.024852$ | $0.801182$ | $0.074557$ | $0.099409$ |
| G | $0.024852$ | $0.049705$ | $0.826034$ | $0.099409$ |
| T | $0.024852$ | $0.049705$ | $0.074557$ | $0.850886$ |

Each column off the diagonal is constant, as the formula says. Rare bases change more often: A keeps its base with probability $0.776$ and T with $0.851$.

**Distance.** With these frequencies, the expected proportion of differences at $d = 0.2$ is $0.7 (1 - 0.751477) = 0.173966$. For an observed $\hat p = 0.2$, the F81 distance is $-0.7 \ln(1 - 0.2/0.7) = 0.235531$, against $0.232616$ for JC69. The F81 value is larger because with skewed frequencies more of the changes return to the same common bases and stay hidden.

**Likelihood.** Felsenstein's 1981 paper computes the [phylogenetic likelihood](/phylogenetic-likelihood/) under this model by pruning, searches for the best tree by adding taxa one at a time and moving branches, and fits the branch lengths by an iterative method. It is the start of [maximum likelihood phylogeny](/maximum-likelihood-phylogeny/) for DNA.

## References
