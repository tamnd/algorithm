---
tag: GH5331
kind: algorithm
slug: pslq-algorithm
name: PSLQ algorithm
aliases:
- partial sum of squares lattice reduction
- PSLQ
- Ferguson-Bailey PSLQ
area: number-theory/lattice-reduction
level: advanced
summary: Iterative algorithm that finds integer relations among real numbers.
solves: [integer-relation-problem]
model: word-ram
complexity:
  vars: {n: the number of input values, X: the squared length of x scaled to a primitive integer vector, W: the largest absolute value of an entry of x or A or B during the run, M: the cost M(k) of multiplying two integers of k binary digits}
  time: {worst: O(n^4 log X), best: O(n^3)}
  space: {extra: O(n^2)}
  bit_operations: {worst: O(n^4 log X M(n log(n W)))}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1992
  people: [Helaman R. P. Ferguson, David H. Bailey]
  note: Introduced in a NASA Ames technical report and analyzed with Steve Arno in Mathematics of Computation in 1999.
prereqs: [integer-relation-problem, gram-schmidt-orthogonalization, size-reduction, lll-algorithm]
see_also: [lll-algorithm, simultaneous-diophantine-approximation, lattice-basis-reduction, lovasz-condition, continued-fraction, euclidean-algorithm, shortest-vector-problem, lattice-basis]
sources:
  - paper: "H. R. P. Ferguson, D. H. Bailey and S. Arno, Analysis of PSLQ, an integer relation finding algorithm, Mathematics of Computation 68(225), 1999"
    locator: pages 351 to 369 (the algorithm with the matrices H_x and A, the lower bound 1/max |h_jj| on the norm of any relation, and the bound on the number of iterations)
  - paper: "D. H. Bailey and D. J. Broadhurst, Parallel integer relation detection, techniques and applications, Mathematics of Computation 70(236), 2001"
    locator: the multilevel and multipair variants of PSLQ and their use in experimental mathematics
  - paper: "D. H. Bailey, P. B. Borwein and S. Plouffe, On the rapid computation of various polylogarithmic constants, Mathematics of Computation 66(218), 1997"
    locator: the digit extraction formula for pi, found by an integer relation search
  - paper: "J. Håstad, B. Just, J. C. Lagarias and C. P. Schnorr, Polynomial time algorithms for finding integer relations among real numbers, SIAM Journal on Computing 18(5), 1989"
    locator: the earlier polynomial-time integer relation algorithm, with a lower bound on the norm of relations
---

PSLQ finds an integer relation among numbers $x_1, \ldots, x_n$: integers $m_1, \ldots, m_n$, not all zero, with $m_1 x_1 + \cdots + m_n x_n = 0$. It keeps a unimodular integer matrix $A$ and a lower trapezoidal matrix $H$ that describes the rows of $A$ projected orthogonally to $x$, and at each step it swaps the two rows chosen by a weighted size rule and size-reduces, much like [LLL](/lll-algorithm/) without the Lovász test. When a relation exists it appears as a column of $A^{-1}$, and at every step the algorithm gives a proved lower bound on the length of any relation. It is the standard tool of experimental mathematics, where it found the Bailey-Borwein-Plouffe formula for $\pi$.

## In plain words

You have a few numbers and suspect that some combination of them with small whole-number weights adds up to exactly zero. PSLQ searches for those weights.

It keeps a list of candidate weight vectors and improves them step by step. Each candidate is judged by how far it is from giving zero. At each step the algorithm picks one pair of candidates by a rule that favours large errors near the front, swaps them, and then subtracts whole multiples of candidates from each other to make the errors small. As soon as one candidate gives exactly zero, it is the answer. Along the way, the algorithm also proves that no answer with smaller weights than a certain bound exists, and this bound grows as it runs.

## The problem

**Notation.** As on all pages of this area, vectors are rows. The input is $x = (x_1, \ldots, x_n) \ne 0$ with $n \ge 2$. An **integer relation** is a nonzero $m \in \mathbb{Z}^n$ with $\langle m, x \rangle = 0$; see the [integer relation problem](/integer-relation-problem/). We write $M_x$ for the length of a shortest relation, $P_x$ for the orthogonal projection onto $x^\perp$, and $\lceil c \rfloor = \lfloor c + 1/2 \rfloor$.

