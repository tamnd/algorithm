---
tag: 9BNWF3
kind: concept
slug: substitution-model
name: Substitution model
aliases:
- nucleotide substitution model
- evolutionary model
area: biology/phylogenetics
level: intro
summary: A continuous-time Markov chain on the states of one site (A, C, G, T for DNA), given by a rate matrix Q, with P(t) = exp(Qt) the change probabilities along a branch of length t.
prereqs: [markov-chain, stationary-distribution, detailed-balance]
see_also: [jukes-cantor-model, gtr-model, rate-heterogeneity, phylogenetic-likelihood, felsenstein-pruning, transition-matrix, pam-matrix, spectral-theorem]
sources:
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 13, Models of DNA evolution
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Models of nucleotide substitution (the rate matrix, P(t) = exp(Qt), the stationary distribution, time reversibility and the spectral form)
  - paper: "Simon Tavaré, Some probabilistic and statistical problems in the analysis of DNA sequences, in R. M. Miura (ed.), Some Mathematical Questions in Biology, DNA Sequence Analysis, Lectures on Mathematics in the Life Sciences 17, American Mathematical Society, 1986, pages 57 to 86"
    locator: the continuous-time Markov chain on the four bases and the reversible form of the rate matrix
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 8, Probabilistic approaches to phylogeny
---

A substitution model is a [continuous-time Markov chain](/markov-chain/) on the states of one site of a sequence: the four bases A, C, G and T for DNA, the 20 amino acids for proteins, or 0 and 1 for a binary character. A rate matrix $Q$ gives the instant rate of each change, and the matrix $P(t) = e^{Qt}$ gives the probability that a site in state $i$ is in state $j$ after a time $t$. Every likelihood and Bayesian method of phylogenetics puts one copy of this chain on each branch of a tree, and the [phylogenetic likelihood](/phylogenetic-likelihood/) is built from the matrices $P(t)$. Named models such as [JC69](/jukes-cantor-model/), [K80](/kimura-two-parameter-model/), [F81](/felsenstein-81-model/), [HKY85](/hky-model/) and [GTR](/gtr-model/) differ only in the constraints that they put on $Q$.

## In plain words

Think of one position in a gene, copied from parent to child over a very long time. Most copies are exact, but now and then the letter at that position changes into another letter. A substitution model is a set of rules for how often each change happens: how often an A becomes a G, how often a C becomes a T, and so on.

From these rates you can compute what you see at the end of a branch of the tree. After a short branch, the letter is most likely the same as at the start. After a very long branch, the start is forgotten, and the letter has a fixed chance to be each base. Simple models use one rate for all changes. Richer models let some changes be faster than others, and let some letters be more common than others.

## The idea

**The states and the rates.** Fix an alphabet of $k$ states ($k = 4$ for DNA, $k = 20$ for amino acids). A rate matrix is a $k \times k$ matrix $Q$ with $Q_{ij} \ge 0$ for $i \ne j$ and with each row summing to zero, so $Q_{ii} = -\sum_{j \ne i} Q_{ij}$. In a short time $h$, a site in state $i$ changes to $j \ne i$ with probability $Q_{ij} h + o(h)$. The time a site stays in state $i$ is exponential with rate $-Q_{ii}$.

**The probabilities along a branch.** The matrix of transition probabilities after a time $t \ge 0$ is the matrix exponential

$$P(t) = e^{Qt} = \sum_{n \ge 0} \frac{(Qt)^n}{n!}.$$

It solves $P'(t) = P(t)\,Q$ with $P(0) = I$, it is a stochastic matrix (entries in $[0, 1]$ and rows that sum to 1) for each $t \ge 0$, and it obeys the Chapman-Kolmogorov equation $P(s + t) = P(s)\,P(t)$. So the change along a path of two branches is the product of the two matrices. The [transition matrix](/transition-matrix/) of a discrete-time chain is the special case $P(1)$.

