---
tag: G0H3ZS
kind: algorithm
slug: thermodynamic-integration
name: Thermodynamic integration
area: scientific-computing/molecular-simulation
level: core
summary: Computes a free energy difference by integrating the ensemble average of dU/dlambda over a coupling parameter lambda from 0 to 1.
model: real-ram
complexity:
  vars: {K: the number of quadrature nodes, N: the number of samples per node}
  time: {worst: O(K N)}
  space: {extra: O(N + K)}
properties: {deterministic: false, randomized: true, iterative: false, unbiased: false}
history:
  year: 1935
  people: [John G. Kirkwood]
  note: Kirkwood introduced a coupling parameter that switches on the interaction of one molecule with the rest of a fluid and wrote the change of free energy as an integral of an average over that parameter.
prereqs: [canonical-ensemble, trapezoidal-rule]
see_also: [free-energy-perturbation, bennett-acceptance-ratio, jarzynski-equality, gauss-legendre-quadrature, simpsons-rule, mcmc-autocorrelation, umbrella-sampling, metropolis-hastings]
sources:
  - paper: doi:10.1063/1.1749657
    title: John G. Kirkwood, Statistical mechanics of fluid mixtures, Journal of Chemical Physics 3(5), 1935, 300-313
    locator: the coupling parameter and the free energy as an integral over it of an average of the coupling energy
  - book: doi:10.1016/B978-0-12-267351-1.X5000-7
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the chapter on free energies, the section on thermodynamic integration
  - book: isbn:9781848162471
    title: Tony Lelièvre, Mathias Rousset and Gabriel Stoltz, Free Energy Computations, A Mathematical Perspective, Imperial College Press, 2010
    locator: the treatment of thermodynamic integration for alchemical transitions
  - book: isbn:9783540384472
    title: Christophe Chipot and Andrew Pohorille (eds.), Free Energy Calculations, Theory and Applications in Chemistry and Biology, Springer Series in Chemical Physics 86, Springer, 2007
    locator: the chapter on thermodynamic integration
---

Thermodynamic integration (TI) computes the free energy difference $\Delta A = A_1 - A_0$ of two states by joining them with a family of potentials $U_\lambda$, $\lambda \in [0, 1]$, and integrating the derivative of the free energy along the path. Kirkwood (1935) showed that this derivative is a canonical average, $dA/d\lambda = \langle \partial U_\lambda / \partial \lambda \rangle_\lambda$ (a theorem). The method samples a few values of $\lambda$, takes the mean of $\partial U / \partial \lambda$ at each, and applies a quadrature rule. It belongs with [free energy perturbation](/free-energy-perturbation/), the [Bennett acceptance ratio](/bennett-acceptance-ratio/) and the [Jarzynski equality](/jarzynski-equality/): FEP and BAR use the energy differences between neighbouring states, TI uses derivatives at the states, and Jarzynski uses the work along switching paths. TI has no exponential average, so it does not depend on rare samples, but it adds a quadrature error.

## In plain words

To find the height difference between two towns, you can walk from one to the other and add up the small rises and falls on the way. Thermodynamic integration does this for free energy.

The path is a slow change of the system from the first state to the second, controlled by a dial. At a few settings of the dial, a simulation measures how fast the energy changes when the dial moves a little. The average of that rate is the slope of the free energy at that setting. A standard rule for the area under a curve then adds up the slopes over the whole path.

There are two errors: the noise of each simulation, and the error of the area rule when it uses too few settings or the curve bends sharply.

## The problem

The input is a family of potentials $U_\lambda(x)$, differentiable in $\lambda$, with $U_0$ and $U_1$ the two end states, a sampler of the canonical ensemble of each $U_\lambda$, the inverse temperature $\beta = 1/(k_B T)$ and a quadrature rule with nodes $\lambda_j \in [0, 1]$ and weights $a_j$. The output is an estimate of
$$\Delta A = A_1 - A_0 = \int_0^1 \Bigl\langle \frac{\partial U_\lambda}{\partial \lambda} \Bigr\rangle_\lambda d\lambda, \qquad A_\lambda = -k_B T \ln \int e^{-\beta U_\lambda(x)}\,dx,$$
and its statistical error. The common linear path is $U_\lambda = (1 - \lambda) U_0 + \lambda U_1$, with $\partial U / \partial \lambda = U_1 - U_0$.

## The algorithm

```pseudo id=main
TI(nodes lambda_1..lambda_K, weights a_1..a_K, SAMPLE, DUDL, N)
L1  total ← 0; var ← 0
L2  for j ← 1 to K do
L3      draw N samples x_i of the state lambda_j with SAMPLE
L4      g_j ← mean of DUDL(lambda_j, x_i); s_j ← its standard error
L5      total ← total + a_j g_j; var ← var + (a_j s_j)²
L6  return (total, sqrt(var))
```

