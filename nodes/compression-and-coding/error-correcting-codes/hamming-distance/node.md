---
tag: ZXVGP4
kind: definition
slug: hamming-distance
name: Hamming distance
aliases:
- Hamming distance between equal-length strings
- Hamming metric
area: compression-and-coding/error-correcting-codes
level: intro
summary: The number of positions in which two words of the same length differ. It is a metric on words of length n and the distance that block codes use.
prereqs: [metric-space]
see_also: [hamming-weight, minimum-distance, binary-symmetric-channel, maximum-likelihood-decoding, population-count, hamming-string-matching, edit-distance, hamming-bound]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: The geometric model of a code on the unit cube, with the distance D(x, y) as the number of coordinates in which x and y differ, and the proof that it is a metric
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 3.3 (the Hamming weight and the Hamming distance of binary n-tuples, the triangle inequality, and minimum distance)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 1.3 (block codes and the Hamming distance over any alphabet) and Chapter 4 (bounds on the parameters of codes, which use the volume of a Hamming ball)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 13 (binary codes, distance properties and the decoding sphere)
---

The Hamming distance between two words of the same length is the number of positions in which they differ. On the set of words of length $n$ over a fixed alphabet it is a [metric](/metric-space/), and it is the distance that block codes use: a code that keeps its codewords far apart in this distance can detect and correct errors that change few symbols. Over a field, the distance of two words is the [Hamming weight](/hamming-weight/) of their difference.

## Definition

Let $\Sigma$ be a finite alphabet with $q = |\Sigma| \ge 2$ symbols, and let $n \ge 0$. A *word* of length $n$ is an element $x = (x_1, \ldots, x_n)$ of $\Sigma^n$. The **Hamming distance** of two words $x, y \in \Sigma^n$ is

$$d(x, y) = \bigl|\{\, i \in \{1, \ldots, n\} : x_i \ne y_i \,\}\bigr|.$$

It is not defined for words of different lengths.

**It is a metric.** For all $x, y, z \in \Sigma^n$:

1. $d(x, y) \ge 0$, and $d(x, y) = 0$ if and only if $x = y$. A count of positions is at least 0, and it is 0 exactly when no position differs.
2. $d(x, y) = d(y, x)$, because $x_i \ne y_i$ is a symmetric condition.
3. $d(x, z) \le d(x, y) + d(y, z)$. If $x_i \ne z_i$, then $x_i \ne y_i$ or $y_i \ne z_i$, since otherwise $x_i = y_i = z_i$. So the set of positions where $x$ and $z$ differ is inside the union of the two other sets, and the size of a union is at most the sum of the sizes.

**Over a group or a field.** If $\Sigma$ is an abelian group, for example $\mathrm{GF}(q)$ or $\mathbb{Z}_q$, then $x_i \ne y_i$ exactly when $x_i - y_i \ne 0$, so

$$d(x, y) = \mathrm{wt}(x - y), \qquad d(x + z, y + z) = d(x, y),$$

where $\mathrm{wt}$ is the [Hamming weight](/hamming-weight/), the number of nonzero coordinates. The second equation (translation invariance) holds because $(x + z) - (y + z) = x - y$. For binary words held in machine words, $x - y = x \oplus y$, so $d(x, y)$ is the [population count](/population-count/) of $x \oplus y$.

**Spheres and balls.** The number of words at distance exactly $i$ from a fixed word is $\binom{n}{i}(q - 1)^i$: choose the $i$ positions that change, then one of the $q - 1$ other symbols at each position. So the Hamming ball of radius $r$ has

$$V_q(n, r) = \sum_{i=0}^{r} \binom{n}{i} (q - 1)^i$$

words, the same for every center. This volume is the base of the [Hamming bound](/hamming-bound/) and the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/).

## Examples and non-examples

**Examples.**

- $d(1011101, 1001001) = 2$: the words differ in the third and the fifth positions. As integers, $1011101_2 \oplus 1001001_2 = 0010100_2$, which has two 1 bits.
- $d(\text{karolin}, \text{kathrin}) = 3$ over the Latin alphabet: the positions 3, 4 and 5 hold r, o, l in one word and t, h, r in the other.
- Over $\mathbb{Z}_5$, $d((2, 1, 7 \bmod 5, 3), (2, 2, 3, 3)) = 2$, since the difference $(0, 4, 4, 0)$ has two nonzero entries.
- The words of length $n$ over $\{0, 1\}$ are the corners of the $n$-dimensional cube, and $d(x, y)$ is the number of edges on a shortest path between the corners $x$ and $y$.
- $V_2(7, 1) = 1 + 7 = 8$ and $V_2(23, 3) = 1 + 23 + 253 + 1771 = 2048 = 2^{11}$. So the 16 balls of radius 1 around the codewords of the [Hamming code](/hamming-code/) of length 7 fill all $2^7 = 128$ words, and the $2^{12}$ balls of radius 3 around the codewords of the binary [Golay code](/golay-code/) fill all $2^{23}$ words.
- **Maximum likelihood on a BSC.** On a [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $p$, a sent word $x$ becomes the word $y$ with probability $p^{d}(1 - p)^{n - d} = (1 - p)^n \bigl(p / (1 - p)\bigr)^{d}$, where $d = d(x, y)$. For $p < 1/2$ the ratio $p / (1 - p)$ is less than 1, so this probability falls as $d$ grows. So on this channel, [maximum likelihood decoding](/maximum-likelihood-decoding/) is decoding to a nearest codeword in Hamming distance.

**Non-examples.**

- **Words of different lengths.** "cat" and "cats" have no Hamming distance. The [edit distance](/edit-distance/) counts insertions and deletions as well as substitutions and is defined for any two strings; for words of the same length it is at most the Hamming distance (for example 01 and 10 have Hamming distance 2 and edit distance 2, but 0101 and 1010 have Hamming distance 4 and edit distance 2).
- **The size of the change.** In $\mathbb{Z}_8$ the words $(0)$ and $(1)$, and the words $(0)$ and $(4)$, are both at Hamming distance 1. The Hamming distance counts only whether a symbol changed, not by how much. The Lee distance and the Euclidean distance measure the size.
- **Counting differing bits of multi-bit symbols.** Over $\mathrm{GF}(2^8)$ a word of bytes $(\mathtt{00}, \mathtt{00})$ and $(\mathtt{FF}, \mathtt{01})$ are at Hamming distance 2 (two symbols differ), although nine bits differ. The distance of a code over $\mathrm{GF}(2^8)$, such as a [Reed-Solomon code](/reed-solomon-code/), counts symbols.

## Related definitions

- [Hamming weight](/hamming-weight/): $\mathrm{wt}(x) = d(x, 0)$, the number of nonzero coordinates.
- [Minimum distance](/minimum-distance/): the least Hamming distance between two different codewords of a code. It fixes how many errors the code detects and corrects.
- [Binary symmetric channel](/binary-symmetric-channel/): the channel model under which the Hamming distance is the right measure of how far apart a sent and a received word are.
- [Hamming string matching](/hamming-string-matching/) and the [k-mismatch problem](/k-mismatch-problem/): find the places where a pattern occurs in a text with at most $k$ mismatches, a string search problem built on the same distance. The [gap Hamming distance](/gap-hamming-distance/) problem is a communication problem on it.
- [Edit distance](/edit-distance/): the distance with insertions and deletions, for strings of any lengths.
- [Population count](/population-count/): the machine operation that computes the distance of two bit vectors from their XOR.

## References
