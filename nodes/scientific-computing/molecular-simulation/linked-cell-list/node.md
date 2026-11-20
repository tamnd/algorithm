---
tag: 4RS32Z
kind: data-structure
slug: linked-cell-list
name: Linked-cell list
aliases:
- cell list
- cell-linked list
area: scientific-computing/molecular-simulation
level: core
summary: Bins atoms into cells of side at least the cutoff, so each atom checks only its own and the neighboring cells. At fixed density all pairs within the cutoff are found in O(N) time.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {N: the number of atoms, M: the number of cells, K: the largest number of atoms in one cell}
  time: {build: O(N + M), all_pairs: O(N K + M), all_pairs_fixed_density: O(N)}
  space: {total: O(N + M)}
history:
  year: 1973
  people: [B. Quentrec, C. Brot, Roger W. Hockney, James W. Eastwood]
  note: Quentrec and Brot gave the cell search for molecular dynamics in 1973, and Hockney and Eastwood described the same structure as the chaining mesh of their particle-particle particle-mesh method.
prereqs: [periodic-boundary-conditions, uniform-grid]
see_also: [verlet-neighbor-list, molecular-dynamics, uniform-grid, spatial-hashing, fixed-radius-near-neighbors, p3m-method, counting-sort, z-order-curve]
sources:
  - paper: doi:10.1016/0021-9991(73)90046-6
    title: B. Quentrec and C. Brot, New method for searching for neighbors in molecular dynamics computations, Journal of Computational Physics 13(3), 1973, 430-432
    locator: the division of the box into cells and the search over the neighboring cells
  - book: isbn:9780852743928
    title: Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988
    locator: the chapter on particle-particle particle-mesh algorithms (the chaining mesh and its linked lists)
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 5.3.2, Cell structures and linked lists
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Appendix F, Saving CPU time (F.2 Cell lists, F.3 Combining the Verlet and cell lists)
---

A linked-cell list cuts a periodic simulation box into cells whose side is at least the cutoff $r_c$, and keeps the atoms of each cell in a chain stored in two integer arrays, `head` and `next`. Two atoms closer than $r_c$ are then in the same cell or in neighboring cells, so the search for all short-range pairs looks at 27 cells around each cell instead of the whole box, and at fixed density it takes $O(N)$ time instead of the $N(N-1)/2$ pair tests of the direct loop. It is the [uniform grid](/uniform-grid/) adapted to [periodic boundary conditions](/periodic-boundary-conditions/) and to a fixed cutoff. It differs from the [Verlet neighbor list](/verlet-neighbor-list/), which stores the pairs themselves and keeps them over many steps; the two are often used together, with the cell list building the Verlet list.

## In plain words

Think of a large hall full of people, and you want every pair of people who stand closer than two meters. Comparing each person with every other person takes too long in a large crowd.

Instead, draw a grid of squares on the floor, each square two meters wide. Two people who stand closer than two meters must stand in the same square or in two squares that touch. So for each square you only compare the people inside it with the people in the eight squares around it.

Each square keeps a short list of the people in it. To make the lists, you walk through the crowd once and put each person in the list of their square. When the crowd moves, you make the lists again, which is fast.

## The abstract type

The structure answers one query over a set of $N$ points $r_1, \ldots, r_N$ in a periodic cubic box of side $L$: report every unordered pair $\{i, j\}$ with $|r_{ij}| < r_c$, where $r_{ij} = r_i - r_j$ is taken under the minimum image rule of [periodic boundary conditions](/periodic-boundary-conditions/), and each pair is reported once. This is the all-pairs form of the [fixed-radius near neighbors](/fixed-radius-near-neighbors/) problem on a torus. The same cells also answer the single query "all atoms within $r_c$ of a point $q$" by a scan of the 27 cells around the cell of $q$. In [molecular dynamics](/molecular-dynamics/) the pairs feed the force loop, and the structure is rebuilt at each time step, or each time the Verlet list needs a rebuild.

## Representation

Let $s = \lfloor L / r_c \rfloor$ and $\ell = L / s$, so that the box is cut into $M = s^3$ cubic cells of side $\ell \ge r_c$. A cell has integer coordinates $k = (k_x, k_y, k_z)$ with $0 \le k_a < s$ and the index $c = k_x + s (k_y + s k_z)$. An atom at the position $r_i$, wrapped into $[0, L)^3$, is in the cell with $k_a = \lfloor x_{i,a} / \ell \rfloor$.

- `head[c]` is one atom of cell $c$, or $-1$ when the cell is empty. It is an array of $M$ integers.
- `next[i]` is the next atom in the same cell as atom $i$, or $-1$ at the end of the chain. It is an array of $N$ integers.

