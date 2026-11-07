---
tag: B6TGDA
kind: algorithm
slug: booth-multiplication
name: Booth's multiplication
aliases:
- Booth's algorithm
- radix-4 Booth multiplication
- Booth recoding
- modified Booth algorithm
area: algebra/integer-arithmetic
level: advanced
summary: Signed multiplication that recodes the multiplier to reduce the number of nonzero partial products.
solves: [integer-multiplication]
model: multitape-turing-machine
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Andrew Donald Booth published the radix-2 method in 1951; MacSorley described the radix-4 recoding, now called modified Booth, in 1961.
prereqs: [twos-complement, schoolbook-multiplication, signed-digit-representation]
see_also: [non-adjacent-form, array-multiplier, wallace-tree-multiplier, dadda-multiplier, carry-save-addition, redundant-number-system, integer-multiplication]
sources:
  - paper: doi:10.1093/qjmam/4.2.236
    title: Andrew D. Booth, A signed binary multiplication technique, The Quarterly Journal of Mechanics and Applied Mathematics 4(2), 1951
    locator: pp. 236 to 240 (the rule on the pair of the current and previous multiplier bits)
  - paper: doi:10.1109/JRPROC.1961.287779
    title: O. L. MacSorley, High-speed arithmetic in binary computers, Proceedings of the IRE 49(1), 1961
    locator: pp. 67 to 91, the section on multiplication (recoding the multiplier in pairs of bits into the digits -2 to 2)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Section 9.4, Multiplication of signed numbers (Booth's recoding), and Section 10.2, Modified Booth's recoding
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 4, Multiplication (recoding of the multiplier, radix 4 and higher)
---

Booth's multiplication multiplies two $n$-bit [two's complement](/twos-complement/) integers by rewriting the multiplier $y$ in [signed digits](/signed-digit-representation/), then adding or subtracting shifted copies of the multiplicand $x$ for the nonzero digits only. In the radix-2 form, the digit at position $i$ is $y_{i-1} - y_i \in \{-1, 0, 1\}$: a run of 1s in $y$ costs one subtraction at its low end and one addition above its high end, however long it is, and the sign of $y$ is handled with no correction step. In the radix-4 form, the *modified Booth* recoding, each pair of bits becomes one digit in $\{-2, -1, 0, 1, 2\}$, so a multiplier has only $\lceil n/2 \rceil$ partial products, each $0$, $\pm x$ or $\pm 2x$. This halving is why almost every hardware multiplier recodes its multiplier this way before an [array](/array-multiplier/) or a [Dadda](/dadda-multiplier/) tree.

## In plain words

To multiply by 99, you can add 99 copies, or you can multiply by 100 and subtract one copy. Booth's idea is the binary form of that trick. A block of 1s in the multiplier, like 0111 1110, equals a single 1 just above the block minus a single 1 at its bottom, so instead of six additions you do one subtraction and one addition.

The algorithm reads the multiplier from right to left, looking at two neighbouring bits at a time. Where a block of 1s starts it subtracts the multiplicand, where it ends it adds it back, and inside blocks it only shifts. It also gets negative numbers right with no extra work. The radix-4 version reads bits in overlapping groups of three and needs only half as many steps.

## The problem

The input is two integers $x$ and $y$ in $n$-bit two's complement, $-2^{n-1} \le x, y < 2^{n-1}$, and the bits of $y$ are $y_{n-1} \ldots y_0$, so $y = -y_{n-1} 2^{n-1} + \sum_{i < n-1} y_i 2^i$. The output is $xy$ in $2n$-bit two's complement, which always fits since $|xy| \le 2^{2n-2}$.

**Cost model.** The bit model (multitape Turing machine, or equally a register machine charged per bit): an addition, subtraction or shift of $(n+1)$-bit registers costs $\Theta(n)$ bit operations. The sequential algorithm does $n$ steps of one shift and at most one addition each, so it costs $\Theta(n^2)$ in every case; this is proved. The number of additions, at most $n$ for radix 2 and at most $\lceil n/2 \rceil$ for radix 4, is also proved; its average, about $n/2$ and $3n/8$ for random multipliers, follows from counting digit patterns. Speeds of real circuits are observations.

