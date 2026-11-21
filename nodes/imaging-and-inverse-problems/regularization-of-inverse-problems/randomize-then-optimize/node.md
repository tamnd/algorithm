---
tag: 27EKVH
kind: algorithm
slug: randomize-then-optimize
name: Randomize-then-optimize
aliases:
- RTO sampler
- RTO
- RTO-MH
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: research
summary: Draw posterior samples for an inverse problem by solving perturbed optimization problems and correcting with a Metropolis step or importance weights.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {N: the number of samples, n: the number of unknowns, M: the number of rows of the stacked residual (data plus prior), k: the Newton steps per sample, T: the cost of one evaluation of F and its Jacobian}
  time: {worst: Θ(N k (T + M n^2)), average: Θ(N k (T + M n^2)), best: Θ(N (T + M n^2))}
  space: {extra: Θ(M n + N n)}
properties: {randomized: true, exact_with_correction: true, needs_gradients: true, parallel_proposals: true}
history:
  year: 2014
  people: [Johnathan M. Bardsley, Antti Solonen, Heikki Haario, Marko Laine]
  note: "Bardsley, Solonen, Haario and Laine (2014) introduced RTO with a Metropolis-Hastings correction for nonlinear least squares posteriors. Wang, Bardsley, Solonen, Cui and Marzouk (2017) extended it to l1-type priors by a change of variables."
prereqs: [bayesian-inverse-problem, metropolis-hastings, gauss-newton-algorithm, qr-decomposition]
see_also: [preconditioned-crank-nicolson-mcmc, independence-sampler, importance-sampling, linear-gaussian-inverse-problem, maximum-a-posteriori-estimation, laplace-approximation, ensemble-kalman-inversion, tikhonov-regularization]
sources:
  - paper: doi:10.1137/140964023
    title: "Johnathan M. Bardsley, Antti Solonen, Heikki Haario and Marko Laine, Randomize-then-optimize, a method for sampling from posterior distributions in nonlinear inverse problems, SIAM Journal on Scientific Computing 36(4), 2014"
    locator: pages A1895 to A1910
  - paper: doi:10.1137/16M1080938
    title: "Zheng Wang, Johnathan M. Bardsley, Antti Solonen, Tiangang Cui and Youssef M. Marzouk, Bayesian inverse problems with l1 priors, a randomize-then-optimize approach, SIAM Journal on Scientific Computing 39(5), 2017"
    locator: pages S140 to S166
  - paper: doi:10.1017/S0962492910000061
    title: "Andrew M. Stuart, Inverse problems, a Bayesian perspective, Acta Numerica 19, 2010"
    locator: pages 451 to 559
---

Randomize-then-optimize (RTO) makes posterior samples by optimization. It applies to posteriors of least squares form, $\pi(x) \propto \exp(-\frac12\lVert F(x) - \bar y\rVert^2)$, which covers a nonlinear forward model with Gaussian noise and a Gaussian prior. Each sample perturbs the data, $\bar y + \varepsilon$ with $\varepsilon \sim N(0, I)$, and solves a projected version of the least squares problem, $Q^TF(x) = Q^T(\bar y + \varepsilon)$, where $Q$ is an orthonormal basis of the range of the Jacobian at the MAP point. For a linear model these solutions are exact, independent posterior samples. For a nonlinear model they come from a known density $q$, and the ratio $\pi/q$ can be computed, so a Metropolis-Hastings step or importance weights remove the bias. Bardsley, Solonen, Haario and Laine introduced the method in 2014. Its proposals are independent of each other, so they can be computed in parallel, and it uses the optimization tools that a MAP estimate needs anyway.

## In plain words

To find the single most likely answer, you solve one least squares problem. To get a spread of plausible answers, RTO adds random noise to the data and to the prior guess, solves the problem again, and repeats. For a linear problem the spread of these answers is exactly the right one. For a nonlinear problem it is a little off. RTO knows by how much, because it can compute the density of its own proposals. A Metropolis-Hastings step then keeps or rejects each answer so that the final set has the right distribution.

## The problem

Sample $\pi(x) \propto \exp(-\frac12\lVert F(x) - \bar y\rVert^2)$ on $\mathbb{R}^n$, with $F: \mathbb{R}^n \to \mathbb{R}^M$, $M \ge n$, smooth, with Jacobian $J$. For a [Bayesian inverse problem](/bayesian-inverse-problem/) with forward map $G$, noise $N(0, \Gamma)$ and prior $N(m_0, C)$, $L^TL = C^{-1}$,

