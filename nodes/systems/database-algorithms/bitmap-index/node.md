---
tag: 4975XR
kind: data-structure
slug: bitmap-index
name: Bitmap index
aliases:
- bit-sliced index
- bitmapped index
- range-encoded bitmap index
area: systems/database-algorithms
level: intro
summary: "An index that keeps, for each value of a column, a bit vector with one bit per row. Bitwise AND, OR and NOT then answer selections."
model: word-ram
complexity:
  vars: {n: the number of rows, c: the number of distinct values of the column, w: the word length of the machine}
  time: {worst: "O(c n / w)"}
  space: {extra: "Θ(c n / w)"}
prereqs: [bit-vector, bitwise-operations, relational-model]
see_also: [roaring-bitmap, run-length-encoding, population-count, join-index, zone-map, selectivity, b-plus-tree, covering-index]
sources:
  - paper: doi:10.1007/3-540-51085-0_42
    title: "Patrick E. O'Neil, Model 204 architecture and performance, High Performance Transaction Systems (HPTS 1987), Lecture Notes in Computer Science 359, Springer (1989)"
    locator: pp. 39 to 59, the bit-map representation of the row sets of a value in Model 204
  - paper: doi:10.1145/253260.253268
    title: "Patrick O'Neil and Dallan Quass, Improved query performance with variant indexes, Proceedings of ACM SIGMOD 1997"
    locator: pp. 38 to 49, the Value-List (bitmap), Projection and Bit-Sliced indexes, and aggregates computed on bit slices
  - paper: doi:10.1145/276304.276336
    title: "Chee-Yong Chan and Yannis E. Ioannidis, Bitmap index design and evaluation, Proceedings of ACM SIGMOD 1998"
    locator: pp. 355 to 366, equality and range encoding, attribute value decomposition, and the space and time trade-off
  - paper: doi:10.1145/304182.304201
    title: "Chee-Yong Chan and Yannis E. Ioannidis, An efficient bitmap encoding scheme for selection queries, Proceedings of ACM SIGMOD 1999"
    locator: pp. 215 to 226, interval encoding
  - paper: doi:10.1145/1132863.1132864
    title: "Kesheng Wu, Ekow J. Otoo and Arie Shoshani, Optimizing bitmap indices with efficient compression, ACM Transactions on Database Systems 31(1) (2006)"
    locator: pp. 1 to 38, the word-aligned hybrid (WAH) code, logical operations on compressed words, and the comparison with BBC
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Chapter 14 (index structures), the section on bitmap indexes
---

A bitmap index on a column $A$ of a relation with $n$ rows keeps a [bit vector](/bit-vector/) of $n$ bits for each value of $A$ (equality encoding) or for each prefix of the sorted values (range encoding). A selection on $A$, or on several columns at a time, becomes a few [bitwise operations](/bitwise-operations/) on these vectors, which a machine does 32 or 64 rows at a time. With range encoding, any range predicate $lo \le A \le hi$ needs at most two bitmaps. Run-length codes such as WAH compress the bitmaps and still allow AND and OR on the compressed words.

## In plain words

Picture a table with a column that has few different values, such as a rating from 0 to 3. For each rating, you keep a long row of switches, one switch for each row of the table. The switch is on when that row has that rating.

To find the rows with rating 1 or 2, you lay the two rows of switches on top of each other and keep each switch that is on in either one. To combine a condition on rating with a condition on another column, you keep only the switches that are on in both. A computer handles 64 switches in one step.

A second way keeps, for each rating, the rows with that rating or less. Then any interval of ratings needs only two rows of switches: one for the top of the interval, and one to take away the part below it.

## The abstract type

The index answers selections on one column of a table with row identifiers $0, \ldots, n-1$. The result of each query is a set of rows, given as a bit vector $X$ with $X[r] = 1$ when row $r$ is in the set.

- `equal(I, v)`: the rows with $A = v$.
- `range(I, lo, hi)`: the rows with $lo \le A \le hi$.
- `append(I, v)`: add row $n$ with value $v$.

