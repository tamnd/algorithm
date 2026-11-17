---
tag: YHHCY9
kind: algorithm
slug: epidemic-data-augmentation-mcmc
name: Data augmentation MCMC for epidemics
aliases:
- O'Neill-Roberts data augmentation
area: biology/epidemic-and-ecological-models
level: research
summary: Infer infection rates from removal times by treating the unobserved infection times as latent variables updated by Metropolis-Hastings.
model: real-ram
complexity:
  vars: {n: the number of cases, M: the number of iterations, N: the population size}
  time: {worst: Θ(M n² log n), average: Θ(M n² log n), best: Θ(M n² log n)}
  space: {extra: Θ(M n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1999
  people: [Philip D. O'Neill, Gareth O. Roberts, Gavin J. Gibson, Eric Renshaw]
  note: Gibson and Renshaw (1998) and O'Neill and Roberts (1999) made the unobserved event times of a stochastic epidemic into extra unknowns of a Markov chain Monte Carlo sampler.
prereqs: [stochastic-sir-model, metropolis-hastings, gibbs-sampling, conjugate-prior]
see_also: [stochastic-sir-model, metropolis-hastings, gibbs-sampling, reversible-jump-mcmc, particle-filter, approximate-bayesian-computation, cori-rt-estimation, sir-epidemic-model]
sources:
  - paper: "Philip D. O'Neill and Gareth O. Roberts, Bayesian inference for partially observed stochastic epidemics, Journal of the Royal Statistical Society Series A 162(1), 1999"
    title: O'Neill and Roberts 1999
    locator: the infection times as missing data, the gamma full conditionals of the rates, the Metropolis-Hastings moves of single infection times, and reversible jump moves for unknown numbers of cases
  - paper: "Gavin J. Gibson and Eric Renshaw, Estimating parameters in stochastic compartmental models using Markov chain methods, IMA Journal of Mathematics Applied in Medicine and Biology 15, 1998"
    title: Gibson and Renshaw 1998
    locator: Markov chain Monte Carlo with the unobserved event times of a compartmental model as extra unknowns
  - paper: "Philip D. O'Neill, A tutorial introduction to Bayesian inference for stochastic epidemic models using Markov chain Monte Carlo methods, Mathematical Biosciences 180, 2002"
    title: O'Neill 2002
    locator: a worked account of the complete-data likelihood of the SIR model and of the data augmentation sampler
  - book: isbn:9780387950501
    title: Hakan Andersson and Tom Britton, Stochastic Epidemic Models and Their Statistical Analysis, Lecture Notes in Statistics 151, Springer, 2000
    locator: Chapter 2 (the standard SIR epidemic model) and the part on statistical inference for epidemic data
---

Data augmentation MCMC estimates the infection rate $\beta$ and the removal rate $\gamma$ of the [stochastic SIR model](/stochastic-sir-model/), the Markov form of the [SIR epidemic](/sir-epidemic-model/) and of the general [epidemic model](/epidemic-model/), from the times at which cases are removed, for example the dates of recovery, isolation or death. The infection times are not observed, and without them the likelihood has no closed form. The method adds them to the unknowns. Given all event times, the likelihood is simple, and $\beta$ and $\gamma$ have gamma full conditionals, so a [Gibbs](/gibbs-sampling/) step draws them exactly. Given the rates, a [Metropolis-Hastings](/metropolis-hastings/) step moves one infection time at a time. The chain targets the joint posterior of the rates and the infection times, so it also gives the posterior of $R_0 = \beta/\gamma$ and of who was infected when.

## In plain words

In an outbreak, health workers often record the day each sick person recovers or is isolated, but nobody sees the moment each person caught the disease. If we knew those moments, estimating how fast the disease spreads would be easy: count the infections and compare them with how much contact the sick had with the healthy.

So the method takes a guess at the hidden moments and improves it in a loop. With the current guess, it draws new values for the speed of spread and the speed of recovery. With these values, it picks one person and proposes a new moment of infection for that person. It keeps the proposal if it fits the model well, and it rejects every proposal that leaves somebody infected while nobody was sick. After many rounds, the values it visits show which speeds are plausible and how sure we can be.

## The problem

**Model.** A closed population of $N$ people follows the Markov SIR model: each susceptible is infected at rate $\beta I/N$, and each infectious person is removed at rate $\gamma$. One person starts the epidemic. The epidemic is over.

**Input.** The removal times $r_1, \ldots, r_n$ of the $n \ge 1$ people who were ever infected, and $N$. Priors $\beta \sim \operatorname{Gamma}(a_\beta, \text{rate } b_\beta)$ and $\gamma \sim \operatorname{Gamma}(a_\gamma, \text{rate } b_\gamma)$, independent, with a flat prior on the infection time of the first case. A number of iterations $M$.

**Output.** A sample $(\beta^{(m)}, \gamma^{(m)}, \mathbf i^{(m)})_{m=1}^{M}$ from a Markov chain whose invariant law is the joint posterior of $\beta$, $\gamma$ and the infection times $\mathbf i = (i_1, \ldots, i_n)$ given $\mathbf r$.

**The complete-data likelihood.** Let $I(t-)$ be the number infectious just before $t$, let $\kappa$ be the first case, and let
$$A = \int S(t) I(t)\, dt = \sum_{j=1}^{n} \sum_{k \ne j} \big(\min(r_j, i_k) - \min(i_j, i_k)\big), \qquad D = \sum_{j=1}^{n} (r_j - i_j),$$
where $k$ runs over all $N$ people and $i_k = \infty$ for a person who is never infected. Then
$$L(\beta, \gamma; \mathbf i, \mathbf r) = \Big(\frac{\beta}{N}\Big)^{n-1} \prod_{j \ne \kappa} I(i_j-)\ \gamma^n\, e^{-\beta A/N - \gamma D}$$
if $i_j < r_j$ for all $j$ and $I(i_j-) \ge 1$ for every $j \ne \kappa$, and $L = 0$ if not.

## The algorithm

```pseudo id=main
DA-MCMC(r[1..n], N, a_β, b_β, a_γ, b_γ, M)
L1  i ← all infections in [min r - 1, min r), in the order of r;  A ← A(i)
L2  for m ← 1 to M do
L3      β ← draw from Gamma(a_β + n - 1, rate b_β + A/N)
L4      γ ← draw from Gamma(a_γ + n, rate b_γ + Σ_j (r_j - i_j))
L5      repeat n times: j ← uniform in {1, …, n}
L6          i′ ← i with i′_j ← r_j - E, where E ← draw from Exp(γ)
L7          if i′ is valid and log U < Σ log I′(i′_k-) - Σ log I(i_k-) - β (A(i′) - A(i)) / N then i ← i′, A ← A(i′)
L8      record (β, γ, i)
```

Line L1 gives a valid start: every case is infected before anybody is removed, so the first case is still infectious at every later infection. Line L6 is an independence proposal: it does not depend on the current $i_j$, and it draws the infectious period of case $j$ from its law under the model. For this reason the factor $\gamma^n e^{-\gamma D}$ cancels in the acceptance ratio of line L7, and only the infection term and the pressure $A$ remain. The change of $A$ comes from the $O(n)$ pair terms that involve case $j$, and the infection term comes from one sorted sweep over the $2n$ event times, which also finds a proposal where somebody is infected while nobody is infectious. The implementation draws in the order: two gamma draws, then for each update the case, the exponential time and the uniform.

## Example

**An exact check.** Take $N = 3$ and two cases with removal times $r_1 = 1$ and $r_2 = 2.5$, and the priors $\operatorname{Gamma}(3, \text{rate } 2)$ for both rates. If we integrate the rates out, the posterior of the infection times is proportional to $\prod_{j \ne \kappa} I(i_j-)\,(b_\beta + A/N)^{-(a_\beta + n - 1)}(b_\gamma + D)^{-(a_\gamma + n)}$. A grid of $500 \times 500$ points gives the posterior means $E[r_1 - i_1] = 0.6937$ and $E[r_2 - i_2] = 2.1937$, and the probability $0.4999$ that case 2 was infected first. A run of 40000 iterations from seed 20261118 gives $0.6967 \pm 0.0072$, $2.1953 \pm 0.0119$ and $0.4968 \pm 0.0056$, where each $\pm$ is one standard error from 40 batch means. The test does the same with 30000 iterations.

**A simulated outbreak.** The implementation also simulates a labelled epidemic. With $N = 30$, $\beta = 2$, $\gamma = 1$, so $R_0 = 2$ is above the [epidemic threshold](/epidemic-threshold/), and seed 3, one case at time 0 leads to $n = 24$ cases, and the last removal is at time 5.689. The sampler gets only the 24 removal times. With the priors $\operatorname{Gamma}(1, \text{rate } 1)$ for both rates, seed 1, 1500 iterations and the first 300 discarded:

| quantity | true value | posterior mean | 95% credible interval |
|---|---|---|---|
| $\beta$ | 2 | 2.163 | [1.188, 3.520] |
| $\gamma$ | 1 | 1.060 | [0.601, 1.837] |
| $R_0 = \beta/\gamma$ | 2 | 2.139 | [1.128, 3.572] |

The intervals are wide, because 24 cases carry little information. With seed 7 the outbreak has 27 cases, and the posterior mean of $R_0$ is 2.73 with the interval [1.48, 4.75].

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The likelihood is the density of a path of a Markov chain: the product of the rates of the events that happen, $\beta I(i_j-)/N$ for each infection after the first and $\gamma$ for each removal, times $\exp$ of minus the integral of the total rate $\beta S I/N + \gamma I$. Since $\int I\, dt = D$ and $\int S I\, dt = A$, this gives $L$. As a function of $\beta$ and $\gamma$, $L$ times the priors is a product of two gamma kernels, so lines L3 and L4 are exact Gibbs draws. Lines L5 to L7 are a Metropolis-Hastings step for $\mathbf i$ given the rates, with the proposal density $\gamma e^{-\gamma(r_j - i_j')}$. The proposal ratio cancels the factor $e^{-\gamma D}$, so the acceptance ratio is the expression in line L7, and an invalid proposal has $L = 0$ and is rejected. Each step leaves the joint posterior invariant, and so does the sweep. The chain is irreducible on the valid vectors, because it can move any case earlier than all others, and from a state where all infections come before the first removal it can reach every such state.

## Complexity

One update of an infection time costs $O(n)$ for the pair terms and $O(n \log n)$ for the sorted sweep. One iteration has $n$ updates and costs $\Theta(n^2 \log n)$, so $M$ iterations cost $\Theta(M n^2 \log n)$. The $N - n$ people who are never infected enter only through the count $N - n$, so the cost does not grow with $N$. The chains of $\beta$, $\gamma$ and $\mathbf i$ take $\Theta(M n)$ space, and the working state takes $\Theta(n)$. A balanced tree over the event times would make the infection term $O(\log n)$ to update, but the pair terms of $A$ stay $O(n)$.

## Properties

- **Exact in the limit, not for finite runs.** The invariant law is the exact posterior, with no approximation of the likelihood. The error of a finite run depends on how fast the chain mixes, and the successive values are correlated. Report the [effective sample size](/effective-sample-size/), not the number of iterations.
- **Conjugate rates.** Gamma priors on the rates are [conjugate](/conjugate-prior/) for the complete-data likelihood, so the rates need no tuning and no rejection.
- **No tuning of the proposal.** The proposal for an infection time uses the current $\gamma$, so its scale follows the posterior. Its acceptance rate falls when the infection times are tightly fixed by the data, for example in a large outbreak with short infectious periods.
- **Rates mix slowly when infection times do.** $\gamma$ given $\mathbf i$ is sharply fixed by $D$, and $D$ moves only by one infection time at a time. So $\gamma$ and the infection times are strongly correlated in the chain.
- **The posterior of $R_0$ comes for free.** Each recorded pair gives a draw of $\beta/\gamma$, so its [credible interval](/credible-interval/) needs no extra work.

## Variants and improvements

- **Epidemics that are not over.** If observation stops at a time $T$, some cases are infected but not yet removed, and their number is unknown. [Reversible jump](/reversible-jump-mcmc/) moves add and remove such cases. O'Neill and Roberts gave this in the same paper. This page does not implement it.
- **Other infectious periods.** For a gamma or fixed infectious period, $D$ is replaced by the log density of each period, the rate $\gamma$ loses its gamma conditional, and a random-walk step on it is used. The proposal for $i_j$ then draws from the period law.
- **Block and joint moves.** Moving several infection times at once, or moving $\gamma$ together with all periods by a common scale factor, reduces the correlation between $\gamma$ and $\mathbf i$.
- **Non-centred parametrisations.** Writing each period as $E_j/\gamma$ with $E_j$ standard exponential makes $\gamma$ and the $E_j$ less dependent in some data sets.
- **Structured populations.** Households, wards and networks add a term for each type of contact to $A$. The same scheme of Gibbs steps for the rates and Metropolis-Hastings steps for the event times still applies.
- **Other methods for the same data.** [Approximate Bayesian computation](/approximate-bayesian-computation/) needs only a simulator, and [particle filters](/particle-filter/), a kind of [sequential Monte Carlo](/sequential-monte-carlo/), give the likelihood of counts over time. Both avoid the latent event times. Approximate Bayesian computation gives an approximate posterior, and a particle filter gives a noisy estimate of the likelihood. The [expectation-maximization](/expectation-maximization/) algorithm uses the same missing-data view to find a maximum likelihood estimate.

## When to use it

Use it when individual removal times are known, the number of cases is small to moderate, and a full Bayesian answer is needed, with the posterior of the rates, of $R_0$ and of the infection times. It is the standard tool for outbreaks in households, hospitals and farms, where the model has a known likelihood once the event times are known. For daily counts of a large epidemic, use a renewal method such as the [Cori method](/cori-rt-estimation/), or a particle filter. For models without a tractable complete-data likelihood, use approximate Bayesian computation.

## Pitfalls

- **An invalid start.** If some case is infected at a time when nobody is infectious, the likelihood is 0 and the acceptance ratio is undefined. Start from a valid vector, as line L1 does.
- **Forgetting the zero-likelihood check.** If case $j$ is the only infectious person when case $k$ is infected, a proposal that moves the infection of $j$ after the infection of $k$ makes the epidemic impossible. The sweep must return $-\infty$ in this case, or the chain leaves the support.
- **The first case.** The first infection has no rate factor. Its time has a flat prior that is bounded above by $r_\kappa$ but not below. The likelihood bounds it in practice, because an early first infection gives a long infectious period and a large $D$, which the factor $e^{-\gamma D}$ makes unlikely.
- **The scale of $\beta$.** The rate in this page is $\beta S I/N$. Some papers use $\beta S I$, so their $\beta$ is this $\beta$ divided by $N$, and the full conditional has rate $b_\beta + A$.
- **Short runs.** Because $\gamma$ and $D$ are correlated, a run of a few hundred iterations can look settled and still be far from the posterior. Run several chains from different starts and compare them.
- **The model is assumed.** The posterior is exact for the Markov SIR model with homogeneous mixing. If the true infectious period is far from exponential, or the population is structured, the rates are biased.

## Implementations

## History

Gibson and Renshaw (1998) used Markov chain Monte Carlo with the unobserved event times of stochastic compartmental models as extra unknowns. O'Neill and Roberts (1999) gave the scheme for the general stochastic epidemic with observed removal times: gamma full conditionals for the rates, Metropolis-Hastings moves for single infection times, and reversible jump moves for unknown numbers of cases. O'Neill (2002) wrote a tutorial account. The idea of data augmentation itself is older, from the work of Tanner and Wong on posterior computation with missing data. Later work extended the method to households, networks, hospital wards and farm outbreaks, and to non-centred and block updates that mix faster.

## References
