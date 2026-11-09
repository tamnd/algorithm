---
tag: RQXSN0
kind: algorithm
slug: lenstra-algorithm
name: Lenstra's algorithm
aliases:
- Lenstra's integer programming algorithm
- Lenstra's flatness algorithm
area: optimization/integer-programming
level: advanced
summary: Solves integer programs in fixed dimension using lattice basis reduction and rounding.
solves: [integer-programming-fixed-dimension, integer-feasibility]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of constraints, s: the size of the input in binary}
  time: {worst: 2^(O(n^3)) s^(O(1))}
  space: {extra: 2^(O(n^3)) s^(O(1))}
properties: {deterministic: true, recursive: true, exact: true}
prereqs: [lll-algorithm, lattice, babai-nearest-plane, polyhedron, integer-feasibility]
see_also: [lenstra-theorem, kannan-algorithm, frank-tardos-algorithm, integer-programming-fixed-dimension, megiddo-fixed-dimension-lp, unimodular-matrix, land-doig-algorithm, minimum-volume-enclosing-ellipsoid]
sources:
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: pp. 538 to 548
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: pp. 515 to 534 (the reduced basis and its properties)
  - paper: doi:10.1007/BF02579403
    title: L. Babai, On Lovász' lattice reduction and the nearest lattice point problem, Combinatorica 6(1), 1986
    locator: pp. 1 to 13 (nearest plane bound)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 18 (the complexity of integer linear programming, Lenstra's algorithm)
  - paper: "F. Eisenbrand, Integer programming and algorithmic geometry of numbers, in 50 Years of Integer Programming 1958 to 2008, Springer, 2010"
    locator: sections on the flatness theorem and Lenstra's algorithm
  - paper: doi:10.1007/s10107-024-02084-1
    title: D. Dadush, F. Eisenbrand and T. Rothvoss, From approximate to exact integer programming, Mathematical Programming, 2024
    locator: introduction (history of running times)
---

Lenstra's algorithm decides whether a polyhedron in $\mathbb{R}^n$ contains an integer point, and with a binary search on the objective it solves [integer programs](/integer-programming-fixed-dimension/). It makes the polyhedron round by a linear map, finds a short vector of the integer [lattice](/lattice/) with the [LLL algorithm](/lll-algorithm/), and then either finds an integer point near the center, or finds a direction in which the polyhedron is thin. In the thin case it recurses on the few hyperplanes of that direction that contain integer points. H. W. Lenstra Jr. published it in 1983; for each fixed $n$ it runs in polynomial time, which is [Lenstra's theorem](/lenstra-theorem/).

## In plain words

Picture a flat plate in space. If the plate is fat in every direction, it must contain a point with whole-number coordinates, because such points are spread evenly. If it does not contain one, it must be thin in some direction, like a sheet of paper. Then the whole-number points that matter lie on a few parallel sheets, and each sheet is a problem with one fewer dimension.

The algorithm first stretches the shape so that it looks round. Then it uses a lattice method to find either a whole-number point near the center or the thin direction. In the thin case it solves the smaller problem on each sheet. The number of sheets depends only on the dimension, so for a fixed dimension the total work stays small.

## The problem

The input is a matrix $A \in \mathbb{Q}^{m \times n}$ and a vector $b \in \mathbb{Q}^m$ such that $P = \{x \in \mathbb{R}^n : A x \le b\}$ is bounded. The output is a point of $P \cap \mathbb{Z}^n$, or NONE when this set is empty. The optimization version asks for $\max\{c^\top x : x \in P \cap \mathbb{Z}^n\}$ with $c \in \mathbb{Z}^n$. A bounded $P$ is the case of the code; the general case reduces to it, because a polyhedron with an integer point has one whose size is polynomial in the input size (Schrijver, Chapter 17), so a large box can be added.

The algorithm uses three facts about lattices. Let $Q$ be a positive definite rational matrix and $\|x\|_Q = \sqrt{x^\top Q x}$.

