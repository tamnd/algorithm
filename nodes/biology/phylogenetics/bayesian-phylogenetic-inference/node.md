---
tag: SBJ5QF
kind: technique
slug: bayesian-phylogenetic-inference
name: Bayesian phylogenetic inference
aliases:
- MCMC phylogenetics
area: biology/phylogenetics
level: advanced
summary: Put a prior on trees, branch lengths and model parameters, and sample their posterior given the alignment with a Markov chain Monte Carlo walk that changes the tree by local moves.
prereqs: [phylogenetic-likelihood, metropolis-hastings, nearest-neighbor-interchange]
see_also: [maximum-likelihood-phylogeny, phylogenetic-bootstrap, parallel-tempering, majority-rule-consensus, effective-sample-size, marginal-likelihood, divergence-time-estimation, reversible-jump-mcmc]
sources:
  - paper: doi:10.1007/BF02338839
    title: Bruce Rannala and Ziheng Yang, Probability distribution of molecular evolutionary trees, a new method of phylogenetic inference, Journal of Molecular Evolution 43(3), 1996, 304-311
    locator: the posterior probability of a tree under a birth-death prior, computed by numerical integration for small trees
  - paper: doi:10.1093/oxfordjournals.molbev.a025811
    title: Ziheng Yang and Bruce Rannala, Bayesian phylogenetic inference using DNA sequences, a Markov chain Monte Carlo method, Molecular Biology and Evolution 14(7), 1997, 717-724
    locator: an MCMC sampler of the posterior of rooted trees under a birth-death prior, for DNA sequences
  - paper: doi:10.1111/j.0006-341X.1999.00001.x
    title: Bob Mau, Michael A. Newton and Bret Larget, Bayesian phylogenetic inference via Markov chain Monte Carlo methods, Biometrics 55(1), 1999, 1-12
    locator: MCMC over clock trees with a proposal that changes the topology and the node times together
  - paper: doi:10.1093/oxfordjournals.molbev.a026160
    title: Bret Larget and Donald L. Simon, Markov chain Monte Carlo algorithms for the Bayesian analysis of phylogenetic trees, Molecular Biology and Evolution 16(6), 1999, 750-759
    locator: the LOCAL move for unrooted trees and the Hastings ratio of the proposals
  - paper: doi:10.1093/bioinformatics/17.8.754
    title: John P. Huelsenbeck and Fredrik Ronquist, MRBAYES, Bayesian inference of phylogenetic trees, Bioinformatics 17(8), 2001, 754-755
    locator: the program MrBayes, with Metropolis-coupled MCMC over trees
  - paper: doi:10.1093/sysbio/sys029
    title: Fredrik Ronquist et al., MrBayes 3.2, efficient Bayesian phylogenetic inference and model choice across a large model space, Systematic Biology 61(3), 2012, 539-542
    locator: convergence diagnostics across runs and model choice by marginal likelihoods
  - paper: doi:10.1186/1471-2148-7-214
    title: Alexei J. Drummond and Andrew Rambaut, BEAST, Bayesian evolutionary analysis by sampling trees, BMC Evolutionary Biology 7, 2007, 214
    locator: the program BEAST, which samples rooted time trees under clock, coalescent and speciation models
  - paper: doi:10.1093/biomet/57.1.97
    title: W. K. Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970, 97-109
    locator: the acceptance probability with the ratio of proposal densities
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 18, Bayesian inference of phylogenies
  - book: isbn:9780199602605
    title: Ziheng Yang, Molecular Evolution, a Statistical Approach, Oxford University Press, 2014
    locator: Chapter 7, Bayesian computation (MCMC), and Chapter 8, Bayesian phylogenetics
---

