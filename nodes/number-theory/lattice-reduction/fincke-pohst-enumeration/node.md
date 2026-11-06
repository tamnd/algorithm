---
tag: 0T8BFG
kind: algorithm
slug: fincke-pohst-enumeration
name: Fincke-Pohst enumeration
aliases:
- Fincke-Pohst
- sphere decoding
- Fincke-Pohst algorithm
- Pohst enumeration
area: number-theory/lattice-reduction
level: advanced
summary: Enumeration of lattice points in a ball via Cholesky-based recursive pruning.
solves: [closest-vector-problem, shortest-vector-problem, bounded-distance-decoding]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, R: the squared radius, T: the number of nodes of the search tree, at most the sum over k of the product over i >= k of (2 (R / ‖b_i*‖^2)^(1/2) + 1)}
  time: {worst: O(n^2 m + n T), best: O(n^2 m), lll_basis_svp: 2^(O(n^2))}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, exact: true, output_sensitive: true}
history:
  year: 1985
  people: [Ulrich Fincke, Michael Pohst]
  note: Pohst described the method in 1981 and Fincke and Pohst gave its complexity analysis in Mathematics of Computation in 1985; it was rediscovered as sphere decoding in communications in the 1990s.
prereqs: [lattice, gram-schmidt-orthogonalization, closest-vector-problem]
see_also: [lattice-enumeration, schnorr-euchner-enumeration, kannan-enumeration, babai-nearest-plane, lll-algorithm, bkz-algorithm, gaussian-heuristic, shortest-vector-problem]
sources:
  - paper: "U. Fincke and M. Pohst, Improved methods for calculating vectors of short length in a lattice, including a complexity analysis, Mathematics of Computation 44(170) (1985)"
    locator: pages 463 to 471 (the enumeration algorithm with Cholesky data and its running time on LLL-reduced bases)
  - paper: "M. Pohst, On the computation of lattice vectors of minimal length, successive minima and reduced bases with applications, ACM SIGSAM Bulletin 15(1) (1981)"
    locator: the enumeration of short vectors by nested intervals
  - paper: "E. Agrell, T. Eriksson, A. Vardy and K. Zeger, Closest point search in lattices, IEEE Transactions on Information Theory 48(8) (2002)"
    locator: pages 2201 to 2214 (Pohst and Schnorr-Euchner enumeration as sphere decoding, with pseudocode and comparisons)
  - paper: "G. Hanrot and D. Stehlé, Improved analysis of Kannan's shortest lattice vector algorithm, CRYPTO 2007, LNCS 4622"
    locator: the bound on the number of enumeration nodes in terms of the Gram-Schmidt norms
---

Fincke-Pohst enumeration lists every vector of a [lattice](/lattice/) inside a ball of squared radius $R$ around a target $t$. It fixes the coefficients from the last to the first, and the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data, equivalently the Cholesky factor of the Gram matrix, turn the ball into one interval of allowed integers per coefficient. It solves the [closest vector problem](/closest-vector-problem/) and the [shortest vector problem](/shortest-vector-problem/) exactly. Its running time depends on the basis, so it runs after [LLL](/lll-algorithm/) or [BKZ](/bkz-algorithm/).

## In plain words

A grid of points is built from a few arrows, and you want every grid point inside a ball.

The grid is stacked in layers, and only a few layers cut through the ball. For each such layer, the ball cuts out a smaller ball inside the layer, and the layer is again stacked in thinner layers. Go down layer by layer, keeping only the layers that still meet what is left of the ball. When no layers are left to choose, you are at a grid point inside the ball.

Each layer comes with a budget: the part of the radius not yet used up by earlier choices. A choice that spends the whole budget early leaves nothing for later and is dropped right away. That cut is what makes the search finite and, on a tidy set of arrows, fast.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a matrix $B$, a target $t \in \mathbb{Q}^m$ (for SVP, $t = 0$) and a squared radius $R \ge 0$.

**Output.** Every $x \in \mathbb{Z}^n$ with $\|t - x B\|^2 \le R$.