$$F(x) = \begin{bmatrix}\Gamma^{-1/2}G(x)\\ L(x - m_0)\end{bmatrix}, \qquad \bar y = \begin{bmatrix}\Gamma^{-1/2}y\\ 0\end{bmatrix}.$$

The output is a Markov chain $x_1, \dots, x_N$ with invariant law $\pi$.

## The algorithm

```pseudo id=main
RTO-MH(F, J, ybar, x_0, N)
L1   xbar ← argmin_x ||F(x) - ybar||² by Gauss-Newton from x_0         ▷ the MAP point
L2   Q ← orthonormal basis of the columns of J(xbar)                    ▷ thin QR, M × n
L3   x ← xbar, w ← weight(xbar)
L4   for k = 1, ..., N
L5       eps ← N(0, I_M)
L6       x' ← solution of Q^T F(x') = Q^T (ybar + eps), Newton from xbar
L7       w' ← |det(Q^T J(x'))|^(-1) exp(-½||F(x') - ybar||² + ½||Q^T (F(x') - ybar)||²)
L8       with probability min(1, w' / w): x ← x', w ← w'
L9       append x to the chain
L10  return the chain and the acceptance rate
```

Line L1 computes the MAP point, the minimizer of the [Tikhonov](/tikhonov-regularization/) type functional $\frac12\lVert F(x) - \bar y\rVert^2$, with the [Gauss-Newton algorithm](/gauss-newton-algorithm/). Line L2 takes a [QR decomposition](/qr-decomposition/) of the Jacobian there. Lines L5 and L6 are the "randomize" and "optimize" steps: the solution of line L6 is a stationary point of $\lVert Q^T(F(x) - \bar y - \varepsilon)\rVert^2$. Line L7 is the weight $w = \pi/q$, where

$$q(x) \propto \lvert\det(Q^TJ(x))\rvert\exp\big(-\tfrac12\lVert Q^T(F(x) - \bar y)\rVert^2\big)$$

is the density of the points made by line L6. It follows from the change of variables $z = Q^TF(x)$, since $z = Q^T(\bar y + \varepsilon)$ is $N(Q^T\bar y, I_n)$. Line L8 is the independence Metropolis-Hastings test, done with logarithms in the code. If line L6 fails, the state stays.

For a linear $F(x) = Hx - h_0$, line L6 is the least squares problem $\min\lVert Hx - h_0 - \bar y - \varepsilon\rVert$, the weight is constant, and line L8 accepts every proposal. So for [linear Gaussian inverse problems](/linear-gaussian-inverse-problem/), RTO is the classical "perturb the data and the prior mean, then solve" method for Gaussian sampling.

## Example

A scalar nonlinear problem: $G(x) = x + x^3$, noise standard deviation $0.5$, observed $y = 1.5$, prior $N(0, 1)$. So $F(x) = [(x + x^3)/0.5;\ x]$ and $\bar y = [3;\ 0]$. The posterior mean and variance, by quadrature on 40001 points in $[-4, 4]$, are $0.7572$ and $0.04321$.

| method, 5000 draws, seed 3 | mean | variance |
|---|---|---|
| quadrature (reference) | 0.7572 | 0.04321 |
| MAP point (line L1) | 0.8400 | none |
| line L6 proposals, no correction | 0.8141 | 0.03122 |
| proposals with importance weights $w$ | 0.7530 | 0.04375 |
| RTO-MH, acceptance rate 0.836 | 0.7598 | 0.03982 |

The uncorrected proposals are biased toward the MAP point and too narrow. Both corrections remove the bias up to Monte Carlo error. The effective sample size of the importance weights, $(\sum w)^2/\sum w^2$, is 4417 of 5000, which shows that $q$ is close to $\pi$ here.

For the linear version, $G(x) = 0.1x$ with noise $0.05$, $y = 0.12$ and prior $N(0, 1)$, RTO-MH accepts all 5000 proposals (seed 1) and gives mean $0.967$ and variance $0.203$; the exact posterior is $N(0.96, 0.2)$. All numbers are measurements with fixed seeds.

## Correctness

The proof is in `proofs/correctness.md`. Under the assumption that $x \mapsto Q^TF(x)$ is one-to-one with nonsingular derivative and that the solver of line L6 finds its solution when there is one, the points of line L6 have the density $q$ above (change of variables), $\pi/q$ is proportional to the weight of line L7, and the independence Metropolis-Hastings step satisfies detailed balance for $\pi$. For an affine $F$ the assumption holds, the weight is constant, and the proposals are exact independent posterior samples. The procedure stops: every loop in it has a fixed bound. The choice of $Q$ at the MAP point is for efficiency; any $Q$ that satisfies the assumption gives a correct chain. How fast the chain mixes depends on how close $q$ is to $\pi$, which is a property of the problem, not a theorem.

