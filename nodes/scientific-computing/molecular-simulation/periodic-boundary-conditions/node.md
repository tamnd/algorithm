---
tag: VY641R
kind: technique
slug: periodic-boundary-conditions
name: Periodic boundary conditions
aliases:
- minimum image convention
area: scientific-computing/molecular-simulation
level: intro
summary: Surrounds the simulation box by periodic images of itself, with each pair interacting through its closest image, so a small system mimics bulk matter.
prereqs: [interatomic-potential]
see_also: [molecular-dynamics, linked-cell-list, verlet-neighbor-list, radial-distribution-function, lennard-jones-potential, ewald-summation, boundary-conditions, microcanonical-ensemble]
sources:
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 1.6, Studying small systems (1.6.2 Periodic boundary conditions, 1.6.3 Potential truncation, 1.6.4 Computer code for periodic boundaries, 1.6.5 Spherical boundary conditions)
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Chapter 3, the section on technical details (periodic boundary conditions and the truncation of interactions)
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21(6), 1953, 1087-1092
    locator: the periodic square of hard disks, with each disk interacting with the nearest image of each other disk
  - paper: doi:10.1103/PhysRev.159.98
    title: Loup Verlet, Computer "experiments" on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1), 1967, 98-103
    locator: a periodic cube of 864 Lennard-Jones atoms
---

Periodic boundary conditions replace the walls of a simulation box by copies of the box: the box of side $L$ is repeated in all directions to fill space, each copy holds the same atoms at the same relative positions, and an atom that leaves through one face comes back through the opposite face. A system of a few hundred or a few thousand atoms then has no surface, and it behaves much more like bulk matter than the same atoms in a closed box would. The forces are computed with the minimum image rule: each atom interacts with the nearest copy of each other atom, which needs a cutoff $r_c \le L/2$. The [linked-cell list](/linked-cell-list/) and the [Verlet neighbor list](/verlet-neighbor-list/) find the pairs within the cutoff fast; this page is about the boundary itself, and [boundary conditions](/boundary-conditions/) treats the same idea for differential equations.

## In plain words

A small box of atoms has walls, and the atoms near the walls feel something no atom in a large sample feels. In a box of a thousand atoms, about half of them touch a wall.

So remove the walls. Imagine the box surrounded by exact copies of itself, like tiles on a floor, in every direction. When an atom moves out through the right side, its copy comes in through the left side at the same moment. Every atom now has neighbors on all sides.

To find the force between two atoms, use the copy of the second atom that is closest to the first one. If the box is large enough compared with the range of the forces, there is only one such copy.

## When it applies

Use periodic boundaries to study a homogeneous bulk phase, a liquid, a gas or a crystal, with a small number of atoms. The conditions are:

- **The forces are short range,** or are treated by a method made for periodic systems. With a cutoff $r_c \le L/2$, the minimum image rule gives each pair at most one image within the cutoff. Coulomb and dipole forces decay too slowly for a cutoff; they need [Ewald summation](/ewald-summation/) or a mesh method such as [particle-mesh Ewald](/particle-mesh-ewald/), which sum over all images.
- **The box is larger than the correlations you want to measure.** The periodic copies impose a period $L$ on the system, so structure at distances above about $L/2$, long-wavelength sound and density waves, and the large fluctuations near a critical point are not represented. The [radial distribution function](/radial-distribution-function/) can be measured only up to $L/2$.
- **The system is not a surface, a cluster or a single molecule,** unless the copies are put far apart. A slab can be studied with periodic boundaries in two directions only, and an isolated molecule in a box large enough that the copies do not interact.

## The template

Let the box be $[0, L)^3$, with $N$ atoms at number density $\rho = N / L^3$, so $L = (N / \rho)^{1/3}$.

