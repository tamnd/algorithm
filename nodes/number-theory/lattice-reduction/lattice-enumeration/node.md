---
tag: JQAH1H
kind: technique
slug: lattice-enumeration
name: Lattice enumeration
aliases:
- exhaustive lattice search
- sphere decoding
- lattice point enumeration
area: number-theory/lattice-reduction
level: advanced
summary: Searches all lattice vectors within a radius using a tree over the Gram-Schmidt coefficients.
prereqs: [gram-schmidt-orthogonalization, lattice-basis, depth-first-search]
see_also: [fincke-pohst-enumeration, schnorr-euchner-enumeration, kannan-enumeration, shortest-vector-problem, closest-vector-problem, bkz-algorithm, lattice-sieving, depth-first-branch-and-bound]
sources:
  - paper: "U. Fincke and M. Pohst, Improved methods for calculating vectors of short length in a lattice, including a complexity analysis, Mathematics of Computation 44 (1985)"
    locator: pages 463 to 471 (enumeration of the vectors in an ellipsoid by bounds on one coordinate at a time, from a Cholesky decomposition of the Gram matrix)
  - paper: "C. P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66, 1994"
    locator: pages 181 to 199 (the enumeration procedure with the zig-zag order and its use inside block reduction)
  - paper: "G. Hanrot and D. Stehlé, Improved analysis of Kannan's shortest lattice vector algorithm, Advances in Cryptology, CRYPTO 2007, LNCS 4622"
    locator: the bound on the number of enumeration nodes for a quasi-HKZ-reduced basis, n^(n/(2e) + o(n))
  - paper: "N. Gama, P. Q. Nguyen and O. Regev, Lattice enumeration using extreme pruning, Advances in Cryptology, Eurocrypt 2010, LNCS 6110"
    locator: the pruned enumeration tree, its cost from the Gaussian heuristic, and extreme pruning with many randomized bases
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 18.5, Enumeration of all short lattice points (the enumeration tree and its use for SVP and CVP)
---

Lattice enumeration lists all lattice vectors in a ball by a depth-first search over their coordinates in a basis, from the last coordinate to the first. Fixing the last coordinates fixes the projection of the vector orthogonal to the earlier basis vectors, and the length of that projection gives a lower bound on the length of every completion; branches whose bound exceeds the radius are cut. It solves the [shortest](/shortest-vector-problem/) and [closest vector](/closest-vector-problem/) problems exactly, in polynomial space, and its running time depends heavily on how well the basis is reduced. It is the subroutine of [BKZ](/bkz-algorithm/) and the main exact method in dimensions up to about one hundred.

## In plain words

To list all lattice points near the origin, choose the coordinates one at a time, starting with the last basis vector. Once the last few coordinates are chosen, part of the vector is fixed: the part that points in directions the remaining basis vectors cannot reach. If that part is already longer than the radius, no choice of the remaining coordinates can help, so that branch is dropped.

Each level of the search has only a few possible values, because the allowed values form a short interval around a center that depends on the choices above. The search walks this tree of choices and reports every leaf that stays within the radius. With a good basis the tree is small; with a bad basis it can be huge.

## When it applies

- You need all lattice vectors of length at most $R$, or a shortest vector, or a closest vector to a target, exactly.
- The dimension is moderate, so a cost exponential in $n$ is acceptable, and memory is limited: enumeration needs only $O(n^2)$ numbers, unlike [sieving](/lattice-sieving/).
- A good basis is available or can be computed, for example by [LLL](/lll-algorithm/) or BKZ, and a radius $R$ is known that is not much larger than the answer: $\|b_1\|$, the [Gaussian heuristic](/gaussian-heuristic/), or Minkowski's bound $\sqrt n \det(L)^{1/n}$.
- The same structure appears whenever a positive definite quadratic form must be minimized over the integers, for example in decoding for multiple antenna channels, where enumeration is called sphere decoding.

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n$, Gram-Schmidt vectors $b_i^*$ with $B_i = \|b_i^*\|^2$, coefficients $\mu_{ij}$, first minimum $\lambda_1$ and determinant $\det(L)$. Let $\pi_k$ be the projection orthogonal to $\operatorname{span}(b_1, \ldots, b_{k-1})$.

## The template

