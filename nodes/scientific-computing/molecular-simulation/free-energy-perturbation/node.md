---
tag: 1TXW31
kind: algorithm
slug: free-energy-perturbation
name: Free energy perturbation
aliases:
- Zwanzig formula
area: scientific-computing/molecular-simulation
level: core
summary: Estimates the free energy difference of two states as -kT log of the average of exp(-dU/kT) over samples of one state.
model: real-ram
complexity:
  vars: {N: the number of samples per window, K: the number of windows}
  time: {worst: O(K N)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, iterative: false, unbiased: false, consistent: true}
history:
  year: 1954
  people: [Robert W. Zwanzig]
  note: Zwanzig wrote the free energy of a perturbed system as a canonical average over the unperturbed one and used it for a high-temperature expansion of the equation of state of gases.
prereqs: [canonical-ensemble, importance-sampling]
see_also: [thermodynamic-integration, bennett-acceptance-ratio, jarzynski-equality, umbrella-sampling, annealed-importance-sampling, jensens-inequality, effective-sample-size, log-sum-exp-trick]
sources:
  - paper: doi:10.1063/1.1740409
    title: Robert W. Zwanzig, High-temperature equation of state by a perturbation method. I. Nonpolar gases, Journal of Chemical Physics 22(8), 1954, 1420-1426
    locator: the perturbation formula for the free energy as an average of exp(-U_1/kT) over the unperturbed system
  - book: isbn:9783540384472
    title: Christophe Chipot and Andrew Pohorille (eds.), Free Energy Calculations, Theory and Applications in Chemistry and Biology, Springer Series in Chemical Physics 86, Springer, 2007
    locator: the chapter on free energy perturbation, its bias and variance, and staging
  - book: isbn:9781848162471
    title: Tony Lelièvre, Mathias Rousset and Gabriel Stoltz, Free Energy Computations, A Mathematical Perspective, Imperial College Press, 2010
    locator: the treatment of free energy differences between two states and the free energy perturbation identity
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: the sections on free energy differences by perturbation and on staging
---

Free energy perturbation (FEP) estimates the free energy difference $\Delta A = A_1 - A_0$ of two states with potential energies $U_0$ and $U_1$ from samples of state 0 alone. It uses the exact identity of Zwanzig (1954), $\Delta A = -k_B T \ln \langle e^{-\beta (U_1 - U_0)} \rangle_0$ with $\beta = 1/(k_B T)$, and replaces the canonical average by a sample mean. It is [importance sampling](/importance-sampling/) of the ratio of partition functions $Z_1 / Z_0$, with state 0 as the proposal. FEP, [thermodynamic integration](/thermodynamic-integration/), the [Bennett acceptance ratio](/bennett-acceptance-ratio/) and the [Jarzynski equality](/jarzynski-equality/) form one family: FEP uses one end state, BAR uses both, TI uses many states between them, and Jarzynski uses nonequilibrium paths. The estimate is exact in the limit of many samples, biased for a finite number, and useless when the two states share few configurations.

## In plain words

You know how a system behaves in one state and want to know how much more or less favourable a second state is. Free energy perturbation takes snapshots of the first state and asks, for each snapshot, how much the energy would change in the second state. It then takes a special kind of average of these changes.

The average gives most weight to the snapshots where the second state is most favourable. If such snapshots are rare in the first state, the average depends on a few lucky ones, and the answer is poor even with many snapshots. The cure is to go in small steps: a chain of states between the two ends, each close to the next, and one small calculation for each pair.

## The problem

The input is a sampler for the canonical ensemble of state 0, the two potential energy functions $U_0$ and $U_1$ on the same configuration space, and $\beta$. The output is an estimate of
$$\Delta A = A_1 - A_0 = -\frac{1}{\beta} \ln \frac{Z_1}{Z_0}, \qquad Z_j = \int e^{-\beta U_j(x)}\, dx,$$
with $A_j = -k_B T \ln Z_j$. The identity behind the method (a theorem, Claim 1 of the proof) is
$$\Delta A = -\frac{1}{\beta} \ln \bigl\langle e^{-\beta \Delta U} \bigr\rangle_0, \qquad \Delta U = U_1 - U_0.$$
It needs that every configuration with $e^{-\beta U_1} > 0$ also has $e^{-\beta U_0} > 0$. For a long path the states are joined by a family $U_\lambda$ with $\lambda \in [0, 1]$, and the staged form uses the windows $0 = \lambda_0 < \lambda_1 < \dots < \lambda_K = 1$.

## The algorithm