Results of different indexes combine by AND, OR and NOT, so a conjunction of predicates on several columns costs a few more bitwise operations. The [population count](/population-count/) of a result gives `COUNT(*)` without a visit to the table.

## Representation

Let $v_0 < v_1 < \cdots < v_{c-1}$ be the distinct values of $A$, kept in a sorted array (the domain).

- **Equality encoding.** One bitmap $E^{j}$ for each $j$, with $E^{j}[r] = 1$ if and only if $A(r) = v_j$. The $c$ bitmaps are disjoint and their OR is all ones.
- **Range encoding.** One bitmap $R^{j}$ for each $j < c - 1$, with $R^{j}[r] = 1$ if and only if $A(r) \le v_j$. The bitmap $R^{c-1}$ would be all ones, so it is not stored. Each $R^{j}$ contains $R^{j-1}$.

The invariant is the defining equation of each bitmap, for every row $r < n$, and no bit at a position $\ge n$ is set.

## Operations

```pseudo id=main
RANGE(I, lo, hi)                          ▷ the rows with lo ≤ A ≤ hi
L1  a ← the least j with v_j ≥ lo          ▷ binary search in the domain
L2  b ← the largest j with v_j ≤ hi
L3  if a > b then return the empty bitmap
L4  if I uses equality encoding then
L5      X ← 0
L6      for j ← a to b do
L7          X ← X OR E^j
L8      return X
L9  U ← R^b                                ▷ all ones when b = c − 1
L10 D ← R^(a−1) if a > 0, else 0
L11 return U AND NOT D, masked to n rows
```

With equality encoding, RANGE reads $b - a + 1$ bitmaps, up to $c$. With range encoding, it reads at most two. `equal(I, v)` is the case $lo = hi = v$: one bitmap $E^{j}$, or $R^{j}$ AND NOT $R^{j-1}$.

`append(I, v)` sets bit $n$ of $E^{j}$ for the $j$ with $v_j = v$, or of every $R^{j}$ with $v_j \ge v$ and $j < c - 1$. A value that is new gets a new bitmap: $E = 0$, or a copy of $R$ of its predecessor (no row has the new value yet). With range encoding, one append can touch $c - 1$ bitmaps, so range encoding trades update cost for query cost.

**Compression with WAH.** The word-aligned hybrid code cuts a bitmap into groups of 31 bits and writes 32-bit words. A *literal* word has its top bit 0 and holds one group as it is. A *fill* word has its top bit 1, the next bit is the fill bit, and the low 30 bits count how many consecutive groups are all 0 or all 1. Two compressed bitmaps of the same length combine without decompression:

```pseudo id=wah
WAH-OP(X, Y, ∘)                           ▷ ∘ is AND or OR; X and Y cover the same groups
L12 x ← the first word of X, y ← the first word of Y, Z ← empty
L13 while x and y exist do
L14     if x and y are both fills then
L15         k ← min(count(x), count(y))
L16         APPEND-FILL(Z, bit(x) ∘ bit(y), k)
L17     else
L18         k ← 1                             ▷ a literal covers one group
L19         APPEND-LITERAL(Z, group(x) ∘ group(y))
L20     count(x) ← count(x) − k, count(y) ← count(y) − k
L21     if count(x) = 0 then x ← the next word of X
L22     if count(y) = 0 then y ← the next word of Y
L23 return Z
```

The group of a fill word is 31 copies of its fill bit, and a literal has count 1. APPEND-LITERAL turns an all-zero or all-one group into a fill, and both APPEND procedures merge a new fill into a last word of Z that is a fill with the same bit.

## Example

The column $A = [2, 0, 3, 1, 2, 0, 3, 2]$ has $n = 8$ rows and $c = 4$ values. Each bitmap is written as rows 0 to 7 from left to right.

