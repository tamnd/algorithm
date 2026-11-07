---
tag: P5JFYQ
kind: definition
slug: radix
name: Radix (base)
aliases:
- base
- number base
area: algebra/integer-arithmetic
level: intro
summary: The integer base b >= 2 whose powers weight the digits of a positional representation.
prereqs: [division-with-remainder, logarithms]
see_also: [positional-number-system, radix-conversion, multiprecision-integer, balanced-ternary, signed-digit-representation, redundant-number-system]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (the radix, the digits, mixed radices, negative and complex bases)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.1, Representation of integers (the word base beta = 2^w and the choice of the base)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 1, Numbers and arithmetic (fixed-radix positional number systems and radix conversion)
---

The radix, or base, of a [positional number system](/positional-number-system/) is the integer $b \ge 2$ whose powers $1, b, b^2, \ldots$ are the weights of the digit positions. With the standard digits $0, 1, \ldots, b - 1$, each nonnegative integer has exactly one representation without leading zeros, and the number of digits of $N \ge 1$ is $\lfloor \log_b N \rfloor + 1$. Hardware uses $b = 2$, people use $b = 10$, and multiple-precision libraries use a large power of two $\beta = 2^w$, so that one digit, called a limb, fills one machine word.

## Definition

A **radix** is an integer $b \ge 2$. The **standard digit set** of radix $b$ is $D_b = \{0, 1, \ldots, b - 1\}$. A **radix-$b$ numeral** is a finite string $d_{k-1} \cdots d_1 d_0$ of digits $d_i \in D_b$, and its value is

$$N = \sum_{i=0}^{k-1} d_i \, b^i .$$

Position $i$ has the **weight** $b^i$. The numeral has **length** $k$, and it is **normalized** if $k = 0$ (the value 0) or $d_{k-1} \ne 0$. The digit $d_0$ is the least significant digit and $d_{k-1}$ the most significant one.

**Digit count.** For each integer $N \ge 1$, the normalized radix-$b$ numeral of $N$ has exactly

$$k = \lfloor \log_b N \rfloor + 1$$

digits. *Proof.* A numeral of length $k$ with $d_{k-1} \ge 1$ has value at least $b^{k-1}$. Its value is at most $\sum_{i=0}^{k-1} (b-1) b^i = b^k - 1$. So $b^{k-1} \le N < b^k$, that is $k - 1 \le \log_b N < k$, and $k - 1 = \lfloor \log_b N \rfloor$. $\square$

The existence and uniqueness of the normalized numeral are proved on the page [positional number system](/positional-number-system/), by repeated [division with remainder](/division-with-remainder/) by $b$.

**Notation of this area.** The pages on integer arithmetic write a long number in the radix $\beta = 2^w$, where $w$ is the word size. A digit in this radix is a **limb**, an $n$-limb number is $A = \sum_{i=0}^{n-1} a_i \beta^i$ with $0 \le a_i < \beta$, and $M(n)$ is the cost of multiplying two $n$-limb numbers. A cost is counted in limb operations on the [word RAM](/word-ram/) or in bit operations in a bit complexity model; each page says which one.

### Related radices

Two radices $b$ and $b^m$, for an integer $m \ge 1$, are related in a simple way: a radix-$b^m$ digit is a block of $m$ radix-$b$ digits. Cut the radix-$b$ numeral into blocks of $m$ digits from the right. The value of block $j$ is the digit of position $j$ in radix $b^m$, because

$$\sum_{i} d_i b^i = \sum_j \Big( \sum_{t=0}^{m-1} d_{jm+t} \, b^t \Big) (b^m)^j ,$$

and each inner sum lies in $\{0, \ldots, b^m - 1\}$. So conversion between binary, octal ($8 = 2^3$), hexadecimal ($16 = 2^4$) and the limb radix $2^w$ only regroups digits, in linear time. Conversion between radices that are not powers of one common integer, such as 2 and 10, needs real arithmetic; see [radix conversion](/radix-conversion/).