The chain of cell $c$ is `head[c]`, `next[head[c]]`, and so on, until $-1$. This is a set of singly linked lists stored in arrays, with no pointers and no memory allocated per atom, which is why the name has the word "linked".

**Invariant (C).** (1) Each atom is in exactly one chain, and the chain of cell $c$ holds exactly the atoms whose wrapped position lies in cell $c$. (2) The cell side is at least the cutoff, $\ell \ge r_c$. (3) There are at least three cells along each side, $s \ge 3$.

Part 3 makes the 27 cells around a cell distinct, so that no pair of cells is visited twice. It also gives $r_c \le \ell \le L/3 < L/2$, so the minimum image rule is well defined for every pair within the cutoff.

## Operations

The build puts each atom at the front of the chain of its cell. The pair search visits, for each cell, the cell itself and a "half shell" $H$ of 13 neighboring cells: the offsets $o \in \{-1, 0, 1\}^3$ whose first nonzero entry is $+1$. Of each two opposite offsets $o$ and $-o$, exactly one is in $H$, so each pair of neighboring cells is visited once, from one side only. This is how the method uses Newton's third law: each pair force is computed once and added to both atoms.

```pseudo id=main
BUILD(r_1..r_N, L, r_c)
L1  s ← ⌊L / r_c⌋; require s ≥ 3; ℓ ← L / s
L2  head[c] ← -1 for each of the s^3 cells c; next[i] ← -1 for each atom i
L3  for i ← 1 to N:
L4      c ← the cell (⌊x_i / ℓ⌋, ⌊y_i / ℓ⌋, ⌊z_i / ℓ⌋) of r_i, with r_i wrapped into [0, L)^3
L5      next[i] ← head[c]; head[c] ← i

ALL-PAIRS()
L6  for each cell c:
L7      for each offset o in {0} ∪ H:          ▷ H holds the 13 offsets whose first nonzero entry is +1
L8          c' ← (c + o) mod s, coordinate by coordinate
L9          for each atom i in the chain of c:
L10             for each atom j in the chain of c', and only the atoms after i when c' = c:
L11                 if |r_ij| < r_c under the minimum image rule then report (i, j)
```

Line L5 is the only update: the new atom becomes the head, and the old head becomes its successor, so a chain lists its atoms in the reverse order of insertion. Line L8 wraps the cell coordinates, which is how the periodic boundary enters the search; the distance in line L11 must then use the minimum image as well, because a pair found through a wrapped cell is a pair across the boundary. In two dimensions, $H$ has 4 offsets: $(0, 1)$, $(1, -1)$, $(1, 0)$ and $(1, 1)$, with the first coordinate along $x$.

**Rebuild.** The structure is not updated atom by atom. When the atoms move, the build runs again in $O(N + M)$ time. Moving one atom to another cell would need a doubly linked chain or a search in a singly linked one.

## Example

Take a periodic square of side $L = 8$ in two dimensions with $r_c = 2$, so $s = 4$, $\ell = 2$ and there are 16 cells, with index $c = k_x + 4 k_y$. Seven atoms are inserted in the order 0 to 6.

| atom | position | cell $(k_x, k_y)$ | index $c$ |
|---|---|---|---|
| 0 | (0.5, 0.5) | (0, 0) | 0 |
| 1 | (1.6, 1.2) | (0, 0) | 0 |
| 2 | (2.4, 0.6) | (1, 0) | 1 |
| 3 | (7.6, 1.0) | (3, 0) | 3 |
| 4 | (4.5, 4.5) | (2, 2) | 10 |
| 5 | (1.0, 7.2) | (0, 3) | 12 |
| 6 | (5.9, 3.1) | (2, 1) | 6 |

After the build, `head[0] = 1` and `next[1] = 0`, so the chain of cell 0 is 1, 0. The other nonempty cells hold one atom each: `head[1] = 2`, `head[3] = 3`, `head[6] = 6`, `head[10] = 4` and `head[12] = 5`. Every other entry of `head` and of `next` is $-1$.

The search computes these distances. Distances across the boundary use the minimum image: for atoms 0 and 3, $\Delta x = 0.5 - 7.6 = -7.1$, which becomes $-7.1 + 8 = 0.9$.

