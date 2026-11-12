---
tag: YCM9KR
kind: data-structure
slug: standard-array
name: Standard array
aliases:
- coset table
- Slepian array
area: compression-and-coding/error-correcting-codes
level: core
summary: A table of all q^n words of a linear code's space, one row per coset with a least weight leader first. A word decodes to the codeword at the top of its column.
model: word-ram
complexity:
  vars: {n: the code length, q: the field size}
  time: {expected: Θ(n), total: Θ(q^n n)}
  space: {extra: Θ(q^n n)}
history:
  year: 1956
  people: [David Slepian]
  note: Slepian described binary group codes as cosets of a subgroup and arranged all words in a table of cosets, with a decoder that reads the codeword at the head of the column.
prereqs: [linear-code, hamming-weight]
see_also: [syndrome-decoding, syndrome, maximum-likelihood-decoding, binary-symmetric-channel, hamming-bound, nearest-codeword-problem, minimum-distance, hamming-code]
sources:
  - paper: doi:10.1002/j.1538-7305.1956.tb02379.x
    title: David Slepian, A class of binary signaling alphabets, Bell System Technical Journal 35(1), 1956, pages 203 to 234
    locator: The group alphabets, their decomposition into cosets, and the table of cosets used for maximum likelihood detection
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.5 (standard array and syndrome decoding, coset leaders, and the probability of a decoding error)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the standard array, cosets and coset leaders)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (standard arrays and syndrome decoding)
---

The standard array of a [linear code](/linear-code/) $C$ is a table of all $q^n$ words of length $n$, with one row for each coset of $C$. The first row is the code itself, and each other row starts with a word of least weight in its coset, the coset leader, followed by the leader plus each codeword. A received word is decoded to the codeword at the top of its column, and this is a nearest codeword decoder. David Slepian introduced the table in 1956; it is the textbook picture behind [syndrome decoding](/syndrome-decoding/), which keeps only the leaders.

## In plain words

Write every possible received word in one big table. The top row holds the valid codewords. To make the next row, take the lightest word, the one with the fewest nonzero symbols, that is not yet in the table, and add it to each word of the top row. Repeat until every word is in the table.

Each row is a group of words that look alike to the parity checks, and its first word is the smallest error that explains the whole group. To decode, find the received word in the table and read the codeword at the top of its column. That is the same as guessing that the smallest error in the group happened.

The table is too large for real codes. It is a way to understand decoding, and a check for small examples.

## The abstract type

The standard array stores a partition of $\mathrm{GF}(q)^n$ into the cosets of $C$, with a chosen representative in each coset, and answers one query:

- DECODE$(r)$: return a codeword $c \in C$ with the least [Hamming distance](/hamming-distance/) $d(r, c)$.

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with $M = q^k$ codewords, generator matrix $G$ ($c = m G$) and parity-check matrix $H$ ($H c^T = 0$). Vectors are rows. $\mathrm{wt}$ is the [Hamming weight](/hamming-weight/), and $t = \lfloor (d - 1)/2 \rfloor$. The channel is a [binary symmetric channel](/binary-symmetric-channel/) BSC($p$) with $p < 1/2$, or its $q$-ary form, with hard decisions.

A **coset** of $C$ is a set $a + C = \{\, a + c : c \in C \,\}$. Two cosets are equal or disjoint, each has $q^k$ words, so there are $q^{n-k}$ of them. A **coset leader** is a word of least weight in its coset.

## Representation

The array has $q^{n-k}$ rows and $q^k$ columns. Fix an order $c_0 = 0, c_1, \ldots, c_{M-1}$ of the codewords. Row $i$ has a leader $\ell_i$, and its entry in column $j$ is

$$A[i][j] = \ell_i + c_j .$$

Row 0 has $\ell_0 = 0$, so it is the code. Column $j$ holds the words that decode to $c_j$. The implementation also keeps an index, a hash map from each word to its place $(i, j)$, so that a lookup does not scan the table.

## Operations