## The algorithm

```pseudo id=main
BOOTH(x, y, n)                                  ▷ x, y: n-bit two's complement
L1  A ← 0 (n + 1 bits); Q ← y (n bits); q₋₁ ← 0
L2  repeat n times
L3      if (q₀, q₋₁) = (1, 0) then A ← A − x          ▷ a run of 1s starts
L4      else if (q₀, q₋₁) = (0, 1) then A ← A + x     ▷ a run of 1s has ended
L5      shift (A, Q, q₋₁) right by one bit, copying the sign bit of A
L6  return the low 2n bits of (A, Q) as a two's complement number

BOOTH-4(x, y, n)                                ▷ radix-4 recoding, n made even by sign extension
L7  for j ← 0 to n/2 − 1 do q_j ← y_(2j−1) + y_(2j) − 2·y_(2j+1)      ▷ y₋₁ = 0, q_j ∈ {−2, …, 2}
L8  P ← Σ_j q_j · x · 4^j                        ▷ q_j · x is 0, ±x or ±2x: a shift and a negation
L9  return P
```

Line L3 and line L4 apply the radix-2 digit $y_{i-1} - y_i$ at step $i$, where $q_0 = y_i$ and $q_{-1} = y_{i-1}$ at that moment. The register $A$ has one bit more than $x$ so that $A - x$ cannot overflow when $x = -2^{n-1}$. In hardware, the $n/2$ partial products of line L8 go into a carry-save tree, and each negation $-x$ is the complement of $x$ plus a 1 that is added in the tree.

## Example

Multiply $x = 3$ by $y = -6$ with $n = 4$: $y = 1010$, and $x = 00011$, $-x = 11101$ in 5 bits. The radix-2 digits from position 0 up are $0, -1, +1, -1$, so $y = -2 + 4 - 8 = -6$.

| step | $(q_0, q_{-1})$ | operation (L3, L4) | $A$ after it | $A$ after L5 | $Q$ after L5 | $q_{-1}$ |
|---|---|---|---|---|---|---|
| start | | | | 00000 | 1010 | 0 |
| 1 | (0, 0) | none | 00000 | 00000 | 0101 | 0 |
| 2 | (1, 0) | $A - x$ | 11101 | 11110 | 1010 | 1 |
| 3 | (0, 1) | $A + x$ | 00001 | 00000 | 1101 | 0 |
| 4 | (1, 0) | $A - x$ | 11101 | 11110 | 1110 | 1 |

The low 8 bits of $(A, Q)$ are $1110\,1110$, which is $-18$. Three operations were needed. With radix 4, the groups $(y_1, y_0, y_{-1}) = (1, 0, 0)$ and $(y_3, y_2, y_1) = (1, 0, 1)$ give $q_0 = -2$ and $q_1 = -1$, so $P = -2 \cdot 3 - 1 \cdot 3 \cdot 4 = -18$ with two partial products. For $y = 0111\,1110$ the radix-2 digits are $-1$ at position 1 and $+1$ at position 7, two operations instead of six.

## Correctness

The radix-2 digits sum to $y$: $\sum_{i=0}^{n-1} (y_{i-1} - y_i) 2^i = \sum_{i=0}^{n-2} y_i 2^{i+1} - \sum_{i=0}^{n-1} y_i 2^i = -y_{n-1} 2^{n-1} + \sum_{i=0}^{n-2} y_i 2^i = y$, with $y_{-1} = 0$; the top term comes out with the negative weight of two's complement, which is why no sign correction is needed. The loop keeps the invariant that after $k$ steps the value of $(A, Q_{\text{top } k})$, read as a two's complement number scaled by $2^{-k}$, equals $x \sum_{i<k} (y_{i-1} - y_i) 2^i$, and that $A$ does not overflow. The radix-4 digits sum to $y$ by the same telescoping grouped in pairs. The full proof is below.

## Complexity

**Time, proved.** BOOTH runs exactly $n$ steps, each with one shift and at most one addition or subtraction of $n + 1$ bits, so $\Theta(n^2)$ bit operations in every case and $\Theta(n)$ extra bits for $A$ and $q_{-1}$.

