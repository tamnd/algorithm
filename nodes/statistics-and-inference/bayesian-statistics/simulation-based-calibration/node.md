---
tag: GB2WNE
kind: algorithm
slug: simulation-based-calibration
name: Simulation-based calibration
aliases:
- SBC
area: statistics-and-inference/bayesian-statistics
level: research
summary: Checks a Bayesian sampler by drawing parameters from the prior, simulating data, and testing that the rank of the true parameter among posterior draws is uniform.
model: real-ram
complexity:
  vars: {N: the number of replications, L: the number of posterior draws per replication, S: the cost of one simulation of data, C: the cost of one run of the sampler under test}
  time: {worst: Θ(N (S + C + L))}
  space: {extra: Θ(L)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Sean Talts, Michael Betancourt, Daniel Simpson, Aki Vehtari, Andrew Gelman, Samantha R. Cook, Donald B. Rubin]
  note: Cook, Gelman and Rubin (2006) validated Bayesian software by checking that posterior quantiles of the true parameter are uniform. Talts, Betancourt, Simpson, Vehtari and Gelman (2018) replaced the quantiles by ranks among posterior draws, which have an exactly uniform law, and added thinning for Markov chains.
prereqs: [bayesian-inference, bayes-theorem, uniform-distribution, chi-squared-goodness-of-fit-test, effective-sample-size]
see_also: [posterior-predictive-check, approximate-bayesian-computation, kolmogorov-smirnov-test, autocorrelation, gelman-rubin-diagnostic, hamiltonian-monte-carlo, variational-inference, metropolis-hastings]
sources:
  - paper: "arXiv:1804.06788"
    title: "Sean Talts, Michael Betancourt, Daniel Simpson, Aki Vehtari and Andrew Gelman, Validating Bayesian inference algorithms with simulation-based calibration, 2018"
    locator: "Section 4.1 and Algorithm 1 (rank statistics and the SBC histogram), Section 4.2 (U shape for posteriors that are too narrow, hump for too wide, skew for bias), Section 5.1 and Algorithm 2 (thinning a Markov chain by its effective sample size), Appendix B (proof of Theorem 1)"
  - paper: doi:10.1198/106186006X136976
    title: "Samantha R. Cook, Andrew Gelman and Donald B. Rubin, Validation of software for Bayesian models using posterior quantiles, Journal of Computational and Graphical Statistics 15(3), 2006"
    locator: "pages 675 to 692: posterior quantiles of the true parameter are uniform for correct software (general locator)"
  - paper: doi:10.1080/10618600.2017.1377082
    title: "Andrew Gelman, Correction to Cook, Gelman and Rubin (2006), Journal of Computational and Graphical Statistics, 2017"
    locator: "the dependence created by autocorrelated draws changes the law of the test statistics of the 2006 paper (general locator)"
---

Simulation-based calibration (SBC) checks that a Bayesian computation is correct, using only the ability to sample from the prior and to simulate data. It repeats one experiment $N$ times: draw a parameter $\tilde\theta$ from the prior, simulate data $\tilde y$ from it, run the method under test on $\tilde y$ to get $L$ posterior draws, and record the rank of $f(\tilde\theta)$ among the $L$ values $f(\theta_l)$ for a chosen function $f$. Given $\tilde y$, the true parameter is itself a draw from the exact posterior, so if the method returns independent exact posterior draws, the rank is uniform on $\{0, 1, \ldots, L\}$. A histogram of the $N$ ranks that is not flat shows an error, and its shape shows which kind: a U shape for posteriors that are too narrow, a hump for posteriors that are too wide, and a slope for a bias.

## In plain words

You have a program that claims to compute the answer to a Bayesian question, and you want to know whether it is right without knowing the right answer. Make up a true value the way the model says values arise, make fake data from it, and ask the program for a sample of plausible values. If the program is right, the true value looks like just one more member of that sample. So it is equally likely to land at any position when you sort the sample: lowest, highest, or anywhere between. Repeat this many times and count the positions. A flat count is what a correct program gives. Too many lowest and highest positions mean the program is too sure of itself; too few mean it is not sure enough; a lean to one side means it is biased.