For SVP, take $t = 0$ and $R = \|b_1\|^2$ and keep the shortest nonzero output; for CVP, take $R$ to be the squared distance of any known lattice vector, such as the output of [Babai's nearest plane method](/babai-nearest-plane/), and keep the closest output.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the Gram-Schmidt data with $N_i = \|b_i^*\|^2$, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the LLL parameter. Write $\tau_j = \langle t, b_j^* \rangle / N_j$ and $o$ for the component of $t$ orthogonal to the span. All arithmetic is exact, on rationals. Time counts arithmetic operations. The bounds in terms of the number of tree nodes and the Gram-Schmidt norms are proved; the node counts from the [Gaussian heuristic](/gaussian-heuristic/) are heuristic.

## The algorithm

The algorithm rests on one identity. For $x \in \mathbb{Z}^n$,

$$\|t - x B\|^2 = \|o\|^2 + \sum_{i=1}^n (x_i - c_i)^2 N_i, \qquad c_i = \tau_i - \sum_{j > i} x_j \mu_{ji}.$$

The term for $i$ depends only on $x_i, \ldots, x_n$. So once $x_{i+1}, \ldots, x_n$ are fixed with partial sum $\rho_{i+1}$, the allowed $x_i$ form the interval $|x_i - c_i| \le \sqrt{(R - \rho_{i+1}) / N_i}$.

```pseudo id=main
FINCKE-POHST(B, R, t)               ▷ every x in Zⁿ with ‖t − x B‖² ≤ R
L1  compute b_i*, N_i, μ_ij, τ_j = ⟨t, b_j*⟩ / N_j and ρ_{n+1} = ‖t‖² − Σ τ_j² N_j
L2  if ρ_{n+1} > R then return ∅
L3  i ← n; new ← true; S ← ∅
L4  while i ≤ n
L5      if new then c_i ← τ_i − Σ_{j>i} x_j μ_ji; x_i ← the least integer with ρ_{i+1} + (x_i − c_i)² N_i ≤ R, if any
L6      else x_i ← x_i + 1
L7      if there is no such x_i or ρ_{i+1} + (x_i − c_i)² N_i > R then i ← i + 1; new ← false; continue
L8      ρ_i ← ρ_{i+1} + (x_i − c_i)² N_i
L9      if i = 1 then add x to S; new ← false
L10     else i ← i − 1; new ← true
L11 return S
```

The loop is a depth-first search of a tree whose nodes at level $i$ are the tuples $(x_i, \ldots, x_n)$ with partial sum at most $R$. The implementation is iterative; the stack is the arrays $x$, $c$ and $\rho$.

## Example

The lattice with rows $b_1 = (2, 0)$, $b_2 = (1, 2)$, the target $t = (0.7, 2.3)$ of the [bounded distance decoding](/bounded-distance-decoding/) page, and $R = 3$. Here $b_1^* = (2, 0)$, $b_2^* = (0, 2)$, $N = (4, 4)$, $\mu_{21} = \tfrac12$, $\tau = (0.35, 1.15)$ and $\rho_3 = 0$.

| Step | Level | $c_i$ | Interval for $x_i$ | $x_i$ | $\rho_i$ | Action |
|------|------|------|------|------|------|------|
| L5 | 2 | $1.15$ | $\lvert x_2 - 1.15 \rvert \le 0.866$ | 1 | $0.09$ | descend |
| L5 | 1 | $0.35 - 0.5 = -0.15$ | $\lvert x_1 + 0.15 \rvert \le 0.853$ | $-1$ | $2.98$ | output $(-1, 1)$ |
| L6 | 1 | | | 0 | $0.18$ | output $(0, 1)$ |
| L6, L7 | 1 | | | 1 | $5.38 > 3$ | up |
| L6 | 2 | | | 2 | $2.89$ | descend |
| L5, L7 | 1 | $0.35 - 1 = -0.65$ | $\lvert x_1 + 0.65 \rvert \le 0.166$ | none | | up |
| L6, L7 | 2 | | | 3 | $13.69 > 3$ | up, done |

The output is $x = (-1, 1)$ and $x = (0, 1)$, the vectors $(-1, 2)$ at squared distance $2.98$ and $(1, 2)$ at squared distance $0.18$, so $(1, 2)$ is the closest vector. The tree has 4 nodes, below the bound $(2 \sqrt{3/4} + 1)^2 \approx 7.46$ on its bottom level. With $t = 0$ and $R = 4$ the output is $0$ and $\pm (2, 0)$, which shows $\lambda_1 = 2$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). By the identity above, the partial sums $\rho_n \le \rho_{n-1} \le \cdots \le \rho_1$ only grow, and $\rho_1 = \|t - x B\|^2$. So a tuple whose partial sum exceeds $R$ has no completion inside the ball, and cutting it loses nothing. For fixed later coordinates, the allowed values of $x_i$ form an interval of integers, which lines L5 to L7 scan from its smallest element up. By induction from level $n$ down, every tuple with partial sum at most $R$ is visited exactly once, so the output is exactly the set of $x$ with $\|t - x B\|^2 \le R$, listed in lexicographic order of $(x_n, \ldots, x_1)$.

## Complexity

