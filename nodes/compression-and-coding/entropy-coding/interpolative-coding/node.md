---
tag: TZXH8F
kind: algorithm
slug: interpolative-coding
name: Binary interpolative coding
aliases:
- interpolative coding
- binary interpolative code
area: compression-and-coding/entropy-coding
level: research
summary: Codes a sorted list by writing its middle element within the range its neighbors and bounds allow, then each half with tighter bounds. Runs of consecutive integers cost 0 bits.
model: word-ram
complexity:
  vars: {n: the count of integers, u: the size of the range of values}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(log n)}
properties: {deterministic: true, online: false, recursive: true}
history:
  year: 1996
  people: [Alistair Moffat, Lang Stuiver]
  note: Moffat and Stuiver presented the method at the Data Compression Conference in 1996 and gave the full account in Information Retrieval in 2000.
prereqs: [recursion, golomb-coding]
see_also: [pfor-delta, elias-fano-encoding, variable-byte-encoding, elias-gamma-coding, delta-encoding, binary-search, inverted-index, enumerative-coding]
sources:
  - paper: doi:10.1023/A:1013002601898
    title: Alistair Moffat and Lang Stuiver, Binary interpolative coding for effective index compression, Information Retrieval 3(1), 2000
    locator: pp. 25 to 47 (the recursive method, centered minimal binary codes, and the experiments on inverted files)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 3.5, Interpolative, and Fig. 4 (arXiv:1908.10598v2)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, second edition, Morgan Kaufmann, 1999
    locator: Chapter 3, Indexing (compression of inverted files, interpolative coding)
---

Binary interpolative coding (BIC) codes a strictly increasing list of integers, such as a posting list, without taking gaps. It writes the middle element first. The bounds of the list and the number of elements on each side limit where the middle element can be, so it takes only about $\log$ of the size of that range in bits. Then it codes the left half and the right half the same way, with the middle element as a new bound. When a sublist has no freedom left, because its elements must be consecutive integers, it costs 0 bits. This makes BIC one of the most compact codes for clustered posting lists, at the price of slow, serial decoding. Alistair Moffat and Lang Stuiver introduced it in 1996.

## In plain words

Suppose you must send 11 sorted numbers, all between 0 and 62. Send the middle one first, the 6th. Five smaller numbers come before it and five larger ones come after it, so it is at least 5 and at most 57. You only need to say where it is in that smaller range.

Now the left five numbers lie between 0 and the middle number, and the right five lie between the middle number and 62. Do the same on each side, again and again. The ranges get tighter as you go down.

If some numbers are packed together with no holes, then at some point a range has exactly as many places as numbers. Then there is nothing to say, and those numbers cost nothing.

## The problem

The input is a strictly increasing list $S[0] < S[1] < \cdots < S[n-1]$ of integers in a known range $[l, h]$, for example the document numbers of one term in an inverted index, with $l = 0$ and $h$ the largest document number. The task is the shortest practical code for the list, given that the decoder knows $n$, $l$ and $h$. The lists are often *clustered*: related documents have close numbers, so the list has dense runs and long gaps. Codes that work on gaps one at a time, such as [Elias gamma](/elias-gamma-coding/) or [Golomb](/golomb-coding/) codes, pay at least one bit per element even inside a dense run.

Notation: $n$ is the count of integers, $u = h - l + 1$ is the size of the range, $\ell$ is a codeword length, and logarithms are base 2. A sublist $S[i..j]$ has $j - i + 1$ elements and bounds $l', h'$ with $l' \le S[i]$ and $S[j] \le h'$.

## The algorithm

```pseudo id=main
BIC-ENCODE(S[0..n−1], l, h, W)             ▷ l ≤ S[0] < ... < S[n−1] ≤ h
L1  T ← a stack holding (0, n − 1, l, h)
L2  while T is not empty: pop (i, j, l', h') from T
L3      if i > j or h' − l' = j − i then continue   ▷ empty, or a run: 0 bits
L4      m ← i + ⌊(j − i)/2⌋
L5      write S[m] − l' − (m − i) to W with a minimal binary code for 0 .. h' − l' − (j − i)
L6      push (m + 1, j, S[m] + 1, h'); then push (i, m − 1, l', S[m] − 1)

BIC-DECODE(n, l, h, R)
L7  T ← a stack holding (0, n − 1, l, h)
L8  while T is not empty: pop (i, j, l', h') from T
L9      if i > j then continue; if h' − l' = j − i then S[i..j] ← l', l' + 1, ..., h'; continue
L10     m ← i + ⌊(j − i)/2⌋; S[m] ← l' + (m − i) + READ-MINIMAL-BINARY(R, h' − l' − (j − i))
L11     push (m + 1, j, S[m] + 1, h'); then push (i, m − 1, l', S[m] − 1)
L12 return S
```

