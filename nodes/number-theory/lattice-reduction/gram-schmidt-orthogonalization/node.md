---
tag: HEDRFN
kind: technique
slug: gram-schmidt-orthogonalization
name: Gram-Schmidt orthogonalization
aliases:
- Gram-Schmidt process
- GSO
- Gram-Schmidt orthogonalisation of a lattice basis
area: number-theory/lattice-reduction
level: core
summary: Turns a basis into an orthogonal basis; used to define lattice reduction notions.
prereqs: [lattice, linear-independence, determinant]
see_also: [gram-schmidt-process, lattice-determinant, size-reduction, lovasz-condition, lll-algorithm, babai-nearest-plane, fincke-pohst-enumeration, cholesky-decomposition]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 17.3, The Gram-Schmidt algorithm (the exact algorithm, the bounds on the sizes of the numbers, and the integral version)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (Gram-Schmidt orthogonalization, the determinant, and the lower bound on the shortest vector)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer GTM 138, 1993
    locator: Section 2.6, Lattice reduction algorithms (Gram-Schmidt in the LLL algorithm, and the integral version with the numbers d_i)
  - paper: "A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261 (1982)"
    locator: pages 515 to 534, Section 1 (the notation b_i*, mu_ij and the use of Gram-Schmidt in basis reduction)
---

Gram-Schmidt orthogonalization turns a [basis](/lattice-basis/) $b_1, \ldots, b_n$ of a [lattice](/lattice/) into orthogonal vectors $b_1^*, \ldots, b_n^*$, where $b_i^*$ is the part of $b_i$ that is orthogonal to $b_1, \ldots, b_{i-1}$. The vectors $b_i^*$ are usually not in the lattice, but their lengths measure the lattice: their product is the [determinant](/lattice-determinant/), and the shortest of them is a lower bound for the shortest nonzero lattice vector. Every notion of basis reduction, from [size reduction](/size-reduction/) and the [Lovász condition](/lovasz-condition/) to [HKZ reduction](/hkz-reduction/), is a condition on the numbers $\mu_{ij}$ and $\|b_i^*\|$ that this technique computes. In lattice work the computation is done in exact rational arithmetic, and the vectors are not normalized, so no square root appears.

## In plain words

A lattice is a grid of points made from a few basic arrows. The arrows can point in bad directions, almost on top of each other, and then the grid is hard to see. Gram-Schmidt keeps the first arrow. From the second arrow it removes the part that points along the first arrow, and keeps only the part at a right angle to it. From the third arrow it removes the parts along the first two, and so on.

The new arrows are at right angles to each other, so lengths and volumes are easy to compute with them. They are not grid points in general, but they tell how thick each new layer of the grid is. A long list of numbers called the coefficients records how much was removed at each step, and many lattice algorithms read their decisions from these numbers.

## When it applies

**Notation used on these pages.** The basis vectors $b_1, \ldots, b_n \in \mathbb{R}^m$ are linearly independent and are the **rows** of the $n \times m$ matrix $B$. The lattice is $L(B) = \{\sum_{i=1}^n x_i b_i : x \in \mathbb{Z}^n\}$. The inner product is $\langle u, v \rangle = \sum_k u_k v_k$ and $\|v\| = \langle v, v \rangle^{1/2}$. The Gram-Schmidt vectors are

$$b_1^* = b_1, \qquad b_i^* = b_i - \sum_{j=1}^{i-1} \mu_{ij} b_j^*, \qquad \mu_{ij} = \frac{\langle b_i, b_j^* \rangle}{\langle b_j^*, b_j^* \rangle} \quad (1 \le j < i \le n),$$

with $\mu_{ii} = 1$ and $\mu_{ij} = 0$ for $j > i$. The map $\pi_i$ is the orthogonal projection onto the orthogonal complement of $\operatorname{span}(b_1, \ldots, b_{i-1})$, so $b_i^* = \pi_i(b_i)$. Other pages of this area use the same symbols: $\lambda_1(L)$ for the length of a shortest nonzero vector, $\det(L)$ for the determinant, and $\delta$ for the parameter of the [LLL algorithm](/lll-algorithm/).

Use the technique when a problem about a lattice needs any of these facts:

- **The basis as a triangular matrix.** $B = M B^*$, where $M = (\mu_{ij})$ is lower triangular with ones on the diagonal and $B^*$ has the orthogonal rows $b_i^*$. In an orthonormal frame adapted to the $b_i^*$, the basis is lower triangular with diagonal $\|b_1^*\|, \ldots, \|b_n^*\|$. This is the [QR decomposition](/qr-decomposition/) of $B^T$ without the normalization, and $M \operatorname{diag}(\|b_i^*\|^2) M^T$ is the [Cholesky decomposition](/cholesky-decomposition/) of the Gram matrix $G = B B^T$.
- **Volumes.** $\det(L) = \prod_{i=1}^n \|b_i^*\|$, and $\det(G) = \prod_i \|b_i^*\|^2$.
- **A lower bound on short vectors.** $\lambda_1(L) \ge \min_i \|b_i^*\|$.
- **Coordinates of a target in layers.** A lattice is the union of the parallel hyperplanes $c\, b_n^* + \operatorname{span}(b_1, \ldots, b_{n-1})$ plus lattice shifts, $c \in \mathbb{Z}$, which are $\|b_n^*\|$ apart. [Babai's nearest plane](/babai-nearest-plane/) and [enumeration](/fincke-pohst-enumeration/) walk down these layers.
- **Reduction conditions.** Size reduction asks $|\mu_{ij}| \le 1/2$. The Lovász condition asks $\|b_i^*\|^2 \ge (\delta - \mu_{i,i-1}^2) \|b_{i-1}^*\|^2$. HKZ, [BKZ](/bkz-algorithm/) and [deep insertion](/deep-lll/) speak about the projections $\pi_i$.

## The template

```pseudo id=main
GSO(b_1, ..., b_n)                 ▷ rows of B, linearly independent; exact rationals
L1  for i ← 1 to n do
L2      v ← b_i
L3      for j ← 1 to i − 1 do
L4          μ_ij ← ⟨b_i, b_j*⟩ / N_j
L5          v ← v − μ_ij b_j*
L6      b_i* ← v
L7      N_i ← ⟨v, v⟩               ▷ N_i = ‖b_i*‖², never a square root
L8  return (b*, μ, N)
```

Line L4 uses $\langle b_i, b_j^* \rangle$. Because $v - b_i$ is a combination of $b_1^*, \ldots, b_{j-1}^*$, which are orthogonal to $b_j^*$, the value $\langle v, b_j^* \rangle$ at that moment is the same number. Using $v$ is the "modified" Gram-Schmidt order. In exact arithmetic the two orders give identical results; in floating point the modified order loses less orthogonality.

**The facts and their proofs.**

1. *Orthogonality and spans.* For each $i$, $b_i^*$ is orthogonal to $b_1^*, \ldots, b_{i-1}^*$, and $\operatorname{span}(b_1^*, \ldots, b_i^*) = \operatorname{span}(b_1, \ldots, b_i)$. Proof by induction on $i$. Assume the claim for $i - 1$. For $k < i$, $\langle b_i^*, b_k^* \rangle = \langle b_i, b_k^* \rangle - \sum_{j<i} \mu_{ij} \langle b_j^*, b_k^* \rangle = \langle b_i, b_k^* \rangle - \mu_{ik} N_k = 0$, because only the term $j = k$ survives. The definition writes $b_i^*$ as $b_i$ plus an element of $\operatorname{span}(b_1, \ldots, b_{i-1})$, so the spans agree. Since $b_1, \ldots, b_i$ are independent, $b_i \notin \operatorname{span}(b_1^*, \ldots, b_{i-1}^*)$, so $b_i^* \ne 0$ and $N_i > 0$: line L4 never divides by zero.
2. *Triangular form.* Rearranging the definition gives $b_i = b_i^* + \sum_{j<i} \mu_{ij} b_j^*$, which is $B = M B^*$.
3. *Determinant.* $G = B B^T = M B^* (B^*)^T M^T = M \operatorname{diag}(N_1, \ldots, N_n) M^T$, and $\det M = 1$, so $\det G = \prod_i N_i$. A second basis $B' = U B$ of the same lattice has $U$ [unimodular](/unimodular-matrix/), so $\det(B' B'^T) = \det(U)^2 \det G = \det G$. Hence $\det(L) = (\det G)^{1/2} = \prod_i \|b_i^*\|$ depends only on the lattice. When $n = m$ it equals $|\det B|$.
4. *Lower bound on $\lambda_1$.* Let $v = \sum_i x_i b_i \ne 0$ with $x \in \mathbb{Z}^n$, and let $k$ be the largest index with $x_k \ne 0$. By fact 2, $v = x_k b_k^* + (\text{a combination of } b_1^*, \ldots, b_{k-1}^*)$, so by orthogonality $\|v\|^2 \ge x_k^2 N_k \ge N_k \ge \min_i N_i$.
5. *Projections.* $\pi_i(b_k) = \sum_{j=i}^{k} \mu_{kj} b_j^*$ for $k \ge i$, so $\|\pi_i(b_k)\|^2 = \sum_{j=i}^{k} \mu_{kj}^2 N_j$. The vectors $\pi_i(b_i), \ldots, \pi_i(b_n)$ form a basis of the projected lattice $\pi_i(L)$, with Gram-Schmidt vectors $b_i^*, \ldots, b_n^*$.
6. *Integrality.* Let $B$ have integer entries and let $d_i = \det(G_i) = \prod_{j \le i} N_j$, the Gram determinant of $b_1, \ldots, b_i$, with $d_0 = 1$. Then each $d_i$ is a positive integer, $d_{i-1} b_i^* \in \mathbb{Z}^m$, and $d_j \mu_{ij} \in \mathbb{Z}$. Proof: $b_i^* = b_i - \sum_{j<i} c_j b_j$, where the $c_j$ solve the linear system $\sum_{j<i} c_j \langle b_j, b_k \rangle = \langle b_i, b_k \rangle$ for $k < i$, whose matrix is $G_{i-1}$. By Cramer's rule, $d_{i-1} c_j \in \mathbb{Z}$, so $d_{i-1} b_i^* \in \mathbb{Z}^m$. Also $\mu_{ij} = \langle b_i, b_j^* \rangle / N_j$ and $N_j = d_j / d_{j-1}$, so $d_j \mu_{ij} = \langle b_i, d_{j-1} b_j^* \rangle \in \mathbb{Z}$.

**Cost.** The loops do $\Theta(n^2 m)$ arithmetic operations on rationals: $i - 1$ inner products and vector updates of length $m$ for each $i$. For integer input with $\|b_i\| \le X$, Hadamard's inequality gives $d_i \le X^{2i}$, so by fact 6 every numerator and denominator has $O(n \log X)$ binary digits. In the integral version below, where all numbers are integers of this size, the whole computation takes $O(n^4 m \log^2 X)$ bit operations with schoolbook multiplication. The bound is proved, not heuristic. A floating-point version with $O(n)$ or fewer digits of precision is what fast LLL implementations use; its error must then be controlled separately.

## Classic examples

1. **The determinant of a lattice.** Fact 3 computes [$\det(L)$](/lattice-determinant/) for a lattice that is not full rank, where $\det B$ does not exist.
2. **[Size reduction](/size-reduction/).** Subtract $\lceil \mu_{ij} \rfloor b_j$ from $b_i$ for $j = i-1, \ldots, 1$ to reach $|\mu_{ij}| \le 1/2$. The $b_i^*$ do not change, only $\mu$ does.
3. **[Lagrange-Gauss reduction](/lagrange-gauss-reduction/).** In dimension 2, the one coefficient $\mu_{21}$ decides each step.
4. **The [LLL algorithm](/lll-algorithm/).** It keeps $|\mu_{ij}| \le 1/2$ and swaps $b_{k-1}, b_k$ when $N_k < (\delta - \mu_{k,k-1}^2) N_{k-1}$. Its termination proof uses the integers $d_i$ of fact 6.
5. **[Babai's nearest plane algorithm](/babai-nearest-plane/)** and **[Fincke-Pohst enumeration](/fincke-pohst-enumeration/).** Both use fact 5 to cut the search into one-dimensional problems, from $b_n^*$ down to $b_1^*$.
6. **[HKZ](/hkz-reduction/) and [BKZ](/bkz-algorithm/).** Both are defined through the projected lattices $\pi_i(L)$ of fact 5.

**A worked example.** Take the rows $b_1 = (1, 1, 1)$, $b_2 = (-1, 0, 2)$, $b_3 = (3, 5, 6)$.

| $i$ | $\mu_{i1}$ | $\mu_{i2}$ | $b_i^*$ | $N_i = \|b_i^*\|^2$ | $d_i$ |
|---|---|---|---|---|---|
| 1 | | | $(1, 1, 1)$ | $3$ | $3$ |
| 2 | $1/3$ | | $(-4/3, -1/3, 5/3)$ | $14/3$ | $14$ |
| 3 | $14/3$ | $13/14$ | $(-3/7, 9/14, -3/14)$ | $9/14$ | $9$ |

So $\det(G) = 3 \cdot \tfrac{14}{3} \cdot \tfrac{9}{14} = 9$ and $\det(L) = 3 = |\det B|$. The integrality of fact 6 is visible: $d_1 b_2^* = (-4, -1, 5)$, $d_2 b_3^* = (-6, 9, -3)$, $d_1 \mu_{21} = 1$, $d_1 \mu_{31} = 14$ and $d_2 \mu_{32} = 13$. Fact 4 gives $\lambda_1 \ge (9/14)^{1/2} \approx 0.80$; the true value is $\lambda_1 = \sqrt 3$, reached by $b_1$. The basis is not size-reduced, because $\mu_{31} = 14/3$.

## Variations

- **Integral Gram-Schmidt.** Store the integers $d_i$ and $\lambda_{ij} = d_j \mu_{ij}$ instead of rationals. The integral LLL of de Weger and Cohen (Cohen, Section 2.6) does all its work with these integers, and the sizes stay $O(n \log X)$.
- **Updates instead of recomputation.** Swapping $b_{k-1}$ and $b_k$ changes only $N_{k-1}$, $N_k$ and the coefficients in rows and columns $k-1$ and $k$; closed formulas give the new values in $O(n)$ operations. Size reduction of $b_k$ changes only row $k$ of $M$.
- **Gram matrix input.** Everything above uses only inner products, so it runs on $G$ alone: $\mu_{ij} N_j = G_{ij} - \sum_{k<j} \mu_{jk} \mu_{ik} N_k$. This is the Cholesky form used by Fincke and Pohst and by the floating-point LLL of Nguyen and Stehlé.
- **Floating point.** The numerical [Gram-Schmidt process](/gram-schmidt-process/) and [Householder reflections](/householder-reflections/) compute an orthonormal version. They are fast but need an error analysis; with too little precision LLL can loop or return a basis that is not reduced.
- **Other orders.** Orthogonalizing the rows in reverse order gives the Gram-Schmidt data of the reversed basis, which is related to the [dual lattice](/dual-lattice/): if $D$ is the dual basis ordered backwards, its Gram-Schmidt lengths are $1/\|b_n^*\|, \ldots, 1/\|b_1^*\|$.

## Pitfalls

- **Normalizing the vectors.** Dividing $b_i^*$ by $\|b_i^*\|$ brings in square roots and ends exact arithmetic. Lattice algorithms keep $b_i^*$ unnormalized and work with $N_i = \|b_i^*\|^2$.
- **Treating $b_i^*$ as lattice vectors.** In the example, $b_3^* = (-3/7, 9/14, -3/14)$ has non-integer entries, while the lattice is in $\mathbb{Z}^3$. The bound $\lambda_1 \ge \min \|b_i^*\|$ is often far from tight.
- **Forgetting that the order matters.** The $b_i^*$ depend on the order of the basis. A swap of two vectors changes $N_{k-1}$ and $N_k$; this is exactly what LLL uses.
- **Dividing by $\langle b_j, b_j \rangle$.** The coefficient is $\langle b_i, b_j^* \rangle / \langle b_j^*, b_j^* \rangle$. With $\langle b_j, b_j \rangle$ in the denominator the vectors are not orthogonal from $j = 2$ on.
- **Dependent input.** If the rows are dependent, some $N_i = 0$ and line L4 divides by zero. Generating sets need a variant (the MLLL algorithm, or a [Hermite normal form](/hermite-normal-form/) first).
- **Classical order in floating point.** Computing $\langle b_i, b_j^* \rangle$ against the original $b_i$ in floating point gives vectors that drift from orthogonality when the basis is badly conditioned. Use the modified order, a Gram matrix with enough precision, or exact rationals.

## Exercises

1. Show that $\|b_i^*\| \le \|b_i\|$, with equality if and only if $b_i$ is orthogonal to $b_1, \ldots, b_{i-1}$. Deduce Hadamard's inequality $\det(L) \le \prod_i \|b_i\|$.
2. Let $b_1 = (1, 0)$ and $b_2 = (5, 1)$. Compute $\mu_{21}$, $b_2^*$ and $\det(L)$, then size-reduce $b_2$ and check that $b_2^*$ does not change.
3. Prove that swapping $b_{k-1}$ and $b_k$ gives the new value $N_{k-1}' = N_k + \mu_{k,k-1}^2 N_{k-1}$ and $N_k' = N_{k-1} N_k / N_{k-1}'$.
4. For the integer basis of the worked example, use fact 6 to predict the denominators that can appear in $b_2^*$ and $b_3^*$, and compare with the table.

## References
