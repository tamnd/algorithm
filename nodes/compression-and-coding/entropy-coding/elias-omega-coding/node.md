---
tag: 7AJD58
kind: algorithm
slug: elias-omega-coding
name: Elias omega coding
aliases:
- omega code
- Elias omega code
- recursive Elias code
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes x >= 1 as a chain of binary groups, each giving the length of the next, ended by a 0. The overhead above log2 x is a sum of iterated logarithms.
model: word-ram
complexity:
  vars: {x: the integer to code}
  time: {worst: Θ(log x), average: Θ(log x), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1975
  people: [Peter Elias]
  note: Elias defined omega in his 1975 paper on universal codes, as the recursive form of the idea behind the delta code.
prereqs: [elias-delta-coding, iterated-logarithm]
see_also: [elias-gamma-coding, universal-code, fibonacci-coding, kraft-inequality, floor-log2, prefix-code, variable-byte-encoding, unary-coding]
sources:
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 194 to 203 (the recursive codeword set omega)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 2, Entropy and Coding (variable-length codes for integers)
---

The Elias omega code writes an integer $x \ge 1$ as a chain of binary groups followed by one zero bit. The last group is $x$ in binary, the group before it is the bit length of $x$ minus one, written in binary, and so on, back to a group of two bits. Each group starts with a one bit, so the decoder knows that a zero ends the chain. The codeword length is $\log_2 x + \log_2 \log_2 x + \log_2\log_2\log_2 x + \cdots$ up to small terms. Peter Elias defined the code in 1975 as the recursive form of [delta coding](/elias-delta-coding/).

## In plain words

To read a number of unknown size, the reader must first know its number of digits. The [delta code](/elias-delta-coding/) gives that count in a short code. The omega code applies the same idea to the count, then to the count of the count, until the count is one.

The encoder works from the right. It writes a zero as the end mark, puts the number in binary in front of it, then puts in front the number of digits it just wrote, less one, and so on, until that value is one.

The decoder works from the left and starts with the value one. When it reads a one, a group follows: the one is its first digit, and the current value says how many more digits to read. The group gives the new value. When it reads a zero, the current value is the answer.

## The problem

The input is a sequence of integers $x_1, \ldots, x_n$, each at least 1, with no known upper bound. The output is one bit string from which a decoder recovers the sequence, with no separators and no parameters. The codeword should be as close as possible to the $\lfloor \log_2 x \rfloor + 1$ digits of $x$ for very large $x$.

Notation: $x$ is one integer to code, $\ell(x)$ is the codeword length in bits, and $\lfloor \log_2 x \rfloor + 1$ is the number of binary digits of $x$. All logarithms are base 2. Probability statements are for a memoryless source.

## The algorithm

```pseudo id=main
OMEGA-ENCODE(x, W)                         ▷ x ≥ 1, W is a bit writer
L1  S ← "0"                                ▷ the end mark
L2  while x > 1 do
L3      S ← (binary digits of x) · S       ▷ put the group in front
L4      x ← ⌊log₂ x⌋                       ▷ the group just written has x + 1 digits
L5  write S to W

OMEGA-DECODE(R)                            ▷ R is a bit reader
L6  x ← 1
L7  while READ-BIT(R) = 1 do               ▷ the 1 is the top digit of the next group
L8      x ← 2^x + (the next x bits of R, read as a binary number)
L9  return x
```

The encoder builds the codeword from the right, because each group depends on the group after it. Line L3 writes $x$ with its leading one, and line L4 replaces $x$ by its bit length minus one, which is the number of digits after the leading one. The loop stops when this value is 1: a group of value 1 would carry no information, because the decoder starts from 1 in line L6.

In the decoder, $x$ is always the number of digits that the next group has after its leading one. Line L7 reads one bit. A one is the leading digit of a group, and line L8 reads the other $x$ digits and makes them, with the leading one, the new $x$. A zero is the end mark.

The number of groups is the number of times that $x \mapsto \lfloor \log_2 x \rfloor$ can be applied before the value is 1, which is about the [iterated logarithm](/iterated-logarithm/) $\log^* x$. So the encoder needs a stack of about $\log^* x$ groups, which is at most 4 groups for $x < 2^{65536}$.

To code 0, code $x + 1$.

## Example

Encode $x = 1000$, binary `1111101000`, with the encoder state after each round:

| step | $x$ | $S$ |
|---|---|---|
| L1 | 1000 | `0` |
| L3, L4 | 9 | `1111101000` `0` |
| L3, L4 | 3 | `1001` `1111101000` `0` |
| L3, L4 | 1 | `11` `1001` `1111101000` `0` |

The codeword is `11 1001 1111101000 0`, 17 bits. The gamma codeword of 1000 has 19 bits and the delta codeword has 16 bits.

Decode it:

| step | bits read | $x$ |
|---|---|---|
| L6 | | 1 |
| L7, L8 | `1`, then 1 bit `1` | 3 |
| L7, L8 | `1`, then 3 bits `001` | 9 |
| L7, L8 | `1`, then 9 bits `111101000` | 1000 |
| L7 | `0` | return 1000 |

The first codewords. Spaces separate the groups.

| $x$ | codeword | $\ell(x)$ |
|---|---|---|
| 1 | 0 | 1 |
| 2 | 10 0 | 3 |
| 3 | 11 0 | 3 |
| 4 | 10 100 0 | 6 |
| 7 | 10 111 0 | 6 |
| 8 | 11 1000 0 | 7 |
| 15 | 11 1111 0 | 7 |
| 16 | 10 100 10000 0 | 11 |
| 100 | 10 110 1100100 0 | 13 |

## Correctness

In the decoder, this invariant holds before each test of line L7: the reader has read the groups of the codeword up to some group, and $x$ is the value of that group (or 1 at the start). Since the encoder wrote, in front of each group of value $v$, a group whose value is the number of digits of $v$ after its leading one, line L8 reads the next group in full and sets $x$ to its value. Each group starts with a one and the end mark is a zero, so line L7 stops exactly at the end mark, when $x$ is the coded value. The codeword set is prefix-free, because the decoder never reads past the end mark of a codeword and returns a different value on each codeword. The full proof is in the proof file.

## Complexity

**Length.** Let $N = \lfloor \log_2 x \rfloor$. The group of $x$ has $N + 1$ digits and the rest of the codeword is the codeword of $N$, so

$$\ell(1) = 1, \qquad \ell(x) = (\lfloor \log_2 x \rfloor + 1) + \ell(\lfloor \log_2 x \rfloor) \text{ for } x \ge 2.$$

Unrolled, $\ell(x) = 1 + \sum_i (\lfloor \log_2 x_i \rfloor + 1)$ over the chain $x_0 = x$, $x_{i+1} = \lfloor \log_2 x_i \rfloor$ while $x_i \ge 2$. This is $\log_2 x + \log_2 \log_2 x + \cdots$ plus about one bit per group. For example $\ell(2) = 3$, $\ell(4) = 6$, $\ell(16) = 11$ and $\ell(2^{16}) = 28$.

**Against delta.** The lengths depend only on $N$. The omega code is strictly shorter than the delta code for each $x \ge 2^{511}$, and for $N = 1, 3, 15, 127, 255$. For most $x$ below $2^{127}$, delta is shorter, by up to 3 bits (for example for $2^{16} \le x < 2^{31}$).

**Time.** The encoder and the decoder do $\Theta(\ell(x)) = \Theta(\log x)$ bit steps, and one step for $x = 1$. On a [word RAM](/word-ram/), each group that fits in a word takes $O(1)$ steps, so a codeword of $O(w)$ bits takes $O(\log^* x)$ steps. The encoder keeps about $\log^* x$ group values, which is $\Theta(1)$ words for any value that fits in memory.

**Kraft sum.** After each group, the next bit is either the end mark or the start of a group of a known length. So a random infinite bit string fails to reach an end mark only if it picks a one at each of infinitely many group boundaries, which has probability 0. The Kraft sum is 1 and the code is complete.

**Universality and asymptotic optimality.** $\ell(x) = \log_2 x + O(\log \log x)$, so $\ell(x)/\log_2 x \to 1$. For a non-increasing distribution with entropy $H$, the same argument as for delta, with $E[\log_2 x] \le H$ and Jensen's inequality, gives $E[\ell] \le H + O(\log H)$. So omega is an asymptotically optimal [universal code](/universal-code/).

## Properties

- **Parameter-free and complete.** No knowledge of the source is needed, and the Kraft sum is 1.
- **Asymptotically optimal**, with the smallest second-order term of the three Elias codes.
- **Recursive in definition, iterative in practice.** The encoder needs a short stack of about $\log^* x$ values, and the decoder needs one variable.
- **Fragile.** One wrong bit changes a group length or the end mark, and the decoder loses its place for the rest of the stream.

## Variants and improvements

- **Elias delta.** The [delta code](/elias-delta-coding/) stops after one level of length coding. It is shorter for most values that occur in practice.
- **Levenshtein code.** Levenshtein's 1968 code has the same recursive structure, but it writes the number of groups in unary at the front instead of an end mark at the back, and it leaves out the leading one of each group. It is described on the [universal code](/universal-code/) page.

## When to use it

Omega is the code of choice only when very large integers are common and every bit counts, for example in theory, in proofs of universality, or in the coding of unbounded counts inside other codes. For typical gaps and counts below $2^{64}$, the [delta code](/elias-delta-coding/) or the [gamma code](/elias-gamma-coding/) is as short or shorter, and the [Golomb](/golomb-coding/) and [variable-byte](/variable-byte-encoding/) codes are faster to decode.

## Pitfalls

- **Writing the bit length instead of the bit length minus one.** Line L4 must set $x \leftarrow \lfloor \log_2 x \rfloor$, the number of digits after the leading one. With $x \leftarrow \lfloor \log_2 x \rfloor + 1$, the loop of line L2 never reaches 1 for $x = 2$ (the value 2 maps to 2), and the encoder does not stop.
- **Building the chain from the left.** The groups must be written in the reverse of the order in which lines L3 and L4 compute them. An encoder that writes each group at once emits the groups in the wrong order; the decoder then reads the wrong lengths.
- **Forgetting the end mark.** Line L1 starts $S$ with the zero bit. Without it, the decoder of line L7 reads into the next codeword.
- **Group length on bad input.** Line L8 reads $x$ bits, and $x$ grows as a tower of powers of 2. A decoder for untrusted input must reject a group length above its word size before it reads the group.

## Implementations

## History

Peter Elias defined the gamma, delta and omega codes in 1975, in the paper that introduced universal codes for the integers. Levenshtein had published a code with the same recursive length structure in 1968, in Russian.

## References
