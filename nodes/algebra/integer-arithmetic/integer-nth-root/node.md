---
tag: 1JFYHN
kind: problem
slug: integer-nth-root
name: Integer n-th root
aliases:
- floor k-th root
- integer k-th root
- iroot
area: algebra/integer-arithmetic
level: core
summary: Compute the largest integer whose k-th power does not exceed a given integer.
model: word-ram
complexity:
  vars: {n: the number of limbs of N, k: the root index, M: the cost M(j) of multiplying two integers of j limbs}
  time: {worst: O((k + log n) M(n))}
prereqs: [integer-square-root, binary-exponentiation]
see_also: [newton-integer-root, integer-square-root, digit-by-digit-square-root, binary-search, newton-raphson-method, logarithms]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.5.2, k-th root (Algorithm RootInt and the cost of k-th roots), and Section 1.5.3, Exact root (perfect powers)
  - paper: doi:10.1090/S0025-5718-98-00952-1
    title: Daniel J. Bernstein, Detecting perfect powers in essentially linear time, Mathematics of Computation 67(223), 1998
    locator: pp. 1253 to 1283 (k-th roots by Newton's method with increasing precision, and the test of all exponents k)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (Newton's method for roots and reciprocals at the cost of multiplication)
---

The integer $k$-th root of a nonnegative integer $N$ is $\lfloor N^{1/k} \rfloor$, the largest integer $s$ with $s^k \le N$. For $k = 2$ it is the [integer square root](/integer-square-root/). It is computed with integers only, because floating-point roots are inexact: in double precision, `int(1000 ** (1/3))` gives 9, not 10. The standard method is [Newton's method on integers](/newton-integer-root/), which for an $n$-limb $N$ and a fixed $k$ costs $O(M(n) \log n)$ limb operations at full precision and $O(M(n))$ with precision doubling, where $M(n)$ is the cost of an $n$-limb product. Integer roots for all $k$ up to $\log_2 N$ decide whether $N$ is a perfect power.

## In plain words

The cube root of 1000 is 10, since $10 \cdot 10 \cdot 10 = 1000$. The cube root of 999 is a little less than 10, and its integer cube root is 9: the biggest whole number whose cube is not more than 999.

For a $k$-th root the question is the same with $k$ factors instead of three. Computers cannot just take a decimal root and drop the fraction, because a decimal root of 1000 may come out as 9.999999 and drop to 9. So they compute with whole numbers: guess a number that is too big, improve it step by step, and stop when it no longer goes down.

## Definition

**Input.** Integers $N \ge 0$ and $k \ge 1$, with $N$ given as an array of $n$ limbs in radix $\beta = 2^w$.

**Output.** The integer $s = \lfloor N^{1/k} \rfloor$, the unique integer $s \ge 0$ with

$$s^k \le N < (s + 1)^k ,$$

and in the version with remainder also $r = N - s^k$, with $0 \le r < (s + 1)^k - s^k$.

**Size.** If $N$ has $B$ binary digits, then $s$ has $\lceil B / k \rceil$ binary digits; in particular $s = 1$ for $k \ge B$ and $N \ge 1$. So only $k < B$ is of interest.

**Cost model.** Word RAM with $w$-bit words; costs in limb operations, with $M(n)$ the cost of an $n$-limb product. Bounds are proved where stated; the speed of a method at a given size is observed.

## Variants

- **Square root.** The case $k = 2$, with its own faster methods; see [integer square root](/integer-square-root/).
- **Exact root.** Decide whether $N = a^k$ and find $a$. Often faster than the floor root, because the root can be computed modulo a power of two (from the low digits) and checked.
- **Perfect power detection.** Decide whether $N = a^k$ for some $k \ge 2$. Only prime $k \le \log_2 N$ need to be tested, since $a^{pq} = (a^q)^p$.
- **Ceiling root.** $\lceil N^{1/k} \rceil$, which is $s$ if $r = 0$ and $s + 1$ otherwise.
- **Real roots to $p$ places.** $\lfloor N^{1/k} 2^p \rfloor = \lfloor (N 2^{kp})^{1/k} \rfloor$, one integer root of a larger number.
- **Rational exponents.** $\lfloor N^{j/k} \rfloor = \lfloor (N^j)^{1/k} \rfloor$.

## Examples

All values were checked by script.

- $\lfloor 814507^{1/3} \rfloor = 93$, since $93^3 = 804357 \le 814507 < 830584 = 94^3$; and $\lfloor 814507^{1/5} \rfloor = 15$, since $15^5 = 759375$ and $16^5 = 1048576$.
- $\lfloor 1000^{1/3} \rfloor = 10$ and $\lfloor 999^{1/3} \rfloor = 9$.
- $\lfloor (2^{64} - 1)^{1/3} \rfloor = 2642245$, the largest cube root of a 64-bit word.
- $\lfloor (2^{64})^{1/64} \rfloor = 2$ and $\lfloor (2^{64} - 1)^{1/64} \rfloor = 1$: for $k$ near the length of $N$ the root is 1 or 2.
- **The floating-point trap.** In double precision, `1000 ** (1/3)` is $9.999999999999998$ and `64 ** (1/3)` is $3.9999999999999996$, so truncation gives 9 and 3. For $N = 10^{30}$, `int(N ** (1/3))` gives $9999999999$, one less than the true root $10^{10}$. The exponent $1/3$ is itself rounded, and the result has only 53 binary digits.

## Known algorithms

| method | cost in limb operations | notes |
|---|---|---|
| [Newton's method](/newton-integer-root/), full precision | $O((k + \log n) M(n))$ | $x \leftarrow \lfloor ((k-1)x + \lfloor N/x^{k-1} \rfloor)/k \rfloor$ from $x_0 \ge s$; stop when $x$ stops decreasing |
| Newton's method with precision doubling | $O(M(n))$ for fixed $k$ | Brent and Zimmermann, Algorithm RootInt; Bernstein's perfect power test |
| Binary search on $s$ | $O(\lceil B/k \rceil \, M(n))$ | each step a $k$-th power by [binary exponentiation](/binary-exponentiation/); simple, used for small $N$ |
| Digit by digit | $\Theta(k n^2)$ for fixed $k$ | the paper method, generalizing the [digit-by-digit square root](/digit-by-digit-square-root/) |
| Floating point, then correct | $O(1)$ for one word | a float estimate, then adjust while $s^k > N$ or $(s+1)^k \le N$ |

The Newton step count has two phases. Far from the root, a step multiplies $x$ by about $(k - 1)/k$, so the start of the right binary length (at most twice the root) needs $O(k)$ steps to get close; near the root, the number of correct digits doubles in each step. A floating-point start removes most of the first phase.

## Bounds

- **Upper bound.** $O(M(n))$ for fixed $k$, by Newton's method with precision doubling, and $O(M(n) \log n)$ at full precision. With $M(n) = O(n \log n)$ in the bit complexity model (Harvey and van der Hoeven, 2019, published 2021), a $k$-th root of a $B$-digit number takes $O(B \log B)$ bit operations for fixed $k$.
- **All exponents.** Bernstein (1998) decides whether $N$ is a perfect power, testing all $k \le \log_2 N$, in time essentially linear in the length of $N$.
- **Lower bound.** $\Omega(n)$ to read $N$; nothing better is known.

## Reductions

- **To powering and division**, by Newton's method: each step computes $x^{k-1}$ and one quotient.
- **To powering only**, by binary search: each step is one comparison $m^k \le N$.
- **The square root** is the case $k = 2$; methods for it, such as the Karatsuba square root, do not carry over directly to larger $k$.
- **Composite exponents.** $\lfloor N^{1/(ab)} \rfloor = \lfloor \lfloor N^{1/a} \rfloor^{1/b} \rfloor$, so a root of composite index is two roots of smaller index. This identity holds for floor roots of integers.

## Applications

- **Perfect power tests** in factoring: a number to be factored is first checked for being a perfect power, because many factoring methods fail on $a^k$. The AKS primality test starts with this step.
- **Bounds in number theory**, such as the largest $a$ with $a^k \le N$ in counting perfect powers below $N$.
- **Geometry and cryptography**: exact cube roots for small-exponent RSA attacks, where a message $m$ with $m^3 < N$ is recovered as the integer cube root of the ciphertext.
- **Exact arithmetic** in computer algebra, where roots of integers must be exact or certified.

## References
