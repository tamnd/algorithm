---
tag: WR206R
kind: algorithm
slug: smooth-particle-mesh-ewald
name: Smooth particle mesh Ewald
aliases:
- SPME
area: scientific-computing/molecular-simulation
level: advanced
summary: A variant of particle mesh Ewald that spreads charges with cardinal B-splines, so the forces are the exact gradient of a smooth approximate energy and need only two FFTs.
model: real-ram
complexity:
  vars: {N: the number of charges, K: the number of grid points per side, n: the B-spline order}
  time: {worst: O(N n^3 + K^3 log K)}
  space: {extra: O(K^3 + N n)}
properties: {deterministic: true, conservative: true}
history:
  year: 1995
  people: [Ulrich Essmann, Lalith Perera, Max L. Berkowitz, Tom Darden, Hsing Lee, Lee G. Pedersen]
  note: Essmann, Perera, Berkowitz, Darden, Lee and Pedersen replaced the Lagrange weights of PME by cardinal B-splines in 1995.
prereqs: [particle-mesh-ewald, b-spline]
see_also: [ewald-summation, p3m-method, convolution-theorem, fast-fourier-transform, molecular-dynamics, shadow-hamiltonian, particle-mesh-method, fast-multipole-method]
sources:
  - paper: doi:10.1063/1.470117
    title: Ulrich Essmann, Lalith Perera, Max L. Berkowitz, Tom Darden, Hsing Lee and Lee G. Pedersen, A smooth particle mesh Ewald method, Journal of Chemical Physics 103(19), 1995, 8577-8593
    locator: Section IV (cardinal B-spline interpolation, the factors b(m) and the analytic forces) and Section VI (results)
  - paper: doi:10.1063/1.464397
    title: Tom Darden, Darrin York and Lee Pedersen, Particle mesh Ewald, An N log(N) method for Ewald sums in large systems, Journal of Chemical Physics 98(12), 1993, 10089-10092
    locator: the original method that SPME changes
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 6.3, Particle-particle particle-mesh methods
---

Smooth particle mesh Ewald (SPME) computes the reciprocal-space part of the [Ewald sum](/ewald-summation/) on a grid, like [particle mesh Ewald](/particle-mesh-ewald/), but it spreads each charge with cardinal B-splines of order $n$ instead of Lagrange weights. B-splines are smooth, so the approximate energy is a differentiable function of the positions, and the forces are its exact gradient, computed by differentiating the weights. The method needs two FFTs per step, against four for PME, and a run with SPME forces conserves energy well. The price is that the forces no longer sum exactly to zero: the net force is a small random vector of the size of the force error. The [P3M method](/p3m-method/) also uses smooth assignment functions, which are B-splines in another form, with an optimised influence function in place of the Ewald factor.

## In plain words

Particle mesh methods share each charge between nearby grid points, find the waves of the grid with a fast Fourier transform, and get the energy from the waves. Plain PME shares charge with weights that change sharply as a charge moves past a grid point, so the forces have small jumps.

Smooth PME uses weights shaped like smooth bumps. As a charge moves, its share of each grid point changes smoothly. The energy is then a smooth function of the positions, and the force is simply how fast the energy changes when a charge moves. Because force and energy match exactly, a simulation keeps its energy well. The grid does break the exact balance of action and reaction a little, so the forces do not add up to exactly zero.

## The problem

The input is $N$ charges $q_j$ at $r_j$ in a cubic box of side $L$ and volume $V$, the Ewald parameter $\alpha$, a grid of $K$ points per side, and the B-spline order $n \ge 3$. We use Gaussian units. The output is an approximation $\tilde E$ of the reciprocal energy
$$E_{\text{rec}} = \frac{2\pi}{V} \sum_{m \ne 0} G(m) |S(m)|^2, \qquad G(m) = \frac{e^{-k^2/4\alpha^2}}{k^2}, \qquad k = \frac{2\pi m}{L},$$
with $S(m) = \sum_j q_j e^{2\pi i m \cdot u_j / K}$ and $u_j = K r_j / L$, and the forces $-\nabla \tilde E$.

## The algorithm

