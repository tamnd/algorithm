---
tag: 6MKE3F
kind: model
slug: kimura-two-parameter-model
name: Kimura two-parameter model
aliases:
- K2P
- K80
area: biology/phylogenetics
level: core
summary: A DNA substitution model with one rate for transitions (A to G, C to T) and a lower rate for transversions, equal base frequencies, and the ratio kappa as its only free parameter.
history:
  year: 1980
  people: [Motoo Kimura]
  note: Kimura gave the model and the distance formula that corrects separately for transitions and transversions, to estimate rates of evolution from compared sequences.
prereqs: [jukes-cantor-model]
see_also: [substitution-model, felsenstein-81-model, hky-model, gtr-model, rate-heterogeneity, phylogenetic-likelihood, neighbor-joining, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1007/BF01731581
    title: Motoo Kimura, A simple method for estimating evolutionary rates of base substitutions through comparative studies of nucleotide sequences, Journal of Molecular Evolution 16 (1980)
    locator: pp. 111 to 120 (the two-rate model, the transition probabilities and the distance with its variance)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Section 1.2 (the K80 model, its transition probabilities and the K80 distance)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 13, Models of DNA evolution
---

The Kimura two-parameter model, K80 or K2P, is a [substitution model](/substitution-model/) for DNA that separates two kinds of change. A *transition* is a change inside a chemical class: between the purines A and G, or between the pyrimidines C and T. A *transversion* is a change between a purine and a pyrimidine. In real DNA, transitions are more frequent, often by a large factor. K80 gives each transition the rate $\alpha$ and each transversion the rate $\beta$, and it keeps the equal base frequencies of [JC69](/jukes-cantor-model/). After the scaling of the rate, the only free parameter is the ratio $\kappa = \alpha / \beta$. Kimura's distance formula $d = -\tfrac12 \ln(1 - 2P - Q) - \tfrac14 \ln(1 - 2Q)$ corrects for multiple changes using the proportions $P$ of transition differences and $Q$ of transversion differences.

## The machine

**States and rates.** With the bases in the order A, C, G, T, each base has one transition partner (A with G, C with T) and two transversion partners. The rate matrix is

$$Q = \begin{pmatrix} -(\alpha + 2\beta) & \beta & \alpha & \beta \\ \beta & -(\alpha + 2\beta) & \beta & \alpha \\ \alpha & \beta & -(\alpha + 2\beta) & \beta \\ \beta & \alpha & \beta & -(\alpha + 2\beta) \end{pmatrix}.$$

The matrix is symmetric, so the stationary distribution is uniform and the chain is reversible. The rate of substitution per site is $\alpha + 2\beta$. Programs scale it to $\alpha + 2\beta = 1$, so that a branch length $t$ is in expected substitutions per site; then $\beta = 1/(\kappa + 2)$ and $\alpha = \kappa/(\kappa + 2)$.

**Transition probabilities.** The eigenvalues of $Q$ are $0$, $-4\beta$ and $-2(\alpha + \beta)$ (twice). For a base $i$, let $P_0$ be the probability of no visible change, $P_1$ the probability of the transition, and $P_2$ the probability of each of the two transversions. Then

$$P_0(t) = \frac14 + \frac14 e^{-4\beta t} + \frac12 e^{-2(\alpha + \beta) t},$$

$$P_1(t) = \frac14 + \frac14 e^{-4\beta t} - \frac12 e^{-2(\alpha + \beta) t},$$

$$P_2(t) = \frac14 - \frac14 e^{-4\beta t}.$$

These sum to 1 as $P_0 + P_1 + 2 P_2$. One way to see them: whether the base is a purine or a pyrimidine is itself a two-state chain with rate $2\beta$ in each direction, which explains the term $e^{-4\beta t}$; given the class, the base inside it follows a second chain, which gives the term with $e^{-2(\alpha + \beta) t}$.

**On a tree.** As with every model here, the root base is drawn from the uniform distribution, each edge applies $P(t_e)$ independently, and sites are independent.

## What it counts

**Two kinds of difference.** Two aligned sequences of $m$ sites have a proportion $\hat P$ of sites that differ by a transition and a proportion $\hat Q$ that differ by a transversion. If they are at distance $d$ (the sum of the branch lengths between them), then the expected values are $P = P_1(d)$ and $Q = 2 P_2(d)$. So

$$1 - 2Q = e^{-4\beta d}, \qquad 1 - 2P - Q = e^{-2(\alpha + \beta) d}.$$

**The K80 distance.** Take logarithms and add, using $\alpha + 2\beta = 1$:

$$\hat d = -\frac12 \ln\left(1 - 2\hat P - \hat Q\right) - \frac14 \ln\left(1 - 2\hat Q\right).$$

The same two equations give the estimate of the ratio,

$$\hat \kappa = \frac{2 \ln(1 - 2\hat P - \hat Q)}{\ln(1 - 2\hat Q)} - 1.$$

These are the maximum likelihood estimates from the two counts. Kimura wrote the distance as $K = 2(\alpha + 2\beta) T$ for two sequences that split a time $T$ ago, which is the same quantity. The formula is defined only when $1 - 2\hat P - \hat Q > 0$ and $1 - 2\hat Q > 0$.

## Relation to other models

- **JC69 is the case $\kappa = 1$.** With $\alpha = \beta$, all three changes have the same rate, and $P_0$, $P_1$ and $P_2$ reduce to the [JC69](/jukes-cantor-model/) formulas. The K80 distance with $\hat P = \hat Q / 2$ is the JC69 distance.
- **HKY85 adds base frequencies.** [HKY85](/hky-model/) keeps the transition and transversion classes and lets the four frequencies differ. K80 is HKY85 with $\pi = (\tfrac14, \tfrac14, \tfrac14, \tfrac14)$. [F81](/felsenstein-81-model/) is the other branch from JC69, with unequal frequencies but $\kappa = 1$.
- **Kimura's three-parameter model.** Kimura in 1981 split the transversions into two classes (A with C and G with T, against A with T and C with G), each with its own rate. K80 is the case where the two classes have the same rate. Both models are group-based, like JC69.
- **[GTR](/gtr-model/)** contains K80 as the case of equal frequencies, $r_{AG} = r_{CT} = \kappa$ and the other four exchangeabilities equal to 1. So the nesting JC69 $\subset$ K80 $\subset$ HKY85 $\subset$ GTR holds, and a likelihood ratio test of K80 against HKY85 has three degrees of freedom.

## Known results in the model

**The row of $P(t)$.** For $\kappa = 2$ the scaled rates are $\alpha = 0.5$ and $\beta = 0.25$, and the eigenvalues are $0, -1, -1.5, -1.5$. At $t = 0.1$, the row of A in $P(t)$ is $(0.906563, 0.023791, 0.045855, 0.023791)$, in the order A, C, G, T.

**Distances.** The table compares the K80 distance with the JC69 distance computed from the total proportion $\hat p = \hat P + \hat Q$.

| $\hat P$ | $\hat Q$ | K80 $\hat d$ | $\hat \kappa$ | JC69 $\hat d$ |
|---|---|---|---|---|
| 0.05 | 0.02 | 0.074122 | 5.263 | 0.073485 |
| 0.15 | 0.05 | 0.241732 | 7.177 | 0.232616 |
| 0.20 | 0.10 | 0.402359 | 5.213 | 0.383119 |
| 0.30 | 0.15 | 0.782316 | 6.773 | 0.687218 |

For close sequences the two distances agree. For distant ones, JC69 is too small, because it assumes that two thirds of all changes are transversions and so it underestimates how many hidden transitions there are.

**The bias of JC69 under K80 data.** At a true distance $d = 0.3$, the expected proportions and the JC69 estimate are:

| $\kappa$ | $P$ | $Q$ | JC69 $\hat d$ |
|---|---|---|---|
| 1 | 0.082420 | 0.164840 | 0.300000 |
| 2 | 0.116390 | 0.129591 | 0.298095 |
| 5 | 0.161651 | 0.078770 | 0.289866 |
| 10 | 0.187734 | 0.047581 | 0.282390 |

The K80 formula returns $0.3$ in each row. The bias of JC69 grows with $\kappa$ and with $d$.

**Likelihood.** On a tree, the [phylogenetic likelihood](/phylogenetic-likelihood/) under K80 uses the closed-form matrices above in [Felsenstein's pruning algorithm](/felsenstein-pruning/), and $\kappa$ is estimated together with the branch lengths.

## References
