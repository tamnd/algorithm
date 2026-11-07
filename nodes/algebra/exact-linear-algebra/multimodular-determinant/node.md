---
tag: BETBZR
kind: algorithm
slug: multimodular-determinant
name: Multimodular determinant
aliases: [modular determinant via Chinese remainder theorem, small primes modular determinant, modular determinant algorithm, CRT determinant]
area: algebra/exact-linear-algebra
level: advanced
summary: Computes an integer determinant by evaluating modulo many primes and reconstructing with the Chinese remainder theorem.
solves: [determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry, ℓ: the binary length of each prime}
  time: {worst: O(n^4 (b + log n) log(n b) + n^3 b (b + log n))}
  space: {extra: O(n^2 ℓ + n (b + log n))}
  field_operations: {worst: O(n^4 (b + log n) / ℓ)}
  bit_operations: {worst: O(n^4 (b + log n) log(n b) + n^3 b (b + log n))}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [determinant-gaussian-elimination, gaussian-elimination-modular, chinese-remainder-theorem, hadamard-bound]
see_also: [determinant-computation, bareiss-algorithm, dixon-p-adic-lifting, garner-algorithm, wiedemann-algorithm, berkowitz-algorithm, miller-rabin, subproduct-tree]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5, Section 5.5, Modular determinant computation (the big prime and small primes modular algorithms, the Hadamard bound on the number of primes, and their cost); Section 5.4, The Chinese remainder algorithm
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 2.2.3, Computing determinants (Gaussian elimination, the Gauss-Bareiss method, and the modular method with the Hadamard bound)
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22(103), 1968
    locator: pp. 565 to 578 (the fraction-free alternative, whose intermediate entries are minors of the input)
  - paper: "I. Borosh and A. S. Fraenkel, Exact solutions of linear equations with rational coefficients by congruence techniques, Mathematics of Computation 20(93), 1966"
    locator: pp. 107 to 112 (solving integer systems and computing determinants modulo several primes)
  - paper: "John Abbott, Manuel Bronstein and Thom Mulders, Fast deterministic computation of determinants of dense matrices, Proceedings of ISSAC 1999, ACM"
    locator: pp. 197 to 204 (a large divisor of the determinant from a linear solve, so fewer primes are needed, and early termination)
  - paper: doi:10.1016/j.jco.2005.04.002
    title: Arne Storjohann, The shifted number system for fast linear algebra on integer matrices, Journal of Complexity 21(4), 2005
    locator: pp. 609 to 650 (a Las Vegas determinant in about n^ω b bit operations, up to logarithmic factors)
---

The multimodular determinant computes $\det A$ for a square integer matrix $A$ without ever handling a large number inside the elimination. It runs [Gaussian elimination modulo a prime](/gaussian-elimination-modular/) for several word-size primes $p_1, p_2, \ldots$, gets $\det A \bmod p_i$ from each, and rebuilds $\det A$ with the [Chinese remainder theorem](/chinese-remainder-theorem/). The [Hadamard bound](/hadamard-bound/) $H$ says in advance how many primes are enough: once their product exceeds $2H$, the residue is the determinant. Each elimination works on numbers of one machine word, and the total cost is smaller by a factor of about $n$ than [elimination over $\mathbb{Q}$](/determinant-gaussian-elimination/) or the [Bareiss algorithm](/bareiss-algorithm/).

## In plain words

The determinant of a table of whole numbers is a whole number, perhaps a huge one. Computing it directly makes the numbers in the middle of the work grow large and slow.

Instead, compute the determinant's remainder after division by a small prime, which only needs arithmetic on small remainders. Do this for many different primes. A theorem says how big the determinant can possibly be, and once the product of the primes is more than twice that size, the remainders pin down the determinant uniquely, sign included. Putting the remainders back together is the Chinese remainder theorem, a standard and cheap step.

## The problem

**Notation.** $A = (a_{ij})$ is an $n \times n$ matrix over the integral domain $\mathbb{Z}$, with $|a_{ij}| < 2^b$, and $a_i$ is its row $i$. $H = \lfloor \prod_i \|a_i\|_2 \rfloor$ is the Hadamard bound in integer form, so $|\det A| \le H \le 2^{n (b + \frac12 \log_2 n)}$. The primes have $\ell$ binary digits each, so each is at least $2^{\ell - 1}$. Costs are given in two models: *field operations*, counting arithmetic operations in the fields $\mathbb{Z}/p\mathbb{Z}$, and *bit operations* with schoolbook integer arithmetic. A matrix over $\mathbb{Q}$ is first multiplied by a common denominator of its entries, which multiplies the determinant by its $n$-th power.

**Input.** The integer matrix $A$.

**Output.** The integer $\det A$.

## The algorithm

