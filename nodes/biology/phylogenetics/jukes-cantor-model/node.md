---
tag: DFJ3G7
kind: model
slug: jukes-cantor-model
name: Jukes-Cantor model
aliases:
- JC69
- Jukes-Cantor 1969 model
area: biology/phylogenetics
level: intro
summary: The simplest DNA substitution model. All bases have frequency 1/4 and every change has the same rate, so P(same) = 1/4 + 3/4 e^(-4t/3) after t substitutions per site.
history:
  year: 1969
  people: [Thomas H. Jukes, Charles R. Cantor]
  note: Jukes and Cantor used equal rates of change among the four nucleotides in a long review of protein evolution, to correct counts of differences for multiple changes at one site.
prereqs: [substitution-model]
see_also: [kimura-two-parameter-model, felsenstein-81-model, gtr-model, rate-heterogeneity, phylogenetic-likelihood, neighbor-joining, long-branch-attraction, tree-metric]
sources:
  - paper: "Thomas H. Jukes and Charles R. Cantor, Evolution of protein molecules, in H. N. Munro (ed.), Mammalian Protein Metabolism, Volume III, Academic Press, New York, 1969, pages 21 to 132"
    locator: the equal-rate model of nucleotide change and the correction of observed differences for multiple changes
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 1, Section 1.2 (the JC69 model, its transition probabilities and the JC69 distance with its variance)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 11 (the Jukes-Cantor distance) and Chapter 13 (models of DNA evolution)
---

The Jukes-Cantor model, JC69, is the simplest [substitution model](/substitution-model/) for DNA. Each of the four bases has stationary frequency $1/4$, and each base changes to each of the other three at the same rate. One number, the branch length $t$ in expected substitutions per site, then fixes all transition probabilities: a site keeps its base with probability $\tfrac14 + \tfrac34 e^{-4t/3}$. Two sequences that differ at a fraction $p$ of their sites are at the corrected distance $d = -\tfrac34 \ln(1 - \tfrac43 p)$. The model is the base case of the families of models on the next pages, and it is the model of many hardness and consistency results in phylogenetics.

## The machine

**States and rates.** The states are A, C, G and T. With the rate scaled to one substitution per unit time, the [rate matrix](/substitution-model/) is

$$Q = \begin{pmatrix} -1 & \tfrac13 & \tfrac13 & \tfrac13 \\ \tfrac13 & -1 & \tfrac13 & \tfrac13 \\ \tfrac13 & \tfrac13 & -1 & \tfrac13 \\ \tfrac13 & \tfrac13 & \tfrac13 & -1 \end{pmatrix}.$$

The original form uses a rate $\mu$ for each of the three changes away from a base, so $Q_{ij} = \mu$ for $i \ne j$; the scaling sets $3\mu = 1$. The stationary distribution is $\pi = (\tfrac14, \tfrac14, \tfrac14, \tfrac14)$, and the model is reversible because $Q$ is symmetric.

**Transition probabilities.** Write $Q = \tfrac13 J - \tfrac43 I$, where $J$ is the all-ones matrix. The two parts commute and $J^2 = 4J$, so $e^{(t/3)J} = I + \tfrac14 (e^{4t/3} - 1) J$ and

$$P(t) = e^{-4t/3} I + \tfrac14 \left(1 - e^{-4t/3}\right) J.$$

In entries,

$$P_{ii}(t) = \frac14 + \frac34 e^{-4t/3}, \qquad P_{ij}(t) = \frac14 - \frac14 e^{-4t/3} \quad (i \ne j).$$

The eigenvalues of $Q$ are $0$ and $-4/3$ (three times). As $t \to \infty$, every entry tends to $1/4$.

**On a tree.** A JC69 tree is a tree with a length $t_e \ge 0$ on each edge. The root base is uniform, and each edge applies $P(t_e)$ independently. Each site of an alignment is an independent draw from this process.

**A useful parametrization.** Put $x_e = e^{-4t_e/3} \in (0, 1]$. Then $P_{ii} = (1 + 3x_e)/4$ and $P_{ij} = (1 - x_e)/4$ are linear in $x_e$, and two edges in a row multiply: a path of edges $e_1, \ldots, e_r$ acts like one edge with $x = x_{e_1} \cdots x_{e_r}$. This makes exact rational tests of likelihood code easy, and the [pruning](/felsenstein-pruning/) tests use it.

**$k$ states.** The same model on $k$ states has $P_{ii}(t) = \tfrac1k + \tfrac{k-1}{k} e^{-kt/(k-1)}$. For $k = 2$ it is the Cavender-Farris-Neyman (CFN) model of a binary character, and for $k = 20$ it is the Poisson model of amino acids.

## What it counts

