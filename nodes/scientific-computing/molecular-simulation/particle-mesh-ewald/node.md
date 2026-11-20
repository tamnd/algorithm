---
tag: QV4418
kind: algorithm
slug: particle-mesh-ewald
name: Particle mesh Ewald
aliases:
- PME
area: scientific-computing/molecular-simulation
level: core
summary: Computes the reciprocal-space part of the Ewald sum by spreading charges on a grid with Lagrange interpolation and using FFTs, in O(N log N) time for N charges.
model: real-ram
complexity:
  vars: {N: the number of charges, K: the number of grid points per side, p: half the interpolation order}
  time: {worst: O(N p^3 + K^3 log K)}
  space: {extra: O(K^3 + N p)}
properties: {deterministic: true}
history:
  year: 1993
  people: [Tom Darden, Darrin York, Lee Pedersen]
  note: Darden, York and Pedersen gave the method in 1993 as an N log N replacement for the reciprocal Ewald sum in simulations of biomolecules.
prereqs: [ewald-summation, fast-fourier-transform, lagrange-interpolation]
see_also: [smooth-particle-mesh-ewald, p3m-method, particle-mesh-method, cloud-in-cell-assignment, convolution-theorem, fast-multipole-method, molecular-dynamics, periodic-boundary-conditions]
sources:
  - paper: doi:10.1063/1.464397
    title: Tom Darden, Darrin York and Lee Pedersen, Particle mesh Ewald, An N log(N) method for Ewald sums in large systems, Journal of Chemical Physics 98(12), 1993, 10089-10092
    locator: the method with Lagrange interpolation of the structure factor
  - paper: doi:10.1063/1.470117
    title: Ulrich Essmann, Lalith Perera, Max L. Berkowitz, Tom Darden, Hsing Lee and Lee G. Pedersen, A smooth particle mesh Ewald method, Journal of Chemical Physics 103(19), 1995, 8577-8593
    locator: Section III (piecewise Lagrangian interpolation and its error bound) and Table I (accuracy of Lagrange and B-spline PME)
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 6.3, Particle-particle particle-mesh methods
---

Particle mesh Ewald (PME) computes the long-range part of the electrostatic energy and forces in a periodic box, the reciprocal sum of [Ewald summation](/ewald-summation/), on a regular grid. Each charge is spread to the nearest grid points with the weights of Lagrange interpolation, so that each Fourier factor $e^{i k \cdot r_j}$ is replaced by its interpolant. The structure factor of all charges is then one 3D [fast Fourier transform](/fast-fourier-transform/) of the charge grid, and the reciprocal field is three more FFTs. The cost is $O(N \log N)$, against $O(N^{3/2})$ for the tuned Ewald sum. The real-space part of the Ewald sum is kept as it is, with a short cutoff. [Smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) replaces the Lagrange weights by B-splines, which makes the forces the exact gradient of the energy. The older [P3M method](/p3m-method/) of Hockney and Eastwood also uses a grid and FFTs, but it builds an optimal influence function for its assignment scheme instead of interpolating the Ewald sum term by term.

## In plain words

The slow part of Ewald summation adds up waves: for every wave, it visits every charge. That gets slow when there are many charges.

PME puts a grid of points into the box and gives each charge to the grid points around it, the way you share a weight between nearby posts. Once all charges sit on the grid, a fast Fourier transform finds the strength of every wave at once. The energy follows from those strengths. To get the forces, the method turns the waves back into a field on the grid, and each charge picks up the field from the same grid points it was given to. A finer grid and more points per charge give a more accurate answer.

## The problem

The input is $N$ charges $q_j$ at $r_j$ in a cubic box of side $L$, volume $V$, the Ewald parameter $\alpha$, a grid of $K$ points per side, with $K$ a power of two, and an interpolation order $2p$. We use Gaussian units. The output is an approximation of the reciprocal energy
$$E_{\text{rec}} = \frac{2\pi}{V} \sum_{m \ne 0} G(m) |S(m)|^2, \qquad G(m) = \frac{e^{-k^2/4\alpha^2}}{k^2}, \qquad S(m) = \sum_j q_j e^{i k \cdot r_j}, \qquad k = \frac{2\pi m}{L},$$
and of the reciprocal forces. With the scaled coordinates $u_j = K r_j / L$, the factor $e^{i k \cdot r_j} = e^{2\pi i m \cdot u_j / K}$ is a product of three factors, one per axis.