**Number of additions, proved.** The number of operations in radix 2 is the number of nonzero digits $y_{i-1} - y_i$, that is the number of positions where $y_i \ne y_{i-1}$. It is at most $n$, reached by $y = \ldots 0101$, and it is at most $2r$ where $r$ is the number of runs of 1s. For a random $y$ each position differs from its neighbour with probability $1/2$, so the mean is $n/2$, the same as for plain shift-and-add: radix-2 Booth is a gain for multipliers with long runs, not on average. In radix 4 there are at most $\lceil n/2 \rceil$ nonzero digits; a digit is 0 exactly when its three bits are $000$ or $111$, so for random bits the mean number of nonzero digits is $3/4$ of $n/2$, that is $3n/8$.

**In hardware, observed.** A parallel multiplier with radix-4 recoding has $\lceil n/2 \rceil + 1$ rows to reduce instead of $n$, which saves about one level in a tree of carry-save adders and almost half the cells of an array; the recoding and the selection of $0, \pm x, \pm 2x$ cost a few gate delays.

## Properties

- **Signed with no correction.** The recoding gives the top bit its negative weight automatically, so the same steps multiply positive and negative numbers.
- **Digit alternation.** In radix 2, the nonzero digits alternate in sign, since a digit $-1$ starts a run and $+1$ ends it.
- **Not minimal.** Radix-2 Booth can produce more nonzero digits than plain binary, for example on $0101\ldots$. The [non-adjacent form](/non-adjacent-form/) has the fewest nonzero signed digits, at most $\lceil (n+1)/2 \rceil$, and about $n/3$ on average.
- **Local.** Each recoded digit depends on two or three neighbouring bits of $y$, so all digits are computed in parallel in constant depth.

## Variants and improvements

- **Radix 8 and higher.** Groups of four bits give digits in $\{-4, \ldots, 4\}$ and $\lceil n/3 \rceil$ partial products, but the multiple $3x$ needs a real addition, which is done once and stored.
- **Unsigned operands.** An unsigned $y$ is extended with a zero bit on top, which can add one more digit.
- **Booth in software.** On machines without a fast multiplier, and in multiplication by constants, recoding into signed digits, or better the non-adjacent form, reduces the number of shift-and-add steps; the same recoding is used for scalar multiplication on elliptic curves.
- **Combined with trees.** The modified Booth partial products are summed with [Wallace](/wallace-tree-multiplier/) or [Dadda](/dadda-multiplier/) trees and a final fast adder, the standard design of hardware multipliers.

## When to use it

Use radix-4 Booth recoding in a parallel hardware multiplier of signed numbers: it halves the number of partial products and handles signs for free. Use the radix-2 sequential form only when the multiplier often has long runs of 1s, or as a simple way to multiply signed numbers in a shift-and-add loop. In software on a word RAM, the machine's multiply instruction is faster, and for large numbers the limb algorithms of [integer multiplication](/integer-multiplication/) apply.

## Pitfalls

- **An accumulator with no spare bit.** With an $n$-bit $A$, line L3 computes $0 - x$ for $x = -2^{n-1}$, which overflows and gives the wrong sign. Line L1 must give $A$ one more bit than $x$, $n + 1$ bits.
- **A logical shift.** Line L5 with a logical shift fills the top of $A$ with 0 and turns negative partial sums into large positive ones. The right shift must copy the sign bit of $A$.
- **Forgetting $q_{-1}$.** Starting line L1 with $q_{-1}$ equal to anything but 0, or not shifting $y_0$ into it in line L5, shifts every digit by one place. The extra bit starts at 0 and receives $q_0$ at every shift.
- **Radix 4 on an odd number of bits.** Line L7 needs an even number of bits; for odd $n$, sign-extend $y$ by one bit first, or the top digit has the wrong weight.

## Implementations

## History

Andrew D. Booth found the method while working on the ARC computers at Birkbeck College, London, and published it in 1951 as a way to multiply signed binary numbers without separate sign handling; desk-calculator operators had long used the decimal shortcut of multiplying by 99 as 100 minus 1. MacSorley (1961) described recoding the multiplier two bits at a time into digits from $-2$ to $2$, the modified Booth algorithm, which halves the number of additions and became the standard in parallel multipliers.

## References
