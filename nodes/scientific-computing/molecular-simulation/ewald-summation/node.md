---
tag: 674E3C
kind: algorithm
slug: ewald-summation
name: Ewald summation
aliases:
- Ewald method
area: scientific-computing/molecular-simulation
level: core
summary: Computes the Coulomb energy and forces of charges in a periodic box by splitting each interaction into a short-range sum in real space and a smooth sum over wave vectors.
model: real-ram
complexity:
  vars: {N: the number of charges, M: the largest wave-vector index m_max}
  time: {worst: O(N^2 + N M^3)}
  space: {extra: O(N)}
properties: {deterministic: true}
history:
  year: 1921
  people: [Paul Peter Ewald, Simon W. de Leeuw, John W. Perram, Edward R. Smith]
  note: Ewald gave the method in 1921 for the potentials of crystal lattices. De Leeuw, Perram and Smith showed in 1980 how the result depends on the surroundings of the infinite system.
prereqs: [periodic-boundary-conditions, molecular-dynamics]
see_also: [particle-mesh-ewald, smooth-particle-mesh-ewald, p3m-method, fast-multipole-method, poisson-equation, linked-cell-list, lennard-jones-potential, direct-n-body-summation]
sources:
  - paper: doi:10.1002/andp.19213690304
    title: Paul P. Ewald, Die Berechnung optischer und elektrostatischer Gitterpotentiale, Annalen der Physik 369(3), 1921, 253-287
    locator: the split of the lattice sum into a real-space part and a reciprocal-space part
  - paper: doi:10.1098/rspa.1980.0135
    title: Simon W. de Leeuw, John W. Perram and Edward R. Smith, Simulation of electrostatic systems in periodic boundary conditions. I. Lattice sums and dielectric constants, Proceedings of the Royal Society of London A 373(1752), 1980, 27-56
    locator: the dependence of the sum on the order of summation and the surface term for a vacuum outside a large sphere
  - paper: doi:10.1080/00268978800101471
    title: John W. Perram, Henrik G. Petersen and Simon W. de Leeuw, An algorithm for the simulation of condensed matter which grows as the 3/2 power of the number of particles, Molecular Physics 65(4), 1988, 875-893
    locator: the choice of the splitting parameter that gives a cost of order N^(3/2)
  - paper: doi:10.1080/08927029208049126
    title: Jiri Kolafa and John W. Perram, Cutoff errors in the Ewald summation formulae for point charge systems, Molecular Simulation 9(5), 1992, 351-368
    locator: estimates of the real-space and reciprocal-space truncation errors
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 6.2, The Ewald sum
  - book: doi:10.1016/B978-0-12-267351-1.X5000-7
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: the section on Ewald sums in the chapter on long-range interactions
---

Ewald summation computes the electrostatic energy and forces of point charges in a periodic box, where each charge interacts with every other charge and with all of their periodic images. The direct sum over images converges slowly, and only conditionally: its value depends on the order of the terms. Ewald's method writes $1/r$ as $\operatorname{erfc}(\alpha r)/r + \operatorname{erf}(\alpha r)/r$. The first part is short range, so it is summed over the neighbours inside a cutoff. The second part is smooth, so its periodic sum converges fast as a Fourier series over wave vectors. A self term and, if needed, a surface term complete the result. With a well chosen $\alpha$, the cost is $O(N^{3/2})$ for $N$ charges. [Particle mesh Ewald](/particle-mesh-ewald/) and [smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) keep the real-space part and compute the reciprocal part on a grid with the fast Fourier transform, in $O(N \log N)$ time. The [P3M method](/p3m-method/) is an older grid method for the same sum.

## In plain words

Charges in a crystal or a liquid push and pull each other over long distances. In a simulation the box repeats in every direction, so each charge feels an endless number of copies. Adding up those copies one by one is slow, and the answer even depends on the order in which you add them.

Ewald's trick is to put a soft cloud of opposite charge around each point charge. The point and its cloud together act only at short range, so you add up only the near neighbours. Then you add back the clouds. A sum of smooth clouds is easy to compute as a sum of waves, and only a few waves matter. One correction removes the energy of each cloud with its own charge. The two sums together give the exact answer, and the width of the cloud only moves work from one sum to the other.

## The problem

The input is $N$ point charges $q_i$ at positions $r_i$ in a cubic box of side $L$ and volume $V = L^3$, with $\sum_i q_i = 0$, and the boundary condition at infinity. We use Gaussian units, so two charges at distance $r$ have energy $q_i q_j / r$. The output is the energy
$$E = \frac12 \sum_{i, j} {\sum_n}' \frac{q_i q_j}{|r_i - r_j + nL|}$$
and the forces $f_i = -\nabla_{r_i} E$. The sum runs over integer vectors $n$, and the prime leaves out $n = 0$ when $i = j$. The series converges only conditionally. We take the limit of sums over growing spheres of images, with either a conductor around the sphere (tin foil boundary conditions, the usual choice in simulations) or a vacuum.

