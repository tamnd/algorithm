---
tag: WZN2G1
kind: data-structure
slug: multiprecision-integer
name: Multiprecision integer representation
aliases:
- limb array
- digit array bignum
- sign-magnitude bignum
area: algebra/integer-arithmetic
level: core
summary: Stores an integer as an array of fixed-size digits (limbs) with a sign.
implements: [big-integer]
model: word-ram
complexity:
  vars: {m: the number of limbs of the first operand, n: the number of limbs of the second operand}
  time: {worst: Θ(m + n), best: Θ(m + n)}
  space: {extra: Θ(m + n)}
prereqs: [positional-number-system, big-integer, word-ram]
see_also: [arbitrary-precision-arithmetic, integer-addition, schoolbook-multiplication, long-division, sign-magnitude-representation, twos-complement, radix-conversion, integer-overflow]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Algorithms A and S on n-place integers, signed numbers, and the remark on the representation of signs)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.1, Representation of integers, and Section 1.2, Addition and subtraction
  - url: https://gmplib.org/manual/Integer-Internals
    title: The GNU Multiple Precision Arithmetic Library manual, Integer Internals
    locator: the fields _mp_size (a signed limb count), _mp_alloc and _mp_d of mpz_t
---

A multiprecision integer is the usual representation of a [big integer](/big-integer/): a sign and an array of limbs, which are the digits of the absolute value in the [radix](/radix/) $\beta = 2^w$, least significant limb first. The array is normalized, so its top limb is never zero, and the number zero has no limbs and no minus sign; then each integer has exactly one representation. Addition, subtraction and comparison take $\Theta(m + n)$ limb operations on the [word RAM](/word-ram/), and they are the base on which [schoolbook multiplication](/schoolbook-multiplication/), [long division](/long-division/) and the fast methods are built.

## In plain words

A computer word holds a number of fixed size, for example up to about eighteen billion billion for a 64-bit word. To hold a larger number, write it in a very large base, where each "digit" fills one word, and store the digits in a list. This is the same as writing a number in decimal, but the digits are huge.

The list starts with the lowest digit, because addition starts there and the carries move up. The list never ends with a zero digit, so each number has only one form, and the length of the list tells the size of the number. The sign is kept apart, as a flag. To add two numbers with the same sign, add the digit lists. With different signs, subtract the smaller list from the larger one, and take the sign of the larger number.

## The abstract type

The representation implements the [big integer](/big-integer/) type: the values are all of $\mathbb{Z}$, with exact `add`, `sub`, `neg`, `compare` and `mul`, and the conversions to and from machine integers. Division by a single limb is given here because [radix conversion](/radix-conversion/) and printing need it; general division is [long division](/long-division/).

## Representation

Fix a word size $w \ge 1$ and $\beta = 2^w$. A value is a pair $(s, a)$, where $s \in \{+, -\}$ is the sign and $a = [a_0, a_1, \ldots, a_{n-1}]$ is a list of $n \ge 0$ limbs with $0 \le a_i < \beta$. It stands for

$$\operatorname{val}(s, a) = \pm \sum_{i=0}^{n-1} a_i \beta^i .$$

**Invariant (N).** If $n > 0$ then $a_{n-1} \ne 0$, and if $n = 0$ then $s = +$.

By the [unique representation theorem](/positional-number-system/), each integer $x$ has exactly one pair that meets (N): $a$ is the normalized radix-$\beta$ numeral of $|x|$, and $s$ is the sign of $x$, with $+$ for zero. So two values are equal exactly when their pairs are equal, and the length $n$ gives the size: $\beta^{n-1} \le |x| < \beta^n$ for $x \ne 0$.

In a real library the pair is a record with three fields. GMP's `mpz_t` has `_mp_d`, a pointer to the limbs; `_mp_alloc`, the number of limbs allocated; and `_mp_size`, the number of limbs in use, which is negative for a negative number. The sign is thus stored in the size, and zero has size 0. This is a [sign-magnitude](/sign-magnitude-representation/) form. A fixed-width machine integer uses [two's complement](/twos-complement/) instead; for numbers of varying length, sign-magnitude makes multiplication and comparison of magnitudes simpler.

**Notation.** $|a|$ is the number of limbs of $a$, and $\operatorname{mag}(a) = \sum a_i \beta^i$. A *limb operation* is one of: an addition or subtraction of two limbs and a carry bit, giving a limb and a carry bit; a product of two limbs, giving two limbs; a division of a two-limb number by a limb when the quotient fits in one limb; and a comparison of two limbs. Each takes $O(1)$ time on the word RAM with words of $w$ bits.

## Operations

### Addition

The main operation is the signed sum. It calls a magnitude addition and a magnitude subtraction, each one pass over the limbs.

