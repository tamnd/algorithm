---
tag: YJEG1W
kind: algorithm
slug: bloom-join
name: Bloom join
aliases:
- Bloom-filter join
- Bloomjoin
area: systems/database-algorithms
level: advanced
summary: "Send a Bloom filter of the join keys of S to the site of R, keep only the tuples of R that pass it, and join them with S. False positives cost data but never lose a match."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of R, N: the number of pages of S, p: the number of tuples per page of R, q: the number of tuples per page of S, m: the number of bits of the filter, k: the number of hash functions, T: the number of output tuples}
  time: {worst: Θ(k (p M + q N) + p q M N), average: O(k (p M + q N) + T), best: O(k (p M + q N) + T)}
  space: {extra: O(m + p M)}
  io:
    worst: "M + 2N"
    average: "M + 2N"
    best: "M + 2N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: false}
history:
  year: 1986
  people: [Lothar F. Mackert, Guy M. Lohman]
  note: "Bloom described the filter in 1970. Mackert and Lohman measured the Bloomjoin with other distributed join methods in the R* system in 1986."
prereqs: [semijoin, bloom-filter]
see_also: [hash-join, hybrid-hash-join, grace-hash-join, yannakakis-algorithm, reduce-side-join, map-side-join, hash-function]
sources:
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970, pages 422 to 426
    locator: the hash-coding method with allowable errors (the bit array, the k bit positions per element, and the false positive rate)
  - url: https://www.vldb.org/conf/1986/P149.PDF
    title: Lothar F. Mackert and Guy M. Lohman, R* optimizer validation and performance evaluation for distributed queries, VLDB 1986, pages 149 to 159
    locator: the part on distributed join methods (semijoins and Bloomjoins compared with shipping whole relations)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 22, Parallel and Distributed Databases, the part on distributed query processing (semijoins and Bloomjoins)
  - paper: doi:10.1145/322234.322238
    title: Philip A. Bernstein and Dah-Ming W. Chiu, Using semi-joins to solve relational queries, Journal of the ACM 28(1), 1981, pages 25 to 40
    locator: the definition of the semijoin and semijoin programs, which the Bloom join approximates
---

The Bloom join computes the equi-join of a relation $R$ at one site with a relation $S$ at another site, and tries to send less data over the network. The site of $S$ puts the join key of each tuple of $S$ into a [Bloom filter](/bloom-filter/) of $m$ bits and sends the bits to the site of $R$. There, each tuple of $R$ whose key fails the filter is dropped, because it cannot have a match. The tuples that pass, $R'$, go to the site of $S$, which joins them with $S$. A Bloom filter has no false negatives, so $R'$ contains the whole [semijoin](/semijoin/) $R \ltimes S$, and no match is lost. It can have false positives, so $R'$ can contain extra tuples, and the final join removes them. The method replaces the exact list of join values of a semijoin with a filter that is often much smaller.

## In plain words

A shop in one city must find which of its 10,000 customers also appear on a list of 500 names kept in another city. Mailing the list is costly, so the other city sends a small card full of holes instead. The card was made by punching, for each name on the list, two holes at places picked from the name.

The shop checks each customer: are both of that customer's holes punched? If one is missing, the customer is surely not on the list. If both are there, the customer is probably on the list, so the shop mails that customer back. The other city then checks each returned customer against the real list. A few customers come back for nothing, but no customer on the list is missed.

## The problem

The input is two relations $R$ and $S$, stored at two sites, and the condition $r.a = s.b$. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/), at the site of $S$. There are two costs. The page I/O at both sites is counted as on the other join pages: $R$ has $M$ pages with $p_R$ tuples per page and $S$ has $N$ pages with $p_S$ tuples per page, and the writes of the output are not counted. The network cost is the number of bits and tuples sent between the sites. In a distributed system with a slow network, the network cost is usually the larger one. The front matter writes $p$ for $p_R$ and $q$ for $p_S$.

## The algorithm

