---
tag: J4S5CW
kind: algorithm
slug: method-of-characteristics-transport
name: Method of characteristics for neutron transport
aliases:
- MOC transport
area: scientific-computing/particle-transport
level: advanced
summary: "Solves the transport equation along long tracks that cross the geometry, the standard method for detailed reactor lattice calculations."
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {T: the number of track segments, P: the number of polar angles, I: the number of iterations, R: the number of flat source regions}
  time: {worst: O(I T P)}
  space: {extra: O(T + R)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
prereqs: [discrete-ordinates-method, source-iteration, transport-sweep]
see_also: [diffusion-synthetic-acceleration, amanatides-woo-traversal, spherical-harmonics-method, gaussian-quadrature, k-eigenvalue-problem, multigroup-approximation]
sources:
  - paper: "J. R. Askew, A characteristics formulation of the neutron transport equation in complicated geometries, report AEEW-M 1108, United Kingdom Atomic Energy Authority, Winfrith, 1972"
    locator: the formulation of transport along straight characteristic lines through regions of any shape with a flat source
  - paper: doi:10.1016/j.anucene.2013.12.012
    title: William Boyd, Samuel Shaner, Lulu Li, Benoit Forget and Kord Smith, The OpenMOC method of characteristics neutral particle transport code, Annals of Nuclear Energy 68, 2014, 43-52
    locator: the description of the track laydown, the segment update with the exponential, the flat source region flux and the source iteration
---

The method of characteristics (MOC) solves the [transport equation](/linear-boltzmann-transport-equation/) by following particles along many parallel straight lines, called tracks, that cross the whole geometry. The geometry is cut into flat source regions, in which the emission of particles is taken as constant. Along each piece of a track inside one region, the transport equation is an ordinary differential equation with a constant source, and its solution is one exponential. The method adds up the change of the angular flux along all the pieces in a region to get the scalar flux there, and it repeats this as a [source iteration](/source-iteration/) until the scattering source settles. Because the tracks need no mesh that fits the cells, MOC handles the circles and rings of fuel pins exactly, and it is the standard method for detailed two-dimensional reactor lattice calculations.

## In plain words

Draw many thin parallel lines across a map of the reactor, for a set of directions. Each line crosses a row of regions. Walk along a line from the edge where nothing comes in. In each region, some of the particles you carry get absorbed or turned aside, and the region adds new particles of its own. A simple formula gives what leaves the region from what entered it.

Every time you walk through a region, note how much the count changed. Add these notes for all lines and all directions, and you know how many particles are in each region on average.

The new particles in a region depend on how many particles hit it and bounce. So you walk all the lines again with the new counts, and you repeat until the counts stop changing.

## The problem

The domain is a rectangle $[0, W] \times [0, H]$, infinite in $z$, cut into regions $i$ of the area $A_i$ with the total cross section $\Sigma_{t,i} > 0$, the scattering cross section $\Sigma_{s,i} \ge 0$ and the isotropic source $q_i$, all in units of $\mathrm{cm}^{-1}$ and particles per $\mathrm{cm}^3$ per second. The faces are vacuum. The unknown is the scalar flux $\phi = \int\psi\,d\Omega$ over the unit sphere, and the emission per steradian is $Q_i = (\Sigma_{s,i}\phi_i + q_i)/(4\pi)$. The one-speed equation is
$$\Omega\cdot\nabla\psi + \Sigma_t\psi = Q .$$

A direction has an azimuthal angle $\alpha$ in the plane and a polar angle $\theta$ to the $z$ axis. The implementation takes $n_a$ azimuthal angles $\alpha_a = \pi(a + 1/2)/n_a$ in $(0, \pi)$, each track walked in both senses, with the weight $\pi/n_a$, and $n_p$ Gauss polar cosines $\mu_p$ in $(0, 1)$ with weights $w_p$ that sum to 2, so the weights of all directions sum to $4\pi$. For each angle the tracks are straight lines at the spacing $\delta_\alpha$, and each track is cut into segments $(i, \ell)$, one for each region that it crosses, with the in-plane length $\ell$. The goal is the region fluxes $\phi_i$ of the flat source MOC equations.

## The algorithm

```pseudo id=main
MOC(regions, Σt, Σs, q, n_a, n_p, spacing, tol)
L1  for each angle α: lay tracks at the spacing δ_α and cut each into segments (i, ℓ)
L2  φ_i ← 0 for every region i
L3  repeat
L4      for each region i:  Q_i/Σt_i ← (Σs_i φ_i + q_i) / (4π Σt_i);  tally_i ← 0;  leak ← 0
L5      for each track, each polar angle p and each of the two senses:  ψ ← 0 (vacuum inflow)
L6          for each segment (i, ℓ) in the order of flight:  Δψ ← (ψ - Q_i/Σt_i)(1 - exp(-Σt_i ℓ / sin θ_p));  tally_i ← tally_i + w Δψ;  ψ ← ψ - Δψ
L7          leak ← leak + w ψ
L8      φ_i ← 4π Q_i/Σt_i + tally_i / (Σt_i A_i) for every region i
L9  until the largest change of φ is at most tol times the largest φ
```

The weight of a track in line L6 is $w = (\pi/n_a)\,w_p\,\delta_\alpha\sin\theta_p$. Line L1 runs once: the tracks and segments depend only on the geometry and the angles, and real codes store them. Line L6 is the exact solution of the equation along a straight path with a constant source: with the optical length $\tau = \Sigma_t\ell/\sin\theta$ of the 3D path, the leaving value is $\psi_{\mathrm{out}} = \psi_{\mathrm{in}}e^{-\tau} + (Q/\Sigma_t)(1 - e^{-\tau})$, and $\Delta\psi = \psi_{\mathrm{in}} - \psi_{\mathrm{out}}$. Line L8 turns the tally into the region flux: the particles lost from the tracks in a region are the particles that the region absorbs or scatters, less those it emits. Line L7 counts the particles that leave the domain. Lines L5 to L7 are a [transport sweep](/transport-sweep/) along the tracks instead of over cells, and there is no ordering problem, since every track is a line from one face to another.

The implementation lays out the tracks on a rectangle grid of $n_x \times n_y$ regions and computes the cut points of each track with the grid lines. For real lattices, a ray tracer cuts the tracks at circles and planes in the same way.

## Example

**One segment by hand.** Take $\psi_{\mathrm{in}} = 0$, $Q/\Sigma_t = 1$ and $\tau = 1.25$. Line L6 gives $\Delta\psi = (0 - 1)(1 - e^{-1.25}) = -0.7134952$, so $\psi_{\mathrm{out}} = 0.7134952$, and the mean over the segment is $1 + (0 - 0.7134952)/1.25 = 0.4292038$.

**A tall strip against the exact slab flux.** A pure absorber with $\Sigma_t = 1$ and $q = 1$ fills $W = 2$, $H = 20$, cut into $n_x = 10$ by $n_y = 5$ regions. In the middle row the strip acts as a slab of 2 mean free paths, whose exact flux is $\phi(x) = \tfrac{q}{2\Sigma_t}\left(2 - E_2(\Sigma_tx) - E_2(\Sigma_t(W - x))\right)$ with the exponential integral $E_2$ (Theorem 6 of the proof). The top and bottom faces change this by less than $3.4 \times 10^{-4}$. The exact averages of the five left cells of the middle row (the right five are the mirror image) are $0.608407$, $0.735378$, $0.798986$, $0.833535$ and $0.849027$. With no scattering, the second iteration already stops. The largest error of the middle row is:

| $n_a$ | $n_p$ | spacing (cm) | largest error | segments |
|---|---|---|---|---|
| 4 | 2 | 0.1 | $2.818 \times 10^{-2}$ | 5520 |
| 8 | 3 | 0.05 | $1.188 \times 10^{-2}$ | 21556 |
| 16 | 3 | 0.05 | $5.681 \times 10^{-3}$ | 42904 |
| 16 | 5 | 0.02 | $3.718 \times 10^{-3}$ | 107168 |
| 32 | 5 | 0.02 | $1.838 \times 10^{-3}$ | 214148 |

At $(32, 5, 0.02)$ the five values are $0.606570$, $0.734935$, $0.798985$, $0.833691$ and $0.849204$. Doubling the azimuthal angles about halves the error here, which is a measurement for this problem; the error is largest in the cells at the faces, where the flux changes fastest with the direction.

**Track areas.** The tracks of each angle cover the area of each region only approximately, since a region gets a whole number of tracks. On a $4 \times 4$ cm square with $8 \times 8$ regions, the track area of a region for one angle differs from its true area by at most $3.829 \times 10^{-3}$ of the area with $n_a = 8$ and the spacing 0.05, and by at most $4.487 \times 10^{-3}$ with $n_a = 4$ and the spacing 0.1. The total track area, averaged over the angles, is $16.0009$ and $16.0062$ against the true $16$. Line L8 uses the true area in the flat source part of the flux (Lemma 3 of the proof), so these errors do not break the balance.

**Balance and symmetry.** On the same square with a heterogeneous, symmetric map of $\Sigma_t$, $\Sigma_s$ and $q$, the iteration stops after 40 iterations, and absorption plus leakage equals the total source to $1.3 \times 10^{-12}$ of the source. The flux is symmetric under the mirror in $x$ to $1.6 \times 10^{-15}$. For a uniform medium with the scattering ratio $c = 0.7$, it takes 50 iterations, with the flux 2.3535 in a center region and 1.0032 in a corner region.

**Scattering ratio and iterations.** On a square of side 8 cm with $8 \times 8$ regions, $(n_a, n_p, \text{spacing}) = (4, 2, 0.2)$ and the tolerance $10^{-6}$, the number of iterations is 19 for $c = 0.5$, 66 for $c = 0.9$ and 125 for $c = 0.99$. The growth is that of [source iteration](/source-iteration/); leakage from the 8 mean free path square keeps the count at $c = 0.99$ much below that of an infinite medium.

## Correctness

The proofs are in the proof file. Line L6 is the exact solution along a straight segment with a flat source (Lemma 1), and the cut points of a track with the grid lines give segments that each lie in one region (Lemma 2). Line L8 equals the quadrature average of the angular flux over the region, with the track area replaced by the true area in the flat source part (Lemma 3). The sum of the tallies over all regions telescopes along every track, so absorption plus leakage equals the source in every iteration, exactly up to the change of the scattering source, for any spacing and any quadrature (Theorem 4). The iteration contracts in the maximum norm with the factor at most $c(1 + 2\varepsilon)$, where $\varepsilon$ is the largest excess of a track area over the true area (Theorem 5), so it converges to a unique fixed point when this factor is below 1. For a strip that is long in $y$, the flux in the middle tends to the exact slab flux with $E_2$ (Theorem 6), which is the reference of the example.

## Complexity

In the [real RAM](/real-ram/) model, line L6 does a constant number of operations, among them one exponential, for each segment, each polar angle and each sense, so one iteration costs $O(TP)$ for $T$ segments and $P$ polar angles, and $I$ iterations cost $O(ITP)$. Lines L4 and L8 cost $O(R)$ per iteration, which is less. Line L1 costs $O(T)$ on a grid, once. The memory is $O(T)$ for the stored segments and $O(R)$ for the fluxes, the sources and the tallies; the angular flux on a track is never stored.

The number of segments grows as the area over the spacing times the number of azimuthal angles, times the mean number of regions a unit length of track crosses. Halving the spacing or doubling $n_a$ doubles $T$, as the table of the example shows. Codes replace the exponential of line L6 by a table or a rational approximation, since it dominates the cost of the segment.

## Properties

- **Exact along each segment.** For a flat source, line L6 has no truncation error. The errors come only from the flat source, the angular quadrature and the track spacing.
- **Conservative.** Absorption plus leakage equals the source in every iteration, for any track layout (Theorem 4 of the proof).
- **Geometry free.** The regions can have any shape. The tracks only need their intersections with the region boundaries, so the circles of fuel pins need no mesh.
- **Positive.** With sources and inflows that are not negative, every $\psi$ is between its inflow and $Q/\Sigma_t$, so no flux is ever negative, unlike [diamond difference](/discrete-ordinates-method/).
- **Iterative.** It converges like [source iteration](/source-iteration/), slowly when the scattering ratio is near 1 and the regions are optically thick.

## Variants and improvements

- **Reflective and periodic boundaries.** Lattice codes lay the tracks so that each track that leaves a face meets the start of another track at the same point, a cyclic layout. The leaving value then becomes the entering value of the next track, which replaces the zero of line L5 with the value of the last iteration.
- **Linear source.** A source that is linear in each region, instead of flat, allows much larger regions for the same accuracy.
- **Acceleration.** Coarse mesh finite difference (CMFD) and other low order diffusion corrections, related to [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/), cut the number of iterations for optically thick problems with high scattering.
- **Polar quadratures.** Codes use quadratures with few polar angles fitted to the integrals of the exponential, such as that of Tabuchi and Yamamoto, so that two or three polar angles are enough for lattice cells.
- **Three dimensions.** Fully 3D MOC lays out tracks in 3D, at a much higher cost; 2D/1D methods couple a 2D MOC in each plane with a 1D solve in the axial direction.
- **Energy and eigenvalues.** With the [multigroup approximation](/multigroup-approximation/) the same sweep runs for each group, inside a power iteration for the [k-eigenvalue problem](/k-eigenvalue-problem/).

## When to use it

Use MOC for two-dimensional lattice and full core calculations where the geometry has curved boundaries and strong local changes, such as fuel pins, control rods and burnable absorbers, and where a mesh that fits the geometry would be hard to make. It suits problems with many regions and few angles per region. For simple rectangle geometries, a [discrete ordinates](/discrete-ordinates-method/) sweep on a grid uses less memory. For optically thick, highly scattering problems, add an acceleration, as in plain [source iteration](/source-iteration/).

## Pitfalls

- **Too few azimuthal angles.** The error falls slowly with $n_a$, and streaming paths between regions, such as channels, can show ray effects. Check the result with a finer angular set.
- **Track spacing too wide (line L1).** A region that only a few tracks cross gets a poor track area and a poor flux. The spacing must be small next to the smallest region.
- **Tracks on the grid lines.** A track that runs along a region boundary has segments with an unclear region. Offset the tracks to the middle of each spacing interval, as the implementation does.
- **Exponent of the 3D path (line L6).** The optical length is $\Sigma_t\ell/\sin\theta$, not $\Sigma_t\ell$. Forgetting the polar factor gives a 2D medium that is too thin.
- **Track area against true area (line L8).** Dividing the tally by the track area instead of the true area breaks the exact balance of Theorem 4 of the proof. The tally form of line L8 with the true area keeps it.
- **Cancellation for small $\tau$.** For very short segments, $1 - e^{-\tau}$ loses digits; use a series or the function expm1.

## Implementations

## History

Askew (1972) described the solution of the transport equation along straight characteristic lines through regions of any shape with a flat source, for the complicated geometries of reactor lattices. The method was taken up by lattice codes in the following decades and became the standard for detailed two-dimensional lattice calculations, with polar quadratures fitted to the exponential, cyclic tracks for reflective boundaries and low order acceleration. Open source codes such as OpenMOC, described by Boyd and coauthors (2014), give the track laydown, the segment update and the source iteration in the form of this page.

## References