```pseudo id=main
WRAP(r)                                      ▷ after each move
L1  for each axis q: x_q ← x_q - L ⌊x_q / L⌋

MINIMUM-IMAGE(r_i, r_j)
L2  Δ ← r_i - r_j
L3  for each axis q: Δ_q ← Δ_q - L round(Δ_q / L)
L4  return Δ, with |Δ| the distance between i and the nearest image of j

PAIR-ENERGY(r_1..r_N, r_c)
L5  require r_c ≤ L / 2
L6  U ← 0; for each pair i < j:
L7      Δ ← MINIMUM-IMAGE(r_i, r_j); if |Δ| < r_c then U ← U + φ(|Δ|)
L8  return U
```

1. **Choose $N$ and $\rho$,** which fix $L$. Check that $r_c \le L/2$ (line L5).
2. **Wrap the positions** into the box after each move (line L1). The wrap changes the stored position by a whole number of box lengths, so it changes no distance.
3. **Use the minimum image** for every pair (lines L2 to L4). After line L3, $|\Delta_q| \le L/2$ on each axis, and $\Delta$ is the shortest of the vectors $r_i - r_j - L m$ over all integer vectors $m$.
4. **Truncate the potential at $r_c$** and say how: truncated, truncated and shifted, or shifted-force, and whether a tail correction is added (see the [Lennard-Jones potential](/lennard-jones-potential/)).
5. **Keep unwrapped positions too** if you measure diffusion, because wrapped positions jump by $L$.

The minimum image rule is one rule inside the technique; it is not the technique. It is the right rule for short-range forces in a cubic or orthorhombic box. In a triclinic box, the rounding of step 3 is done on the scaled coordinates, and it can miss the nearest image when the box is strongly skewed.

**Why $r_c \le L/2$.** Two images of atom $j$ are $L$ apart, so they cannot both be closer than $L/2$ to atom $i$. With $r_c \le L/2$, each atom $i$ sees at most one image of each $j$ within the cutoff, and the minimum image finds it. With $r_c > L/2$, some pairs have two images within the cutoff, and the minimum image rule counts only one of them.

## Classic examples

**One dimension.** With $L = 10$, $x_1 = 1$ and $x_2 = 9$, the plain difference is $x_1 - x_2 = -8$, and $\mathrm{round}(-0.8) = -1$, so $\Delta = -8 + 10 = 2$. The nearest image of atom 2 is at $9 - 10 = -1$, at distance 2 from atom 1, across the boundary. An atom at $x = 10.3$ wraps to $0.3$, and one at $x = -0.4$ wraps to $9.6$.

**The Lennard-Jones liquid near the triple point.** A standard state is $\rho^* = 0.8442$ in reduced units. With $N = 108$ atoms, $L = (108 / 0.8442)^{1/3} = 5.0388 \sigma$, so $L/2 = 2.519 \sigma$, and the usual cutoff $r_c = 2.5 \sigma$ just fits. With $N = 864$, as in Verlet's 1967 runs, $L = 10.078 \sigma$. For argon with $\sigma = 0.3405$ nm, a box of 256 atoms at $\rho^* = 0.8$ is $6.840 \sigma = 2.33$ nm on a side.

**An fcc crystal in the box.** A face-centered cubic lattice of $3 \times 3 \times 3$ unit cells holds $4 \cdot 27 = 108$ atoms and fills a periodic box exactly, with cell side $a = L / 3$. At $\rho^* = 0.8442$, $a = 1.6796 \sigma$ and the nearest neighbors are at $a / \sqrt 2 = 1.1877 \sigma$. Under the minimum image rule, each atom has 54 neighbors within $r_c = 2.5 \sigma$: 12 at $1.1877$, 6 at $1.6796$, 24 at $2.0571$ and 12 at $2.3753$. With the Lennard-Jones potential truncated at $r_c$ without a shift, the energy is $U / N = -6.7734 \epsilon$, the same as a direct sum over the infinite lattice with the same cutoff. The test file checks both facts.

**How few pairs interact.** A cutoff sphere holds the fraction $\frac{4}{3}\pi r_c^3 / L^3$ of the box. For $N = 864$ at $\rho^* = 0.8442$ and $r_c = 2.5$, this is 6.4 percent; the [linked-cell list](/linked-cell-list/) turns this into a saving.

