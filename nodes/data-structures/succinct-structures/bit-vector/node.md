---
tag: 6G48XR
kind: data-structure
slug: bit-vector
name: Bit vector
aliases:
- bit array
- bitvector
area: data-structures/succinct-structures
level: intro
summary: A static sequence of bits that supports access, rank and select queries.
model: word-ram
complexity:
  vars: {n: the number of bits, w: the number of bits in a machine word}
  time: {build: Θ(n), access: Θ(1), rank: O(n/w), select: O(n/w)}
  space: {total: n + O(w)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bitwise-operations, population-count, word-ram]
see_also: [rank-select-problem, rank-select-dictionary, jacobson-rank, rrr-bitvector, sd-array, dynamic-bit-vector, succinct-data-structures, bit-set]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 3, Section 3.1 (Elements of Fixed Size), and Chapter 4 (Bitvectors), Sections 4.1 (Access) and 4.2.1 (Sparse Sampling)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3 (Bitwise tricks and techniques), sideways addition and the extraction of the lowest 1 bit
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the bit vector with rank and select as the base of succinct trees
  - paper: doi:10.1007/978-3-540-68552-4_12
    title: Sebastiano Vigna, Broadword implementation of rank/select queries, 7th Workshop on Experimental Algorithms (WEA 2008), Lecture Notes in Computer Science 5038, 154-168
    locator: the rank9 layout and broadword select in a word
---

A bit vector is a sequence $B[0 \ldots n-1]$ of bits, packed $w$ to a machine word, that answers three queries: $\text{access}(i) = B[i]$, $\text{rank}_b(i)$, the number of bits equal to $b$ in $B[0 \ldots i-1]$, and $\text{select}_b(j)$, the position of the $j$-th bit equal to $b$. In plain packed form it uses $n$ bits plus less than one word, answers access in $O(1)$ time on the [word RAM](/word-ram/), and answers rank and select by a scan with [population count](/population-count/) in $O(n/w)$ time. It is the input of the [rank and select problem](/rank-select-problem/), and the base layer of each [succinct data structure](/succinct-data-structures/). The indexes on the page [rank/select dictionary](/rank-select-dictionary/) make rank and select take $O(1)$ time with $o(n)$ more bits.

## In plain words

A computer word holds 64 bits. A list of yes or no answers needs only one bit for each answer, so 64 answers fit in one word. To read answer number 100, you go to word 1 and look at bit 36 of it. This is one step.

To count the yes answers before a place, you count the bits that are on in each full word before it, and then in a part of the next word. Computers have an instruction that counts the bits that are on in a word in one step, so this goes 64 answers at a time. To find where the tenth yes answer is, you go word by word and subtract the counts until the word that holds it, and then look inside that word. Both of these take time that grows with the length of the list, but with a small factor.

## The abstract type

A bit vector is the static case of a sequence over the alphabet $\{0, 1\}$, so it is the binary case of the [static indexable sequence](/static-sequence/). It is built once from a list of bits and does not change. The operations are:

| operation | result |
|---|---|
| `build(b)` | the bit vector with $B[i] = b[i]$ for $0 \le i < n$ |
| `length()` | $n$ |
| `access(i)` | $B[i]$, for $0 \le i < n$ |
| `rank1(i)`, `rank0(i)` | $\text{rank}_1(i) = \lvert\{p < i : B[p] = 1\}\rvert$, and $\text{rank}_0(i) = i - \text{rank}_1(i)$, for $0 \le i \le n$ |
| `select1(j)`, `select0(j)` | the position $p$ with $B[p] = b$ and $\text{rank}_b(p) = j - 1$, for $1 \le j \le \text{rank}_b(n)$ |

The exact definitions and identities of rank and select are on the page of the [rank and select problem](/rank-select-problem/).

## Representation

The bits are stored in an array $W[0 \ldots \lceil n/w \rceil - 1]$ of $w$-bit words, with $n$ kept in one more word. Bit $i$ of the sequence is bit $i \bmod w$ of word $W[\lfloor i/w \rfloor]$, where bit 0 is the least significant bit. The invariant is:

- **(P1)** for $0 \le i < n$: $B[i] = \lfloor W[\lfloor i/w \rfloor] / 2^{i \bmod w} \rfloor \bmod 2$;
- **(P2)** each bit of the last word at a position of $n$ or more is 0.