**Substitutions per site.** The branch length $t$ is the expected number of substitutions per site along the branch. Some of them are not visible: a site can change and change back, or change twice to a third base. The probability that the two ends of a branch differ is

$$p(t) = \frac34 \left(1 - e^{-4t/3}\right),$$

which is less than $t$ for every $t > 0$ and tends to $3/4$ as $t \to \infty$.

**The JC69 distance.** Two sequences of $m$ sites differ at $x$ sites, so $\hat p = x/m$. Under JC69 the number of differences is binomial with success probability $p(d)$, and $\hat p$ is the [maximum likelihood estimate](/maximum-likelihood-estimation/) of $p$. Because $p(d)$ is increasing in $d$, the estimate of $d$ is the inverse of $p(d)$ at $\hat p$:

$$\hat d = -\frac34 \ln\left(1 - \frac43 \hat p\right).$$

The delta method gives its approximate variance

$$\mathrm{Var}(\hat d) \approx \frac{\hat p (1 - \hat p)}{m \left(1 - \tfrac43 \hat p\right)^2}.$$

**Saturation.** When $\hat p \ge 3/4$ the formula is not defined, and the estimate of $d$ is infinite. Near $3/4$ the variance becomes very large: the sequences carry almost no information about how far apart they are.

## Relation to other models

- **It is the special case of all common DNA models.** [K80](/kimura-two-parameter-model/) with $\kappa = 1$ is JC69. [F81](/felsenstein-81-model/) with equal base frequencies is JC69. So JC69 sits at the bottom of both chains JC69 $\subset$ K80 $\subset$ HKY85 $\subset$ GTR and JC69 $\subset$ F81 $\subset$ HKY85, and a [likelihood ratio test](/maximum-likelihood-estimation/) of JC69 against K80 has one degree of freedom.
- **It treats transitions and transversions alike.** Real DNA has more transitions than transversions. When data come from K80 with $\kappa > 1$, JC69 underestimates long distances. For example, at $d = 0.3$ and $\kappa = 5$ the expected proportions of transition and transversion differences are $0.161651$ and $0.078770$; the K80 formula gives back $d = 0.3$, but JC69 gives $0.289866$.
- **It has one rate for all sites.** Real sites vary in rate. The [rate heterogeneity](/rate-heterogeneity/) models JC69+$\Gamma$ and JC69+I add this to JC69.
- **It is a group-based model.** The rates depend only on whether two bases are equal, so the model is invariant under the Klein four-group acting on the bases, like K80 and Kimura's three-parameter model. For such models the Fourier (Hadamard) transform turns the site-pattern probabilities into a simple function of the edge lengths.

## Known results in the model

**Closed forms.** The transition probabilities and the two-sequence distance have the closed forms above. The table gives $P(t)$ and the distance at some values.

| $t$ | $P_{ii}(t)$ | $P_{ij}(t)$ | | $\hat p$ | $\hat d$ |
|---|---|---|---|---|---|
| 0.1 | 0.906380 | 0.031207 | | 0.2 | 0.232616 |
| 0.5 | 0.635063 | 0.121646 | | 0.5 | 0.823959 |
| 1 | 0.447698 | 0.184101 | | 0.7 | 2.031038 |
| 2 | 0.302113 | 0.232629 | | 0.74 | 3.238116 |

For $\hat p = 0.2$ and $m = 100$ sites, the variance is $0.2 \times 0.8 / (100 \times (1 - 0.8/3)^2) = 0.0029752$, so the standard error of $\hat d = 0.2326$ is about $0.0545$. The last row shows saturation: a change of $\hat p$ from $0.7$ to $0.74$ moves $\hat d$ by more than 1.

**The distance is additive in expectation.** If $d_{ij}$ is the sum of the edge lengths on the path between leaves $i$ and $j$, then the expected proportion of differences is $p(d_{ij})$, so applying the inverse gives back an exact [tree metric](/tree-metric/). This is why [neighbor joining](/neighbor-joining/) on JC69 distances is a consistent method: as the sequences get longer, the estimated distances converge to a tree metric and the method returns the true tree.

**Likelihood on a tree.** The [phylogenetic likelihood](/phylogenetic-likelihood/) under JC69 is computed by [Felsenstein's pruning algorithm](/felsenstein-pruning/). Maximum likelihood is a statistically consistent estimator of the tree under JC69. Finding the maximum likelihood tree is NP-hard under JC69 and under the CFN model ([ML tree is NP-hard](/ml-tree-np-hard/)).

**Long branch attraction.** Felsenstein's four-taxon example, two long branches that are not neighbors, already makes [maximum parsimony](/maximum-parsimony/) inconsistent under JC69-like models. See [long branch attraction](/long-branch-attraction/).

## References
