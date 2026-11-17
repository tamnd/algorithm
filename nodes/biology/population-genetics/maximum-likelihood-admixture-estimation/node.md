---
tag: KYJWNZ
kind: algorithm
slug: maximum-likelihood-admixture-estimation
name: Maximum likelihood admixture estimation
aliases:
- ADMIXTURE algorithm
area: biology/population-genetics
level: advanced
summary: Fit ancestry proportions and population allele frequencies by maximum likelihood with block relaxation and quasi-Newton acceleration.
model: real-ram
complexity:
  vars: {n: the number of individuals, m: the number of sites, k: the number of ancestral populations, T: the number of rounds}
  time: {worst: O(T n m k), average: O(T n m k), best: O(n m k)}
  space: {extra: O(n m + n k + m k)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [David H. Alexander, John Novembre, Kenneth Lange]
  note: "Alexander, Novembre and Lange released ADMIXTURE in 2009. It maximizes the likelihood of the STRUCTURE admixture model by block relaxation, with sequential quadratic programming in each block and a quasi-Newton acceleration. Tang and coauthors had fitted the same likelihood by EM in FRAPPE in 2005."
prereqs: [pritchard-stephens-donnelly-model, maximum-likelihood-estimation, expectation-maximization]
see_also: [population-structure-inference, genetic-principal-components, nonnegative-matrix-factorization, coordinate-descent, quasi-newton-method, projected-gradient-descent, local-ancestry-inference, fixation-index]
sources:
  - paper: doi:10.1101/gr.094052.109
    title: David H. Alexander, John Novembre and Kenneth Lange, Fast model-based estimation of ancestry in unrelated individuals, Genome Research 19(9), 2009
    locator: pp. 1655-1664 (the log-likelihood, block relaxation over Q and F, sequential quadratic programming for each block, and quasi-Newton acceleration)
  - paper: "Hua Tang, Jie Peng, Pei Wang and Neil J. Risch, Estimation of individual admixture, analytical and study design considerations, Genetic Epidemiology 28(4), 2005"
    title: Tang, Peng, Wang and Risch 2005
    locator: pp. 289-301 (FRAPPE, an EM algorithm for the same likelihood)
  - paper: doi:10.1007/s11222-009-9166-3
    title: Hua Zhou, David H. Alexander and Kenneth Lange, A quasi-Newton acceleration for high-dimensional optimization algorithms, Statistics and Computing 21(2), 2011
    locator: pp. 261-273 (the secant approximation of the differential of an algorithm map and the extrapolated step)
  - paper: doi:10.1093/genetics/155.2.945
    title: Jonathan K. Pritchard, Matthew Stephens and Peter Donnelly, Inference of population structure using multilocus genotype data, Genetics 155(2), 2000
    locator: pp. 945-959 (the admixture model whose likelihood ADMIXTURE maximizes)
---

Maximum likelihood admixture estimation fits the admixture model of the [Pritchard-Stephens-Donnelly model](/pritchard-stephens-donnelly-model/) by maximizing its likelihood instead of sampling from a posterior. Each individual $i$ has ancestry proportions $q_{i1}, \ldots, q_{iK}$ over $K$ ancestral populations, and each population $k$ has an allele frequency $f_{kj}$ at site $j$. The best known program is ADMIXTURE, by Alexander, Novembre and Lange (2009). It updates all ancestry proportions with the frequencies fixed, then all frequencies with the proportions fixed, and repeats; this is block relaxation, a form of [coordinate descent](/coordinate-descent/) by blocks. A quasi-Newton step speeds up the repetition. The result is a local maximum of the likelihood, found much faster than with the Gibbs sampler of STRUCTURE.

## In plain words

Assume that there were a few source populations, each with its own share of each variant. Every person is a mix of these sources in some proportions. The method looks for the source frequencies and the mixing proportions that make the observed genotypes most likely.

It improves one set while it holds the other fixed. With the source frequencies fixed, it finds better mixing proportions for each person. With the proportions fixed, it finds better frequencies for each variant and source. Each of these steps makes the data at least as likely as before. A jump that guesses where the steps are going makes the method faster. The answer can depend on the start, so users run it from several starts and keep the best.

## The problem

**Input.** Genotypes $g_{ij} \in \{0, 1, 2\}$ for $n$ individuals at $m$ biallelic sites, and a number $K$ of ancestral populations.

**Model.** Given $Q = (q_{ik})$ with each row on the simplex and $F = (f_{kj})$ with entries in $[0, 1]$, each of the two allele copies of individual $i$ at site $j$ comes from population $k$ with probability $q_{ik}$ and then carries allele 1 with probability $f_{kj}$, independently of all other copies. So $g_{ij}$ is binomial with 2 trials and success probability $\phi_{ij} = \sum_k q_{ik} f_{kj}$, and the log-likelihood is

$$L(Q, F) = \sum_{i, j} \big[ g_{ij} \ln \phi_{ij} + (2 - g_{ij}) \ln (1 - \phi_{ij}) \big].$$

This is the likelihood of the admixture model of STRUCTURE, without the prior. The matrix $\Phi = Q F$ of expected allele frequencies is a product of two nonnegative factors, so the problem is a [nonnegative matrix factorization](/nonnegative-matrix-factorization/) with a binomial likelihood in place of the squared error and with the rows of $Q$ on the simplex.

**Output.** $(\hat Q, \hat F)$ at a local maximum of $L$ over the product of simplices and boxes, and the value $L(\hat Q, \hat F)$.

## The algorithm

```pseudo id=main
ADMIXTURE(G, K, rng)
L1  Q, F ← a random start from rng
L2  repeat at most T times                          ▷ x = (Q, F)
L3      x1 ← BLOCK(x)                               ▷ improve Q with F fixed, then F with Q fixed
L4      x2 ← BLOCK(x1)
L5      u ← x1 - x; v ← x2 - x1
L6      c ← -uᵀu / uᵀ(v - u)
L7      y ← project((1 - c) x1 + c x2) onto the feasible set
L8      if L(y) < L(x2) then y ← x2
L9      x ← y
L10     if L gained less than ε in this round then stop
L11 return Q, F
```

**The blocks.** With $F$ fixed, $L$ splits into $n$ problems, one per row $q_i$, each concave in $q_i$ on a simplex of dimension $K - 1$. With $Q$ fixed, $L$ splits into $m$ problems, one per column $f_j$, each concave in $f_j$ on the box $[0, 1]^K$. ADMIXTURE solves each small problem approximately by sequential quadratic programming: a quadratic approximation of the log-likelihood is maximized under the constraints. The code on this page takes one EM step in each block instead. The hidden data are the source populations of the allele copies. With $\phi_{ij}$ at the current values, the expected number of copies of allele 1 in $g_{ij}$ that come from population $k$ is $a_{ijk} = g_{ij} q_{ik} f_{kj} / \phi_{ij}$, and of allele 0 it is $b_{ijk} = (2 - g_{ij}) q_{ik} (1 - f_{kj}) / (1 - \phi_{ij})$. The EM updates are

$$q_{ik} \leftarrow \frac{1}{2m} \sum_j (a_{ijk} + b_{ijk}), \qquad f_{kj} \leftarrow \frac{\sum_i a_{ijk}}{\sum_i (a_{ijk} + b_{ijk})}.$$

These are the updates of FRAPPE, applied one block at a time. They are slower per unit of progress than the SQP steps, but they also never lower $L$, and they keep $Q$ and $F$ feasible.

**The acceleration.** Lines L5 to L7 treat a round of block relaxation as a map $x \mapsto \mathcal F(x)$ whose fixed point is wanted. The secant pair $(u, v)$ gives a rank-one estimate of the differential of $\mathcal F$, and line L6 solves the linearized fixed point equation along it. With $c = 1$ the step is $x_2$; larger $c$ extrapolates further along the path. Line L7 puts each row of $Q$ back on the simplex and clips $F$ to $[\delta, 1 - \delta]$, and line L8 rejects a step that is worse than two plain rounds. This is the scheme of Zhou, Alexander and Lange (2011) with one secant pair.

## Example

One individual, three sites and $K = 2$, with $F$ fixed to $f_1 = (0.8, 0.4, 0.9)$ and $f_2 = (0.2, 0.4, 0.3)$, genotype $g = (2, 0, 1)$ and start $q = (0.5, 0.5)$.

- Site 1: $\phi = 0.5$. The two copies of allele 1 split as $0.4/0.5$ and $0.1/0.5$, so $1.6$ copies go to population 1 and $0.4$ to population 2.
- Site 2: $\phi = 0.4$. The two copies of allele 0 split as $0.3/0.6$ and $0.3/0.6$: $1.0$ and $1.0$.
- Site 3: $\phi = 0.6$. The copy of allele 1 splits $0.75$ and $0.25$; the copy of allele 0 splits $0.05/0.4 = 0.125$ and $0.875$.

The totals are $3.475$ and $2.525$ out of 6, so the new $q$ is $(0.5792, 0.4208)$, and $L$ rises from $-3.8351$ to $-3.7038$. Further EM steps give $q_1 = 0.6367, 0.6774, 0.7059, \ldots$, which approach the maximum $q_1 = 0.7790$, where $L = -3.5536$. After 7 steps $q_1$ is only $0.7508$. The gap shrinks by a nearly constant factor per step, which is the slow linear convergence that the SQP steps and the acceleration of ADMIXTURE avoid.

## Correctness

Each block step never lowers $L$. For the EM step, the reason is the usual EM inequality for the model with known source populations: in that model the log-likelihood is a sum of multinomial terms, and the updates are its maximum likelihood values given the expected counts. The Q update keeps each row on the simplex, because $\sum_k (a_{ijk} + b_{ijk}) = 2$ for every $(i, j)$, so the row sums are $2m / 2m = 1$. The F update is a ratio in $[0, 1]$. Line L8 accepts the extrapolated point only if its likelihood is at least that of $x_2$, which is at least $L(x)$, so the values $L$ never decrease. Since $L \le 0$, they converge. At a fixed point with positive entries, the partial derivatives of $L$ in a row of $Q$ are all equal to $2m$, and the partial derivatives in the interior entries of $F$ are 0. These are the Karush-Kuhn-Tucker conditions of the constrained problem. The full proof is below. Nothing here shows that the point is the global maximum.

## Complexity

- **One block step.** Computing $\phi_{ij}$ for all pairs costs $O(n m K)$, and so do the sums of the EM updates. A round of line L3 costs $O(n m K)$, and lines L4 to L8 add a constant factor.
- **Rounds.** The number of rounds $T$ depends on the data and the start. Plain EM converges linearly and can need thousands of rounds; the SQP blocks and the acceleration cut this a lot in the experiments of Alexander and coauthors.
- **Space.** $O(n m)$ for the genotypes and $O((n + m) K)$ for $Q$ and $F$.
- **Comparison.** One sweep of the STRUCTURE Gibbs sampler also costs $O(n m K)$, but it needs many thousands of sweeps for a posterior summary, and ADMIXTURE reached similar estimates in far less time on the data of its paper.

## Properties

- **Local maxima.** $L$ is concave in each block but not jointly. Different starts can end at different local maxima, so several starts are the norm.
- **Label switching.** Any permutation of the $K$ populations gives the same likelihood. Runs must be aligned before they are compared.
- **Saddle points.** A start where all rows of $Q$ are equal and all populations have the same frequencies is a fixed point of the EM steps, and for structured data it is not a maximum. A random start avoids it.
- **Boundary values.** Many maximum likelihood values lie on the boundary, with $f_{kj} = 0$ or $1$ or $q_{ik} = 0$. EM often approaches them slowly, because it multiplies each entry by a factor and an entry that is positive stays positive unless the data give it no weight at all. SQP treats the bounds as constraints and can land on them.
- **$K = 1$.** The maximum is $\hat f_{1j} = \sum_i g_{ij} / (2n)$, the sample allele frequency, reached in one F step.

## Variants and improvements

- **Choosing $K$.** A later version of ADMIXTURE adds cross-validation: it holds out entries of $G$, fits the model to the rest and measures how well it predicts the held-out genotypes.
- **Supervised mode.** If some individuals are known to come from one population, their rows of $Q$ are fixed, and only the rest are fitted.
- **Bayesian fits.** STRUCTURE samples from the posterior by [Gibbs sampling](/gibbs-sampling/), which gives uncertainty but is much slower. Variational methods give an approximate posterior at a cost close to that of ADMIXTURE.
- **Large data.** Programs for millions of individuals use stochastic or alternating least squares versions of the same factorization.
- **Other optimizers.** [Projected gradient descent](/projected-gradient-descent/) and [quasi-Newton methods](/quasi-newton-method/) on the full parameter vector also work, but the block form keeps each subproblem small.

## When to use it

Use it for genome-wide data on many unrelated individuals when you want ancestry proportions with a clear meaning, and when the sample has no strong relatedness. For a first look, or to choose covariates, [principal components of genotypes](/genetic-principal-components/) are faster and need no $K$. For the ancestry of each segment of a genome, use [local ancestry inference](/local-ancestry-inference/).

## Pitfalls

- **The model is a simplification.** Real populations do not come from $K$ discrete sources without drift between them. The method fits a $K$-source model to any data, including data from a continuous gradient, and the bars it draws can then mislead.
- **Linkage.** The likelihood treats sites as independent. Dense data in linkage disequilibrium count the same signal many times, which makes the fit look more certain than it is. Pruning sites in high LD is common.
- **Relatives.** Families form their own cluster, which takes one of the $K$ components.
- **Sample sizes.** A large group can split into several components while small groups merge, so proportions depend on the sampling design.
- **Convergence.** Stop on the gain in log-likelihood and compare several starts. A small change of the parameters per round does not mean a maximum.

## Implementations

## History

Pritchard, Stephens and Donnelly (2000) defined the admixture model and fitted it with a Gibbs sampler in STRUCTURE. Tang, Peng, Wang and Risch (2005) maximized the same likelihood by EM in FRAPPE. Alexander, Novembre and Lange (2009) released ADMIXTURE, which uses block relaxation with sequential quadratic programming and a quasi-Newton acceleration, and was much faster on genome-wide data. Zhou, Alexander and Lange (2011) published the acceleration as a general method for algorithm maps.

## References