- An [LLL-reduced basis](/lll-reduction/) $b_1, \dots, b_n$ of $\mathbb{Z}^n$ in the norm $\|\cdot\|_Q$ has [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors with $\|b_i^*\|_Q^2 \le 2^{n-i} \|b_n^*\|_Q^2$.
- [Babai's nearest plane](/babai-nearest-plane/) method finds $y \in \mathbb{Z}^n$ with $\|y - c\|_Q^2 \le \frac{1}{4} \sum_i \|b_i^*\|_Q^2$.
- If $B$ is the matrix with columns $b_1, \dots, b_n$ and $d^\top$ is the last row of $B^{-1}$, then $d \in \mathbb{Z}^n$ and $|d^\top w| \le \|w\|_Q / \|b_n^*\|_Q$ for each $w \in \mathbb{R}^n$.

## The algorithm

This version uses a simplex of maximum volume to make $P$ round. Lenstra's paper uses a different rounding step with the same purpose.

```pseudo id=main
LENSTRA(A, b)                              ▷ n is the number of columns of A
L1  if n = 0 then return () if 0 ≤ b, else NONE
L2  V ← the vertices of P;  if V = ∅ then return NONE
L3  if the affine hull of V is not ℝⁿ then d ← a primitive integer normal of it; δ ← dᵀv for v ∈ V; return NONE if δ ∉ ℤ, else SLICE(A, b, d, {δ})
L4  S ← a simplex of maximum volume with vertices in V;  c ← the barycenter of S
L5  Q ← the matrix that makes S a regular simplex of edge 1 in the norm ‖·‖_Q
L6  b₁, …, bₙ ← an LLL-reduced basis of ℤⁿ in the norm ‖·‖_Q
L7  y ← the nearest plane point of ℤⁿ for c
L8  if y ∈ P then return y
L9  d ← the last row of B⁻¹, where B has the columns b₁, …, bₙ
L10 return SLICE(A, b, d, {⌈min over v ∈ V of dᵀv⌉, …, ⌊max over v ∈ V of dᵀv⌋})

SLICE(A, b, d, K)
L11 W ← a unimodular matrix with dᵀW = e₁ᵀ;  for each k ∈ K: z ← LENSTRA(A W without its first column, b − k · (A W)₁); if z ≠ NONE then return W (k, z)
L12 return NONE
```

Line L5 is explicit. If $S$ has the vertices $v_0, \dots, v_n$, let $T = [v_1 - v_0, \dots, v_n - v_0]^{-1}$ and let $G$ be the matrix with $G_{ii} = 1$ and $G_{ij} = 1/2$ for $i \ne j$. Then $Q = T^\top G T$. In the norm of $G$ the standard simplex with vertices $0, e_1, \dots, e_n$ has all edges of length 1. In line L11 the substitution $x = W z$ maps $\mathbb{Z}^{n-1}$ onto the integer points of the hyperplane $d^\top x = k$, because $W$ is [unimodular](/unimodular-matrix/) and $d^\top W z = z_1$. The matrix $W$ comes from the [extended Euclidean algorithm](/extended-euclidean-algorithm/) applied to the entries of $d$, which have greatest common divisor 1.

For optimization, find one point $x$, then do a binary search on $t$ between $c^\top x$ and $\lfloor \max_{v \in V} c^\top v \rfloor$, with the extra constraint $c^\top x \ge t$. This adds a factor that is linear in the input size.

## Example

Let $P$ be the strip $36/5 \le 3x_1 + 5x_2 \le 39/5$ with $x_1, x_2 \ge 0$. It has no integer point, because $3x_1 + 5x_2$ is an integer at each integer point.

1. The vertices are $(0, 36/25)$, $(0, 39/25)$, $(12/5, 0)$ and $(13/5, 0)$. The flat test of line L3 fails, since $P$ has area.
2. Of the four triangles, two have the largest doubled area $39/125$. The first one in the order of the code has the vertices $(0, 36/25)$, $(0, 39/25)$ and $(13/5, 0)$, with barycenter $c = (13/15, 1)$.
3. Line L5 gives $Q = \begin{pmatrix} 3925/169 & 3125/78 \\ 3125/78 & 625/9 \end{pmatrix}$, and line L6 gives the reduced basis $b_1 = (-2, 1)$, $b_2 = (-5, 3)$.
4. The nearest plane point is $y = (1, 1)$, with $3 + 5 = 8 > 39/5$, so $y \notin P$.
5. $B = \begin{pmatrix} -2 & -5 \\ 1 & 3 \end{pmatrix}$ has the inverse $\begin{pmatrix} -3 & -5 \\ 1 & 2 \end{pmatrix}$, so $d = (1, 2)$. At the four vertices, $x_1 + 2x_2$ takes the values $72/25$, $78/25$, $12/5$ and $13/5$. Only $k = 3$ lies in the range.
6. On the line $x_1 + 2x_2 = 3$, the points of $P$ have $6/5 \le x_2 \le 3/2$. The recursive call in dimension 1 finds no integer in this interval and returns NONE.

So the answer is NONE after two levels with one hyperplane each. The direction $(3, 5)$ would show the emptiness with zero hyperplanes; the algorithm does not need the best direction, only one in which $P$ is thin enough. For the strip $30 \le 5x_1 + 8x_2 \le 61/2$ with $0 \le x_1 \le 10$ and $x_2 \ge 0$, the direction found is $d = (-5, -8)$, the only hyperplane is $-5x_1 - 8x_2 = -30$, and the call in dimension 1 returns the point $(6, 0)$.

## Correctness

**Theorem.** For every bounded rational polyhedron $P$, LENSTRA returns an integer point of $P$ if one exists, and NONE otherwise. At each call in dimension $n$ that reaches line L10, the set $K$ has at most $n^2 2^{n/2} + 1$ elements.

The full proof is below. Line L3 is safe because every integer point of $P$ satisfies $d^\top x = \delta$. Lines L10 and L11 are safe because every integer point $x$ has $d^\top x \in \mathbb{Z}$, so it lies on one of the hyperplanes $d^\top x = k$ with $k \in K$, and the substitution $x = W z$ is a bijection between $\mathbb{Z}^{n-1}$ and the integer points of each hyperplane. The bound on $|K|$ follows from three inclusions: the ball of radius $r = 1/\sqrt{2n(n+1)}$ around $c$ lies in $S \subseteq P$, the polytope $P$ lies in the ball of radius $n^2 r$ (by the maximality of the volume of $S$), and if $y \notin P$ then $\|y - c\|_Q > r$, so $\|b_n^*\|_Q > 2r / 2^{n/2}$, and the width of $P$ in the direction $d$ is less than $n^2 2^{n/2}$.

## Complexity

The recursion has depth $n$, and a call in dimension $k$ makes at most $k^2 2^{k/2} + 1$ recursive calls. So the tree has at most $\prod_{k=1}^{n} (k^2 2^{k/2} + 1) = 2^{O(n^2)}$ nodes, a number that depends only on $n$. In each node, the code enumerates the vertices with $\binom{m}{n}$ linear systems and the simplex with at most $\binom{|V|}{n+1}$ determinants, and LLL and the nearest plane step take a number of arithmetic operations polynomial in $n$ and in the size of the numbers. For fixed $n$ this is polynomial in $m$.

The time in the bit model also depends on the sizes of the numbers after the substitutions of line L11. Lenstra's analysis of his version shows that these sizes stay polynomial in the input size for fixed $n$, with a total time of the form $2^{O(n^3)}$ times a polynomial in the input size. Dadush, Eisenbrand and Rothvoss remark that a careful analysis gives $2^{O(n^2)}$ in place of $2^{O(n^3)}$. This page does not prove a size bound for the code, which uses a different rounding step.

## Properties

- **Exact.** All arithmetic is rational, and the answer NONE is a proof that no integer point exists.
- **Polynomial in fixed dimension.** For each fixed $n$ the time is polynomial in the input size, by [Lenstra's theorem](/lenstra-theorem/). [Integer feasibility](/integer-feasibility/) is [NP-complete](/np-complete/) when $n$ is part of the input.
- **Branching on hyperplanes.** It branches on general integer directions $d$, not on single variables as [branch and bound](/land-doig-algorithm/) does. This is why the number of branches is bounded by a function of $n$ alone.
- **Deterministic.** The vertex order, the choice of the simplex and LLL are deterministic.

## Variants and improvements

- **Kannan.** [Kannan's algorithm](/kannan-algorithm/) uses a shortest vector of the dual lattice instead of an LLL vector, and gets $n^{O(n)}$ in place of $2^{O(n^3)}$.
- **Frank and Tardos.** The [Frank-Tardos algorithm](/frank-tardos-algorithm/) replaces a rational objective by an integer one of polynomially bounded size with the same optimal solutions. Applied to the numbers of the input, this keeps the numbers inside the fixed-dimension algorithms small.
- **Rounding by ellipsoids.** Many accounts use an ellipsoid $E$ with $E \subseteq P \subseteq (n+1) E$ or a similar pair, computed with the [ellipsoid method](/ellipsoid-method/) or a [minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), in place of a simplex.
- **Faster dependence on n.** Dadush gave a $2^{O(n)} n^n$ algorithm, and Reis and Rothvoss a randomized $(\log 2n)^{O(n)}$ algorithm.
- **Generalized basis reduction.** Lovász and Scarf reduce a basis directly in the width norm of $P$, without a rounding step.

## When to use it

Use Lenstra's algorithm, or one of its successors, when the number of integer variables is small and the coefficients are large, so that [branch and bound](/land-doig-algorithm/) on single variables needs a huge tree. For the usual models with many variables, [branch and cut](/branch-and-cut/) is far faster in practice.

## Pitfalls

- **Unbounded polyhedra.** The rounding step needs a bounded $P$. Add a bounding box first; it must be large enough to keep an integer point when one exists.
- **Lower-dimensional polyhedra.** If $P$ has no interior, no simplex of positive volume exists. Line L3 handles this case with an equation of the affine hull.
- **The direction must be integer and primitive.** A rational $d$ must be scaled to integers with greatest common divisor 1, or the slices $d^\top x = k$ miss integer points or count them twice.
- **Floating point.** The method is exact only in rational arithmetic. Rounding errors in LLL or in $W$ can give a wrong NONE.
- **The rounding step is the expensive part of the code.** Enumerating all vertices and all simplices is polynomial only for fixed $n$, and it grows fast with $n$.

## Implementations

The Python code is exact: it uses `fractions.Fraction` everywhere and integer matrices for the lattice. It enumerates the vertices by brute force over all sets of $n$ rows, runs LLL with $\delta = 3/4$ in the norm $Q$, and builds $W$ with the extended Euclidean algorithm. The function `lenstra_maximize` adds a box to make $P$ bounded and does the binary search on the objective. The tests compare the optimum with brute force over all integer points of the box in dimensions 1 to 3, on random instances, thin strips and slabs, flat polyhedra and empty ones.

## History

Lenstra published the algorithm in Mathematics of Operations Research in 1983. It uses the basis reduction algorithm of Lenstra, Lenstra and Lovász (1982). Kannan improved the dependence on $n$ in 1987, and in the same year Frank and Tardos showed how to make the algorithms of Lenstra and Kannan run in polynomial space. The later work of Dadush (2012) and of Reis and Rothvoss (2023) improved the dependence on $n$ further.

## References