- **Per node.** Computing $c_i$ takes $O(n)$ operations, and the other steps $O(1)$ plus one integer square root. The loop runs at most $2T + 1$ times for $T$ tree nodes, so the total is $O(n^2 m + n T)$ arithmetic operations, with $O(n^2 m)$ for Gram-Schmidt. Storing the $\mu_{ij}$ and the partial sums of $c_i$ brings the cost per node down to $O(1)$ amortized in the classical implementations.
- **The number of nodes, proved.** For fixed later coordinates, $x_i$ takes at most $2 \sqrt{R / N_i} + 1$ values, so the nodes of level $k$ number at most $\prod_{i \ge k} (2 \sqrt{R / N_i} + 1)$. This is small when the $N_i$ are large compared with $R$, which is what reduction achieves.
- **LLL preprocessing, proved.** For an LLL-reduced basis with $\delta = 3/4$ and $R = \|b_1\|^2$, $R / N_i \le 2^{i-1}$, and the bound becomes $2^{O(n^2)}$. Fincke and Pohst gave an analysis of this kind for LLL-reduced input in 1985.
- **Stronger preprocessing, proved.** With a quasi-HKZ basis, as in [Kannan's algorithm](/kannan-enumeration/), the cost becomes $n^{n/(2e) + o(n)}$ for SVP (Hanrot and Stehlé, 2007).
- **The number of nodes, heuristic.** By the Gaussian heuristic, the nodes of level $k$ number about $V_{n-k+1}(\sqrt R) / \prod_{i \ge k} \|b_i^*\|$, where $V_d(r)$ is the volume of a $d$-dimensional ball of radius $r$. For BKZ-reduced bases this predicts $2^{\Theta(n^2/\beta)}$ nodes for block size $\beta$, and the predictions match experiments.
- **Space.** $O(n m)$ numbers for the Gram-Schmidt data plus $O(n)$ for the search state. The output can be much larger: it has as many entries as there are lattice points in the ball.

## Properties

- **Exact.** It returns all solutions, not an approximation; it is output sensitive, since the cost is at least the number of points in the ball.
- **Deterministic.** The order of the output is fixed: lexicographic in $(x_n, \ldots, x_1)$.
- **Basis dependent cost, basis independent output.** Two bases of the same lattice give the same vectors in different coordinates, at very different costs.
- **Radius monotone.** A larger $R$ gives a superset of the output, and a larger tree.
- **Polynomial space.** Unlike sieving, it needs only polynomial space beyond the output.

## Variants and improvements

- **Schnorr-Euchner order.** [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) visits the values of $x_i$ in zigzag order around $c_i$, closest first, and shrinks $R$ whenever a shorter vector is found. For SVP and CVP this finds a good answer early and prunes more; it is the standard form in software and in sphere decoders.
- **Pruned enumeration.** Gama, Nguyen and Regev (2010) replace the radius $R$ at level $k$ by a smaller $R_k$, losing a controlled fraction of solutions but gaining an exponential speedup; with rerandomization this is extreme pruning, used inside [BKZ](/bkz-algorithm/) 2.0.
- **Kannan's algorithm.** [Kannan enumeration](/kannan-enumeration/) first reduces the basis so strongly, recursively, that the tree is only $n^{O(n)}$ nodes.
- **Sphere decoding.** In communications, the same search over a channel matrix finds the maximum-likelihood point for MIMO detection; Viterbo and Boutros popularized it in 1999.
- **Successive minima and short vectors.** Pohst's original aim was to compute all short vectors, the [successive minima](/successive-minima/) and reduced bases of algebraic number fields.

## When to use it

- To solve SVP or CVP exactly in moderate dimension, up to about 60 to 80 with reduction alone and higher with extreme pruning, when polynomial memory matters.
- To list all short vectors, for example to compute a kissing number, a theta series or all solutions of a quadratic form problem.
- As the SVP oracle inside BKZ for block sizes where it beats sieving.
- Not on an unreduced basis, and not in dimensions where sieving, with time $2^{0.292 n + o(n)}$ heuristically, is faster.

## Pitfalls

- **Skipping reduction.** The tree size depends on the smallest $N_i$; on a raw basis it is astronomically large.
- **Radius too large.** For CVP, start from a known upper bound such as Babai's distance, not from a guess.
- **Floating-point boundaries.** In floating point, a point exactly on the sphere may be dropped or a point just outside kept; use exact arithmetic or a small safety margin when every point matters.
- **Recursion depth.** A recursive implementation in dimension $n$ is fine for small $n$, but the iterative form avoids call overhead and depth limits.
- **Forgetting the orthogonal part.** When $t$ is outside the span, its orthogonal component adds $\|o\|^2$ to every distance; omit it and the interval bounds are wrong.

## Implementations

## History

Michael Pohst described enumeration with nested intervals in 1981, to compute short vectors and successive minima in algebraic number theory, and Ulrich Fincke and Pohst published the improved method with a complexity analysis in Mathematics of Computation in 1985, using LLL as preprocessing. Kannan's algorithm of 1983 had already shown that stronger preprocessing gives $n^{O(n)}$ time. Schnorr and Euchner introduced the zigzag order in 1994, and in the late 1990s the method reappeared as sphere decoding in digital communications. Gama, Nguyen and Regev's extreme pruning of 2010 made enumeration the method behind many SVP records.

## References
