---
tag: Y2JYEC
kind: algorithm
slug: bennett-acceptance-ratio
name: Bennett acceptance ratio
aliases:
- BAR method
area: scientific-computing/molecular-simulation
level: advanced
summary: Estimates a free energy difference from samples of both end states by solving an equation for the minimum-variance estimate.
model: real-ram
complexity:
  vars: {n: the total number of samples of the two states, b: the number of bisection steps}
  time: {worst: O(b n)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, iterative: true, unbiased: false, consistent: true}
history:
  year: 1976
  people: [Charles H. Bennett]
  note: Bennett derived the estimator that uses the samples of both states with the weight function of least asymptotic variance, as a refinement of the Metropolis acceptance ratio between two states.
prereqs: [free-energy-perturbation, bisection-method]
see_also: [bridge-sampling, maximum-likelihood-estimation, thermodynamic-integration, jarzynski-equality, weighted-histogram-analysis-method, importance-sampling, umbrella-sampling, delta-method]
sources:
  - paper: doi:10.1016/0021-9991(76)90078-4
    title: Charles H. Bennett, Efficient estimation of free energy differences from Monte Carlo data, Journal of Computational Physics 22(2), 1976, 245-268
    locator: the acceptance ratio identity for an arbitrary weight function, the optimal weight and the self-consistent equation with the Fermi function
  - paper: doi:10.1103/PhysRevLett.91.140601
    title: Michael R. Shirts, Eric Bair, Giles Hooker and Vijay S. Pande, Equilibrium free energies from nonequilibrium measurements using maximum-likelihood methods, Physical Review Letters 91, 140601, 2003
    locator: the derivation of the BAR equation as a maximum likelihood estimate from the forward and reverse work and its variance
  - paper: doi:10.1063/1.2978177
    title: Michael R. Shirts and John D. Chodera, Statistically optimal analysis of samples from multiple equilibrium states, Journal of Chemical Physics 129, 124105, 2008
    locator: the multistate generalization (MBAR) that reduces to BAR for two states
  - book: isbn:9783540384472
    title: Christophe Chipot and Andrew Pohorille (eds.), Free Energy Calculations, Theory and Applications in Chemistry and Biology, Springer Series in Chemical Physics 86, Springer, 2007
    locator: the treatment of the Bennett acceptance ratio among the free energy perturbation methods
---

The Bennett acceptance ratio (BAR) estimates the free energy difference $\Delta A = A_1 - A_0$ of two states from samples of both states. [Free energy perturbation](/free-energy-perturbation/) uses one state and is poor in one of its two directions; BAR uses both directions at once with the weight that makes the large-sample variance smallest (Bennett 1976, a theorem). The estimate is the root of one equation in one unknown, which has exactly one root, so a bisection always finds it. In statistics the same estimator is the optimal case of [bridge sampling](/bridge-sampling/) (Meng and Wong 1996), and it is also the maximum likelihood estimate of $\Delta A$ given the energy differences (Shirts and co-workers 2003). With FEP, [thermodynamic integration](/thermodynamic-integration/) and the [Jarzynski equality](/jarzynski-equality/) it forms the standard set of free energy methods; for many states, MBAR (Shirts and Chodera 2008) generalizes it.

## In plain words

Free energy perturbation looks from one state towards the other. Looking from the first state works well in some cases, and looking from the second works well in others, but each view alone can miss what the other sees.

Bennett's method looks from both sides at once. For each snapshot of either state, it asks how much the energy would change in the other state. It then finds the one value of the free energy difference that makes the two sets of snapshots agree, in a balanced way that gives each snapshot a weight between zero and one. No single lucky snapshot can dominate.

The answer comes from a simple search: try a value, see which side is too large, and halve the interval.

## The problem

The input is $n_0$ samples $x_i$ of the canonical ensemble of state 0 and $n_1$ samples $y_j$ of state 1, the energies $U_0$ and $U_1$ on both sets, and $\beta = 1/(k_B T)$. Write the reduced differences
$$w_{F,i} = \beta\,(U_1(x_i) - U_0(x_i)), \qquad w_{R,j} = \beta\,(U_0(y_j) - U_1(y_j)),$$
and the Fermi function $f(t) = 1 / (1 + e^t)$. The output is the root $C$ of
$$\sum_{j=1}^{n_1} f(w_{R,j} + C) = \sum_{i=1}^{n_0} f(w_{F,i} - C), \qquad \beta \widehat{\Delta A} = C - \ln(n_1 / n_0),$$
and an error bar. The identity behind it holds for every weight function (Claim 1 of the proof), and the Fermi function comes from the weight of least variance (Claim 4).

