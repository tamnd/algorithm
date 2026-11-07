---
tag: MQ8TPZ
kind: technique
slug: gaussian-elimination-modular
name: Gaussian elimination for modular systems
aliases:
- Gauss method for modular systems
- Gaussian elimination modulo p
- modular Gaussian elimination
area: algebra/exact-linear-algebra
level: core
summary: Solves linear systems over a prime modulus by row reduction using modular inverses in place of division.
prereqs: [gaussian-elimination, modular-inverse, fermat-little-theorem]
see_also: [gauss-jordan-elimination, multimodular-determinant, linear-system-modulo-2, bitset-gaussian-elimination, chinese-remainder-theorem, dixon-p-adic-lifting, linear-congruence, montgomery-multiplication]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 5, Section 5.5, Modular determinant computation (elimination modulo many small primes, the Hadamard bound on the number of primes, and the unlucky primes)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2, Linear algebra algorithms on square matrices (the algorithms are stated over an arbitrary field, which includes Z/pZ)
  - url: "https://cp-algorithms.com/linear_algebra/linear-system-gauss.html"
    title: cp-algorithms, Gauss method for solving system of linear equations
    locator: the sections on the modular case and on the number of solutions
  - paper: doi:10.1007/BF01459082
    title: John D. Dixon, Exact solution of linear equations using p-adic expansions, Numerische Mathematik 40, 1982
    locator: pp. 137 to 141 (one elimination modulo p, then p-adic lifting to the rational solution)
  - paper: "John A. Howell, Spans in the module (Z_m)^s, Linear and Multilinear Algebra 19(1), 1986"
    locator: pp. 67 to 77 (a canonical echelon form over Z/mZ for a composite modulus m)
---

Gaussian elimination works over every field, and for a prime $p$ the integers modulo $p$ form a field $\mathbb{Z}/p\mathbb{Z}$. So the elimination loop runs unchanged on residues: every addition and multiplication is reduced modulo $p$, and every division by a pivot $c$ becomes a multiplication by the [modular inverse](/modular-inverse/) $c^{-1} \bmod p$. The technique solves systems of congruences modulo a prime, counts their solutions, inverts matrices modulo $p$, and computes ranks and determinants modulo $p$. Its larger use is as the inner step of modular methods over $\mathbb{Z}$ and $\mathbb{Q}$, where numbers would otherwise grow: reduce the integer matrix modulo one or more primes, eliminate with entries of fixed size, and lift or combine the results.

Notation: $p$ is a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$ with residues $0, \dots, p-1$, $A$ is an $m \times n$ matrix over $\mathbb{F}_p$ or over $\mathbb{Z}$, $n$ is also the size of a square matrix, and for an integer matrix $b$ is the maximum binary length of an entry. $\bar{A}$ is the matrix of the residues of $A$ modulo $p$.

## In plain words

Ordinary elimination divides by the leading number of a row. With remainders modulo a prime, you cannot divide in the usual way, but every nonzero remainder has a partner that multiplies with it to give 1. Multiplying by that partner does the same job as dividing. So you run the usual elimination and keep every number as a remainder. The numbers never grow, which makes it fast and safe. The prime must really be prime, or some numbers have no partner.

## When it applies

The technique needs three things.

