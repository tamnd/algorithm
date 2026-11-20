---
tag: NKWXRA
kind: data-structure
slug: verlet-neighbor-list
name: Verlet neighbor list
aliases:
- Verlet list
area: scientific-computing/molecular-simulation
level: core
summary: Stores for each atom the atoms within the cutoff plus a skin, and is rebuilt only when some atom has moved more than half the skin.
model: word-ram
complexity:
  vars: {N: the number of atoms, P: the number of pairs in the list}
  time: {build_direct: O(N^2), build_with_cells_fixed_density: O(N), step: O(N + P)}
  space: {total: O(N + P)}
history:
  year: 1967
  people: [Loup Verlet]
  note: Verlet kept for each atom a table of the atoms within a radius somewhat larger than the cutoff in his 1967 simulations of the Lennard-Jones fluid, and refreshed it only from time to time.
prereqs: [periodic-boundary-conditions, linked-cell-list]
see_also: [linked-cell-list, molecular-dynamics, periodic-boundary-conditions, lennard-jones-potential, fixed-radius-near-neighbors, verlet-integration, respa-multiple-time-step, uniform-grid]
sources:
  - paper: doi:10.1103/PhysRev.159.98
    title: Loup Verlet, Computer "experiments" on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1), 1967, 98-103
    locator: the table of neighbors within a radius larger than the cutoff, refreshed at intervals
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 5.3.1, The Verlet neighbour list (the automatic update test on the two largest displacements, and the measured speedup for the Lennard-Jones fluid)
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Appendix F, Saving CPU time (F.1 Verlet list, F.3 Combining the Verlet and cell lists, F.4 Efficiency)
---

A Verlet neighbor list stores, once, all pairs of atoms closer than a list radius $r_\ell = r_c + s$, where $r_c$ is the cutoff of the forces and the skin $s > 0$ is a margin, and then reuses this list for many time steps. At each step the force loop tests only the stored pairs, and the list is built again only when the atoms have moved far enough that a pair outside the list could have come within $r_c$. It differs from the [linked-cell list](/linked-cell-list/), which stores the atoms by position and is rebuilt at every step; a cell list is the usual way to build a Verlet list. Both are parts of the force loop of [molecular dynamics](/molecular-dynamics/) under [periodic boundary conditions](/periodic-boundary-conditions/).

## In plain words

Suppose you must check, many times a minute, which people in a crowd stand within two meters of each other. People walk slowly, so the answer changes little from one check to the next.

So once in a while, write down every pair of people within two and a half meters, a little more than you need. At each check, look only at the pairs on your paper. A pair that was more than two and a half meters apart cannot come within two meters until the two people have walked half a meter between them.

Keep track of how far people walked since you made the paper. When the two who walked farthest have together walked more than half a meter, make a new paper.

## The abstract type

The list answers, at each time step $n$, the query "all unordered pairs $\{i, j\}$ with $|r_{ij}| < r_c$" for the current positions $r_1, \ldots, r_N$ in a periodic cubic box of side $L$, with the distance taken under the minimum image rule. The positions change a little between queries. The list is a cache of candidate pairs with a test that says when the cache can no longer be trusted. The answer is the same as that of the direct loop or a [linked-cell list](/linked-cell-list/) at every step; only the cost differs.

## Representation

- The list radius is $r_\ell = r_c + s$, with $r_\ell \le L/2$, so that the minimum image of each pair in the list is unique.
- The list is the set of pairs $(i, j)$ with $i < j$ and $|r_{ij}^0| < r_\ell$ at the last build. Codes store it in compressed form: an array `point` of $N + 1$ start positions and an array `list` of neighbors, so that the neighbors of atom $i$ with $j > i$ are `list[point[i]]` to `list[point[i+1] - 1]`. The implementation keeps a plain list of pairs.
- The reference positions $r_i^0$, the positions at the last build.
- The displacement of atom $i$ since the build, $d_i = |r_i - r_i^0|$, taken under the minimum image rule so that an atom that crosses the boundary and is wrapped back into the box does not seem to have jumped by $L$.

**Invariant (V).** Let $d_{(1)} \ge d_{(2)}$ be the two largest displacements since the last build. If $d_{(1)} + d_{(2)} \le s$, then every pair with $|r_{ij}| < r_c$ now is in the list.

The reason is the triangle inequality on the torus. If the pair was not in the list, then $|r_{ij}^0| \ge r_\ell$ at the build, and now $|r_{ij}| \ge |r_{ij}^0| - d_i - d_j \ge r_c + s - (d_{(1)} + d_{(2)}) \ge r_c$. So the pair is not within the cutoff.