## Variations

- **Non-cubic boxes.** A truncated octahedron or a rhombic dodecahedron also fills space with copies, and for a given distance between images it holds fewer atoms. Allen and Tildesley give 256 atoms for a cube, 197 for a truncated octahedron and 181 for a rhombic dodecahedron at the same density and the same smallest distance between images (Section 1.6.2). The saving matters for a solute in water, where the solvent is the main cost.
- **Triclinic boxes.** Write $r = h s$, with the box matrix $h$ whose columns are the edge vectors and scaled coordinates $s \in [0, 1)^3$. Wrap and round the scaled coordinates. Barostats such as [Parrinello-Rahman](/parrinello-rahman-barostat/) change $h$ during the run.
- **Sliding boundaries for shear.** In Lees-Edwards boundaries, the copies above and below the box move with opposite velocities, which drives a steady shear flow for measurements of viscosity.
- **Slabs and wires.** Periodic in two directions for an interface or a membrane, or in one direction for a wire. Long-range sums then need forms of Ewald summation adapted to the geometry.
- **Spherical boundary conditions.** Put the atoms on the surface of a four-dimensional sphere, which has no boundary and no preferred direction (Allen and Tildesley, Section 1.6.5).
- **Long-range forces.** With charges, the sum over all images converges only conditionally. [Ewald summation](/ewald-summation/) splits it into a short-range part, computed with the minimum image, and a smooth part summed in Fourier space.

## Pitfalls

- **A cutoff above half the box.** With $r_c > L/2$, some pairs interact through two images, and the minimum image rule silently drops one. Check $r_c \le L/2$, or use a larger box.
- **Wrapping with truncation instead of floor.** In many languages, `int(x / L)` rounds toward zero, so a position $x = -0.4$ is not wrapped. Use the floor, as in line L1. In floating point, $x - L \lfloor x / L \rfloor$ can return exactly $L$ for a tiny negative $x$; map it to 0.
- **Diffusion from wrapped positions.** The mean squared displacement must use unwrapped positions, or it stops growing near $L^2 / 6$ per axis, the mean squared difference of two independent uniform positions in $[0, L)$.
- **Molecules cut by the boundary.** The atoms of one molecule can be wrapped into different sides of the box. Compute bond vectors with the minimum image, or wrap whole molecules by their centers.
- **Angular momentum.** Periodic boundaries break rotational symmetry, so the total angular momentum is not conserved; the total linear momentum is. The kinetic temperature then uses $N_f = 3N - 3$ degrees of freedom when the total momentum is fixed at zero (see the [microcanonical ensemble](/microcanonical-ensemble/)).
- **Finite-size effects.** Periodic boundaries remove surfaces, not all effects of size. The period $L$ suppresses long waves and limits correlations; results such as the diffusion coefficient or a critical temperature depend on $N$ and need a study at several sizes.

## Exercises

1. With $L = 10$, give the minimum image vector from $x_j = 0.5$ to $x_i = 6$, and the wrapped positions of $x = 23.5$ and $x = -10.5$.
2. Show that after line L3, $|\Delta_q| \le L/2$, and that $\Delta$ is the shortest of the vectors $r_i - r_j - L m$, $m \in \mathbb{Z}^3$, in a cubic box.
3. Find the smallest number of atoms of a cubic box at $\rho^* = 0.8$ that allows $r_c = 3 \sigma$.
4. In a cubic box of side $L$, place two atoms at $(0, 0, 0)$ and $(L/2, L/2, 0)$. How many images of the second atom are at the smallest distance from the first? What does the rounding of line L3 return?
5. In a two-dimensional box with edge vectors $(L, 0)$ and $(L/2, L)$, find two points for which rounding the scaled coordinates does not give the nearest image.
6. Explain why the total angular momentum of an isolated cluster is conserved, but that of a periodic liquid is not.

## References