```pseudo id=main
FEP(x_1, ..., x_N samples of state 0, U_0, U_1, beta)
L1  d_i ← U_1(x_i) - U_0(x_i) for each i
L2  m ← min_i d_i                                  ▷ shift so that no exponential overflows
L3  s ← sum_i exp(-beta (d_i - m))
L4  return m - (1 / beta) ln(s / N)

STAGED-FEP(lambda_0 = 0 < lambda_1 < ... < lambda_K = 1, SAMPLE, U, beta, N)
L5  dA ← 0
L6  for k ← 0 to K - 1 do
L7      draw N samples x_i of the state lambda_k with SAMPLE
L8      dA ← dA + FEP(x, U_{lambda_k}, U_{lambda_{k+1}}, beta)
L9  return dA
```

Line L4 equals $-\beta^{-1} \ln \bigl( N^{-1} \sum_i e^{-\beta d_i} \bigr)$, and the shift by $m$ makes every exponent at most 0 with one of them equal to 0. The windows of STAGED-FEP are independent, so the errors of the windows add in quadrature. The error bar of one window is the delta-method error $\mathrm{sd}(w) / (\beta \sqrt{N}\, \overline{w})$ with $w_i = e^{-\beta (d_i - m)}$; it assumes independent samples and a finite variance of $w$. For a correlated chain, use [block averages](/mcmc-autocorrelation/) instead.

## Example

