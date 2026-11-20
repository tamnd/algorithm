---
tag: 2RM7MC
kind: algorithm
slug: fast-multipole-method
name: Fast multipole method
aliases:
- Greengard-Rokhlin fast multipole method
area: scientific-computing/n-body-and-particle-methods
level: core
summary: "Evaluates all pairwise interactions of N particles to a set accuracy in O(N) time, with multipole and local expansions on a tree and translations between them."
model: real-ram
complexity:
  vars: {N: the number of charges, p: the number of terms of each expansion, s: the mean number of charges in a leaf box}
  time: {best: "Θ(N p)", average: "Θ(N p^2 / s + N s)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N + N p / s)"}
properties: {deterministic: true}
history:
  year: 1987
  people: [Leslie Greengard, Vladimir Rokhlin]
  note: Greengard and Rokhlin published the 2D method with multipole and local expansions and an error bound in the Journal of Computational Physics in 1987.
prereqs: [direct-n-body-summation, quadtree, multipole-expansion, multipole-truncation-error-bound, multipole-to-local-translation]
see_also: [barnes-hut-algorithm, adaptive-fast-multipole-method, kernel-independent-fast-multipole-method, black-box-fast-multipole-method, fast-gauss-transform, multipole-acceptance-criterion, octree, boundary-element-method]
sources:
  - paper: doi:10.1016/0021-9991(87)90140-9
    title: "Leslie Greengard and Vladimir Rokhlin, A fast algorithm for particle simulations, Journal of Computational Physics 73(2), 1987, 325-348"
    locator: the 2D algorithm with the logarithmic kernel, the translation lemmas, the error bound and the operation count
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: Section 4 (Lemmas 4.2 and 4.6 to 4.8, the interaction list and the operation count of the FMM) and Section 5 (three dimensions)
  - book: isbn:9780262071109
    title: Leslie Greengard, The Rapid Evaluation of Potential Fields in Particle Systems, MIT Press, 1988
    locator: the 3D algorithm with spherical harmonic expansions and its error bounds
  - paper: doi:10.1137/0915046
    title: "Keith Nabors, F. T. Korsmeyer, F. T. Leighton and Jacob White, Preconditioned, adaptive, multipole-accelerated iterative methods for three-dimensional first-kind integral equations of potential theory, SIAM Journal on Scientific Computing 15(3), 1994, 713-735"
    locator: the proof that an adaptive multipole algorithm costs O(N) for any distribution of the charges
---

The fast multipole method (FMM) computes the potentials and forces of $N$ charges or masses on each other to a set accuracy. It puts the particles in a tree of boxes, a [quadtree](/quadtree/) in 2D and an [octree](/octree/) in 3D. Each box gets a [multipole expansion](/multipole-expansion/) of its own particles, built from the leaves up. Each box then gets a local (Taylor) expansion of the field of all particles that are not near it, built from the root down: a [multipole-to-local translation](/multipole-to-local-translation/) brings in the boxes of its interaction list, and the parent passes down the rest. At the leaves, the local expansion gives the far field at each particle, and the near field is summed directly. With $p$ terms in each expansion, the error falls geometrically in $p$ by the [truncation bound](/multipole-truncation-error-bound/), and for a fixed $p$ and a uniform distribution the cost is $O(N)$ instead of the $\Theta(N^2)$ of [direct summation](/direct-n-body-summation/). This page gives the 2D method of Greengard and Rokhlin (1987) for the logarithmic kernel.

## In plain words

The pull of a far group of particles is smooth, so a short list of numbers describes it well. The FMM uses two kinds of such lists. The first kind says how one box pulls on everything far from it. The second kind says how everything far away pulls on the points inside one box.

Put the particles in boxes, and cut each box into four smaller ones, a few times. Make the first list for each small box, then merge the lists of four boxes into the list of their parent. Then, for each box, turn the first lists of the boxes at a medium distance into a second list for this box, and add the second list of its parent. At the bottom, each particle reads the far pull from the second list of its box and adds the pull of its close neighbours one by one.

## The problem