**The stationary distribution.** A distribution $\pi$ with $\pi Q = 0$ satisfies $\pi P(t) = \pi$ for all $t$, because $\pi Q^n = 0$ for each $n \ge 1$. If every state can reach every other state through positive rates, $\pi$ is unique and positive, and each row of $P(t)$ tends to $\pi$ as $t \to \infty$. Phylogenetic models usually assume that the root is drawn from $\pi$ and that the same $Q$ holds on every branch (a *stationary* and *homogeneous* model). Then each node of the tree has the [stationary distribution](/stationary-distribution/) $\pi$, and $\pi_j$ is the expected frequency of base $j$.

**Time reversibility.** The model is reversible when it satisfies [detailed balance](/detailed-balance/):

$$\pi_i Q_{ij} = \pi_j Q_{ji} \quad \text{for all } i, j.$$

Write $\Pi = \mathrm{diag}(\pi)$. Detailed balance says $\Pi Q = Q^{\mathsf T} \Pi$. By induction, $\Pi Q^n = Q^{\mathsf T} \Pi Q^{n-1} = (Q^{\mathsf T})^n \Pi$, so $\Pi P(t) = P(t)^{\mathsf T} \Pi$, that is, $\pi_i P_{ij}(t) = \pi_j P_{ji}(t)$. A pair of sequences at the two ends of a branch then has the same joint distribution in both directions, and the likelihood of a tree does not depend on where the root is (the pulley principle on the [phylogenetic likelihood](/phylogenetic-likelihood/) page). Each reversible model can be written as $Q_{ij} = r_{ij} \pi_j$ with a symmetric matrix $r$; this is the [GTR model](/gtr-model/).

**Computing $P(t)$.** For a reversible $Q$ with $\pi > 0$, the matrix $S = \Pi^{1/2} Q \Pi^{-1/2}$ has entries $S_{ij} = \sqrt{\pi_i}\, Q_{ij} / \sqrt{\pi_j}$, and detailed balance makes it symmetric. By the [spectral theorem](/spectral-theorem/), $S = U \Lambda U^{\mathsf T}$ with $U$ orthogonal and $\Lambda$ real and diagonal, so

$$P(t) = \Pi^{-1/2}\, U\, e^{\Lambda t}\, U^{\mathsf T}\, \Pi^{1/2}.$$

One eigenvalue is 0 (the row sums of $Q$ are zero), and the others are negative when $Q$ is irreducible. A program [diagonalizes](/diagonalization/) $Q$ one time in $O(k^3)$ and then gets each $P(t)$ in $O(k^3)$, or in $O(k^2)$ per entry that it needs. The small models have closed forms for $P(t)$ and need no eigensolver.

**Branch lengths.** The expected number of substitutions per unit time at stationarity is $\sum_i \pi_i (-Q_{ii})$. Programs scale $Q$ so that this sum is 1. Then a branch of length $t$ carries on average $t$ substitutions per site, and the branch length is measured in *expected substitutions per site*. Only the product of the rate and the time enters $P(t)$: the pair $(cQ, t/c)$ gives the same matrix as $(Q, t)$. So data from one site pattern cannot separate a fast rate from a long time; the [molecular clock](/molecular-clock/) and dated fossils are needed for that.

**Counting parameters.** A general $Q$ on $k$ states has $k(k-1)$ free off-diagonal rates, one of which is fixed by the scaling. A reversible $Q$ has $k(k-1)/2$ exchangeabilities and $k - 1$ free frequencies, so for DNA it has $6 + 3 - 1 = 8$ free parameters. The table lists the DNA models of the next pages.

| model | constraint on $Q_{ij}$, $i \ne j$ | free parameters |
|---|---|---|
| [JC69](/jukes-cantor-model/) | $Q_{ij} = \mu$ | 0 |
| [K80](/kimura-two-parameter-model/) | $\kappa \beta$ for a transition, $\beta$ for a transversion | 1 ($\kappa$) |
| [F81](/felsenstein-81-model/) | $Q_{ij} = \mu \pi_j$ | 3 (frequencies) |
| [HKY85](/hky-model/) | $\kappa \beta \pi_j$ for a transition, $\beta \pi_j$ for a transversion | 4 |
| [GTR](/gtr-model/) | $Q_{ij} = r_{ij} \pi_j$, $r$ symmetric | 8 |