**By hand.** Three samples of state 0 have $\beta \Delta U = 0, 1, 2$, in units of $k_B T$. Then $m = 0$, $s = 1 + e^{-1} + e^{-2} = 1.503215$ and
$$\beta \Delta A \approx -\ln(1.503215 / 3) = 0.691006.$$
The plain mean of $\beta \Delta U$ is 1. The FEP estimate is always at most the plain mean (Jensen's inequality), and here the sample with $\beta \Delta U = 0$ carries more than half of the weight.

**Harmonic wells, both directions.** Let $U_0 = x^2/2$ and $U_1 = x^2$ in one dimension at $k_B T = 1$, so $k_0 = 1$, $k_1 = 2$ and $\Delta A = \frac{1}{2} \ln(k_1 / k_0) = 0.346574$ exactly. The forward estimate samples the wide well ($x \sim N(0, 1)$) and the reverse estimate samples the narrow well ($x \sim N(0, 1/2)$) and returns $-\mathrm{FEP}$ of the opposite difference:

| $N$ | forward (seed 1) | forward error bar | reverse (seed 2) |
|---|---|---|---|
| 10 | 0.3565 | 0.1249 | 0.3808 |
| 100 | 0.3100 | 0.0369 | 0.5622 |
| 1000 | 0.3536 | 0.0125 | 0.3496 |
| 10000 | 0.3441 | 0.0039 | 0.3424 |

The forward direction has $E[w] = 1/\sqrt{2}$ and $E[w^2] = 1/\sqrt{3}$, so the large-$N$ variance of the estimate is $0.1547 / N$ (a theorem, Claim 5), and the error bars match it. The reverse direction has $E[w^2] = \infty$: the weight $e^{x^2/2}$ is not square integrable under $N(0, 1/2)$. Its estimate still converges, but there is no valid error bar and the error falls more slowly than $1/\sqrt{N}$.

**Bias.** Over 4000 independent runs of $N = 5$ forward samples, the mean of the estimate is $\Delta A + 0.0190 \pm 0.0031$, close to the first-order bias $\mathrm{var}(w) / (2 N \beta E[w]^2) = 0.0155$. With $N = 2$ the bias is 0.0591 (first order 0.0387), and with $N = 20$ it is 0.0040 (first order 0.0039). The bias is always upward (Claim 4).

**Staging a poor overlap.** Move a unit well by $a = 3$: $U_\lambda = (x - 3\lambda)^2 / 2$. The free energy does not change, so $\Delta A = 0$. With 1200 samples in total, split over $K$ equal windows:

| $K$ | estimate (seed 1) | error bar | spread over replicas | theory spread |
|---|---|---|---|---|
| 1 | 0.7975 | 0.1853 | 0.5033 | 2.598 |
| 2 | 0.1844 | 0.1175 | 0.156 | 0.168 |
| 3 | 0.0877 | 0.0992 | 0.110 | 0.114 |
| 6 | 0.0370 | 0.0888 | 0.089 | 0.092 |
| 12 | 0.0308 | 0.0860 | 0.085 | 0.088 |

The theory variance is $K^2 (e^{a^2/K^2} - 1) / 1200$ (Claim 7). With one window it is huge, but the estimate does not show it: the error bar of 0.185 says the answer is $0.80 \pm 0.19$, more than four error bars from the truth, and the spread over replicas, 0.50, is far below the theory value, because the samples that would raise it almost never occur. With six windows the error bar, the spread and the theory agree.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The Zwanzig identity** $Z_1 / Z_0 = \langle e^{-\beta \Delta U} \rangle_0$ holds whenever the support of state 1 lies inside the support of state 0.
2. **The shift** on lines L2 to L4 does not change the value and keeps every exponential in $(0, 1]$.
3. **Consistency.** For independent samples, or an ergodic chain, the estimate converges to $\Delta A$ with probability 1.
4. **Bounds and bias.** The estimate lies between $\min_i \Delta U_i$ and the mean of $\Delta U_i$, and its expected value is at least $\Delta A$ for every $N$.
5. **Error.** If $E[w^2] < \infty$, then $\sqrt{N}(\widehat{\Delta A} - \Delta A)$ tends to a normal law with variance $\mathrm{var}(w) / (\beta^2 E[w]^2)$, and the first-order bias is $\mathrm{var}(w) / (2 N \beta E[w]^2)$.
6. **Staging.** The window identities add up to the identity for the whole path.
7. **The two examples**: the exact moments for the harmonic wells and the variance $K^2(e^{a^2/K^2} - 1)/N$ for the shifted well.

## Complexity

One window costs $N$ evaluations of $\Delta U$ and $N$ exponentials, so the staged form costs $\Theta(K N)$ plus $K N$ draws from the sampler, which in practice is the dominant cost (molecular dynamics or Monte Carlo). The extra space is $O(N)$ for the differences, or $O(1)$ if a running maximum and a running sum are kept. The number of samples needed for a given error is proportional to $\mathrm{var}(w) / E[w]^2$, which grows exponentially as the overlap gets worse: for the shifted well it is $e^{a^2} - 1$ in one window and $K^2(e^{a^2/K^2} - 1)$ over $K$ windows (a theorem for that example).

## Properties

- **Exact identity, biased estimator.** The identity is a theorem; the estimate is biased upward for finite $N$ and consistent.
- **Asymmetric.** The forward and reverse estimates are not equally good. The better direction is usually the one that samples the state with the wider distribution (a heuristic), as in the harmonic example.
- **Only end states.** One window needs samples of one state and the energy of the other on those samples; it needs no derivative of $U$.
- **Self-deceiving error bars.** When the overlap is poor, the error bar from the samples is too small, as in the shifted well with one window.
- **Insensitive to a constant.** Adding a constant $c$ to $U_1$ adds $c$ to the estimate exactly.

## Variants and improvements

- **Staging** with intermediate $\lambda$ windows, as above. The number and spacing of windows is a choice; a common heuristic keeps the standard deviation of $\beta \Delta U$ in each window near 1 to 2.
- **Bennett acceptance ratio.** [BAR](/bennett-acceptance-ratio/) uses the samples of both states of a window and has the lowest variance among a broad class of estimators; MBAR (Shirts and Chodera 2008) extends it to all windows at once.
- **Cumulant expansion.** $\beta \Delta A = \beta \langle \Delta U \rangle_0 - \frac{\beta^2}{2} \mathrm{var}_0(\Delta U) + \dots$, exact to second order when $\Delta U$ is normal. It is a model, not an identity, and it fails for skewed distributions.
- **Nonequilibrium paths.** The [Jarzynski equality](/jarzynski-equality/) is FEP with the instantaneous switch replaced by a finite-time switch; [annealed importance sampling](/annealed-importance-sampling/) is its counterpart in statistics.
- **Thermodynamic integration** replaces the exponential average by an integral of $\langle \partial U / \partial \lambda \rangle_\lambda$, which has no exponential and is often more stable.

## When to use it

Use FEP for small changes, where the two states share most of their important configurations: a small mutation of a ligand, a change of a charge, a new force field term. Its simplicity and its use of end states only make it a quick first estimate, and in staged form it is the classic alchemical method. For large changes, use many windows and combine them with BAR, or use thermodynamic integration. Run both directions: if the forward and reverse estimates disagree by much more than their error bars, the overlap is too poor.

## Pitfalls

- **Poor overlap with small error bars.** The estimate can be wrong by many error bars, as in the one-window shifted well. Always compare forward and reverse, or look at the histogram of $\beta \Delta U$.
- **Infinite variance.** In the reverse harmonic case the variance of $w$ is infinite, and the usual error bar is meaningless.
- **Overflow.** Computing $e^{-\beta \Delta U}$ without the shift overflows or underflows for $|\beta \Delta U|$ beyond a few hundred.
- **Particles that appear.** When atoms are switched on, configurations where they overlap others give $U_1 = \infty$ and break the support condition in the reverse direction; soft-core potentials are the standard fix.
- **Correlated samples.** The error formula assumes independent samples; use block averages for a correlated chain.

## Implementations

## History

Zwanzig (1954) wrote the free energy of a perturbed system as an average of the Boltzmann factor of the perturbation over the unperturbed system, and expanded it for the equation of state of gases at high temperature. The same identity became a computational method once Monte Carlo and molecular dynamics could sample the unperturbed system. Bennett (1976) analysed its variance and showed how to use both states. Its alchemical use, in which atoms are mutated through intermediate states, became common in the 1980s for solvation and binding free energies.

## References
