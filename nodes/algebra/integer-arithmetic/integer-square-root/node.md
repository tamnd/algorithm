---
tag: J24NNS
kind: problem
slug: integer-square-root
name: Integer square root
aliases:
- floor square root
- isqrt
- integer square root with remainder
area: algebra/integer-arithmetic
level: core
summary: Compute the largest integer whose square does not exceed a given integer.
model: word-ram
complexity:
  vars: {n: the number of limbs of N, M: the cost M(k) of multiplying two integers of k limbs}
  time: {worst: O(M(n))}
prereqs: [integer-multiplication, floor-division, binary-search]
see_also: [newton-integer-root, digit-by-digit-square-root, integer-nth-root, newton-square-root, modular-square-root, fermat-factorization, trial-division, continued-fraction]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.5.1, Square root (Algorithm SqrtInt by Newton's method, and Algorithm SqrtRem, the Karatsuba square root, with cost O(M(n)))
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (division and square roots reduce to multiplication by Newton's method), and the answer to exercise 4.3.1 on integer square roots
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 21, Square-rooting methods (the pencil-and-paper method, restoring shift and subtract square roots, and convergence methods)
---

The integer square root of a nonnegative integer $N$ is $\lfloor \sqrt{N} \rfloor$, the largest integer $s$ with $s^2 \le N$. It is computed with integers only, without floating point, and often together with the remainder $r = N - s^2$. For an $n$-limb $N$ it can be found in $O(M(n))$ limb operations on the [word RAM](/word-ram/), where $M(n)$ is the cost of multiplying two $n$-limb numbers, so a square root costs a constant number of multiplications. The basic methods are [Newton's method](/newton-integer-root/), [digit-by-digit extraction](/digit-by-digit-square-root/) and binary search. Integer square roots appear in factoring, in primality tests and sieves, and wherever a bound $\sqrt{N}$ must be exact.

## In plain words

The square root of 20 is about 4.47. The integer square root drops the part after the point and keeps 4: the biggest whole number whose square is not more than 20, since $4 \cdot 4 = 16$ is not more than 20, but $5 \cdot 5 = 25$ is.

For small numbers a calculator gives the answer. For numbers with hundreds or thousands of digits it does not, because it keeps only about 16 digits and can round the last one the wrong way. So programs compute the answer with whole numbers only, guessing and correcting. A good method is about as fast as a few multiplications of numbers that size.

## Definition

**Input.** An integer $N \ge 0$, given as an array of $n$ limbs in radix $\beta = 2^w$.

**Output.** The integer $s = \lfloor \sqrt{N} \rfloor$, the unique integer $s \ge 0$ with

$$s^2 \le N < (s + 1)^2 ,$$

and, in the version *with remainder*, also $r = N - s^2$. The remainder satisfies $0 \le r \le 2s$, since $N \le (s + 1)^2 - 1 = s^2 + 2s$. Conversely, a pair $(s, r)$ with $N = s^2 + r$ and $0 \le r \le 2s$ determines $s = \lfloor \sqrt{N} \rfloor$.

**Size.** If $N$ has $N_b$ binary digits, then $s$ has $\lceil N_b / 2 \rceil$ binary digits, so $s$ has about $n/2$ limbs. This follows from $2^{N_b - 1} \le N < 2^{N_b}$.

**Cost model.** Word RAM with $w$-bit words, costs in limb operations, and $M(n)$ for the cost of an $n$-limb product. The bound $O(M(n))$ is proved; the speed of a method at a given size is observed.

## Variants

- **Ceiling root.** $\lceil \sqrt{N} \rceil$, which is $s$ if $r = 0$ and $s + 1$ otherwise.
- **Perfect square test.** Decide whether $N = s^2$, that is, whether $r = 0$. Fast filters by residues modulo small numbers (a square is $0, 1, 4$ or $9$ modulo 16) reject most non-squares before the root is computed.
- **The $k$-th root.** $\lfloor N^{1/k} \rfloor$; see [integer $k$-th root](/integer-nth-root/).
- **Root of a quotient.** $\lfloor \sqrt{N / D} \rfloor$ or $\lfloor \sqrt{N} \cdot 2^p \rfloor$, the real square root to $p$ binary places, which is $\lfloor \sqrt{N 4^p} \rfloor$.
- **Correctly rounded square root** of a floating-point number, as required by IEEE 754; this is the same problem on the significand.
- **Modular square root.** Find $x$ with $x^2 \equiv a \pmod p$; a different problem, see [modular square root](/modular-square-root/).

## Examples

All values were checked by script.

- $\lfloor \sqrt{0} \rfloor = 0$, $\lfloor \sqrt{1} \rfloor = 1$, $\lfloor \sqrt{2} \rfloor = 1$, $\lfloor \sqrt{15} \rfloor = 3$, $\lfloor \sqrt{16} \rfloor = 4$.
- $\lfloor \sqrt{814507} \rfloor = 902$ with remainder $903$: $902^2 = 813604$, and $903 \le 2 \cdot 902$.
- $\lfloor \sqrt{10^{12}} \rfloor = 10^6$, a perfect square with $r = 0$.
- $\lfloor \sqrt{2^{128} - 1} \rfloor = 2^{64} - 1$, the largest value whose root fits in a 64-bit word.
- **The floating-point trap.** For $N = 4503599761588224 = 67108865^2 - 1$, the true root is $67108864$, but `int(sqrt(N))` in double precision gives $67108865$: $N$ has 53 binary digits, and the double nearest to $\sqrt{N}$ is $67108865$. It is the smallest $s$ with $\lfloor \texttt{sqrt}(s^2 - 1) \rfloor \ne s - 1$: below $2^{26}$ the gap between $\sqrt{s^2 - 1}$ and $s$ is more than half a unit in the last place, and a search from $2^{26} - 10$ found this one first.

## Known algorithms

| method | cost in limb operations | notes |
|---|---|---|
| [Newton's method](/newton-integer-root/) with full precision | $O(M(n) \log n)$ | $x \leftarrow \lfloor (x + \lfloor N/x \rfloor)/2 \rfloor$ from any $x_0 \ge \sqrt{N}$; quadratic convergence |
| Newton's method with precision doubling | $O(M(n))$ | each step at twice the precision of the last; Brent and Zimmermann, Section 1.5.1 |
| Karatsuba square root (SqrtRem) | $O(M(n))$ | recursive, root and remainder of the top half, then one division; used in GMP |
| [Digit-by-digit](/digit-by-digit-square-root/) | $\Theta(n^2)$ | the pencil-and-paper method, one root digit at a time; also the restoring and non-restoring hardware forms |
| Binary search on $s$ | $O(n \, M(n))$ | about $nw/2$ steps of one squaring each; simple but slow |
| Floating point, then correct | $O(1)$ for one word | `sqrt` in double precision, then adjust by $\pm 1$; only for $N < 2^{52}$ or with care |

Newton's method on integers starts at any $x_0 \ge \lfloor \sqrt{N} \rfloor$ and stops when the sequence stops decreasing; the last value is the root. With $x_0$ of the right binary length, it takes $O(\log n)$ steps, and the step count is at most about $\log_2 (N_b)$ plus a constant.

## Bounds

- **Upper bound.** $O(M(n))$ limb operations: by Newton's method with precision doubling, the costs of the steps form a geometric series dominated by the last, which costs a constant number of $n$-limb products and divisions, and division costs $O(M(n))$ by [Newton-Raphson division](/newton-raphson-division/). With the current best bound $M(n) = O(n \log n)$ in the bit complexity model (Harvey and van der Hoeven, 2019, published 2021), an integer square root of $N_b$ binary digits takes $O(N_b \log N_b)$ bit operations.
- **Lower bound.** $\Omega(n)$, to read the input. No better lower bound is known in general.
- **Equivalence with multiplication.** Squaring reduces to square roots up to constant factors, so the problems have the same complexity up to a constant; Alt proved such an equivalence in 1979. In the other direction, multiplication reduces to squaring by $ab = ((a + b)^2 - (a - b)^2)/4$.

## Reductions

- **To multiplication and division**, by Newton's method: each step is a division $\lfloor N / x \rfloor$, an addition and a shift. See [Newton's method for integer roots](/newton-integer-root/).
- **To a smaller square root**, in the Karatsuba square root: from the root $s'$ and remainder of the top half of $N$, one division gives the next $n/4$ limbs of the root, and one squaring corrects the remainder.
- **To $k$-th roots.** The square root is the case $k = 2$ of the [integer $k$-th root](/integer-nth-root/).
- **From real square roots.** $\lfloor \sqrt{N} \cdot 2^p \rfloor = \lfloor \sqrt{N \cdot 4^p} \rfloor$, so a fixed-point square root to $p$ places is one integer square root.

## Applications

- **Factoring.** [Fermat's method](/fermat-factorization/) tests whether $\lceil \sqrt{N} \rceil^2 - N, (\lceil \sqrt{N} \rceil + 1)^2 - N, \ldots$ is a square, and Lehman's method, Hart's one-line method and [SQUFOF](/shanks-squfof/) all use exact square roots and square tests.
- **Bounds for search.** [Trial division](/trial-division/) and the [sieve of Eratosthenes](/sieve-of-eratosthenes/) stop at $\lfloor \sqrt{N} \rfloor$; an error of one in the bound misses a factor or does extra work.
- **Continued fractions** of $\sqrt{N}$, used for Pell equations and in the continued fraction factoring method, start from $\lfloor \sqrt{N} \rfloor$; see [continued fraction](/continued-fraction/).
- **Perfect powers.** A test whether $N = a^k$ for some $k \ge 2$ uses integer roots for each prime $k \le \log_2 N$.
- **Libraries.** Python has `math.isqrt` (since version 3.8) and GMP has `mpz_sqrt` and `mpz_sqrtrem`.

## References