The cardinal B-spline $M_n$ is a piecewise polynomial of degree $n - 1$ on $[0, n]$, built by $M_2(x) = 1 - |x - 1|$ and $M_n(x) = \frac{x}{n-1} M_{n-1}(x) + \frac{n-x}{n-1} M_{n-1}(x-1)$. The Euler exponential spline gives
$$e^{2\pi i m u / K} \approx b(m) \sum_g M_n(u - g) e^{2\pi i m g / K}, \qquad b(m) = \Bigl(\sum_{j=0}^{n-1} M_n(j) e^{-2\pi i m j / K}\Bigr)^{-1},$$
exact at the grid points. So $S(m) \approx b(m_1) b(m_2) b(m_3) \sum_g Q(g) e^{2\pi i m \cdot g / K}$, with $Q(g) = \sum_j q_j \prod_a M_n(u_{ja} - g_a)$. Let $C(m) = \frac{4\pi}{V} G(m)$ and $B(m) = \prod_a |b(m_a)|^2$.

```pseudo id=main
SPME-RECIPROCAL(q, r, L, α, K, n)
L1  for each charge j and axis a: u ← K r_ja / L, the n values M_n(u - g) and M_n'(u - g) for the n grid points g ≤ u
L2  Q(g) ← Σ_j q_j M_n(u_j1 - g_1) M_n(u_j2 - g_2) M_n(u_j3 - g_3), indices modulo K
L3  F ← conj(FFT3(Q))
L4  for each m ≠ 0 with -K/2 < m_a ≤ K/2 do
L5      E ← E + ½ C(m) B(m) |F(m)|²;  P(m) ← C(m) B(m) F(m)
L6  φ ← Re FFT3(P)                               ▷ φ = Θ ∗ Q, a convolution on the grid
L7  for each charge j: g_j ← Σ_g ∇_u[M_n(u_j1 - g_1) M_n(u_j2 - g_2) M_n(u_j3 - g_3)] φ(g)
L8  return (E, F_j = -q_j (K / L) g_j for each j)
```

The derivative of line L1 is $M_n'(x) = M_{n-1}(x) - M_{n-1}(x - 1)$, so it comes from the same recursion. For odd $n$ and $2 m_a = K$, $b(m_a)$ is undefined; the code sets $B = 0$ there, as Essmann et al. suggest. The full Ewald energy adds the real-space and self parts.

## Example

Take the same system as on the [PME](/particle-mesh-ewald/) page: $N = 8$ random charges with zero sum (seed 7), $L = 6$, $\alpha = 0.8$, and the exact reciprocal energy $0.7425644480$. Relative errors of SPME, and the largest component of the net force:

| $K$ | $n$ | energy error | force error | net force |
|---|---|---|---|---|
| 8 | 4 | $1.26 \times 10^{-2}$ | $4.90 \times 10^{-2}$ | $1.0 \times 10^{-2}$ |
| 8 | 6 | $2.19 \times 10^{-3}$ | $7.83 \times 10^{-3}$ | $2.0 \times 10^{-3}$ |
| 8 | 8 | $7.89 \times 10^{-4}$ | $2.19 \times 10^{-3}$ | $6.2 \times 10^{-4}$ |
| 16 | 4 | $5.27 \times 10^{-4}$ | $4.60 \times 10^{-3}$ | $5.8 \times 10^{-4}$ |
| 16 | 6 | $1.07 \times 10^{-5}$ | $1.02 \times 10^{-4}$ | $1.6 \times 10^{-5}$ |
| 16 | 8 | $4.43 \times 10^{-7}$ | $4.29 \times 10^{-6}$ | $7.1 \times 10^{-7}$ |

On the grid with $K = 16$, order 6 gives an energy error 50 times smaller than PME with six Lagrange points, $5.32 \times 10^{-4}$. The net force shrinks with the force error, but it is never zero. The forces agree with central differences of $\tilde E$ (step $10^{-6}$, $K = 8$, $n = 4$) to $1.3 \times 10^{-9}$, which is the error of the difference formula: they are the gradient of the approximate energy, even where they are not close to the exact forces.

For $n = 4$ the B-spline is the cubic $M_4$, with $M_4(1) = M_4(3) = 1/6$ and $M_4(2) = 2/3$. A charge exactly on a grid point gives $1/6$, $2/3$, $1/6$ of its charge to that point and its two neighbours on each axis.