```pseudo id=main
ADD((s, a), (t, b))                       ▷ both normalized
L1  if s = t then
L2      return (s, ADD-MAG(a, b))
L3  c ← CMP-MAG(a, b)
L4  if c = 0 then return (+, [ ])           ▷ x + (−x) is 0, never −0
L5  if c > 0 then return (s, SUB-MAG(a, b))
L6  return (t, SUB-MAG(b, a))

ADD-MAG(a, b)                             ▷ swap first so that m = |a| ≥ |b| = n
L7  carry ← 0
L8  for i ← 0 to m − 1 do
L9      t ← a[i] + (b[i] if i < n else 0) + carry
L10     if t ≥ β then c[i] ← t − β, carry ← 1 else c[i] ← t, carry ← 0
L11 if carry = 1 then c[m] ← 1
L12 return c

SUB-MAG(a, b)                             ▷ requires mag(a) ≥ mag(b); m = |a|, n = |b|
L13 borrow ← 0
L14 for i ← 0 to m − 1 do
L15     t ← a[i] − (b[i] if i < n else 0) − borrow
L16     if t < 0 then c[i] ← t + β, borrow ← 1 else c[i] ← t, borrow ← 0
L17 while c is not empty and the top limb of c is 0 do remove it
L18 return c
```

With equal signs, the magnitudes add (lines L1 and L2). With different signs, the result has the sign of the operand with the larger magnitude, and its magnitude is the difference (lines L3 to L6). Line L4 keeps the invariant for zero. The sum $t$ of line L9 is at most $2(\beta - 1) + 1 = 2\beta - 1$, so a carry is 0 or 1. In SUB-MAG, $t \ge -\beta$, so a borrow is 0 or 1. Line L11 adds the one new limb that a sum can need, and line L17 removes the zero limbs that a difference can leave at the top: the difference of two close numbers can be much shorter than both.

Subtraction is $\operatorname{ADD}(x, -y)$, and negation flips $s$ unless the value is zero.

### Comparison

```pseudo id=cmp
CMP-MAG(a, b)                             ▷ both normalized; returns the sign of mag(a) − mag(b)
C1  if |a| ≠ |b| then return (1 if |a| > |b| else −1)
C2  for i ← |a| − 1 down to 0 do
C3      if a[i] ≠ b[i] then return (1 if a[i] > b[i] else −1)
C4  return 0
```

Line C1 is correct only because of (N): a normalized array with more limbs has a larger magnitude. The signed comparison first compares the signs, and for two negative values it reverses the result of CMP-MAG.

### Multiplication and division by a limb

```pseudo id=mul
MUL((s, a), (t, b))                       ▷ m = |a|, n = |b|
M1  if m = 0 or n = 0 then return (+, [ ])
M2  c ← [0] · (m + n)
M3  for i ← 0 to m − 1 do
M4      carry ← 0
M5      for j ← 0 to n − 1 do
M6          (carry, c[i + j]) ← c[i + j] + a[i] · b[j] + carry     ▷ high limb, low limb
M7      c[i + n] ← carry
M8  remove the top limb of c if it is 0
M9  return (+ if s = t else −, c)

DIV-LIMB((s, a), d)                        ▷ 0 < d < β; returns (q, r) with mag(a) = q d + r, 0 ≤ r < d
D1  r ← 0
D2  for i ← |a| − 1 down to 0 do
D3      (q[i], r) ← (⌊(r β + a[i]) / d⌋, (r β + a[i]) mod d)
D4  normalize q and return ((s, q), r)
```

MUL is the [schoolbook method](/schoolbook-multiplication/), which proves why line M6 never overflows two limbs. A product of normalized numbers has $m + n - 1$ or $m + n$ limbs, so line M8 removes at most one limb. In DIV-LIMB, $r < d$ before line D3, so $r \beta + a_i < d \beta$ and the quotient digit is less than $\beta$: one two-by-one limb division of the hardware.

## Example

Take $w = 4$, so $\beta = 16$. Let $x = 4093 = 15 \cdot 256 + 15 \cdot 16 + 13$, with the limbs $a = [13, 15, 15]$, and $y = 3$, with $b = [3]$. Both are positive, so ADD calls ADD-MAG:

| $i$ | $a_i$ | $b_i$ | carry in | $t$ | $c_i$ | carry out |
|---|---|---|---|---|---|---|
| 0 | 13 | 3 | 0 | 16 | 0 | 1 |
| 1 | 15 | 0 | 1 | 16 | 0 | 1 |
| 2 | 15 | 0 | 1 | 16 | 0 | 1 |

Line L11 appends the limb 1, so $x + y = [0, 0, 0, 1] = 16^3 = 4096$. The carry from the lowest limb ran through all the limbs equal to $\beta - 1$ and made a new limb.

Now add $x = 4093$ and $z = -4096$, with the limbs $[0, 0, 0, 1]$. The signs differ. CMP-MAG returns $-1$ at line C1, because $z$ has 4 limbs and $x$ has 3. So line L6 returns the sign of $z$ and SUB-MAG$([0, 0, 0, 1], [13, 15, 15])$:

| $i$ | top limb | bottom limb | borrow in | $t$ | $c_i$ | borrow out |
|---|---|---|---|---|---|---|
| 0 | 0 | 13 | 0 | $-13$ | 3 | 1 |
| 1 | 0 | 15 | 1 | $-16$ | 0 | 1 |
| 2 | 0 | 15 | 1 | $-16$ | 0 | 1 |
| 3 | 1 | 0 | 1 | 0 | 0 | 0 |