- **A field.** $\mathbb{Z}/m\mathbb{Z}$ is a field exactly when $m$ is prime. Then each nonzero residue $c$ has an inverse, computed by the [extended Euclidean algorithm](/extended-euclidean-algorithm/) in $O(\log p)$ arithmetic steps, or as $c^{p-2} \bmod p$ by [Fermat's little theorem](/fermat-little-theorem/). For a composite $m$ some nonzero residues have no inverse, and the loop must change (see Variations).
- **A problem stated modulo $p$, or a reason to reduce.** Either the input is a system of congruences modulo $p$, or it is an integer problem whose answer can be recovered from residues: a determinant (combine the residues for several primes with the [Chinese remainder theorem](/chinese-remainder-theorem/)), a rational solution (lift a solution modulo $p$ to one modulo $p^k$ and reconstruct the fractions), or a rank (the rank modulo $p$ is a lower bound, equal for all but finitely many $p$).
- **Residues that fit the machine.** If $p < 2^{w/2}$ on a machine with $w$-bit words, a product of two residues fits in one word, and each field operation is $O(1)$ word operations. Competitive programs use $p = 998244353$ or $p = 10^9 + 7$ with 64-bit products.

Reduction modulo $p$ is a ring homomorphism $\mathbb{Z} \to \mathbb{F}_p$. It commutes with sums and products, and so with every polynomial expression in the entries. In particular $\det \bar{A} = \overline{\det A}$, every minor of $\bar{A}$ is the residue of the minor of $A$, and the adjugate commutes with reduction. These facts are what make the residues useful.

## The template

The pseudocode indexes rows and columns from $0$. It computes the reduced row echelon form, as in [Gauss-Jordan elimination](/gauss-jordan-elimination/), because that form gives the solution directly. The plain staircase form of [Gaussian elimination](/gaussian-elimination/) works as well, with back substitution.

```pseudo id=main
MOD-ELIM(A, p)                               ▷ A is m × n with entries in {0, …, p − 1}, p prime
L1  r ← 0, P ← empty list
L2  for j ← 0 to n − 1 do
L3      q ← the least i with r ≤ i < m and A[i, j] ≠ 0, or NONE
L4      if q = NONE then continue with the next j
L5      swap rows r and q
L6      c ← INVERSE-MOD(A[r, j], p)            ▷ c · A[r, j] ≡ 1 (mod p)
L7      for t ← j to n − 1 do A[r, t] ← A[r, t] · c mod p
L8      for each i ≠ r with A[i, j] ≠ 0 do
L9          f ← A[i, j]
L10         for t ← j to n − 1 do A[i, t] ← (A[i, t] − f · A[r, t]) mod p
L11     append j to P; r ← r + 1
L12 return A, r, P
```

To solve $Ax \equiv b \pmod p$, run MOD-ELIM on $[A \mid b]$. If column $n$ is a pivot, there is no solution. Otherwise set the free variables to $0$ and read $x_{P[k]}$ from row $k$ of the last column. A consistent system of rank $r$ has exactly $p^{\,n - r}$ solutions, because the solutions are one solution plus the nullspace, a vector space of dimension $n - r$ over a field with $p$ elements. For the inverse, run it on $[A \mid I]$ as in Gauss-Jordan elimination. For the determinant, use the staircase loop and multiply the pivots, negating once for each swap.

**Correctness.** The proofs for [Gaussian elimination](/gaussian-elimination/) and [Gauss-Jordan elimination](/gauss-jordan-elimination/) use only the field axioms. With residues and $c = A[r, j]^{-1}$ in $\mathbb{F}_p$ they hold word for word.

**Cost.** The loop does the same number of field operations as over $\mathbb{Q}$: $O(mn \min(m, n))$, which is $n^3 + O(n^2)$ for the reduced form of a nonsingular $n \times n$ matrix and $2n^3/3 + O(n^2)$ for the staircase form. Add at most $\min(m, n)$ inversions, each $O(\log p)$ operations. Each operation on residues costs $O(\log^2 p)$ bit operations with schoolbook arithmetic, or $O(1)$ word operations when $p$ fits in a half word. So the bit cost is $O(n^3 \log^2 p)$ for an $n \times n$ matrix, independent of the size of the integers in the original problem. Compare $O(n^5 (b + \log n)^2)$ for elimination over $\mathbb{Q}$.

## Classic examples

**A system modulo 7.** Solve $2x + 3y + z \equiv 1$, $4x + y + 5z \equiv 2$, $x + 6y + 3z \equiv 3 \pmod 7$. The determinant is $-52 \equiv 4$, so there is one solution. The inverses modulo $7$ are $2^{-1} = 4$, $3^{-1} = 5$, $4^{-1} = 2$, $5^{-1} = 3$ and $6^{-1} = 6$.

| step | action | row 0 | row 1 | row 2 |
| --- | --- | --- | --- | --- |
| start | | 2 3 1 \| 1 | 4 1 5 \| 2 | 1 6 3 \| 3 |
| $j = 0$ | multiply row 0 by $2^{-1} = 4$; subtract $4 \cdot$ row 0 from row 1 and $1 \cdot$ row 0 from row 2 | 1 5 4 \| 4 | 0 2 3 \| 0 | 0 1 6 \| 6 |
| $j = 1$ | multiply row 1 by $4$; subtract $5 \cdot$ row 1 from row 0 and $1 \cdot$ row 1 from row 2 | 1 0 0 \| 4 | 0 1 5 \| 0 | 0 0 1 \| 6 |
| $j = 2$ | pivot is $1$; subtract $5 \cdot$ row 2 from row 1 | 1 0 0 \| 4 | 0 1 0 \| 5 | 0 0 1 \| 6 |

So $(x, y, z) = (4, 5, 6)$. Check: $8 + 15 + 6 = 29 \equiv 1$, $16 + 5 + 30 = 51 \equiv 2$ and $4 + 30 + 18 = 52 \equiv 3$.

**Counting solutions.** The system with rows $(1, 2, 3)$, $(2, 4, 6)$, $(1, 0, 1)$ and right side $(1, 2, 5)$ reduces modulo $7$ to rows $(1, 0, 1 \mid 5)$, $(0, 1, 1 \mid 5)$ and a zero row. The rank is $2$ and column $3$ is not a pivot, so there are $7^{3-2} = 7$ solutions, $(5 - z, 5 - z, z)$ for $z \in \mathbb{F}_7$. A brute-force search over the $343$ vectors finds the same $7$.

**Determinants by the Chinese remainder theorem.** For the integer matrix $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, the [Hadamard bound](/hadamard-bound/) gives $|\det M| \le \sqrt{5 \cdot 11 \cdot 17} < 31$. Elimination modulo $7$ and $11$ gives $\det M \equiv 4 \pmod 7$ and $\det M \equiv 7 \pmod{11}$. The Chinese remainder theorem gives the residue $18$ modulo $77$, and $77 > 2 \cdot 30$, so the symmetric residue $18$ is the determinant. This is the [multimodular determinant](/multimodular-determinant/) algorithm: for an $n \times n$ matrix with $b$-bit entries it needs $O(n(b + \log n) / \log p)$ primes, so with word-size primes the eliminations cost $O(n^4 (b + \log n))$ word operations in total, plus the cost of reducing the entries and of the Chinese remaindering (MCA Section 5.5).

**Rational solutions by lifting.** [Dixon's p-adic lifting](/dixon-p-adic-lifting/) inverts $\bar{A}$ once modulo a prime $p$ that does not divide $\det A$, and then uses that inverse to find the $p$-adic digits of the solution of $Ax = b$ one at a time. A final rational reconstruction gives the fractions. The one elimination modulo $p$ is the only cubic step.

**Systems over $\mathbb{F}_2$.** Modulo $2$, the only nonzero pivot is $1$, so line L7 does nothing, and subtraction is XOR. This is the setting of [linear systems modulo 2](/linear-system-modulo-2/), of [XOR constraints in SAT solvers](/xor-gaussian-elimination/), and of the matrix step of factoring algorithms such as the [quadratic sieve](/quadratic-sieve/). Packing rows into words gives [bitset Gaussian elimination](/bitset-gaussian-elimination/).

**Counting spanning trees modulo a prime.** By the [matrix-tree theorem](/matrix-tree-theorem/), the number of spanning trees is a determinant of a reduced Laplacian. When only the count modulo $p$ is asked, elimination modulo $p$ gives it with no large numbers.

## Variations

- **Choice of inverse.** The extended Euclidean algorithm costs $O(\log p)$ steps. Fermat's $c^{p-2}$ costs $O(\log p)$ multiplications and is shorter to write. Only $\min(m, n)$ inverses are needed, so the choice matters little.
- **Avoiding the inverse in the row update.** Scale the pivot row once (line L7) and use $f = A[i, j]$ as the multiplier, as in the template. The alternative, multiplying by $A[i, j] \cdot A[r, j]^{-1}$ in each row, needs the same single inverse per pivot.
- **Fast reduction.** For many operations modulo one $p$, [Montgomery multiplication](/montgomery-multiplication/) or [Barrett reduction](/barrett-reduction/) replace the division in "mod p" by multiplications. Another trick is lazy reduction: with $p < 2^{31}$ and unsigned 64-bit sums, several products $< 2^{62}$ can be added before one reduction.
- **Fraction-free elimination modulo $p$.** Multiplying rows by pivots in place of dividing ([Bareiss](/bareiss-algorithm/) style) avoids inverses entirely, at the cost of more multiplications. It is used when inversion is expensive, for example in a ring where it is not always possible.
- **Composite modulus.** Over $\mathbb{Z}/m\mathbb{Z}$ with $m$ composite, a pivot that is not a unit cannot be scaled to $1$. Either factor $m$, solve modulo each prime power, and combine by the Chinese remainder theorem, or use gcd row operations: for two rows with entries $u$ and $v$ in the pivot column, the [extended Euclidean algorithm](/extended-euclidean-algorithm/) gives $s, t$ with $su + tv = g = \gcd(u, v)$, and the unimodular $2 \times 2$ transformation with rows $(s, t)$ and $(-v/g, u/g)$ replaces the two entries by $g$ and $0$. Repeating this gives an echelon form, and Howell's canonical form makes it unique.
- **Random primes.** For an integer matrix, a prime chosen at random from a large set divides a fixed nonzero minor only with small probability, which gives Monte Carlo algorithms for the rank and for singularity tests.

## Pitfalls

- **A composite modulus.** Over $\mathbb{Z}/6\mathbb{Z}$, the matrix with rows $(2, 3)$ and $(3, 2)$ has $\det = -5 \equiv 1$, so it is invertible, and it is its own inverse: its square is $\begin{pmatrix} 13 & 12 \\ 12 & 13 \end{pmatrix} \equiv I$. But neither $2$ nor $3$ is a unit modulo $6$, so the template fails at the first pivot. Fermat's inverse $c^{m-2} \bmod m$ silently returns a wrong value for a composite $m$; the extended Euclidean algorithm at least reports $\gcd(c, m) \ne 1$.
- **Unlucky primes.** The rank modulo $p$ can be smaller than the rank over $\mathbb{Q}$: $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ has determinant $-2$, so it has rank $2$ over $\mathbb{Q}$ but rank $1$ modulo $2$. The system with rows $(2, 3, 1)$, $(4, 1, 5)$, $(1, 6, 2)$ has determinant $-42$ and a unique rational solution, but modulo $7$ it reduces to a pivot in the right-hand column and has no solution. A prime is unlucky for a nonsingular $A$ exactly when it divides $\det A$, and there are at most $\log_2 |\det A| \le n(b + \tfrac12 \log_2 n)$ such primes by the Hadamard bound. Modular algorithms must detect them, for example by checking the result or by comparing ranks over several primes.
- **Negative remainders.** In C, C++, Java and Go, `a % p` is negative for a negative `a`. Compute `(a - f * b) % p` as `(a + (p - f) * b) % p`, or add `p` after the subtraction.
- **Overflow.** A product of two residues needs $2 \lceil \log_2 p \rceil$ bits. For $p$ near $2^{62}$, 64-bit products overflow; use 128-bit products or Montgomery arithmetic.
- **Reducing the input.** Negative integer entries must be mapped to $\{0, \dots, p-1\}$ before the zero test on line L3, or an entry $\equiv 0$ that is stored as $p$ or $-p$ is taken as a pivot.
- **Recovering rationals.** A solution modulo $p$ is not the rational solution. It gives the rational solution only through lifting and rational reconstruction, with enough precision from the bound of [Cramer's rule](/cramers-rule/) and the Hadamard bound.

## Exercises

1. Show that a consistent system $Ax \equiv b \pmod p$ of rank $r$ in $n$ unknowns has exactly $p^{n-r}$ solutions. *Answer:* the solutions are $x_0 + N$, where $N$ is the nullspace of $\bar{A}$, of dimension $n - r$ by the [rank-nullity theorem](/rank-nullity-theorem/), so $|N| = p^{n - r}$.
2. Invert $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ modulo $5$. *Answer:* $\det \equiv -2 \equiv 3$ and $3^{-1} = 2$, so the inverse is $2 \cdot \begin{pmatrix} 4 & -2 \\ -3 & 1 \end{pmatrix} \equiv \begin{pmatrix} 3 & 1 \\ 4 & 2 \end{pmatrix}$.
3. Give a $2 \times 2$ integer matrix of rank $2$ over $\mathbb{Q}$ whose rank is $1$ modulo every prime $p \le 7$. *Answer:* $\begin{pmatrix} 1 & 0 \\ 0 & 210 \end{pmatrix}$, since $210 = 2 \cdot 3 \cdot 5 \cdot 7$.
4. Over $\mathbb{Z}/6\mathbb{Z}$, transform the column $(2, 3)^T$ to $(1, 0)^T$ with a unimodular $2 \times 2$ integer matrix. *Answer:* $\gcd(2, 3) = 1 = (-1) \cdot 2 + 1 \cdot 3$, so use the rows $(-1, 1)$ and $(-3, 2)$, with determinant $1$.

## References
