---
tag: JSK194
kind: algorithm
slug: binary-to-gray-conversion
name: Binary to Gray code conversion
aliases:
- binary-to-Gray
- g = b XOR (b >> 1)
- Gray code of a number
area: combinatorics/gray-codes
level: intro
summary: Computes the Gray code of b as b XOR (b shifted right by one) in constant word operations.
solves: [gray-code-conversion]
model: word-ram
complexity:
  vars: {n: the number of bits of b}
  time: {worst: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
prereqs: [binary-reflected-gray-code, bitwise-operations]
see_also: [gray-to-binary-conversion, gray-code-conversion, gray-code, ruler-sequence, k-ary-gray-code, bit-parity]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (the formula g(k) = k XOR floor(k/2) for the Gray binary code and the bitwise rule a_j = b_j XOR b_(j+1))
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 1, the section on the Gray code and parity (the routine gray_code(x) = x XOR (x >> 1))
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.2 (ranking and unranking the binary reflected Gray code)
---

Binary to Gray conversion maps a number $b$ to $g(b) = b \oplus \lfloor b/2 \rfloor$, the string of rank $b$ in the [binary reflected Gray code](/binary-reflected-gray-code/). In bits, the Gray code keeps the top bit of $b$, and each other bit is the exclusive or of a bit of $b$ and the bit to its left. On a [word RAM](/word-ram/) it takes one shift and one exclusive or, so the unrank function of the reflected code costs $O(1)$ time. The inverse map is [Gray to binary conversion](/gray-to-binary-conversion/).

## In plain words

Write the number in binary. Look at each pair of neighboring digits. If the two digits are the same, write 0. If they are different, write 1. For the leftmost digit, compare it with an extra 0 on its left. The digits you wrote form the Gray code of the number.

A computer does all the pairs at the same time. It slides a copy of the number one place to the right and compares the copy with the number, digit by digit. Where they differ it writes 1. That is one shift and one compare per number.

## The problem

Given an integer $b$ with $0 \le b < 2^n$, compute $g(b)$, the entry of rank $b$ in the reflected Gray code $\Gamma_n$ of $n$-bit strings. Here $n$ is the number of bits. We write $b = \sum_j b_j 2^j$ with bits $b_j \in \{0, 1\}$, so $b_j = 0$ for $j \ge n$, and the string $a_{n-1} \ldots a_0$ stands for $\sum_j a_j 2^j$. This is the "unrank" half of [Gray code conversion](/gray-code-conversion/).

## The algorithm

The first procedure works on a machine word. The second works on an array of bits, for numbers that do not fit in a word.

```pseudo id=main
TO-GRAY(b)                                ▷ b ≥ 0 fits in a word
L1  return b ⊕ ⌊b / 2⌋                    ▷ ⌊b / 2⌋ is the right shift b >> 1

TO-GRAY-BITS(b_0, ..., b_{n−1})           ▷ b_0 is the lowest bit
L2  b_n ← 0
L3  for j ← 0 to n − 1 do
L4      a_j ← b_j ⊕ b_{j+1}
L5  return (a_0, ..., a_{n−1})
```

Bit $j$ of $\lfloor b/2 \rfloor$ is $b_{j+1}$, so line L1 computes exactly the bits of line L4 for all $j$ at once.

## Example

Take $b = 13 = 1101_2$. Then $\lfloor 13/2 \rfloor = 0110_2 = 6$, and $1101 \oplus 0110 = 1011_2 = 11$. Bit by bit, with $b_4 = 0$: $a_3 = 1 \oplus 0 = 1$, $a_2 = 1 \oplus 1 = 0$, $a_1 = 0 \oplus 1 = 1$, $a_0 = 1 \oplus 0 = 1$. So $g(13) = 1011$, which is entry 13 of the 4-bit list 0000, 0001, 0011, 0010, 0110, 0111, 0101, 0100, 1100, 1101, 1111, 1110, 1010, 1011, 1001, 1000.

| $b$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| binary | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| $g(b)$ | 000 | 001 | 011 | 010 | 110 | 111 | 101 | 100 |

## Correctness

The claim is that, for each $n \ge 0$ and each $0 \le b < 2^n$, the entry of rank $b$ in $\Gamma_n$ has bits $a_j = b_j \oplus b_{j+1}$. The proof in `proofs/correctness.md` is by induction on $n$ with the definition $\Gamma_{n+1} = 0\Gamma_n,\ 1\Gamma_n^R$. In the second half, the rank $b = 2^{n+1} - 1 - c$ of the entry $1\Gamma_n[c]$ has the low $n$ bits of $c$ complemented. Complementing two neighbor bits does not change their exclusive or, and the new top bit is right because $b_n = 1$. Line L1 equals line L4 for each bit, because bit $j$ of $\lfloor b/2 \rfloor$ is $b_{j+1}$.

## Complexity

- **Word version.** TO-GRAY is one shift and one exclusive or, so $\Theta(1)$ time on a word RAM when $b$ fits in a word.
- **Bit version.** TO-GRAY-BITS takes $\Theta(n)$ time and $\Theta(n)$ space for the output. This is optimal for an output of $n$ separate bits.
- **Big integers.** For a number of $n$ bits stored in $\lceil n/w \rceil$ words of $w$ bits, the shift and the exclusive or take $\Theta(n/w)$ word operations.

## Properties

- **A bijection.** $g$ maps $\{0, \ldots, 2^n - 1\}$ onto itself, for each $n$. If $g(x) = g(y)$, then $z = x \oplus y$ satisfies $z = \lfloor z/2 \rfloor$, so $z = 0$.
- **Linear.** $g(x \oplus y) = g(x) \oplus g(y)$. As a map on $n$-bit vectors over GF(2), $g$ has a matrix with ones on the diagonal and on the diagonal next to it.
- **Same length.** $g(b)$ and $b$ have the same highest one bit, so $g(b) < 2^n$ exactly when $b < 2^n$.
- **Parity.** The number of ones in $g(b)$ is odd exactly when $b$ is odd. The exclusive or of all $a_j$ is $b_0 \oplus b_1 \oplus b_1 \oplus \cdots \oplus b_n = b_0$, because the inner terms cancel and $b_n = 0$.
- **Neighbors.** $g(b) \oplus g(b-1) = 2^{\rho(b)}$ for $b \ge 1$, where $\rho$ is the [ruler function](/ruler-sequence/).

## Variants and improvements

- **Inverse.** [Gray to binary conversion](/gray-to-binary-conversion/) computes $b$ from $g(b)$ by a prefix exclusive or.
- **Base $k$.** The reflected $k$-ary code has a similar digit rule: digit $j$ of the code is $b_j$ or $k - 1 - b_j$, by the parity of the higher digits. See [k-ary Gray code](/k-ary-gray-code/).
- **Many numbers at once.** The formula has no branch, so it vectorizes: apply it to each element of an array with SIMD instructions.

## When to use it

Use it to unrank the reflected Gray code: to find the code at a given position, to jump to the middle of a listing, or to split a listing among several workers. To list all codes in order, a [loopless generator](/loopless-gray-code-generation/) is as fast and keeps only one string. Use the bit version when the numbers are longer than a word.

## Pitfalls

- **Signed shift.** In languages where `>>` on a negative signed integer is an arithmetic shift, line L1 on a negative number keeps the sign bit and gives a wrong result. Use unsigned integers, or reject $b < 0$.
- **Wrong shift direction.** $b \oplus 2b$ is not the Gray code. For $b = 1$ it gives 3, but $g(1) = 1$. Line L1 needs the right shift $\lfloor b/2 \rfloor$.
- **Missing top bit.** In line L4 with $j = n - 1$ the code reads $b_n$. Line L2 must set $b_n = 0$, or the loop reads past the end of the array.
- **Using g as its own inverse.** $g(g(b)) \ne b$ in general: $g(g(2)) = g(3) = 2$ by luck, but $g(g(4)) = g(6) = 5$. Decode with the prefix exclusive or.

## Implementations

## History

The formula comes with the reflected code itself. Knuth, in Section 7.2.1.1, gives $g(k) = k \oplus \lfloor k/2 \rfloor$ and the rule $a_j = b_j \oplus b_{j+1}$, and traces the code to Frank Gray's patent of 1953 and earlier sources.

## References