Rule (P2) keeps the padding out of the counts of 1s. The space is $w \lceil n/w \rceil + w < n + 2w$ bits.

## Operations

POPCOUNT$(x)$ is the number of 1 bits of the word $x$. It is one instruction on current processors, and a short sequence of shifts, masks and additions otherwise (see [population count](/population-count/)). The operation $x \wedge (x - 1)$ clears the lowest 1 bit of $x$, and LOWEST$(x)$ is the index of the lowest 1 bit of $x \ne 0$.

```pseudo id=main
BUILD(b[0 .. n − 1])
L1  W ← an array of ⌈n / w⌉ words, all 0
L2  for i ← 0 to n − 1 do
L3      if b[i] = 1 then W[⌊i / w⌋] ← W[⌊i / w⌋] or 2^(i mod w)

ACCESS(i)                                  ▷ 0 ≤ i < n
L4  return (W[⌊i / w⌋] >> (i mod w)) and 1

RANK1(i)                                   ▷ the number of 1s in B[0 .. i − 1], 0 ≤ i ≤ n
L5  q ← ⌊i / w⌋, r ← i mod w, c ← 0
L6  for k ← 0 to q − 1 do c ← c + POPCOUNT(W[k])
L7  if r > 0 then c ← c + POPCOUNT(W[q] and (2^r − 1))
L8  return c

SELECT1(j)                                 ▷ the position of the j-th 1, 1 ≤ j ≤ m
L9  k ← 0
L10 while POPCOUNT(W[k]) < j do j ← j − POPCOUNT(W[k]), k ← k + 1
L11 x ← W[k]
L12 repeat j − 1 times: x ← x and (x − 1)  ▷ clear the lowest 1 bit
L13 return k · w + LOWEST(x)
```

**Build.** Lines L1 to L3 set bit $i \bmod w$ of word $\lfloor i/w \rfloor$ for each 1 of the input. The bits past $n$ are never set, so (P2) holds. The time is $\Theta(n)$, or $\Theta(n/w)$ if the input comes as words.

**Access.** Line L4 shifts the word right so that bit $i \bmod w$ comes to position 0, and masks it. This is (P1) read as a program. The time is $O(1)$.

**Rank.** Line L6 counts the 1s of the $q$ full words before position $i$. Line L7 counts the 1s of the low $r$ bits of the next word, which are the positions $qw$ to $i - 1$. The guard $r > 0$ avoids a read past the array when $i = n$ is a multiple of $w$. The time is $O(q + 1) = O(n/w + 1)$. Then $\text{rank}_0(i) = i - \text{rank}_1(i)$.

**Select.** The loop of line L10 skips whole words and subtracts their counts from $j$, until the word $W[k]$ that holds the wanted 1. That 1 is the $j$-th 1 of $W[k]$, with the new $j$. Line L12 clears the $j - 1$ lowest 1 bits, so the wanted 1 is now the lowest, and line L13 returns its position. The time is $O(n/w + w)$; with a broadword select in a word, or a table of the answers for each byte, the work inside the word is $O(1)$ or $O(\lg w)$.

**Select of a 0.** $\text{select}_0$ runs the same code on the complement $\neg W[k]$ of each word. In the last word, the complement must be masked to its first $n - w(\lceil n/w \rceil - 1)$ bits, or the padding counts as 0s.

## Example

Take $w = 8$ to keep the words small, and $B = 1011\,0010\,1100\,0111$, so $n = 16$ and $m = 9$. Bit 0 of a word is the least significant bit, so the first eight bits $1, 0, 1, 1, 0, 0, 1, 0$ give $W[0] = 2^0 + 2^2 + 2^3 + 2^6 = 77$, which is $01001101$ in binary when written with the most significant bit first. The next eight bits give $W[1] = 2^0 + 2^1 + 2^5 + 2^6 + 2^7 = 227 = 11100011_2$.

| query | the steps | result |
|---|---|---|
| ACCESS(9) | $W[1] \gg 1 = 113$, and $113 \wedge 1 = 1$ | 1 |
| RANK1(13) | $q = 1$, $r = 5$; POPCOUNT$(77) = 4$; $227 \wedge 31 = 3$ and POPCOUNT$(3) = 2$ | 6 |
| RANK0(13) | $13 - 6$ | 7 |
| SELECT1(7) | POPCOUNT$(77) = 4 < 7$, so $j = 3$ and $k = 1$; POPCOUNT$(227) = 8 \ge 3$; $x = 227 \to 226 \to 224$; LOWEST$(224) = 5$ | $8 + 5 = 13$ |
| SELECT0(4) | $\neg 77 = 178$ in 8 bits, POPCOUNT $= 4 \ge 4$; $x = 178 \to 176 \to 160 \to 128$; LOWEST$(128) = 7$ | 7 |