The algorithm keeps an integer matrix $A$ with $\det A = \pm 1$ and its inverse $B = A^{-1}$, also integer, and the vector $y = x B$, so that $x = y A$ and $y_j = \langle x, \text{column } j \text{ of } B \rangle$. A zero $y_j$ means that column $j$ of $B$ is a relation.

**The matrix $H$ as Gram-Schmidt data.** Let $p_i = a_i P_x$ be the rows of $A$ projected onto $x^\perp$, a space of dimension $n - 1$. Ferguson, Bailey and Arno keep an $n \times (n-1)$ lower trapezoidal matrix $H$ with $H H^{\mathsf T} = A P_x A^{\mathsf T}$, the Gram matrix of the $p_i$; its rows are the coordinates of the $p_i$ in an orthonormal basis of $x^\perp$. Such a factor is unique up to the signs of its columns, so it is the Gram-Schmidt data of $p_1, \ldots, p_n$:

$$h_{jj}^2 = B_j = \|p_j^*\|^2, \qquad \frac{h_{ij}}{h_{jj}} = \mu_{ij} \qquad (j \le n - 1),$$

and $p_n^* = 0$, since $n$ vectors lie in a space of dimension $n - 1$. This page uses $\mu_{ij}$ and $B_j$, which are rational when $x$ is rational, so the whole algorithm runs in exact arithmetic. Every decision of the algorithm depends only on $|h_{jj}|$ and on $h_{ij} / h_{jj}$, so it makes the same choices as the version with square roots; a 120-digit implementation of the original made the same choices and returned the same relations on 59 random rational inputs.

## The algorithm

The parameter is $\gamma > \sqrt{4/3}$; the implementation uses $\gamma^2 = 2$.

```pseudo id=main
PSLQ(x_1..x_n)                              ▷ exact form: H is stored as μ_ij and B_j = h_jj²
L1  A ← I; B ← I; y ← x; if some y_j = 0 then return e_j
L2  compute μ_ij and B_j of the rows p_i = a_i − (⟨a_i, x⟩ / ⟨x, x⟩) x, for j ≤ n − 1
L3  HERMITE-REDUCE
L4  loop
L5      if some y_j = 0 then return column j of B          ▷ a relation
L6      r ← the index 1 ≤ r ≤ n − 1 maximizing γ^(2r) B_r
L7      swap rows a_r, a_r+1; swap y_r, y_r+1; swap columns r, r+1 of B
L8      update μ and B by the swap formulas of LLL, with B_n = 0
L9      HERMITE-REDUCE

HERMITE-REDUCE                               ▷ size reduction of all rows p_i
L10 for i ← 2 to n, for j ← i − 1 down to 1 do
L11     t ← ⌈μ_ij⌋; a_i ← a_i − t a_j; μ_ik ← μ_ik − t μ_jk for k < j; μ_ij ← μ_ij − t
L12     y_j ← y_j + t y_i; column j of B ← column j of B + t · column i of B
```

**Line L8.** With $\mu = \mu_{r+1, r}$, the swap sets $B_r' = B_{r+1} + \mu^2 B_r$, $\mu_{r+1,r}' = \mu B_r / B_r'$ and $B_{r+1}' = B_r B_{r+1} / B_r'$, exchanges $\mu_{r,j}$ and $\mu_{r+1,j}$ for $j < r$, and updates $\mu_{i,r}, \mu_{i,r+1}$ for $i > r + 1$ as in the [LLL algorithm](/lll-algorithm/). For $r = n - 1$ it gives $B_{n-1}' = \mu^2 B_{n-1}$ and keeps $B_n = 0$; in the original description this is the case without the corner rotation of $H$.

**Line L12.** The row operation $a_i \leftarrow a_i - t a_j$ on $A$ is the column operation $b_j \leftarrow b_j + t b_i$ on $B = A^{-1}$, and then $y = x B$ changes only in entry $j$.

**The lower bound.** At any moment, every integer relation $m$ satisfies $\|m\| \ge 1 / \max_{j \le n-1} \sqrt{B_j}$, and $\max_j B_j$ never increases. So if the algorithm is stopped early, it has proved that no relation shorter than this bound exists.

## Example

**Small integers.** Take $x = (3, 5, 7)$. Then $P_x$ has Gram matrix $I - x^{\mathsf T} x / 83$, and Gram-Schmidt gives $B_1 = 74/83$, $B_2 = 49/74$, $\mu_{21} = -15/74$, $\mu_{31} = -21/74$, $\mu_{32} = -5/7$. Hermite reduction rounds $\mu_{32}$ to $-1$, so it adds row 2 of $A$ to row 3; then $y = (3, -2, 7)$.

