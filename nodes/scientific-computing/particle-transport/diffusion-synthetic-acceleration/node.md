---
tag: XAVARJ
kind: algorithm
slug: diffusion-synthetic-acceleration
name: Diffusion synthetic acceleration
area: scientific-computing/particle-transport
level: advanced
summary: "Speeds up source iteration by correcting each iterate with a diffusion solve for the error, which captures the slowly converging smooth modes."
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of directions, M: the number of cells, I: the number of iterations}
  time: {worst: O(I N M)}
  space: {extra: O(M)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
prereqs: [source-iteration, diffusion-approximation-of-transport]
see_also: [gmres, preconditioning, multigrid-method, spectral-radius, discrete-ordinates-method, transport-sweep, thomas-algorithm]
sources:
  - paper: "R. E. Alcouffe, Diffusion synthetic acceleration methods for the diamond-differenced discrete-ordinates equations, Nuclear Science and Engineering 64(2), 1977, 344-355"
    locator: the derivation of a diffusion equation consistent with diamond difference and its stability for thick cells
  - paper: "W. H. Reed, The effectiveness of acceleration techniques for iterative methods in transport theory, Nuclear Science and Engineering 45(3), 1971, 245-254"
    locator: the Fourier analysis of the diffusion correction for the continuous problem
  - paper: "E. W. Larsen, Unconditionally stable diffusion-synthetic acceleration methods for the slab geometry discrete ordinates equations. Part I: Theory, Nuclear Science and Engineering 82(1), 1982, 47-63"
    locator: the four-step procedure that derives a consistent diffusion equation from a given transport discretization
  - paper: doi:10.1016/S0149-1970(01)00023-3
    title: Marvin L. Adams and Edward W. Larsen, Fast iterative methods for discrete-ordinates particle transport calculations, Progress in Nuclear Energy 40(1), 2002, 3-159
    locator: the sections on diffusion synthetic acceleration, its Fourier analysis and the consistency requirement
  - paper: "J. S. Warsa, T. A. Wareing and J. E. Morel, Krylov iterative methods and the degraded effectiveness of diffusion synthetic acceleration for multidimensional SN calculations in problems with material discontinuities, Nuclear Science and Engineering 147(3), 2004, 218-248"
    locator: DSA as a preconditioner for Krylov methods and its loss of effectiveness in multidimensional problems with material discontinuities
---

Diffusion synthetic acceleration (DSA) makes [source iteration](/source-iteration/) fast in thick scattering media. Source iteration removes the error modes that vary fast in space in a few sweeps, but it damps the smooth modes only by the factor $c$, the scattering ratio, per sweep. These smooth modes are the ones that the [diffusion approximation](/diffusion-approximation-of-transport/) describes well. So after each sweep DSA solves a diffusion equation for the error, with the change of the scattering source as its source, and adds the result to the flux. One diffusion solve costs much less than a sweep. In an infinite medium the error then falls by at most about $0.2247c$ per iteration instead of $c$. This holds on the discrete level only if the diffusion equation is discretized consistently with the transport scheme; a diffusion equation that is discretized on its own can make the iteration diverge in thick cells.

## In plain words

Source iteration follows the particles one bounce at a time. In a thick material where almost every collision is a bounce, you need hundreds of sweeps.

The slow part of the error is smooth: it changes slowly from cell to cell. A diffusion equation gets smooth errors right, and it is cheap to solve. So after each sweep you solve a diffusion equation for the error and add that guess to the flux.

The sweep removes the rough part of the error and the diffusion solve removes the smooth part. Together they cut the error by about five times in each step, however thick the material is. The catch: the diffusion equation must be built from the same cell equations as the sweep. If it is built in another way, the two parts disagree in thick cells, and the iteration can blow up.

## The problem

The model is the one-speed slab problem of the [source iteration](/source-iteration/) page. The slab has $M$ cells with the widths $h_j$, the total and scattering cross sections $\Sigma_{t,j}$ and $\Sigma_{s,j}$ in $\mathrm{cm}^{-1}$, the absorption $\Sigma_{a,j} = \Sigma_{t,j} - \Sigma_{s,j}$ and an isotropic source $q_j$. The directions and weights are the $N$-point Gauss-Legendre rule with $N$ even, the weights sum to 2, and the equations are
$$\mu_n \frac{d\psi_n}{dx} + \Sigma_t\,\psi_n = \frac{\Sigma_s\,\phi + q}{2}, \qquad \phi = \sum_{n=1}^{N} w_n\psi_n,$$
with diamond difference in space. Each face is vacuum or reflecting. Write $\phi = T\phi + b$ for these equations, as on the source iteration page. The problem is to find the same solution $\phi$ as source iteration, in far fewer sweeps, when $c = \Sigma_s/\Sigma_t$ is near 1 and the slab is many mean free paths thick.

## The algorithm

```pseudo id=main
DSA(N, Σt, Σs, q, h, faces, tol, φ0)
L1  φ_j ← φ0_j (or 0) for every cell j
L2  repeat
L3      S_j ← (Σs_j φ_j + q_j) / 2 for every cell j               ▷ the scattering source of the last iterate
L4      φ½ ← SWEEP(S)                                           ▷ one transport sweep of all directions
L5      R_j ← Σs_j (φ½_j - φ_j) for every cell j                ▷ the source of the remaining error
L6      f ← the solution of -d/dx (D df/dx) + Σa f = R, discretized consistently with diamond difference; D = 1/(3Σt)
L7      φ_new ← φ½ + f;  d ← max_j |φ_new_j - φ_j|;  φ ← φ_new
L8  until d ≤ tol · max_j |φ_j| (or d is not finite)
```

Line L4 is the [transport sweep](/transport-sweep/) of the source iteration page, with the reflected values solved exactly. Line L5 is the change of the scattering source in this sweep. The error that is left, $\phi - \phi_{1/2}$, solves the transport equation with this source, and line L6 replaces that transport problem by a diffusion problem.

Line L6 is the part that makes DSA work. Its unknowns are the values $f_i$ at the cell edges. Write $g_j = 2/(3\Sigma_{t,j}h_j)$ and $s_j = \Sigma_{a,j}h_j/2$. The row of the inner edge $i$ between the cells $L$ and $R$ is
$$(-g_L + s_L)f_{i-1} + (g_L + g_R + s_L + s_R)f_i + (-g_R + s_R)f_{i+1} = R_Lh_L + R_Rh_R .$$
A face row keeps the terms of its one cell, and a vacuum face adds 1 to its diagonal entry (the Marshak condition: no particles enter). The correction in cell $j$ is $(f_j + f_{j+1})/2$. These rows are the diamond difference P1 equations with the current eliminated (Theorem 2 of the proof), which is the method of Alcouffe (1977). The system is tridiagonal, symmetric and positive definite, and the [Thomas algorithm](/thomas-algorithm/) solves it in $O(M)$ operations.

The implementation also has the usual cell-centered diffusion equation as the option "inconsistent", with the face coefficient $1/(h_L/(2D_L) + h_R/(2D_R))$. It is a correct discretization of diffusion, but it does not match diamond difference.

## Example

**An infinite medium by hand.** Take $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $\Sigma_s = 0.9\ \mathrm{cm}^{-1}$, $q = 1$, both faces reflecting and $\phi^{(0)} = 0$. Line L3 gives $S = 0.5$, and the sweep gives $\psi = 0.5$ in every direction, so $\phi_{1/2} = 1$. Line L5 gives $R = 0.9 \cdot (1 - 0) = 0.9$. The source is flat, so the diffusion solution has no gradient: $\Sigma_a f = R$, $f = 0.9/0.1 = 9$. Line L7 gives $\phi = 10 = q/\Sigma_a$, the exact solution, after one iteration. Source iteration needs 154 iterations to reach a change of $10^{-8}$ in the same problem.

**The Fourier factors.** In an infinite homogeneous medium the error mode $\cos(\lambda\Sigma_tx)$ is multiplied by $\omega_{SI}$ in each source iteration and by $\omega$ in each DSA iteration (Theorem 5 of the proof). For $c = 1$:

| $\lambda$ | source iteration, continuous | DSA, continuous | source iteration, $S_8$ | DSA, $S_8$ |
|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 0 |
| 0.5 | 0.927295 | 0.054838 | 0.927295 | 0.054838 |
| 1 | 0.785398 | 0.141593 | 0.785397 | 0.141589 |
| 2.525 | 0.472756 | 0.224665 | 0.471030 | 0.222127 |
| 5 | 0.274680 | 0.187642 | 0.254061 | 0.164548 |
| 20 | 0.076042 | 0.069112 | 0.029043 | 0.021761 |

Source iteration is slow for small $\lambda$, the smooth modes. DSA is worst at $\lambda \approx 2.5$, where neither the sweep nor diffusion is good, and the largest factor is $0.2247$. The largest $S_8$ factor over all $\lambda$ is $0.222386$.

**Thick cells.** Take $c = 0.99$, $S_8$, 100 equal cells, vacuum faces and $q = 0$. The Fourier columns are the largest factor over all modes on a reflecting slab of equal cells (Theorems 5 and 7 of the proof). The measured columns are the ratio of the last two changes after 40 iterations from a rough start (300 for source iteration).

| $\Sigma_th$ | consistent, Fourier | consistent, measured | inconsistent, Fourier | inconsistent, measured | source iteration, measured |
|---|---|---|---|---|---|
| 0.1 | 0.2190 | 0.2118 | 0.2152 | 0.2082 | 0.9659 |
| 1 | 0.2190 | 0.2137 | 0.7370 | 0.7161 | 0.9900 |
| 10 | 0.2190 | 0.2141 | 42.42 | 40.37 | 0.9899 |

The consistent scheme has the same rate for every cell size. The inconsistent one is as good for thin cells, slow for cells of one mean free path, and diverges for thick cells. Its rate for thick cells is near $c/(1 - c + 4/(3\Sigma_t^2h^2))$, which exceeds 1 once $\Sigma_th > 1.1664$.

**Iterations to convergence.** With $c = 0.99$, $S_8$, $q = 1$, vacuum faces and $\mathrm{tol} = 10^{-8}$:

| slab | cells | source iteration | consistent DSA | inconsistent DSA | leakage at $x = L$ |
|---|---|---|---|---|---|
| 10 mean free paths | 40 | 437 | 11 | 10 | 3.70841381 |
| 100 mean free paths | 400 | 1356 | 10 | 10 | 5.13942747 |

The cells here are 0.25 mean free paths, so both DSA schemes work. In a heterogeneous slab of 60 cells with random $\Sigma_t$ in $[0.5, 20]$, $c$ in $[0.9, 0.999]$, widths in $[0.05, 2]$ cm, one reflecting and one vacuum face, consistent DSA reaches $\mathrm{tol} = 10^{-12}$ in 17 iterations, source iteration needs 2188, and inconsistent DSA overflows after 266 iterations.

## Correctness

The proofs are in the proof file. If $\phi$ is the diamond difference solution, the DSA error satisfies $e \mapsto (T + C\Sigma_s(T - I))e$, where $C$ is the diffusion solve of line L6. So the exact solution is a fixed point, and DSA converges to the same answer as source iteration whenever the spectral radius of this map is below 1 (Theorem 3). The edge system of line L6 is exactly the diamond difference P1 system with the current eliminated, and it is symmetric positive definite if some cell absorbs or some face is vacuum (Theorems 1 and 2). For $S_2$ with reflecting faces, P1 and $S_2$ are the same equations, so one DSA iteration gives the exact solution in any heterogeneous slab (Theorem 4). On equal cells with reflecting faces, the cosine modes are eigenvectors, the flat mode is removed in one step, and the eigenvalue is the factor of the $S_N$ equations exact in space at $\lambda = 2\tan(\theta/2)/(\Sigma_th)$ (Theorem 5). From this, $|\omega| \le 3H_Nc < c$ for every cell size, with $3H_8 = 0.3799$ (Theorem 6). The inconsistent scheme has a different factor, which exceeds 1 for thick cells (Theorem 7).

## Complexity

In the [real RAM](/real-ram/) model, one iteration is one sweep, $O(NM)$ operations, plus one tridiagonal solve, $O(M)$ operations. So $I$ iterations cost $O(INM)$, and the diffusion solve adds only a fraction of about $1/N$ to the work of source iteration. The gain is in $I$. On equal cells with reflecting faces, Theorem 6 bounds the rate by $0.38c$ for $S_8$, so $I$ is at most about $\ln(\mathrm{tol})/\ln(0.38)$, which is 19 for $\mathrm{tol} = 10^{-8}$, independent of $c$, $M$ and the cell size. The measured counts are 10 to 11, against 437 to 1356 for source iteration. The extra memory is $O(M)$ for the residual, the tridiagonal system and the correction.

## Properties

- **The same answer.** DSA changes the iteration, not the equations. Its fixed point is the diamond difference solution of source iteration (Theorem 3).
- **A rate that does not depend on the scattering ratio.** On equal cells with reflecting faces, the error falls by at most $0.38c$ per iteration for $S_8$ (Theorem 6). The measured rate is about $0.22c$, which matches the Fourier maximum $0.2247c$ of the continuous problem.
- **Unconditional stability.** With the consistent diffusion equation, the bound holds for every cell thickness (Theorem 6). The inconsistent equation diverges once $\Sigma_th > 2/\sqrt{3(2c - 1)}$ on fine meshes (Theorem 7).
- **Exact for S2 with reflection.** P1 and $S_2$ are the same equations, so the correction is the exact error (Theorem 4).
- **Cheap.** One tridiagonal solve per sweep in a slab. In several dimensions, the diffusion solve is a sparse elliptic problem, which [multigrid](/multigrid-method/) or [conjugate gradients](/conjugate-gradient-method/) solve at a cost small next to a sweep, as a rule of thumb.

## Variants and improvements

- **Inconsistent DSA.** A diffusion equation discretized on its own, such as the cell-centered scheme of the implementation, is simpler and works for cells thinner than about one mean free path (Theorem 7).
- **Larsen's four-step method.** Larsen (1982) derived consistent diffusion equations for other transport discretizations by taking the P1 moments of the discrete transport equations, as Theorem 2 does for diamond difference. For linear discontinuous and multidimensional schemes the fully consistent equation is large, and partially consistent schemes are used, as described in the review of Adams and Larsen (2002).
- **DSA as a preconditioner.** Write the transport problem as $(I - T)\phi = b$ and use the diffusion solve as a [preconditioner](/preconditioning/) for [GMRES](/gmres/). Warsa, Wareing and Morel (2004) found that this keeps the speed in multidimensional problems with strong material discontinuities, where plain DSA loses much of its effectiveness.
- **Other low-order operators.** Transport synthetic acceleration uses a cheap low-order transport problem, such as $S_2$, in place of diffusion. Nonlinear schemes such as coarse mesh finite difference use a diffusion problem whose coefficients are updated from the transport solution. Both appear in the review of Adams and Larsen (2002).
- **Energy groups and eigenvalues.** In the [multigroup approximation](/multigroup-approximation/) DSA accelerates the inner iteration of each group. For the [k-eigenvalue problem](/k-eigenvalue-problem/) a similar diffusion correction accelerates the outer power iteration.

## When to use it

Use DSA when source iteration is slow: $c$ near 1 and a slab many mean free paths thick, as in reactor cores with water, or in radiative transfer in optically thick matter. Derive the diffusion equation from the transport discretization, as in line L6, or at least check its Fourier factor for thick cells. In multidimensional problems with strong material discontinuities, use DSA as a preconditioner for a Krylov method. When the problem is thin or strongly absorbing, plain source iteration is already fast and DSA brings little.

## Pitfalls

- **An inconsistent diffusion equation (line L6).** A diffusion scheme that is correct for diffusion can still make DSA diverge. In the example the cell-centered scheme has the rate 40 for cells of 10 mean free paths. Test the scheme with thick cells.
- **The wrong face condition (line L6).** Vacuum faces need the Marshak row. With a zero flux face condition the correction is wrong near the face, and the edge system does not match the P1 equations.
- **A singular system.** With $c = 1$ in every cell and both faces reflecting, the edge system is singular (Theorem 1), and so is the transport problem. Fix the flux level by another condition.
- **Negative flux fixups.** A fixup in the sweep makes the transport scheme nonlinear and no longer consistent with line L6. As a rule of thumb, the rate then becomes worse in thick cells.
- **The sign of the residual (line L5).** The source of the diffusion problem is $\Sigma_s(\phi_{1/2} - \phi)$, the change of the scattering source, not the change of the flux.
- **The weight convention.** With weights that sum to 2, the scattering source is $(\Sigma_s\phi + q)/2$ and the diffusion equation is written for $\phi$. Other conventions need matching factors in lines L3 and L6.

## Implementations

## History

Kopp proposed the synthetic method in 1963: a low-order problem corrects each transport iterate. Reed (1971) analyzed the diffusion correction by Fourier analysis for the continuous problem and found the factor $0.2247c$, but discretized forms of the method could be unstable for thick cells. Alcouffe (1977) showed that the diffusion equation must be derived from the diamond difference transport equations, and the result was stable for every cell thickness. Larsen (1982) turned this into a general procedure and proved unconditional stability in slab geometry. Adams and Larsen (2002) review the theory. Warsa, Wareing and Morel (2004) showed that DSA loses effectiveness in multidimensional problems with material discontinuities and that Krylov methods with a DSA preconditioner restore it.

## References
