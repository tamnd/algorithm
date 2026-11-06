---
tag: ARHDFM
kind: algorithm
slug: schnorr-euchner-enumeration
name: Schnorr-Euchner enumeration
aliases:
- Schnorr-Euchner algorithm
- Schnorr-Euchner zig-zag enumeration
area: number-theory/lattice-reduction
level: advanced
summary: Fincke-Pohst enumeration with a zig-zag order and an improved radius update.
solves: [shortest-vector-problem, closest-vector-problem]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the basis vectors, N: the number of nodes of the enumeration tree that the search visits, X: the largest squared length of an input vector of an integer basis, M: the cost M(k) of multiplying two integers of k binary digits}
  time: {worst: O(n^2 m + n N), best: O(n^2 m)}
  space: {extra: O(n^2 + n m)}
  bit_operations: {worst: O((n^2 m + n N) M(n^2 log X))}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1994
  people: [Claus Peter Schnorr, Martin Euchner]
  note: Published in Mathematical Programming as the enumeration step of their practical block reduction; it refines the enumeration of Pohst and of Fincke and Pohst.
prereqs: [lattice-enumeration, gram-schmidt-orthogonalization, shortest-vector-problem]
see_also: [fincke-pohst-enumeration, kannan-enumeration, bkz-algorithm, lll-algorithm, babai-nearest-plane, closest-vector-problem, lattice-sieving, root-hermite-factor]
sources:
  - paper: "C. P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66, 1994"
    locator: pages 181 to 199 (the enumeration procedure ENUM with the zig-zag order of the coordinates and the radius that shrinks to each new short vector)
  - paper: "U. Fincke and M. Pohst, Improved methods for calculating vectors of short length in a lattice, including a complexity analysis, Mathematics of Computation 44 (1985)"
    locator: pages 463 to 471 (the enumeration with intervals for one coordinate at a time, which Schnorr and Euchner reorder)
  - paper: "G. Hanrot and D. Stehlé, Improved analysis of Kannan's shortest lattice vector algorithm, Advances in Cryptology, CRYPTO 2007, LNCS 4622"
    locator: the bound n^(n/(2e) + o(n)) on the number of enumeration nodes for a quasi-HKZ-reduced basis
  - paper: "N. Gama, P. Q. Nguyen and O. Regev, Lattice enumeration using extreme pruning, Advances in Cryptology, Eurocrypt 2010, LNCS 6110"
    locator: the cost of the enumeration tree under the Gaussian heuristic, and pruned enumeration
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 18.5, Enumeration of all short lattice points
---

Schnorr-Euchner enumeration finds a shortest nonzero vector of a lattice, or a lattice vector closest to a target, by a depth-first search over the coordinates of the vector in a basis. It is [lattice enumeration](/lattice-enumeration/) with two choices that make it fast in practice: at each level the coordinate is tried in zig-zag order around its center, nearest first, and each time a shorter vector is found the search radius shrinks to its length. It needs only polynomial space, it is exact, and it is the standard SVP subroutine of [BKZ](/bkz-algorithm/); its running time is exponential in the rank and depends heavily on how well the input basis is reduced.

## In plain words

Pick the coordinates of the vector one at a time, starting with the last basis vector. Once some coordinates are fixed, the part of the vector they decide is already known, and its length is a lower bound for every way of finishing. If the bound is too large, give up on that choice and go back one step.

At each step there is a best value for the next coordinate, the one that keeps the known part shortest. The search tries that value first, then its neighbours on alternating sides, moving outward. So good candidates are met early. The first full vector found sets a bound, every later one must beat it, and the bound only gets tighter, which cuts away more and more of the search.

## The problem

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a lattice $L$ of rank $n$, Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij}$ with $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$, $B_i = \|b_i^*\|^2$, and first minimum $\lambda_1$. We write $\lceil c \rfloor = \lfloor c + 1/2 \rfloor$ for the nearest integer.

**SVP.** Given the basis, find integers $x_1, \ldots, x_n$, not all zero, minimizing $\|\sum_i x_i b_i\|$. The value is $\lambda_1$; see the [shortest vector problem](/shortest-vector-problem/).

**CVP.** Given also a target $t \in \mathbb{Q}^m$, find integers $x_i$ minimizing $\|t - \sum_i x_i b_i\|$; see the [closest vector problem](/closest-vector-problem/).

Both rest on one identity. Writing $v = \sum_i x_i b_i$ in the Gram-Schmidt basis gives $v = \sum_k (x_k - c_k) b_k^*$ with centers $c_k = -\sum_{j > k} x_j \mu_{jk}$, so

$$\|v\|^2 = \sum_{k=1}^n (x_k - c_k)^2 B_k, \qquad \ell_k := \sum_{i \ge k} (x_i - c_i)^2 B_i = \|\pi_k(v)\|^2,$$