| value $v_j$ | $E^{j}$ (rows with $A = v_j$) | $R^{j}$ (rows with $A \le v_j$) |
|---|---|---|
| 0 | 01000100 | 01000100 |
| 1 | 00010000 | 01010100 |
| 2 | 10001001 | 11011101 |
| 3 | 00100010 | not stored (all ones) |

The query $1 \le A \le 2$ has $a = 1$ and $b = 2$.

- Equality encoding: $E^{1}$ OR $E^{2}$ = 00010000 OR 10001001 = 10011001.
- Range encoding: $R^{2}$ AND NOT $R^{0}$ = 11011101 AND 10111011 = 10011001.

Both give rows 0, 3, 4 and 7. The query $1 \le A \le 3$ reads three bitmaps with equality encoding and only $R^{0}$ with range encoding, since $R^{3}$ is all ones.

**WAH.** Take $n = 200$ rows, so 7 groups of 31 bits (the last group has 14 real bits and 17 bits of padding). Let $X$ have rows 62 to 199 set, and $Y$ rows 0 to 99.

| bitmap | groups | WAH words |
|---|---|---|
| $X$ | 0 0 1 1 1 1 L | 0x80000002, 0xC0000004, 0x00003FFF |
| $Y$ | 1 1 1 L 0 0 0 | 0xC0000003, 0x0000007F, 0x80000003 |
| $X$ AND $Y$ | 0 0 1 L 0 0 0 | 0x80000002, 0xC0000001, 0x0000007F, 0x80000003 |
| $X$ OR $Y$ | 1 1 1 1 1 1 L | 0xC0000006, 0x00003FFF |

WAH-OP for AND takes five steps for seven groups: fill 0 (2) with fill 1 (3) gives a 0-fill of 2 groups; fill 1 (4) with the rest of fill 1 (1) gives a 1-fill of 1; the rest of fill 1 (3) with the literal 0x7F gives 0x7F; fill 1 (2) with fill 0 (3) gives a 0-fill of 2; and the literal 0x3FFF with the last 0-fill group gives an all-zero group, which merges into the 0-fill before it.

On a larger case, a column of $n = 10\,000$ rows with $c = 100$ values drawn uniformly by `random.Random(1)` has an equality index of $100 \times 10\,000$ bits, or 31,250 words of 32 bits. WAH stores it in 15,002 words. The same values in sorted order compress to 493 words, because each bitmap is then one run of ones, which takes about five words: a 0-fill, a literal, a 1-fill, a literal and a 0-fill.

## Correctness

For equality encoding, RANGE returns the OR of the $E^{j}$ with $lo \le v_j \le hi$, which is the set of rows whose value lies in $[lo, hi]$, because each row has exactly one value. For range encoding, the rows with $A \le hi$ are exactly $R^{b}$, since $v_b$ is the largest value at most $hi$, and the rows with $A < lo$ are exactly $R^{a-1}$, since $v_{a-1}$ is the largest value below $lo$. Their difference is the answer. WAH-OP is correct because each step applies the operation to the same groups of $X$ and $Y$, and the appends write those result groups in order. The full proof is below.

## Complexity

In the [word RAM](/word-ram/) with words of $w$ bits, one bitmap of $n$ bits has $\lceil n / w \rceil$ words.

| operation | equality encoding | range encoding |
|---|---|---|
| find $a$ and $b$ | $O(\log c)$ | $O(\log c)$ |
| `equal` | $O(n / w)$, one bitmap | $O(n / w)$, two bitmaps |
| `range` | $O((b - a + 1) \, n / w)$, up to $O(c n / w)$ | $O(n / w)$, at most two bitmaps |
| `append` | $O(1)$ bit set | up to $c - 1$ bit sets |
| space | $c n$ bits | $(c - 1) n$ bits |