The nodes are independent runs, so their errors add in quadrature on line L5. For a correlated chain, $s_j$ on line L4 must come from block averages or an estimate of the [autocorrelation time](/mcmc-autocorrelation/). The returned error is statistical only; the quadrature error is separate and must be judged by refining the rule. The tests use the composite [trapezoidal rule](/trapezoidal-rule/), the composite [Simpson rule](/simpsons-rule/) and [Gauss-Legendre](/gauss-legendre-quadrature/) nodes on $[0, 1]$.

## Example

**Harmonic wells, quadrature only.** Let $U_\lambda = (1 + \lambda) x^2 / 2$ at $k_B T = 1$, from $k_0 = 1$ to $k_1 = 2$. Then $\partial U / \partial \lambda = x^2 / 2$ and $\langle x^2 \rangle_\lambda = 1 / (1 + \lambda)$, so the integrand is $g(\lambda) = 0.5 / (1 + \lambda)$ and $\Delta A = \frac12 \ln 2 = 0.346574$. With the exact means at the nodes:

| rule | nodes | value | error |
|---|---|---|---|
| trapezoid, 2 intervals | 0, 0.5, 1 | 0.354167 | $7.59 \times 10^{-3}$ |
| trapezoid, 4 intervals | 5 | 0.348512 | $1.94 \times 10^{-3}$ |
| trapezoid, 8 intervals | 9 | 0.347061 | $4.87 \times 10^{-4}$ |
| Simpson, 2 intervals | 0, 0.5, 1 | 0.347222 | $6.49 \times 10^{-4}$ |
| Simpson, 4 intervals | 5 | 0.346627 | $5.34 \times 10^{-5}$ |
| Gauss-Legendre, 1 node | 0.5 | 0.333333 | $-1.32 \times 10^{-2}$ |
| Gauss-Legendre, 2 nodes | 0.211325, 0.788675 | 0.346154 | $-4.20 \times 10^{-4}$ |
| Gauss-Legendre, 3 nodes | 0.112702, 0.5, 0.887298 | 0.346561 | $-1.27 \times 10^{-5}$ |

By hand, the trapezoid with two intervals is $\frac14 g(0) + \frac12 g(0.5) + \frac14 g(1) = 0.125 + 0.166667 + 0.0625 = 0.354167$. Halving the interval divides the trapezoid error by 4 and the Simpson error by about 12 here (16 in the limit), as their orders 2 and 4 predict.

**Harmonic wells, sampled.** Three Gauss-Legendre nodes with $N$ exact normal draws per node (seed 1):

| $N$ | estimate | error bar | error |
|---|---|---|---|
| 100 | 0.32963 | 0.0272 | $-0.0169$ |
| 1000 | 0.34545 | 0.0089 | $-0.0011$ |
| 10000 | 0.34552 | 0.0029 | $-0.0011$ |

The quadrature error, $1.3 \times 10^{-5}$, is far below the statistical error, so here more samples help and more nodes would not.

**A quartic well with Metropolis sampling.** Let $U_\lambda = (1 - \lambda) x^2 / 2 + \lambda x^4 / 4$ at $k_B T = 1$. A direct quadrature of the two partition functions gives $\Delta A = -0.022510$. A random-walk Metropolis chain of 20000 steps per node, with error bars from 20 batch means (seed 2):

| rule | estimate | error bar | quadrature error alone |
|---|---|---|---|
| Gauss-Legendre, 3 nodes | $-0.026796$ | 0.0042 | $-0.00212$ |
| Gauss-Legendre, 5 nodes | $-0.026466$ | 0.0030 | $-0.00023$ |
| trapezoid, 4 intervals | $-0.011124$ | | 0.01287 |