## Correctness

The proof below shows these claims:

1. **The spline identity is exact at the grid points,** and between them its error is bounded by a constant times $(2|m| / K)^n$, a theorem of Essmann et al. (1995).
2. **What the code computes.** Lines L1 to L5 compute $\tilde E = \frac12 \sum C B |\mathcal{F}Q|^2$, the reciprocal energy with the spline structure factor.
3. **The convolution.** Line L6 gives the real array $\phi = \Theta * Q$, and $\tilde E = \frac12 \sum_g Q(g) \phi(g)$.
4. **The forces are the exact gradient** of $\tilde E$, and they are continuous for $n \ge 3$.
5. **The net force averages to zero.** The energy is periodic under shifts of all charges by one grid spacing, so the net force has mean zero over a cell, but it is not zero in general.

The tests check the B-spline values and their derivatives, the zeros of $b$ for odd order, the gradient against central differences, the fall of the error with $K$ and $n$, and a net force that is not zero but much smaller than the forces.

## Complexity

Spreading and the forces cost $\Theta(N n^3)$. The two FFTs cost $\Theta(K^3 \log K)$ and the loop over wave vectors $\Theta(K^3)$. With a fixed grid spacing, $K^3 = \Theta(N)$, so the total is $\Theta(N \log N)$. The factors $B(m)$ depend only on $K$ and $n$ and can be computed once. Memory is $\Theta(K^3)$.

## Properties

- **Energy conserving.** The forces are the gradient of $\tilde E$, so a symplectic integrator keeps a shadow of the total energy without a drift from the mesh. This is a consequence of the [shadow Hamiltonian](/shadow-hamiltonian/) theory, given a smooth enough total potential.
- **Not momentum conserving.** The net force is the gradient of $\tilde E$ under a common shift of all charges, which is not exactly constant. Essmann et al. (1995) note that the method conserves energy but not momentum, and that the average net force can be removed.
- **High order.** With $n = 6$ or 8, a modest grid gives errors of $10^{-5}$ or better in the example.
- **Smoothness.** $M_n$ has $n - 2$ continuous derivatives, so the forces are $C^{n-3}$ in the positions.

## Variants and improvements

- **Other kernels.** The same machinery computes the dispersion sum $\sum C_6 / r^6$, and any kernel with a known Fourier transform.
- **Multipoles.** Point dipoles and higher multipoles are spread by derivatives of the B-splines.
- **Removing the net force.** Subtract the mean net force from each atom, or the mass-weighted mean, so that the centre of mass does not drift.
- **Parallel FFTs.** Large codes split the grid over processors, and some run the reciprocal part on fewer processors than the real-space part.

## When to use it

SPME is the default method for long-range electrostatics in biomolecular simulation programs. Use it whenever the system is periodic and has more than a few thousand charges. For small systems, or to test an implementation, use the plain [Ewald sum](/ewald-summation/). For systems that are not periodic, or are periodic in fewer than three directions, other methods fit better.

## Pitfalls

- **An order that is too low.** With $n = 3$ the force is only continuous, not smooth, and the accuracy is poor. Use $n \ge 4$.
- **Odd order and even $K$.** $b(m)$ is undefined at $2m = K$. Set that term to zero or use an even order.
- **Forgetting $B(m)$.** Without the factors $|b|^2$ the energy is the energy of the smeared charges, with a large error at large $|m|$.
- **The net force.** Over a long run it can accelerate the whole system. Remove it, or check the centre of mass.
- **Off-grid derivatives.** The forces need the derivative of the weights, not an interpolated field. Mixing the two loses the energy conservation.

## Implementations

## History

Darden, York and Pedersen (1993) introduced particle mesh Ewald with Lagrange interpolation. Two years later, Essmann, Perera, Berkowitz, Darden, Lee and Pedersen (1995) replaced the Lagrange weights by cardinal B-splines, an idea based on the Euler exponential spline. In the 1995 paper they used splines of order 4, 6 and 8, cubic, fifth and seventh degree, for low, medium and high accuracy. They wrote that the earlier PME obeyed Newton's third law to machine precision but did not conserve energy, and that the new method conserves energy but not momentum. The method is now the standard choice in programs for biomolecular simulation.

## References