| cell | offsets that reach a nonempty cell | distances tested | pairs reported |
|---|---|---|---|
| (0, 0) | itself; (1, 0) to cell (1, 0) | 1-0: 1.304; 1-2: 1.000; 0-2: 1.903 | (0, 1), (1, 2), (0, 2) |
| (1, 0) | (1, 1) to cell (2, 1) | 2-6: 4.301 | none |
| (3, 0) | (1, -1) to cell (0, 3); (1, 0) to cell (0, 0) | 3-5: 2.280; 3-1: 2.010; 3-0: 1.030 | (0, 3) |
| (2, 1) | (0, 1) to cell (2, 2); (1, -1) to cell (3, 0) | 6-4: 1.980; 6-3: 2.702 | (4, 6) |
| (0, 3) | (0, 1) to cell (0, 0); (1, 0) to cell (1, 3), empty; (1, -1) to cell (1, 2), empty; (1, 1) to cell (1, 0) | 5-1: 2.088; 5-0: 1.393; 5-2: 1.980 | (0, 5), (2, 5) |
| (2, 2) | none | none | none |

The search computes 12 distances and reports 7 pairs: (0, 1), (0, 2), (0, 3), (0, 5), (1, 2), (2, 5) and (4, 6). The direct loop computes all $7 \cdot 6 / 2 = 21$ distances and finds the same 7 pairs. Pair (2, 5) is found through two wrapped steps: cell (0, 3) plus the offset $(1, 1)$ is cell $(1, 4 \bmod 4) = (1, 0)$. In a box this small, the saving is small; the saving grows with the box, as the next sections show.

## Correctness

The build keeps (C): each atom goes to the chain of the one cell that holds its wrapped position, and part 2 and part 3 follow from line L1. Two atoms within $r_c$ of each other, under the minimum image, have cell coordinates that differ by $-1$, 0 or $+1$ modulo $s$ on each axis, because their coordinates differ by less than $r_c \le \ell$ on each axis, and two numbers that differ by less than 1 have floors that differ by at most 1. With $s \ge 3$, the values $-1$, 0 and $+1$ are distinct modulo $s$, so the offset from one cell to the other is unique. If the offset is 0, the pair is tested once inside the own cell; if not, exactly one of the offset and its negative is in $H$, so the pair is tested from one of the two cells only. So each pair within the cutoff is tested exactly once, in line L11, and reported. Every reported pair passes the distance test, so no wrong pair is reported. The full proof is in the proofs folder.

## Complexity

The model is the [word RAM](/word-ram/): a cell index is computed in $O(1)$ by three floors and integer arithmetic, and one distance test counts as one operation.

