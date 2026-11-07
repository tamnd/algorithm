---
tag: DQVFXD
kind: abstract-type
slug: big-integer
name: Big integer
aliases:
- arbitrary-precision integer
- bignum
- multiprecision integer
area: algebra/integer-arithmetic
level: intro
summary: Abstract type for integers of unbounded size supporting arithmetic and comparison.
prereqs: [arbitrary-precision-arithmetic, division-with-remainder, floor-division]
see_also: [multiprecision-integer, integer-addition, integer-multiplication, integer-division, integer-overflow, twos-complement, sign-magnitude-representation, radix-conversion]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Chapter 1, Integer arithmetic (Section 1.1, the representation with a sign and n words; Sections 1.2 to 1.7, the operations and their costs)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Algorithms A, S, M and D on nonnegative n-place integers, and the treatment of signs)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 3.4, 'mod', the binary operation (the floor quotient and the remainder with the sign of the divisor)
  - url: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
    title: The Python Standard Library, Numeric types, int, float, complex
    locator: the notes on floor division, modulo and the bitwise operations on negative integers
  - paper: doi:10.4230/LIPIcs.ICALP.2019.10
    title: Peyman Afshani, Casper Benjamin Freksen, Lior Kamma and Kasper Green Larsen, Lower bounds for multiplication via network coding, ICALP 2019, LIPIcs 132
    locator: article 10, the main theorem (an Omega(n lg n) size bound for constant-degree circuits, under the conjecture of Li and Li)
---

A big integer is an abstract data type whose values are all the integers $\mathbb{Z}$, with no bound on their size, and whose operations are the exact arithmetic operations, comparison and conversion to and from text. It is the interface that [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/) offers to a program: a value behaves as a mathematical integer, and only the time and memory of an operation grow with its size. Python's `int`, Java's `BigInteger` and GMP's `mpz_t` are big integers. The usual implementation is a [multiprecision integer](/multiprecision-integer/), a sign and an array of limbs.

## In plain words

A normal integer type in a program has a fixed size. If a result is too large, it wraps around or the program fails. A big integer is a number type that never does this. You can add, multiply and divide numbers of any size, and the answer is always exact.

The type says what the operations do, and not how. Addition must give the true sum, division must give the true quotient and remainder, and a comparison must give the true order. A library is free to store the number in any way and to use any method, as long as the answers are right.

The price of this freedom is time. Small numbers are fast, but an operation on long numbers takes longer, and multiplication and division take longer than addition.

## Operations

A value $x$ of the type is an integer in $\mathbb{Z}$. We write $|x|$ for its absolute value and $\ell(x) = \lceil \log_\beta(|x| + 1) \rceil$ for its length in limbs of the base $\beta = 2^w$, so $\ell(0) = 0$. The costs in the last column are in limb operations on the [word RAM](/word-ram/) for operands of at most $n$ limbs. $M(n)$ is the cost of multiplying two $n$-limb numbers. The table follows the notation of [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/).

