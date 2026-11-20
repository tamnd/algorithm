---
tag: HXR9T4
kind: algorithm
slug: spherical-harmonics-method
name: Spherical harmonics method
aliases:
- PN method
- PN approximation
area: scientific-computing/particle-transport
level: core
summary: "Expands the angular flux in spherical harmonics up to degree N, giving a hyperbolic system of moment equations."
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the degree of the expansion, M: the number of cells}
  time: {worst: O(M N^3)}
  space: {extra: O(M N^2)}
properties: {deterministic: true, randomized: false, exact: false, iterative: false}
prereqs: [linear-boltzmann-transport-equation, legendre-polynomials, diffusion-approximation-of-transport]
see_also: [discrete-ordinates-method, gaussian-quadrature, diffusion-synthetic-acceleration, method-of-characteristics-transport, banded-matrix, source-iteration]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the chapter on the spherical harmonics method, its boundary conditions and its relation to discrete ordinates in slab geometry
  - paper: "R. E. Marshak, Note on the spherical harmonic method as applied to the Milne problem for a sphere, Physical Review 71, 1947, 443-446"
    locator: the boundary conditions on half-range moments of the incoming flux
  - paper: "R. G. McClarren and C. D. Hauck, Robust and accurate filtered spherical harmonics expansions for radiative transfer, Journal of Computational Physics 229(16), 2010, 5597-5614"
    locator: the oscillations and negative values of truncated expansions and the filters that damp them
---

The spherical harmonics method, or $P_N$ method, approximates the angular dependence of the [transport equation](/linear-boltzmann-transport-equation/) by a finite expansion. The angular flux is written as a sum of spherical harmonics up to degree $N$, and taking moments of the transport equation gives a coupled system of first-order equations for the coefficients. In a slab the harmonics are the [Legendre polynomials](/legendre-polynomials/), and the system has $N + 1$ unknowns. It is hyperbolic, and its wave speeds are the roots of $P_{N+1}$, which are the [Gauss](/gaussian-quadrature/) nodes. For this reason $P_N$ with the Mark boundary conditions is the same discrete scheme as $S_{N+1}$ in a slab. $P_1$ is the [diffusion approximation](/diffusion-approximation-of-transport/). Unlike [discrete ordinates](/discrete-ordinates-method/), the expansion treats all directions alike, so it has no ray effects in several dimensions, but a truncated expansion can be negative.

## In plain words

At each point, particles move in all directions, and some directions carry more particles than others. The method describes this spread by a few numbers: the total, the net flow in one direction, how lopsided the spread is, and so on, each one a finer detail than the last. You keep the first few of these numbers and drop the rest.

The transport equation then becomes a small set of equations for these numbers. With only the total and the net flow you get diffusion. With more numbers you get closer to the true transport answer.

In a slab this is the same as following particles along a few special directions, so the two methods give the same numbers. The difference is how you solve: here all the unknowns are solved together in one linear system, with no repeated sweeps.

## The problem

The slab $0 \le x \le L$ has $M$ cells with the widths $h_j$, the total and scattering cross sections $\Sigma_{t,j}$ and $\Sigma_{s,j}$ in $\mathrm{cm}^{-1}$, the absorption $\Sigma_{a,j} = \Sigma_{t,j} - \Sigma_{s,j}$ and an isotropic source $q_j$. The angular flux $\psi(x, \mu)$ solves
$$\mu\,\frac{\partial\psi}{\partial x} + \Sigma_t\psi = \frac{\Sigma_s\phi + q}{2}, \qquad \phi = \int_{-1}^1\psi\,d\mu,$$
with a vacuum or a reflecting condition at each face. The $P_N$ method, for $N$ odd, writes
$$\psi(x, \mu) \approx \sum_{l=0}^{N}\frac{2l + 1}{2}\,\phi_l(x)P_l(\mu), \qquad \phi_l = \int_{-1}^1 P_l\psi\,d\mu .$$
So $\phi_0$ is the scalar flux and $\phi_1$ is the current. Multiplying the transport equation by $P_l$ and integrating, with the recurrence $(2l + 1)\mu P_l = (l + 1)P_{l+1} + lP_{l-1}$, gives the $P_N$ equations
$$\frac{l + 1}{2l + 1}\phi_{l+1}' + \frac{l}{2l + 1}\phi_{l-1}' + \sigma_l\phi_l = q\,\delta_{l0}, \qquad l = 0, \ldots, N, \quad \phi_{N+1} = 0,$$
with $\sigma_0 = \Sigma_a$ and $\sigma_l = \Sigma_t$ for $l \ge 1$. In matrix form, $Au' + Su = qe_0$ for $u = (\phi_0, \ldots, \phi_N)$. Each face needs $(N + 1)/2$ conditions:

- **Marshak**: the half-range moments $\int_0^1 P_{2i-1}\psi\,d\mu$ of the incoming flux are zero for $i = 1, \ldots, (N + 1)/2$.
- **Mark**: the incoming flux is zero at the positive roots of $P_{N+1}$.
- **Reflection**: all odd moments are zero.

## The algorithm

```pseudo id=main
PN-SLAB(N, Σt, Σs, q, h, faces, bc)
L1  A ← the (N+1) × (N+1) streaming matrix: A[l][l+1] = (l+1)/(2l+1), A[l][l-1] = l/(2l+1)
L2  add (N+1)/2 rows for the face x = 0: Marshak, Mark or reflection conditions on the moments u_0
L3  for each cell j and l = 0..N: add the row [A (u_{j+1} - u_j)/h_j + S_j (u_j + u_{j+1})/2]_l = q_j δ_{l0}
L4  add (N+1)/2 rows for the face x = L
L5  solve the banded linear system for the edge moments u_0, ..., u_M
L6  φ_j ← (u_{j,0} + u_{j+1,0})/2;  leakages ← -u_{0,1} at x = 0 and u_{M,1} at x = L
```

The unknowns are the $N + 1$ moments at each of the $M + 1$ cell edges, $(N + 1)(M + 1)$ in all. Line L3 is diamond difference: the cell value is the mean of the edge values. Lines L2 and L4 give $(N + 1)/2$ rows each, so the system is square. The rows are ordered from left to right, so the matrix is [banded](/banded-matrix/) with about $1.5(N + 1)$ diagonals on each side of the main one, and [Gaussian elimination](/gaussian-elimination/) with partial pivoting keeps the fill inside the band. The Marshak rows use the half-range integrals $\int_0^1 P_mP_l\,d\mu$, which a Gauss rule with $N + 1$ points computes exactly.

Scattering couples only $\phi_0$ to itself, through $\sigma_0 = \Sigma_a$. So line L5 includes it, and no source iteration is needed.

## Example

**The speeds by hand.** For $N = 1$, $A = \begin{pmatrix}0 & 1\\ 1/3 & 0\end{pmatrix}$, with the eigenvalues $\pm 1/\sqrt3 = \pm 0.577350$, the nodes of the two-point Gauss rule. For $N = 3$ the eigenvalues are $\pm 0.339981$ and $\pm 0.861136$, the roots of $P_4$. For $N = 1$ the equations are $\phi_1' + \Sigma_a\phi_0 = q$ and $\tfrac13\phi_0' + \Sigma_t\phi_1 = 0$, which is diffusion with $D = 1/(3\Sigma_t)$.

**Convergence in N.** Take $\Sigma_t = 1$, $c = 0.9$, $q = 1$, vacuum faces and 200 cells. The table gives the leakage through one face and the flux at the center. $P_N$ with Mark conditions gives the same numbers as $S_{N+1}$ with diamond difference on the same mesh, to $2 \times 10^{-12}$ in the measurements; the reference is $S_{16}$.

