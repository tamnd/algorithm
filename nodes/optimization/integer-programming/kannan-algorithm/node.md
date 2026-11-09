---
tag: 3NGX0Y
kind: algorithm
slug: kannan-algorithm
name: Kannan's algorithm
aliases:
- Kannan's shortest-vector enumeration for integer programming
- Kannan's integer programming algorithm
area: optimization/integer-programming
level: research
summary: Improves the fixed-dimension running time by enumerating short lattice vectors with a Lenstra-style search.
solves: [integer-programming-fixed-dimension, integer-feasibility]
model: word-ram
complexity:
  vars: {n: the number of variables, s: the size of the input in binary}
  time: {worst: n^(O(n)) s^(O(1))}
  space: {extra: s^(O(1))}
properties: {deterministic: true, recursive: true, exact: true}
prereqs: [lenstra-algorithm, dual-lattice, covering-radius, shortest-vector-problem, closest-vector-problem]
see_also: [lenstra-theorem, kannan-enumeration, fincke-pohst-enumeration, hkz-reduction, frank-tardos-algorithm, integer-programming-fixed-dimension]
sources:
  - paper: doi:10.1287/moor.12.3.415
    title: R. Kannan, Minkowski's convex body theorem and integer programming, Mathematics of Operations Research 12(3), 1987
    locator: pp. 415 to 440
  - paper: doi:10.1145/800061.808749
    title: R. Kannan, Improved algorithms for integer programming and related lattice problems, Proceedings of the 15th ACM Symposium on Theory of Computing, 1983
    locator: pp. 193 to 206 (enumeration of short vectors on a reduced basis)
  - paper: doi:10.1007/BF01445125
    title: W. Banaszczyk, New bounds in some transference theorems in the geometry of numbers, Mathematische Annalen 296, 1993
    locator: pp. 625 to 635 (the bound on the first minimum of the dual lattice times the covering radius)
  - paper: "F. Eisenbrand, Integer programming and algorithmic geometry of numbers, in 50 Years of Integer Programming 1958 to 2008, Springer, 2010"
    locator: sections on the flatness theorem and on Kannan's algorithm
---

Kannan's algorithm decides whether a polyhedron in $\mathbb{R}^n$ contains an integer point, and solves [integer programs in fixed dimension](/integer-programming-fixed-dimension/) in $n^{O(n)}$ times a polynomial in the input size. It has the same frame as [Lenstra's algorithm](/lenstra-algorithm/): make the polyhedron round, then find an integer point near the center or a thin direction. The difference is that it finds a shortest lattice vector exactly by enumeration instead of an approximate one by LLL, so the number of branches per level drops from exponential in $n$ to at most $n^3$. R. Kannan published it in 1983 and 1987.

## In plain words

Lenstra's method looks for a direction in which a shape is thin, but it accepts a direction that is only roughly the thinnest. Then it must try many parallel sheets of whole-number points. Kannan's method spends more work to find the exactly best direction and the exactly nearest whole-number point. With the best direction, few sheets cross the shape, so the search tree is much smaller.

The search for the best direction tries all short candidates in a careful order. That costs more than the rough method, but it pays off, because the saving is in the number of branches at every level of the recursion.

## The problem

The input is $A \in \mathbb{Q}^{m \times n}$ and $b \in \mathbb{Q}^m$ such that $P = \{x \in \mathbb{R}^n : A x \le b\}$ is bounded. The output is a point of $P \cap \mathbb{Z}^n$, or NONE if this set is empty. With a binary search on the objective, the same routine maximizes $c^\top x$ over $P \cap \mathbb{Z}^n$.

For a positive definite matrix $Q$ let $\|x\|_Q = \sqrt{x^\top Q x}$. The [dual lattice](/dual-lattice/) of $\mathbb{Z}^n$ in this norm is $\mathbb{Z}^n$ with the norm $\|\cdot\|_{Q^{-1}}$, and $|d^\top w| \le \|d\|_{Q^{-1}} \|w\|_Q$ for all $d, w$. The [covering radius](/covering-radius/) $\mu$ is the largest $Q$-distance from a point of $\mathbb{R}^n$ to $\mathbb{Z}^n$, and $\lambda_1^*$ is the $Q^{-1}$-length of a shortest nonzero integer vector. Banaszczyk's transference bound states $\lambda_1^* \, \mu \le n/2$.

## The algorithm

