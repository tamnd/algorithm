---
tag: 3W1M2Y
kind: concept
slug: integer-overflow
name: Integer overflow
aliases:
- arithmetic overflow
- wraparound
- integer wraparound
area: algebra/integer-arithmetic
level: intro
summary: A result that falls outside the range a fixed-width integer can represent.
prereqs: [twos-complement, positional-number-system]
see_also: [ones-complement, sign-magnitude-representation, sign-extension, multiprecision-integer, arbitrary-precision-arithmetic, carry-propagation, congruence, binary-search]
sources:
  - book: isbn:9780134092669
    title: Randal E. Bryant and David R. O'Hallaron, Computer Systems, A Programmer's Perspective, third edition, Pearson, 2016
    locator: Section 2.3, Integer arithmetic (unsigned and two's complement addition, negation and multiplication, with the rules for detecting overflow)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2013
    locator: Chapter 2, Basics, the section on overflow detection (signed and unsigned addition, subtraction and multiplication)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 2, Representing signed numbers (the ranges of the signed encodings and overflow in complement addition)
  - url: https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/
    title: Joshua Bloch, Extra, Extra, Read All About It, Nearly All Binary Searches and Mergesorts are Broken, Google Research Blog, 2006
    locator: the overflow of (low + high) / 2 in the JDK binary search
---

Integer overflow happens when the exact result of an operation on fixed-width integers lies outside the range that the width can represent. A $w$-bit word holds the unsigned values $0, \ldots, 2^w - 1$ and the [two's complement](/twos-complement/) values $-2^{w-1}, \ldots, 2^{w-1} - 1$; an addition, subtraction, multiplication, negation or division whose true result is outside the range cannot be stored. Almost all hardware then keeps the low $w$ bits, which is the true result modulo $2^w$, and sets a flag. What a program sees depends on the language: a wrapped value, a trap, a saturated value, or, in C for signed types, undefined behavior. [Multiprecision integers](/multiprecision-integer/) avoid overflow by growing, and they are built from the same carry that signals unsigned overflow in one word.

## In plain words

A car's odometer with five wheels shows at most 99999. Drive one more kilometer and it shows 00000. Nothing is broken in the counter; it can only hold five digits, and the sixth digit is lost.

Computer integers work the same way. A number is kept in a fixed number of binary digits. When a sum or a product needs more digits than there are, the extra top digits are dropped, and what is left can be a small number, or a negative one. If the program does not check for this, it goes on with a wrong value. Many real bugs, crashes and security holes come from this. The cure is to know the range, to check before or after each risky step, or to use numbers that grow as needed.

## The idea

**Ranges.** Fix a word of $w$ bits. As an unsigned integer, the word $x_{w-1} \cdots x_0$ has the value $\sum_i x_i 2^i$, in $U_w = [0, 2^w - 1]$. As a two's complement integer it has the value $-x_{w-1}2^{w-1} + \sum_{i < w-1} x_i 2^i$, in $T_w = [-2^{w-1}, 2^{w-1} - 1]$. An operation on values in the range **overflows** when its exact integer result is not in the range. For $w = 8$ the ranges are $[0, 255]$ and $[-128, 127]$; for $w = 32$, $T_{32} = [-2147483648, 2147483647]$.

**Wraparound.** Hardware adders and multipliers compute the exact result modulo $2^w$, the low $w$ bits. In both encodings the stored word is the unique value of the range [congruent](/congruence/) to the exact result modulo $2^w$. So the wrapped result is wrong as an integer, but right modulo $2^w$, and this is why the same adder serves both encodings. Some code relies on this on purpose: hash functions, random number generators and checksums compute modulo $2^w$.

**Detecting overflow in addition.** For unsigned $a + b$, the result overflows exactly when the carry out of the top bit is 1, or, in code, when the wrapped sum $s$ satisfies $s < a$. For two's complement $a + b$, the result overflows exactly when $a$ and $b$ have the same sign and $s$ has the other sign. Equivalently, the carry into the top bit differs from the carry out of it. Two values of different signs can never overflow when added. For subtraction $a - b$, the signed rule is: $a$ and $b$ have different signs and $s$ has the sign of $b$.

**The other operations.**

- **Negation.** In two's complement, $-(-2^{w-1}) = 2^{w-1}$ is not in $T_w$, so negation and absolute value of the minimum overflow, and wrap back to the minimum.
- **Division.** Unsigned division never overflows. Signed division overflows in one case only, $-2^{w-1} / (-1)$, and on many processors this case traps like a division by zero.
- **Multiplication.** The exact product of two $w$-bit values needs up to $2w$ bits. It fits when the high half of the double-width product is zero (unsigned), or is the sign extension of the low half (signed). Without a double-width product, test $a \ne 0$ and $s / a \ne b$ for the wrapped product $s$, or compare $|b|$ with $\lfloor (2^{w-1} - 1) / |a| \rfloor$ before multiplying.
- **Shifts.** A left shift by $k$ multiplies by $2^k$ and overflows when any of the top $k + 1$ bits differ (signed) or any of the top $k$ bits is 1 (unsigned). A shift by $w$ or more is undefined in C.
- **Conversions.** Converting to a narrower type, or a floating-point number to an integer type, can overflow too.

**What languages do.** In C and C++, unsigned arithmetic wraps modulo $2^w$ by definition, while signed overflow is undefined behavior, which lets the compiler assume it never happens and remove checks written after the fact, such as `if (a + b < a)` for signed $a, b$. Java and Go wrap signed values. Rust panics on overflow in debug builds and wraps in release builds unless told otherwise, and it offers checked, wrapping and saturating methods. Python integers are [arbitrary precision](/arbitrary-precision-arithmetic/) and never overflow. Compilers also give checked operations, such as `__builtin_add_overflow` in GCC and Clang, which compile to an add and a test of the flag.

**Overflow as a carry.** In a multiprecision addition with base $\beta = 2^w$, each limb addition overflows by design, and the carry out, 0 or 1, goes into the next limb. In this sense unsigned overflow of one word is the carry of the [positional number system](/positional-number-system/), and a big integer is a way to keep the digit that one word would drop.

## Examples

All examples use $w = 8$ unless stated. The values were checked by script.

- **Signed addition.** $100 + 100 = 200 > 127$. The stored word is $11001000_2$, which is $-56$ in two's complement: $200 - 256 = -56$. Both operands are positive and the result is negative, so the sign rule detects the overflow. The carry into bit 7 is 1 and the carry out is 0, which differ.
- **The edge of the range.** $127 + 1$ gives $-128$, and $-128 - 1$ gives $127$.
- **Negation of the minimum.** $-(-128)$ gives $-128$, and so $|{-128}| = -128$ in 8-bit code, a negative absolute value.
- **Unsigned addition.** $200 + 100 = 300$. The stored value is $300 - 256 = 44$, with a carry out of 1, and $44 < 200$ detects it.
- **Multiplication.** $16 \cdot 16 = 256$, stored as $0$: the low 8 bits of $100000000_2$. The test $s / a = 0 / 16 = 0 \ne 16$ detects it.
- **A midpoint in 32 bits.** With $lo = hi = 2^{30}$, the sum $lo + hi = 2^{31}$ wraps to $-2^{31}$, and $(lo + hi)/2$ gives $-2^{30}$, a negative index. The form $lo + (hi - lo)/2 = 2^{30}$ cannot overflow when $0 \le lo \le hi$. Bloch reported in 2006 that the [binary search](/binary-search/) and the merge sort of the JDK had this bug, which appears only for arrays of more than $2^{30}$ elements.
- **Time in 32 bits.** A signed 32-bit count of seconds since 1 January 1970 reaches its maximum $2^{31} - 1$ at 03:14:07 UTC on 19 January 2038, and the next second wraps to a date in 1901. This is the year 2038 problem.
- **A conversion.** The first flight of the Ariane 5 rocket, in 1996, failed after a 64-bit floating-point value was converted to a 16-bit signed integer and was too large, an exception the software did not handle.

**Non-example.** Adding a positive and a negative value, such as $100 + (-100)$ or $127 + (-128)$, never overflows in two's complement, even though the unsigned view of the same words has a carry out. A carry out alone is not a signed overflow.

## Where it is used

- **Correct programs.** Every computation of sizes, indices and offsets in fixed-width integers must keep each intermediate value in range. Overflow in a size computation, such as $n \cdot k$ bytes for an array of $n$ items of $k$ bytes, is a common source of buffer overflows and security holes.
- **Modular arithmetic on purpose.** Hashing, checksums, linear congruential generators and multiplication modulo $2^w$ use the wraparound as a feature. Unsigned types in C make this defined.
- **Multiprecision arithmetic.** The carry of each limb operation is the unsigned overflow of one word, and [multiprecision integers](/multiprecision-integer/) are built on detecting it. Instruction sets give an add with carry for this.
- **Hardware design.** The overflow flag of a processor is computed from the carries into and out of the top bit of the adder. The [one's complement](/ones-complement/) and [sign-magnitude](/sign-magnitude-representation/) encodings have their own overflow rules.
- **Saturating arithmetic.** Signal and image processing often clamp a result to the largest or smallest value instead of wrapping, so that a too-bright pixel stays white instead of turning black.

## References
