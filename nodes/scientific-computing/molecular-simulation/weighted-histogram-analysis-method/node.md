---
tag: 53HG7A
kind: algorithm
slug: weighted-histogram-analysis-method
name: Weighted histogram analysis method
aliases:
- WHAM
area: scientific-computing/molecular-simulation
level: advanced
summary: Combines the biased histograms of umbrella sampling windows into one unbiased free energy profile by solving self-consistent equations.
model: real-ram
complexity:
  vars: {K: the number of windows, B: the number of bins, I: the number of iterations}
  time: {worst: O(I K B)}
  space: {extra: O(K B)}
properties: {deterministic: true, randomized: false, iterative: true, unbiased: false, consistent: true}
history:
  year: 1992
  people: [Shankar Kumar, John M. Rosenberg, Djamal Bouzida, Robert H. Swendsen, Peter A. Kollman]
  note: Kumar and co-workers extended the multiple histogram method of Ferrenberg and Swendsen to the biased windows of umbrella sampling and gave the self-consistent equations used today.
prereqs: [umbrella-sampling, maximum-likelihood-estimation, fixed-point-iteration]
see_also: [bennett-acceptance-ratio, convex-function, log-sum-exp-trick, free-energy-perturbation, metadynamics, collective-variable, kernel-density-estimation, newton-raphson-method]
sources:
  - paper: doi:10.1002/jcc.540130812
    title: Shankar Kumar, John M. Rosenberg, Djamal Bouzida, Robert H. Swendsen and Peter A. Kollman, The weighted histogram analysis method for free-energy calculations on biomolecules. I. The method, Journal of Computational Chemistry 13(8), 1992, 1011-1021
    locator: the WHAM equations for the unbiased probabilities and the window free energies, and their iterative solution
  - paper: doi:10.1063/1.2978177
    title: Michael R. Shirts and John D. Chodera, Statistically optimal analysis of samples from multiple equilibrium states, Journal of Chemical Physics 129, 124105, 2008
    locator: the MBAR estimating equations and their relation to WHAM in the limit of narrow bins
  - paper: doi:10.1002/wcms.66
    title: Johannes Kästner, Umbrella sampling, Wiley Interdisciplinary Reviews, Computational Molecular Science 1(6), 2011, 932-942
    locator: the use of WHAM to combine the windows of umbrella sampling
---

The weighted histogram analysis method (WHAM) combines the histograms of the $K$ windows of [umbrella sampling](/umbrella-sampling/) into one free energy profile along a [collective variable](/collective-variable/). Each window $k$ has a known bias $w_k(s)$ and an unknown free energy $f_k$, which is the constant that the simple join of neighbouring windows tries to guess. WHAM finds all $f_k$ and the unbiased bin probabilities $p(b)$ together, from two coupled equations, and weights every window's counts in every bin by how much information they carry. The solution is the [maximum likelihood estimate](/maximum-likelihood-estimation/) of $p$ given the histograms, and the minimum of one [convex function](/convex-function/) of the $f_k$, so it is unique. The classic solver is a [fixed-point iteration](/fixed-point-iteration/), simple but sometimes slow. For two states with no bins, the same equations give the [Bennett acceptance ratio](/bennett-acceptance-ratio/); for many states with no bins they give MBAR.

## In plain words

Umbrella sampling gives many small pieces of a free energy curve, each seen through its own known spring. Each piece is correct only up to an unknown shift up or down.

WHAM finds all the shifts at once. It makes a guess for the true curve, uses it to predict what each simulation should have seen, and corrects the shifts until the predictions agree with the counts. Where several simulations saw the same region, it trusts each one in proportion to how many samples it put there.

The result does not depend on the order of the pieces, and it uses all the data in every region.

## The problem

