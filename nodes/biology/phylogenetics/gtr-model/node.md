---
tag: JG74MQ
kind: model
slug: gtr-model
name: General time-reversible model
aliases:
- GTR
- REV model
- GTR model
area: biology/phylogenetics
level: advanced
summary: The most general reversible DNA model. Q_ij = r_ij pi_j with a symmetric matrix r of six exchangeabilities and four base frequencies, for 8 free parameters after scaling.
history:
  year: 1986
  people: [Simon Tavaré]
  note: Tavaré described the continuous-time Markov chains on the four bases and the general reversible form of the rate matrix in lectures on the analysis of DNA sequences.
prereqs: [hky-model, detailed-balance]
see_also: [substitution-model, jukes-cantor-model, kimura-two-parameter-model, felsenstein-81-model, rate-heterogeneity, phylogenetic-likelihood, spectral-theorem, pam-matrix]
sources:
  - paper: "Simon Tavaré, Some probabilistic and statistical problems in the analysis of DNA sequences, in R. M. Miura (ed.), Some Mathematical Questions in Biology, DNA Sequence Analysis, Lectures on Mathematics in the Life Sciences 17, American Mathematical Society, 1986, pages 57 to 86"
    locator: the reversible rate matrix on the four bases and its parametrization by symmetric rates times base frequencies
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Models of nucleotide substitution (the general time-reversible model, the unrestricted model, and the spectral computation of P(t))
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 13, Models of DNA evolution (the general time-reversible model)
---

The general time-reversible model, GTR, is the largest [substitution model](/substitution-model/) for DNA that is still reversible. It writes each rate as $Q_{ij} = r_{ij} \pi_j$, where $\pi$ is the stationary distribution of the bases and $r$ is a symmetric matrix of six *exchangeabilities*, one for each pair of bases. Every reversible rate matrix on four states has exactly this form. After the scaling of time, GTR has 8 free parameters: 5 exchangeabilities and 3 frequencies. All the named DNA models on the earlier pages are special cases of it, so the family is nested as JC69 $\subset$ K80 $\subset$ HKY85 $\subset$ GTR and JC69 $\subset$ F81 $\subset$ HKY85 $\subset$ GTR. GTR with gamma [rate heterogeneity](/rate-heterogeneity/) is the default DNA model in many likelihood programs.

## The machine

**States and rates.** The states are A, C, G, T with frequencies $\pi_j > 0$. Fix six numbers $r_{AC}, r_{AG}, r_{AT}, r_{CG}, r_{CT}, r_{GT} \ge 0$ and put $r_{ji} = r_{ij}$. Then for $i \ne j$

$$Q_{ij} = r_{ij} \pi_j, \qquad Q_{ii} = -\sum_{j \ne i} r_{ij} \pi_j.$$

**Reversible, and all reversible models.** The flow $\pi_i Q_{ij} = r_{ij} \pi_i \pi_j$ is symmetric in $i$ and $j$, so [detailed balance](/detailed-balance/) holds and $\pi$ is stationary. Conversely, let $Q$ be any rate matrix that is reversible with respect to a positive $\pi$. Define $r_{ij} = Q_{ij} / \pi_j$. Detailed balance $\pi_i Q_{ij} = \pi_j Q_{ji}$ reads $\pi_i \pi_j r_{ij} = \pi_j \pi_i r_{ji}$, so $r$ is symmetric and $Q$ is a GTR matrix. So GTR is not one model among many reversible ones; it is the set of all of them.

**Parameters.** The overall rate is not identifiable from the branch lengths, so programs scale $Q$ so that $\sum_i \pi_i (-Q_{ii}) = 2 \sum_{i < j} r_{ij} \pi_i \pi_j = 1$, or equivalently fix one exchangeability (often $r_{GT} = 1$) and scale the branch lengths. That leaves $6 - 1 = 5$ exchangeabilities and $4 - 1 = 3$ frequencies. A general rate matrix with no reversibility has 12 off-diagonal rates, 11 after scaling; this is the *unrestricted* model.

**Computing $P(t)$.** There is no simple closed form, but reversibility makes the eigenvalue method stable. Let $\Pi = \mathrm{diag}(\pi)$ and $S = \Pi^{1/2} Q \Pi^{-1/2}$. Then $S_{ij} = \sqrt{\pi_i \pi_j}\, r_{ij}$ for $i \ne j$, which is symmetric. By the [spectral theorem](/spectral-theorem/), $S = U \Lambda U^{\mathsf T}$ with $U$ orthogonal, and

$$P(t) = \Pi^{-1/2}\, U e^{\Lambda t} U^{\mathsf T}\, \Pi^{1/2}, \qquad P_{ij}(t) = \sqrt{\frac{\pi_j}{\pi_i}} \sum_{m} U_{im} U_{jm} e^{\lambda_m t}.$$

