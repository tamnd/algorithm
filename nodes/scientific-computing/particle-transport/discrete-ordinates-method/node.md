---
tag: S57PHM
kind: algorithm
slug: discrete-ordinates-method
name: Discrete ordinates method
aliases:
- SN method
area: scientific-computing/particle-transport
level: core
summary: Solves the transport equation along a finite set of directions with quadrature weights, sweeping each direction through the mesh.
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {N: the number of directions, M: the number of cells, I: the number of source iterations}
  time: {worst: O(I N M)}
  space: {extra: O(N M)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 1943
  people: [G. C. Wick, S. Chandrasekhar, B. G. Carlson]
  note: Wick replaced the angular integral of the transport equation by a Gauss quadrature in 1943, Chandrasekhar developed the method of discrete ordinates for radiative transfer in the 1940s, and Carlson made the S_N method of reactor codes at Los Alamos in the 1950s.
prereqs: [linear-boltzmann-transport-equation, gauss-legendre-quadrature, upwind-scheme]
see_also: [source-iteration, transport-sweep, diffusion-synthetic-acceleration, spherical-harmonics-method, method-of-characteristics-transport, multigroup-approximation, analog-monte-carlo-transport, k-eigenvalue-problem]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the chapters on discrete ordinates in slab geometry (Gauss quadrature, diamond difference, negative fluxes, source iteration) and in multidimensional geometry (level-symmetric quadrature, ray effects)
  - paper: doi:10.1016/S0149-1970(01)00023-3
    title: Marvin L. Adams and Edward W. Larsen, Fast iterative methods for discrete-ordinates particle transport calculations, Progress in Nuclear Energy 40(1), 2002, 3-159
    locator: the sections on the slab geometry S_N equations, the spatial discretizations and the source iteration
  - paper: "K. D. Lathrop, Ray effects in discrete ordinates equations, Nuclear Science and Engineering 32, 1968, 357-369"
    locator: the origin of ray effects in two-dimensional S_N solutions and their size
  - book: isbn:9780486605906
    title: S. Chandrasekhar, Radiative Transfer, Oxford University Press, 1950, Dover reprint 1960
    locator: the chapter on the method of discrete ordinates with Gauss points for the transfer equation in plane-parallel atmospheres
  - paper: "G. C. Wick, Über ebene Diffusionsprobleme, Zeitschrift für Physik 121, 1943, 702-718"
    locator: the replacement of the angular integral by a Gauss quadrature in plane problems
  - paper: "B. G. Carlson, Solution of the transport equation by S_n approximations, Los Alamos Scientific Laboratory report LA-1891, 1955"
    locator: the S_n method of Los Alamos
---

The discrete ordinates method, or $S_N$ method, solves the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) on a finite set of $N$ directions. It replaces the integral of the angular flux over all directions by a quadrature with weights, so the equation becomes $N$ transport equations, one per direction, coupled only through the scattering source. Each of these is solved by a sweep through the mesh in the direction of flight, and the coupling is handled by [source iteration](/source-iteration/). The [spherical harmonics method](/spherical-harmonics-method/) expands the angular flux in moments instead of sampling it at points, the [method of characteristics](/method-of-characteristics-transport/) sweeps along long tracks instead of through cells, and [Monte Carlo transport](/analog-monte-carlo-transport/) follows random particle histories.

## In plain words

Particles fly in every direction, so the unknown depends on position and on direction. The method keeps only a few directions, for example eight, chosen so that a sum over them with fixed weights gives the total over all directions very accurately.

For one direction the problem is easy. Particles that fly to the right only depend on what is to their left, so you start at the left edge and walk through the cells one by one to the right. In each cell you compute how many particles come out from how many go in and how many are made inside.

The particles that scatter change direction, so the directions are linked. You guess the scattered particles, walk all directions, add them up with the weights to get a better guess, and repeat until nothing changes.

## The problem