The input is $N$ real charges $q_i$ at distinct points $z_i = x_i + \mathrm{i} y_i$ of the unit square, written as complex numbers, and a number of terms $p$. The output is an approximation of each potential and field

$$u_j = \sum_{i \ne j} q_i \log|z_j - z_i|, \qquad \nabla u_j = \sum_{i \ne j} q_i \frac{z_j - z_i}{|z_j - z_i|^2},$$

where the field is written as a complex number. The potential $u$ is the real part of the complex potential $\phi(z) = \sum_i q_i \log(z - z_i)$, and $\nabla u = \overline{\phi'(z)}$. In 2D gravity with $G = 1$, the potential of a mass $m_i$ is $m_i \log|z - z_i|$ and the acceleration is $-\nabla u$. The error is measured against direct summation and is bounded in terms of $p$ and $A = \sum_i |q_i|$.

## The algorithm

Level $l$ of the tree has $4^l$ boxes of side $2^{-l}$. The leaves are at level $L$, chosen so that a leaf holds about $s$ charges. Two boxes of one level are near neighbours if they touch, even at a corner. The interaction list of a box is the set of children of the near neighbours of its parent that are not near neighbours of the box; it has at most 27 boxes.

```pseudo id=main
FMM(q, z, p, L)
L1  for each leaf B: a_B ← P2M of the charges of B about the center of B
L2  for l ← L - 1 down to 2: for each box B at level l: a_B ← Σ M2M(a_C) over the children C of B
    for l ← 2 to L do
L3      for each box B at level l: for each box T in the interaction list of B: b_T ← b_T + M2L(a_B)
L4      if l < L then for each box T at level l: for each child D of T: b_D ← b_D + L2L(b_T)
    for each leaf T and each charge j in T do
L5      u_j ← Re of the local expansion b_T at z_j;  field_j ← conj of its derivative
L6      add the direct terms of all charges i ≠ j in T and in the near neighbours of T
L7  return u, field
```

The four translations are, with all centers moved so that the new center is $0$ and the old center is $z_0$ (Lemmas 4.2 and 4.6 to 4.8 of Beatson and Greengard):

- **P2M**, line L1: $a_0 = \sum q_i$ and $a_k = -\sum q_i (z_i - c)^k / k$ for $1 \le k \le p$, so that $\phi(z) \approx a_0 \log(z - c) + \sum_{k=1}^{p} a_k / (z - c)^k$.
- **M2M**, line L2: $b_0 = a_0$ and $b_l = -a_0 z_0^l / l + \sum_{k=1}^{l} a_k z_0^{l-k} \binom{l-1}{k-1}$.
- **M2L**, line L3: $b_0 = a_0 \log(-z_0) + \sum_{k=1}^{p} (-1)^k a_k z_0^{-k}$ and $b_l = -a_0 / (l z_0^l) + z_0^{-l} \sum_{k=1}^{p} (-1)^k a_k z_0^{-k} \binom{l+k-1}{k-1}$; see [multipole-to-local translation](/multipole-to-local-translation/).
- **L2L**, line L4: the Taylor shift of the polynomial $\sum_k b_k (z - z_0)^k$, done in place by Horner's scheme.

Lines L1 and L2 are the upward pass, and lines L3 and L4 the downward pass. The order matters only in one place: the local expansion of a box at level $l$ must hold all its M2L terms before line L4 passes it to the children. Levels 0 and 1 have empty interaction lists, because all their boxes touch.

## Example

Take $N = 400$ charges uniform in $[-1, 1]$ at points uniform in the unit square (seed 5), and $L = 3$, so the 64 leaves hold 6.25 charges on average. Direct summation uses $400 \cdot 399 = 159600$ ordered pairs. The FMM of the implementation uses 18302 ordered pairs in the near field and 1272 M2L translations, the same for every $p$. Against direct summation:

| $p$ | relative error of $u$ (2-norm) | largest error of $u$ | relative error of the field (2-norm) |
|---|---|---|---|
| 3 | $6.6 \times 10^{-4}$ | $2.7 \times 10^{-2}$ | $3.9 \times 10^{-3}$ |
| 6 | $1.8 \times 10^{-5}$ | $1.0 \times 10^{-3}$ | $1.6 \times 10^{-4}$ |
| 9 | $6.4 \times 10^{-7}$ | $3.2 \times 10^{-5}$ | $7.7 \times 10^{-6}$ |
| 12 | $3.0 \times 10^{-8}$ | $1.7 \times 10^{-6}$ | $4.7 \times 10^{-7}$ |
| 16 | $7.3 \times 10^{-10}$ | $5.3 \times 10^{-8}$ | $1.5 \times 10^{-8}$ |
| 20 | $1.8 \times 10^{-11}$ | $1.6 \times 10^{-9}$ | $4.8 \times 10^{-10}$ |

These are measurements. Each extra term gains a factor of about 2.5 in the potential. The worst-case bound of the proof falls by a factor $\gamma = 2\sqrt{2} - 1 \approx 1.83$ per term, so it is pessimistic for random charges. The field loses about one digit against the potential, because a derivative of the expansion has larger coefficients.

The 1272 translations follow from the interaction lists: each of the 16 boxes at level 2 and each of the 64 boxes at level 3 sends its expansion to every box of its list, and boxes at the edge of the square have shorter lists than the 27 of an interior box.

## Correctness

The proof is in the proof file. The near-neighbour relation of two leaves holds at an initial range of levels, so each far charge is used exactly once, through the one ancestor pair at which the relation first fails (Lemma 1). The M2M and L2L steps are exact for $p$-term expansions (Lemmas 2 and 3), so the only errors come from the truncations in M2L. Two boxes of the interaction list have centers at least $2w$ apart, and their charges and targets lie within $w / \sqrt{2}$ of the centers. Lemma 4.7 of Beatson and Greengard then bounds the error of each M2L step by a constant times $A_c (1/\gamma)^{p+1}$, with $\gamma = 2\sqrt{2} - 1$ and $A_c$ the total absolute charge of the source box. The errors add over the disjoint source boxes, so the total error is at most $\sum_i |q_i|$ times the same factor, and it tends to 0 as $p \to \infty$ (Theorem).

## Complexity

The model is the [real RAM](/real-ram/). Each step is counted in complex operations, for a uniform distribution with $s$ charges per leaf, so that there are about $N / s$ leaves.

- **Operation count (theorem for the uniform tree).** Beatson and Greengard count about $N p$ operations for P2M, $29 (N/s) p^2$ for the M2M, M2L and L2L translations, $N p$ for L2P and $9 N s$ for the near field. With $s = p$ the total is about $40 N p$. Each translation costs $O(p^2)$ in 2D, and there are at most $27$ M2L translations per box and $4$ M2M and $4$ L2L translations per parent. The total is $\Theta(N p^2 / s + N s + N p)$, which is $\Theta(N p)$ for $s$ near $p$, and $O(N)$ for a fixed $p$.
- **Measured.** With $s = 8$, $p = 10$ and random charges (seed 7), the near field uses 44.5, 58.2 and 64.4 ordered pairs per charge for $N = 125$, $500$ and $2000$. The count per charge tends to a constant near $9 s$, as the operation count says; it is smaller for small $N$, because more boxes are at the edge.
- **Accuracy and cost together.** For an accuracy $\varepsilon$, the bound needs $p = O(\log(1/\varepsilon))$ terms, so with $s \approx p$ the cost is $O(N \log(1/\varepsilon))$.
- **Worst case.** A uniform tree does not follow the charges. If all charges fall into a few leaves, the near field is $\Theta(N^2)$. The [adaptive FMM](/adaptive-fast-multipole-method/) fixes this for a tree of bounded depth, and Nabors, Korsmeyer, Leighton and White (1994) proved an $O(N)$ bound for every distribution for their adaptive scheme.
- **Space.** $\Theta(N)$ for the charges and $\Theta(p)$ coefficients per box, so $\Theta(N + N p / s)$.
- **Three dimensions.** An expansion has $(p + 1)^2$ terms, an interior box has an interaction list of 189 boxes, and a direct M2L costs $O(p^4)$. This is why the faster 3D translations of the variants below matter.

## Properties

- **Error control.** The error is bounded in terms of $p$ by a theorem, not set by a rule of thumb as the opening angle of the [Barnes-Hut algorithm](/barnes-hut-algorithm/) is. The bound is a worst case and is usually far above the measured error.
- **Linear in the charges.** The output is a linear function of $q$. This is what lets the FMM act as a fast matrix-vector product inside an iterative solver such as [GMRES](/gmres/) for [boundary element](/boundary-element-method/) equations.
- **Exact translations.** M2M and L2L lose nothing; all the truncation error is in P2M, M2L and L2P.
- **Not symmetric.** Like a tree code, the FMM does not apply equal and opposite forces to each pair, so momentum is conserved only up to the error.
- **Deterministic.** The result does not depend on the order of the charges, up to rounding.

## Variants and improvements

- **Adaptive trees.** The [adaptive FMM](/adaptive-fast-multipole-method/) of Carrier, Greengard and Rokhlin (1988) refines only where there are many charges and adds two more lists for boxes of different sizes.
- **Faster 3D translations.** Rotation-based translations cost $O(p^3)$, and the plane-wave (exponential) expansions of Greengard and Rokhlin (1997) cut the M2L work further. FFT-based M2L uses the Toeplitz structure of the operator.
- **Kernel independent and black box versions.** The [kernel-independent FMM](/kernel-independent-fast-multipole-method/) replaces the expansions with equivalent densities on circles or surfaces, and the [black-box FMM](/black-box-fast-multipole-method/) uses Chebyshev interpolation; both need only kernel evaluations.
- **Other kernels.** The same tree with Hermite expansions gives the [fast Gauss transform](/fast-gauss-transform/), and expansions in Bessel functions give FMMs for the Helmholtz and Yukawa kernels.
- **Mesh hybrids.** For periodic gravity, [P3M](/p3m-method/) and [TreePM](/treepm-method/) combine a mesh for the long range with direct sums or a tree for the short range.

## When to use it

Use the FMM when you need many potentials or forces with a guaranteed accuracy and $N$ is large, for example $N \ge 10^4$ in 2D: in vortex methods, electrostatics, boundary integral equations solved by iteration, and charged particle simulations. For low accuracy (one percent) the [Barnes-Hut algorithm](/barnes-hut-algorithm/) is simpler and often as fast. For periodic systems, a mesh method such as [particle-mesh Ewald](/particle-mesh-ewald/) is usually easier. For small $N$, use [direct summation](/direct-n-body-summation/).

## Pitfalls

- **Using M2L for near boxes.** The M2L series converges only when the boxes are well separated. Converting a near neighbour gives wrong results without a warning. Build the interaction list exactly by the definition.
- **The order of the downward pass.** A box must receive all its M2L terms before L2L passes its expansion to its children.
- **Scaling.** For large $p$, the powers $z_0^k$ and $a_k$ overflow or underflow. Store the coefficients scaled by the box size, $a_k / w^k$ and $b_l w^l$.
- **The branch of the logarithm.** The imaginary part of $\log(-z_0)$ in M2L depends on the branch. The potential uses only the real part, which is safe, but code that uses the imaginary part (the stream function) must keep the branch cuts consistent.
- **Measuring the error of one example only.** The error depends on the distribution, on the signs of the charges and on $p$. Check against direct summation on a sample of targets for the real problem.
- **Unbalanced trees.** With a uniform tree, a clustered distribution puts many charges in a few leaves, and the near field becomes $\Theta(N^2)$. Use the adaptive version.

## Implementations

## History

Rokhlin (1985) used multipole ideas for the integral equations of potential theory. Greengard and Rokhlin (1987) published the fast multipole method for particle simulations in 2D, with the complex form of the logarithmic potential, the translations and the error bounds. Greengard's thesis, published by MIT Press in 1988, extended the method to 3D with spherical harmonics. Carrier, Greengard and Rokhlin (1988) gave the adaptive version, and Greengard and Rokhlin (1997) a faster 3D version with plane-wave expansions. Later work gave kernel independent forms (Ying, Biros and Zorin 2004) and black box forms (Fong and Darve 2009).

## References
