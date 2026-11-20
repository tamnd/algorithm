---
tag: ZGYN85
kind: algorithm
slug: source-iteration
name: Source iteration
aliases:
- scattering source iteration
area: scientific-computing/particle-transport
level: core
summary: Solves the transport equation by repeated sweeps with the scattering source lagged, which converges slowly when the scattering ratio is near one.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of directions, M: the number of cells, I: the number of iterations}
  time: {worst: O(I N M)}
  space: {extra: O(N M)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
prereqs: [discrete-ordinates-method, transport-sweep, fixed-point-iteration]
see_also: [diffusion-synthetic-acceleration, neumann-series, power-iteration, spectral-radius, gmres, k-eigenvalue-problem, jacobi-method]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the sections on source iteration in slab geometry and its convergence in an infinite medium
  - paper: doi:10.1016/S0149-1970(01)00023-3
    title: Marvin L. Adams and Edward W. Larsen, Fast iterative methods for discrete-ordinates particle transport calculations, Progress in Nuclear Energy 40(1), 2002, 3-159
    locator: the sections on source iteration, its Fourier analysis and its stopping criteria
---

Source iteration solves the discrete [transport equation](/linear-boltzmann-transport-equation/) by fixed-point iteration on the scattering source. It takes the scalar flux of the last iterate, builds the scattering source from it, and solves the streaming and collision part for every direction exactly by a [transport sweep](/transport-sweep/). This needs no matrix, and each iteration costs one sweep. Iterate $l$ is the flux of the particles that have collided fewer than $l$ times. So the error falls by about the scattering ratio $c$ per iteration, and the method is very slow in thick media with $c$ near 1. [Diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) and Krylov methods such as [GMRES](/gmres/) are the standard ways to make it fast.

## In plain words

Particles fly, hit atoms, and either disappear or bounce off in a new direction. If you knew where the bounced particles come from, the rest would be easy: you walk each direction through the mesh once, from the side where the particles enter.

So you guess the bounced particles, walk all directions, and use the result as the next guess. The first walk counts the particles that have not bounced yet. The second walk adds the particles that bounced once, the third those that bounced twice, and so on.

This works well when most particles escape or are absorbed after a few bounces. When almost every collision is a bounce and the material is thick, particles bounce hundreds of times, and you need hundreds of walks.

## The problem

The model is the one-speed slab problem of the [discrete ordinates](/discrete-ordinates-method/) page. The slab $0 \le x \le L$ has $M$ cells with the total and scattering cross sections $\Sigma_{t,j}$ and $\Sigma_{s,j}$ in $\mathrm{cm}^{-1}$ and an isotropic source $q_j$. The directions $\mu_n$ and the weights $w_n$ are the $N$-point Gauss-Legendre rule, the weights sum to 2, and the equations are
$$\mu_n \frac{d\psi_n}{dx} + \Sigma_t\, \psi_n = \frac{\Sigma_s\, \phi + q}{2}, \qquad \phi = \sum_{n=1}^{N} w_n \psi_n,$$
with diamond difference in space. Each face is vacuum, has given incoming values, or reflects. The scattering ratio is $c = \max_j \Sigma_{s,j}/\Sigma_{t,j}$.

Write $\phi = T\phi + b$ for these equations. Here $b$ is the flux that one sweep gives from the source $q/2$ and the incoming data, and $T$ is the map that sweeps the source $\Sigma_s v/2$ with zero data. The problem is to find the fixed point $\phi$.

## The algorithm

```pseudo id=main
SOURCE-ITERATION(N, Σt, Σs, q, Δx, boundary conditions, tol, φ0)
L1  φ_j ← φ0_j (or 0) for every cell j
L2  repeat
L3      S_j ← (Σs_j φ_j + q_j) / 2 for every cell j          ▷ the scattering source of the last iterate
L4      φ_new ← SWEEP(S): for each direction solve the cells in the direction of flight, then φ_new_j ← Σ_n w_n ψ_nj
L5      d ← max_j |φ_new_j − φ_j|;  φ ← φ_new
L6  until d ≤ tol · max_j |φ_j|
```

Line L4 is the [transport sweep](/transport-sweep/) with the diamond difference cell solve of the [discrete ordinates](/discrete-ordinates-method/) page. With a reflecting face, the implementation sweeps the directions that leave through that face first, so the reflected value is current and not lagged. With two reflecting faces, it finds the incoming value of each pair of mirror directions from one scalar equation (Lemma 1 of the proof). Line L6 is a test on the change; Theorem 6 of the proof shows what it says about the error.

## Example

**An infinite medium by hand.** Take $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $\Sigma_s = 0.5\ \mathrm{cm}^{-1}$, $q = 1$, both faces reflecting and $\phi^{(0)} = 0$. The sweep of a constant source $S$ gives $\psi = S/\Sigma_t$ in every direction, so line L4 gives $\phi_{\mathrm{new}} = 2S = 0.5\phi + 1$.

| $l$ | $\phi^{(l)}$ | change $d$ |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 1.5 | 0.5 |
| 3 | 1.75 | 0.25 |
| 4 | 1.875 | 0.125 |
| 5 | 1.9375 | 0.0625 |

The exact value is $q/(\Sigma_t - \Sigma_s) = 2$. Each iteration adds one more term of $1 + c + c^2 + \cdots$, the particles after one more collision, and the error halves.

**The cost of $c$ near 1.** In the same infinite medium with $\mathrm{tol} = 10^{-8}$:

| $c$ | iterations | relative error at the stop | error / last change |
|---|---|---|---|
| 0.5 | 27 | $7.45 \times 10^{-9}$ | 1 |
| 0.9 | 154 | $8.98 \times 10^{-8}$ | 9 |
| 0.99 | 1376 | $9.86 \times 10^{-7}$ | 99 |
| 0.999 | 11509 | $9.98 \times 10^{-6}$ | 999 |

The number of iterations grows like $1/(1 - c)$, and the error left at the stop is $c/(1 - c)$ times the last change, as Theorem 6 of the proof states.

**Fourier modes.** On a reflecting slab of 40 cells of width $0.5\ \mathrm{cm}$ with $\Sigma_t = 1$, $c = 0.9$ and $S_8$, the cosine modes $\cos(\pi k (j + 1/2)/40)$ are eigenvectors of one iteration (Theorem 5 of the proof). The eigenvalue depends on $\lambda = 4\tan(\pi k/80)$:

| $k$ | $\lambda$ | eigenvalue, diamond difference | $c\arctan(\lambda)/\lambda$, continuous |
|---|---|---|---|
| 0 | 0 | 0.9 | 0.9 |
| 1 | 0.157160 | 0.892698 | 0.892698 |
| 3 | 0.473431 | 0.840567 | 0.840567 |
| 10 | 1.656854 | 0.558181 | 0.558282 |
| 39 | 101.81 | 0.00107183 | 0.013799 |

The modes that oscillate fast from cell to cell die in a few iterations. The flat and slowly varying modes keep almost all of their size, and they set the rate. These are the modes that diffusion describes well, which is why a diffusion correction removes them.

**A finite slab.** With vacuum faces the flat mode leaks out, so a thin slab converges faster. With $c = 0.99$, $S_8$ and cells of $0.25$ mean free paths, the measured ratio of successive changes is $0.60455$ for $L = 1$, $0.96592$ for $L = 10$ and $0.98997$ for $L = 100$ mean free paths. With $q = 1$ and $\mathrm{tol} = 10^{-8}$ this means 36, 437 and 1356 iterations.

## Correctness

The proofs are in the proof file. From $\phi^{(0)} = 0$, iterate $l$ is the partial sum $b + Tb + \cdots + T^{l-1}b$ of the [Neumann series](/neumann-series/), the flux of the particles with fewer than $l$ collisions. With vacuum, given or reflecting faces, $T$ is a contraction by the factor $c$ in the norm $\|v\|_t^2 = \sum_j \Sigma_{t,j}v_j^2\Delta x_j$, so for $c < 1$ the discrete equations have one solution and the iteration converges to it from every start. In a homogeneous medium with both faces reflecting, the flat mode has the eigenvalue exactly $c$, so the bound is sharp, and the cosine modes have the eigenvalues $(c/2)\sum_n w_n/(1 + \lambda^2\mu_n^2)$. If the error falls by $\rho < 1$ per iteration, the error after the stop is at most $\rho/(1 - \rho)$ times the last change.

## Complexity

In the [real RAM](/real-ram/) model, one iteration is one sweep, $O(NM)$ operations; reflection at both faces adds two sweeps per pair of directions, which is the same order. So $I$ iterations cost $O(INM)$. The infinite medium is the worst case of Theorem 3. There the relative change after $l$ iterations is $c^{l-1}(1 - c)/(1 - c^l)$, so the test of line L6 stops after about $1 + \ln(\mathrm{tol}/(1 - c))/\ln c$ iterations (a theorem for that case; it matches the table). For $c = 0.99$ this is about 100 times $\ln(10^{-2}/\mathrm{tol})$. The memory is $O(M)$ for $\phi$ and the source if each direction is added into $\phi$ as soon as it is swept; the implementation keeps the $O(NM)$ angular fluxes only to return them.

## Properties

- **Linear convergence.** The error falls by at most $c$ per iteration in the weighted norm, with any faces (Theorem 3). The bound does not depend on the mesh or on $N$.
- **Sharp in thick media.** In an infinite medium the rate is exactly $c$. In a finite slab the rate is lower, because the flat mode leaks, and it tends to $c$ as the slab gets thicker.
- **Smoothing.** Modes that vary fast in space decay fast, with the factor $c\arctan(\lambda)/\lambda$ in the continuous problem. Only the smooth modes are slow.
- **A physical meaning.** Each iteration adds one generation of scattered particles, so the iterates from zero increase toward the solution when the exact transport operator is used and the data are not negative. Diamond difference can give negative values, so this monotone growth is not guaranteed for it.
- **Matrix free.** The only operation is a sweep, which inverts the streaming and collision operator in $O(NM)$ operations.

## Variants and improvements

- **Diffusion synthetic acceleration.** After each sweep, solve a diffusion equation for the error and add the correction. By the Fourier analysis of the continuous problem in an infinite medium, this reduces the factor to at most about $0.2247c$, if the diffusion equation is discretized consistently with the transport scheme ([diffusion synthetic acceleration](/diffusion-synthetic-acceleration/)).
- **Krylov methods.** The fixed point $\phi = T\phi + b$ is the linear system $(I - T)\phi = b$. [GMRES](/gmres/) solves it with one sweep per matrix-vector product. As a rule of thumb from the review of Adams and Larsen (2002), it converges much faster than plain iteration for $c$ near 1, and more so with a diffusion [preconditioner](/preconditioning/).
- **Inner and outer iterations.** With energy groups ([multigroup approximation](/multigroup-approximation/)), source iteration is the inner iteration of each group, and an outer [Gauss-Seidel](/gauss-seidel-method/) iteration over the groups handles the scattering between groups. For a reactor, the [k-eigenvalue problem](/k-eigenvalue-problem/) adds an outer [power iteration](/power-iteration/) on the fission source.
- **Other sweeps.** The same iteration works with any spatial scheme for line L4 (step, linear discontinuous, characteristics) and in two and three dimensions; the contraction factor $c$ of the continuous problem stays the same.

## When to use it

Use plain source iteration when particles collide only a few times before they are absorbed or escape: $c$ well below 1, or a slab that is thin in mean free paths. Shielding problems with strong absorption are of this type. In thick scattering media, such as a reactor core with water or radiative transfer in optically thick matter, use it only inside an accelerated or Krylov method. It is also the reference iteration against which accelerations are measured.

## Pitfalls

- **False convergence (line L6).** A small change does not mean a small error. With $c = 0.99$ the error can be 99 times the last change. Divide the tolerance by $c/(1 - c)$, or estimate the rate from the ratio of successive changes and use Theorem 6.
- **Slow convergence that looks like stagnation.** For $c = 0.999$ the change falls by 0.1 percent per iteration. A run with a cap on the number of iterations can stop far from the solution without a warning.
- **Lagged reflection.** If the reflected value is taken from the last iteration, as in the discrete ordinates page, reflection adds its own slow mode. Sweeping the leaving directions first (one reflecting face) or solving for the incoming value (two faces) avoids this.
- **The weight convention (line L3).** The factor $1/2$ belongs to weights that sum to 2. With weights that sum to 1 or to $4\pi$ the source must be divided to match, or the effective $c$ is wrong.
- **Negative values.** Diamond difference with thick cells gives negative angular fluxes. The iteration still converges (Theorem 3), but a negative flux fixup makes the sweep nonlinear, and the convergence proof no longer applies.

## Implementations

## History

Source iteration is the natural way to solve the discrete ordinates equations, and it was used from the first $S_N$ codes of the 1950s on. Its slow convergence for $c$ near 1 led to the synthetic methods, in which a cheaper low-order problem corrects each transport iterate: Kopp proposed the idea in 1963, and Alcouffe (1977) showed how to make the diffusion correction stable with diamond difference. Lewis and Miller (1984) give the iteration and its infinite medium rate in textbook form. Adams and Larsen (2002) review its Fourier analysis together with the accelerations and the Krylov methods that replace it.

## References