The middle element $S[m]$ has $m - i$ elements before it in the sublist, all distinct and at least $l'$, so $S[m] \ge l' + (m - i)$. It has $j - m$ elements after it, all at most $h'$, so $S[m] \le h' - (j - m)$. Line L5 writes the offset $S[m] - l' - (m - i)$, which lies in $0 .. r$ with $r = h' - l' - (j - i)$. When $r = 0$, line L3 sees $h' - l' = j - i$: the sublist must be $l', l' + 1, \ldots, h'$, and nothing is written.

**The stack.** The recursive form codes the middle, then the left half, then the right half. Line L6 pushes the right half first and the left half last, so the left half is popped first and the order of the codewords is the pre-order of the recursion. The stack holds the right siblings along the current path plus at most one more tuple, so its size is at most $\lfloor \log n \rfloor + 2$; no deep recursion is needed.

**Minimal binary codes.** A value in $0 .. r$ fits in $k = \lceil \log(r + 1) \rceil$ bits. If $r + 1$ is not a power of two, $c = 2^k - (r + 1)$ of the values can take $k - 1$ bits instead, as in the truncated binary code of the [Golomb code](/golomb-coding/). Moffat and Stuiver give the short codewords to the values in the middle of the range, a *centered* minimal binary code, because the middle element tends to fall near the middle of its range. This implementation gives the short codewords to the values $s, \ldots, s + c - 1$ with $s = \lfloor r/2 \rfloor - \lfloor c/2 \rfloor + (r \bmod 2)$, the range given by Pibiri and Venturini: it rotates the range so that $s$ maps to 0, then uses the truncated binary code. A plain binary mode with $k$ bits per value is also given, for comparison with the survey.

## Example

Code $S = [3, 4, 7, 13, 14, 15, 21, 25, 36, 38, 54]$ with $l = 0$ and $h = 62$ (the example of Pibiri and Venturini, Fig. 4, where 62 is the last element of the full list and is sent first). The nodes in the order of the output:

| sublist | $l'$ | $h'$ | middle | offset | $r$ | plain | minimal |
|---|---|---|---|---|---|---|---|
| 3 4 7 13 14 **15** 21 25 36 38 54 | 0 | 62 | 15 | 10 | 52 | 6 | 6 |
| 3 4 **7** 13 14 | 0 | 14 | 7 | 5 | 10 | 4 | 3 |
| **3** 4 | 0 | 6 | 3 | 3 | 5 | 3 | 2 |
| **4** | 4 | 6 | 4 | 0 | 2 | 2 | 2 |
| **13** 14 | 8 | 14 | 13 | 5 | 5 | 3 | 3 |
| **14** | 14 | 14 | 14 | | 0 | 0 | 0 |
| 21 25 **36** 38 54 | 16 | 62 | 36 | 18 | 42 | 6 | 5 |
| **21** 25 | 16 | 35 | 21 | 5 | 18 | 5 | 4 |
| **25** | 22 | 35 | 25 | 3 | 13 | 4 | 4 |
| **38** 54 | 37 | 62 | 38 | 1 | 24 | 5 | 5 |
| **54** | 39 | 62 | 54 | 15 | 23 | 5 | 4 |

The offsets $10, 5, 3, 0, 5, 18, 5, 3, 1, 15$ and the plain lengths $6, 4, 3, 2, 3, 6, 5, 4, 5, 5$ are those of the survey. The element 14 has $l' = h' = 14$ and costs nothing. The plain code takes 43 bits and the centered minimal code takes 38 bits, against 66 bits for 11 values in 6 bits each.

To decode, the decoder knows $n = 11$, $l = 0$ and $h = 62$. For the root it computes $r = 62 - 0 - 10 = 52$, reads the offset 10, and sets $S[5] = 0 + 5 + 10 = 15$. Then it pops $S[0..4]$ with $l' = 0$, $h' = 14$, computes $r = 10$, reads 5 and sets $S[2] = 0 + 2 + 5 = 7$, and so on in the same order as the encoder.

## Correctness

The invariant of both loops is: every tuple $(i, j, l', h')$ on the stack has $l' \le S[i]$, $S[j] \le h'$, and the same tuples are on both stacks in the same order. It holds for the first tuple by the input condition. If it holds for the popped tuple, then $l' + (m - i) \le S[m] \le h' - (j - m)$, so the offset of line L5 is in $0 .. r$, and lines L10 and L5 use the same $r$ and the same code, so line L10 recovers $S[m]$. The two new tuples meet the invariant because the list is strictly increasing: $S[m - 1] \le S[m] - 1$ and $S[m + 1] \ge S[m] + 1$. When $h' - l' = j - i$, the $j - i + 1$ distinct integers in $[l', h']$ are all of them, so line L9 fills them in right. The full proof is in the proof file.