## Correctness

The invariant (P1) and (P2) holds after BUILD and never changes, since the structure is static. ACCESS is (P1). RANK1 is correct because the positions $0$ to $i - 1$ split into the $q$ full words and the low $r$ bits of $W[q]$, and by (P1) the count of 1s in each part is the population count of the matching bits. SELECT1 is correct by the invariant of line L10: the 1s in the words before $W[k]$ number $j_0 - j$, where $j_0$ is the first value of $j$, so the wanted 1 is the $j$-th 1 of $W[k]$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case | note |
|---|---|---|
| build | $\Theta(n)$ | $\Theta(n/w)$ from packed input |
| access | $\Theta(1)$ | one shift and one mask |
| rank | $O(n/w + 1)$ | one POPCOUNT for each word |
| select | $O(n/w + w)$ | $O(n/w + 1)$ with a constant-time select in a word |
| space | $n + O(w)$ bits | at most $w - 1$ bits of padding and one word for $n$ |

The model is the word RAM with $w \ge \lg n$, and POPCOUNT counts as one operation. Without it, POPCOUNT of a word takes $O(\lg w)$ operations by the parallel sum of bit fields, so rank costs $O(n \lg w / w)$.

## Variants

- **Sampled counts.** Store $\text{rank}_1$ at the start of each block of $s$ words, in $n \lg n / (sw)$ extra bits. Then rank scans at most $s$ words. With two levels and $s$ fixed this is the practical *rank9* layout of Vigna, and with a table for small blocks it is [Jacobson's rank structure](/jacobson-rank/) with $O(1)$ time.
- **Constant-time select.** Store the position of each $k$-th 1 and finish by a scan or by more samples. This is the [rank/select dictionary](/rank-select-dictionary/).
- **Compressed bit vectors.** When the bits are skewed, the [RRR bit vector](/rrr-bitvector/) uses about $\lg \binom{n}{m}$ bits, and the [SD-array](/sd-array/) uses about $m \lg(n/m) + 2m$ bits.
- **Mutable bits.** Writing $B[i]$ is one OR or AND NOT on a word, but any rank index then needs an update. Insertions and deletions need the [dynamic bit vector](/dynamic-bit-vector/).

## When to use it

Use a plain bit vector for a set of small integers or a list of flags when access and set operations on whole words are what you need, for example a [bit set](/bit-set/) for the [sieve of Eratosthenes](/sieve-of-eratosthenes/). Add a rank and select index when the code asks for counts or positions many times. If the vector holds few 1s, a compressed form is smaller than $n$ bits. If the vector changes, use a dynamic structure, since each update of a plain vector with an index costs time.

## Pitfalls

- **Bit order in a word.** Line L4 takes bit 0 as the least significant bit. If BUILD uses the most significant bit first and ACCESS the least, every query is wrong. Pick one order and use it in all lines.
- **Padding bits.** If BUILD leaves garbage in the last word past position $n - 1$, line L7 is still right, but select of a 0 and a rank that counts whole words are wrong. Keep (P2), and mask the complement in the last word for $\text{select}_0$.
- **Reading past the end.** RANK1$(n)$ with $n$ a multiple of $w$ has $q = \lceil n/w \rceil$. Line L7 must not read $W[q]$ when $r = 0$.
- **Off by one in rank.** $\text{rank}_1(i)$ here counts $B[0 \ldots i-1]$ and does not include $B[i]$. Code that mixes this with the inclusive form of many papers gets $\text{rank}(\text{select}(j)) = j$ or $j - 1$ by mistake.
- **Shift counts.** In C, a shift of a 64-bit word by 64 is undefined, so $2^r - 1$ for $r = 64$ must be written with care. Line L7 uses $r < w$ only.

## Implementations

## History

Packing flags into the bits of a word is as old as binary computers. Knuth treats the word-level operations used here, sideways addition (population count) and the isolation of the lowest 1 bit, in Section 7.1.3 of the fourth volume. The idea of a bit vector that answers rank and select as the base of space-efficient trees and graphs comes from Jacobson's 1989 paper and thesis.

## References