## Operations

```pseudo id=main
BUILD(r_1..r_N)
L1  r_ℓ ← r_c + s
L2  for each pair i < j:
L3      if |r_ij| < r_ℓ under the minimum image rule then add (i, j) to the list
L4  r_i^0 ← r_i for each atom i

PAIRS(r_1..r_N)                          ▷ called once per time step
L5  d_i ← |r_i - r_i^0| under the minimum image rule, for each atom i
L6  if d_(1) + d_(2) > s, where d_(1) ≥ d_(2) are the two largest d_i then
L7      BUILD(r_1..r_N)
L8  for each pair (i, j) in the list:
L9      if |r_ij| < r_c then report (i, j)
```

Lines L2 and L3 are the direct loop here; with a linked-cell list of cell side at least $r_\ell$, the build looks only at neighboring cells. Line L6 is the automatic update test that Allen and Tildesley give, after Fincham (1981) and Thompson (1983). The simpler and more common test is the half-skin rule: rebuild when $d_{(1)} > s/2$. It is also safe, because $d_{(1)} \le s/2$ gives $d_{(1)} + d_{(2)} \le s$, but it rebuilds at least as often. Many codes skip the test and rebuild every 10 to 20 steps; that interval is a choice, and it is safe only if no two atoms can close the skin between rebuilds.

## Example

Take a box of side $L = 10$ (in units of $\sigma$) with $r_c = 2.5$ and $s = 0.5$, so $r_\ell = 3.0$. Three atoms lie at $r_0 = (1, 0, 0)$, $r_1 = (3.95, 0, 0)$ and $r_2 = (1, 3.05, 0)$.

| pair | distance at the build | in the list ($< 3.0$) | within $r_c$ ($< 2.5$) |
|---|---|---|---|
| (0, 1) | 2.950 | yes | no |
| (0, 2) | 3.050 | no | no |
| (1, 2) | 4.243 | no | no |

The list is $\{(0, 1)\}$, and the step reports no pair.

**Two atoms move toward each other.** Atom 0 moves to $(1, 0.3, 0)$ and atom 2 to $(1, 2.75, 0)$, so $d = (0.3, 0, 0.3)$. Now $|r_{02}| = 2.45 < r_c$, but the pair is not in the list. Each atom alone moved less than the skin, so a test of the form "rebuild when one atom has moved more than $s$" does not rebuild, and the force loop misses the pair. The test of line L6 gives $0.3 + 0.3 = 0.6 > 0.5$ and rebuilds. The new list is $\{(0, 1), (0, 2)\}$, with $|r_{01}| = 2.965$ and $|r_{02}| = 2.45$, and the step reports $(0, 2)$. The half-skin rule also rebuilds, since $0.3 > 0.25$.

**One atom moves more than the other.** Start again from the build. Atom 1 moves to $(3.65, 0, 0)$ and atom 2 to $(1, 2.95, 0)$, so $d = (0, 0.3, 0.1)$. The test of line L6 gives $0.3 + 0.1 = 0.4 \le 0.5$, so the list is kept. The half-skin rule rebuilds, since $0.3 > 0.25$. Both report no pair, which is right: $|r_{01}| = 2.65$ and $|r_{02}| = 2.95$ are both above $r_c$. The test of line L6 saved one build.

## Correctness

PAIRS reports exactly the pairs within $r_c$. Each reported pair passes the test of line L9, so it is within the cutoff. Conversely, after lines L5 to L7, either the list was just built, so that $d_{(1)} = d_{(2)} = 0$, or the test of line L6 found $d_{(1)} + d_{(2)} \le s$; in both cases invariant (V) holds, and every pair within $r_c$ is in the list, so line L9 reports it. Each pair is stored once with $i < j$, so it is reported once. The proof uses only the triangle inequality for the minimum image distance, which is the distance on the torus, so it holds even when atoms cross the boundary between builds. The full proof is in the proofs folder.

## Complexity

The model is the [word RAM](/word-ram/), with one distance test counted as one operation. Let $P$ be the number of pairs in the list.