## The algorithm

```pseudo id=main
BAR(w_F[1..n_0], w_R[1..n_1], beta)          ▷ f(t) = 1 / (1 + e^t)
L1  M ← ln(n_1 / n_0)
L2  lo ← min(min_i w_F[i], min_j -w_R[j]) - 40; hi ← max(max_i w_F[i], max_j -w_R[j]) + 40
L3  while hi - lo > tol do
L4      C ← (lo + hi) / 2
L5      if sum_j f(w_R[j] + C) > sum_i f(w_F[i] - C) then lo ← C
L6      else hi ← C
L7  return ((lo + hi) / 2 - M) / beta
```

The left side of the equation decreases strictly in $C$ and the right side increases strictly, so their difference has exactly one sign change, and lines L3 to L6 keep the root inside $[lo, hi]$. The bracket of line L2 holds whenever $n_0 / n_1$ and $n_1 / n_0$ are below $e^{40} - 1$ (Claim 3). The function $f$ is computed as $e^{-t}/(1 + e^{-t})$ for $t > 0$, so it never overflows. Each test of line L5 costs $O(n_0 + n_1)$. A Newton step on the same equation converges faster, but bisection cannot fail.

The error bar is the delta-method error at the root,
$$\sigma^2_{\beta \Delta A} \approx \frac{\mathrm{var}\, f(w_F - C)}{n_0\, \overline{f(w_F - C)}^2} + \frac{\mathrm{var}\, f(w_R + C)}{n_1\, \overline{f(w_R + C)}^2},$$
for independent samples. It is a large-sample estimate.

## Example

**By hand.** One sample of each state, with $U_1 - U_0 = 1.0$ at the state-0 sample and $0.2$ at the state-1 sample, at $\beta = 1$. Then $w_F = 1.0$, $w_R = -0.2$, $M = 0$, and the equation $f(-0.2 + C) = f(1.0 - C)$ holds when $-0.2 + C = 1.0 - C$, so $C = 0.6$ and $\Delta A = 0.6$: the mean of the two energy differences. FEP from state 0 alone would give 1.0 and from state 1 alone 0.2.

**Harmonic wells.** $U_0 = x^2/2$ and $U_1 = x^2$ at $k_B T = 1$, so $\Delta A = \frac12 \ln 2 = 0.346574$. With $N$ exact samples of each state (seed 1):

| $N$ | BAR | BAR error bar | FEP forward | FEP reverse |
|---|---|---|---|---|
| 10 | 0.3303 | 0.0992 | 0.3565 | 0.3616 |
| 100 | 0.3214 | 0.0303 | 0.3100 | 0.3166 |
| 1000 | 0.3517 | 0.0103 | 0.3536 | 0.3345 |

Over 500 independent replicas (seed 4), the mean error and the spread of each estimate were:

| $N$ per state | BAR | FEP forward | FEP reverse |
|---|---|---|---|
| 20 | $-0.0019$, spread 0.0719 | $-0.0030$, spread 0.0886 | $-0.0039$, spread 0.1997 |
| 200 | $-0.0024$, spread 0.0232 | $-0.0028$, spread 0.0278 | $-0.0034$, spread 0.0817 |

BAR has the smallest spread, and the forward FEP spread at $N = 200$ matches its theory value $\sqrt{0.1547/200} = 0.0278$. The reverse FEP has infinite variance here, and its spread is the worst.

**Poor overlap.** A unit well moved by $a = 3$, with $\Delta A = 0$ exactly and 1000 samples of each state (seed 1): BAR gives $-0.039 \pm 0.091$, forward FEP gives 0.851, and reverse FEP gives $-0.301$. The two FEP estimates each lean on the rare tail of the other state; BAR needs only the region between the states, where both have some samples.