| iteration | $\gamma^2 B_1, \gamma^4 B_2$ | $r$ | $y$ after the step | $B_1, B_2$ after | bound $1 / \max B_j$ before |
|---|---|---|---|---|---|
| 1 | $148/83, 196/74$ | 2 | $(-1, -1, -2)$ | $74/83, 2/37$ | $83/74$ |
| 2 | $148/83, 8/37$ | 1 | $(1, -1, -2)$ | $22/83, 2/11$ | $83/74$ |
| 3 | $44/83, 8/11$ | 2 | $(0, 0, -1)$ | $22/83, 1/22$ | $83/22$ |

After iteration 3, $y_1 = 0$, and column 1 of $B$ is $(-1, 2, -1)$: indeed $-3 + 10 - 7 = 0$. (Column 2, $(-2, -3, 3)$, is a second relation.) The bound of the last row says that every relation has $\|m\|^2 \ge 83/22 \approx 3.8$; the one found has $\|m\|^2 = 6$, and it is the shortest.

**A truncated real vector.** For $x = (1, 1.4142136, 1.7320508)$, the 7-digit values of $1, \sqrt 2, \sqrt 3$ as exact rationals, PSLQ takes 18 iterations and returns $(748, -1325, 650)$, of length about 1655. Before the last iteration it has proved that every relation has length at least 953. No small relation exists, because $1, \sqrt 2, \sqrt 3$ are linearly independent over $\mathbb{Q}$; the relation found is an artefact of the truncation, of size about the inverse of the precision to the power $1/(n-1)$.

## Correctness

The steps are unimodular row operations on $A$ with the matching column operations on $B$, so $A$ stays unimodular, $B = A^{-1}$ and $y = x B$; a returned column $b$ of $B$ is nonzero and has $\langle x, b \rangle = y_j = 0$. Lines L8 and L11 are the Gram-Schmidt updates of a swap and of a size reduction, applied to the rows $p_i$, so $\mu$ and $B$ stay their Gram-Schmidt data. While all $y_j \ne 0$, no $n - 1$ rows of $A$ span a space containing $x$, which keeps $B_1, \ldots, B_{n-1} > 0$ and the divisions well defined. For the bound, a relation $m$ lies in $x^\perp$, and $A m^{\mathsf T}$ is a nonzero integer vector with entries $\langle p_i, m \rangle$; the first $k$ with $\langle p_k^*, m \rangle \ne 0$ gives $1 \le |\langle p_k, m \rangle| = |\langle p_k^*, m \rangle| \le \|p_k^*\| \|m\|$. Termination for rational $x$ follows from a potential argument below. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**Cost model.** Exact rational arithmetic. The input is $x \in \mathbb{Q}^n$; scaling it to a primitive integer vector does not change any step, and $X$ is the squared length of that vector. The counts are arithmetic operations; for bits, $W$ bounds the absolute values of the entries of $x$, $A$ and $B$ during the run.

- **Iterations (proved, rational input).** The potential $D = \prod_{j=1}^{n-1} B_j^{n-j}$ starts at most 1 and drops by a factor at least $\tau^2 = 4 \gamma^2 / (4 + \gamma^2)$ at each iteration, and while no relation has been found it stays at least $X^{-(n-1)}$. So the number $I$ of iterations satisfies $\tau^{2I} \le X^{n-1}$, that is $I \le (n - 1) \ln X / \ln \tau^2 = O(n \log X)$; with $\gamma^2 = 2$, $\tau^2 = 4/3$.
- **Iterations (proved by Ferguson, Bailey and Arno, real input).** If $x \in \mathbb{R}^n$ has a relation of length $M_x$, PSLQ in exact real arithmetic finds a relation within $\binom{n}{2} \log(\gamma^{n-1} M_x) / \log \tau$ iterations, a bound that does not depend on the size of the numbers.
- **Operations per iteration.** The swap costs $O(n)$ for $A$, $B$ and $\mu$; Hermite reduction costs $O(n^3)$ for $\mu$ and $O(n^3)$ for the rows of $A$ and columns of $B$. Line L2 costs $O(n^3)$. The total is $O(n^3 I) = O(n^4 \log X)$, and $O(n^3)$ if a relation is found at once.
- **Bits.** All Gram-Schmidt data are ratios of minors of the integer matrix $\langle a_i, a_j \rangle \|x\|^2 - \langle a_i, x \rangle \langle a_j, x \rangle$, so they have $O(n \log(n W))$ digits, and the cost is $O(n^4 \log X \cdot M(n \log(n W)))$. We do not prove a bound on $W$ here; in the tests the entries stay small.
- **Floating point.** In practice $x$ is real and known to $d$ digits, and PSLQ runs in floating point with somewhat more than $d$ digits; it can then detect relations whose size is at most about $10^{d/(n-1)}$ before the precision runs out, which is the main practical limit.
- **Space.** $O(n^2)$ numbers.