| width | $N$ | leakage, Marshak | leakage, Mark | center, Marshak | center, Mark |
|---|---|---|---|---|---|
| 2 | 1 | 0.770384 | 0.786622 | 2.668245 | 2.513710 |
| 2 | 3 | 0.747011 | 0.752284 | 2.989767 | 2.952453 |
| 2 | 5 | 0.744451 | 0.746609 | 3.014498 | 3.003413 |
| 2 | 7 | 0.743879 | 0.745022 | 3.012406 | 3.007473 |
| 2 | $S_{16}$ | 0.743626 | | 3.009311 | |
| 10 | 1 | 1.329221 | 1.378312 | 9.054526 | 9.019608 |
| 10 | 3 | 1.300960 | 1.310459 | 9.036516 | 9.032432 |
| 10 | 5 | 1.297676 | 1.301576 | 9.038102 | 9.036307 |
| 10 | 7 | 1.296625 | 1.298734 | 9.038601 | 9.037620 |
| 10 | $S_{16}$ | 1.296145 | | 9.038785 | |

$P_1$ with Marshak conditions gives the leakage $1.329221$, against $1.329219$ for the exact diffusion solution. In these runs the Marshak leakage is more accurate than the Mark leakage at every $N$, and the error of the Marshak leakage falls by a factor of about 3 to 8 per step of 2 in $N$.

**Decay constants.** In an infinite medium with $\Sigma_t = 1$, the slowest $P_N$ mode decays like $e^{-\kappa x}$ (Theorem 7 of the proof):

| $N$ | 1 | 3 | 5 | 7 | 15 | transport |
|---|---|---|---|---|---|---|
| $c = 0.5$ | 1.224745 | 0.988751 | 0.964672 | 0.959481 | 0.957521 | 0.957504 |
| $c = 0.9$ | 0.547723 | 0.525560 | 0.525430 | 0.525430 | 0.525430 | 0.525430 |

The transport values are those of the diffusion approximation page. When scattering dominates, the flux is nearly isotropic and low orders are already accurate.

**The flux at a vacuum face.** For the slab of width 2, the incoming flux $\psi(0, \mu)$, $\mu > 0$, should be 0. The expansion gives:

| $\mu$ | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|
| $P_1$ | 0.6548 | 0.4237 | 0.1926 | -0.0385 | -0.2696 | -0.3852 |
| $P_3$ | 0.5944 | 0.1800 | -0.1093 | -0.1822 | 0.0524 | 0.3136 |
| $P_7$ | 0.3600 | -0.1149 | -0.0476 | 0.0901 | -0.0924 | 0.2042 |

A polynomial in $\mu$ cannot jump from 0 to the outgoing flux at $\mu = 0$, so it oscillates and goes negative. The boundary conditions make only some moments of the incoming flux zero.

## Correctness

The proofs are in the proof file. The $P_N$ equations are the exact moment equations with $\phi_{N+1} = 0$ (Lemma 1). The matrix $A$ has the eigenvectors $(P_0(\mu_k), \ldots, P_N(\mu_k))$ with the eigenvalues $\mu_k$, the roots of $P_{N+1}$, so the system is hyperbolic with $(N + 1)/2$ incoming characteristics at each face (Theorem 2). The map from the values at the Gauss nodes to the moments is invertible, and it turns the diamond difference $P_N$ rows with Mark or reflecting conditions into the diamond difference $S_{N+1}$ equations; so these have the same solution, and it is unique when every cell absorbs (Theorem 4). The row $l = 0$ gives exact particle balance for any face conditions (Theorem 5). $P_1$ is diffusion, and its Marshak form is the edge system of [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) (Theorem 6). The decay constants are the roots of the $S_{N+1}$ dispersion function (Theorem 7). The method is a model error: as $N$ grows, the answers approach transport, which the tables measure.

## Complexity

In the [real RAM](/real-ram/) model the system has $n = (N + 1)(M + 1)$ unknowns and a lower bandwidth of about $1.5N$. Banded elimination with partial pivoting costs $O(n \cdot N \cdot N) = O(MN^3)$ operations and stores $O(MN^2)$ numbers. This does not depend on the scattering ratio. $S_{N+1}$ with [source iteration](/source-iteration/) costs $O(INM)$ for $I$ iterations, which is cheaper for small $c$ and more expensive when $I$ is large. In three dimensions there are $(N + 1)^2$ moments, and in two dimensions with symmetry $(N + 1)(N + 2)/2$; the equations are then solved by iterative methods.