## The algorithm

For one axis, $W(u, g)$ is the weight of the grid point $g$ in the Lagrange interpolation of a function at $u$ from the $2p$ points $\lfloor u \rfloor - p + 1, \ldots, \lfloor u \rfloor + p$. Then $e^{2\pi i m u / K} \approx \sum_g W(u, g) e^{2\pi i m g / K}$, and $S(m) \approx \sum_g Q(g) e^{2\pi i m \cdot g / K}$ for the charge grid $Q$.

```pseudo id=main
PME-RECIPROCAL(q, r, L, α, K, p)
L1  for each charge j: u_j ← K r_j / L, and the 2p Lagrange weights W(u_ja, ·) for each axis a
L2  Q(g) ← Σ_j q_j W(u_j1, g_1) W(u_j2, g_2) W(u_j3, g_3), indices modulo K
L3  S̃ ← conj(FFT3(Q))
L4  for each m ≠ 0 with -K/2 < m_a ≤ K/2 do
L5      E ← E + (2π / V) G(m) |S̃(m)|²;  A_d(m) ← k_d G(m) S̃(m) for d = 1, 2, 3
L6  field_d(g) ← -(4π / V) Im FFT3(A_d)(g) for d = 1, 2, 3
L7  F_j ← q_j Σ_g W(u_j1, g_1) W(u_j2, g_2) W(u_j3, g_3) field(g) for each charge j
L8  return (E, F)
```

Line L5 leaves out the Nyquist component $2 m_d = K$ of $A_d$, which has no sign. The total Ewald energy adds the real-space and self parts of the [Ewald summation](/ewald-summation/) page, with a cutoff small enough that a [linked cell list](/linked-cell-list/) finds the pairs in $O(N)$ time.

## Example

Take $N = 8$ random charges with zero sum (seed 7) in a box of side $L = 6$, with $\alpha = 0.8$. The exact reciprocal energy, summed term by term over $|m_a| \le 9$, is $0.7425644480$. The table shows the relative errors of PME:

| $K$ | order $2p$ | energy error | force error |
|---|---|---|---|
| 8 | 2 | $2.51 \times 10^{-1}$ | $1.71 \times 10^{-1}$ |
| 8 | 4 | $5.85 \times 10^{-2}$ | $2.01 \times 10^{-2}$ |
| 8 | 6 | $2.15 \times 10^{-2}$ | $7.82 \times 10^{-3}$ |
| 16 | 2 | $7.57 \times 10^{-2}$ | $3.56 \times 10^{-2}$ |
| 16 | 4 | $4.62 \times 10^{-3}$ | $1.26 \times 10^{-3}$ |
| 16 | 6 | $5.32 \times 10^{-4}$ | $2.63 \times 10^{-4}$ |

The force error is the root mean square of the error vectors divided by that of the exact forces. Both errors fall with a finer grid and with a higher order, and the order helps more on the finer grid. In every run the sum of the forces is below $2 \times 10^{-16}$, zero up to rounding.

For one charge, the weights of line L1 are those of Lagrange interpolation. With $p = 1$ and $u = 2.3$, the two points are 2 and 3, with weights 0.7 and 0.3. With $p = 2$ the four points are 1 to 4, with weights $-0.0595, 0.7735, 0.3315, -0.0455$, and these reproduce $1, u, u^2, u^3$ exactly.

## Correctness

The proof below shows these claims:

1. **Interpolation error.** For each wave vector, the interpolated Fourier factor differs from the exact one by at most $\frac{(p!)^2}{(2p)!} (2\pi |m| / K)^{2p}$, a theorem. Essmann et al. (1995) give a sharper bound of the same form.
2. **What the code computes.** Lines L1 to L5 compute the reciprocal energy with the interpolated structure factor, over the wave vectors that the grid resolves.
3. **The field.** Line L6 is the exact reciprocal field of the interpolated charges at the grid points, and line L7 interpolates it back with the same weights.
4. **Zero net force.** Because the same weights spread the charges and pick up the field, the forces add up to exactly zero in exact arithmetic.

The forces are not the gradient of the computed energy, because the Lagrange weights are not differentiable at the grid points. So a PME run does not conserve energy exactly, even with a symplectic integrator. The tests check the FFT against its definition, the Lagrange weights against polynomials, the fall of the errors with $K$ and $p$, the zero net force, and the invariance under a shift by one grid spacing.

## Complexity

Spreading and interpolation cost $\Theta(N p^3)$, since each charge touches $(2p)^3$ grid points. The four FFTs of $K^3$ points cost $\Theta(K^3 \log K)$, and the loop over wave vectors costs $\Theta(K^3)$. At a fixed density and accuracy, the grid spacing is fixed, so $K^3 = \Theta(N)$ and the total is $\Theta(N \log N)$. The memory is $\Theta(K^3)$ for the grids. The real-space part costs $\Theta(N)$ with a fixed cutoff.

## Properties

- **Momentum conservation.** The forces sum to zero up to rounding, so the centre of mass does not drift.
- **No energy conservation.** The forces are not the gradient of any function, so the total energy can drift slowly over a long run.
- **Accuracy is tunable.** Error falls like $(|m| / K)^{2p}$ for each wave vector, and the large wave vectors that interpolate badly carry the small factor $G(m)$.
- **Parallel structure.** The work is local spreading and interpolation plus FFTs, the same pattern as the [particle mesh method](/particle-mesh-method/) of gravity codes.

## Variants and improvements

- **Smooth PME.** [Smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) uses cardinal B-splines and gets the forces by differentiating the weights: two FFTs, smooth forces, and energy conservation, at the cost of a small net force.
- **P3M.** The [P3M method](/p3m-method/) uses an assignment such as [cloud-in-cell](/cloud-in-cell-assignment/) and an influence function optimised for that assignment.
- **Analytic differentiation.** The forces can also come from the derivative of the weights, as in SPME, or from finite differences on the grid.
- **Other potentials.** The same mesh approach works for the $1/r^6$ dispersion sum.

## When to use it

Use PME for the long-range electrostatics of large periodic systems, such as proteins and membranes in water, where the plain Ewald sum is too slow. Today most programs use the smooth variant. PME with Lagrange interpolation still matters when the exact cancellation of the net force is more important than the conservation of energy, and as a step to understand SPME.

## Pitfalls

- **A coarse grid with a large $\alpha$.** If $\pi K / L$ is not well above $2\alpha$, the wave vectors that the grid cannot resolve carry real weight, and the error is large. Raise $K$ or lower $\alpha$ and lengthen the real-space cutoff.
- **Energy drift.** With interpolated forces, a long run can gain or lose energy. Check the drift, or use SPME.
- **Wrong signs in the FFT.** The structure factor uses $e^{+ik \cdot r}$, and most FFT libraries use $e^{-ik \cdot r}$ in the forward transform. A conjugate in the wrong place gives the right energy and wrong forces.
- **The Nyquist component.** It has no defined sign for the field. Drop it, or use an odd $K$.

## Implementations

## History

Darden, York and Pedersen (1993) introduced particle mesh Ewald with Lagrange interpolation of the Fourier factors, as an $N \log N$ method for Ewald sums in large systems. Essmann, Perera, Berkowitz, Darden, Lee and Pedersen (1995) replaced the Lagrange weights by B-splines, and compared the two in their Table I. In that paper they note that the original PME conserved momentum to machine precision, because the forces were interpolated symmetrically, but did not conserve energy. The P3M method of Hockney and Eastwood is an earlier grid method for the same sum.

## References
