---
tag: 09XZRF
kind: algorithm
slug: gray-to-binary-conversion
name: Gray to binary conversion
aliases:
- Gray-to-binary decoding
- prefix XOR of Gray code
- rank of a Gray code
area: combinatorics/gray-codes
level: intro
summary: Recovers binary from Gray code by a running XOR from the most significant bit down.
solves: [gray-code-conversion]
model: word-ram
complexity:
  vars: {n: the number of bits of the code, w: the word size}
  time: {worst: Θ(n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
prereqs: [binary-to-gray-conversion, bitwise-operations, prefix-sums]
see_also: [binary-to-gray-conversion, gray-code-conversion, binary-reflected-gray-code, bit-parity, ranking-unranking, gray-code]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (the inverse of the Gray binary code, b_j = a_j XOR a_(j+1) XOR ..., and the form a XOR floor(a/2) XOR floor(a/4) XOR ...)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 1, the section on the Gray code and parity (the inverse Gray code by shifts of 1, 2, 4, ...)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.2 (ranking the binary reflected Gray code)
---

Gray to binary conversion takes a string $a$ of the [binary reflected Gray code](/binary-reflected-gray-code/) and returns its rank $b$, the number with $a = b \oplus \lfloor b/2 \rfloor$. Bit $j$ of $b$ is the exclusive or of all bits of $a$ at position $j$ or higher, so $b$ is the prefix exclusive or of $a$ read from the top bit down. A loop over the bits takes $\Theta(n)$ steps for an $n$-bit code. On a [word RAM](/word-ram/) with $w$-bit words, shifts by $1, 2, 4, \ldots$ take $\lceil \lg w \rceil$ steps.

## In plain words

Read the Gray code from the left. Keep one running bit, which starts at 0. For each digit of the code, if the digit is 1, flip the running bit. After each digit, write the running bit down. The digits you wrote are the number in binary.

This undoes the forward conversion. The forward step wrote, for each position, whether two neighbor digits of the number differ. Reading from the left, you know the digit on the left, and the code digit tells you whether the next digit is the same or different.

A computer can do it faster on a whole word. It combines the word with a copy shifted by one place, then by two places, then by four, and so on. Each round doubles how far the running flips reach.

## The problem

Given an $n$-bit string $a = a_{n-1} \ldots a_0$, stored as the integer $\sum_j a_j 2^j$, find the integer $b$ with $0 \le b < 2^n$ and $b \oplus \lfloor b/2 \rfloor = a$. This is the rank of $a$ in the reflected code $\Gamma_n$, and the "rank" half of [Gray code conversion](/gray-code-conversion/). Here $n$ is the number of bits and $w$ is the word size.

## The algorithm

The first procedure works for an integer of any length. The second works on one word in $\lceil \lg w \rceil$ rounds.

```pseudo id=main
FROM-GRAY(a)                              ▷ a ≥ 0
L1  b ← 0
L2  while a ≠ 0 do
L3      b ← b ⊕ a
L4      a ← ⌊a / 2⌋
L5  return b

FROM-GRAY-FAST(a, w)                      ▷ 0 ≤ a < 2^w
L6  s ← 1
L7  while s < w do
L8      a ← a ⊕ ⌊a / 2^s⌋
L9      s ← 2s
L10 return a
```

FROM-GRAY adds up the shifted copies $a, \lfloor a/2 \rfloor, \lfloor a/4 \rfloor, \ldots$ with exclusive or. FROM-GRAY-FAST gets the same sum by doubling: after the round with shift $s$, each bit holds the exclusive or of a window of $2s$ bits of the input.

## Example

Take $a = 1011_2 = 11$.

| step | $a$ | $b$ |
|---|---|---|
| start | 1011 | 0000 |
| L3, L4 | 0101 | 1011 |
| L3, L4 | 0010 | 1110 |
| L3, L4 | 0001 | 1100 |
| L3, L4 | 0000 | 1101 |

The result is $b = 1101_2 = 13$, and indeed $13 \oplus 6 = 11$. FROM-GRAY-FAST with $w = 4$ does two rounds: $1011 \oplus 0101 = 1110$, then $1110 \oplus 0011 = 1101$. Bit by bit from the top: $b_3 = 1$, $b_2 = 1 \oplus 0 = 1$, $b_1 = 1 \oplus 1 = 0$, $b_0 = 0 \oplus 1 = 1$.

## Correctness

The full proof is in `proofs/correctness.md`. If $a = b \oplus \lfloor b/2 \rfloor$, then $a_i = b_i \oplus b_{i+1}$, and the sum $a_j \oplus a_{j+1} \oplus \cdots \oplus a_{n-1}$ telescopes to $b_j \oplus b_n = b_j$. So the rank has bits $b_j = \bigoplus_{i \ge j} a_i$. FROM-GRAY computes this: after $t$ rounds, $b = \bigoplus_{r=0}^{t-1} \lfloor a_0 / 2^r \rfloor$ for the input $a_0$, and bit $j$ of $\lfloor a_0/2^r \rfloor$ is bit $j + r$ of $a_0$. The loop stops after exactly as many rounds as $a_0$ has bits, because each round removes one bit. For FROM-GRAY-FAST, the invariant of line L7 is that bit $j$ of $a$ is the exclusive or of the input bits $j$ to $j + s - 1$. Line L8 joins two windows of length $s$ into one of length $2s$. When the loop stops, $s \ge w$, and each window reaches past the top bit of the input.

## Complexity

- **FROM-GRAY.** The loop runs once for each bit of $a$, so $\Theta(n)$ word operations for an $n$-bit code that fits in a word, and $\Theta(1)$ when $a = 0$.
- **FROM-GRAY-FAST.** $\lceil \lg w \rceil$ rounds, each with one shift and one exclusive or, so $\Theta(\log w)$ for each word, whatever the value of $a$.
- **Bit arrays.** With the bits in an array, $b_{n-1} = a_{n-1}$ and $b_j = a_j \oplus b_{j+1}$ for $j$ from $n - 2$ down to 0. This takes $\Theta(n)$ time, which is optimal: bit $b_0$ is the [parity](/bit-parity/) of all bits of $a$, so each bit of the input must be read.

## Properties

- **The inverse of $g$.** The map is the inverse of [binary to Gray conversion](/binary-to-gray-conversion/), so it is a bijection on $\{0, \ldots, 2^n - 1\}$ and it is linear over exclusive or.
- **The lowest bit is the parity.** $b_0 = a_0 \oplus a_1 \oplus \cdots \oplus a_{n-1}$. So the rank of a code is odd exactly when the code has an odd number of ones.
- **A prefix scan.** The bits of $b$ are the [prefix sums](/prefix-sums/) of the bits of $a$ modulo 2, taken from the top bit down. FROM-GRAY-FAST is the doubling scheme of a parallel prefix scan, applied inside one word.

## Variants and improvements

- **From the top down on arrays.** The array form above is the "running exclusive or" of the summary. It needs no shifts and works for codes of any length.
- **Several words.** For a long code split into words, convert each word with FROM-GRAY-FAST from the top word down, and flip a word when the parity of all higher words is 1.
- **Parity instructions.** On a machine with a fast population count, $b_j$ is the parity of $\lfloor a / 2^j \rfloor$, so one bit can be found without the others.
- **Base $k$.** The reflected $k$-ary code has a similar inverse: digit $j$ of the rank is $a_j$ or $k - 1 - a_j$, by the parity of the sum of the higher digits of the code. See [k-ary Gray code](/k-ary-gray-code/).

## When to use it

Use it to rank a Gray code: to read the position of a Gray coded encoder as a number, to find where a string sits in the reflected listing, or to sort Gray coded keys by their rank. Use FROM-GRAY-FAST for words of a fixed size, because its time does not depend on the value. Use the array form for long codes.

## Pitfalls

- **Applying $g$ again.** $a \oplus \lfloor a/2 \rfloor$ is the forward map, not the inverse. For $a = 6$ it gives 5, but the rank of $110$ is 4. Line L3 must add all shifts, not only the shift by one.
- **A word size that is too small.** Line L7 must run until $s \ge w$ for a $w$ at least the bit length of $a$. With $w = 32$ on a 64-bit value, bits above position 32 do not reach the low bits, and the result is wrong.
- **The wrong direction on arrays.** The rule $b_j = a_j \oplus b_{j+1}$ needs $b_{j+1}$ first, so the loop must go from the top bit down. A loop from bit 0 upward computes a different map.
- **Signed shift.** As in the forward map, line L4 or line L8 on a negative signed integer with an arithmetic shift does not stop or gives a wrong result. Use unsigned integers.

## Implementations

## History

Knuth, in Section 7.2.1.1, gives the inverse rule $b_j = a_j \oplus a_{j+1} \oplus \cdots \oplus a_{n-1}$ next to the forward formula $g(k) = k \oplus \lfloor k/2 \rfloor$, and the shift method $b = a \oplus \lfloor a/2 \rfloor \oplus \lfloor a/4 \rfloor \oplus \cdots$. The doubling form for a word is a standard trick of bit manipulation; Arndt gives it in Chapter 1 of Matters Computational.

## References