The last column uses the exact means at the nodes. The integrand $\langle x^4/4 - x^2/2 \rangle_\lambda$ is 0.25 at $\lambda = 0$, 0.0822 at 0.1, $-0.0489$ at 0.5 and $-0.088$ at 1: it falls steeply near $\lambda = 0$, where the quartic term first cuts off the tails of the Gaussian. The trapezoid with five nodes misses this bend by 0.013, about four times the statistical error.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **Kirkwood's identity.** $dA_\lambda / d\lambda = \langle \partial U_\lambda / \partial \lambda \rangle_\lambda$, so $\Delta A$ is the integral of the average over $[0, 1]$.
2. **Curvature.** $d^2 A / d\lambda^2 = \langle \partial^2 U / \partial \lambda^2 \rangle_\lambda - \beta\, \mathrm{var}_\lambda(\partial U / \partial \lambda)$. On the linear path the first term is 0, so $A(\lambda)$ is concave and the integrand never increases along the path.
3. **The estimator.** With independent runs at the nodes, the output is an unbiased estimate of the quadrature sum $\sum_j a_j g(\lambda_j)$, its variance is $\sum_j a_j^2 \mathrm{var}(\bar g_j)$, and it converges to that sum as $N \to \infty$.
4. **Total error.** The error is the quadrature error of the rule on $g$ plus a statistical error of order $N^{-1/2}$. The rule of order $p$ gives a quadrature error $O(K^{-p})$ for a smooth $g$.
5. **The harmonic example**: the exact integrand $0.5/(1+\lambda)$ and $\Delta A = \frac12 \ln 2$.

## Complexity

$K$ nodes with $N$ samples each cost $K N$ evaluations of $\partial U / \partial \lambda$ plus $K N$ steps of the sampler, which dominate. The extra space is $O(N)$ for the samples of one node, or $O(1)$ with running sums, and $O(K)$ for the means. For a target error $\varepsilon$, the statistical part needs $N K = O(\varepsilon^{-2})$ samples in total, and the quadrature part needs $K = O(\varepsilon^{-1/p})$ nodes for a smooth integrand (a theorem for a fixed smooth integrand; the constants depend on the path).

## Properties

- **No exponential average.** Each node needs only a plain mean, so the result does not depend on rare samples, unlike FEP.
- **Biased by the quadrature, not by the sampling.** For a fixed rule, the estimator is unbiased for the quadrature sum; the quadrature error is a deterministic bias.
- **Needs derivatives.** The code must supply $\partial U / \partial \lambda$; on the linear path it is $U_1 - U_0$.
- **Path-independent result, path-dependent cost.** $\Delta A$ does not depend on the path, but the smoothness of the integrand and the variance at each node do.
- **Monotone integrand on the linear path** (Claim 2), which helps to spot errors: a mean that rises along the path is noise or a sampling failure.

## Variants and improvements

- **Nonlinear paths.** Paths such as $U_\lambda = (1 - \lambda)^k U_0 + \lambda^k U_1$, or soft-core potentials for atoms that appear or vanish, remove singularities of the integrand at the ends. The choice of path is a choice.
- **Quadrature.** Gauss-Legendre nodes avoid the end points, where the integrand may be singular; adaptive placement puts more nodes where the integrand bends.
- **Slow growth.** One run that changes $\lambda$ slowly during the simulation integrates on the fly. It has a hysteresis error unless the change is very slow; the [Jarzynski equality](/jarzynski-equality/) turns finite-speed runs into an exact estimate.
- **Other parameters.** The same identity with temperature or volume as the parameter gives the Gibbs-Helmholtz route and integration of the pressure; integration from an Einstein crystal (Frenkel and Ladd 1984) gives absolute free energies of solids.
- **Combining with BAR.** The same runs give both the derivatives and the energy differences between neighbouring nodes, so TI and [BAR](/bennett-acceptance-ratio/) can be compared on the same data.

## When to use it

Use TI when $\partial U / \partial \lambda$ is cheap and smooth along the path, for example for alchemical changes with soft-core potentials, for changes of temperature or density, and for absolute free energies from a reference system. It is robust when the end states overlap poorly, since each node needs only local sampling. Prefer BAR or MBAR on the same windows when the integrand has sharp features that need too many nodes, or when derivatives are not available.

## Pitfalls

- **Too few nodes** where the integrand bends, as in the quartic example with the trapezoid.
- **Singular end points.** When atoms vanish with a linear path, $\langle \partial U / \partial \lambda \rangle$ can diverge at $\lambda = 0$ or 1; use soft-core paths or Gauss nodes.
- **Correlated samples.** The plain standard error is too small for a Markov chain; use batch means.
- **Hidden slow modes.** If a slow motion of the system does not relax at a node, the mean at that node is wrong with a small error bar. Run forward and backward along $\lambda$ and compare.
- **Ignoring the quadrature error.** The error bar returned by the method is statistical only.

## Implementations

## History

Kirkwood (1935) introduced the coupling parameter in his theory of fluid mixtures: it switches on the interaction of one molecule with the rest, and the free energy change is an integral of the mean coupling energy. The identity became a simulation method when Monte Carlo and molecular dynamics could compute the averages. Thermodynamic integration over temperature and density had long been used in thermodynamics, and Frenkel and Ladd (1984) used integration from an Einstein crystal for the free energy of solids.

## References