```pseudo id=main
BUILD-STANDARD-ARRAY(C)          ▷ codewords c_0 = 0, c_1, ..., c_(M − 1)
L1  row 0 ← (c_0, c_1, ..., c_(M − 1))
L2  for each v in GF(q)^n, by increasing weight do
L3      if v is in no row yet then
L4          ℓ ← v                                     ▷ the coset leader
L5          append the row (ℓ + c_0, ℓ + c_1, ..., ℓ + c_(M − 1))
L6          mark each entry of the new row as used
L7      if there are q^(n − k) rows then return the rows
```

```pseudo id=decode
DECODE(r)
L8  find the row i and the column j with r = ℓ_i + c_j
L9  return c_j
```

Line L2 visits the words in order of weight. Words of the same weight may come in any fixed order; the implementation reads them as numbers with the first position most significant and takes the largest first. The order only decides between leaders of equal weight.

The error pattern that DECODE assumes is $r - c_j = \ell_i$, the leader of the row.

## Example

The binary $[5, 2, 3]$ code with generator rows $10110$ and $01011$ has the codewords $c_0 = 00000$, $c_1 = 01011$, $c_2 = 10110$, $c_3 = 11101$, and $q^{n-k} = 8$ cosets. Line L2 takes the zero word (already in row 0), then the five words of weight 1, each in a new coset, then words of weight 2. The first weight 2 word that is not yet used is $11000$, and the next is $10001$. Then all 32 words are used.

| leader | $c_0 = 00000$ | $c_1 = 01011$ | $c_2 = 10110$ | $c_3 = 11101$ |
|---|---|---|---|---|
| 00000 | 00000 | 01011 | 10110 | 11101 |
| 10000 | 10000 | 11011 | 00110 | 01101 |
| 01000 | 01000 | 00011 | 11110 | 10101 |
| 00100 | 00100 | 01111 | 10010 | 11001 |
| 00010 | 00010 | 01001 | 10100 | 11111 |
| 00001 | 00001 | 01010 | 10111 | 11100 |
| 11000 | 11000 | 10011 | 01110 | 00101 |
| 10001 | 10001 | 11010 | 00111 | 01100 |

**Decoding.** The word $r = 11100$ is in the row of $00001$, column $c_3$, so DECODE returns $11101$: one error, in the last position.

**Ties.** The row of $11000$ also holds $00101$, another word of weight 2. The row of $10001$ also holds $01100$. So a word such as $r = 00101$ is at distance 2 from both $c_0$ and $c_3$. The array decodes it to $c_3$, because L2 chose $11000$ as the leader. A different order of equal weight words gives a different, equally good, decoder.

**Error rate.** A sent codeword is decoded correctly exactly when the error is a coset leader (see Correctness). On BSC($p$) the leaders are one word of weight 0, five of weight 1 and two of weight 2, so

$$P_c = (1 - p)^5 + 5 p (1 - p)^4 + 2 p^2 (1 - p)^3 .$$

At $p = 0.1$ this is $0.59049 + 0.32805 + 0.01458 = 0.93312$, so the block error rate is $0.06688$.

## Correctness

The full proof is in the proofs file. In outline:

- **The rows are distinct cosets.** Line L5 writes the coset $\ell + C$. Line L3 picks $\ell$ only if it is in no earlier row. If $\ell + C$ were an earlier row, $\ell$ would be in it. Distinct cosets are disjoint, so no word appears twice.
- **The rows cover all words.** Every word is visited by L2 and is either already used or becomes a leader. The cosets have $q^k$ words each, so when there are $q^{n-k}$ rows at line L7, all $q^n$ words are used.
- **Each leader has least weight in its row.** The leader $\ell$ is the first word of its coset in the order of L2. A lighter word $x$ of the same coset comes earlier; at that time $x$ was either unused, and would have started this coset, or used, and then the coset was already a row. Both contradict the choice of $\ell$.
- **DECODE returns a nearest codeword.** If $r = \ell_i + c_j$, then for each codeword $c$, $r - c$ is in the coset of $r$, so $d(r, c) = \mathrm{wt}(r - c) \ge \mathrm{wt}(\ell_i) = d(r, c_j)$.

