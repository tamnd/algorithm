---
tag: YG36BM
kind: algorithm
slug: dixon-p-adic-lifting
name: Dixon p-adic lifting
aliases:
- Dixon's algorithm
- p-adic linear system solving
- Hensel lifting for linear systems
area: algebra/exact-linear-algebra
level: research
summary: Solves an integer linear system by lifting a solution modulo a prime power to a rational solution.
solves: [linear-system-solving]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of A and b, k: the number of p-adic digits}
  time: {worst: O(n^3 (b + log n)^2)}
  space: {extra: O(n^2 (b + log n))}
  field_operations: {worst: O(n^3 + k n^2)}
  bit_operations: {worst: O(n^3 (b + log n)^2)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [cramers-rule, hadamard-bound, gaussian-elimination-modular, extended-euclidean-algorithm]
see_also: [hensel-lifting, multimodular-determinant, bareiss-algorithm, wiedemann-algorithm, linear-diophantine-system, matrix-inversion, chinese-remainder-theorem, determinant-computation]
sources:
  - paper: doi:10.1007/BF01459082
    title: John D. Dixon, Exact solution of linear equations using p-adic expansions, Numerische Mathematik 40, 1982
    locator: pp. 137 to 141 (the lifting with one inverse modulo p, and the cost O(n^3 log^2 n) for bounded entries)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.10, Rational number reconstruction (the Euclidean algorithm stopped halfway, and uniqueness when 2ND < m)
  - paper: "Robert T. Moenck and John H. Carter, Approximate algorithms to derive exact solutions to systems of linear equations, EUROSAM 1979, Lecture Notes in Computer Science 72"
    locator: pp. 65 to 73 (p-adic approximation of the solution of an integer system)
  - paper: "Thom Mulders and Arne Storjohann, Certified dense linear system solving, Journal of Symbolic Computation 37(4), 2004"
    locator: pp. 485 to 510 (Dixon lifting for singular and rectangular systems, with certificates of inconsistency)
  - paper: "Arne Storjohann, The shifted number system for fast linear algebra on integer matrices, Journal of Complexity 21(4), 2005"
    locator: pp. 609 to 650 (high-order lifting, a nonsingular system in about n^ω b bit operations)
---

Dixon's algorithm solves a nonsingular integer system $Ax = b$ exactly, without fractions in the main loop. It inverts $A$ once modulo a small prime $p$, then computes the $p$-adic digits of the solution one at a time, each from the previous remainder, with integers of the size of the input. After enough digits it turns the residue modulo $p^k$ back into fractions by rational reconstruction, a halted Euclidean algorithm. The cost is $O(n^3 (b + \log n)^2)$ bit operations, a factor $n$ less than modular or fraction-free elimination for the same task, and it is the standard method for dense integer and rational systems.

Notation: $A$ is an $n \times n$ matrix over $\mathbb{Z}$ with columns $a_1, \dots, a_n$, $b \in \mathbb{Z}^n$, and $b$ also stands for the maximum binary length of an entry of $A$ and of the vector $b$ when it appears in a cost. $\|v\|$ is the Euclidean norm, $p$ is a prime that fits in a machine word, and $\omega$ is the exponent of matrix multiplication. Field operations are operations in $\mathbb{Z}/p\mathbb{Z}$. Bit costs assume schoolbook integer arithmetic.

## In plain words

To solve a system of equations with whole-number coefficients exactly, the method first solves it in a tiny world where every number is replaced by its remainder after division by a small prime. That gives the last digit of the answer, written in base p. Subtracting what is already known and dividing by p leaves a new system of the same kind, which gives the next digit, using the same inverse again. After enough digits, a short Euclid-style computation turns the long number back into an exact fraction.

## The problem

Input: an $n \times n$ integer matrix $A$ and a vector $b \in \mathbb{Z}^n$. Output: the unique $x \in \mathbb{Q}^n$ with $Ax = b$ if $\det A \ne 0$, and the answer NONE if $A$ is singular. Rational inputs reduce to this case after clearing denominators row by row. The cost of interest is the number of bit operations as a function of $n$ and $b$.

The size of the answer is known in advance. By [Cramer's rule](/cramers-rule/), $x_j = \det A_j(b) / \det A$, and by the [Hadamard bound](/hadamard-bound/) the numerators and the denominator have absolute value below

$$
N = \Big\lfloor \|b\| \prod_j \|a_j\| \Big\rfloor + 1, \qquad D = \Big\lfloor \prod_j \|a_j\| \Big\rfloor + 1,
$$

which have $O(n(b + \log n))$ bits. The algorithm computes $x$ modulo a power $p^k > 2ND$, which determines it.

## The algorithm

```pseudo id=main
DIXON(A, b)                                  ▷ A is n × n over Z, b ∈ Z^n
L1  choose a prime p with p ∤ det A, and C ← A^{-1} mod p; if none exists, return NONE
L2  N ← ⌊‖b‖ ∏_j ‖a_j‖⌋ + 1; D ← ⌊∏_j ‖a_j‖⌋ + 1
L3  k ← the least integer with p^k > 2 N D
L4  r ← b; x̄ ← 0
L5  for i ← 0 to k − 1 do
L6      y ← C r mod p                        ▷ entries in [0, p)
L7      x̄ ← x̄ + y · p^i
L8      r ← (r − A y) / p                     ▷ exact division over Z
L9  for j ← 1 to n do
L10     x_j ← RATIONAL-RECONSTRUCTION(x̄_j, p^k, N, D)
L11 return x
```

Line L1 computes $C$ by [Gauss-Jordan elimination modulo p](/gaussian-elimination-modular/). If $p$ divides $\det A$, the elimination finds no pivot and the next prime is tried. The implementation tries primes downward from $2^{31} - 1$, and returns NONE once the product of the failed primes exceeds $D$, because then $\det A$, which is smaller than $D$ in absolute value, is divisible by a larger number and must be $0$.

Line L8 divides exactly: $y \equiv C r$ means $A y \equiv r \pmod p$. RATIONAL-RECONSTRUCTION$(u, m, N, D)$ runs the [extended Euclidean algorithm](/extended-euclidean-algorithm/) on $m$ and $u$, keeping the remainders $r_i$ and the cofactors $t_i$ with $r_i \equiv t_i u \pmod m$, and stops at the first remainder $r_i \le N$. It returns $r_i / t_i$ if $|t_i| \le D$, and fails otherwise.

## Example

Take $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, $b = (1, 2, 3)$ and $p = 7$. Here $\det M = 18$, which $7$ does not divide, and

$$
C = M^{-1} \bmod 7 = \begin{pmatrix} 1 & 6 & 2 \\ 6 & 2 & 3 \\ 2 & 3 & 3 \end{pmatrix}.
$$

The squared column norms are $5$, $11$ and $17$, with product $935$, and $\|b\|^2 = 14$, so line L2 gives $D = \lfloor \sqrt{935} \rfloor + 1 = 31$ and $N = \lfloor \sqrt{13090} \rfloor + 1 = 115$. Then $2ND = 7130$, and $k = 5$ since $7^4 = 2401 < 7130 < 16807 = 7^5$.

| $i$ | $y$ | $\bar{x}$ | new $r$ |
| --- | --- | --- | --- |
| 0 | (5, 5, 3) | (5, 5, 3) | (−2, −3, −2) |
| 1 | (4, 4, 2) | (33, 33, 17) | (−2, −3, −2) |
| 2 | (4, 4, 2) | (229, 229, 115) | (−2, −3, −2) |
| 3 | (4, 4, 2) | (1601, 1601, 801) | (−2, −3, −2) |
| 4 | (4, 4, 2) | (11205, 11205, 5603) | (−2, −3, −2) |

In step $0$, $r = b = (1, 2, 3)$, $C r = (19, 19, 17) \equiv (5, 5, 3)$, and $M y = (15, 23, 17)$, so the new remainder is $((1, 2, 3) - (15, 23, 17)) / 7 = (-2, -3, -2)$. From then on the remainder repeats, so the digits repeat, as for a fraction in any base.

Reconstruction modulo $m = 16807$: for $u = 11205$, the Euclidean algorithm gives the pairs $(r_i, t_i) = (16807, 0), (11205, 1), (5602, -1), (1, 3)$, and stops at $r = 1 \le 115$ with $t = 3 \le 31$, so $x_1 = 1/3$. The same holds for $x_2$. For $u = 5603$ it gives $(5603, 1), (5601, -2), (2, 3)$, so $x_3 = 2/3$. Indeed $M (1/3, 1/3, 2/3)^T = (1, 2, 3)^T$. The implementation's tests check this run.

## Correctness

After step $i$, the digits found so far satisfy $A \bar{x} + p^{i+1} r = b$. This holds at the start with $\bar{x} = 0$ and $r = b$, and step $i$ keeps it because it adds $p^i A y$ to the first term and removes $p^i (A y)$ from the second. So at the end $A \bar{x} \equiv b \pmod{p^k}$, and since $A$ is invertible modulo $p$, $\bar{x}$ is the residue of the true solution $x = s_j / t_j$, with $s_j \equiv t_j \bar{x}_j \pmod{p^k}$, $|s_j| < N$ and $0 < t_j < D$. Two fractions in this range that agree modulo $p^k$ satisfy $|s t' - s' t| \le 2ND < p^k$, so they are equal. The halted Euclidean algorithm finds this fraction: its remainders are the smallest values of $|\sigma p^k + t u|$ for cofactors $|t|$ up to each bound, so it reaches a remainder at most $N$ before its cofactor passes $D$. The [full proof](proofs/correctness.md) gives both lemmas and the test for singular matrices.

## Complexity

**Field operations.** Line L1 costs $O(n^3)$ operations modulo $p$ for each prime tried. Each lifting step is two matrix-vector products, $O(n^2)$ operations. With $k = \lceil \log_p(2ND) \rceil = O(n (b + \log n) / \log p)$ steps, the total is $O(n^3 + k n^2)$, which is $O(n^3)$ word operations for bounded $b$ and a word-size $p$.

**Bit operations.** The remainders stay small: if every entry of $r$ is at most $R = \max(\|b\|_\infty, n \max |a_{ij}|)$ in absolute value, then the new entries are at most $(R + n \max|a_{ij}| (p - 1)) / p \le R$. So each step multiplies numbers of $O(b + \log n)$ bits by numbers of $O(\log p)$ bits, $O(n^2)$ times, which costs $O(n^2 (b + \log n) \log p)$. Over the $k$ steps this is $O(n^3 (b + \log n)^2)$. Building $\bar{x}$ adds $O(n k^2 \log^2 p)$, and the $n$ reconstructions on numbers of $O(n(b + \log n))$ bits cost $O(n^2 (b + \log n)^2)$ each. All three terms are $O(n^3 (b + \log n)^2)$. This bound is proved, given a prime $p$ with $p \nmid \det A$ on the first try. At most $\log_2 D / 30 = O(n (b + \log n))$ primes above $2^{30}$ divide a nonzero $\det A$, so a prime chosen at random from a large enough set of word-size primes works with high probability, while a fixed order of primes can meet the bad ones first. For a singular $A$, the test of line L1 tries $O(n (b + \log n))$ primes, at $O(n^3)$ each.

For comparison, fraction-free elimination by the [Bareiss algorithm](/bareiss-algorithm/) costs $O(n^5 (b + \log n)^2)$ bit operations with schoolbook arithmetic, and a multimodular solver with the [Chinese remainder theorem](/chinese-remainder-theorem/) costs $O(n^4 (b + \log n))$, since it needs $O(n (b + \log n))$ primes with an $O(n^3)$ elimination each. Dixon needs one elimination and then only matrix-vector products. In a run of the implementation on random $40 \times 40$ systems with $21$-bit entries, Dixon took about $0.07$ s and elimination with Python fractions about $0.3$ s, for denominators of $841$ bits. These timings are observations on one machine, not bounds.

**Space.** The inverse $C$ takes $n^2$ words, $A$ takes $O(n^2 b)$, and $\bar{x}$ grows to $n$ numbers of $O(n(b + \log n))$ bits, so the space is $O(n^2 (b + \log n))$.

## Properties

- **One inverse, many digits.** The only cubic work is the inverse modulo $p$. All later work is matrix-vector products with $C$ and $A$, so the method suits several right-hand sides and matrices with fast products.
- **No intermediate growth.** The remainders $r$ stay as small as the input, unlike the entries of elimination over $\mathbb{Q}$, which grow to the size of minors.
- **Exact output.** The result is the exact rational solution in lowest terms, with the common denominator a divisor of $\det A$.
- **Deterministic** with a fixed sequence of primes. The cost bound with high probability needs a random prime.
- **Not in place.** It stores $C$, $A$, $r$ and $\bar{x}$.

## Variants and improvements

- **Early termination.** The Hadamard bounds are often far from the true size. One can try rational reconstruction every few steps and stop when the result satisfies $A x = b$, which saves much of the lifting on typical inputs. This is a heuristic speedup with a final exact check.
- **Matrix lifting.** Storing $C$ and lifting a block of right-hand sides at once turns the matrix-vector products into matrix-matrix products, so fast [matrix multiplication](/matrix-multiplication-exponent/) applies.
- **High-order lifting.** Storjohann's shifted number system lifts many digits at once and solves a nonsingular system in about $n^\omega b$ bit operations up to logarithmic factors.
- **Singular and rectangular systems.** Mulders and Storjohann extend the method to find a solution of a consistent system, or a certificate that it is inconsistent, from a random full-rank minor.
- **Sparse and structured matrices.** If $A$ is sparse, $C r \bmod p$ can be computed by the [Wiedemann algorithm](/wiedemann-algorithm/) instead of a stored inverse, which gives a lifting solver for sparse integer systems.
- **Integer solutions.** Diophantine solvers for [linear Diophantine systems](/linear-diophantine-system/) combine several rational solutions with different denominators to find an integer solution; see also the [Hermite normal form](/hermite-normal-form/).
- **Polynomial systems.** The same lifting with an irreducible polynomial in place of $p$ solves systems over $K[x]$, with rational function reconstruction at the end. It is the linear case of [Hensel lifting](/hensel-lifting/).

## When to use it

Use Dixon lifting for a dense nonsingular system with integer or rational entries when the exact solution is needed, for example in computer algebra, exact optimization, or as the inner step of determinant, Smith form and Diophantine algorithms. For small systems, [Bareiss](/bareiss-algorithm/) or elimination over $\mathbb{Q}$ is simpler. For very large sparse systems, combine the lifting with a black-box solver.

## Pitfalls

- **An unlucky prime.** If $p \mid \det A$, the inverse modulo $p$ does not exist. The code must detect this and try another prime, not fail.
- **Too few digits.** With $p^k \le 2ND$ the reconstruction may return a wrong fraction or fail. Compute $k$ from proved bounds, or check $A x = b$ at the end.
- **Wrong stopping rule in reconstruction.** The Euclidean algorithm must stop at the first remainder at most $N$, not at the last nonzero remainder, and the cofactor must be checked against $D$.
- **Signs.** The cofactor $t_i$ can be negative; normalize the fraction so the denominator is positive.
- **Inexact division.** Line L8 must divide $r - A y$, with $y$ reduced to $[0, p)$ and computed from the current $r$. A remainder from Python's `%` on negative numbers is fine, but a C remainder can be negative and needs a fix.
- **Rational inputs.** Clearing denominators row by row changes $b$ too; the bounds must be computed from the scaled integer system.

## Implementations

## History

Robert Moenck and John Carter described $p$-adic approximation for linear systems in 1979. John Dixon gave the algorithm with one inverse modulo $p$ and a full cost analysis in 1982, and showed it was faster than the multimodular method by a factor of about $n$. Rational reconstruction by the halted Euclidean algorithm goes back to Paul Wang's work on $p$-adic methods in 1981. Later work extended the method to singular and sparse systems and, with Storjohann's high-order lifting, brought the cost close to that of matrix multiplication.

## References