## Complexity

Line L1 is one Gauss-Newton solve, and line L2 a QR factorization in $\Theta(Mn^2)$. Each Newton step of line L6 evaluates $F$ and $J$ (cost $T$), forms $Q^TJ$ in $\Theta(Mn^2)$, and solves an $n \times n$ system in $\Theta(n^3) \subseteq O(Mn^2)$. Line L7 needs one more $Q^TJ$ and a determinant. With $k$ Newton steps per sample, $N$ samples cost $\Theta(Nk(T + Mn^2))$ after the MAP point. In the linear case $k = 1$ and one factorization can be reused for all samples. Memory is $\Theta(Mn)$ for $Q$ and $J$ plus $\Theta(Nn)$ for the chain. The $N$ optimizations are independent and run in parallel; only line L8 is sequential, and it is cheap.

## Properties

- Exact for linear Gaussian problems with no rejection; exact with the correction for nonlinear ones under the injectivity assumption.
- The proposals do not depend on the current state, so they can be computed in parallel and in advance.
- Uses optimization software: a Gauss-Newton or Newton solver, Jacobians, and a QR factorization.
- Needs the least squares form of the posterior. A non-Gaussian prior must first be transformed into this form.
- Works well when the posterior is close to Gaussian near the MAP point; the acceptance rate falls as the nonlinearity grows.

## Variants and improvements

- **Importance sampling.** Use the weights $w$ of line L7 directly as self-normalized importance weights instead of line L8. All samples are used, and the [importance sampling](/importance-sampling/) effective sample size measures the quality.
- **Linear RTO for Gaussian sampling.** Perturb the data and the prior mean and solve the regularized least squares problem. With conjugate gradients this samples high-dimensional Gaussian posteriors with only matrix-vector products.
- **l1 and other non-Gaussian priors.** Wang, Bardsley, Solonen, Cui and Marzouk (2017) map an $\ell_1$ type prior to a Gaussian reference by a change of variables and apply RTO in the new variables.
- **Subspace versions.** For large $n$, restrict the nonlinear solve to a low-dimensional subspace informed by the data and treat the rest as the prior, which reduces $k$ and the cost of line L6.
- **Randomized maximum likelihood.** A related method from petroleum reservoir modeling perturbs the data and the prior sample and solves the full, unprojected problem. It is exact only in the linear case and has no simple density for a correction.

## When to use it

Use RTO when the posterior has least squares form, a MAP solver with Jacobians is available, and the posterior is not far from Gaussian, so that $q$ is close to $\pi$. It is attractive when many processors are available, because samples are independent optimizations. For linear Gaussian problems it is the method of choice for exact samples. If the posterior is strongly multimodal, the map $Q^TF$ fails to be one-to-one, or Jacobians are not available, use [pCN](/preconditioned-crank-nicolson-mcmc/) or another MCMC method instead.

## Pitfalls

- Treating the proposals of line L6 as posterior samples for a nonlinear model. They are biased; skip lines L7 and L8 only for linear models.
- A solve in line L6 that converges to a different root, or fails, when $Q^TF$ is not one-to-one. Then the density of line L7 is wrong and the chain is biased without warning. Check the residual of the solve and monitor failures.
- Solving the unprojected problem $\min\lVert F(x) - \bar y - \varepsilon\rVert^2$ in line L6. Its solutions do not have the density of line L7.
- Forgetting the determinant in line L7, or computing it for $J$ instead of $Q^TJ$. In the linear case it is constant and the mistake is invisible; in the nonlinear case it biases the result.
- Working with $w$ instead of $\log w$ in line L8. The exponentials overflow for realistic problems.
- A rank-deficient Jacobian in line L2. Then $Q$ has fewer than $n$ columns and the method is not defined; the prior part of $F$ prevents this when it is present.

## Implementations

## History

The idea of sampling a linear Gaussian posterior by perturbing the data and the prior and solving the least squares problem is older, and appears in statistics, in geostatistics and in signal processing under several names. Randomized maximum likelihood applied the same idea, without a correction, to nonlinear reservoir models in the 1990s. Bardsley, Solonen, Haario and Laine (2014) introduced the projection with $Q$, derived the proposal density and added the Metropolis-Hastings correction, which made the method exact for nonlinear problems. Wang, Bardsley, Solonen, Cui and Marzouk (2017) extended RTO to $\ell_1$ type priors, and later work studied scalable and subspace versions.

## References