So the array implements minimum distance decoding, which equals [maximum likelihood decoding](/maximum-likelihood-decoding/) on BSC($p$) with $p < 1/2$. If $c$ is sent and $e$ is the error, the received word $c + e$ is in the row of $e + C$, at the column of $c + e - \ell$. This is $c$ if and only if $e = \ell$. So the decoder corrects exactly the error patterns that are coset leaders. Every word of weight at most $t$ is the only word of least weight in its coset, since two such words differ by a codeword of weight at most $2t < d$. So every error of weight at most $t$ is corrected.

## Complexity

| operation | time | space |
|---|---|---|
| BUILD-STANDARD-ARRAY | $\Theta(q^n n)$ field operations | $\Theta(q^n n)$ symbols |
| DECODE, by a scan of the array | $O(q^n n)$ | none |
| DECODE, with the index of the places | $\Theta(n)$ expected, to hash $r$ | $\Theta(q^n n)$ for the index |
| syndrome table instead of the array | $\Theta(n (n - k))$ for $H r^T$ | $\Theta(q^{n-k} n)$ |

BUILD writes $q^n$ words of $n$ symbols, and the loop of L2 also generates up to $q^n$ words. The last row of the table shows the cost of the alternative: the [syndrome decoding](/syndrome-decoding/) table keeps only the $q^{n-k}$ leaders, indexed by $H r^T$. For the binary $[23, 12, 7]$ Golay code the array has $2^{23} = 8388608$ entries, and the syndrome table has $2^{11} = 2048$.

## Variants

- **Syndrome table.** Keep only the first column and index it by the syndrome $H \ell^T$. This is [syndrome decoding](/syndrome-decoding/), with the same output as the array.
- **Incomplete decoding.** Keep only the rows whose leader has weight at most $t$. A received word in another row is reported as an error that cannot be corrected. This is bounded distance decoding: it detects more errors and corrects fewer.
- **Coset leader weight distribution.** The number $\alpha_w$ of leaders of weight $w$ gives the exact correct decoding probability on BSC($p$), $P_c = \sum_w \alpha_w p^w (1 - p)^{n - w}$. The largest leader weight is the covering radius of the code.
- **Perfect codes.** If every leader has weight at most $t$, the balls of radius $t$ around the codewords fill the space and the code meets the [Hamming bound](/hamming-bound/) with equality. The [Hamming code](/hamming-code/) has exactly the zero leader and the $n$ leaders of weight 1.
- **Other channels.** For a channel other than BSC($p$) with $p < 1/2$, a leader must be the most probable error of its coset, not the lightest. The table shape stays the same.

## When to use it

Use the standard array to teach or to check syndrome decoding, to find the coset leader weight distribution and the covering radius of a small code, and as an exhaustive reference decoder in tests. Do not use it as a decoder for a real code: it needs $q^n$ entries, while the syndrome table needs $q^{n-k}$, and algebraic or iterative decoders need far less. For codes with large $n - k$ even the syndrome table is too large; the general problem is the [nearest codeword problem](/nearest-codeword-problem/), which is NP-hard.

## Pitfalls

- **Leaders not of least weight.** If line L2 visits words in another order, a leader can be heavy, and DECODE is then not a nearest codeword decoder. In the example, with $11011$ as the leader of its row instead of $10000$, the word $10000 = 11011 + 01011$ decodes to $01011$, at distance 4, instead of $00000$, at distance 1.
- **No test for used words.** Without line L3, a word of an existing coset starts a second copy of that coset. The rows are no longer disjoint, and line L7 stops before some cosets appear, so some words are not in the array.
- **Assuming unique decoding beyond t.** Leaders of weight more than $t$ may have ties, as $11000$ and $00101$ in the example. Line L4 picks one, and the decoder is still nearest, but it is not the only nearest decoder, and the error rate depends on the choice only through the number of leaders of each weight.
- **The wrong column.** DECODE must return the codeword at the head of the column, $c_j$, not the leader $\ell_i$ (the error estimate) and not the row index.

## Implementations

## History

David Slepian studied binary codes that are closed under addition modulo 2, which he called group alphabets, in the Bell System Technical Journal in 1956. He described them as subgroups of the group of binary words, and he decomposed the space into cosets of the code to give a simple maximum likelihood detector for the binary symmetric channel: the table that textbooks now call the standard array, or the Slepian array. The name coset leader comes from this table. Later texts replaced the full table by the table of syndromes.

## References
