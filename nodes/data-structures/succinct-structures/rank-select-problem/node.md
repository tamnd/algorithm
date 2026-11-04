---
tag: 9RNDV7
kind: problem
slug: rank-select-problem
name: Rank and select problem
aliases:
- rank and select queries
area: data-structures/succinct-structures
level: core
summary: Given a bit vector, return the number of 1s up to a position (rank) or the position of the i-th 1 (select).
prereqs: [bit-vector, prefix-sums, asymptotic-notation]
see_also: [jacobson-rank, rank-select-dictionary, fully-indexable-dictionary, rrr-bitvector, sd-array, dynamic-bit-vector, static-sequence, patrascu-succinct-lower-bound]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4 (Bitvectors), Sections 4.2 (Rank), 4.3 (Select) and 4.5.2 (Predecessors and Successors)
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the rank directory and the use of rank and select for tree navigation
  - paper: doi:10.1145/1290672.1290680
    title: Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct indexable dictionaries with applications to encoding k-ary trees, prefix sums and multisets, ACM Transactions on Algorithms 3(4), Article 43, 2007
    locator: Section 1 (the definitions of rank and select and the space bounds) and the fully indexable dictionary
  - paper: doi:10.1016/j.tcs.2007.07.041
    title: Alexander Golynski, Optimal lower bounds for rank and select indexes, Theoretical Computer Science 387(3), 2007, 348-359
    locator: the main theorem, the lower bound on the size of an index when the bit vector is stored in plain form
  - paper: doi:10.1109/FOCS.2008.83
    title: Mihai Pătraşcu, Succincter, 49th Annual Symposium on Foundations of Computer Science (FOCS 2008), 305-313
    locator: the main theorem on rank and select with redundancy n/(lg n / t)^t
---

The rank and select problem asks to preprocess a [bit vector](/bit-vector/) $B$ of length $n$ so that two queries are fast: $\text{rank}_1(B, i)$, the number of 1s before position $i$, and $\text{select}_1(B, j)$, the position of the $j$-th 1. The same queries for 0s are $\text{rank}_0$ and $\text{select}_0$. On the [word RAM](/word-ram/) both queries can be answered in $O(1)$ time with $n + o(n)$ bits, which is the base of most [succinct data structures](/succinct-data-structures/). Rank is a [prefix sum](/prefix-sums/) of bits, and select is its inverse.

## In plain words

You have a long row of lights, each on or off. Rank answers: how many lights are on to the left of this place? Select answers the other way around: where is the fifth light that is on?

With a list of running counts, rank is one lookup, and with a list of the places of the lights that are on, select is one lookup. Both lists take much more memory than the row of lights. The real problem is to answer both questions fast while you add only a little memory to the row itself, much less than the row. Trees, text indexes and sets of numbers can all be stored as rows of lights, and then each of their questions becomes a few rank and select questions.

## Definition

The input is a bit vector $B = B[0] B[1] \cdots B[n-1]$ with $B[i] \in \{0, 1\}$. Let $m$ be the number of 1s. For $b \in \{0, 1\}$, $0 \le i \le n$ and $1 \le j \le \text{rank}_b(B, n)$:

$$\text{rank}_b(B, i) = \left|\{\, p : 0 \le p < i,\ B[p] = b \,\}\right|,$$

$$\text{select}_b(B, j) = \text{the unique } p \text{ with } B[p] = b \text{ and } \text{rank}_b(B, p) = j - 1.$$

So $\text{rank}_b(B, i)$ counts the $b$s in the prefix $B[0 \ldots i-1]$, and $\text{select}_b(B, j)$ is the 0-based position of the $j$-th $b$. The value $p$ in the second line exists and is unique, because $\text{rank}_b(B, p)$ grows by exactly one at each position $p$ with $B[p] = b$. The query $\text{access}(B, i) = B[i]$ is part of the problem when $B$ is not stored in plain form.

The task is a static data structure: build it once from $B$, then answer any number of queries. The costs are the space in bits, the query time and the build time. The model is the word RAM with words of $w \ge \lg n$ bits, or the [cell-probe model](/cell-probe-model/) for lower bounds.

These identities follow from the definition and hold for each $B$:

- $\text{rank}_0(B, i) + \text{rank}_1(B, i) = i$.
- $\text{rank}_b(B, \text{select}_b(B, j)) = j - 1$ and $B[\text{select}_b(B, j)] = b$.
- $\text{select}_b(B, j) = \min\{\, p : \text{rank}_b(B, p + 1) = j \,\}$, so select can be found by a [binary search](/binary-search/) over rank.
- For $S = \{p : B[p] = 1\}$, the value $\text{rank}_1(B, x)$ is the number of elements of $S$ less than $x$, and $\text{select}_1(B, j)$ is the $j$-th smallest element of $S$.

## Variants

- **Rank only, or select only.** Some uses need one query. Rank alone needs less extra space in practice.
- **Inclusive rank, 1-based positions.** Many papers, among them Navarro's book, write $\text{rank}_1(B, i)$ for the number of 1s in $B[1 \ldots i]$. The value is the same as $\text{rank}_1(B, i)$ here with 0-based positions and an exclusive end. Only the indexing changes.
- **Plain or systematic.** The bit vector stays in plain form and an *index* of extra bits is added. The size of the index is the *redundancy*. A *non-systematic* structure may store $B$ in any encoding.
- **Compressed.** When $m$ is far from $n/2$, the space target is $\lg \binom{n}{m}$ bits, not $n$. This is the [fully indexable dictionary](/fully-indexable-dictionary/) of Raman, Raman and Rao, built for example by the [RRR bit vector](/rrr-bitvector/).
- **Sparse.** When $m \ll n$, a structure on the positions of the 1s, such as the [SD-array](/sd-array/), uses about $m(2 + \lg(n/m))$ bits.
- **Dynamic.** The bit vector also supports insertion and deletion of bits, or bit flips. This is the [dynamic bit vector](/dynamic-bit-vector/).
- **Larger alphabets.** For a sequence over an alphabet of $\sigma$ symbols, $\text{rank}_c$ and $\text{select}_c$ for each symbol $c$ define the [static indexable sequence](/static-sequence/). The [wavelet tree](/wavelet-tree/) reduces it to bit vectors.

## Examples

Let $B = 1011\,0010\,1100\,0111$, so $n = 16$ and $m = 9$. The spaces only help reading.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $B[i]$ | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | |
| $\text{rank}_1(B, i)$ | 0 | 1 | 1 | 2 | 3 | 3 | 3 | 4 | 4 | 5 | 6 | 6 | 6 | 6 | 7 | 8 | 9 |

- $\text{rank}_1(B, 10) = 6$ and $\text{rank}_0(B, 10) = 10 - 6 = 4$.
- The 1s are at positions $0, 2, 3, 6, 8, 9, 13, 14, 15$. So $\text{select}_1(B, 1) = 0$, $\text{select}_1(B, 5) = 8$ and $\text{select}_1(B, 9) = 15$.
- The 0s are at positions $1, 4, 5, 7, 10, 11, 12$. So $\text{select}_0(B, 4) = 7$.
- Check of an identity: $\text{rank}_1(B, \text{select}_1(B, 7)) = \text{rank}_1(B, 13) = 6 = 7 - 1$.
- The query $\text{select}_1(B, 10)$ is not defined, because $m = 9$.

## Known algorithms

