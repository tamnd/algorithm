---
tag: TQ44SE
kind: algorithm
slug: lagrange-gauss-reduction
name: Lagrange-Gauss reduction
aliases:
- Gauss reduction
- two-dimensional lattice reduction
- Lagrange's algorithm
- Gauss's algorithm for binary quadratic forms
area: number-theory/lattice-reduction
level: intro
summary: Exact algorithm that reduces a two-dimensional lattice basis and finds the shortest vector.
solves: [shortest-vector-problem]
model: word-ram
complexity:
  vars: {m: the length of the two vectors, β: the largest binary length of an input entry, R: the squared length of the shorter input vector divided by λ_1^2}
  time: {worst: O(m (1 + log R)), best: O(m)}
  space: {extra: O(m)}
  bit_operations: {worst: O(m (β + log m)^3), refined: O(m (β + log m)^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1773
  people: [Joseph-Louis Lagrange, Carl Friedrich Gauss]
  note: Lagrange reduced binary quadratic forms in 1773; Gauss gave the theory of reduced forms in the Disquisitiones Arithmeticae of 1801.
prereqs: [lattice, gram-schmidt-orthogonalization, euclidean-algorithm]
see_also: [lll-algorithm, size-reduction, shortest-vector-problem, successive-minima, minkowski-reduced-basis, hermite-constant, continued-fraction, lattice-basis-reduction]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 17.1, Lattice basis reduction in two dimensions (the algorithm, the proof that it finds the minima, and its number of iterations)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (Lagrange's algorithm, its history and its analysis)
  - paper: "P. Q. Nguyen and D. Stehlé, Low-dimensional lattice basis reduction revisited, ACM Transactions on Algorithms 5(4), Article 46 (2009)"
    locator: the greedy algorithm, which is Lagrange's algorithm in dimension 2, and its quadratic bit complexity in dimensions up to 4
  - paper: "B. Vallée, Gauss' algorithm revisited, Journal of Algorithms 12(4) (1991)"
    locator: pages 556 to 572 (worst-case and average-case analysis of the number of iterations)
---

Lagrange-Gauss reduction takes a basis $b_1, b_2$ of a [lattice](/lattice/) of rank 2 and returns a basis $u, v$ of the same lattice with $\|u\| = \lambda_1$ and $\|v\| = \lambda_2$, the two [successive minima](/successive-minima/). So it solves the [shortest vector problem](/shortest-vector-problem/) exactly in dimension 2. It works like the [Euclidean algorithm](/euclidean-algorithm/) on vectors: it subtracts the best integer multiple of the shorter vector from the longer one, swaps, and repeats. The number of iterations is logarithmic in the input, and the algorithm is the base case and the inner step of the [LLL algorithm](/lll-algorithm/).

## In plain words

You have two arrows that build a grid of points in a plane. They may be long and point in almost the same direction. You want two short arrows that build the same grid.

Take the shorter arrow. Subtract it from the longer arrow as many times as makes the longer one as short as possible. Now the second arrow may have become the shorter one; if so, swap their roles and do it again. When the subtraction no longer gives an arrow shorter than the other one, stop. The two arrows you hold now are as short as any two grid arrows can be. Each round makes the arrows much shorter, so few rounds are needed even for huge numbers.

## The problem

**Input.** Two linearly independent vectors $b_1, b_2 \in \mathbb{Q}^m$, $m \ge 2$, the rows of a basis $B$ of $L = L(B)$.

**Output.** A basis $(u, v)$ of $L$ that is **Lagrange-reduced** (also called Gauss-reduced):

$$\|u\| \le \|v\| \qquad \text{and} \qquad |\mu| \le \tfrac12, \quad \text{where } \mu = \frac{\langle u, v \rangle}{\langle u, u \rangle}.$$

The second condition is the [size reduction](/size-reduction/) of $v$ against $u$. For a reduced basis, $\|u\| = \lambda_1(L)$ and $\|v\| = \lambda_2(L)$, and the angle between $u$ and $v$ lies between $60$ and $120$ degrees.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows, $b_i^*$ and $\mu_{ij}$ are the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data and $\lambda_1$ is the first minimum. All arithmetic is exact, on integers or rationals. The time bound counts arithmetic operations; the bit bound counts operations on binary digits for integer input whose entries have binary length at most $\beta$.

## The algorithm

```pseudo id=main
LAGRANGE-GAUSS(b_1, b_2)          ▷ linearly independent; returns a reduced basis (u, v)
L1  (u, v) ← (b_1, b_2); if ‖u‖ > ‖v‖ then swap u and v
L2  loop
L3      q ← ⌈⟨u, v⟩ / ⟨u, u⟩⌋        ▷ nearest integer, halves rounded up
L4      v ← v − q u
L5      if ‖v‖ ≥ ‖u‖ then return (u, v)
L6      swap u and v
```

Line L3 computes the coefficient $\mu$ of the [Gram-Schmidt](/gram-schmidt-orthogonalization/) decomposition and rounds it. Line L4 makes $v$ as short as possible among the vectors $v - k u$, $k \in \mathbb{Z}$: the squared norm $\|v - k u\|^2 = \|v^*\|^2 + (\mu - k)^2 \|u\|^2$ is smallest at the integer nearest to $\mu$. If the new $v$ is still at least as long as $u$, the pair is reduced and line L5 returns it. Otherwise $v$ is now the shorter vector, and line L6 swaps the roles. The comparisons use squared norms, so no square root is computed.

## Example

Reduce $b_1 = (24, 60)$, $b_2 = (21, 53)$. The determinant is $|24 \cdot 53 - 60 \cdot 21| = 12$. Line L1 swaps, since $\|b_2\|^2 = 3250 < 3456 = \|b_1\|^2$.

| iteration | $u$ | $v$ | $\mu$ | $q$ | new $v$ | $\|\text{new } v\|^2$ | $\|u\|^2$ | action |
|---|---|---|---|---|---|---|---|---|
| 1 | $(21, 53)$ | $(24, 60)$ | $1842/1625 \approx 1.13$ | 1 | $(3, 7)$ | 58 | 3250 | swap |
| 2 | $(3, 7)$ | $(21, 53)$ | $217/29 \approx 7.48$ | 7 | $(0, 4)$ | 16 | 58 | swap |
| 3 | $(0, 4)$ | $(3, 7)$ | $7/4 = 1.75$ | 2 | $(3, -1)$ | 10 | 16 | swap |
| 4 | $(3, -1)$ | $(0, 4)$ | $-2/5$ | 0 | $(0, 4)$ | 16 | 10 | return |

The output is $u = (3, -1)$, $v = (0, 4)$, with $|\mu| = 2/5 \le 1/2$ and $\|u\|^2 = 10 \le 16 = \|v\|^2$. So $\lambda_1 = \sqrt{10}$ and $\lambda_2 = 4$, and the determinant is still $|3 \cdot 4 - (-1) \cdot 0| = 12$. The squared length of $u$ falls $3250, 58, 16, 10$: from iteration 1 to 3 by a factor of about 200, and from iteration 2 to 4 by a factor of 5.8, more than the factor 3 that the proof guarantees.

## Correctness

Each step multiplies the pair by an integer matrix of determinant $\pm 1$, so the pair stays a basis of $L$. At the return, line L4 has made $|\mu| \le 1/2$ and line L5 has checked $\|v\| \ge \|u\|$. For a reduced pair and any $w = x u + y v \ne 0$,

$$\|w\|^2 \ge (x^2 - |xy| + y^2) \|u\|^2 + y^2 (\|v\|^2 - \|u\|^2) \ge \|u\|^2,$$

because $x^2 - |xy| + y^2 \ge 1$ for integers not both zero; and if $y \ne 0$ the bound improves to $\|v\|^2$. So $u$ is a shortest vector and $v$ is a shortest vector independent of $u$. The full proof, with termination, is in the proof below.

## Complexity

Let $r_k = \|u\|^2$ at the start of iteration $k$. The proof shows that $r_{k+1} < r_{k-1}/3$ for every iteration $2 \le k < T$: a step that does not stop must use $|q| \ge 2$, because $q = 0$ or $q = \pm 1$ on a pair that was size-reduced in the previous step cannot give a shorter vector. Since $r_T \ge \lambda_1^2$, the number of iterations is

$$T \le 2 + 2 \log_3 \frac{\min(\|b_1\|^2, \|b_2\|^2)}{\lambda_1^2} = O(1 + \log R).$$

- **Arithmetic operations.** Each iteration costs $O(m)$, so the total is $O(m (1 + \log R))$ in the worst case and $O(m)$ for an input that is already reduced. This bound is proved.
- **Bit operations.** For integer entries of binary length at most $\beta$, $\lambda_1 \ge 1$, so $T = O(\beta + \log m)$, and every number has $O(\beta + \log m)$ binary digits. Schoolbook multiplication gives $O(m (\beta + \log m)^3)$. As for Euclid's algorithm, the sizes of the quotients telescope, and Nguyen and Stehlé prove a quadratic bound $O(m (\beta + \log m)^2)$ for this algorithm and its greedy generalizations up to dimension 4.
- **Space.** Two vectors and a few scalars, $O(m)$ numbers.
- **Average case.** Vallée analysed the number of iterations for random inputs; it is $O(1)$ on average for natural distributions, with a geometric tail.

## Properties

- **Exact.** All operations are on integers or rationals, and the result is exact; no precision issue arises.
- **Optimal output.** It returns both minima, not an approximation. In dimension 2 a Lagrange-reduced basis is the same as a [Minkowski-reduced](/minkowski-reduced-basis/) and an [HKZ-reduced](/hkz-reduction/) basis.
- **Unique up to signs and ties.** The reduced basis is unique up to the signs of $u$ and $v$, except when $\|u\| = \|v\|$ or $|\mu| = 1/2$.
- **The Hermite bound in dimension 2.** From $\|v^*\|^2 = \|v\|^2 - \mu^2 \|u\|^2 \ge \tfrac34 \|u\|^2$ and $\det(L) = \|u\| \|v^*\|$, one gets $\lambda_1^2 \le \tfrac{2}{\sqrt 3} \det(L)$. This is the exact value $\gamma_2 = 2/\sqrt 3$ of the [Hermite constant](/hermite-constant/), reached by the hexagonal lattice.

## Variants and improvements

- **The LLL step.** The [LLL algorithm](/lll-algorithm/) applies a relaxed version of this step to the projected pairs $(\pi_{k-1}(b_{k-1}), \pi_{k-1}(b_k))$: it swaps only if the swap shortens $b_{k-1}^*$ by a factor $\delta < 1$, which makes the number of swaps polynomial in any dimension.
- **Greedy reduction in dimensions 3 and 4.** Semaev, and then Nguyen and Stehlé, extended the algorithm by reducing the last vector against the closest vector of the lattice spanned by the others. The result is Minkowski-reduced up to dimension 4 and the cost stays quadratic; the greedy method fails to be optimal from dimension 5 on.
- **Binary quadratic forms.** The same algorithm on the form $a x^2 + b x y + c y^2$, with $a = \|u\|^2$, $b = 2 \langle u, v \rangle$ and $c = \|v\|^2$, is Lagrange's and Gauss's reduction of positive definite forms: a form is reduced when $|b| \le a \le c$.
- **Fast versions.** Like the [half-GCD](/half-gcd/), a divide-and-conquer version works on the leading parts of the numbers and reaches a quasi-linear bit cost; the method is due to Schönhage and later to Yap.
- **The relaxed condition.** Stopping as soon as $\|v\| \ge \|u\| / \sqrt{\delta}$ fails, with $\delta < 1$, gives a basis that is reduced up to the factor $\delta$; this is the 2-dimensional LLL.

## When to use it

Use it whenever a lattice of rank 2 must be reduced: for the reduction of binary quadratic forms and class group computations, for finding a short pair of vectors in a two-dimensional knapsack or Diophantine problem, and as a test case for any reduction code. It is exact and needs no parameters. In higher dimension it is not enough by itself; use [LLL](/lll-algorithm/) for a polynomial-time approximation, and [BKZ](/bkz-algorithm/) or [enumeration](/fincke-pohst-enumeration/) for stronger results.

## Pitfalls

- **Rounding with truncation.** Replacing line L3 by $q \leftarrow \lfloor \mu \rfloor$ (integer division) leaves $|\mu - q|$ up to 1, so the output can fail $|\mu| \le 1/2$ and need not contain a shortest vector. Use the nearest integer.
- **Stopping on $\|v\| > \|u\|$ only.** Line L5 must return when $\|v\| \ge \|u\|$. With a strict test, a pair with $\|v\| = \|u\|$ is swapped again and the loop can cycle forever, for example on $u = (1, 0)$, $v = (0, 1)$.
- **Floating point $\mu$.** For entries above $2^{26}$ or so, computing $\mu$ in double precision can round to the wrong integer, and the loop then may not stop or may return a pair that is not reduced. Compute $q$ from the exact inner products, as $\lfloor (2\langle u, v \rangle + \langle u, u \rangle) / (2 \langle u, u \rangle) \rfloor$ in integer arithmetic.
- **Dependent input.** For dependent vectors the loop reaches $u = 0$ and line L3 divides by zero. Check $\langle b_1, b_1 \rangle \langle b_2, b_2 \rangle \ne \langle b_1, b_2 \rangle^2$ first, or reduce the generating set by the gcd-like process until one vector becomes 0.
- **Comparing norms, not squared norms.** Taking square roots costs time and introduces rounding. All comparisons in lines L1 and L5 work on squared norms.

## Implementations

## History

Lagrange described the reduction of binary quadratic forms in 1773, and Gauss developed the theory of reduced forms in the Disquisitiones Arithmeticae (1801). The algorithm is often called Gauss's algorithm, but Nguyen's survey traces it to Lagrange. Its worst-case and average-case analysis as an algorithm is due to Lagarias (1980) and Vallée (1991), and the quadratic bit complexity was proved by Nguyen and Stehlé for this algorithm and its extension to dimensions 3 and 4.

## References