The input is, for each window $k = 1, \dots, K$, the histogram $n_k(b)$ over bins $b = 1, \dots, B$ of a collective variable, the number of samples $N_k = \sum_b n_k(b)$, the bias $w_k(b)$ at the bin centres, and $\beta = 1/(k_B T)$. Let $n(b) = \sum_k n_k(b)$. The output is the unbiased probabilities $p(b)$, with $\sum_b p(b) = 1$, and the window free energies $f_k$, which solve
$$p(b) = \frac{n(b)}{\sum_k N_k\, e^{\beta (f_k - w_k(b))}}, \qquad e^{-\beta f_k} = \sum_b p(b)\, e^{-\beta w_k(b)}.$$
The profile is then $F(b) = -\beta^{-1} \ln p(b)$, up to a constant. The first equation weights the counts of all windows in bin $b$; the second says that $f_k$ is the free energy of window $k$ in the unbiased distribution $p$.

## The algorithm

```pseudo id=main
WHAM(n_k(b), w_k(b), beta, tol)
L1  f_k ← 0 for every window k
L2  repeat
L3      for each bin b: p(b) ← n(b) / sum_k N_k exp(beta (f_k - w_k(b)))
L4      p ← p / sum_b p(b)
L5      for each window k: f_k ← -ln(sum_b p(b) exp(-beta w_k(b))) / beta
L6  until the largest change of any f_k is below tol
L7  return p, f
```

Line L3 is the first equation and line L5 the second. Line L4 fixes the free constant: the equations do not change when every $f_k$ moves by the same amount and $p$ is scaled to match, so $p$ is normalized at each step. All sums are done in the log domain with the [log-sum-exp trick](/log-sum-exp-trick/), because $e^{-\beta w_k(b)}$ spans hundreds of orders of magnitude for bins far from the centre of window $k$. Empty bins get $p(b) = 0$.