```pseudo id=main
MULTIMODULAR-DET(A)                    ▷ A is n × n over Z
L1  if n = 0 then return 1
L2  H ← ⌊ Π_i ‖a_i‖_2 ⌋                    ▷ integer square root of Π_i ‖a_i‖_2^2
L3  M ← 1; r ← 0; p ← the first prime of the list
L4  while M ≤ 2H do
L5      d ← det(A mod p) over Z/pZ, by elimination with row swaps
L6      r ← r + M · ((d − r) M^{−1} mod p); M ← M p        ▷ now r ≡ det A (mod M), 0 ≤ r < M
L7      p ← the next prime of the list
L8  if r > ⌊M/2⌋ then r ← r − M
L9  return r
```

Line L2 needs only integers: $\prod_i \|a_i\|_2^2$ is an integer, and its integer square root is $H$. Line L5 is ordinary [Gaussian elimination](/gaussian-elimination/) over the field $\mathbb{Z}/p\mathbb{Z}$, with the product of the pivots and a sign for each swap. Line L6 is one step of the incremental Chinese remainder algorithm (Garner's method): it keeps $r$ modulo $M$ and fixes it modulo the new prime. Line L8 picks the representative of $r$ modulo $M$ in the symmetric range, which recovers negative determinants. A zero row makes $H = 0$, so the loop does not run and the answer is $0$.

## Example

Take

$$A = \begin{pmatrix} 3 & 1 & 4 \\ 1 & 5 & 9 \\ 2 & 6 & 5 \end{pmatrix}, \qquad \det A = -90.$$

The squared row norms are $26$, $107$ and $65$, with product $180830$, so $H = \lfloor \sqrt{180830} \rfloor = 425$ and we need $M > 850$. With tiny primes for illustration, starting at $7$:

| step | $p$ | $d = \det A \bmod p$ | $t = (d - r) M^{-1} \bmod p$ | new $r$ | new $M$ |
|---|---|---|---|---|---|
| 1 | 7 | 1 | 1 | 1 | 7 |
| 2 | 11 | 9 | 9 | 64 | 77 |
| 3 | 13 | 1 | 11 | 911 | 1001 |

After three primes $M = 1001 > 850$. Since $911 > 500$, line L8 returns $911 - 1001 = -90$. In practice the primes have about 31 or 63 binary digits, and a $3 \times 3$ matrix like this needs only one.

## Correctness

The determinant is a polynomial with integer coefficients in the entries, and reduction modulo $p$ is a ring homomorphism, so $\det (A \bmod p) = \det A \bmod p$ for every prime $p$; there are no unlucky primes, unlike for gcds or for solving. Line L6 keeps the invariant $r \equiv \det A \pmod M$ and $0 \le r < M$ for the product $M$ of the primes used so far, because the primes are distinct. The loop stops because $M$ at least doubles at each step. At the end $M > 2H \ge 2 |\det A|$, and exactly one integer in the range $(-M/2, M/2]$ is congruent to $r$ modulo $M$; line L8 returns it, and $\det A$ is in this range. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Number of primes.** With primes of at least $2^{\ell - 1}$, $s$ primes give $M \ge 2^{s (\ell - 1)}$, so

$$s \le \Big\lfloor \frac{\log_2 H + 1}{\ell - 1} \Big\rfloor + 1, \qquad \log_2 H \le n \big(b + \tfrac12 \log_2 n\big).$$

So $s = O(n (b + \log n) / \ell)$. This bound is proved. With $\ell = 31$, a $100 \times 100$ matrix with 32-bit entries needs at most $\lceil (100 (32 + 3.33) + 1) / 30 \rceil = 118$ primes.

**Field operations.** Each elimination costs $\tfrac23 n^3 + O(n^2)$ operations in $\mathbb{Z}/p\mathbb{Z}$, so the total is $s (\tfrac23 n^3 + O(n^2)) = O(n^4 (b + \log n) / \ell)$. With fast elimination in $O(n^\omega)$ per prime, it is $O(n^{\omega + 1} (b + \log n) / \ell)$.

**Bit operations.** An operation modulo an $\ell$-digit prime costs $O(\ell^2)$, so the eliminations cost $O(n^4 (b + \log n) \ell)$. Reducing the $n^2$ entries of $b$ digits modulo $s$ primes costs $O(n^2 \cdot s \cdot b \ell) = O(n^3 b (b + \log n))$ schoolbook, and the Chinese remainder steps cost $O((s \ell)^2) = O(n^2 (b + \log n)^2)$. There are enough primes of $\ell = \Theta(\log (n b))$ digits by the prime number theorem, so the total is

$$O\big(n^4 (b + \log n) \log (n b) + n^3 b (b + \log n)\big).$$

These bounds are proved. For comparison, elimination over $\mathbb{Q}$ and the Bareiss algorithm do $\Theta(n^3)$ operations on integers of up to $n (b + \log n)$ digits, which is $O(n^5 (b + \log n)^2)$ schoolbook: the modular method saves a factor of about $n (b + \log n) / \log (n b)$. Reducing all entries with a [subproduct tree](/subproduct-tree/) and fast multiplication makes the reduction and reconstruction steps quasi-linear in their input and output sizes.

**Space.** One reduced copy of $A$, $n^2$ residues of $\ell$ digits, plus $r$ and $M$ with $O(n (b + \log n))$ digits.

**Observed behaviour.** The Hadamard bound is attained by Hadamard matrices, but it is pessimistic for random matrices. For a matrix with independent random $\pm 1$ entries the expected value of $(\det A)^2$ is $n!$, so $\log_2 |\det A|$ is typically about $\tfrac12 n \log_2 e \approx 0.72 n$ less than $\log_2 H = \tfrac12 n \log_2 n$. This is the motivation for early termination, below.

## Properties

- **Deterministic.** With a deterministic list of primes, such as consecutive primes above $2^{\ell - 1}$ found by a deterministic primality test, every run does the same work and the output is always correct.
- **Embarrassingly parallel.** The eliminations for different primes are independent.
- **No growth of numbers** inside the eliminations, so they run in machine words, with vector instructions or floating-point units.
- **Fixed cost.** The number of primes depends only on $H$, not on the actual size of $\det A$, unless early termination is used.

## Variants and improvements

- **Big prime version.** Use one prime $p > 2H$ and compute $\det A \bmod p$ directly. It is simpler but the arithmetic is on numbers of $n (b + \log n)$ digits, which costs as much as Bareiss up to logarithmic factors.
- **Early termination.** Stop when the reconstructed symmetric residue has not changed for $k$ more random primes. It is then correct with high probability, and the number of primes is about $\log_2 |\det A| / \ell$ instead of $\log_2 H / \ell$. It turns the algorithm into a Monte Carlo one, unless the bound is used as a final check.
- **Large divisor first.** Solving $A x = v$ for a random $v$ by [Dixon lifting](/dixon-p-adic-lifting/) gives the denominator of $x$, which is a divisor of $\det A$ and usually most of it. Then only $\det A$ divided by this divisor must be found by CRT, which needs few primes (Abbott, Bronstein and Mulders, 1999).
- **Fast elimination.** Each modular determinant in $O(n^\omega)$ through a fast LUP decomposition.
- **Asymptotically fast methods.** Eberly, Giesbrecht and Villard (2000) and Storjohann (2005) compute $\det A$ in about $n^\omega b$ bit operations, up to logarithmic factors, with Las Vegas algorithms; Storjohann's uses high-order lifting.
- **Characteristic polynomial and other invariants.** The same scheme computes the characteristic polynomial, minors, the adjugate and the [rank](/rank-computation/) (with a probabilistic choice of prime), each with its own size bound.

## When to use it

Use it for dense integer matrices of moderate to large size when an exact determinant is needed, for example in exact geometry predicates, lattice computations and combinatorics (counting spanning trees with the matrix tree theorem). It is the method of choice in most computer algebra systems for dense integer determinants, usually with early termination and a large divisor step. For very small matrices, Bareiss or cofactor expansion is simpler; for a sign alone, floating point with an error bound is often enough; for sparse matrices, use [Wiedemann's method](/wiedemann-algorithm/) modulo each prime.

## Pitfalls

- **Forgetting the sign.** The modulus must exceed $2H$, not $H$, and the residue must be taken in the symmetric range; otherwise negative determinants come out as large positive numbers.
- **Zero pivots modulo $p$.** A pivot can vanish modulo $p$ although it is nonzero over $\mathbb{Q}$, so the elimination modulo $p$ must swap rows; for example the pivot $7$ is zero modulo $7$.
- **Repeated primes.** The moduli must be pairwise coprime; using the same prime twice breaks the Chinese remainder step without any error message.
- **Computing $H$ in floating point.** Rounding can make the bound too small. Use the integer square root of the integer $\prod_i \|a_i\|_2^2$, or round up generously.
- **Rational input.** Clear denominators first and divide the result by the $n$-th power of the common denominator.

## Implementations

## History

Congruence techniques for exact linear algebra go back at least to the 1960s, with the modular solution of integer systems by Borosh and Fraenkel (1966) and the multistep fraction-free elimination of Bareiss (1968) as the main alternative. The modular determinant with the Hadamard bound became the standard dense method in computer algebra in the 1970s, alongside the modular gcd algorithms of the same period, and it is presented in this form in the textbooks of Cohen (1993) and von zur Gathen and Gerhard (1999). Abbott, Bronstein and Mulders (1999) reduced the number of primes with a divisor found by lifting, and Eberly, Giesbrecht and Villard (2000) and Storjohann (2005) brought the bit cost close to that of matrix multiplication.

## References