Bayesian phylogenetic inference treats the tree as an unknown with a prior distribution. Given an alignment $D$, [Bayes' theorem](/bayes-theorem/) gives the posterior over the topology $\tau$, the branch lengths $\mathbf b$ and the model parameters $\theta$:
$$P(\tau, \mathbf b, \theta \mid D) = \frac{P(D \mid \tau, \mathbf b, \theta)\, P(\tau, \mathbf b, \theta)}{P(D)}.$$
The likelihood $P(D \mid \tau, \mathbf b, \theta)$ is the [phylogenetic likelihood](/phylogenetic-likelihood/), computed by [Felsenstein pruning](/felsenstein-pruning/). The normalizer $P(D)$ is a sum over $(2n-5)!!$ topologies of an integral over the branch lengths, which no one can compute for real data. So programs sample the posterior instead, with a [Metropolis-Hastings](/metropolis-hastings/) chain that changes the topology by local moves such as [NNI](/nearest-neighbor-interchange/) and changes the numbers by small steps. The fraction of samples whose tree contains a split estimates the posterior probability of that split. Yang and Rannala (1997), Mau, Newton and Larget (1999) and Larget and Simon (1999) gave early samplers, and MrBayes (Huelsenbeck and Ronquist 2001) and BEAST (Drummond and Rambaut 2007) made the method common.

## In plain words

Maximum likelihood looks for the one tree that explains the data best. The Bayesian method asks a different question: given the data and what we believed before, how probable is each tree? The answer is a probability for every tree, not a single tree.

There are far too many trees to score them all. So the method takes a random walk. It starts from some tree and, at each step, proposes a small change: swap two branches, or make one branch longer or shorter. If the change makes the data more probable, it takes it. If not, it takes it only some of the time, with a chance that shrinks the worse the change is. After a long walk, the walk spends time on each tree in proportion to that tree's probability. Count how often each branch grouping appears, and you have its probability.

## When it applies

The model is $n$ taxa with $m$ aligned sites, of DNA, protein or binary characters, and an explicit substitution model such as the [Jukes-Cantor model](/jukes-cantor-model/). Trees are unrooted binary trees for time-reversible models without a clock, or rooted trees with node ages under a [molecular clock](/molecular-clock/). The method needs three things: a likelihood, a prior on every unknown, and proposals that can reach every state. The chain explores the $(2n-5)!!$ topologies by local moves, so for large $n$ a run is a heuristic sample: a chain can stay in one region of tree space for longer than the run.

Common priors are uniform on topologies, or a [Yule](/yule-model/) or [birth-death](/birth-death-process/) prior on rooted trees; independent exponential priors on unrooted branch lengths; and Dirichlet or gamma priors on rates and frequencies. The posterior answers questions that a point estimate cannot, such as the probability of a clade with all other unknowns averaged out, and it carries the uncertainty of the tree into later steps such as [divergence time estimation](/divergence-time-estimation/).

## The template

A state is $x = (\tau, \mathbf b)$ with any model parameters added. The holes are the proposal $q(x' \mid x)$ and the prior $P(x)$. With $u$ uniform in $[0, 1)$, the acceptance test is the Metropolis-Hastings rule
$$\alpha(x, x') = \min\Bigl(1,\ \frac{P(D \mid x')\, P(x')\, q(x \mid x')}{P(D \mid x)\, P(x)\, q(x' \mid x)}\Bigr).$$

```pseudo id=main
PHYLO-MCMC(D, start, N, burn, rng)
L1  x ← (start, every branch length set to its first value); λ ← log P(D | x)
L2  for step = 0, 1, ..., N - 1 do
L3      x' ← PROPOSE(x): an NNI with probability 1/2, else a new value of one branch length
L4      λ' ← log P(D | x')
L5      if u < α(x, x') then
L6          (x, λ) ← (x', λ')
L7      if step ≥ burn then add 1 to the count of the topology of x
L8  return each count divided by N - burn
```

The code uses a small model on purpose, so that the exact posterior can be found by listing all states: JC69, a uniform prior on topologies, and each of the $2n - 3$ branch lengths uniform on the two values 0.05 and 0.3. The NNI proposal picks one of the $n - 3$ internal edges and one of its 2 interchanges; it keeps every branch length, and the central branch keeps its length under its new split. The length proposal picks one of the $2n - 3$ branches and its other value. Both proposals are symmetric, $q(x' \mid x) = q(x \mid x')$, and the prior is uniform, so $\alpha$ is the likelihood ratio capped at 1.

**Why the chain samples the posterior.** Write $\pi(x) = P(x \mid D)$. For $x \ne x'$, the chain moves from $x$ to $x'$ with probability $q(x' \mid x)\, \alpha(x, x')$, and
$$\pi(x)\, q(x' \mid x)\, \alpha(x, x') = \min\bigl(\pi(x)\, q(x' \mid x),\ \pi(x')\, q(x \mid x')\bigr),$$
which is symmetric in $x$ and $x'$. So the chain satisfies [detailed balance](/detailed-balance/) with respect to $\pi$, and $\pi$ is a [stationary distribution](/stationary-distribution/). NNI moves connect all binary topologies, and length moves connect all length vectors, so the chain is irreducible; rejections make it aperiodic. Then the fraction of steps spent on each topology tends to its posterior probability as $N \to \infty$.

**Cost.** One step costs one proposal, $O(n)$ for a local move with good data structures and $O(n^2)$ in the simple code, and one likelihood. With $s$ states per site, a full pruning pass costs $O(n m s^2)$. A local move changes the partial likelihoods only on the path from the change to the root, so programs update $O(d\, m s^2)$ values, where $d$ is the depth of the changed vertex. A run of $N$ steps then costs $O(N n m s^2)$ in the worst case. The number of steps needed is set by the [mixing time](/mixing-time/), which has no useful general bound.

## Classic examples

**Five taxa, exact against MCMC.** Take A = ACGTTA, B = ACGTTG, C = ACATCG, D = GCATTG and E = GTATCG. The model above has $15 \times 2^7 = 1920$ states, and the exact posterior of each topology is the sum of the likelihoods of its 128 length vectors, divided by the total. Start the chain at $((A,E),D,(B,C))$, which has posterior 0.003, and run it with `random.Random(12345)`.

| topology | exact | 2000 steps | 10000 steps | 60000 steps |
|---|---|---|---|---|
| $((A,B),C,(D,E))$ | 0.3762 | 0.3744 | 0.3564 | 0.3843 |
| $((A,B),D,(C,E))$ | 0.3762 | 0.3894 | 0.3875 | 0.3715 |
| $((A,B),E,(C,D))$ | 0.0745 | 0.0767 | 0.0685 | 0.0750 |
| total variation distance to the exact | | 0.031 | 0.037 | 0.012 |

The first run discards 200 steps as [burn-in](/burn-in/) and the others discard 2000. The distance at 10000 steps is larger than at 2000 steps: with a few thousand correlated samples, the error is mostly chance. The test asserts a distance below 0.03 at 60000 steps.

The posterior probability of the split AB | CDE is 0.827. The splits DE | ABC and CE | ABD have 0.449 each, since the data cannot decide between them. Two states share the highest likelihood, $\log L = -29.998$: in both, the branches to B, C and D have length 0.05 and the other branches 0.3. A single maximum likelihood tree would show one of the two topologies; the posterior shows that the data are split between them.

**MrBayes.** Huelsenbeck and Ronquist (2001) run several chains at once, all but one heated so that they cross valleys of the posterior, and swap states between them. This is Metropolis-coupled MCMC, a form of [parallel tempering](/parallel-tempering/). MrBayes 3.2 (Ronquist et al. 2012) runs two or more independent analyses and compares their split frequencies to check convergence.

**BEAST.** Drummond and Rambaut (2007) sample rooted trees whose node heights are ages, under strict or [relaxed clocks](/relaxed-molecular-clock/), with coalescent or birth-death tree priors. The output is a sample of dated trees.

**Clock trees.** Mau, Newton and Larget (1999) sampled clock trees by a move that changes the topology and the node times together.

## Variations

- **Integrating parameters.** Sample the parameters of the substitution model and the rate heterogeneity along with the tree, so that the split probabilities average over them.
- **Different moves.** NNI, SPR and TBR-type moves, the LOCAL move of Larget and Simon (1999), and multipliers on branch lengths. Moves that change the number of parameters, as between models, need [reversible jump MCMC](/reversible-jump-mcmc/).
- **Model choice.** Compare models by their [marginal likelihoods](/marginal-likelihood/) $P(D)$, estimated by stepping-stone or path sampling.
- **Summary of the sample.** Report the [majority-rule consensus](/majority-rule-consensus/) of the sampled trees with the posterior probability on each split, or the tree in the sample with the highest product of its split probabilities.

## Pitfalls

- **Convergence.** A chain that has not converged gives wrong probabilities with no warning. Run several chains from different starts, compare their split frequencies, check the [effective sample size](/effective-sample-size/) of each parameter, and check the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) where it applies.
- **Posterior probability is not bootstrap support.** The two numbers answer different questions, and the posterior is often higher. A split with posterior 0.95 and [bootstrap](/phylogenetic-bootstrap/) support 70 is a common sight.
- **Short internal branches.** When the true internal branch is very short, the posterior can still put a high probability on one resolution, the star tree paradox.
- **Branch length priors.** The prior on branch lengths has a strong effect on the total tree length and can change the split probabilities. An exponential prior with a mean far from the data can give trees that are much too long.
- **Harmonic mean estimator.** The marginal likelihood estimated by the harmonic mean of the sampled likelihoods is unstable and biased; use stepping-stone or path sampling.
- **Asymmetric proposals.** A move whose reverse has a different probability, such as a multiplier on a branch length, needs the Hastings ratio. Leaving it out samples the wrong distribution.

## Exercises

1. Check by hand that the NNI proposal of the code is symmetric: the reverse NNI of a move exists, and it has the same probability.
2. With a uniform prior on 15 topologies and only the topology unknown (branch lengths fixed), write the posterior of each topology in terms of the 15 likelihoods.
3. Show that the chain with only NNI moves is irreducible on topologies, using the fact that NNI connects all binary trees.
4. A proposal multiplies one branch length $b$ by $e^{\lambda (u - 1/2)}$ for $u$ uniform in $[0, 1)$. Show that its Hastings ratio is $b'/b$.
5. In the five-taxon example, explain why DE | ABC and CE | ABD have the same posterior, by looking at the sites.

## References