### The radix and the cost

For an integer $N$, the lengths in two radices $b$ and $c$ have the ratio $\log_b N / \log_c N \to \ln c / \ln b$. A decimal digit holds $\log_2 10 \approx 3.32$ binary digits. In a library with limbs of radix $2^w$, an $N$-bit number has $n = \lceil N / w \rceil$ limbs, and a schoolbook product costs about $n^2$ limb products. A larger $w$ makes $n$ smaller, but each limb product must still fit in the hardware: the full product of two $w$-bit limbs has $2w$ bits. This is why libraries use $w$ equal to the word size (GMP uses 64-bit limbs on 64-bit machines) or a little less (CPython stores an `int` in 30-bit digits, which leaves room for carries in a 64-bit word).

## Examples and non-examples

**The year 2026 in several radices.** The digit counts agree with $\lfloor \log_b 2026 \rfloor + 1$.

| radix $b$ | numeral | digits |
|---|---|---|
| 2 | $11111101010$ | 11 |
| 3 | $2210001$ | 7 |
| 8 | $3752$ | 4 |
| 10 | $2026$ | 4 |
| 16 | $7\mathrm{EA}$ | 3 |
| $2^8 = 256$ | $[7, 234]$ | 2 |

The hexadecimal numeral comes from the binary one by regrouping: $111\,1110\,1010$ gives the blocks $7$, $\mathrm{E} = 14$ and $\mathrm{A} = 10$. The radix-256 digits are the two bytes $7 = 2026 \operatorname{div} 256$ and $234 = 2026 \bmod 256$.

**Sizes of large numbers.** $10^{100}$ has 101 decimal digits, 333 binary digits and 42 limbs of radix $2^8$. The largest 64-bit unsigned integer, $2^{64} - 1 = 18446744073709551615$, has 20 decimal digits. Since $10^{19} < 2^{64}$, a decimal library can store 19 decimal digits in one 64-bit limb, with the radix $10^{19}$.

**Non-examples.**

- $b = 1$ is not a radix. All the weights $1^i$ are 1, the only standard digit is 0, and no positive number can be written. The *unary* system, which writes $N$ as $N$ marks, is not positional.
- $b = 0$ is not a radix: each weight after the first is 0, so only the digit $d_0$ counts.
- A digit outside $D_b$ breaks uniqueness. In radix 10 with the digits $0, \ldots, 10$, the number 10 is both $10$ and the one-digit string $(10)$. Such systems are useful on purpose: they are the [redundant number systems](/redundant-number-system/), and the [signed-digit representations](/signed-digit-representation/) and [balanced ternary](/balanced-ternary/) change the digit set too.
- A negative base, such as $-2$ with the digits 0 and 1, also represents each integer once, including the negative ones, and Knuth treats it with the other bases in Section 4.1. It is not a radix in the sense of this page, which requires $b \ge 2$.
- Mixed radices, where position $i$ has the weight $b_0 b_1 \cdots b_{i-1}$, are a generalization; the time of day in hours, minutes and seconds is one. The [factorial number system](/factorial-number-system/) is the mixed radix with $b_i = i + 2$.

## Related definitions

- [Positional number system](/positional-number-system/): the general system of which the radix is the parameter, with the proof that each number has one representation.
- [Multiprecision integer](/multiprecision-integer/): the data structure that stores a number as an array of limbs in the radix $\beta = 2^w$.
- [Radix conversion](/radix-conversion/): the problem of changing the radix of a numeral.
- [Two's complement](/twos-complement/), [ones' complement](/ones-complement/) and [sign-magnitude](/sign-magnitude-representation/): the ways to add a sign to a radix-2 numeral of fixed length.
- [Radix sort](/radix-sort/): the sorting method that reads keys digit by digit in a chosen radix.

## References