## The problem

**Input.** A prior $\pi(\theta)$ to draw from; a simulator of data $y \sim p(y \mid \theta)$; the method under test, which given data $y$ returns $L$ draws meant to come from the posterior $\pi(\theta \mid y)$; a real function $f$ of the parameter, such as one coordinate; the number of replications $N$.

**Output.** The counts of the ranks $0, \ldots, L$ over the $N$ replications, and a test of their uniformity.

**What the test can show.** Uniform ranks are necessary for a correct method, not sufficient. They test that the computed posterior is calibrated on average over the prior and the data, not that it is right for every data set.

## The algorithm

```pseudo id=main
SBC(π, SIMULATE, SAMPLER, f, N, L)
L1  counts[0..L] ← 0
L2  for n ← 1 to N
L3      θ̃ ← a draw from the prior π
L4      ỹ ← SIMULATE(θ̃)
L5      θ₁..θ_L ← SAMPLER(ỹ, L)                        ▷ the method under test
L6      r ← #{l : f(θ_l) < f(θ̃)} + U{0..#{l : f(θ_l) = f(θ̃)}}   ▷ ties broken at random
L7      counts[r] ← counts[r] + 1
L8  return counts                                       ▷ uniform on 0..L if SAMPLER is correct
```

L3 and L4 draw $(\tilde\theta, \tilde y)$ from the joint law of the model. The joint density $\pi(\theta)p(y \mid \theta)$ equals $p(y)\pi(\theta \mid y)$, so $\tilde y$ is a draw from the prior predictive law and, given $\tilde y$, $\tilde\theta$ is a draw from the exact posterior. L5 runs the method on $\tilde y$. L6 computes the rank. The term $U\{0..e\}$, a uniform integer up to the number $e$ of ties, matters only when $f(\theta)$ can take repeated values, for example with a discrete parameter. L8 returns the counts; the usual test is Pearson's [chi-squared test](/chi-squared-goodness-of-fit-test/) against equal expected counts, often after merging the $L + 1$ ranks into $B$ equal bins, together with a plot of the histogram.

**Markov chain samplers.** If L5 runs a Markov chain, its draws are correlated, and correlated draws give a U-shaped histogram even when the chain targets the right law. Talts and coauthors (2018) run a longer chain and keep every $T$-th state, with $T$ the chain length divided by its [effective sample size](/effective-sample-size/), so that about $L$ nearly independent draws remain.

## Example

**Model.** $\theta \sim N(0, 1)$ and $y_1, \ldots, y_5 \sim N(\theta, 1)$, so the posterior is $N(\sum y_i/6, 1/6)$, with standard deviation $0.408$. The function is $f(\theta) = \theta$.

**Trace.** Six replications with $L = 4$ exact posterior draws, from `random.Random(3)`:

| $n$ | $\tilde\theta$ | posterior mean | the 4 draws, sorted | rank |
|---|---|---|---|---|
| 1 | 0.095 | 0.211 | 0.193, 0.275, 0.508, 0.986 | 0 |
| 2 | 1.127 | 0.735 | 0.071, 0.120, 0.192, 0.638 | 4 |
| 3 | $-0.172$ | $-0.382$ | $-1.204$, $-0.727$, $-0.545$, $-0.075$ | 3 |
| 4 | $-0.504$ | $-1.073$ | $-1.200$, $-0.939$, $-0.885$, $-0.857$ | 4 |
| 5 | 1.045 | 0.461 | $-0.302$, 0.015, 0.141, 0.898 | 4 |
| 6 | $-0.953$ | $-1.362$ | $-2.173$, $-1.661$, $-0.925$, $-0.686$ | 2 |

Each rank is between $0$ (the truth is below all draws) and $4$ (above all). Six ranks say little; uniformity shows only over many replications.

**Correct and wrong samplers.** $N = 1000$ replications with $L = 20$ draws, from `random.Random(7)`. The $21$ ranks are merged into $7$ bins of $3$; a flat histogram has $142.9$ per bin. The $p$-value is from the chi-squared test on all $21$ ranks ($20$ degrees of freedom).