**Unequal sample sizes.** With 3000 samples of state 0 and 300 of state 1 in the harmonic case (seed 5), BAR gives $0.3381 \pm 0.0068$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The acceptance ratio identity.** For every weight function $W$ for which the averages exist, $Z_1 / Z_0 = \langle W e^{-\beta U_1} \rangle_0 / \langle W e^{-\beta U_0} \rangle_1$.
2. **The Bennett equation.** With the weight $W \propto 1/(n_0 e^{-\beta U_0} + n_1 e^{\beta \Delta A} e^{-\beta U_1})$ the identity becomes the expected form of the equation above, which holds at the true $C = \beta \Delta A + \ln(n_1 / n_0)$.
3. **One root and a valid bracket.** The sample equation has exactly one root, it lies in the bracket of line L2, and bisection converges to it.
4. **Least variance.** Among all weights, the large-sample relative variance of the ratio estimate is smallest for the weight of Claim 2 (by the Cauchy-Schwarz inequality).
5. **Symmetry and exact cases.** Swapping the states changes the sign of the estimate exactly, a constant difference $U_1 - U_0 = c$ gives $c$ exactly, and one sample of each state gives the mean of the two differences.

The estimator is consistent. Like FEP it is biased for finite samples, but its bias and variance are much smaller when the states overlap poorly.

## Complexity

Each evaluation of the equation costs $O(n_0 + n_1)$, and bisection on a bracket of width $L$ needs $\lceil \log_2(L / \mathrm{tol}) \rceil$ steps, about 45 for double precision on the brackets here. So BAR costs $O(b\, n)$ time with $b \approx 50$, which is negligible next to the cost of the samples. The extra space is $O(1)$ beyond the input arrays. Newton's method needs fewer evaluations but must be safeguarded.

## Properties

- **Uses both states.** It needs samples of both end states of each window and the energy of the other state on each sample.
- **Least asymptotic variance** among acceptance ratio estimators (a theorem), and it never needs an exponential of a large positive number: each weight lies in $(0, 1)$.
- **Antisymmetric.** Swapping the roles of the states gives exactly $-\widehat{\Delta A}$, unlike FEP.
- **Shift by a constant.** Adding a constant $c$ to $U_1$ adds exactly $c$ to the estimate.
- **Maximum likelihood.** The same equation is the maximum likelihood estimate of $\Delta A$ from the two sets of energy differences (Shirts and co-workers 2003), which also gives its variance.
- **Asymptotically optimal, not exactly unbiased.** For small samples it is biased, though much less than FEP when the overlap is poor.

## Variants and improvements

- **MBAR.** For $K$ states with samples of each, MBAR (Shirts and Chodera 2008) solves $K$ coupled equations and uses all samples in every free energy; for two states it is BAR. Its histogram form for a coordinate is close to [WHAM](/weighted-histogram-analysis-method/).
- **Nonequilibrium BAR.** With forward and reverse work values from switching runs instead of energy differences, the same equation gives $\Delta A$ through the Crooks relation (Shirts and co-workers 2003).
- **Bridge sampling.** In statistics, [bridge sampling](/bridge-sampling/) with the optimal bridge and its iterative scheme (Meng and Wong 1996) is the same estimator for ratios of normalizing constants.
- **Staging.** For a long path, BAR is applied to each pair of neighbouring windows and the results are added, as in staged FEP.

## When to use it

Use BAR whenever samples of both end states of a window are available, which is the usual case for staged alchemical calculations: it costs nothing extra over FEP, gives a smaller error and is robust. Prefer MBAR when many windows are coupled. If BAR and both FEP directions agree within their error bars, the overlap is good; if BAR is far from both, or its error bar is large, add windows.

## Pitfalls

- **No overlap at all.** If no sample of either state falls in the region that both states visit, BAR returns a number with a large error bar; it cannot invent the missing region.
- **Wrong sign convention.** $w_R$ is $\beta(U_0 - U_1)$ on the state-1 samples; mixing it up with $\beta(U_1 - U_0)$ gives a wrong root with no warning.
- **Correlated samples.** The error bar assumes independent samples; subsample the chain or use block averages.
- **Forgetting the $\ln(n_1 / n_0)$ term** for unequal sample sizes.
- **Overflow in $f$.** Computing $1/(1 + e^t)$ directly overflows for large $t$; use the two-branch form.

## Implementations

## History

Bennett (1976) asked how to best combine Monte Carlo data from two states to estimate the ratio of their partition functions. He wrote an identity that holds for every weight function, found the weight of least variance, and obtained the equation with the Fermi function; the name comes from the Metropolis acceptance probability that appears in a special case. Meng and Wong (1996) found the same estimator in statistics as the optimal bridge sampler. Shirts, Bair, Hooker and Pande (2003) showed it is a maximum likelihood estimate and extended it to nonequilibrium work, and Shirts and Chodera (2008) generalized it to many states as MBAR.

## References