- **Against a list of row ids.** A [B+ tree](/b-plus-tree/) that stores a list of row ids for each value needs $n$ row ids of $r$ bits each, $n r$ bits in all. The uncompressed equality bitmaps need $c n$ bits. So they are smaller when $c < r$, for example fewer than 32 values against 32-bit row ids. Compression moves this limit far up for sparse bitmaps.
- **WAH.** Each step of WAH-OP finishes at least one word of $X$ or of $Y$: two fills drop the shorter count to zero, and a step with a literal finishes that literal. So the loop runs at most $|X| + |Y|$ times and writes at most that many words. The time is $O(|X| + |Y|)$ word operations, whatever $n$ is. Wu, Otoo and Shoshani prove a bound of this kind, and also prove that the compressed equality index of one column takes $O(n)$ words in total.

## Variants

- **Bit-sliced index.** O'Neil and Quass store one bitmap $B_i$ for each binary digit $i$ of the value. The index has $\lceil \lg (\max A + 1) \rceil$ bitmaps whatever $c$ is, and a sum over a result set $F$ is $\sum_i 2^i \cdot \mathrm{popcount}(B_i \text{ AND } F)$. Range predicates on bit slices take a pass over all slices.
- **Interval encoding.** Chan and Ioannidis (1999) give an encoding in which each bitmap marks the rows whose value lies in a window of about $c/2$ consecutive values. It uses about half the bitmaps of range encoding, and each range or equality predicate still needs at most two of them.
- **Multi-component (attribute value decomposition).** Chan and Ioannidis (1998) write each value in a mixed radix, for example $v = 10 x + y$, and keep a small index for each digit. This trades space against the number of bitmaps that a query reads.
- **Binning.** For a column with many values, a bitmap marks a bin of values. The rows of the edge bins are then checked against the column. This makes the index a filter, like a [zone map](/zone-map/) at row level.
- **Compression.** Byte-aligned codes such as BBC compress better, while WAH works on whole words and runs logical operations faster, as Wu, Otoo and Shoshani measured. [Roaring bitmaps](/roaring-bitmap/) split the row ids into chunks of $2^{16}$ and store each chunk as an array, a bitmap or a list of runs. Plain [run-length encoding](/run-length-encoding/) is the base of the fill words.
- **Bitmap join index.** The bitmap of a value of a dimension table marks the rows of the fact table that join with it. See [join index](/join-index/).

## When to use it

Use a bitmap index on columns with few distinct values in read-mostly analytic data: star-schema dimensions, flags, status codes, and ad hoc conjunctions of many such predicates. It also helps for counts, because a count is a population count. Prefer a B+ tree for a column with many distinct values that is read by point lookups, and for data with frequent updates. Use range encoding when range predicates dominate, and equality encoding when updates or equality predicates dominate.

## Pitfalls

- **NOT without a mask.** NOT sets the bits of positions past the last row (the padding of the last word). Mask the result to $n$ bits, as line L11 does.
- **NULLs and deleted rows.** NOT $E^{j}$ also returns rows where $A$ is NULL and rows that were deleted. Keep a bitmap of the existing non-NULL rows and AND it into each negation.
- **Range encoding with equality bitmaps.** A range query on an equality-encoded index on a column with many values reads up to $c$ bitmaps. Pick range or interval encoding for such workloads.
- **Updates on compressed bitmaps.** A change of one row rewrites a word that covers many rows, and in a system with locks it can block every row of that word. Bitmap indexes suit bulk loads and appends, not frequent single-row updates.
- **Different lengths in WAH-OP.** Both operands must cover the same number of rows. Extend the shorter one with a 0-fill first.

## Implementations

## History

Patrick O'Neil described the bitmap representation of the rows of a value in the Model 204 system of Computer Corporation of America, at the HPTS workshop of 1987, printed in 1989. O'Neil and Quass (1997) compared it with the projection index and introduced the bit-sliced index. Chan and Ioannidis studied the design space of encodings: equality, range and multi-component encodings in 1998, and interval encoding in 1999. Wu, Otoo and Shoshani gave the WAH code and its analysis in 2006; their FastBit library at Lawrence Berkeley National Laboratory uses it.

## References