| sampler | counts in 7 bins | $p$-value | shape |
|---|---|---|---|
| exact posterior | 140, 147, 139, 160, 122, 150, 142 | 0.69 | flat |
| standard deviation $\times 0.6$ | 254, 111, 85, 100, 104, 99, 247 | $3 \times 10^{-79}$ | U |
| standard deviation $\times 1.5$ | 66, 134, 190, 228, 175, 148, 59 | $2 \times 10^{-28}$ | hump |
| mean $+ 0.5$ standard deviations | 277, 187, 175, 112, 101, 89, 59 | $4 \times 10^{-46}$ | falling |
| the prior, ignoring the data | 147, 142, 135, 155, 135, 141, 145 | 0.25 | flat |
| exact Markov chain, $\rho = 0.9$ | 292, 90, 119, 76, 82, 81, 260 | $3 \times 10^{-190}$ | U |
| the same chain, every 19th state | 149, 128, 140, 154, 149, 127, 153 | 0.41 | flat |

When the draws are too narrow, the truth often falls outside them, so ranks $0$ and $20$ are common. When they are too wide, the truth sits in their middle. When they are shifted up, the truth tends to be below them. The prior sampler passes, although it ignores the data: the truth and the draws are then independent draws from the prior, so the rank is uniform. The Markov chain has the exact posterior as its stationary law, and its first state is an exact draw, but with lag-one correlation $0.9$ its $20$ consecutive states cluster, and the truth falls outside the cluster too often. The effective sample size of such a chain is $n(1 - \rho)/(1 + \rho) = n/19$, so keeping every $19$th state of a chain of length $380$ restores a flat histogram.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **The truth is a posterior draw.** Given $\tilde y$, $\tilde\theta$ has the law $\pi(\theta \mid \tilde y)$, by [Bayes' theorem](/bayes-theorem/).
2. **Uniform ranks.** If the method returns $L$ independent draws from the exact posterior and $f(\theta)$ has no atoms, the rank is uniform on $\{0, \ldots, L\}$. The $L + 1$ values are exchangeable given $\tilde y$, so the truth is equally likely to hold each position.
3. **Ties.** With random tie breaking, as in L6, the rank is uniform with no condition on atoms; the plain count of smaller values is not, since rank $0$ is then too likely.
4. **What is tested.** With a continuous computed posterior distribution function $G_y$, the rank is binomial$(L, u)$ given $u = G_{\tilde y}(f(\tilde\theta))$, and the ranks are uniform for every $L$ exactly when $u$ is Uniform(0, 1). This explains the shapes and why the prior sampler passes.

What is proved and what is only measured: claims 1 to 4 are exact, and the tests check claim 3 and the prior sampler in exact rational arithmetic on discrete models. The chi-squared law of the test statistic is a large-sample approximation. With Markov chain draws none of the claims apply; the effect of thinning in the table is measured only.

**A correction.** Theorem 1 of Talts and coauthors (2018) states uniformity of the plain rank for any one-dimensional function. It needs the condition of claim 2: a constant $f$, or a discrete parameter, gives ties, and the plain rank is then not uniform. The randomized rank of L6 removes the condition.

## Complexity

Each replication makes one prior draw, one simulation of cost $S$, one run of the method of cost $C$, and $L$ comparisons, so the total time is $\Theta(N(S + C + L))$. The run of the method is usually the dominant cost, since it is a full posterior computation; SBC costs $N$ times one analysis. The replications are independent and run in parallel. With a Markov chain thinned by $T$, $C$ includes $TL$ chain steps. The memory is the $L$ draws of one replication and the $L + 1$ counts, $\Theta(L)$.

How many replications are needed: under uniformity each count is binomial$(N, 1/(L+1))$, with relative spread $\sqrt{L/N}$. To see a $10$ percent excess in a bin of $1/B$ of the ranks with a few standard errors, $N$ must be in the thousands, which is why moderate $N$ catches only clear errors.

## Properties

- **Randomized.** The counts and the $p$-value vary with the seed; a correct method fails the test at level $\alpha$ in a fraction $\alpha$ of runs.
- **Needs no exact posterior.** Only prior draws and data simulation are required, so it checks methods for models where no other reference exists.
- **Checks one function at a time.** A separate histogram is needed for each coordinate or function $f$, and errors that affect only the dependence between coordinates can pass all of them.
- **Necessary, not sufficient.** It checks calibration averaged over the prior predictive law. The prior sampler passes, and a method that is wrong for some data sets and wrong in the other direction for others can pass.
- **Diagnostic shapes.** The histogram shows the kind of error, not only its presence.

## Variants and improvements

- **Posterior quantiles.** Cook, Gelman and Rubin (2006) used the quantile of the truth among the draws, transformed to the normal scale, and combined the results across parameters. With finite $L$ the quantile is discrete, so its law is not exactly uniform; ranks remove that problem.
- **Bins.** Merge the $L + 1$ ranks into $B$ bins of equal size, with $B$ dividing $L + 1$, to stabilize the counts.
- **Tests on the empirical distribution function.** Compare the empirical distribution function of the normalized ranks $r/(L+1)$ with the uniform one, for example by a [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) or simultaneous confidence bands; these are more powerful than the histogram for smooth departures.
- **Data-dependent test quantities.** Taking $f$ to depend on the data as well, such as the log-likelihood of $\tilde y$ at $\theta$, can reveal errors that every coordinate misses (Modrák and coauthors 2023).
- **Amortized methods.** For neural posterior estimators and other likelihood-free methods, such as [approximate Bayesian computation](/approximate-bayesian-computation/), each replication is cheap once the method is trained, so SBC with large $N$ is a standard check.

## When to use it

Use SBC when you write a new sampler, a new model implementation, or an approximate method such as [variational inference](/variational-inference/) or ABC, and want evidence that it computes the posterior it should. It finds coding errors in the model, wrong priors in the sampler, and approximations that are systematically too narrow or too wide. For a single data set and an exact-in-principle sampler such as [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/), convergence checks such as the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) are cheaper; SBC checks the method over the whole prior. To check the model against real data, use a [posterior predictive check](/posterior-predictive-check/) instead: SBC assumes the model is true.