A *transition* is a change between the two purines (A and G) or between the two pyrimidines (C and T). A *transversion* is a change between a purine and a pyrimidine. Many models add [rate heterogeneity](/rate-heterogeneity/) across sites on top of $Q$.

## Examples

**JC69.** With the states in the order A, C, G, T, the scaled JC69 matrix has $Q_{ij} = 1/3$ for $i \ne j$ and $Q_{ii} = -1$. Its eigenvalues are $0$ and $-4/3$ (three times). For a branch of length $t = 0.1$, $P_{ii}(0.1) = 0.906380$ and $P_{ij}(0.1) = 0.031207$ for $i \ne j$. These are the closed form $\tfrac14 + \tfrac34 e^{-4t/3}$ and $\tfrac14 - \tfrac14 e^{-4t/3}$, and they agree with $e^{Qt}$ computed from the spectral form.

**K80 with $\kappa = 2$.** The scaled matrix has rate $0.5$ for each transition, $0.25$ for each transversion and $-1$ on the diagonal. The row of A in $Q$ is $(-1, 0.25, 0.5, 0.25)$. The eigenvalues are $0, -1, -1.5, -1.5$. For $t = 0.1$ the row of A in $P(t)$ is $(0.906563, 0.023791, 0.045855, 0.023791)$: the change to G, a transition, is about twice as likely as each transversion.

**Reversible with unequal frequencies.** Take GTR with $\pi = (0.1, 0.2, 0.3, 0.4)$ and exchangeabilities $r_{AC} = 1$, $r_{AG} = 4$, $r_{AT} = 0.5$, $r_{CG} = 1.2$, $r_{CT} = 3$, $r_{GT} = 1$. After scaling, $P(0.2)$ gives $\pi_A P_{AC} = 0.1 \times 0.030608 = 0.0030608$ and $\pi_C P_{CA} = 0.2 \times 0.015304 = 0.0030608$, as detailed balance requires, and $\pi P(0.2) = \pi$.

**A non-reversible chain.** On three states, let each state move to the next one in the cycle $1 \to 2 \to 3 \to 1$ at rate 1. The uniform distribution is stationary, because each column of $Q$ also sums to zero. But $\pi_1 Q_{12} = 1/3$ and $\pi_2 Q_{21} = 0$, so the chain is not reversible. A tree likelihood under this chain changes when the root moves.

**Not a rate matrix.** A matrix with a negative off-diagonal entry, or with a row that does not sum to zero, is not a rate matrix: $e^{Qt}$ then has negative entries or rows that do not sum to 1 for some $t > 0$.

## Where it is used

- **Likelihood of a tree.** The [phylogenetic likelihood](/phylogenetic-likelihood/) multiplies the matrices $P(t_e)$ of the branches, and [Felsenstein's pruning algorithm](/felsenstein-pruning/) computes it in time linear in the number of taxa and sites.
- **Tree inference.** [Maximum likelihood phylogeny](/maximum-likelihood-phylogeny/) and [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/) fit the tree and the parameters of $Q$ together.
- **Distances.** Each model gives a corrected distance between two sequences, the length of branch that best explains their differences: the JC69 and K80 formulas are on their pages. [Neighbor joining](/neighbor-joining/) and other distance methods use these distances.
- **Ancestors.** [Ancestral sequence reconstruction](/ancestral-sequence-reconstruction/) uses $P(t)$ to score the states of the internal nodes.
- **Scoring matrices.** The [PAM matrices](/pam-matrix/) of Dayhoff come from a Markov chain on amino acids: PAM$n$ is the $n$-th power of a one-step matrix, the discrete-time form of $e^{Qt}$.
- **Discrete-time chains.** The [Markov chain](/markov-chain/) page covers chains with discrete steps; a substitution model is the continuous-time chain whose transition matrix over time $t$ is $e^{Qt}$.

## References