The eigenvalues $\lambda_m$ are real. One is 0 with eigenvector $\sqrt{\pi}$, and the other three are negative when the chain is irreducible. A program [diagonalizes](/diagonalization/) $S$ one time for each new $Q$, and then each branch length costs only the $e^{\lambda_m t}$ and a matrix product. A non-reversible $Q$ can have complex eigenvalues and a badly conditioned eigenvector matrix.

## What it counts

The entries $r_{ij}$ measure how easily two bases swap, apart from how common they are. The expected number of $i \leftrightarrow j$ changes per unit time at stationarity is $\pi_i Q_{ij} + \pi_j Q_{ji} = 2 r_{ij} \pi_i \pi_j$. So a large count of A and G changes in the data can come from a large $r_{AG}$ or from large $\pi_A$ and $\pi_G$, and the model separates the two. Branch lengths are, as always, expected substitutions per site.

## Relation to other models

| model | exchangeabilities | frequencies | free parameters |
|---|---|---|---|
| [JC69](/jukes-cantor-model/) | all equal | equal | 0 |
| [K80](/kimura-two-parameter-model/) | $r_{AG} = r_{CT} = \kappa$, others 1 | equal | 1 |
| [F81](/felsenstein-81-model/) | all equal | free | 3 |
| [HKY85](/hky-model/) | $r_{AG} = r_{CT} = \kappa$, others 1 | free | 4 |
| TN93 | $r_{AG} = \kappa_1$, $r_{CT} = \kappa_2$, others 1 | free | 5 |
| GTR | free | free | 8 |

- **Nested tests.** Each model in the table is GTR with some constraints, so a likelihood ratio test of HKY85 against GTR has $8 - 4 = 4$ degrees of freedom. Model selection programs fit the family and compare the fits with such tests or with information criteria.
- **Beyond reversibility.** The unrestricted model drops reversibility. Its likelihood depends on the position of the root, and the [pulley principle](/phylogenetic-likelihood/) fails for it.
- **Amino acids.** GTR on 20 states has $190 - 1 + 19 = 208$ free parameters, too many for one alignment. Empirical protein models instead fix the 190 exchangeabilities from large databases; the [PAM matrices](/pam-matrix/) of Dayhoff are the first such model.
- **Across sites.** GTR fixes one $Q$ for all sites. [Rate heterogeneity](/rate-heterogeneity/) scales $Q$ by a random rate at each site, which gives GTR+$\Gamma$ and GTR+I+$\Gamma$.

## Known results in the model

**A worked matrix.** Take $\pi = (0.1, 0.2, 0.3, 0.4)$ in the order A, C, G, T and exchangeabilities $r_{AC} = 1$, $r_{AG} = 4$, $r_{AT} = 0.5$, $r_{CG} = 1.2$, $r_{CT} = 3$, $r_{GT} = 1$. The raw rate is $2(0.02 + 0.12 + 0.02 + 0.072 + 0.24 + 0.12) = 1.184$, and dividing by it gives

| | A | C | G | T |
|---|---|---|---|---|
| A | $-1.351351$ | $0.168919$ | $1.013514$ | $0.168919$ |
| C | $0.084459$ | $-1.402027$ | $0.304054$ | $1.013514$ |
| G | $0.337838$ | $0.202703$ | $-0.878378$ | $0.337838$ |
| T | $0.042230$ | $0.506757$ | $0.253378$ | $-0.802365$ |

The eigenvalues are $0$, $-0.797966$, $-1.751415$ and $-1.884741$. At $t = 0.2$ the symmetrized eigenvalue method gives

| | A | C | G | T |
|---|---|---|---|---|
| A | $0.768994$ | $0.030608$ | $0.164401$ | $0.035997$ |
| C | $0.015304$ | $0.764926$ | $0.054364$ | $0.165406$ |
| G | $0.054800$ | $0.036243$ | $0.847104$ | $0.061853$ |
| T | $0.008999$ | $0.082703$ | $0.046390$ | $0.861908$ |

It satisfies $\pi P(0.2) = \pi$ and $\pi_i P_{ij} = \pi_j P_{ji}$ for each pair; for A and C both sides are $0.0030608$.

**Rooting.** Under GTR, as under every reversible model with the root drawn from $\pi$, the likelihood of a tree does not depend on the root position. So GTR trees are unrooted, and a root needs extra information such as an outgroup or a [molecular clock](/molecular-clock/).

**Identifiability.** For a GTR tree with all branch lengths positive, the distribution of site patterns at the leaves determines the unrooted tree topology. This is a consequence of a stronger result for the general Markov model on trees, and it is why [maximum likelihood](/maximum-likelihood-phylogeny/) is consistent under GTR.

## References
