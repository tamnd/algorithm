---
tag: WE4PJK
kind: definition
slug: radial-distribution-function
name: Radial distribution function
aliases:
- pair correlation function
area: scientific-computing/molecular-simulation
level: intro
summary: The density of particles at distance r from a given particle divided by the bulk density, estimated from a histogram of pair distances.
prereqs: [periodic-boundary-conditions]
see_also: [molecular-dynamics, lennard-jones-potential, canonical-ensemble, iterative-boltzmann-inversion, kernel-density-estimation, linked-cell-list, interatomic-potential, histogram]
sources:
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 2.6 (structural quantities, the definition of g(r) and its use for the energy and the pressure) and Section 8.2 (liquid structure, the histogram method and its normalization)
  - book: isbn:9780123870322
    title: Jean-Pierre Hansen and Ian R. McDonald, Theory of Simple Liquids, with Applications to Soft Matter, fourth edition, Academic Press, 2013
    locator: the chapters on statistical mechanics and on the static structure of liquids (particle densities, distribution functions and the structure factor)
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Chapter 4, the measurement of the radial distribution function in molecular dynamics
  - paper: doi:10.1103/PhysRev.136.A405
    title: Aneesur Rahman, Correlations in the motion of atoms in liquid argon, Physical Review 136(2A), 1964, A405-A411
    locator: the pair distribution function of simulated liquid argon
---

The radial distribution function $g(r)$ of a homogeneous and isotropic system of $N$ particles in a volume $V$ is the mean density of particles at distance $r$ from a given particle, divided by the mean density $\rho = N/V$. It is 0 where particles cannot be, it has peaks at the distances of the neighbor shells, and in a liquid it goes to 1 at large $r$, where the position of one particle says nothing about the others. In a simulation it is measured with a histogram of pair distances, and it is the main description of the structure of a liquid. Through Fourier transform it gives the structure factor that X-ray and neutron scattering measure.

## Definition

Let $r_1, \ldots, r_N$ be the positions, $r_{ij} = r_i - r_j$, and let $\langle \cdot \rangle$ be the average in the ensemble of the simulation, usually the [canonical ensemble](/canonical-ensemble/) or the [microcanonical ensemble](/microcanonical-ensemble/). The pair distribution function is
$$g(\mathbf{r}) = \frac{V}{N^2}\left\langle \sum_{i=1}^{N} \sum_{j \ne i} \delta(\mathbf{r} - r_{ij}) \right\rangle .$$
If the system is homogeneous and isotropic, $g$ depends only on $r = |\mathbf{r}|$, and the radial distribution function $g(r)$ is the average of $g(\mathbf{r})$ over the sphere of radius $r$. Then $\rho\, g(r)\, 4\pi r^2\, dr$ is the mean number of particles at a distance between $r$ and $r + dr$ from a given particle.

**Normalization.** With this definition, $\int_V \rho\, g(\mathbf{r})\, d\mathbf{r} = N - 1$, the number of other particles. So in a finite system at fixed $N$, $g$ goes to $1 - O(1/N)$ at large $r$, not to 1 exactly; for an ideal gas it is $(N - 1)/N$ at every $r$.

**The histogram estimator.** In a cubic periodic box of side $L$, take bins of width $\Delta r$ up to $L/2$ and count each pair through its nearest image, as in [periodic boundary conditions](/periodic-boundary-conditions/). Over $\tau$ configurations, bin $k$ collects $h_k$, the number of ordered pairs with $k\Delta r \le r_{ij} < (k+1)\Delta r$. An ideal gas at the same density has on average
$$n_k^{id} = \frac{4\pi\rho}{3}\left[((k+1)\Delta r)^3 - (k\Delta r)^3\right]$$
particles in that shell around each particle, and the estimate is $g(r_k) = h_k / (N \tau\, n_k^{id})$ at the bin center $r_k = (k + \tfrac{1}{2})\Delta r$.

```pseudo id=main
RDF(configurations C_1..C_τ, L, Δr, K)
L1  require K Δr ≤ L / 2
L2  h_k ← 0 for k = 0..K-1
L3  for each configuration:
L4      for each pair i < j:
L5          d ← |MINIMUM-IMAGE(r_i - r_j)|
L6          k ← ⌊d / Δr⌋; if k < K then h_k ← h_k + 2        ▷ the pair counts for i and for j
L7  for each bin k: n_k ← (4πρ/3)(((k+1)Δr)^3 - (kΔr)^3)
L8      g_k ← h_k / (N τ n_k)
L9  return g
```

The cost is $O(\tau N^2)$ with the double loop, or $O(\tau N)$ at fixed density with a [linked-cell list](/linked-cell-list/) whose cells have side at least $K\Delta r$. The result is the true $g$ averaged over each bin, so a small $\Delta r$ gives more detail and more noise; a [kernel density estimate](/kernel-density-estimation/) is a smooth alternative to the [histogram](/histogram/).