The filter is an array $F$ of $m$ bits with $k$ hash functions $g_1, \dots, g_k$ from keys to $\{0, \dots, m - 1\}$. The implementation computes them by double hashing: $g_i(x) = (h(x) + i \cdot h'(x)) \bmod m$, with two 64-bit halves $h$ and $h'$ of a BLAKE2b digest of the key.

```pseudo id=main
BLOOM-JOIN(R, S, a, b, m, k)               ▷ R at site 1, S at site 2, the join r.a = s.b
L1  F ← an array of m bits, all 0          ▷ at site 2
L2  for each tuple s of S do set F[g_1(s.b)], ..., F[g_k(s.b)] to 1
L3  send F to site 1                        ▷ m bits
L4  R′ ← an empty list                       ▷ at site 1
L5  for each tuple r of R do
L6      if F[g_i(r.a)] = 1 for every i from 1 to k then append r to R′
L7  send R′ to site 2                        ▷ |R′| tuples
L8  join R′ with S at site 2 by a hash join with a table on R′
L9  return the result of line L8
```

Line L6 is the filter test. If a key $x$ is in $S$, line L2 set all $k$ bits of $x$, so every tuple of $R$ with key $x$ passes. If $x$ is not in $S$, its $k$ bits may still all be set by other keys, and then the tuples with key $x$ pass as *false positives*. Line L8 is an in-memory [hash join](/hash-join/) with $R'$ as the build input. It compares the keys themselves, so a false positive finds no partner there and gives no output. A larger $R'$ can use any join method of the site, such as the [Grace hash join](/grace-hash-join/).

## Example

Let $R$ have the keys $1, 2, \dots, 12$, three tuples per page ($M = 4$), and let $S$ have the keys $[3, 7, 7, 11]$, two tuples per page ($N = 2$). The filter has $m = 16$ bits and $k = 2$ hash functions. The bit positions of the implementation are:

| key | $g_1, g_2$ | in $S$ | passes line L6 |
|---|---|---|---|
| 3 | 3, 10 | yes | yes |
| 7 | 14, 7 | yes | yes |
| 11 | 6, 11 | yes | yes |
| 1 | 14, 7 | no | yes, the same bits as key 7 |
| 8 | 6, 7 | no | yes, bit 6 from key 11 and bit 7 from key 7 |
| 2, 4, 5, 6, 9, 10, 12 | for example 2: 1, 8 | no | no, at least one bit is 0 |

After line L2, the bits $\{3, 6, 7, 10, 11, 14\}$ are set. Line L6 keeps the keys $1, 3, 7, 8, 11$, so $R'$ has 5 tuples: the 3 tuples of the semijoin $R \ltimes S$ and 2 false positives. Line L8 finds 4 output tuples: key 3 once, key 7 twice and key 11 once. Keys 1 and 8 find no partner. The I/O cost is $N + M + N = 2 + 4 + 2 = 8$ page reads, and the network carries 16 bits and 5 tuples, instead of the 12 tuples of $R$.

**A measured reduction.** The tests use $|R| = 10{,}000$ tuples with distinct keys and $S$ with 500 distinct keys from the same range, chosen with the seed 2026. Exactly 500 tuples of $R$ have a match.

| $m$ | $k$ | tuples in $R'$ | false positives | rate | formula |
|---|---|---|---|---|---|
| 4096 | 3 | 786 | 286 | 286/9500 = 0.0301 | 0.0288 |
| 32768 | 6 | 500 | 0 | 0 | 0.00000045 |

The formula is the usual estimate $(1 - e^{-k n/m})^k$ for $n = 500$ keys in the filter. The counts are exact for this seed, and the tests check them.

**Is it cheaper than a semijoin?** Take keys of 4 bytes and tuples of 100 bytes, in the measured case. Sending $R$ costs $10{,}000 \cdot 800 = 8{,}000{,}000$ bits. An exact semijoin sends the 500 keys and 500 tuples: $16{,}000 + 400{,}000 = 416{,}000$ bits. The Bloom join with $m = 4096$ sends $4096 + 786 \cdot 800 = 632{,}896$ bits, and with $m = 32{,}768$ it sends $32{,}768 + 400{,}000 = 432{,}768$ bits. So the filter must be tuned. It wins against the semijoin when the keys are long, such as strings, or when $S$ has many distinct keys, because the filter size does not depend on the key length.

## Correctness

The proof uses one lemma about joins: if $R \ltimes S \subseteq X \subseteq R$, then $X \bowtie S = R \bowtie S$. A tuple of $R$ outside $X$ has no partner in $S$, so removing it removes no output, and a tuple of $X$ keeps all its partners. Here $X = R'$. It is a part of $R$ by line L6, and it contains $R \ltimes S$ because a key in $S$ has all its bits set by line L2. So line L8 returns $R \bowtie S$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **I/O.** Line L2 reads $S$ ($N$ pages), line L5 reads $R$ ($M$ pages) and line L8 reads $S$ again ($N$ pages), if $R'$ fits in memory at site 2. The total is $M + 2N$ page reads, for any data. Site 2 can save the second scan if $S$ fits in memory.
- **Network.** $m$ bits for the filter and $|R'|$ tuples for the reduced relation. With $n$ distinct keys in $S$, the expected number of tuples in $R'$ is about $|R \ltimes S| + \varepsilon \cdot |R \setminus (R \ltimes S)|$, with $\varepsilon \approx (1 - e^{-k n/m})^k$. The estimate holds for a key chosen independently of the hash functions; a key that is a false positive lets all of its duplicates through.
- **Choosing $m$ and $k$.** For fixed $m/n$, the rate $\varepsilon$ is least for $k \approx (m/n) \ln 2$, and then $\varepsilon \approx 0.6185^{m/n}$. About 10 bits per key give about one percent false positives.
- **Work in memory.** Each test and each insertion computes $k$ positions. With a hash table on $R'$, the expected work is $O(k (p_R M + p_S N) + T)$.

## Properties

- **No match is lost.** The filter has no false negatives, so the result is exact for any $m \ge 1$ and $k \ge 1$. A bad choice costs network traffic, never correctness.
- **Equality only.** The filter answers membership of a key, so the join condition must be an equality.
- **Fixed filter size.** The filter takes $m$ bits whatever the length of the key, while an exact semijoin sends every distinct key.
- **Deterministic.** For fixed hash functions, $R'$ and the costs are fixed. The false positive rate is a statement about keys that do not depend on the hash functions.

## Variants and improvements

- **Exact semijoin.** Send $\pi_b(S)$ instead of a filter. Then $R' = R \ltimes S$ exactly, at the cost of sending each distinct key. See the page [semijoin](/semijoin/).
- **Bit-vector filters in local hash joins.** A [hybrid](/hybrid-hash-join/) or [Grace](/grace-hash-join/) hash join can build a bit vector on the build input while it partitions it, and use it to drop tuples of the probe input before they are written to disk. This saves disk I/O instead of network traffic.
- **Runtime filters.** Many analytic engines build a Bloom filter on the build side of a hash join and push it down to the scan of the probe side, often across machines.
- **Filters on clusters.** Before a [reduce-side join](/reduce-side-join/), a filter on the smaller input can drop most tuples of the larger input in the map step, so less data is shuffled. If the smaller input fits in memory, a [map-side join](/map-side-join/) needs no filter at all.
- **Both directions.** Filter $R$ by $S$ and then $S$ by the reduced $R$, as in a semijoin program. On an acyclic query, this is an approximate form of the reduction step of the [Yannakakis algorithm](/yannakakis-algorithm/).

## When to use it

Use it for an equi-join across sites when the network is the bottleneck, the join is selective, and one relation is much smaller in distinct keys than the other is in tuples. It is most useful when the keys are long, because the filter size does not grow with the key length. If most tuples of $R$ match, the filter removes little and only adds the cost of the bits and the extra scan of $S$. Then it is better to send the smaller relation whole.

## Pitfalls

- **Treating the filter as exact.** Line L8 must join with $S$ and compare the keys. A tuple that passes line L6 may have no match.
- **Different hash functions at the two sites.** Lines L2 and L6 must use the same functions $g_1, \dots, g_k$ and the same $m$. A mismatch gives false negatives, and matches are lost.
- **A filter that is too small.** With $m$ much smaller than $n$, almost every bit is set, and the filter passes almost everything. In the measured case, 4096 bits for 500 keys pass 286 extra tuples, while 32,768 bits pass none.
- **Heavy duplicates in $R$.** One key that is a false positive lets every tuple with that key through. The estimate per key is not an estimate per tuple when keys repeat.

## Implementations

## History

Bloom (1970) introduced the filter as a way to test membership with a small table at the cost of a few errors, and showed how the error rate depends on the size of the table and the number of bits per element. Bernstein and Chiu (1981) studied exact semijoins as a way to reduce relations before a join, and the SDD-1 system used them across sites. Mackert and Lohman (1986) measured distributed join methods in the R* system, including semijoins and Bloomjoins. Ramakrishnan and Gehrke, Chapter 22, present the Bloomjoin as the bit-vector form of the semijoin for distributed queries.

## References