The model is one-speed transport in a slab $0 \le x \le L$ with isotropic scattering. The direction is the cosine $\mu \in [-1, 1]$ of the angle with the $x$ axis, the angular flux is $\psi(x, \mu)$ and the scalar flux is $\phi(x) = \int_{-1}^{1} \psi(x, \mu)\, d\mu$. With the total and scattering cross sections $\Sigma_t(x)$ and $\Sigma_s(x)$ in $\mathrm{cm}^{-1}$ and an isotropic source $q(x)$ per unit length, the equation is
$$\mu \frac{\partial \psi}{\partial x} + \Sigma_t\, \psi = \frac{\Sigma_s\, \phi + q}{2},$$
with the incoming flux $\psi(0, \mu)$ given for $\mu > 0$ and $\psi(L, \mu)$ given for $\mu < 0$. A vacuum face has zero incoming flux, and a reflecting face sends the outgoing flux back in the mirror direction. This page uses $\phi = \int_{-1}^1 \psi\, d\mu$, so the emission per unit $\mu$ is $(\Sigma_s\phi + q)/2$ and the weights sum to 2. Books that keep the azimuthal factor $2\pi$ have weights that sum to 1 or to $4\pi$, with the source divided to match. The scattering ratio is $c = \Sigma_s/\Sigma_t$.

The $S_N$ equations replace the integral by the $N$-point [Gauss-Legendre](/gauss-legendre-quadrature/) rule with nodes $\mu_n$ and weights $w_n$, $N$ even:
$$\mu_n \frac{d\psi_n}{dx} + \Sigma_t\, \psi_n = \frac{\Sigma_s\, \phi + q}{2}, \qquad \phi = \sum_{n=1}^{N} w_n \psi_n .$$
The rule is exact for polynomials in $\mu$ of degree up to $2N - 1$, it is symmetric about $\mu = 0$, and it has no node at $\mu = 0$. In space, the slab has $M$ cells $C_j = [x_{j-1/2}, x_{j+1/2}]$ of widths $\Delta x_j$ with constant data, and the scheme is diamond difference: the cell balance with the cell value equal to the mean of the two face values.

## The algorithm

```pseudo id=main
DISCRETE-ORDINATES(N, Σt, Σs, q, Δx, boundary conditions, tol)
L1  μ_1..μ_N, w_1..w_N ← the N-point Gauss-Legendre rule
L2  φ_j ← 0 for every cell j
L3  repeat
L4      S_j ← (Σs_j φ_j + q_j) / 2 for every cell j          ▷ lagged scattering source
L5      for each direction n with μ_n > 0 do
L6          ψ_in ← the incoming value at x = 0 (0, the data, or the mirror outgoing value)
L7          for j ← 1 to M do  a ← 2|μ_n| / Δx_j;  ψ_nj ← (S_j + a ψ_in) / (Σt_j + a);  ψ_in ← 2 ψ_nj − ψ_in
L8      for each direction n with μ_n < 0: the same from x = L, for j ← M down to 1
L9      φ_j ← Σ_n w_n ψ_nj for every cell j
L10 until the largest change of φ is at most tol times the largest φ
```

Line L7 is the diamond difference cell solve: the cell balance $|\mu_n|(\psi_{\mathrm{out}} - \psi_{\mathrm{in}})/\Delta x_j + \Sigma_{t,j}\psi_{nj} = S_j$ with $\psi_{nj} = (\psi_{\mathrm{in}} + \psi_{\mathrm{out}})/2$, solved for the cell value, and then the outgoing value $\psi_{\mathrm{out}} = 2\psi_{nj} - \psi_{\mathrm{in}}$ becomes the incoming value of the next cell. Lines L5 to L8 are the [transport sweep](/transport-sweep/) of each direction, and lines L3 to L10 are the [source iteration](/source-iteration/). At a reflecting face, line L6 uses the outgoing value of the mirror direction from the last iteration, which the symmetric rule provides.

## Example

**A two-cell slab by hand.** Take $S_2$, two cells of width 1 cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $\Sigma_s = 0.5\ \mathrm{cm}^{-1}$, $q = 1$ and vacuum faces. Line L1 gives $\mu = \pm 1/\sqrt{3} = \pm 0.577350$ and $w = 1, 1$, so $a = 2/\sqrt{3} = 1.154701$.

- Iteration 1, line L4: $\phi = 0$, so $S_1 = S_2 = 0.5$.
- Line L7 for $\mu > 0$: cell 1 gets $\psi = 0.5/2.154701 = 0.232051$ and passes $2 \cdot 0.232051 = 0.464102$ to cell 2, which gets $\psi = (0.5 + 1.154701 \cdot 0.464102)/2.154701 = 0.480762$ and sends $0.497423$ out at $x = 2$.
- Line L8: by symmetry, $\mu < 0$ gives $0.480762$ in cell 1 and $0.232051$ in cell 2.
- Line L9: $\phi_1 = \phi_2 = 0.232051 + 0.480762 = 0.712813$.