## Pitfalls

- **Autocorrelated draws.** Taking $L$ consecutive states of a Markov chain in L5 gives a U-shaped histogram even for a correct chain; in the example, $p = 3 \times 10^{-190}$. Thin the chain to about $L$ effective draws.
- **Plain ranks with ties.** Counting only the smaller values in L6 when $f(\theta)$ has atoms makes rank $0$ too likely, which looks like an error of the method. Break ties at random.
- **Drawing the truth from a different prior.** If L3 draws from a prior other than the one the method uses, the truth is no longer a posterior draw, and correct methods fail. Use the same prior in both places, or use SBC exactly to detect such a mismatch.
- **Reading a flat histogram as proof.** The prior sampler gives flat ranks in the example. A flat histogram from L8 says the method is calibrated on average, not that it uses the data correctly; compare also the posterior spread with the prior spread.
- **Too few replications.** With $N$ of a few hundred, the histogram of L8 is noisy, and only large errors are visible. Choose $N$ in the thousands for subtle errors, and use the same seed scheme to reproduce failures.
- **Priors that are too wide.** Very wide priors in L3 simulate extreme data sets on which the method fails for numerical reasons that never matter in practice. Use the prior of the actual analysis, and inspect failing replications.

## Implementations

## History

Geweke (2004) tested posterior simulators by comparing two ways of drawing from the joint law of parameters and data. Cook, Gelman and Rubin (2006) proposed to validate Bayesian software by simulating parameters from the prior and data from the model, and checking that the posterior quantiles of the true parameters are uniform. Gelman (2017) published a correction noting that dependence between draws changes the law of their test statistics. Talts, Betancourt, Simpson, Vehtari and Gelman (2018) replaced the quantiles by rank statistics, whose law is exactly uniform for independent draws, interpreted the shapes of the rank histogram, and gave a thinning rule for Markov chains. SBC is now a standard check in probabilistic programming and in simulation-based inference.

## References