The fixed points of this iteration are exactly the minimizers of the convex function
$$L(f) = \sum_b n(b) \ln \sum_k N_k\, e^{\beta (f_k - w_k(b))} - \beta \sum_k N_k f_k,$$
(Claim 2), which also gives a stopping test and a faster solver: [Newton's method](/newton-raphson-method/) or a quasi-Newton method on $L$.

## Example

The data are those of the umbrella sampling page: $U(x) = 8(x^2 - 1)^2$, $s = x$, $k_B T = 1$, 17 harmonic windows at $-1.6, -1.4, \dots, 1.6$ with $\kappa = 50$, 20000 Metropolis samples per window, and 32 bins on $[-1.6, 1.6]$. The exact barrier at the bin centres is 7.884 and the exact asymmetry $F(-0.95) - F(0.95)$ is 0.

| method and seed | iterations | barrier $F(0.05) - F(0.95)$ | asymmetry | largest error, $U < 9$ |
|---|---|---|---|---|
| simple join, seed 1 | | 7.787 | $-0.195$ | 0.263 |
| WHAM, seed 1 | 1026 | 7.777 | $-0.155$ | 0.207 |
| WHAM, seed 2 | 983 | 7.883 | 0.055 | 0.303 |

With tol $= 10^{-10}$ the iteration took about 0.2 s. WHAM is only slightly better than the simple join on this easy one-dimensional case; its advantage is that it needs no order of joins and uses all overlaps at once, which matters for many windows, for two-dimensional grids and for windows of different temperatures.

**Exact histograms.** With $n_k(b) = N_k P_k(b)$ set to the exact biased bin probabilities, the iteration recovered $p$ to $1.5 \times 10^{-14}$ in 326 iterations. This checks the equations without sampling noise.

**Bin width.** Against the exact bin free energies (seed 1, tol $10^{-8}$), the root mean square error was 0.227 with 16 bins, 0.090 with 32, 0.074 with 64 and 0.077 with 128. With wide bins the bias evaluated at the bin centre is a poor value for the whole bin; with narrow bins the counts per bin are small and the statistical error stops the gain.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **Maximum likelihood.** If the counts of each window are multinomial with the biased bin probabilities $p(b) e^{-\beta w_k(b)} / \sum_{b'} p(b') e^{-\beta w_k(b')}$, the WHAM equations are the conditions for the maximum of the likelihood over $p$.
2. **The convex function.** A point $f$ is a fixed point of lines L3 to L5 if and only if it is a stationary point of $L$.
3. **Uniqueness.** If every $N_k > 0$ and the biases are finite, $L$ is convex, it does not change when all $f_k$ move by the same amount, and it is strictly convex and grows without bound in every other direction. So it has a minimizer, unique up to that shift, and the normalized $p$ is unique.
4. **Exact data.** If the histograms equal their expected values, the true bin probabilities solve the equations.

The proof does not show that the plain iteration converges for every input, and the number of iterations is a measurement.

## Complexity

Each iteration costs $O(K B)$ exponentials and logarithms, so $I$ iterations cost $O(I K B)$. The extra space is $O(K B)$ for the bias table. The number of iterations depends on the overlap of the windows: when it is poor, the iteration moves the $f_k$ slowly, and hundreds or thousands of iterations are common, as in the example. Newton's method on $L$ costs $O(K^2 B + K^3)$ per step and usually converges in a few steps.

## Properties

- **One profile, no order.** All windows enter at once, with no chain of joins.
- **Unique solution** up to the shared constant, for any data with all $N_k > 0$ and finite biases.
- **Maximum likelihood** for independent samples in each window; for correlated samples it is still consistent, and $N_k$ can be replaced by an effective number of samples.
- **Bins.** It works on a histogram, so the bin width adds a discretization error; MBAR removes the bins.
- **Works for any biases and temperatures** in the form $e^{-\beta_k (U + w_k)}$ when the energies are histogrammed too.

## Variants and improvements

- **MBAR.** The binless form, with one "bin" per sample (Shirts and Chodera 2008); it reduces to BAR for two states.
- **Multiple temperatures.** The original multiple histogram method of Ferrenberg and Swendsen (1989) combined runs at different temperatures to get the density of states.
- **Newton and quasi-Newton solvers** on the convex function $L$ converge much faster than the fixed-point iteration.
- **Error bars** by bootstrap over blocks of each window, or from the Hessian of $L$.
- **Two or more collective variables.** The equations are the same with bins on a grid.

## When to use it

Use WHAM to analyse umbrella sampling, replica exchange or multiple-temperature runs whenever the data can be put on a histogram of one or two variables. For high-dimensional data, or to avoid the bin error, use MBAR. Before WHAM, check that the windows overlap: WHAM always returns an answer, even for windows that share no bins, and the answer is then not reliable.

## Pitfalls

- **Poor overlap.** The solution is unique even when the windows barely overlap, but it is then fixed by a few counts in the tails and has a large error.
- **Underflow and overflow.** $e^{-\beta w_k(b)}$ is tiny far from the window centre; compute in the log domain.
- **Bin width.** The bias is taken at the bin centre; the bin width must be small next to $k_B T / (\kappa |s - s_k|)$ over the range each window covers.
- **Stopping too early.** A tolerance on the change of $f$ per step can stop a slowly converging iteration far from the solution; check the gradient of $L$ as well.
- **Correlated samples.** The likelihood assumes independent samples; the profile is still fine, but naive error bars are too small.
- **Samples outside the bins** must be dropped from $N_k$ too, or every window is counted with too many samples.

## Implementations

## History

Ferrenberg and Swendsen (1989) introduced the multiple histogram method to combine Monte Carlo runs at several temperatures. Kumar, Rosenberg, Bouzida, Swendsen and Kollman (1992) extended it to biased runs such as umbrella sampling windows and to free energies along a coordinate, and gave the equations in their present form. Later work wrote WHAM as a maximum likelihood problem and as the minimum of a convex function, and Shirts and Chodera (2008) removed the bins with MBAR.

## References