The two directions of each cell together give $\phi = K S$ with $K = (2 + 4a)/(1 + a)^2 = 1.425626$, and $S = \phi/4 + 1/2$. So each iteration maps $\phi$ to $K\phi/4 + K/2$, and the error falls by the factor $K/4 = 0.356406$ per iteration. The iterates are $0.712813$, $0.966864$, $1.057410$, and the fixed point is $(K/2)/(1 - K/4) = 1.107551$. At the fixed point the absorption is $(\Sigma_t - \Sigma_s)\phi \cdot 2 = 1.107551$ and each face leaks $0.446224$, so absorption plus leakage is $2.000000$, the total source.

**A pure absorber, refined in angle.** A slab of 2 mean free paths ($\Sigma_t = 1$, $\Sigma_s = 0$, $L = 2$) has the incoming flux $\psi = 1$ for all $\mu > 0$ at $x = 0$. The exact transmitted fraction of the incoming current is $2E_3(2) = 0.0602668$, where $E_3$ is the exponential integral. With 200 cells:

| $N$ | transmission | error |
|---|---|---|
| 2 | 0.031298 | $2.90 \times 10^{-2}$ |
| 4 | 0.057516 | $2.75 \times 10^{-3}$ |
| 8 | 0.059652 | $6.14 \times 10^{-4}$ |
| 16 | 0.060081 | $1.85 \times 10^{-4}$ |

The error comes from the angular quadrature. The integrand $\mu e^{-2/\mu}$ is very flat near $\mu = 0$, and few nodes fall there. A beam along $\mu = 1$ through the same slab gives $e^{-2} = 0.135335$, which line L7 reproduces to $2 \times 10^{-6}$ with 400 cells.

**Second order in space.** A slab of 10 mean free paths with $c = 0.9$, $q = 1$ and $S_8$ leaks $1.2990211$, $1.2988042$, $1.2987497$ and $1.2987360$ through each face with 20, 40, 80 and 160 cells. The observed orders from three successive meshes are $1.994$ and $1.998$, which is the second order of diamond difference.

**An infinite medium.** With reflecting faces on both sides, $\Sigma_t = 1$, $\Sigma_s = 0.5$ and $q = 1$, the solution is $\phi = q/(\Sigma_t - \Sigma_s) = 2$ in every cell, to $10^{-11}$.

## Correctness

The proofs are in the proof file. Line L7 solves the diamond difference equations of one cell exactly, and lines L5 to L8 solve those of a whole direction, because each cell needs only the cell upstream. At a fixed point of the iteration, the total absorption plus the net leakage equals the total source exactly, because the weights sum to 2 and the face fluxes telescope. With vacuum or given incoming faces and $c = \max_j \Sigma_{s,j}/\Sigma_{t,j} < 1$, the discrete equations have exactly one solution, and the iteration reaches it with the error reduced at least by the factor $c$ per iteration in a weighted $L^2$ norm. This holds for diamond difference although it can give negative values. In a pure absorber the diamond difference transmission along one direction has an error of at most $(\Sigma_t L/|\mu|)^3/(12M^2)$. The second order with scattering in the example is a measurement.

## Complexity

In the [real RAM](/real-ram/) model, line L7 costs a fixed number of operations, so one iteration costs $O(NM)$, and $I$ iterations cost $O(INM)$. The number of iterations depends on the problem: it grows like $\log(1/\mathrm{tol})/\log(1/c)$ in a thick medium, so it is large for $c$ near 1 ([source iteration](/source-iteration/) gives the analysis, and [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) removes the growth). Storing all $\psi_{nj}$ needs $O(NM)$ memory; if only $\phi$ and the face values for reflection are kept, $O(M + N)$ is enough. In three dimensions with $M$ cells and a quadrature of $N$ directions the cost of an iteration is again $O(NM)$, and for the level-symmetric $S_N$ sets the number of directions is $N(N + 2)$.

## Properties

