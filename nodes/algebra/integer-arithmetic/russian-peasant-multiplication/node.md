---
tag: ANVYVS
kind: algorithm
slug: russian-peasant-multiplication
name: Russian peasant multiplication
aliases:
- Egyptian multiplication
- ancient Egyptian multiplication
- peasant multiplication
- duplation and mediation
- shift-and-add multiplication
area: algebra/integer-arithmetic
level: intro
summary: Multiply by repeated doubling and halving, using only addition and bit shifts.
solves: [integer-multiplication]
model: word-ram
complexity:
  vars: {N: the number of binary digits of the multiplier y, n: the number of limbs of each operand}
  time: {worst: Θ(N n), best: Θ(N n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [positional-number-system, integer-addition, loop-invariant]
see_also: [schoolbook-multiplication, binary-exponentiation, lattice-multiplication, booth-multiplication, array-multiplier, integer-multiplication, addition-chain]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms, 2019
    locator: Chapter 0, Introduction, Section 0.2, Multiplication (lattice multiplication and duplation and mediation, the peasant method, with its correctness argument)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the right-to-left binary method, the same scheme with products in place of sums)
  - book: isbn:9783540633693
    title: Jean-Luc Chabert (editor), A History of Algorithms, From the Pebble to the Microchip, Springer, 1999
    locator: Chapter 1, the section on Egyptian multiplication by doubling (the Rhind papyrus)
---

Russian peasant multiplication computes $x \cdot y$ with only doubling, halving and addition: it halves $y$ and doubles $x$ until $y$ reaches zero, and adds the current $x$ to the result at each step where $y$ is odd. It is the binary expansion of $y$ in disguise, since the steps where $y$ is odd are the 1 bits of $y$. On limb arrays it takes $N$ rounds of shifts and additions for an $N$-bit multiplier, so $\Theta(Nn)$ limb operations on the [word RAM](/word-ram/); this is $\Theta(N^2)$ bit operations, the order of [schoolbook multiplication](/schoolbook-multiplication/), but a factor of about $w$ slower in limb operations. Its value is as a simple method for hardware without a multiplier, and as the pattern of [binary exponentiation](/binary-exponentiation/).

## In plain words

Write the two numbers at the top of two columns. In the left column, halve the number again and again, dropping any half, until you reach 1. In the right column, double the number the same number of times. Now cross out each row whose left number is even. Add up the right numbers that are left. The sum is the product.

It works because halving the left number reads its binary digits one by one, from the lowest. An odd number means a 1 digit. The right column holds the first number times one, two, four, eight and so on. So the sum adds exactly the right powers of two times the first number. A computer does the same with shifts, which are cheap.

## The problem

The input is two nonnegative integers $x$ and $y$, here as limb arrays in the radix $\beta = 2^w$ ([multiprecision integers](/multiprecision-integer/) without signs). The output is $x y$, the problem of [integer multiplication](/integer-multiplication/). For signed values, multiply the magnitudes and apply the sign rule.

**Cost model.** Costs are in limb operations on the word RAM with $w$-bit words, and in bit operations where the page says so. $N$ is the number of binary digits of $y$, and $n$ the number of limbs of each operand, so $N \le nw$.

## The algorithm

```pseudo id=main
PEASANT-MUL(x, y)                ▷ x, y ≥ 0
L1  p ← 0
L2  while y > 0 do
L3      if y is odd then p ← p + x
L4      x ← 2x                   ▷ a shift left by one bit
L5      y ← ⌊y / 2⌋              ▷ a shift right by one bit
L6  return p
```

On a limb array, "$y$ is odd" reads the lowest bit of the lowest limb, the doubling of line L4 shifts each limb left by one bit and passes the top bit of each limb into the next one, and the halving of line L5 does the reverse. The addition of line L3 is a [multiprecision addition](/integer-addition/). No limb product is used anywhere.

## Example

Multiply $x = 4093$ by $y = 199$. In binary $199 = 11000111_2$, so the loop runs 8 times.

| round | $y$ | $y$ odd | $x$ | $p$ after line L3 |
|---|---|---|---|---|
| 1 | 199 | yes | 4093 | 4093 |
| 2 | 99 | yes | 8186 | 12279 |
| 3 | 49 | yes | 16372 | 28651 |
| 4 | 24 | no | 32744 | 28651 |
| 5 | 12 | no | 65488 | 28651 |
| 6 | 6 | no | 130976 | 28651 |
| 7 | 3 | yes | 261952 | 290603 |
| 8 | 1 | yes | 523904 | 814507 |

After round 8, $y = 0$ and the loop stops. The result is $814507 = 4093 \cdot 199$. The rows with an odd $y$ are the rows $1, 2, 3, 7, 8$, which match the 1 bits $2^0, 2^1, 2^2, 2^6, 2^7$ of 199: $4093 \cdot (1 + 2 + 4 + 64 + 128) = 4093 \cdot 199$.

## Correctness

Let $x_0$ and $y_0$ be the inputs. The invariant of the loop of line L2 is

$$p + x \cdot y = x_0 \cdot y_0 .$$

It holds at the start, with $p = 0$. If $y$ is even, then $2x \cdot \lfloor y/2 \rfloor = x y$, and $p$ does not change. If $y$ is odd, then $2x \cdot \lfloor y/2 \rfloor = x(y - 1)$, and line L3 adds $x$ to $p$, so $p + x + x(y - 1) = p + xy$. In both cases the invariant holds after the round. The loop stops because $y$ drops to at most half, and when $y = 0$ the invariant gives $p = x_0 y_0$. The full proof is below.

## Complexity

The loop runs once for each binary digit of $y$: $N = \lfloor \log_2 y_0 \rfloor + 1$ rounds for $y_0 \ge 1$, and none for $y_0 = 0$. In round $r$, the value $x$ is $x_0 2^{r-1}$, which has at most $m + \lceil N/w \rceil$ limbs if $x_0$ has $m$ limbs, and $p < x_0 2^{r}$ has as many. So each round costs $O(m + n)$ limb operations for the shifts and the addition, and the shift of $y$ costs $O(n)$. The total is $\Theta(N (m + n))$, which is $\Theta(N n)$ for operands of $n$ limbs each, the same in each case, since the shifts happen in every round whatever the bits.

In bit operations, for two $N$-bit inputs this is $\Theta(N^2)$, the same order as the schoolbook method. In limb operations, with $N = nw$, it is $\Theta(w n^2)$ against $\Theta(n^2)$ for schoolbook, because a limb product handles $w$ bits of the multiplier at once. The number of additions is the number of 1 bits of $y$, between 1 and $N$; on average over $N$-bit numbers it is about $N/2$.

## Properties

- **No multiplier needed.** Only addition, shifts and a parity test. This is why the method is the default for processors and microcontrollers without a multiply instruction, and the sequential shift-and-add multiplier in hardware does the same, one bit per clock cycle.
- **Not constant time.** The additions happen only for 1 bits of $y$. A program that must not leak $y$, such as cryptographic code, must add $x$ or 0 in each round.
- **Asymmetric.** The cost depends on the bit length of $y$. Choose the shorter operand as $y$.

## Variants and improvements

- **Left-to-right form.** Scan the bits of $y$ from the top: $p \leftarrow 2p$, then $p \leftarrow p + x$ for a 1 bit. This needs only $p$ and $x$, not a growing copy of $x$, and is the form of most hardware.
- **Higher radix.** Process $k$ bits of $y$ at once with a table of $x, 2x, \ldots, (2^k - 1)x$; with $k = w$ this becomes multiplication by limbs, the schoolbook method.
- **Signed digits.** [Booth recoding](/booth-multiplication/) writes $y$ with digits $-1, 0, 1$, so that long runs of 1 bits cost one subtraction and one addition.
- **Exponentiation.** Replace the addition by a product and the doubling by a squaring, and the same loop computes $x^y$: the [binary exponentiation](/binary-exponentiation/) method. Over a group or a ring with a cheap "addition", the same loop computes $y \cdot x$, for example the scalar multiple of a point on an elliptic curve.
- **Multiplication modulo $m$.** Reduce $p$ and $x$ modulo $m$ after each step, which keeps the numbers small. This gives $xy \bmod m$ without an overflowing product, a common trick for 64-bit moduli on machines without a 128-bit product.

## When to use it

Use it on hardware without a multiplier, to compute $xy \bmod m$ when $xy$ would overflow, or as a teaching example of a loop invariant. For multiprecision numbers on a machine with a multiply instruction, use the [schoolbook method](/schoolbook-multiplication/) or a faster one: they are about $w$ times faster.

## Pitfalls

- **Testing the wrong number for parity.** Line L3 tests $y$, the number that is halved. Testing $x$, which is doubled and so even after the first round, gives a wrong result.
- **Doubling before adding.** If lines L3 and L4 are swapped, each added term is twice too large, and the result is $2xy$. The addition must use the value of $x$ before the doubling.
- **Overflow of $x$.** In fixed-width code, the doubling of line L4 in the last round makes $x = x_0 2^N$, which is larger than the product $x_0 y_0 \ge x_0 2^{N-1}$, up to twice as large. In the example the last $x$ is $1047808$ while the product is $814507$. Either skip the last doubling or use a width of one bit more than the product.
- **Signed values.** With a negative $y$, $\lfloor y/2 \rfloor$ in two's complement never reaches 0 (it stays at $-1$), and the loop does not stop. Multiply the magnitudes.

## Implementations

## History

Multiplication by doubling and adding is the method of the Egyptian scribes: the Rhind papyrus, of about 1650 BC, multiplies by writing the doublings of one factor and adding those that match the binary digits of the other. Chabert's history describes it in its first chapter. The names *duplation* and *mediation*, for doubling and halving, come from later European arithmetic books, where the two were counted as operations of their own. The name "Russian peasant multiplication" is traditional, and it is not clear who first used it. Knuth describes the same scheme for powers as the right-to-left binary method.

## References
