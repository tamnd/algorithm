---
tag: VD1YS1
kind: problem
slug: divergence-time-estimation
name: Divergence time estimation
aliases:
- dating phylogenies
area: biology/phylogenetics
level: advanced
summary: Given a rooted tree, aligned sequences, a clock model and calibrations such as fossil ages, estimate the age of every internal node. Without a calibration, only relative ages are identifiable.
prereqs: [molecular-clock, relaxed-molecular-clock]
see_also: [bayesian-phylogenetic-inference, ultrametric-tree-reconstruction, upgma, birth-death-process, yule-model, kingman-coalescent, regularization, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1007/BF01797451
    title: Charles H. Langley and Walter M. Fitch, An examination of the constancy of the rate of molecular evolution, Journal of Molecular Evolution 3(3), 1974, 161-177
    locator: the maximum likelihood ages of a clock tree from Poisson counts of substitutions on its branches
  - paper: doi:10.1093/oxfordjournals.molbev.a025731
    title: Michael J. Sanderson, A nonparametric approach to estimating divergence times in the absence of rate constancy, Molecular Biology and Evolution 14(12), 1997, 1218-1231
    locator: nonparametric rate smoothing, the choice of ages that makes the rates of adjacent branches as close as possible
  - paper: doi:10.1093/oxfordjournals.molbev.a003974
    title: Michael J. Sanderson, Estimating absolute rates of molecular evolution and divergence times, a penalized likelihood approach, Molecular Biology and Evolution 19(1), 2002, 101-109
    locator: the penalized likelihood with a roughness penalty on rate changes between adjacent branches, and the choice of the smoothing parameter by cross-validation
  - paper: doi:10.1093/oxfordjournals.molbev.a025892
    title: Jeffrey L. Thorne, Hirohisa Kishino and Ian S. Painter, Estimating the rate of evolution of the rate of molecular evolution, Molecular Biology and Evolution 15(12), 1998, 1647-1657
    locator: Bayesian estimation of ages under autocorrelated rates, by MCMC
  - paper: doi:10.1371/journal.pbio.0040088
    title: Alexei J. Drummond, Simon Y. W. Ho, Matthew J. Phillips and Andrew Rambaut, Relaxed phylogenetics and dating with confidence, PLoS Biology 4(5), 2006, e88
    locator: joint Bayesian estimation of the tree and the ages under uncorrelated relaxed clocks
  - paper: doi:10.1093/molbev/msm088
    title: Ziheng Yang, PAML 4, phylogenetic analysis by maximum likelihood, Molecular Biology and Evolution 24(8), 2007, 1586-1591
    locator: the program MCMCTree for Bayesian dating with soft bounds on fossil calibrations
  - book: isbn:9780199602605
    title: Ziheng Yang, Molecular Evolution, a Statistical Approach, Oxford University Press, 2014
    locator: Chapter 10, Molecular clock and estimation of species divergence times, Section 10.3, likelihood estimation, and Section 10.4, Bayesian estimation
---

Divergence time estimation, or dating a phylogeny, asks for the ages of the internal nodes of a rooted tree. The data are aligned sequences and a few calibrations: fossil ages that bound the age of some nodes, or the sampling dates of the tips. The link between sequences and time is a clock model. Under a [strict clock](/molecular-clock/) the length of each branch is one rate times its duration, and under a [relaxed clock](/relaxed-molecular-clock/) each branch has its own rate. Sequences alone give only branch lengths, which are products of rate and time, so a calibration is needed to turn them into ages: without one, every age can be doubled and every rate halved with no change in the likelihood. The main methods are maximum likelihood under a strict clock (Langley and Fitch 1974), rate smoothing and penalized likelihood (Sanderson 1997, 2002), and Bayesian MCMC under relaxed clocks (Thorne, Kishino and Painter 1998; Drummond et al. 2006).

## In plain words

Sequences tell you how much two species have changed since they split. They do not tell you how long ago that was, because a lot of change could mean a long time or a fast rate. To read time, you need at least one known date, such as a fossil that shows a group existed 60 million years ago.

With that date, you can work out the rate of change, and then the ages of all other splits on the tree. If the rate differs between branches, you also need a rule for how it may vary, such as "neighbor branches have similar rates". The answer is an age for every split, with a range that shows how sure you can be.

## Definition

**Input.** A rooted binary tree $\tau$ on $n$ taxa, usually fixed in advance; an alignment of $m$ sites, such as DNA; a substitution model; a clock model, which gives each branch $e$ a rate $r_e$ (one common rate for a strict clock); and a set of calibrations, each a bound $t_v \ge a_v$, $t_v \le c_v$ or $t_v = a_v$ on the age of a node $v$, or a prior density on $t_v$. If the tree is not given, it must be found too, by a heuristic search or MCMC over the $(2n-3)!!$ rooted binary trees.

**Output.** Ages $t_v$ for the internal vertices, with $t_u > t_v$ when $u$ is the parent of $v$, and the leaves at age 0 (or at their sampling dates). The branch from $u$ to $v$ has length $b_e = r_e (t_u - t_v)$. A likelihood method returns a point estimate with a confidence interval; a Bayesian method returns the posterior distribution of the ages.

**Theorem (rate and time are not identified).** For every $c > 0$, the parameters $(\mathbf r, \mathbf t)$ and $(c\,\mathbf r, \mathbf t / c)$ give the same branch lengths, so they give the same likelihood for every data set. Hence without a calibration, the likelihood can identify at most the branch lengths: under a strict clock these are the relative ages $t_v / t_{\text{root}}$ and the products $r\,t_v$.

*Proof.* The length of branch $e$ from $u$ to $v$ is $c\,r_e \cdot (t_u - t_v)/c = r_e (t_u - t_v)$, and the likelihood depends on $\mathbf r$ and $\mathbf t$ only through the branch lengths. Under a strict clock, $t_v / t_{\text{root}}$ and $r\,t_v$ do not change under the scaling, and they determine all branch lengths. $\blacksquare$

One calibration with a fixed age fixes $c$. A calibration that is only a minimum, $t_v \ge a_v$, does not: every scaling with $t_v \ge a_v$ keeps the same maximum likelihood. Bayesian methods resolve this with a prior on the ages and rates, so the result then depends on the prior.

## Variants

- **Strict clock with a fixed calibration.** One rate; the ages follow from the heights of the nodes in substitutions, scaled to the calibration.
- **Relaxed clock.** Rates vary by branch, with an autocorrelated or uncorrelated prior, and the ages are estimated jointly with the rates, usually by MCMC.
- **Soft bounds.** A calibration is a density on the age with a small probability outside the bounds, as in MCMCTree, so that a wrong fossil date does not force a wrong answer.
- **Tip dating.** For fast-evolving viruses, the sampling dates of the sequences calibrate the clock, and the problem asks for the date of the most recent common ancestor.
- **Joint tree and time.** The topology is unknown and sampled together with the ages, as in BEAST.

## Examples

**Langley-Fitch with one calibration.** Take the rooted tree $((A,B),C)$ with Poisson counts of substitutions on its branches: 10 on the branch to A, 14 on the branch to B, 8 on the branch from the root to the ancestor of A and B, and 30 on the branch from the root to C. A fossil fixes the root age at $T = 60$ million years (My). Under a strict clock with rate $r$ per My for the whole sequence, and the ancestor of A and B at age $t$, the expected counts are $rt$, $rt$, $r(T - t)$ and $rT$. For fixed $t$ the best rate is $62 / (t + 120)$, and the log likelihood is then highest at

| quantity | value |
|---|---|
| age $t$ of the ancestor of A and B | 33.853 My |
| rate $r$ | 0.40298 substitutions per My |
| expected counts on A, B, the inner branch and C | 13.64, 13.64, 10.54, 24.18 |
| log likelihood | -10.4391 |

The expected counts sum to the observed 62. Without the fossil, the same log likelihood $-10.4391$ comes from $(r, T, t) = (0.806, 30, 16.93)$ or from $(0.134, 180, 101.56)$; only the ratio $t / T = 0.564$ and the products $rt$ and $rT$ are fixed by the data. The counts on A and B, 10 and 14, differ from the common expectation 13.64; a model with a free rate on each branch fits better, with log likelihood $-8.914$, which is the departure that a relaxed clock would absorb.

**Penalized likelihood.** Sanderson (2002) lets each branch have its own rate and maximizes
$$\log L(\mathbf r, \mathbf t) - \lambda \sum_{e} (r_e - r_{\mathrm{parent}(e)})^2$$
under the calibrations, where the sum runs over branches with a parent branch. A large smoothing parameter $\lambda$ forces a near strict clock; a small one lets rates vary freely and makes the ages poorly determined. The program r8s chooses $\lambda$ by cross-validation: it removes each tip in turn and measures how well the rest predicts its branch.

## Known algorithms

- **Langley and Fitch (1974).** Maximum likelihood ages under a strict clock, from substitution counts or from the sequences, by numerical optimization over the ages.
- **Ultrametric fit and scale.** Fit a clock tree to distances, as by [UPGMA](/upgma/) or [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/), and scale the heights so that the calibrated node has its age.
- **Nonparametric rate smoothing.** Sanderson (1997) chooses ages that minimize the squared differences of rates between adjacent branches, given the branch lengths of a tree without a clock.
- **Penalized likelihood.** Sanderson (2002), in the program r8s, as above.
- **Bayesian MCMC.** Thorne, Kishino and Painter (1998) with autocorrelated rates; MCMCTree in PAML (Yang 2007) with soft bounds; BEAST (Drummond et al. 2006) with uncorrelated rates and an unknown tree. These sample the ages, the rates and the parameters of the [tree prior](/birth-death-process/) together, by [Bayesian inference](/bayesian-phylogenetic-inference/).

## Bounds

The limits are statistical, not computational. By the theorem above, no method can identify ages without a calibration. Under a strict clock with one fixed calibration, the maximum likelihood ages converge to the true ages as $m \to \infty$. Under a relaxed clock, the rate of each branch is a free parameter tied only by its prior, so even with unlimited sequence data the uncertainty in the ages does not shrink to zero: it is bounded below by the uncertainty in the calibrations and by the spread of the rates. Each likelihood evaluation costs $O(n m s^2)$ for $n$ taxa, $m$ sites and $s$ states by [Felsenstein pruning](/felsenstein-pruning/), and the number of evaluations of an optimizer or MCMC run has no useful general bound.

## Reductions

- **Strict clock to ultrametric fitting.** With a clock and branch lengths known, dating is the fit of an [ultrametric](/ultrametric/) to the tree and one scaling.
- **Dating to constrained optimization.** With the topology fixed, likelihood dating maximizes a smooth function over the polytope of ages with $t_u > t_v$ on each branch and the calibration bounds.
- **Rooting.** A clock places the root, so a dating method that is given an unrooted tree also chooses its root, as in [tree rooting](/tree-rooting/).

## Applications

- **Timescales of evolution.** The ages of the splits of major groups, such as the families of mammals or flowering plants, from fossil calibrations.
- **Epidemics.** The date of the common ancestor of a virus outbreak, from the sampling dates of the sequences, with coalescent tree priors such as the [Kingman coalescent](/kingman-coalescent/).
- **Rates of speciation.** Dated trees feed [birth-death](/birth-death-process/) and [Yule](/yule-model/) models of diversification.
- **Biogeography.** Ages of splits are compared with the dates of events such as the opening of an ocean or the rise of a mountain range.

## References