- **Deterministic.** The result has no statistical noise; its errors come from the angular quadrature, the spatial mesh and the stopping test.
- **Conservative.** The converged solution satisfies the particle balance of each cell and of the whole slab exactly (Theorem 3 of the proof).
- **Not positive.** Diamond difference gives a negative outgoing value in a source-free cell when $\Sigma_t\Delta x > 2|\mu|$. In the test, $\mu = 0.1$, $\Sigma_t = 1$ and $\Delta x = 1$ turn the incoming value 1 into $-0.666667$.
- **Second order in space.** For smooth solutions and thin cells; the order drops where the solution has kinks, for example near a boundary where the incoming flux jumps.
- **Exact in angle up to degree $2N - 1$.** The Gauss rule integrates every polynomial in $\mu$ up to this degree, so any angular flux that is such a polynomial has an exact scalar flux.

## Variants and improvements

- **Other spatial schemes.** The step scheme (the outgoing value equals the cell value) is positive and first order. The step characteristic scheme integrates the equation exactly in each cell for a flat source. Weighted diamond schemes and linear discontinuous finite elements trade accuracy against positivity; linear discontinuous elements stay accurate with thick cells in diffusive regions, where diamond difference can oscillate and go negative.
- **Multidimensional quadratures.** In two and three dimensions, the directions form sets on the unit sphere. Level-symmetric sets have the same cosines on each axis, and product sets combine a Gauss rule in the polar cosine with equal azimuthal steps.
- **Energy and anisotropy.** The [multigroup approximation](/multigroup-approximation/) gives one $S_N$ problem per energy group, coupled by group to group scattering. Anisotropic scattering adds Legendre moments of the flux to the source.
- **Faster iterations.** [Diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) or a Krylov method such as [GMRES](/gmres/) with the sweep as the operator replaces plain source iteration in diffusive problems.
- **Eigenvalue problems.** The [k-eigenvalue problem](/k-eigenvalue-problem/) is solved by [power iteration](/power-iteration/) on the fission source, with an $S_N$ fixed source solve in each step.

## When to use it

Use the $S_N$ method for shielding, reactor core and radiation problems where the whole flux field is needed without statistical noise, the geometry fits a mesh, and the cross sections can be put into groups. In optically thick, highly scattering media, use it with an acceleration. When the geometry is very complex, use the [method of characteristics](/method-of-characteristics-transport/) or Monte Carlo; when the flux is nearly isotropic everywhere, the [diffusion approximation](/diffusion-approximation-of-transport/) is much cheaper.

## Pitfalls

- **Negative fluxes (line L7).** Thick cells give negative values, which can make a cross section feedback or a nonlinear coupling fail. A set-to-zero fixup puts the outgoing value to zero and computes the cell value again from the balance. This keeps the balance, but the scheme becomes nonlinear and only first order in those cells. Refine the mesh or use a positive scheme.
- **Ray effects.** In two and three dimensions, a localized source in a weakly scattering medium is seen only along the few quadrature directions, so the flux far away has unphysical rays (Lathrop 1968). More directions reduce them slowly; a first collision source or a Monte Carlo estimate of the uncollided flux removes their main cause.
- **The weight convention.** The source term must match the normalization of the weights. With weights that sum to 2 the source is $(\Sigma_s\phi + q)/2$; mixing this with a rule normalized to 1 or to $4\pi$ makes the scattering source wrong by a constant factor.
- **The stopping test (line L10).** A small change between iterations does not mean a small error when $c$ is near 1: the error can be about $c/(1 - c)$ times the change.
- **Reflecting faces (line L6).** The reflected value lags one iteration behind. This slows the iteration, and the quadrature must contain the mirror of each direction.
- **Isotropic incident flux.** A flux that is constant in $\mu$ on $(0, 1]$ is not a polynomial on $[-1, 1]$, and the transmitted current has the slow angular convergence of the second example.

## Implementations

## History

Wick (1943) replaced the angular integral of the transfer equation by a Gauss quadrature, and Chandrasekhar developed this method of discrete ordinates for radiative transfer in plane-parallel atmospheres; his book Radiative Transfer (1950) collects the work. At Los Alamos, Carlson made the $S_n$ method for neutron transport in the 1950s, first with a piecewise linear angular flux and then with general quadrature sets, and it became the basis of the deterministic transport codes of the following decades. Lathrop (1968) explained the ray effects of multidimensional $S_N$ solutions. Lewis and Miller (1984) give the slab and multidimensional methods in textbook form, and Adams and Larsen (2002) review the spatial schemes and the iterations.

## References