where $\pi_k$ is the projection orthogonal to $b_1, \ldots, b_{k-1}$. The partial norm $\ell_k$ depends only on $x_k, \ldots, x_n$, and $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_n$. For CVP, $t = t_\perp + \sum_k \tau_k b_k^*$ with $\tau_k = \langle t, b_k^* \rangle / B_k$ and $t_\perp$ orthogonal to the span, and the same holds with $c_k = \tau_k - \sum_{j > k} x_j \mu_{jk}$ and an extra constant $\|t_\perp\|^2$.

## The algorithm

```pseudo id=main
SCHNORR-EUCHNER(b_1..b_n)                  ▷ a shortest nonzero vector; a loop, not recursion
L1  compute μ_ij and B_i = ‖b_i*‖² exactly
L2  R² ← B_1; best ← (1, 0, ..., 0)          ▷ b_1 is the first candidate
L3  k ← n; ℓ_n+1 ← 0; c_n ← 0; x_n ← 0
L4  loop
L5      ℓ_k ← ℓ_k+1 + (x_k − c_k)² · B_k
L6      if ℓ_k < R² and k > 1 then
L7          k ← k − 1; c_k ← −Σ_{j>k} x_j μ_jk; x_k ← ⌈c_k⌋; continue at L5     ▷ go down
L8      else if ℓ_k < R² then                                ▷ a leaf: k = 1
L9          if x ≠ 0 then R² ← ℓ_1; best ← x                  ▷ shrink the radius
L10     else k ← k + 1                                        ▷ go up
L11         if k > n then return best and R²
L12     x_k ← NEXT(x_k)            ▷ zig-zag around c_k; only x_k + 1 while x_k+1..x_n are all 0
```

**The zig-zag order.** At level $k$ the values are tried in order of nondecreasing distance from the center $c_k$: first $\lceil c_k \rfloor$, then the nearer of its two neighbours, then the other one, and so on outward,

$$\lceil c_k \rfloor, \ \lceil c_k \rfloor + s, \ \lceil c_k \rfloor - s, \ \lceil c_k \rfloor + 2 s, \ \lceil c_k \rfloor - 2 s, \ \ldots, \qquad s = \begin{cases} +1 & c_k \ge \lceil c_k \rfloor, \\ -1 & \text{otherwise.} \end{cases}$$

Since $\ell_k$ grows with $|x_k - c_k|$, once one value fails the test of line L6 or L8, every later value fails too, so going up at line L10 loses nothing. This is the property that the hole ORDER of [lattice enumeration](/lattice-enumeration/) requires.

**Symmetry.** $v$ and $-v$ have the same length. While $x_{k+1} = \cdots = x_n = 0$ the center is $c_k = 0$, and line L12 tries only $x_k = 0, 1, 2, \ldots$; so every pair $\pm v$ is met once, with a positive last nonzero coordinate. The zero vector is the leaf where all $x_k = 0$, and line L9 skips it.

**The radius.** Line L2 starts with $R^2 = \|b_1\|^2$, which is at least $\lambda_1^2$. The tests are strict, so the search only accepts vectors strictly shorter than the best one so far, and line L9 lowers $R^2$ to each one it accepts.

