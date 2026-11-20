---
tag: B4084E
kind: algorithm
slug: adaptive-fast-multipole-method
name: Adaptive fast multipole method
aliases:
- Carrier-Greengard-Rokhlin algorithm
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: "Refines the FMM tree only where particles are dense and uses four interaction lists (U, V, W and X), so the cost stays near linear in N for strongly nonuniform distributions."
model: real-ram
complexity:
  vars: {N: the number of charges, p: the number of terms of each expansion, s: the largest number of charges in a leaf, D: the number of levels of the tree}
  time: {best: "Θ(N p)", average: "Θ(N p^2 / s + N s)", worst: "O(D N (p^2 / s + p + s))"}
  space: {extra: "O(N + D N p / s)"}
properties: {deterministic: true}
history:
  year: 1988
  people: [J. Carrier, Leslie Greengard, Vladimir Rokhlin]
  note: Carrier, Greengard and Rokhlin published the adaptive version of the 2D fast multipole method in the SIAM Journal on Scientific and Statistical Computing in 1988.
prereqs: [fast-multipole-method, quadtree, multipole-to-local-translation]
see_also: [barnes-hut-algorithm, kernel-independent-fast-multipole-method, black-box-fast-multipole-method, multipole-truncation-error-bound, octree, hashed-oct-tree, z-order-curve, direct-n-body-summation]
sources:
  - paper: doi:10.1137/0909044
    title: "J. Carrier, L. Greengard and V. Rokhlin, A fast adaptive multipole algorithm for particle simulations, SIAM Journal on Scientific and Statistical Computing 9, 1988, 669-686"
    locator: the adaptive tree, the lists of boxes of different sizes and the numerical results for nonuniform distributions
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: "Lemma 4.7 for the error of the multipole-to-local step; Section 4.2 for a simpler adaptive scheme that only prunes empty boxes"
  - paper: doi:10.1016/j.jcp.2003.11.021
    title: "Lexing Ying, George Biros and Denis Zorin, A kernel-independent adaptive fast multipole algorithm in two and three dimensions, Journal of Computational Physics 196(2), 2004, 591-626"
    locator: the names U, V, W and X of the four lists of an adaptive tree
  - paper: doi:10.1137/0915046
    title: "Keith Nabors, F. T. Korsmeyer, F. T. Leighton and Jacob White, Preconditioned, adaptive, multipole-accelerated iterative methods for three-dimensional first-kind integral equations of potential theory, SIAM Journal on Scientific Computing 15(3), 1994, 713-735"
    locator: the proof that an adaptive multipole algorithm costs O(N) for any distribution of the charges
---

The adaptive fast multipole method computes the potentials and fields of $N$ charges on each other, like the [fast multipole method](/fast-multipole-method/), but on a tree that follows the charges. A box of the [quadtree](/quadtree/) is split only when it holds more than $s$ charges, and empty boxes are dropped, so dense clusters get deep, small leaves and empty regions get none. Leaves of different sizes can then touch, and the single interaction list of the uniform method is replaced by four lists. The $V$ list does the usual [multipole-to-local translations](/multipole-to-local-translation/) between boxes of one size. The $W$ and $X$ lists connect a leaf with smaller boxes near it, and the $U$ list holds the adjacent leaves for the direct sum. Carrier, Greengard and Rokhlin (1988) gave the method in 2D; this page uses the list names of Ying, Biros and Zorin (2004).

## In plain words

The plain FMM cuts the square into equal boxes. If most particles sit in a few small clumps, most boxes are empty and a few boxes are full, and the full boxes make the near sums slow. The adaptive FMM cuts a box again only when it has too many particles. So the boxes are small where the particles are crowded and large where they are thin.

Now a big box can touch small boxes. A small box that is near a big box but does not touch it is still far enough for a short summary. The method uses the summary of the small box at each particle of the big box, and it turns the particles of the big box into a summary for the small box. All other steps are as in the plain FMM.