## The algorithm

With $r_{ij} = r_i - r_j$, $k = 2\pi m / L$ for integer vectors $m$, and $S(k) = \sum_j q_j e^{i k \cdot r_j}$, the energy is
$$E = \underbrace{\frac12 \sum_{i,j} {\sum_n}' q_i q_j \frac{\operatorname{erfc}(\alpha |r_{ij} + nL|)}{|r_{ij} + nL|}}_{E_{\text{real}}} + \underbrace{\frac{2\pi}{V} \sum_{k \ne 0} \frac{e^{-k^2/4\alpha^2}}{k^2} |S(k)|^2}_{E_{\text{rec}}} \underbrace{- \frac{\alpha}{\sqrt\pi} \sum_i q_i^2}_{E_{\text{self}}} + E_{\text{surf}},$$
with $E_{\text{surf}} = 0$ for tin foil and $E_{\text{surf}} = \frac{2\pi}{3V} |\sum_i q_i r_i|^2$ for a vacuum.

```pseudo id=main
EWALD(q, r, L, α, r_c, m_max, surface)
L1  V ← L³;  E_real, E_rec ← 0;  f_i ← 0 for each i
L2  for each pair i ≤ j and each image n with d = |r_ij + nL| < r_c, leaving out i = j, n = 0 do
L3      E_real ← E_real + w q_i q_j erfc(α d) / d          ▷ w = 1/2 if i = j, else 1
L4      if i ≠ j then add the pair force to f_i and subtract it from f_j
L5  for each m with 0 < |m| ≤ m_max, one of each pair m, -m do
L6      k ← 2π m / L;  S ← Σ_j q_j exp(i k · r_j)
L7      E_rec ← E_rec + 2 (2π / V) G(k) |S|²              ▷ G(k) = exp(-k² / 4α²) / k²
L8      f_i ← f_i + 2 (4π / V) q_i G(k) Im(exp(i k · r_i) conj(S)) k for each i
L9  E_self ← -(α / √π) Σ_i q_i²
L10 if surface = vacuum then E_surf ← (2π / 3V) |M|², f_i ← f_i - (4π / 3V) q_i M, with M = Σ_i q_i r_i
L11 return (E_real + E_rec + E_self + E_surf, f)
```

The pair force of line L4 is $q_i q_j \bigl(\operatorname{erfc}(\alpha d)/d + \frac{2\alpha}{\sqrt\pi} e^{-\alpha^2 d^2}\bigr) (r_{ij} + nL) / d^2$. The terms for $m$ and $-m$ in line L7 are equal, since $S(-k)$ is the complex conjugate of $S(k)$, so the loop visits half of the wave vectors and doubles each term. The implementation visits all pairs; a production code finds the pairs within $r_c$ with a [linked cell list](/linked-cell-list/).

## Example

**The Madelung constant of rock salt.** Put 8 ions of charge $\pm 1$ on the corners of a cube of side $a = 1$, alternating in sign, in a periodic box of side $2$. This is the conventional cell of NaCl. The energy per ion pair is $-M q^2 / a$, where $M$ is the Madelung constant, so $M = -E / 4$. With $r_c = 8$ and $m_{\max} = 14$, so that both sums have converged:

| $\alpha$ | $E_{\text{real}}$ | $E_{\text{rec}}$ | $E_{\text{self}}$ | $M$ |
|---|---|---|---|---|
| 1.0 | $-2.485025$ | 0.008283 | $-4.513517$ | 1.7475646 |
| 1.5 | $-0.726067$ | 0.506084 | $-6.770275$ | 1.7475646 |
| 2.0 | $-0.110133$ | 2.146908 | $-9.027033$ | 1.7475646 |
| 2.5 | $-0.009747$ | 4.303281 | $-11.283792$ | 1.7475646 |

The parts change by orders of magnitude, but their sum does not. The value agrees with the known Madelung constant of NaCl, 1.747565. A small $\alpha$ puts the work in real space, and a large $\alpha$ puts it in reciprocal space. With $\alpha = 2.5$, $r_c = 2.5$ and $m_{\max} = 9$ the result is already $1.7475645946$.

**The order of summation matters.** Take four charges $1, -1, 0.5, -0.5$ at random positions (seed 5) in a box of side 3. Sum $q_i q_j / r$ directly over all images inside a sphere of $R$ boxes:

| $R$ | 4 | 8 | 16 |
|---|---|---|---|
| direct sum | $-1.1155944$ | $-1.1156453$ | $-1.1156499$ |

The spherical sums converge to the Ewald energy with a vacuum outside the sphere, $-1.1156502$. The tin foil energy is $-1.4827084$. The difference, $0.3670582$, is the surface term $\frac{2\pi}{3V}|M|^2$ of the dipole moment of the box. Neither value is wrong: they are the energies of two different physical systems.

## Correctness

The proof below shows these claims:

1. **The split is exact.** For each $\alpha > 0$, the four parts add up to the limit of the spherical sums. The erfc part converges absolutely. The erf part is the potential of a lattice of Gaussian charges, and the Poisson equation turns it into the Fourier series $E_{\text{rec}}$. The self term removes the energy of each Gaussian with its own point charge. This is a theorem.
2. **The code computes the truncated sums.** Lines L2 to L8 compute $E_{\text{real}}$ over the images inside $r_c$ and $E_{\text{rec}}$ over $|m| \le m_{\max}$.
3. **The forces are the exact gradient** of the computed energy, between the moments when an image crosses the cutoff sphere.
4. **Truncation error.** Each left-out term is at most of size $e^{-s^2}$, up to slowly changing factors, with $s = \alpha r_c = k_c / 2\alpha$. That the total error behaves the same way is a heuristic, supported by the estimates of Kolafa and Perram (1992).

The tests check the Madelung constant, the independence of $\alpha$ to $10^{-8}$, the limit of the spherical sums, the forces against central differences of the energy, zero net force, and periodicity.

## Complexity

The real-space part costs one evaluation of erfc per pair within $r_c$. The reciprocal part costs $\Theta(N)$ per wave vector. With the error level $s$ fixed, the real part costs about $N^2 s^3 / (\alpha^3 V)$ with a cell list and the reciprocal part about $N s^3 \alpha^3 V$. The product does not depend on $\alpha$, so the sum is smallest when the two are equal, at $\alpha \propto N^{1/6} / V^{1/3}$, and the total is $\Theta(N^{3/2})$ (Perram, Petersen and de Leeuw 1988). The implementation visits all pairs, so it costs $O(N^2 + N M^3)$ with $M = m_{\max}$, and $O(N)$ extra space. Mesh methods reduce the reciprocal part to $O(N \log N)$ with a fixed small cutoff.

## Properties

- **Exact in the limit.** Every truncation error goes to 0 as $r_c$ and $m_{\max}$ grow, at any fixed $\alpha$.
- **Smooth forces.** The reciprocal forces are smooth functions of the positions, and with a large enough $r_c$ the jump of the real-space energy at the cutoff is negligible.
- **Momentum.** The pair forces of line L4 cancel, and the reciprocal forces sum to zero because $\sum_i q_i e^{i k \cdot r_i} \overline{S} = |S|^2$ is real.
- **Needs a neutral box.** For a net charge the $k = 0$ term diverges. Codes add a uniform background charge, which changes the energy by a constant.

## Variants and improvements

- **Particle mesh methods.** [Particle mesh Ewald](/particle-mesh-ewald/), [smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) and [P3M](/p3m-method/) spread the charges on a grid and compute $E_{\text{rec}}$ with FFTs in $O(N \log N)$ time.
- **Other potentials.** The same split works for dispersion, $1/r^6$, and for dipoles and higher multipoles.
- **Slabs.** For a system periodic in two directions, a correction for the dipole normal to the slab, or a two-dimensional form of the sum, is used.
- **Tree and multipole methods.** The [fast multipole method](/fast-multipole-method/) computes the sum in $O(N)$ time without Fourier transforms.

## When to use it

Use the Ewald sum for charged or polar systems in a periodic box: ionic crystals, molten salts, water, proteins in solution. In its plain form it is good for a few hundred to a few thousand charges, and as a reference to test a mesh method. For large systems use a mesh method. Do not use a plain cutoff for Coulomb forces: the error is large and the structure of water and ions changes.

## Pitfalls

- **A net charge.** The sum is not defined. Neutralise the box, or know that the background charge adds a constant.
- **The wrong boundary condition.** Tin foil and vacuum give different energies and different forces when the box has a dipole moment, as the example shows. Most codes use tin foil.
- **Badly balanced parameters.** If $\alpha r_c$ is small, the real-space error is large, and if $k_c / 2\alpha$ is small, the reciprocal error is large. Check that the energy does not change with $\alpha$.
- **A cutoff longer than half the box** with the minimum image only. The real-space sum then misses images. The implementation loops over all images inside $r_c$.
- **The self term.** Forgetting it, or using it with the wrong $\alpha$, shifts the energy by a large constant, as the column $E_{\text{self}}$ shows.

## Implementations

## History

Ewald (1921) introduced the method to compute the optical and electrostatic potentials of crystal lattices. Simulations of ionic liquids and of water later used it for the Coulomb forces in a periodic box. De Leeuw, Perram and Smith (1980) worked out how the sum depends on the order of summation and on the medium around the system, which explains the surface term. Perram, Petersen and de Leeuw (1988) showed that a good choice of $\alpha$ gives a cost of order $N^{3/2}$. Darden, York and Pedersen (1993) replaced the reciprocal sum by an FFT on a grid, which led to the particle mesh Ewald methods used today.

## References