The list is $[3, 0, 0, 0]$. Line L17 removes three zero limbs, and the result is $(-, [3]) = -3$.

## Correctness

Each operation takes normalized pairs and returns a normalized pair whose value is the exact result. For ADD-MAG the key fact is the carry invariant $\sum_{j < i} c_j \beta^j + \text{carry} \cdot \beta^i = \sum_{j < i} (a_j + b_j) \beta^j$ before step $i$; for SUB-MAG it is the same with a borrow and a minus sign. The proof of all operations, with the case analysis of ADD on the signs, is in the proof below.

## Complexity

All costs are in limb operations on the word RAM, for operands of $m$ and $n$ limbs.

| operation | worst case | notes |
|---|---|---|
| `add`, `sub` | $\Theta(m + n)$ | one pass, plus CMP-MAG for opposite signs; the copy of the longer operand costs $\Theta(\max(m, n))$ |
| `neg` | $O(1)$ in place | $\Theta(n)$ if the limbs are copied |
| `compare` | $O(n)$ | $O(1)$ when the signs or the lengths differ |
| `mul` | $\Theta(m n)$ | the schoolbook method; the fast methods replace it for large sizes |
| division by a limb | $\Theta(n)$ | $n$ two-by-one limb divisions |
| space | $\Theta(m + n)$ | the result; a sum can have $\max(m, n) + 1$ limbs, a product $m + n$ |

ADD-MAG and SUB-MAG do $\max(m, n)$ steps of $O(1)$ limb operations each, and line L17 removes each limb at most once. CMP-MAG reads each limb at most once. These bounds are tight: in the worst case the result has $\Theta(\max(m, n))$ limbs, and each limb of the output must be written. The page [schoolbook multiplication](/schoolbook-multiplication/) counts the $mn$ limb products of MUL.

The carry of a sum moves far only on special inputs. On the example above it runs through all limbs; for random limbs, a carry out of a position happens with probability about $\frac12$, and the expected length of the longest run of carries is $O(\log n)$. The time of a software addition is $\Theta(m + n)$ in each case anyway, because each limb is read.

## Variants

- **Two's complement limbs.** Store a negative number as $\beta^n + x$ in $n$ limbs, the infinite [two's complement](/twos-complement/) form cut at a length where the top bit shows the sign. Addition then needs no case analysis, but multiplication and division need corrections, and the length must be chosen to avoid [overflow](/integer-overflow/). Java's `BigInteger` keeps sign-magnitude inside and simulates this form for the bitwise operations.
- **Most significant limb first.** Some decimal and teaching codes store the limbs in the order of the printed digits. Addition then runs from the end of the array; nothing else changes.
- **Decimal radix.** Limbs in radix $10^k$, for example $10^9$ in a 32-bit word or $10^{19}$ in a 64-bit word, make printing a linear-time operation, at the cost of a division by a constant in each carry.
- **Small-value optimization.** Many libraries store a value that fits in one word without an array, and switch to the limb array only on overflow. CPython's `int` uses one representation, with 30-bit digits, for all sizes.
- **Nails.** GMP has an option to leave the top bits of each limb empty (the "nails"), so that carries can be added later. This is a small [redundant number system](/redundant-number-system/).

## When to use it

Use this representation whenever integers can exceed the machine word, and a language or library does not already give a big integer type. Use the radix $2^w$ for computation, and a decimal radix only when most of the work is input and output of decimal numbers. For a fixed, known size, such as 256-bit cryptographic numbers, a fixed array of limbs without a length field and without branches on the length is faster and safer against timing attacks.

## Pitfalls

- **Negative zero.** If line L4 returns $(s, [\,])$ for $x + (-x)$, then $5 + (-5)$ is $-0$, and an equality test that compares the pairs finds $-0 \ne 0$. Always return $(+, [\,])$, and set the sign of a zero product to $+$ (line M1).
- **Not normalizing after a subtraction.** Without line L17, $4096 - 4093$ is $[3, 0, 0, 0]$, and line C1 then decides by length that it is larger than $[5]$. Every operation that can shrink a result must remove the zero top limbs.
- **The carry of a full limb.** In C, `t = a[i] + b[i] + carry` overflows in a $w$-bit variable when $w$ is the word size. Compute the carry as `(t < a[i])` or with the add-with-carry instruction, or use a double-width type; the pseudocode uses the exact sum.
- **Comparison by length with unequal signs.** For negative values, more limbs means a smaller value. CMP-MAG compares magnitudes only; the signed comparison must reverse its result when both values are negative.
- **Mixing radices.** Two values with different $w$ cannot be added limb by limb. The implementation below rejects this case.

## Implementations

## History

Knuth's Section 4.3.1 gives the classical algorithms on $n$-place integers in radix $b$, and discusses how to treat the signs. The word limb and the signed size field are those of GMP.

## References