- **Build.** $O(N + M)$: line L2 fills the arrays, and lines L3 to L5 do $O(1)$ work per atom.
- **All pairs, worst case.** The search visits $14 M$ cell pairs, and for a cell pair it tests $n_c \, n_{c'}$ distances, where $n_c$ is the number of atoms in cell $c$. Each atom of cell $c$ is tested against at most $14 K$ atoms when its cell is visited, so the cost is $O(N K + M)$. When all atoms are in one cell, $K = N$ and the cost is $N(N-1)/2$ tests, the same as the direct loop.
- **All pairs at fixed density.** Hold the density $\rho = N / L^3$ and the cutoff fixed as $N$ grows. Then $M = s^3 \le L^3 / r_c^3 = N / (\rho r_c^3)$, so $M = O(N)$. For $N$ independent uniform positions, a cell pair holds $N(N-1)/M^2$ test pairs on average and a cell holds $N(N-1)/(2M^2)$ pairs with itself, so the expected number of tests is $13.5 \, N (N-1) / M \approx 13.5 \, N \rho \ell^3$, which is $O(N)$. A bound for every configuration, not only on average, needs a minimum distance: if no two atoms are closer than $\delta$, the balls of radius $\delta / 2$ around the atoms of one cell are disjoint and lie in a cube of side $\ell + \delta$, so $K \le (6 / \pi)(\ell / \delta + 1)^3$, and the cost is $O(N)$ for each configuration. The steep repulsion of a liquid keeps atoms apart in the states a simulation visits, but this is an observation, not a property of the potential.
- **Wasted tests.** The 27 cells around an atom cover a volume of $27 \ell^3 \ge 27 r_c^3$, and only the sphere of volume $\frac{4}{3}\pi r_c^3 \approx 4.19 r_c^3$ holds neighbors. So at best about 15.5 percent of the tested pairs are within the cutoff. This is a geometric ratio, not a measurement.
- **Space.** $M + N$ integers for `head` and `next`.

| operation | time | case |
|---|---|---|
| build | $O(N + M)$ | worst |
| all pairs | $O(N K + M)$ | worst |
| all pairs | $O(N)$ | fixed density, expected for uniform positions or with a minimum distance |
| space | $O(N + M)$ | total |

The test file checks the fixed-density bound by measurement. At $\rho = 1$ and $r_c = \ell = 1$ in three dimensions, boxes of side 4, 6 and 8 (64, 216 and 512 atoms at uniform random positions) give between 10 and 17 tests per atom, close to the expected 13.5.

## Variants

- **Cells smaller than the cutoff.** With $\ell = r_c / 2$ the search covers the $5^3 = 125$ cells of side $\ell$ around a cell, a volume of $15.6 r_c^3$ instead of $27 r_c^3$, so a larger fraction of the tests (about 27 percent) are hits. There are more cells to visit, and the best choice is found by measurement for each machine.
- **Sorted arrays instead of chains.** Sort the atoms by cell index with a [counting sort](/counting-sort/), and keep for each cell the start of its block. The atoms of one cell are then next to each other in memory, which helps caches and GPUs. Ordering the cells along a [Z-order curve](/z-order-curve/) keeps neighboring cells close in memory too.
- **Combined with a Verlet list.** Build the [Verlet neighbor list](/verlet-neighbor-list/) with the cell list, using the cutoff $r_c$ plus the skin as the cell side. The list build then costs $O(N)$, and the list is reused for many steps (Frenkel and Smit, Appendix F.3).
- **Hashed cells.** When the box is not periodic or the atoms fill only a small part of it, store only the nonempty cells in a hash table keyed by the cell coordinates. This is [spatial hashing](/spatial-hashing/).
- **Non-cubic boxes.** In a box with edge vectors $a$, $b$ and $c$, cut each scaled coordinate into cells, and choose the number of cells along each edge so that the distance between opposite faces of a cell is at least $r_c$.
- **Chaining mesh.** In the [P3M method](/p3m-method/), Hockney and Eastwood use the same cells, with the short-range cutoff as the cell side, for the particle-particle part of the force.

## When to use it

Use a linked-cell list whenever the forces have a finite cutoff and the system has more than a few hundred atoms, so that the direct loop becomes the main cost. It suits [molecular dynamics](/molecular-dynamics/) with short-range pair potentials, the real-space part of [Ewald summation](/ewald-summation/), and [dissipative particle dynamics](/dissipative-particle-dynamics/). Use it alone when the atoms move fast relative to the cutoff, as in a hot gas, and pair it with a Verlet list when the atoms move little per step, as in a liquid or a solid. When the density varies strongly, for example a cluster in a mostly empty box, most cells are empty or crowded, and a [k-d tree](/kd-tree/) or an [octree](/octree/) adapts better. For forces without a cutoff, such as gravity or full Coulomb sums, the cells do not help; use the [Barnes-Hut algorithm](/barnes-hut-algorithm/), the [fast multipole method](/fast-multipole-method/) or Ewald methods.

## Pitfalls

- **Fewer than three cells per side.** With $s = 2$, the offsets $+1$ and $-1$ reach the same cell, so the pairs between those two cells are counted twice; with $s = 1$, the minimum image of a pair is not unique. Use the direct loop for small boxes, or check $L \ge 3 r_c$.
- **A cell side smaller than the cutoff.** If $\ell$ is chosen as $r_c$ rounded down, pairs at a distance between $\ell$ and $r_c$ can be two cells apart and are missed with no error message. Compute $s$ with a floor of $L / r_c$, never a ceiling.
- **Atoms outside the box.** An atom that has left $[0, L)$ gives a cell coordinate outside $[0, s)$. Wrap the position before the floor. In floating point, a tiny negative coordinate can wrap to exactly $L$; clamp the cell coordinate to $s - 1$, as the implementation does.
- **Forgetting the minimum image in the distance.** A pair found through a wrapped cell is a pair across the boundary, so the plain difference $r_i - r_j$ is wrong for it.
- **Double counting in the own cell.** In the own cell, test each atom only against the atoms after it in the chain. Otherwise each pair is found twice and each atom is tested against itself.
- **Claiming $O(N)$ without fixed density.** The bound needs a bounded number of atoms per cell. A system that condenses into a small region, or a test that adds atoms to a fixed box, does not have it.

## Implementations

## History

The cell search came into molecular dynamics through Quentrec and Brot in 1973, who cut the box into cells to find the neighbors of each atom quickly. Hockney and Eastwood used the same structure as the "chaining mesh" for the short-range part of their particle-particle particle-mesh method. Allen and Tildesley describe the form with a head array and a list array, after Knuth's linked lists and after Hockney and Eastwood, and it is now a standard part of molecular dynamics codes, together with the Verlet list of 1967.

## References