**What it gives.** For a potential that is a sum of pair terms $\phi(r)$, the energy and the pressure are integrals over $g$ (theorems for a homogeneous system):
$$\frac{U}{N} = 2\pi\rho \int_0^\infty \phi(r)\, g(r)\, r^2\, dr, \qquad P = \rho k_B T - \frac{2\pi}{3}\rho^2 \int_0^\infty r\,\phi'(r)\, g(r)\, r^2\, dr .$$
The tail corrections of the [Lennard-Jones potential](/lennard-jones-potential/) are these integrals from $r_c$ to infinity with $g = 1$. The running coordination number $n(R) = 4\pi\rho \int_0^R g(r)\, r^2\, dr$ is the mean number of neighbors closer than $R$; taken to the first minimum of $g$, it counts the first shell.

## Examples and non-examples

**Two atoms in a box.** Put $N = 2$ atoms independently and uniformly in a periodic box of volume $V$. Given one atom, the other one has density $1/V$ everywhere, and $\rho = 2/V$, so $g(r) = (1/V)/(2/V) = 1/2$ at every $r \le L/2$. This is the $(N-1)/N$ rule; the tests of the code confirm it with random positions.

**A simple cubic crystal.** Put $N = 27$ atoms on a simple cubic lattice with spacing 1 in a periodic box with $L = 3$, so $\rho = 1$, and use $\Delta r = 0.125$ up to $L/2 = 1.5$. Each atom has 6 neighbors at distance 1 and 12 at $\sqrt 2 \approx 1.414$. So $h_8 = 27 \cdot 6 = 162$ in the bin $[1, 1.125)$ and $h_{11} = 27 \cdot 12 = 324$ in the bin $[1.375, 1.5)$, and all other bins are empty. For bin 8, $n_8^{id} = \tfrac{4\pi}{3}(1.125^3 - 1) = 1.7753$, so $g = 162 / (27 \cdot 1.7753) = 6 / 1.7753 = 3.3797$. For bin 11, $g = 12 / 3.2479 = 3.6946$. The running coordination number is 6 after the first shell and 18 after the second; with a larger box it is 26 after the third shell of 8 atoms at $\sqrt 3$. In a body-centered cubic crystal the first shells hold 8 and 6 atoms, and in a face-centered cubic crystal the first shell holds 12.

**A simple liquid.** In the Lennard-Jones liquid near its triple point, $g(r)$ is close to 0 below about $0.9\sigma$, has a high first peak near $1.1\sigma$, then a few smaller peaks about $\sigma$ apart, and is close to 1 beyond about $3\sigma$. The first peak and the minimum after it hold about 12 neighbors. These values are measurements from simulation, and they agree with scattering data for argon.

**A dilute gas.** At low density, $g(r) \to \exp(-\phi(r)/k_B T)$, the Boltzmann factor of one pair. For hard spheres of diameter $d$, $g = 0$ for $r < d$ at every density.

**Non-example: a system that is not homogeneous.** Near a wall, at an interface or in a pore, the density depends on the position. A single function of $r$ normalized by one bulk density mixes regions with different densities and is not the radial distribution function; one uses the full pair density of two positions instead.

**Non-example: a system that is not isotropic.** In a crystal or a liquid crystal, $g(\mathbf{r})$ depends on the direction. The spherical average $g(r)$ still exists, as in the crystal example above, but it loses the angular information.

**Non-example: beyond half the box.** In a cubic periodic box, a sphere of radius $r > L/2$ around an atom leaves the region in which each pair has one nearest image. The histogram then misses pairs, and its estimate falls below the true $g$. The estimator stops at $L/2$.

## Related definitions

- **Structure factor.** $S(k) = 1 + \rho \int (g(\mathbf{r}) - 1)\, e^{-i \mathbf{k} \cdot \mathbf{r}}\, d\mathbf{r}$, the quantity that scattering experiments measure.
- **Potential of mean force.** $w(r) = -k_B T \ln g(r)$, the free energy of a pair at distance $r$, averaged over all other particles. [Iterative Boltzmann inversion](/iterative-boltzmann-inversion/) starts from it to fit a coarse-grained pair potential that reproduces a target $g$.
- **Compressibility equation.** In the grand canonical ensemble, $\rho k_B T \kappa_T = 1 + \rho \int (g(\mathbf{r}) - 1)\, d\mathbf{r}$, with $\kappa_T$ the isothermal compressibility. In a box at fixed $N$ the $O(1/N)$ term of $g$ matters in this integral.
- **Pair distribution of two positions.** $\rho^{(2)}(\mathbf{r}_1, \mathbf{r}_2)$, the density of pairs with one particle at each position. In a homogeneous system $\rho^{(2)} = \rho^2 g(\mathbf{r}_1 - \mathbf{r}_2)$.
- **Coordination number.** The integral of $4\pi\rho\, g(r)\, r^2$ up to the first minimum of $g$.

## References