For $v = \sum_i x_i b_i$, write $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$ and collect terms along each $b_k^*$:

$$v = \sum_{k=1}^n (x_k - c_k) b_k^*, \qquad c_k = -\sum_{j > k} x_j \mu_{jk}, \qquad \|\pi_k(v)\|^2 = \ell_k = \sum_{i \ge k} (x_i - c_i)^2 B_i.$$

The center $c_k$ depends only on $x_{k+1}, \ldots, x_n$, and $\ell_k = \ell_{k+1} + (x_k - c_k)^2 B_k$. So $\ell_n \le \ell_{n-1} \le \cdots \le \ell_1 = \|v\|^2$, and $\|v\| \le R$ forces $\ell_k \le R^2$ at every level. The template walks the tree whose nodes at level $k$ are the partial vectors $(x_k, \ldots, x_n)$ with $\ell_k \le R_k^2$. It has three holes: ORDER (the order of the values tried at one level), BOUND (the radii $R_k$) and VISIT (what to do at a leaf).

```pseudo id=main
ENUMERATE(μ, B_1..B_n, R)                ▷ all x with ‖Σ x_i b_i‖ ≤ R, as a loop
L1  k ← n; ℓ_n+1 ← 0; c_n ← 0; x_n ← FIRST(c_n)
L2  while k ≤ n do
L3      ℓ_k ← ℓ_k+1 + (x_k − c_k)² · B_k
L4      if ℓ_k ≤ R_k² then                  ▷ hole BOUND: R_k = R for full enumeration
L5          if k = 1 then
L6              VISIT(x); x_1 ← NEXT(x_1)    ▷ hole VISIT: report, or shrink R
L7          else
L8              k ← k − 1; c_k ← −Σ_{j>k} x_j μ_jk; x_k ← FIRST(c_k)
L9      else
L10         k ← k + 1; if k ≤ n then x_k ← NEXT(x_k)   ▷ hole ORDER
```

**The rule for ORDER.** The values of $x_k$ must be tried so that once one fails the test of line L4, all later ones fail too; then going up at line L10 loses nothing. Two orders satisfy it:

- *Increasing order* (Fincke and Pohst): FIRST$(c) = \lceil c - r \rceil$ with $r = \sqrt{(R_k^2 - \ell_{k+1}) / B_k}$ and NEXT$(x) = x + 1$. The values in the interval $[c - r, c + r]$ all pass, and the first value above it fails, as do all larger ones.
- *Zig-zag order* (Schnorr and Euchner): FIRST$(c) = \lfloor c \rceil$, then the integers by increasing distance from $c$, alternating sides. Then $(x_k - c_k)^2$ never decreases, which also makes the first leaves found short.

**Correctness.** Every vector $v$ with $\|v\| \le R$ has $\ell_k \le R^2$ for all $k$, so all prefixes of its coordinate vector pass line L4 with $R_k = R$, and by the ORDER rule the search reaches it. Every visited leaf has $\ell_1 = \|v\|^2 \le R^2$. The tree is finite because each level has an interval of length $2r$. For SVP, skip $x = 0$ and visit only one of $\pm x$, for example by requiring the last nonzero coordinate to be positive.

**Cost.** The number of nodes at level $k$ is the number of vectors of the projected lattice $\pi_k(L)$ of length at most $R$. The work per node is $O(n)$ for the center, or $O(1)$ amortized with a table of partial sums. Space is $O(n^2)$.

