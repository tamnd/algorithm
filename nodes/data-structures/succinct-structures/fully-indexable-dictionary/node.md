---
tag: ZEDY5H
kind: data-structure
slug: fully-indexable-dictionary
name: Fully indexable dictionary
aliases:
- FID
area: data-structures/succinct-structures
level: advanced
summary: A compressed set representation supporting rank, select and access, introduced by Raman, Raman and Rao.
model: word-ram
complexity:
  vars: {u: the size of the universe, n: the number of elements of the set}
  time: {member: O(1), rank: O(1), select: O(1), predecessor: O(1), successor: O(1)}
  space: {total: "n log(u / n) + O(n + u log log u / log u)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2002
  people: [Rajeev Raman, Venkatesh Raman, S. Srinivasa Rao]
  note: The fully indexable dictionary was defined and built in the SODA 2002 paper of Raman, Raman and Rao; the journal version appeared in 2007.
prereqs: [rank-select-dictionary, static-dictionary-problem, binomial-coefficient]
see_also: [rrr-bitvector, rank-select-problem, sd-array, elias-fano-encoding, predecessor-problem, compressed-data-structure, patrascu-succinct-lower-bound, succinct-data-structures]
sources:
  - paper: doi:10.1145/1290672.1290680
    title: Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct indexable dictionaries with applications to encoding k-ary trees, prefix sums and multisets, ACM Transactions on Algorithms 3(4), Article 43, 2007
    locator: Section 1 (the definitions of the indexable dictionary and the fully indexable dictionary, and the statements of the main results) and the section that builds the fully indexable dictionary from blocks of class and offset
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4, Sections 4.1.1 (Zero-Order Compression), 4.2.3 (Rank on Compressed Bitvectors) and 4.5.2 (Predecessors and Successors)
  - paper: doi:10.1109/FOCS.2008.83
    title: Mihai Pătraşcu, Succincter, 49th Annual Symposium on Foundations of Computer Science (FOCS 2008), 305-313
    locator: the main theorem for sets, lg C(u, n) + u / (lg u / t)^t + Õ(u^{3/4}) bits with O(t) query time
---

A fully indexable dictionary (FID) stores a set $S \subseteq \{0, 1, \ldots, u-1\}$ of $n$ elements and answers, in $O(1)$ time on the [word RAM](/word-ram/), membership, $\text{rank}(x) = |\{y \in S : y < x\}|$, $\text{select}(i)$, the $i$-th smallest element of $S$, and the same rank and select for the complement $\bar{S}$. Raman, Raman and Rao built it in $\lceil \lg \binom{u}{n} \rceil + O(u \lg \lg u / \lg u)$ bits, which is the [information-theoretic minimum](/information-theoretic-bound/) for $n$-element sets plus a term that is $o(u)$. In bit-vector terms it is the [rank and select problem](/rank-select-problem/) on the characteristic vector of $S$, in space that adapts to $n$. This page is about the set interface and the bounds; the block encoding that reaches them is on the page [RRR bit vector](/rrr-bitvector/).

## In plain words

A set of numbers from a fixed range can be stored as a row of bits, one bit for each number in the range, set to 1 when the number is in the set. With a rank and select index on that row, you can ask whether a number is in the set, how many members are smaller than it, which member is the tenth smallest, and which member comes just before or just after a number.

A fully indexable dictionary answers all these questions, also for the numbers that are not in the set, and it does it in less space than the row when the set is small or very large. It uses about as many bits as you need to say which set, among all sets of that size, you have. The rest of the structure is a small index on top.

## The abstract type

The FID is a static [ordered set](/ordered-set/) over the universe $U = \{0, \ldots, u-1\}$, built once from $S$, with these queries for $0 \le x < u$, $0 \le r \le u$, $1 \le i \le n$ and $1 \le k \le u - n$:

| query | result |
|---|---|
| `member(x)` | true when $x \in S$ |
| `rank(r)` | $\lvert\{y \in S : y < r\}\rvert$ |
| `select(i)` | the $i$-th smallest element of $S$ |
| `rank_out(r)` | $\lvert\{y \notin S : y < r\}\rvert = r - \text{rank}(r)$ |
| `select_out(k)` | the $k$-th smallest element of $U \setminus S$ |
| `pred(x)`, `succ(x)` | $\max\{y \in S : y \le x\}$ and $\min\{y \in S : y \ge x\}$, or none |

Raman, Raman and Rao also define the weaker **indexable dictionary** (ID): it has select, and it has rank only for $x \in S$ (for $x \notin S$ it reports that $x$ is not in the set). The ID can be stored in $\lceil \lg \binom{u}{n} \rceil + o(n) + O(\lg \lg u)$ bits, with a redundancy that depends on $n$ and not on $u$. The FID needs the full rank, so it can answer [predecessor](/predecessor-problem/) queries, and this costs redundancy in terms of $u$.

## Representation

Let $B[0 \ldots u-1]$ be the characteristic vector of $S$: $B[x] = 1$ if and only if $x \in S$. The FID is any structure that answers access, $\text{rank}_1$, $\text{rank}_0$, $\text{select}_1$ and $\text{select}_0$ on $B$. Each query of the abstract type is then one or two of these primitive queries, as in the pseudocode below.

The space bound comes from the encoding of $B$. Raman, Raman and Rao cut $B$ into blocks of $b = \lceil \frac12 \lg u \rceil$ bits. A block with $c$ ones is stored as its *class* $c$, in $\lceil \lg(b + 1) \rceil$ bits, and its *offset*, the index of the block among the $\binom{b}{c}$ blocks of class $c$, in $\lceil \lg \binom{b}{c} \rceil$ bits. Since $\prod_k \binom{b}{c_k} \le \binom{u}{n}$, the offsets take at most $\lg \binom{u}{n} + u/b$ bits. The classes, the pointers into the offsets and the rank and select directories take $O(u \lg \lg u / \lg u)$ bits more. The [RRR bit vector](/rrr-bitvector/) page gives the encoding and its proof.

## Operations

The primitives ACCESS, RANK1, SELECT1 and SELECT0 are those of the encoding of $B$. Each takes $O(1)$ time in the RRR encoding.

```pseudo id=main
MEMBER(x)                                    ▷ 0 ≤ x < u
L1  return ACCESS(x) = 1

RANK(r)                                      ▷ the number of elements less than r, 0 ≤ r ≤ u
L2  return RANK1(r)

SELECT(i)                                    ▷ the i-th smallest element, 1 ≤ i ≤ n
L3  return SELECT1(i)

PRED(x)                                      ▷ the largest element ≤ x, 0 ≤ x < u
L4  r ← RANK1(x + 1)
L5  if r = 0 then return none
L6  return SELECT1(r)

SUCC(x)                                      ▷ the smallest element ≥ x, 0 ≤ x < u
L7  r ← RANK1(x)
L8  if r = n then return none
L9  return SELECT1(r + 1)

RANK-OUT(r)                                  ▷ the number of non-elements less than r
L10 return r − RANK1(r)

SELECT-OUT(k)                                ▷ the k-th smallest non-element, 1 ≤ k ≤ u − n
L11 return SELECT0(k)
```

**Predecessor.** $\text{RANK1}(x+1)$ counts the elements $\le x$. If it is $r \ge 1$, the largest of them is the $r$-th smallest element. **Successor.** $\text{RANK1}(x)$ counts the elements $< x$. If $r < n$, the $(r+1)$-th smallest element is the smallest one $\ge x$. **Complement.** Each $y < r$ is in $S$ or in $\bar{S}$, so the non-elements less than $r$ number $r - \text{rank}(r)$; select on $\bar{S}$ is $\text{select}_0$ on $B$.

Each query is at most two primitive calls, so each takes $O(1)$ time when the primitives do.

## Example

Let $u = 16$ and $S = \{0, 2, 3, 6, 8, 9, 13, 14, 15\}$, so $n = 9$ and $B = 1011\,0010\,1100\,0111$. The complement is $\bar{S} = \{1, 4, 5, 7, 10, 11, 12\}$.

| query | the steps | result |
|---|---|---|
| MEMBER(7) | $B[7] = 0$ | false |
| RANK(10) | $\text{rank}_1(10)$ | 6 |
| SELECT(4) | $\text{select}_1(4)$ | 6 |
| PRED(12) | $r = \text{rank}_1(13) = 6$, then $\text{select}_1(6)$ | 9 |
| SUCC(10) | $r = \text{rank}_1(10) = 6 < 9$, then $\text{select}_1(7)$ | 13 |
| SUCC(15) | $r = \text{rank}_1(15) = 8 < 9$, then $\text{select}_1(9)$ | 15 |
| PRED(1) | $r = \text{rank}_1(2) = 1$, then $\text{select}_1(1)$ | 0 |
| RANK-OUT(10) | $10 - 6$ | 4 |
| SELECT-OUT(5) | $\text{select}_0(5)$ | 10 |

The class of 9-element subsets of a 16-element universe has $\binom{16}{9} = 11440$ members, so $\lceil \lg 11440 \rceil = 14$ bits are needed, against 16 for $B$. The gap grows with $u$: for $u = 2^{20}$ and $n = 2^{10}$, $\lg \binom{u}{n} \approx 11{,}710$ bits, against $2^{20}$ bits for $B$.

## Correctness

Each query of the pseudocode is a short identity of rank and select on the characteristic vector, proved in [the proof of correctness](proofs/correctness.md). The two identities for predecessor and successor are

$$\text{pred}(x) = \text{select}_1(\text{rank}_1(x + 1)), \qquad \text{succ}(x) = \text{select}_1(\text{rank}_1(x) + 1),$$

when the right side is defined. The space bound is the theorem of Raman, Raman and Rao, whose proof for the offsets is on the [RRR bit vector](/rrr-bitvector/) page.

## Complexity

| query | time, worst case, RRR encoding |
|---|---|
| member, rank, select | $O(1)$ |
| pred, succ | $O(1)$: two primitive calls |
| rank and select on $\bar{S}$ | $O(1)$ |
| build | $O(u)$ |

**Space, lower bound.** Any representation that tells all $n$-element subsets of $U$ apart needs $\lceil \lg \binom{u}{n} \rceil$ bits for some set, because there are $\binom{u}{n}$ of them and $b$ bits have only $2^b$ values. By the bounds $(u/n)^n \le \binom{u}{n} \le (eu/n)^n$, this is $n \lg(u/n) + O(n)$ bits.

**Space, upper bound.** The RRR encoding uses $\lg \binom{u}{n} + O(u \lg \lg u / \lg u)$ bits. Pătraşcu's structure uses $\lg \binom{u}{n} + u / (\lg u / t)^t + \tilde{O}(u^{3/4})$ bits for $O(t)$ query time. The redundancy is in terms of $u$, so when $n$ is much smaller than $u / \lg u$, the FID is not succinct for the class of $n$-element sets: for $n = o(u \lg \lg u / \lg^2 u)$ the term $u \lg \lg u / \lg u$ is larger than $n \lg(u/n)$. For such sets, the [SD-array](/sd-array/) and [Elias-Fano](/elias-fano-encoding/) use $n \lg(u/n) + O(n)$ bits, with $O(1)$ select and $O(\lg(u/n))$ rank.

**Lower bound on the redundancy.** In the [cell-probe model](/cell-probe-model/), Pătraşcu and Viola proved that a structure for rank with $t$ probes needs redundancy $u / w^{O(t)}$; see [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/).

## Variants

- **Indexable dictionary.** Rank only for elements, with $o(n)$ redundancy; enough for minimal perfect hashing of a static set to $\{0, \ldots, n-1\}$, since $\text{rank}(x)$ for $x \in S$ is such a hash.
- **Multisets.** Raman, Raman and Rao store a multiset of $n$ elements from $U$ in $\lceil \lg \binom{u + n}{n} \rceil + o(n)$ bits with rank and select, by the map of a multiset to a set of the same size in a larger universe.
- **Prefix sums.** A sequence of $n$ non-negative integers with sum $u$ maps to a set of $n$ elements in a universe of size $u + n$; select then gives the prefix sums in $O(1)$ time.
- **Compressed in practice.** The [RRR bit vector](/rrr-bitvector/) with fixed blocks of 15 or 63 bits, and the [SD-array](/sd-array/) for sparse sets.

## When to use it

Use an FID when a static set needs full rank, predecessor and successor, and its density $n/u$ is neither tiny nor close to $1/2$: for example the bit vectors of a compressed [wavelet tree](/wavelet-tree/), or a set of marked nodes in a succinct tree. If $n/u$ is about $1/2$, the plain [rank/select dictionary](/rank-select-dictionary/) is as small and faster. If $n \ll u$, use [Elias-Fano](/elias-fano-encoding/). If you need only membership and the rank of members, an indexable dictionary or a [perfect hash](/perfect-hashing/) table is smaller.

## Pitfalls

- **Rank of a non-member.** An indexable dictionary cannot answer $\text{rank}(x)$ for $x \notin S$. Code that uses an ID for predecessor search gets wrong answers silently.
- **Predecessor off by one.** PRED$(x)$ needs $\text{rank}_1(x + 1)$, the elements $\le x$, as in line L4. With $\text{rank}_1(x)$ it returns the largest element $< x$, which is wrong when $x \in S$.
- **The last element.** SUCC$(x)$ must test $r = n$ in line L8 before line L9 calls $\text{select}_1(n + 1)$, which is not defined.
- **Redundancy in $u$.** The $o(u)$ term is in the size of the universe, not of the set. For a few thousand elements of a universe of $2^{40}$, the FID is far larger than a sorted array.

## Implementations

## History

Raman, Raman and Rao defined the indexable and the fully indexable dictionary at SODA 2002, with the class and offset encoding of blocks and its use for $k$-ary trees and multisets; the journal version, with prefix sums added to the title, appeared in ACM Transactions on Algorithms in 2007. Pătraşcu's "Succincter" (2008) gave the optimal trade-off between redundancy and query time.

## References