Lines L1 to L5 are the rounding step of [Lenstra's algorithm](/lenstra-algorithm/): the barycenter $c$ of a maximum-volume simplex $S$ in $P$, and the norm $Q$ in which $S$ is regular with edge 1.

```pseudo id=main
KANNAN(A, b)                               ▷ n is the number of columns of A
L1  if n = 0 then return () if 0 ≤ b, else NONE
L2  V ← the vertices of P;  if V = ∅ then return NONE
L3  if the affine hull of V is not ℝⁿ then d ← a primitive integer normal of it; δ ← dᵀv for v ∈ V; return NONE if δ ∉ ℤ, else SLICE(A, b, d, {δ})
L4  S ← a simplex of maximum volume with vertices in V;  c ← the barycenter of S
L5  Q ← the matrix that makes S a regular simplex of edge 1 in the norm ‖·‖_Q
L6  y ← an integer point that minimizes ‖y − c‖_Q            ▷ exact closest vector
L7  if y ∈ P then return y
L8  d ← a nonzero integer vector that minimizes ‖d‖_{Q⁻¹}    ▷ exact shortest dual vector
L9  return SLICE(A, b, d, {⌈min over v ∈ V of dᵀv⌉, …, ⌊max over v ∈ V of dᵀv⌋})

SLICE(A, b, d, K)
L10 W ← a unimodular matrix with dᵀW = e₁ᵀ;  for each k ∈ K: z ← KANNAN(A W without its first column, b − k · (A W)₁); if z ≠ NONE then return W (k, z)
L11 return NONE
```

Lines L6 and L8 solve the [closest vector problem](/closest-vector-problem/) and the [shortest vector problem](/shortest-vector-problem/) exactly. The code first reduces the basis with the [LLL algorithm](/lll-algorithm/), takes the point of [Babai's nearest plane](/babai-nearest-plane/) method (for L6) or the shortest basis vector (for L8) as the first candidate, and then runs [Fincke-Pohst enumeration](/fincke-pohst-enumeration/): it visits every coefficient vector whose partial sums of squares stay below the best value found so far. A shortest vector is primitive, so line L10 can use it as it is.

The page code branches on hyperplanes. Kannan's own algorithm uses a stronger reduction of the basis and can fix several coordinates at once, so that its subproblems are affine subspaces of any lower dimension, not only hyperplanes.

## Example

Use the strip $36/5 \le 3x_1 + 5x_2 \le 39/5$ with $x_1, x_2 \ge 0$ from the page on [Lenstra's algorithm](/lenstra-algorithm/). It has no integer point.

1. Lines L1 to L5 give the barycenter $c = (13/15, 1)$ and $Q = \begin{pmatrix} 3925/169 & 3125/78 \\ 3125/78 & 625/9 \end{pmatrix}$. Here $r^2 = 1/(2n(n+1)) = 1/12$.
2. Line L6 gives the closest integer point $y = (1, 1)$, with $\|y - c\|_Q^2 = 628/1521 > 1/12$. The point is not in $P$.
3. Line L8 computes $Q^{-1} = \begin{pmatrix} 676/75 & -26/5 \\ -26/5 & 1884/625 \end{pmatrix}$ and finds the shortest nonzero vector $d = (-1, -2)$ with $\|d\|_{Q^{-1}}^2 = 508/1875$. For comparison, the normal $(3, 5)$ of the strip has $\|(3,5)\|_{Q^{-1}}^2 = 12/25 = 900/1875$: the norm measures the width of the simplex $S$, not of $P$.
4. The values of $-x_1 - 2x_2$ at the vertices lie in $[-78/25, -12/5]$, so $K = \{-3\}$.
5. On the line $x_1 + 2x_2 = 3$, the call in dimension 1 sees an interval with no integer and returns NONE.

The answer is NONE, with one hyperplane at the first level. In this small case LLL already gives the same direction up to sign, so the search is the same as in Lenstra's algorithm; the two differ when $n$ grows and LLL is far from optimal.

## Correctness

**Theorem.** For every bounded rational polyhedron $P$, KANNAN returns an integer point of $P$ if one exists, and NONE otherwise. Each call in dimension $n$ that reaches line L9 has $|K| \le n^3$.

Correctness is the same as for Lenstra's algorithm: line L7 returns only points of $P \cap \mathbb{Z}^n$, and lines L3, L9 and L10 cover every integer point of $P$ by the hyperplanes $d^\top x = k$, $k \in K$. For the bound, let $r = 1/\sqrt{2n(n+1)}$. The ball $B_Q(c, r)$ lies in $P$, and $P$ lies in $B_Q(c, n^2 r)$. If line L9 runs, then $y \notin P$, so the $Q$-distance from $c$ to $\mathbb{Z}^n$ is more than $r$, and $\mu > r$. Banaszczyk's bound gives $\|d\|_{Q^{-1}} = \lambda_1^* \le n/(2\mu) < n/(2r)$. For $p, p' \in P$,
$$|d^\top (p - p')| \le \|d\|_{Q^{-1}} \, \|p - p'\|_Q < \frac{n}{2r} \cdot 2 n^2 r = n^3,$$
so $K$ has at most $n^3$ elements. The full proof is in the proof file.

## Complexity

The recursion has depth $n$, and a call in dimension $k$ makes at most $k^3$ calls in dimension $k - 1$. So the tree has at most $\prod_{k=1}^n k^3 = (n!)^3 = n^{O(n)}$ leaves, compared with $2^{O(n^2)}$ for Lenstra's algorithm.

The work in a node is dominated by the two enumerations. Kannan's enumeration on a suitably reduced basis visits $n^{O(n)}$ points (see [Kannan enumeration](/kannan-enumeration/)), and the bit sizes of the numbers stay polynomial in the input size for fixed $n$. This gives the total of $n^{O(n)} s^{O(1)}$. The page code uses an LLL-reduced basis for the enumeration, which is simpler; its known worst-case bound is $2^{O(n^2)}$ points per enumeration, so the code does not reach Kannan's bound. The vertex and simplex steps of the code are polynomial only for fixed $n$, as on the Lenstra page.

## Properties

- **Exact.** All arithmetic is rational, and NONE is a proof that $P$ has no integer point.
- **Few branches.** At most $n^3$ hyperplanes per level, against $n^2 2^{n/2} + 1$ for the LLL version.
- **Polynomial in fixed dimension.** For each fixed $n$, the time is polynomial in the input size, which reproves [Lenstra's theorem](/lenstra-theorem/) with a better dependence on $n$.
- **Deterministic.** Both enumerations are deterministic.

## Variants and improvements

- **Lenstra's algorithm.** The [LLL version](/lenstra-algorithm/) replaces the exact shortest vector by an LLL vector, which is cheaper per node but gives $2^{O(n^2)}$ branches per level.
- **Small numbers.** The [Frank-Tardos algorithm](/frank-tardos-algorithm/) replaces the objective by an equivalent integer vector of polynomially bounded size, which keeps the numbers in the recursion small.
- **Better bounds on n.** Dadush gave an algorithm with time $2^{O(n)} n^n$, and Reis and Rothvoss a randomized algorithm with time $(\log 2n)^{O(n)}$, using a better flatness bound.
- **Enumeration with pruning.** Practical codes use [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) in lines L6 and L8, which visits the candidates in order of increasing distance.

## When to use it

Use it when the number of variables is small, the coefficients are large, and a proof of the result is needed, so that [branch and bound](/land-doig-algorithm/) on single variables is too slow. The exact enumerations cost more per node than LLL, so for very small $n$ the [LLL version](/lenstra-algorithm/) is often enough. For models with many variables, [branch and cut](/branch-and-cut/) is the practical choice.

## Pitfalls

- **The direction must be shortest in the dual norm.** The width of the ellipsoid in the direction $d$ is $2R \|d\|_{Q^{-1}}$, so the norm is $Q^{-1}$, not $Q$.
- **The closest point must be exact for the bound.** If line L6 returns an approximate point that is outside $P$, the distance from $c$ to the lattice can still be small, and the bound $\mu > r$ fails. The algorithm stays correct, but $|K|$ can be larger.
- **Zero vector.** The shortest vector search must exclude $0$.
- **Floating point.** Enumeration with rounded numbers can miss the minimum, or accept a vector that is not shortest. The code uses `fractions.Fraction`.

## Implementations

The Python code is exact and uses only the standard library. The function `closest_point` does the enumeration for both lines L6 and L8, with the option `nonzero=True` for the shortest vector; it keeps the best value found so far as the radius and stops a branch when the partial sum of squares exceeds it. The function `kannan_maximize` adds a box and does the binary search on the objective. The tests compare the optimum with brute force over the box, check the closest and shortest vectors against brute force over a ball that contains all candidates, and check that every branching level has at most $n^3$ hyperplanes.

## History

Kannan presented the algorithm at STOC 1983 and published the full version in Mathematics of Operations Research in 1987. It improved the $2^{O(n^3)}$ dependence of [Lenstra's algorithm](/lenstra-algorithm/) to $n^{O(n)}$, and its enumeration routine became a standard tool for the shortest vector problem. Banaszczyk's transference bound of 1993 later gave the simple $n^3$ count of hyperplanes used above.

## References