## Properties

- **Proved lower bound.** At each step, $1 / \max_j |h_{jj}|$ is a lower bound on $M_x$, and it never decreases.
- **Not always the shortest relation.** For $x = (-5/2, -6, -7)$ PSLQ returns $(0, 7, -6)$, of squared length 85, while $(2, -2, 1)$ of squared length 9 is also a relation.
- **Finds a relation when one exists.** For real input with a relation, it terminates within the bound above, in exact arithmetic.
- **Numerically stable.** The original version is designed to work in floating point, with the size of $y_j$ and of the $h_{jj}$ telling when a relation has been found or the precision is exhausted.

## Variants and improvements

- **Multipair PSLQ.** Swap several disjoint pairs per iteration, which suits parallel machines (Bailey and Broadhurst).
- **Multilevel PSLQ.** Run most iterations in low precision and correct the matrices with high precision now and then, which is much faster for high precision inputs.
- **LLL-based relation finding.** Apply [LLL](/lll-algorithm/) to the lattice with basis rows $(e_i, C x_i)$ for a large constant $C$; a short vector gives a relation. It is simpler but needs the right scale $C$ and gives no lower bound.
- **HJLS.** The earlier algorithm of Håstad, Just, Lagarias and Schnorr is also polynomial and also gives lower bounds; PSLQ is closely related and numerically more stable.
- **Two numbers.** For $n = 2$ the index $r$ is always 1, and PSLQ becomes a form of the [Euclidean algorithm](/euclidean-algorithm/) on $x_1, x_2$ with nearest-integer quotients, related to the [continued fraction](/continued-fraction/) of $x_1 / x_2$.

## When to use it

Use it to recognize a number from its digits: is a constant a rational combination of known constants, or a root of a small polynomial (take $x = (1, \alpha, \alpha^2, \ldots, \alpha^d)$)? It is the method of choice in experimental mathematics and in high-precision physics computations. For an exact rational vector, cheaper methods based on gcds exist; for a single approximation problem with a bound on the denominators, see [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/).

## Pitfalls

- **Not enough precision.** With $d$ digits, PSLQ always finds some relation of size about $10^{d/(n-1)}$, whether or not a true one exists, as in the second example; a found relation is believable only if it is much smaller than that and stays the same when the precision increases.
- **The parameter.** $\gamma$ must exceed $\sqrt{4/3}$, so that $\tau > 1$; at $\gamma^2 = 4/3$ the potential argument gives no decrease.
- **Zero entries.** If some $x_j = 0$, the unit vector $e_j$ is a relation, and the Gram-Schmidt data of line L2 would divide by zero; check first, as line L1 does.
- **Partial reduction.** Some versions size-reduce only part of $H$ after a swap. The iteration bound still holds as long as $|\mu_{r+1,r}| \le 1/2$ before each swap, since the decrease $B_r' \le B_{r+1} + B_r / 4$ uses exactly that coefficient; skipping it breaks the bound.
- **Relations in $B$, not in $A$.** The relation is a column of $A^{-1}$; the rows of $A$ are not relations.

## Implementations

## History

Ferguson and Forcade (1979) gave the first integer relation algorithm for more than two numbers that is guaranteed to work, extending the [continued fraction](/continued-fraction/) idea, and Håstad, Just, Lagarias and Schnorr (1989) gave a polynomial-time algorithm based on lattice reduction. Ferguson and Bailey introduced PSLQ in a NASA Ames technical report (1991, revised 1992), and the analysis with Arno appeared in 1999. Bailey, Borwein and Plouffe used PSLQ to discover their 1997 formula for $\pi$ that allows computing its binary digits independently, and in 2000 PSLQ was listed among the top ten algorithms of the century in Computing in Science and Engineering.

## References