| operation | signature | what it returns | usual cost |
|---|---|---|---|
| `from-int` | $\text{from-int}(k) \to x$ | the value of a machine integer $k$ | $O(1)$ |
| `parse` | $\text{parse}(s, b) \to x$ | the integer written by the string $s$ in base $b$ | $O(M(n) \log n)$ |
| `to-string` | $\text{to-string}(x, b) \to s$ | the digits of $x$ in base $b$, with a sign | $O(M(n) \log n)$ |
| `sign` | $\text{sign}(x) \to \{-1, 0, 1\}$ | the sign of $x$ | $O(1)$ |
| `neg`, `abs` | $\text{neg}(x) \to y$ | $-x$, and $|x|$ | $O(1)$ in place, $O(n)$ for a copy |
| `compare` | $\text{compare}(x, y) \to \{-1, 0, 1\}$ | the sign of $x - y$ | $O(n)$ |
| `add`, `sub` | $\text{add}(x, y) \to z$ | $x + y$, and $x - y$ | $\Theta(n)$ |
| `mul` | $\text{mul}(x, y) \to z$ | $x y$ | $M(n)$ |
| `divmod` | $\text{divmod}(x, y) \to (q, r)$ | for $y \ne 0$: $q = \lfloor x / y \rfloor$ and $r = x - q y$ | $O(M(n))$ |
| `shift-left` | $\text{shl}(x, k) \to y$ | $x \cdot 2^k$ for $k \ge 0$ | $O(n + k/w)$ |
| `shift-right` | $\text{shr}(x, k) \to y$ | $\lfloor x / 2^k \rfloor$ for $k \ge 0$ | $O(n)$ |
| `and`, `or`, `xor`, `not` | $\text{and}(x, y) \to z$ | the bitwise result in infinite [two's complement](/twos-complement/) | $O(n)$ |
| `pow` | $\text{pow}(x, k) \to y$ | $x^k$ for $k \ge 0$ | $O(M(k n))$ |
| `gcd` | $\text{gcd}(x, y) \to g$ | the [greatest common divisor](/greatest-common-divisor/) $\ge 0$ | $O(M(n) \log n)$ |
| `isqrt` | $\text{isqrt}(x) \to s$ | for $x \ge 0$: $\lfloor \sqrt{x} \rfloor$ | $O(M(n))$ |
| `bit-length` | $\text{bitlen}(x) \to \mathbb{N}$ | the least $k \ge 0$ with $|x| < 2^k$ | $O(1)$ |

**Division conventions.** The table uses [floor division](/floor-division/), the rule of Python, Ruby and of Concrete Mathematics: the quotient rounds toward $-\infty$ and the remainder has the sign of the divisor. Java's `BigInteger.divide`, the C operators on machine integers and GMP's `mpz_tdiv_qr` truncate toward zero instead, and the remainder then has the sign of the dividend. GMP also has `mpz_fdiv_qr` for the floor rule and `mpz_cdiv_qr` for the ceiling rule. A program that moves between languages must check which rule it gets. The page [division with remainder](/division-with-remainder/) gives the Euclidean rule, in which the remainder is never negative.

**Bitwise operations.** For a negative $x$, the bits are those of the infinite two's complement form, in which $x = -1$ has all bits equal to 1. So $\text{not}(x) = -x - 1$ for each $x$, and $\text{and}(x, 2^k - 1) = x \bmod 2^k \ge 0$. Python and GMP's `mpz_and` follow this rule, even though they store the magnitude.

## Laws

Each implementation satisfies the following equations for all integers $x, y, z$ and all $k, j \ge 0$.

- **The ring laws.** $(\mathbb{Z}, +, \cdot, 0, 1)$ is a commutative ring: $x + y = y + x$, $(x + y) + z = x + (y + z)$, $x + 0 = x$, $x + (-x) = 0$, $xy = yx$, $(xy)z = x(yz)$, $1 \cdot x = x$, and $x(y + z) = xy + xz$. Also $x - y = x + (-y)$.
- **No zero divisors.** $xy = 0$ implies $x = 0$ or $y = 0$.
- **Order.** `compare` is a total order with $x \le y \Rightarrow x + z \le y + z$, and $x \le y$, $z > 0 \Rightarrow xz \le yz$.
- **Division.** For $y \ne 0$, $\text{divmod}(x, y) = (q, r)$ is the unique pair with $x = qy + r$ and $0 \le r < y$ when $y > 0$, $y < r \le 0$ when $y < 0$. In particular $\text{divmod}(x, 1) = (x, 0)$, and $\text{divmod}(x + ky, y) = (q + k, r)$ for each integer $k$.
- **Shifts.** $\text{shl}(x, k) = x \cdot 2^k$ and $\text{shr}(x, k) = \text{divmod}(x, 2^k)_1$, so $\text{shr}(\text{shl}(x, k), k) = x$ and $\text{shr}(\text{shr}(x, k), j) = \text{shr}(x, k + j)$. For $x < 0$, a right shift rounds toward $-\infty$: $\text{shr}(-1, 1) = -1$.
- **Round trip.** $\text{parse}(\text{to-string}(x, b), b) = x$ for each base $b \ge 2$, and $\text{to-string}$ has no leading zero digit, so the string of each value is unique.
- **Powers.** $\text{pow}(x, 0) = 1$ (also for $x = 0$) and $\text{pow}(x, k + 1) = \text{pow}(x, k) \cdot x$.
- **Square root.** For $x \ge 0$, $s = \text{isqrt}(x)$ satisfies $s^2 \le x < (s + 1)^2$.
- **Bit length.** For $x \ne 0$, $2^{\text{bitlen}(x) - 1} \le |x| < 2^{\text{bitlen}(x)}$, and $\text{bitlen}(0) = 0$.

**Examples.** In Python, `divmod(-7, 2)` is `(-4, 1)` and `divmod(7, -2)` is `(-4, -1)`, both as the floor rule says. In Java, `BigInteger.valueOf(-7).divideAndRemainder(BigInteger.valueOf(2))` gives $-3$ and $-1$, by truncation. Both satisfy $x = qy + r$; they differ in the range of $r$. Also `-7 >> 1` is $-4$ in Python, which is $\lfloor -7/2 \rfloor$, and `~5` is $-6$.

## Implementations

| implementation | representation | add | mul | divmod | notes |
|---|---|---|---|---|---|
| [multiprecision integer](/multiprecision-integer/), schoolbook | sign and $n$ limbs | $\Theta(n)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | the base of all others; [schoolbook multiplication](/schoolbook-multiplication/) and [long division](/long-division/) |
| the same, with [Karatsuba](/karatsuba-multiplication/) | sign and $n$ limbs | $\Theta(n)$ | $O(n^{\log_2 3})$ | $O(n^{\log_2 3})$ | CPython uses Karatsuba above a size cut-off |
| the same, with [Toom-Cook](/toom-cook-multiplication/) and FFT | sign and $n$ limbs | $\Theta(n)$ | $O(n \log n \log\log n)$ for the largest sizes | $O(M(n))$ | GMP chooses the method by size |
| [sign-magnitude](/sign-magnitude-representation/) with decimal limbs | limbs in base $10^k$ | $\Theta(n)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | `to-string` is $\Theta(n)$; used by some decimal libraries |
| [residue number system](/residue-number-system/) | residues modulo fixed primes | $\Theta(n)$ | $\Theta(n)$ | not direct | needs a known bound on the result; compare and divide are slow |

The fourth row trades a fast conversion to decimal for slower arithmetic, because carries in base $10^k$ need a division by a constant. The last row is not a full implementation of the type, because the residues do not show the size or the sign without a [Chinese remainder](/chinese-remainder-theorem/) reconstruction.

## Lower bounds

- **Linear operations.** Addition, subtraction and comparison of two $n$-limb values need $\Omega(n)$ time in each model in which an operation reads $O(1)$ limbs: if an algorithm does not read a limb of an operand, an adversary can change that limb, which changes the answer of a comparison and the matching limb of a sum. So the $\Theta(n)$ bounds of the table are tight.
- **Multiplication.** No lower bound better than $\Omega(n)$ is proved for multiplication in a general model such as the multitape Turing machine or Boolean circuits. Under a conjecture about network coding, Afshani, Freksen, Kamma and Larsen (2019) proved that Boolean circuits of bounded fan-in and fan-out for multiplication need $\Omega(N \log N)$ gates for $N$-bit inputs, which matches the upper bound of Harvey and van der Hoeven. The page [integer multiplication](/integer-multiplication/) states these results.
- **Division and roots.** Division with remainder and the integer square root are at least as hard as multiplication up to a constant factor: $xy = ((x + y)^2 - (x - y)^2)/4$ needs two squarings, and a squaring $x^2$ can be computed from reciprocals by $x^2 = 1/(1/x - 1/(x+1)) - x$ in enough precision. So $D(n) = \Theta(M(n))$, with $D(n) = O(M(n))$ from Newton's method.

## References