| structure | space in bits | rank | select |
|---|---|---|---|
| no index, scan the [bit vector](/bit-vector/) word by word | $n$ | $O(n / w)$ | $O(n / w)$ |
| a full table of rank values and of 1 positions | $O(n \lg n)$ | $O(1)$ | $O(1)$ |
| [Jacobson's rank structure](/jacobson-rank/) | $n + O(n \lg \lg n / \lg n)$ | $O(1)$ | $O(\lg n)$ by binary search |
| [rank/select dictionary](/rank-select-dictionary/) (Jacobson rank and Clark select) | $n + o(n)$ | $O(1)$ | $O(1)$ |
| [RRR bit vector](/rrr-bitvector/), a [fully indexable dictionary](/fully-indexable-dictionary/) | $\lg \binom{n}{m} + O(n \lg \lg n / \lg n)$ | $O(1)$ | $O(1)$ |
| [Elias-Fano](/elias-fano-encoding/) and the [SD-array](/sd-array/) | $m \lceil \lg(n/m) \rceil + 2m + o(m)$ | $O(\lg(n/m))$ | $O(1)$ for $\text{select}_1$ |
| [dynamic bit vector](/dynamic-bit-vector/) | $n + o(n)$ | $O(\lg n)$ | $O(\lg n)$ |

The times are worst case on the word RAM with $w = \Theta(\lg n)$. The $O(1)$ times rely on [population count](/population-count/) of a word, or on a table of $o(n)$ bits that holds the answers for all short blocks.

## Bounds

**Space.** There are $2^n$ bit vectors of length $n$, so a structure that can recover each of them needs at least $n$ bits in the worst case. If $m$ is known, there are $\binom{n}{m}$ vectors, so at least $\lceil \lg \binom{n}{m} \rceil$ bits are needed. This is the counting argument of the [information-theoretic bound](/information-theoretic-bound/). Both queries together determine $B$, since $B[i] = \text{rank}_1(B, i + 1) - \text{rank}_1(B, i)$.

**Upper bounds.** With $w = \Theta(\lg n)$, rank and select take $O(1)$ time with $n + O(n \lg \lg n / \lg n)$ bits: Jacobson (1989) gave rank, and Clark (1996) and Munro (1996) gave select. Raman, Raman and Rao reached $\lg \binom{n}{m} + O(n \lg \lg n / \lg n)$ bits with $O(1)$ time. Pătraşcu (2008) lowered the redundancy to $n / (\lg n / t)^t + \tilde{O}(n^{3/4})$ bits for $O(t)$ query time, on top of $n$ or of $\lg \binom{n}{m}$ bits.

**Lower bounds.** If $B$ is stored in plain form and a query reads $O(\lg n)$ bits of $B$, Golynski (2007) proved that the index needs $\Omega(n \lg \lg n / \lg n)$ bits, both for rank and for select. So the classic structures are optimal among systematic ones. Without that condition, Pătraşcu and Viola (2010) proved in the cell-probe model with $w$-bit cells that a structure with query time $t$ needs $n + n / w^{O(t)}$ bits. This matches the upper bound of Pătraşcu up to the constant in the exponent. See [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/). For the dynamic version, Fredman and Saks (1989) proved an amortized bound of $\Omega(\lg n / \lg \lg n)$ per operation in the cell-probe model.

## Reductions

- **To prefix sums.** Rank is the [prefix sums](/prefix-sums/) problem on an array of 0s and 1s. So each prefix sum structure answers rank, but in $\Theta(n \lg n)$ bits if the sums are stored in full.
- **Select by rank.** Select reduces to $O(\lg n)$ rank queries by binary search, from the third identity above. So a rank structure alone answers select in $O(\lg n)$ time.
- **Sets and predecessor.** For a set $S \subseteq \{0, \ldots, n-1\}$ with characteristic vector $B$, the [predecessor](/predecessor-problem/) of $x$ in $S$ is $\text{select}_1(B, \text{rank}_1(B, x + 1))$ when $\text{rank}_1(B, x + 1) \ge 1$. So a rank/select structure is a static ordered set in $n + o(n)$ bits with $O(1)$ predecessor queries.
- **From sequences.** Rank and select on a sequence over $\sigma$ symbols reduce to rank and select on $O(\lg \sigma)$ bit vectors by the [wavelet tree](/wavelet-tree/), at a factor $O(\lg \sigma)$ in time.

## Applications

- Succinct trees: [LOUDS](/louds-tree/), [balanced parentheses](/balanced-parentheses-representation/) and [DFUDS](/dfuds/) map each tree move to rank and select on the bits of the tree.
- Compressed text indexes: the [FM-index](/fm-index/) counts the matches of a pattern with rank on the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of the text.
- Monotone sequences and sets of integers: [Elias-Fano](/elias-fano-encoding/) finds the $j$-th element by select on its upper bits. [Inverted indexes](/inverted-index/) store their lists this way.
- Arrays of items of variable length: mark the first bit of each item with a 1 in a second bit vector. Then select finds where the $j$-th item starts.

## References