## Complexity

**Time.** Each element is the middle of exactly one node or is filled in by a run, so there are at most $n$ nodes that write, and each does $O(1)$ work besides its codeword. On a [word RAM](/word-ram/) a codeword of at most $w$ bits is read or written in $O(1)$ steps, so encoding and decoding take $\Theta(n)$ time. The decoder is serial: each node needs the bounds that its parent decoded.

**Space.** The stack holds at most $\lfloor \log n \rfloor + 2$ tuples.

**Size.** At depth $d$ of the recursion there are at most $2^d$ nodes, and their ranges $[l', h']$ are disjoint, so the sizes $r + 1$ of their offset ranges sum to at most $u$. A codeword for a range of size $r + 1$ takes at most $\log(r + 1) + 1$ bits, and $\log$ is concave, so the codewords at depth $d$ take at most $2^d \log(u / 2^d) + 2^d$ bits. Write $\log(u/2^d) = \log(u/n) + \log(n/2^d)$ and sum over the levels: the first part gives at most $n \log(u/n)$, and the second part is a sum $\sum_d 2^d \log(n/2^d) = O(n)$. So the total is $n \log(u/n) + O(n)$ bits. When $n$ is much smaller than $u$, the information-theoretic minimum for a set of $n$ elements in a range of $u$ is $\log \binom{u}{n} \approx n \log(u/n) + 1.44n$ bits, so BIC is within $O(n)$ bits of it on any list. On clustered lists it can use less than one bit per element.

## Properties

- **No gaps needed.** It works on the values themselves, and it uses the bounds from both sides, which a gap code cannot.
- **Sub-bit cost on runs.** A run of consecutive integers between two coded elements costs 0 bits, so a dense list can take far less than $n$ bits.
- **Serial.** The decoder cannot start a node before its parent; there is no random access inside a list, and no SIMD parallelism.
- **Needs $n$, $l$ and $h$.** The decoder must know the count and the bounds; an index stores them with the list.

## Variants and improvements

- **Code choice for the middle.** Plain binary, left-most minimal binary, and centered minimal binary give the same decoder structure with different sizes; Moffat and Stuiver used the centered form.
- **Tournament coding.** Teuhola's tournament code of integer sequences (Computer Journal, 2008) is closely related and uses a different tree over the elements.
- **Blocked lists.** Index systems can split a long list into blocks of, for example, 128 elements and code each block with BIC, with the bounds of each block stored in a small header, so that a query can skip blocks.

## When to use it

Use BIC where size matters most and decoding speed matters less: static inverted indexes stored on slow media, archives of posting lists, and lists of clustered integers such as the neighbors of a node in a web graph after a good ordering of the nodes. If queries decode many lists per second, [PForDelta](/pfor-delta/), [variable-byte encoding](/variable-byte-encoding/) or [Elias-Fano encoding](/elias-fano-encoding/) are several times faster. If the list must support random access or search by value, use Elias-Fano.

## Pitfalls

- **Range off by one.** Line L5 uses $r = h' - l' - (j - i)$, where $j - i$ is one less than the number of elements. Using the count $j - i + 1$ gives a range one too small, and the largest legal offset no longer fits. The survey's text gives the width as $\lceil \log(h - l - n + 1) \rceil$, but its Fig. 4 uses $\lceil \log(h - l - n + 2) \rceil$, which is $\lceil \log(r + 1) \rceil$; the figure is right.
- **Bounds of the halves.** A line L6 that pushes $(m + 1, j, S[m], h')$ and $(i, m - 1, l', S[m])$ makes each range one too wide. The code still decodes, but the run test of line L3 no longer fires, so runs do not cost 0 bits. The right line L6 uses $S[m] + 1$ and $S[m] - 1$.
- **Equal elements.** With repeats, line L5 can write a negative offset, because the bound $S[m] \ge l' + (m - i)$ needs distinct elements. A list that is only nondecreasing must first be mapped to $S[i] + i$, with $h$ raised by $n - 1$, and then lines L1 to L6 apply.
- **Push order.** If line L6 pushes the left half first but line L11 pushes the right half first, the decoder reads the codewords of one half with the ranges of the other and returns wrong values with no error. Lines L6 and L11 must push in the same order: right half, then left half.

## Implementations

## History

Alistair Moffat and Lang Stuiver presented interpolative coding at the Data Compression Conference in 1996, under the title "Exploiting clustering in inverted file compression", and published the full account, with centered minimal binary codes and experiments on text collections, in Information Retrieval in 2000. Witten, Moffat and Bell describe it in the second edition of Managing Gigabytes (1999). Later surveys of index compression, such as that of Pibiri and Venturini (2020), find it among the most compact list codes and among the slowest to decode.

## References