- *Proved, any reduced basis.* At level $k$ at most $2R / \sqrt{B_k} + 1$ values pass. For an [LLL-reduced](/lll-reduction/) basis and $R = \|b_1\|$, $B_k \ge \alpha^{-(k-1)} \|b_1\|^2$, so the tree has at most $\prod_k (2 \alpha^{(k-1)/2} + 1) = 2^{O(n^2)}$ nodes.
- *Proved, strong preprocessing.* With a quasi-HKZ-reduced basis, [Kannan's algorithm](/kannan-enumeration/) enumerates $n^{n/(2e) + o(n)}$ nodes (Hanrot and Stehlé), so SVP is solved in time $n^{n/(2e) + o(n)}$ and polynomial space.
- *Heuristic.* By the [Gaussian heuristic](/gaussian-heuristic/), level $k$ has about $V_{n-k+1} R^{n-k+1} / \prod_{i \ge k} \sqrt{B_i}$ nodes, where $V_d$ is the volume of the unit ball. For a basis whose Gram-Schmidt lengths follow the geometric series assumption with [root Hermite factor](/root-hermite-factor/) $\delta_0$, the middle levels dominate and the count is about $\delta_0^{n^2/4}$ times $2^{O(n)}$: still $2^{O(n^2)}$, but with a small constant.

**Example.** The basis $(1, 2, 3, 4), (2, 5, 7, 9), (3, 7, 11, 14), (4, 9, 14, 20)$ has $B = (30, 3/10, 1/3, 4/3)$, and its lattice has $\lambda_1 = 1$. Full enumeration with $R = 1$ visits 16 nodes. LLL turns it into $(0, -1, 0, 0), (0, 0, 1, 1), (1, 0, -1, 0), (-1, 0, -1, 0)$ with $B = (1, 2, 3/2, 4/3)$, and the same enumeration visits 6 nodes. The small $B_2 = 3/10$ of the first basis makes the interval at level 2 wide. The gap grows quickly with the dimension.

## Classic examples

- **[Fincke-Pohst enumeration](/fincke-pohst-enumeration/).** The template with increasing order and a fixed radius, computed from a Cholesky decomposition of the Gram matrix; it lists all vectors in an ellipsoid.
- **[Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/).** Zig-zag order and a radius that shrinks each time a shorter vector is found; the standard SVP subroutine of BKZ.
- **[Kannan's enumeration](/kannan-enumeration/).** Recursively HKZ-reduces the basis before enumerating, which gives the best proved bound $n^{O(n)}$, improved to $n^{n/(2e) + o(n)}$ by Hanrot and Stehlé.
- **[BKZ](/bkz-algorithm/).** Runs enumeration on projected blocks $\pi_i(b_i), \ldots, \pi_i(b_{i+\beta-1})$ of size $\beta$.
- **[Closest vector problem](/closest-vector-problem/) and [bounded distance decoding](/bounded-distance-decoding/).** The same tree with the target included in the centers solves CVP exactly; see Variations.

## Variations

- **CVP.** For a target $t$ in the span, write $t = \sum_k \tau_k b_k^*$ and use the centers $c_k = \tau_k - \sum_{j > k} x_j \mu_{jk}$; then $\ell_1 = \|t - v\|^2$. Starting with the radius of [Babai's nearest plane](/babai-nearest-plane/) answer, $R^2 = \frac14 \sum_k B_k$ at most, guarantees a nonempty search.
- **Pruning.** Use radii $R_k < R$ at the levels near the root of the tree, large $k$, where few coordinates are fixed. The search then misses some vectors, but the tree shrinks far more than the success probability. Gama, Nguyen and Regev proposed extreme pruning: very small bounds, repeated on many randomized bases, which gives an exponential speedup in practice over full enumeration.
- **Counting and listing.** With VISIT = count, enumeration computes the number of lattice vectors in a ball, the first coefficients of the theta series of the lattice.
- **Parallel enumeration.** The tree can be split among processors at an upper level; the subtrees are independent.

## Pitfalls

- **Poorly reduced input.** The tree size depends on $\prod_k \sqrt{B_k}$ in the lower levels; a basis with tiny $B_k$ at some level makes the intervals there wide. Always reduce with LLL or BKZ first.
- **Wrong direction of the search.** The coordinates must be fixed from $x_n$ down to $x_1$, because $c_k$ depends on the later coordinates; fixing $x_1$ first gives no bound.
- **Recursion.** A recursive version has depth $n$, which is fine in most languages, but an explicit loop as above is easier to stop, prune and parallelize.
- **Floating point radii.** Computing $r = \sqrt{(R^2 - \ell_{k+1}) / B_k}$ in floating point can drop a boundary value. Test the exact condition $(x_k - c_k)^2 B_k \le R^2 - \ell_{k+1}$ when exactness matters, and try one more value on each side.
- **Symmetry and the zero vector.** For SVP, the zero vector passes every test and every vector appears with its negative; exclude 0 and halve the work at the top level.
- **Too large a radius.** The cost grows like $R^n$. Start from $\|b_1\|$ of a reduced basis, or from the Gaussian heuristic when a probabilistic answer is enough.

## References