**CVP.** For a target $t$, use the centers $c_k = \tau_k - \sum_{j > k} x_j \mu_{jk}$, drop the symmetry rule and the test $x \ne 0$, and start from the vector of [Babai's nearest plane](/babai-nearest-plane/) method, with $R^2$ its squared distance to $t_\perp$ removed. The implementation does this.

## Example

Take the basis $b_1 = (1, 1, 1)$, $b_2 = (-1, 0, 2)$, $b_3 = (3, 5, 6)$, with $\det(L) = 3$. Its Gram-Schmidt data are

$$B_1 = 3, \quad B_2 = \tfrac{14}{3}, \quad B_3 = \tfrac{9}{14}, \qquad \mu_{21} = \tfrac13, \quad \mu_{31} = \tfrac{14}{3}, \quad \mu_{32} = \tfrac{13}{14}.$$

The search starts with $R^2 = B_1 = 3$. Each row is one execution of line L5; coordinates are written $(x_1, x_2, x_3)$.

| node | level $k$ | $x$ | $c_k$ | $\ell_k$ | action |
|---|---|---|---|---|---|
| 1 | 3 | $(\cdot, \cdot, 0)$ | $0$ | $0$ | down |
| 2 | 2 | $(\cdot, 0, 0)$ | $0$ | $0$ | down |
| 3 | 1 | $(0, 0, 0)$ | $0$ | $0$ | zero vector, skipped; $x_1 \to 1$ |
| 4 | 1 | $(1, 0, 0)$ | $0$ | $3$ | fails ($3 \not< 3$); up, $x_2 \to 1$ |
| 5 | 2 | $(\cdot, 1, 0)$ | $0$ | $14/3$ | fails; up, $x_3 \to 1$ |
| 6 | 3 | $(\cdot, \cdot, 1)$ | $0$ | $9/14$ | down |
| 7 | 2 | $(\cdot, -1, 1)$ | $-13/14$ | $2/3$ | down |
| 8 | 1 | $(-4, -1, 1)$ | $-13/3$ | $1$ | found; $R^2 \to 1$ |
| 9 | 1 | $(-5, -1, 1)$ | $-13/3$ | $2$ | fails; up, $x_2 \to 0$ |
| 10 | 2 | $(\cdot, 0, 1)$ | $-13/14$ | $14/3$ | fails; up, $x_3 \to 2$ |
| 11 | 3 | $(\cdot, \cdot, 2)$ | $0$ | $18/7$ | fails; $k = 4 > n$, return |

At node 7 the center $c_2 = -13/14$ rounds to $-1$, and $\ell_2 = 9/14 + (1/14)^2 \cdot 14/3 = 2/3$. At node 8, $c_1 = -(-1 \cdot \tfrac13 + 1 \cdot \tfrac{14}{3}) = -13/3$ rounds to $-4$, and $\ell_1 = 2/3 + (1/3)^2 \cdot 3 = 1$. The answer is $-4 b_1 - b_2 + b_3 = (0, 1, 0)$, of squared length $1 = \lambda_1^2$, after 11 nodes. Node 9 shows the zig-zag: $c_1 = -4.33$ lies below $-4$, so the next value tried is $-5$, which already fails against the new radius 1, and the level is closed after two values.

## Correctness

The output is a pair $(x, R^2)$ with $x \ne 0$ and $\|\sum_i x_i b_i\|^2 = R^2$; this holds at the start ($x = e_1$, $R^2 = B_1$) and is kept by line L9, because $\ell_1$ is the squared length of the vector by the identity above. Suppose some nonzero $u = \sum_i y_i b_i$ had $\|u\|^2$ below the final $R^2$; replace $u$ by $-u$ if needed so that its last nonzero coordinate is positive. Every partial norm $\ell_k(y)$ is at most $\|u\|^2$, so below every value that $R^2$ takes. At each level the values are tried in order of nondecreasing $\ell_k$, and the level is left only after a value fails; that value has $\ell_k \ge R^2 > \ell_k(y)$, so $y_k$ was tried before it and passed. By induction from level $n$ down, the search reaches the leaf $y$, where line L9 sets $R^2 \le \|u\|^2$: a contradiction. The search terminates because every level stops after finitely many values ($B_k > 0$, so $\ell_k \to \infty$ as $|x_k| \to \infty$) and the depth is $n$. The full proofs, also for CVP, are in [the correctness proof](proofs/correctness.md).

## Complexity

**Cost model.** The analysis counts arithmetic operations on exact rationals, for an input of $n$ linearly independent rows in $\mathbb{Q}^m$ (or $\mathbb{Z}^m$ with squared lengths at most $X$ for the bit bounds); $N$ is the number of times line L5 runs, the nodes of the search tree.

- **Operations.** Gram-Schmidt costs $O(n^2 m)$. Each node costs $O(1)$ at line L5 and $O(n)$ for the center at line L7, so the search costs $O(n N)$ and the total is $O(n^2 m + n N)$. Every run visits at least $2n$ nodes: the zero path passes at all $n$ levels, and every level must then fail once. An orthogonal basis with $b_1$ shortest reaches $N = 2n$, for a total of $O(n^2 m)$.
- **Bits (proved).** For an integer basis the Gram-Schmidt data have numerators and denominators of $O(n \log X)$ digits, and every $\ell_k$ is a rational with denominator dividing $\prod_i d_i d_{i-1}$, where $d_i$ is the Gram determinant of $b_1, \ldots, b_i$; so all numbers have $O(n^2 \log X)$ digits, and each operation costs $O(M(n^2 \log X))$.
- **The number of nodes (proved).** The radius never exceeds $\|b_1\|$, so every node is either a node of the tree of radius $\|b_1\|$ or the first failing child of one; this gives
$$N \le 1 + 2 \sum_{k=1}^n \prod_{i=k}^n \Big( 2 \sqrt{B_1 / B_i} + 1 \Big).$$
For a $\delta$-[LLL-reduced](/lll-reduction/) input, $B_1 / B_i \le \alpha^{i-1}$ with $\alpha = 1 / (\delta - 1/4)$, so $N \le 1 + 2 n \, 3^n \alpha^{n (n-1)/4} = 2^{O(n^2)}$. For a quasi-HKZ-reduced input, Hanrot and Stehlé proved $N \le n^{n/(2e) + o(n)}$, which is the basis of [Kannan's algorithm](/kannan-enumeration/).
- **Heuristic and observed.** Under the Gaussian heuristic and the geometric series assumption, the tree for a basis with [root Hermite factor](/root-hermite-factor/) $\delta_0$ has about $\delta_0^{n^2/4} 2^{O(n)}$ nodes; this is why enumeration is run on a BKZ-reduced basis. The shrinking radius and the zig-zag order make the search much faster than plain Fincke-Pohst in practice, but no proved bound shows a gain beyond the factor of the radius $\lambda_1$ instead of $\|b_1\|$.
- **Space.** $O(n^2)$ for $\mu$ and $O(n)$ for the search state, plus $O(nm)$ for the basis; no list of vectors is stored.

## Properties

- **Exact and deterministic.** With rational arithmetic the output is a shortest vector, and the same input gives the same output.
- **Polynomial space.** Unlike [sieving](/lattice-sieving/), it stores only the current path.
- **Anytime.** The best vector so far is always available, and it only improves; stopping early gives an approximate answer.
- **Depends on the basis.** The answer is a property of the lattice, but $N$ depends strongly on the basis: the example above takes 11 nodes, and its [LLL](/lll-algorithm/) form $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$ takes 6. The 4-dimensional basis $(1, 2, 3, 4), (2, 5, 7, 9), (3, 7, 11, 14), (4, 9, 14, 20)$ of the [lattice enumeration](/lattice-enumeration/) page takes 25 nodes, starting from $R^2 = 30$, and its LLL form takes 8.

## Variants and improvements

- **[Fincke-Pohst enumeration](/fincke-pohst-enumeration/).** The same tree with the values of $x_k$ in increasing order over an interval and a fixed radius; Schnorr-Euchner reorders it and shrinks the radius.
- **Pruned enumeration.** Replace $R^2$ at level $k$ by a smaller bound $R_k^2$; the search may then miss the answer, with a probability that can be estimated under the Gaussian heuristic. Extreme pruning (Gama, Nguyen and Regev) uses very small bounds and repeats on many randomized bases, for an exponential speedup in practice.
- **Inside BKZ.** [BKZ](/bkz-algorithm/) calls the enumeration on projected blocks $\pi_k(b_k), \ldots, \pi_k(b_{k+\beta-1})$ to find a shortest vector of each block.
- **[Kannan's algorithm](/kannan-enumeration/).** Preprocesses the basis to quasi-HKZ form recursively before enumerating, for the proved bound $n^{n/(2e) + o(n)}$.
- **Floating point.** Libraries such as fplll use floating-point $\mu$ and $B$, with error analyses that bound the precision needed; the exact version here is for small dimension and for testing.
- **CVP and sphere decoding.** The same search with a target, as above, is the sphere decoder of communication theory.

## When to use it

Use it when an exact shortest or closest vector is needed in moderate dimension, after reducing the basis with [LLL](/lll-algorithm/) or BKZ, or as the SVP oracle inside BKZ. In high dimension, sieving algorithms are faster in recent experiments, at the price of exponential memory; for an approximate answer in polynomial time, use LLL or [Babai's nearest plane](/babai-nearest-plane/) method.

## Pitfalls

- **An unreduced basis.** The search is correct for any basis, but $N$ can be huge; reduce the basis first.
- **The zero vector.** For SVP the leaf $x = 0$ has $\ell_1 = 0$ and must be skipped, or the search returns it.
- **Strict versus non-strict tests.** With $\ell_k < R^2$ the search returns one shortest vector; with $\ell_k \le R^2$ and a fixed radius it lists all vectors of length at most $R$, a different task.
- **Symmetry applied too low.** Only the levels where all higher coordinates are 0 may skip negative values; elsewhere $c_k \ne 0$ and both sides are needed.
- **The starting side of the zig-zag.** The second value must be the neighbour on the side of $c_k$; starting on the wrong side breaks the nondecreasing order, and then going up after a failure can miss vectors.
- **Floating-point centers.** Rounding errors in $c_k$ can make the search try values in the wrong order or cut a branch that should stay; use exact arithmetic or a proved precision.
- **Recursion.** A recursive version is natural but needs depth $n$; the loop form above uses $O(n)$ explicit state.

## Implementations

## History

Pohst (1981) and Kannan (1983) introduced the enumeration of short lattice vectors by a search over the Gram-Schmidt coordinates, and Fincke and Pohst (1985) gave the version with one interval per coordinate and its analysis. Schnorr and Euchner (1994) described the zig-zag order and the shrinking radius as the enumeration step of their practical block reduction, the algorithm now called BKZ, and used it to solve subset sum instances. Hanrot and Stehlé (2007) proved the bound $n^{n/(2e) + o(n)}$ for Kannan's preprocessing, and Gama, Nguyen and Regev (2010) introduced extreme pruning, which made enumeration practical in higher dimensions.

## References