## Properties

- **Hyperbolic.** The speeds are the Gauss nodes, all inside $(-1, 1)$, so information moves at most at the particle speed (Theorem 2).
- **Equal to S_(N+1) in a slab.** With Mark conditions, also on the discrete level with diamond difference (Theorem 4).
- **Rotationally invariant.** In several dimensions the spherical harmonics up to degree $N$ span a space that rotations map to itself, so no direction is preferred. This is why $P_N$ has no ray effects, which [discrete ordinates](/discrete-ordinates-method/) has.
- **Not positive.** A truncated expansion can be negative, near faces, voids and beams (the example).
- **Conservative.** The $l = 0$ row is the exact balance of each cell (Theorem 5).
- **Direct.** Scattering enters the system, so no source iteration is needed and the cost does not grow as $c \to 1$.

## Variants and improvements

- **Anisotropic scattering.** With the Legendre moments $\Sigma_{s,l}$ of the scattering kernel, the diagonal entries become $\sigma_l = \Sigma_t - \Sigma_{s,l}$. The method takes scattering of degree up to $N$ at no extra cost.
- **Simplified P_N.** The $SP_N$ equations replace the one-dimensional derivatives by three-dimensional gradients and divergences. They give a set of $(N + 1)/2$ coupled diffusion equations, which is much cheaper than full $P_N$ and is used in reactor core codes, as a rule of thumb more accurate than diffusion near interfaces.
- **Filtered P_N.** McClarren and Hauck (2010) damp the highest moments after each step or in the equations. This reduces the oscillations and negative values of the example.
- **Even-parity and odd-parity forms.** Eliminating the odd moments gives a second-order, self-adjoint system for the even ones, which suits finite elements.
- **Other boundary conditions.** Marshak and Mark conditions are the common choices; variational conditions also exist. The example shows that the choice matters for low $N$.

## When to use it

Use $P_N$ when the angular flux is smooth: media where scattering dominates, with no voids and no strong beams, and in several dimensions when ray effects of [discrete ordinates](/discrete-ordinates-method/) would be a problem. Its moment form also suits radiative transfer and coupling to other moment models. Low orders, $P_1$ to $P_3$ or $SP_3$, are a step above diffusion at a modest cost. In a slab, $P_N$ and $S_{N+1}$ are equivalent, and the choice is between a direct banded solve and a sweep with acceleration. Avoid it near vacuum faces, in voids and for streaming particles, where the expansion oscillates.

## Pitfalls

- **Even N (line L1).** With $N$ even, 0 is a root of $P_{N+1}$, so one speed is 0 and the faces need $N/2$ or $N/2 + 1$ conditions that do not split evenly. Use odd $N$.
- **Negative flux.** The reconstructed angular flux, and in hard problems even the scalar flux, can be negative. Use more moments, a filter, or a positive method.
- **Boundary conditions (lines L2 and L4).** Vacuum cannot be imposed exactly; Marshak and Mark give different answers at low $N$. A mismatch between the conditions and the expansion order is a common error.
- **The normalization.** With $\phi_l = \int P_l\psi\,d\mu$, the expansion has the factor $(2l + 1)/2$. Another convention changes the entries of $A$ and of the boundary rows.
- **The cost in several dimensions.** The number of moments grows like $N^2$, and the equations couple all of them. Large $N$ in three dimensions is expensive, which is why $SP_N$ and discrete ordinates are often used.

## Implementations

## History

Jeans introduced the spherical harmonics expansion for radiative transfer in stars in 1917. In neutron transport, Mark proposed the boundary condition at the roots of $P_{N+1}$ in reports of the 1940s, and Marshak (1947) proposed the conditions on half-range moments. The equivalence of $P_N$ and $S_{N+1}$ in slab geometry made the two methods two views of one approximation. The simplified $SP_N$ equations were proposed by Gelbard around 1960. Lewis and Miller (1984) give the method and its boundary conditions in textbook form, and McClarren and Hauck (2010) are an example of the more recent work on filters that control the oscillations.

## References