- **Build.** $N(N-1)/2$ tests with the direct loop. With a linked-cell list whose cells have side at least $r_\ell$, $O(N)$ at fixed density.
- **Step without a rebuild.** $O(N)$ for the displacements of line L5 and the two largest values, and $O(P)$ for the pair tests.
- **Size of the list.** At number density $\rho$, an atom has on average about $\frac{4}{3}\pi r_\ell^3 \rho$ atoms within $r_\ell$, so $P \approx \frac{2}{3}\pi r_\ell^3 \rho N$, which is $O(N)$ at fixed density. For the Lennard-Jones liquid at $\rho^* = 0.8$ with $r_c = 2.5$ and $s = 0.3$, this is about 73.6 neighbors per atom within $r_\ell = 2.8$, of which about 52.4 lie within $r_c$: about 71 percent of the tested pairs are hits, against at most 15.5 percent for the 27 cells of a cell list. These are geometric averages for a uniform density, not measurements.
- **Space.** $O(N + P)$.

| operation | time | case |
|---|---|---|
| build | $O(N^2)$ | direct loop |
| build | $O(N)$ | with a cell list, at fixed density |
| step | $O(N + P)$ | without a rebuild |
| space | $O(N + P)$ | total |

The number of steps between rebuilds depends on the skin, the temperature and the time step $h$, so the gain is a measurement. A larger skin makes rebuilds rarer and the list longer; the best skin is found by trying a few values. Allen and Tildesley show the speedup for the Lennard-Jones fluid at $r_c^* = 2.5$, $\rho^* = 0.78$, $T^* = 0.85$ and $h^* = 0.005$ as a function of the skin (Section 5.3.1).

## Variants

- **Half-skin rule.** Rebuild when one atom has moved more than $s/2$. It needs only the largest displacement, and it rebuilds at least as often as the test of line L6.
- **Fixed interval.** Rebuild every $k$ steps, with $k$ often 10 to 20. It needs no displacement tracking, but it has no guarantee: a fast atom can cross the skin, and a missed pair gives a wrong force with no warning. It is a rule of thumb.
- **Verlet list built with cells.** Build the list with a [linked-cell list](/linked-cell-list/) of cell side $r_\ell$, so that both the build and the step are $O(N)$ at fixed density (Frenkel and Smit, Appendix F.3).
- **Full list.** Store each pair twice, once for each atom. It doubles the memory and the tests, but each atom then sums its own force with no writes to other atoms, which suits parallel and GPU code.
- **Lists for Monte Carlo.** In Monte Carlo, one atom moves at a time, and the same displacement test decides when to rebuild.
- **Multiple time steps.** In [RESPA](/respa-multiple-time-step/), the short-range force uses the Verlet list and the slow force is evaluated less often.

## When to use it

Use a Verlet list when atoms move a small distance per step compared with the cutoff, as in liquids, solids and biomolecules, so that one build serves many steps. It is worth more when the force per pair is costly, because the list wastes fewer tests than the 27 cells of a cell list. For a small system, a few hundred atoms or fewer, build it with the direct loop. For a large system, build it with a linked-cell list. Do not use it when the atoms move fast relative to the skin, as in a hot gas or a shock, because the list is then rebuilt at almost every step and the extra memory buys nothing; a plain [linked-cell list](/linked-cell-list/) is then better.

## Pitfalls

- **Testing one displacement against the full skin.** Two atoms that each move $0.6 s$ toward each other close a gap of $1.2 s$, so the test $d_{(1)} > s$ misses pairs, as the example shows. Use the half-skin rule or the two largest displacements.
- **Displacements per step instead of since the build.** The test needs the displacement from the reference positions $r_i^0$ of the last build. Small steps add up.
- **Displacements across the boundary.** If positions are wrapped into the box, an atom that crosses the boundary seems to jump by $L$. Use the minimum image of $r_i - r_i^0$, or keep unwrapped positions for the displacements.
- **A list radius above half the box.** With $r_\ell > L/2$, a pair can have two images within $r_\ell$, and one stored pair cannot stand for both. Check $r_c + s \le L/2$, as the implementation does.
- **A box that changes size.** Under a barostat, the box and all distances scale. A list built in the old box can miss pairs in the new one unless the test accounts for the change.
- **Calling it a speedup in all cases.** The gain depends on the skin, the density and the temperature. It is a measured result for a given system.

## Implementations

## History

Loup Verlet introduced the list in his 1967 paper on the Lennard-Jones fluid, the same paper that made the Verlet integrator popular. He kept for each atom a table of the atoms within a radius somewhat larger than the cutoff and refreshed it only from time to time, so most steps did not search the whole box. Automatic tests based on the displacements since the last build came later; Allen and Tildesley credit the test on the two largest displacements to Fincham (1981) and Thompson (1983). Combining the list with cells, so that the build too is linear in $N$, became the standard method in molecular dynamics codes.

## References