## The problem

The input is $N$ real charges $q_i$ at distinct points $z_i$ of the unit square, written as complex numbers, a number of terms $p$ and a leaf size $s$. The output is an approximation of each potential and field

$$u_j = \sum_{i \ne j} q_i \log|z_j - z_i|, \qquad \nabla u_j = \sum_{i \ne j} q_i \frac{z_j - z_i}{|z_j - z_i|^2},$$

with the field written as a complex number, $\overline{\phi'(z_j)}$ for $\phi(z) = \sum_i q_i \log(z - z_i)$. The charges can be distributed in any way; the method should not slow down much when they are strongly clustered.

## The algorithm

Two boxes are *adjacent* if their closed squares share a point, and *colleagues* if they are adjacent and of the same level. For a leaf $b$:

- $U(b)$ is the set of leaves adjacent to $b$, with $b$ itself.
- $V(b)$, defined for every box at level 2 or deeper, is the set of children of the colleagues of the parent of $b$ that are not adjacent to $b$. It is the interaction list of the uniform FMM, at most 27 boxes.
- $W(b)$ is the set of boxes that descend from a colleague of $b$, are not adjacent to $b$, but have a parent that is adjacent to $b$. They are smaller than $b$.
- $X(d)$ is the set of leaves $b$ with $d \in W(b)$. It is the inverse of $W$.

```pseudo id=main
ADAPTIVE-FMM(q, z, p, s)
L1  build the tree: split each box with more than s charges, and drop empty boxes
L2  build U(b) and W(b) for each leaf b, V(b) for each box b, and X as the inverse of W
L3  for each box B from the finest level up: a_B ← P2M of the charges of B if B is a leaf, else Σ M2M(a_C) over the children C
    for each box B from the root down do
L4      b_B ← Σ M2L(a_C) over C in V(B)  +  Σ P2L(charges of C) over C in X(B)
L5      b_B ← b_B + L2L(b_P), where P is the parent of B
    for each leaf T and each charge j in T do
L6      u_j, field_j ← local expansion b_T at z_j  +  Σ multipole expansion a_C at z_j over C in W(T)
L7      add the direct terms of all charges i ≠ j in the leaves of U(T); return u, field
```

P2M, M2M, M2L and L2L are the translations of the [fast multipole method](/fast-multipole-method/). The two new operations are:

- **M2P**, line L6 (the $W$ list): evaluate the multipole expansion $a_0 \log(z - c) + \sum_k a_k (z - c)^{-k}$ of a small box at each target of the leaf, and its derivative $a_0 / (z - c) - \sum_k k a_k (z - c)^{-k-1}$.
- **P2L**, line L4 (the $X$ list): add the charges of a large leaf directly into the local expansion about the center $c$ of a small box, with $b_0 \mathrel{+}= q \log(c - z_i)$ and $b_l \mathrel{+}= -q / (l (z_i - c)^l)$.

The leaf $b$ can find its lists without a search over all boxes. The coarser leaves of $U(b)$ are leaf colleagues of the ancestors of $b$. The finer leaves of $U(b)$ and all of $W(b)$ come from one descent from the colleagues of $b$: a child that touches $b$ is followed further, and a child that does not touch $b$ goes into $W(b)$.

## Example

Take $N = 400$ charges uniform in $[-1, 1]$: 85 percent of the points are in three Gaussian clusters of standard deviation $0.02$ about $(0.2, 0.3)$, $(0.7, 0.75)$ and $(0.8, 0.2)$, and the rest are uniform in the unit square (the generator of the test file, seed 3). With $s = 10$ the tree has 144 boxes and 104 leaves at the levels 2 to 7. The lists have 750 ($U$), 850 ($V$), 310 ($W$) and 310 ($X$) entries in total, and no $V$ list has more than 15 boxes. The near field uses 14266 ordered pairs, against $400 \cdot 399 = 159600$ for direct summation. Against direct summation:

| $p$ | relative error of $u$ (2-norm) | largest error of $u$ | relative error of the field (2-norm) |
|---|---|---|---|
| 3 | $4.1 \times 10^{-4}$ | $3.6 \times 10^{-2}$ | $3.7 \times 10^{-3}$ |
| 6 | $7.5 \times 10^{-6}$ | $8.9 \times 10^{-4}$ | $1.5 \times 10^{-4}$ |
| 9 | $2.7 \times 10^{-7}$ | $3.5 \times 10^{-5}$ | $5.5 \times 10^{-6}$ |
| 12 | $1.1 \times 10^{-8}$ | $1.2 \times 10^{-6}$ | $3.1 \times 10^{-7}$ |
| 16 | $2.7 \times 10^{-10}$ | $3.6 \times 10^{-8}$ | $6.5 \times 10^{-9}$ |
| 20 | $5.8 \times 10^{-12}$ | $8.8 \times 10^{-10}$ | $2.9 \times 10^{-10}$ |

These are measurements. The errors fall at the same rate as for the uniform FMM on uniform points. For the same charges, the uniform FMM of the [fast multipole method](/fast-multipole-method/) page with leaves at level 3 uses 47596 ordered pairs in the near field. With leaves at level 6 it uses 14180 pairs, but it needs 5404 M2L translations, against 850 here, because a uniform tree that is deep enough for the clusters has many boxes in the thin background.

## Correctness

The proof is in the proof file. Adjacency of the ancestors of two leaves holds at an initial range of levels. A case analysis on the level where it first fails, and on which leaf is coarser, shows that each source leaf reaches each target leaf by exactly one of the four routes: the direct sum ($U$), one M2L at a common level ($V$), one multipole evaluation of a smaller box ($W$), or one direct local expansion into a smaller box ($X$) (Lemma 3). The $V$ boxes are separated as in the uniform method, so Lemma 4.7 of Beatson and Greengard bounds their error with the ratio $1 / (2\sqrt{2} - 1) \approx 0.55$. A box of $W(b)$ is at least $1.5$ of its own sides from every point of $b$, so the [truncation bound](/multipole-truncation-error-bound/) applies with the ratio $\sqrt{2} / 3 \approx 0.47$, and the same holds for $X$ (Lemma 4). The translations M2M and L2L are exact, so the total error is at most $\sum_i |q_i|$ times a factor that tends to 0 as $p$ grows (Theorem).

## Complexity

The model is the [real RAM](/real-ram/), with $D$ the number of levels of the tree.

- **Boxes (theorem).** A box is split only if it holds more than $s$ charges, and the boxes of one level are disjoint, so each level has at most $N / s$ split boxes and at most $4 N / s$ boxes. The tree has $O(D N / s)$ boxes.
- **Lists (theorem).** Each $V$ list has at most 27 boxes. A leaf touches only a bounded number of leaves that are at least as large as it, so the $U$ lists have $O(D N / s)$ entries in total. A box $d$ is in $W(b)$ only for leaves $b$ that touch the parent of $d$ and are at least as large as it, so the $W$ and $X$ lists also have $O(D N / s)$ entries in total.
- **Work.** P2M and L2P cost $O(N p)$; M2M, L2L and M2L cost $O(p^2)$ per box and list entry; M2P and P2L cost $O(s p)$ per list entry; the direct sum costs $O(s^2)$ per entry of $U$. The total is $O(N p + D N (p^2 / s + p + s))$. For a depth $D$ that does not grow with $N$, this is $O(N)$ for fixed $p$ and $s$.
- **Any distribution.** The depth can grow without bound if two charges are very close, so the bound above is not $O(N)$ for every input. Nabors, Korsmeyer, Leighton and White (1994) proved an $O(N)$ bound for every distribution for an adaptive scheme that also compresses chains of boxes with one child.
- **Measured.** For the clustered generator of the example, with $s = 10$ and $p = 10$, the near field uses 38.4, 39.7 and 41.5 ordered pairs per charge, and the tree has 165, 611 and 2388 boxes, for $N = 500$, $2000$ and $8000$: both grow linearly with $N$.
- **Reported.** Carrier, Greengard and Rokhlin report that, for 25600 particles in a strongly nonuniform distribution, their code was about 200 times faster than direct summation, about 3 times faster than the nonadaptive FMM and needed about a quarter of its storage.
- **Space.** $O(N)$ for the charges and $O(p)$ coefficients per box, so $O(N + D N p / s)$.

## Properties

- **Same accuracy as the uniform FMM.** The new routes $W$ and $X$ have a smaller ratio than $V$, so the error bound is the one of the uniform method.
- **Linear in the charges.** The output is a linear function of $q$, so the method is a fast matrix-vector product inside iterative solvers.
- **Exact near field.** All pairs of adjacent leaves, of any sizes, are summed directly.
- **Deterministic.** The tree and the lists depend only on the positions and on $s$, not on the order of the charges.

## Variants and improvements

- **Kernel independent and black box versions.** The [kernel-independent FMM](/kernel-independent-fast-multipole-method/) uses the same four lists with equivalent densities, and the [black-box FMM](/black-box-fast-multipole-method/) with Chebyshev interpolation.
- **Three dimensions.** The same lists work on an [octree](/octree/); the $V$ list has up to 189 boxes.
- **Level-restricted trees.** Many codes refine the tree further so that adjacent leaves differ by at most one level (a 2:1 balance). Then the $W$ and $X$ lists are short and the cost per box is bounded.
- **Pruning only.** Beatson and Greengard (Section 4.2) describe a simpler adaptive scheme that only drops empty boxes of a uniform tree.
- **Parallel trees.** A [hashed oct-tree](/hashed-oct-tree/) with keys on a [Z-order curve](/z-order-curve/) lets parallel codes distribute the boxes and find the lists by key arithmetic.

## When to use it

Use the adaptive FMM when the charges are strongly nonuniform, for example particles in clusters, boundary points of complicated curves, or vortex sheets that roll up, and you need a guaranteed accuracy. For nearly uniform points, the uniform FMM is simpler and as fast. For low accuracy, the [Barnes-Hut algorithm](/barnes-hut-algorithm/), which is adaptive by nature, is simpler. For small $N$, use [direct summation](/direct-n-body-summation/).

## Pitfalls

- **Missing or double interactions.** The four lists must cover each pair of leaves exactly once. A small error in the definition of adjacency, for example open instead of closed squares, loses corner neighbours or counts them twice. Test the coverage of every pair of leaves on a small clustered input.
- **The order of the downward pass.** The $X$ contributions are added into the local expansion of a box before L2L passes it to the children. If they are added at the leaves only, the descendants of a box of $W$ miss them.
- **Coincident points.** Two equal points make every box that holds them split forever. Limit the depth, and treat equal points by the near field.
- **Long $U$ and $W$ lists.** Without a 2:1 balance, a large leaf next to a deeply refined region can have very long lists. The total is bounded, but the work per box is not.
- **Leaf size.** A small $s$ makes many boxes and many translations; a large $s$ makes the direct sums slow. Choose $s$ near $p$ in 2D and measure.

## Implementations

## History

Greengard and Rokhlin (1987) gave the fast multipole method on a uniform tree. Carrier, Greengard and Rokhlin (1988) made the tree adaptive and added the lists for boxes of different sizes, which kept the cost close to linear for strongly nonuniform charges. Nabors, Korsmeyer, Leighton and White (1994) proved an $O(N)$ bound for any distribution for an adaptive multipole scheme in 3D. Ying, Biros and Zorin (2004) used the same lists, named $U$, $V$, $W$ and $X$, in their kernel-independent adaptive FMM.

## References
