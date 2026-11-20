---
tag: 3WNNGB
kind: algorithm
slug: weak-greedy-reduced-basis
name: Weak greedy algorithm for reduced bases
area: scientific-computing/uncertainty-quantification
level: advanced
summary: "Builds a reduced basis by adding the parameter with the largest error bound. If the Kolmogorov n-width decays like n^-a or exp(-c n^a), the greedy error decays at a rate of the same type."
model: real-ram
complexity:
  vars: {n: "the number of finite element unknowns, with banded matrices in 1D", r: the final size of the reduced basis, m: the number of training parameters, Q: the number of affine terms}
  time: {offline: "O(Q^2 r^2 n + m r^4 + m Q^2 r^3)", online: "O(Q r^2 + r^3 + Q^2 r^2)"}
  space: {extra: "O(Q r n + Q^2 r^2 + m)"}
properties: {deterministic: true, exact: false, iterative: true, certified: true}
history:
  year: 2003
  people: [Karen Veroy, Christophe Prud'homme, Dimitrios V. Rovas, Anthony T. Patera]
  note: The greedy choice of parameters with an error bound comes from the reduced basis work of Patera and coworkers. The convergence rates in terms of the Kolmogorov width were proved from 2011 to 2013.
prereqs: [reduced-basis-method, kolmogorov-width, cea-lemma]
see_also: [pod-galerkin-reduced-model, empirical-interpolation-method, discrete-empirical-interpolation-method, orthogonal-matching-pursuit, gram-schmidt-process, forward-uncertainty-propagation, multifidelity-monte-carlo]
sources:
  - paper: doi:10.1137/100795772
    title: Peter Binev, Albert Cohen, Wolfgang Dahmen, Ronald DeVore, Guergana Petrova and Przemyslaw Wojtaszczyk, Convergence rates for greedy algorithms in reduced basis methods, SIAM Journal on Mathematical Analysis 43(3), 2011, 1457-1472
    locator: the weak greedy algorithm with a parameter gamma, and the polynomial rate of the greedy error under a polynomial decay of the Kolmogorov width
  - paper: doi:10.1051/m2an/2011056
    title: Annalisa Buffa, Yvon Maday, Anthony T. Patera, Christophe Prud'homme and Gabriel Turinici, A priori convergence of the greedy algorithm for the parametrized reduced basis method, ESAIM Mathematical Modelling and Numerical Analysis 46(3), 2012, 595-603
    locator: the first a priori bound of the greedy error, by a factor that grows like 2^n times the Kolmogorov width
  - paper: doi:10.1007/s00365-013-9186-2
    title: Ronald DeVore, Guergana Petrova and Przemyslaw Wojtaszczyk, Greedy algorithms for reduced bases in Banach spaces, Constructive Approximation 37(3), 2013, 455-466
    locator: "Section 3, the comparison of the greedy error with the Kolmogorov width and its corollaries for polynomial and exponential decay (Theorem 3.2 and Corollary 3.3 in the arXiv version 1204.2290)"
  - book: isbn:9783319224695
    title: Jan S. Hesthaven, Gianluigi Rozza and Benjamin Stamm, Certified Reduced Basis Methods for Parametrized Partial Differential Equations, SpringerBriefs in Mathematics, Springer, 2016
    locator: Chapter 3 (the greedy basis generation) and Chapter 4 (the error bounds that drive it)
---

The weak greedy algorithm builds the basis of a [reduced basis method](/reduced-basis-method/) one parameter at a time. It starts from an empty basis. At each step it evaluates the cheap a posteriori error bound $\Delta(\mu)$ at every parameter of a finite training set $\Xi$, picks the parameter where the bound is largest, solves the full problem there once and adds that solution to the basis. It stops when the largest bound is below a tolerance. So it needs only $r$ full solves for a basis of size $r$, and it returns a certified error bound on all of $\Xi$. The word "weak" means that the algorithm does not pick the worst approximated solution, which it cannot know, but a solution whose error is at least a fixed fraction $1/\kappa$ of the worst one. The [Kolmogorov width](/kolmogorov-width/) $d_n$ is the best error that any $n$-dimensional space can give. The theory compares the greedy error $\sigma_n$ with $d_n$: if $d_n$ decays like a power of $n$ or like an exponential of a power, then $\sigma_n$ decays in the same way, with other constants. The [POD-Galerkin model](/pod-galerkin-reduced-model/) builds its basis from many snapshots and needs no error bound.

## In plain words

You want a few full solutions that describe the solutions at all parameters. A good plan is to look where the current basis is worst and to add the solution there. You cannot measure the true error at every parameter, because that needs a full solve at each one. But the reduced basis method gives a cheap bound for each parameter, and the bound is never smaller than the error and never larger than a fixed multiple of it. So you look where the bound is largest. That point is not always the worst one, but it is never much better than the worst one, and this is enough to make the basis almost as good as the best possible basis of the same size.

## The problem

The setting is the one of the [reduced basis method](/reduced-basis-method/). A truth space $X = \mathbb{R}^n$ has the inner product $(u, v)_X = u^T X v$. For each parameter $\mu$, the truth solution $u(\mu)$ solves $A(\mu) u = F$ with $A(\mu) = \sum_{q=1}^{Q} \theta_q(\mu) A_q$. The form $a(u, v; \mu) = v^T A(\mu) u$ is coercive and continuous with constants $\alpha(\mu)$ and $\gamma(\mu)$, and a lower bound $0 < \alpha_{LB}(\mu) \le \alpha(\mu)$ is known. For a space $X_j$, $u_j(\mu)$ is the Galerkin solution in $X_j$, and

$$\Delta_j(\mu) = \frac{\|X^{-1}(F - A(\mu) u_j(\mu))\|_X}{\alpha_{LB}(\mu)}$$

is the residual bound, with $\|u(\mu) - u_j(\mu)\|_X \le \Delta_j(\mu) \le (\gamma(\mu)/\alpha_{LB}(\mu)) \|u(\mu) - u_j(\mu)\|_X$. The books write $N$ for the reduced size and $N_h$ or $\mathcal{N}$ for the truth size. This page writes $r$ and $n$.

The input is the affine data, a finite training set $\Xi \subset \mathcal{P}$ with $m$ points, a tolerance $\varepsilon_{tol} \ge 0$ and a largest size $r_{max}$. The output is a nested sequence $X_1 \subset X_2 \subset \cdots \subset X_r$ with $X_j = \operatorname{span}\{u(\mu_1), \ldots, u(\mu_j)\}$, the offline tables for $X_r$, and the number $\varepsilon_r = \max_{\mu \in \Xi} \Delta_r(\mu)$, which bounds the error on $\Xi$.

The example uses the model problem of the reduced basis page: $-u'' + \mu u = 1$ on $(0, 1)$ with zero boundary values, P1 elements with $n = 99$, $A(\mu) = K + \mu M$, $X = K + \bar{\mu} M$ with $\bar{\mu} = 10$, and $\alpha_{LB}(\mu) = \min(1, \mu/\bar{\mu})$. Then $\gamma(\mu) \le \max(1, \mu/\bar{\mu})$, so $\gamma(\mu)/\alpha_{LB}(\mu) \le 10$ for $\mu \in [1, 100]$.

## The algorithm

```pseudo id=main
WEAK-GREEDY(A_1..A_Q, F, X, α_LB, Ξ, ε_tol, r_max)
L1  μ ← argmax over μ' in Ξ of ‖F‖_X' / α_LB(μ')          ▷ the bound of the empty basis
L2  repeat
L3      solve A(μ) u = F; add u to the X-orthonormal basis Z and extend the offline tables
L4      Δ(μ') ← the online bound of the reduced basis method, for each μ' in Ξ
L5      k ← the index of the largest Δ(μ') over Ξ
L6      if Δ(μ_k) ≤ ε_tol or Z has r_max columns then
L7          return Z, the tables, the chosen parameters and ε_r = Δ(μ_k)
L8      μ ← μ_k
```

Line L1 uses the bound of the empty basis, $u_0 = 0$, whose residual is $F$. So the first parameter is the one with the smallest $\alpha_{LB}$, here $\mu = 1$. Line L3 is the only full solve of a step. It orthonormalizes the new snapshot against $Z$ in the $X$ inner product, two passes of [Gram-Schmidt](/gram-schmidt-process/), and adds the new rows and columns to the tables $Z^T A_q Z$, $F^T X^{-1} A_q z_j$ and $(A_q z_i)^T X^{-1} A_p z_j$ of the reduced basis method. Line L4 is the online stage of that method, run $m$ times. It uses only the small tables, so its cost does not depend on $n$. Lines L5 and L6 find the largest bound and test it. Line L8 moves to the chosen parameter, and the loop solves there next.

## Example

**A strong greedy step by hand.** The strong greedy algorithm uses the true distance in place of the bound. Take three vectors in $\mathbb{R}^3$ with the Euclidean norm: $v_1 = (2, 0, 0)$, $v_2 = (1, 1, 0)$ and $v_3 = (1, 1, 0.5)$. Their norms are $2$, $\sqrt{2}$ and $1.5$, so step 1 takes $v_1$ with $\sigma_0 = 2$. After the projection onto $e_1$, the remainders are $(0, 1, 0)$ and $(0, 1, 0.5)$, so step 2 takes $v_3$ with $\sigma_1 = \sqrt{1.25} \approx 1.118$. The remainder of $v_2$ after the projection onto $(0, 1, 0.5)/\sqrt{1.25}$ is $(0, 0.2, -0.4)$, so $\sigma_2 = \sqrt{0.2} \approx 0.447$. A weak greedy step with $\kappa = 2$ could also take $v_2$ in step 2, because its distance 1 is at least $\sigma_1/2$.

**The model problem.** The training set has the $m = 41$ points $\mu = 10^{i/20}$, $i = 0, \ldots, 40$, from 1 to 100, and $\varepsilon_{tol} = 10^{-6}$. The table is a measurement from the test file. Step $j$ adds $\mu_j$; the columns give the largest bound and the largest true error $\|u - u_j\|_X$ over $\Xi$ after the step, and the range of the effectivity $\Delta_j / \|u - u_j\|_X$ over $\Xi$ (at the parameters with an error above $10^{-9}$).

| $j$ | $\mu_j$ | $\varepsilon_j = \max_\Xi \Delta_j$ | $\max_\Xi \|u - u_j\|_X$ | at $\mu$ | effectivity |
|---|---|---|---|---|---|
| 0 | | 2.047 | 0.371 | 1 | |
| 1 | 1 | $2.671 \times 10^{-2}$ | $1.845 \times 10^{-2}$ | 35.48 | 1.00 to 8.15 |
| 2 | 100 | $3.336 \times 10^{-3}$ | $2.790 \times 10^{-3}$ | 17.78 | 1.00 to 8.50 |
| 3 | 3.981 | $1.262 \times 10^{-4}$ | $1.171 \times 10^{-4}$ | 44.67 | 1.00 to 8.72 |
| 4 | 44.67 | $1.851 \times 10^{-6}$ | $1.708 \times 10^{-6}$ | 70.80 | 1.00 to 9.72 |
| 5 | 70.80 | $6.448 \times 10^{-8}$ | $4.219 \times 10^{-8}$ | 19.95 | 1.01 to 44.2 |

The loop stops at $r = 5$, with 5 full solves. The bound falls by about two orders of magnitude per step. Up to $j = 4$ the effectivity is below $\gamma/\alpha_{LB} \le 10$, as the theory says. At $j = 5$ the largest effectivity is 44: the bound has reached the rounding floor of the residual, see the pitfalls. The bound is still above the error. The algorithm does not pick the worst point: after step 1 the worst error is at $\mu = 35.48$, but the largest bound is at $\mu = 100$, so step 2 takes $\mu = 100$. A strong greedy run with the true errors picks $1, 35.48, 100, 10, 70.80$, and its largest errors after steps 2, 3 and 4 are $1.934 \times 10^{-3}$, $9.861 \times 10^{-5}$ and $2.108 \times 10^{-6}$. So the weak choice costs little. On 1000 test points in $[1, 100]$ that are not in $\Xi$, the largest error after step 5 is $4.232 \times 10^{-8}$ and the largest bound is $7.273 \times 10^{-8}$.

## Correctness

The proof file shows three facts, in exact arithmetic. First, the loop stops after at most $m$ steps, and line L3 never adds a snapshot that is already in the span. The reason is that $\Delta_j(\mu_i) = 0$ at each chosen parameter, because the reduced solution reproduces the truth there. So a bound above $\varepsilon_{tol}$ is never at a chosen point. Second, if the loop stops by the tolerance, then $\|u(\mu) - u_r(\mu)\|_X \le \varepsilon_{tol}$ for every $\mu \in \Xi$, because the bound is reliable. Third, each step is a weak greedy step: with $\kappa = \max_{\Xi} \gamma(\mu)^2 / (\alpha(\mu)\, \alpha_{LB}(\mu))$,

$$\operatorname{dist}_X(u(\mu_{j+1}), X_j) \ge \frac{1}{\kappa} \max_{\mu \in \Xi} \operatorname{dist}_X(u(\mu), X_j) .$$

The proof chains [Cea's lemma](/cea-lemma/), $\|u - u_j\|_X \le (\gamma/\alpha) \operatorname{dist}_X(u, X_j)$, with the two sides of the bound. In the example $\kappa \le 100$, and the test checks this inequality at each step.

The rates are theorems of the cited papers, for a weak greedy algorithm with the parameter $1/\kappa$ on a compact set $\mathcal{K}$ of a Hilbert space, here $\mathcal{K} = \{u(\mu) : \mu \in \Xi\}$. Let $\sigma_n = \max_{\mathcal{K}} \operatorname{dist}(u, X_n)$ and let $d_n$ be the Kolmogorov $n$-width of $\mathcal{K}$. DeVore, Petrova and Wojtaszczyk prove that $d_n \le C_0 n^{-a}$ gives $\sigma_n \le C_1 n^{-a}$ with $C_1 = 2^{5a+1} \kappa^2 C_0$, and that $d_n \le C_0 e^{-c_0 n^a}$ gives $\sigma_n \le C e^{-c_1 n^a}$ with $c_1 = 2^{-1-2a} c_0$. So the exponent of a polynomial rate is kept, and the exponential rate is kept with a smaller constant in the exponent. The rates do not say that $\sigma_n$ is close to $d_n$ for each $n$.

## Complexity

In the [real RAM](/real-ram/) model, with banded matrices in 1D, step $j$ costs one full solve, $O(n)$, Gram-Schmidt against $j$ vectors, $O(j n)$, $Q$ solves with $X$, $O(Q n)$, and the new table entries, $O(Q^2 j n)$. The $m$ online solves of line L4 cost $O(m(Q j^2 + j^3 + Q^2 j^2))$. The sum over $j \le r$ is $O(Q^2 r^2 n + m r^4 + m Q^2 r^3)$. The main gain over POD is the number of full solves: $r$ in place of $m$. Memory is $O(Q r n)$ for the representers, $O(Q^2 r^2)$ for the tables and $O(m)$ for the bounds. The implementation stores the matrices dense for simplicity, so its products with $X$ cost $O(n^2)$; only its solves are tridiagonal.

## Properties

- **Few full solves.** One per basis vector.
- **Certified on the training set.** The returned $\varepsilon_r$ bounds the error at every $\mu \in \Xi$.
- **Nested.** Each basis contains the earlier ones, so a larger tolerance gives a prefix of the same basis.
- **Rate of the width.** Polynomial and exponential decay of $d_n$ carry over to $\sigma_n$.
- **Not optimal for each $n$.** $\sigma_n \ge d_n$ always, and the constants of the rate theorems can be large.
- **Deterministic.** The same input gives the same basis. Ties in line L5 go to the first index.

## Variants and improvements

- **Strong greedy.** Use the true error or the projection error in place of the bound. This needs a full solve at each training point, so it is a tool for analysis or for small problems.
- **POD-greedy.** For a time-dependent problem, add the leading [POD](/pod-galerkin-reduced-model/) modes of the error trajectory at the chosen parameter.
- **Adaptive training sets.** Refine $\Xi$ near the chosen points, or draw a new random $\Xi$ at each step, to control the error away from the training points.
- **Goal-oriented greedy.** Drive the loop with an output bound in place of the bound on the field.
- **Interpolation points.** The [empirical interpolation method](/empirical-interpolation-method/) and [DEIM](/discrete-empirical-interpolation-method/) use the same greedy idea to choose functions and points.
- **Compressed sensing analogue.** [Orthogonal matching pursuit](/orthogonal-matching-pursuit/) also adds, at each step, the element that is most correlated with the residual.

## When to use it

Use the weak greedy algorithm to build a reduced basis when a cheap and reliable error bound exists, when each full solve is costly and when the training set must be large. It is the standard offline stage of the certified reduced basis method. When no error bound exists, use POD on snapshots or a strong greedy run on a small training set. When the solution set has a slowly decaying width, for example for transport with a moving front, no linear basis is small, and the greedy loop only shows this by a slow decay of $\varepsilon_j$.

## Pitfalls

- **The rounding floor.** The bound is computed from $\rho^2$, a difference of numbers of size $\|F\|_{X'}^2$, so it cannot go much below $\sqrt{\varepsilon_{mach}}\, \|F\|_{X'} / \alpha_{LB}$, about $10^{-8}$ here. A tolerance below the floor makes the loop run to $r_{max}$, and at the floor the bound can choose a point at random. In the example the effectivity jumps to 44 at $r = 5$.
- **Certified only on $\Xi$.** The bound is computed at the training points only. A coarse $\Xi$ can miss a region with a large error. Check the bound on a fresh test set, as in the example.
- **A bad lower bound.** If $\alpha_{LB}$ is too small, the bound and $\kappa$ are large, the greedy choice is driven by the stability factor and not by the error, and the loop picks too many points where $\alpha_{LB}$ is small.
- **Dependent snapshots in floating point.** Near the floor, the chosen snapshot can be almost in the span. The implementation raises an error when the orthogonal part is below $10^{-10}$ times the snapshot norm.
- **Online work on the mesh.** If line L4 forms the reduced matrix or the residual from vectors of length $n$, each step costs $O(m Q^2 r^2 n)$, and the training sweep becomes as slow as a sweep of full solves.

## Implementations

## History

The greedy choice of parameters, driven by the a posteriori error bound, is part of the reduced basis methods of Patera, Maday and coworkers, and is usually traced to a 2003 conference paper of Veroy, Prud'homme, Rovas and Patera. Buffa, Maday, Patera, Prud'homme and Turinici gave the first a priori convergence result in 2012, with a factor that grows like $2^n$. Binev, Cohen, Dahmen, DeVore, Petrova and Wojtaszczyk introduced the parameter $\gamma$ of a weak greedy algorithm and proved in 2011 that it keeps a polynomial rate of the Kolmogorov width. DeVore, Petrova and Wojtaszczyk gave in 2013 a short direct proof that also covers exponential rates and Banach spaces.

## References
