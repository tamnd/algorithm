---
tag: WV9S0Z
kind: data-structure
slug: binary-fuse-filter
name: Binary fuse filter
area: data-structures/probabilistic-structures
level: research
summary: Static filter improving on xor filters with a segmented, faster-to-build layout.
model: word-ram
complexity:
  vars: {n: the number of keys, r: the bits per fingerprint}
  time: {worst: Θ(1)}
  space: {extra: Θ(n r)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [xor-filter, peeling-decoding, hypergraph]
see_also: [ribbon-filter, bloomier-filter, bloom-filter-lower-bound, cuckoo-filter, bloom-filter, approximate-membership]
sources:
  - paper: doi:10.1145/3510449
    title: Thomas Mueller Graf and Daniel Lemire, Binary fuse filters, fast and smaller than xor filters, ACM Journal of Experimental Algorithmics 27, 2022
    locator: the segment layout, the segment length and size factor, construction by peeling, and the experiments (also arXiv 2201.01174)
  - paper: doi:10.4230/LIPIcs.ESA.2019.38
    title: Martin Dietzfelbinger and Stefan Walzer, Dense peelable random uniform hypergraphs, 27th European Symposium on Algorithms (ESA 2019)
    locator: fuse graphs, whose edges lie in a window of consecutive segments, and their peeling thresholds
  - paper: doi:10.1145/3376122
    title: Thomas Mueller Graf and Daniel Lemire, Xor filters, faster and smaller than Bloom and cuckoo filters, ACM Journal of Experimental Algorithmics 25, 2020
    locator: Section 3 (the xor filter that the binary fuse filter improves)
---

A binary fuse filter is an [xor filter](/xor-filter/) with a different placement of the three cells of each key. The table is cut into many segments of $L$ cells, with $L$ a power of 2. Each key picks a start segment $s$ at random and one cell in each of the segments $s$, $s + 1$ and $s + 2$. As in the xor filter, the table is built by peeling so that the xor of the three cells of each key is its $r$-bit fingerprint, and a query compares the two. This local placement lets the table peel at about $1.125 n$ cells instead of $1.23 n$, so the filter uses about $1.125 \log_2(1/\varepsilon)$ bits per key for large sets, within 13 percent of the [space lower bound](/bloom-filter-lower-bound/). Graf and Lemire introduced it in 2022, building on the fuse graphs of Dietzfelbinger and Walzer.

## In plain words

An xor filter gives each key three places, one in each third of a table, and fills the table so that the three numbers of each key combine to its code. To fill it, it looks for a place that only one key uses, sets that key aside, and repeats. This needs a table about 23 percent larger than the number of keys, or it gets stuck.

A binary fuse filter cuts the table into many small pieces in a row, and gives each key three places in three pieces next to each other. The pieces at the two ends of the row are used by fewer keys, so the setting-aside starts there easily. Each key set aside frees up the next pieces, and the process moves along the row like a wave. This works with a table only about 12 percent larger than the number of keys.

## The abstract type

As for the xor filter: BUILD$(S)$ makes a filter from a fixed set $S$ of $n$ keys, and QUERY$(x)$ returns true for each $x \in S$, and true for an $x \notin S$ with probability $2^{-r}$. There are no updates. This is the static [approximate membership problem](/approximate-membership/).

## Representation

The filter has a segment length $L$, a number $t \ge 1$ of start segments, and an array $B$ of $(t + 2)L$ cells of $r$ bits, seen as segments $0$ to $t + 1$ of $L$ cells each. A key $x$ has a start segment $s(x) \in \{0, \ldots, t - 1\}$, offsets $a_0(x), a_1(x), a_2(x) \in \{0, \ldots, L - 1\}$ and an $r$-bit fingerprint $\mathrm{fp}(x)$, all from [hash functions](/hash-function/). Its cells are
$$ h_j(x) = (s(x) + j) L + a_j(x), \qquad j = 0, 1, 2, $$
which lie in three different segments, so they are distinct.

**Invariant (X).** For each $x \in S$, $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \mathrm{fp}(x)$.

**The sizes.** The reference code of Graf and Lemire chooses, for $n \ge 2$ keys,
$$ L = 2^{\lfloor \ln n / \ln 3.33 + 2.25 \rfloor}, \qquad \text{capped at } 2^{18}, \qquad \text{capacity} = \mathrm{round}\big(n \cdot \max(1.125,\; 0.875 + 0.25 \ln(10^6)/\ln n)\big), $$
and $t = \max(1, \lceil \text{capacity}/L \rceil - 2)$, so that the table has $(t + 2)L \ge$ capacity cells. Small sets get a larger factor, because the end effects of the segments matter more when there are few of them.

| $n$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ | $10^7$ | $10^8$ |
|---|---|---|---|---|---|---|
| $L$ | 128 | 512 | 2048 | 8192 | 32768 | 131072 |
| $t$ | 9 | 23 | 56 | 136 | 342 | 857 |
| cells per key | 1.408 | 1.280 | 1.188 | 1.130 | 1.127 | 1.126 |

## Operations

```pseudo id=main
BUILD(S, r)
L1  choose L and t from n as above
L2  repeat choose the hash functions at random until PEEL(S) succeeds with order (x_1, c_1), ..., (x_n, c_n)
L3  B ← an array of (t + 2) L cells of r bits, all 0
L4  for i ← n down to 1 do
L5      B[c_i] ← fp(x_i) ⊕ the two cells of x_i other than c_i

CELLS(x)
L6  s ← s(x);  return (s L + a_0(x), (s + 1) L + a_1(x), (s + 2) L + a_2(x)) and fp(x)

PEEL(S)
L7  for each cell c: count[c] ← the number of keys that use c;  xor[c] ← the xor of their indices
L8  Q ← a queue of the cells c with count[c] = 1
L9  while Q is not empty: take c from Q; if count[c] = 1 then x ← the key xor[c], append (x, c) to the order
L10     and remove x from its three cells, adding each cell whose count becomes 1 to Q
L11 succeed when the order has all n keys

QUERY(B, x)
L12 (c_0, c_1, c_2), f ← CELLS(x);  return f = B[c_0] ⊕ B[c_1] ⊕ B[c_2]
```

Lines L2 to L5 and L7 to L11 are those of the [xor filter](/xor-filter/); only the cells of line L6 differ. In the reference code, $h_0(x)$ is a uniform cell of the first $tL$ cells taken from one 64-bit hash by a multiply-and-shift, and the offsets in the next two segments are $h_0$'s offset xored with other bits of the same hash. Because $L$ is a power of 2 this is cheap, which gives the word "binary" in the name. The Python code takes the start segment and the three offsets from independent hash words instead.

**Why it peels at a smaller size.** In a random hypergraph with edges anywhere, peeling fails above about $0.818 n$ edges for $n$ vertices, which is the 1.222 cells per key of the xor filter. In a fuse graph, the first and last segments are covered by fewer windows of three segments, so they have fewer keys for each cell and peel at once. Their removal lowers the load of the next segments, which then peel, and so on toward the middle. Dietzfelbinger and Walzer (2019) showed that with many segments this works up to a density close to the threshold at which the xor system stops having a solution at all, about $0.918$ keys per cell, that is about $1.09$ cells per key. The factor 1.125 leaves a margin for a finite number of segments.

## Example

Let $L = 2$ and $t = 2$, so $B$ has 8 cells in 4 segments $\{0, 1\}$, $\{2, 3\}$, $\{4, 5\}$, $\{6, 7\}$, and let $r = 4$. A key with start segment 0 uses segments 0, 1, 2, and one with start segment 1 uses segments 1, 2, 3.

| key | start | cells | fp |
|---|---|---|---|
| a | 0 | 0, 2, 4 | 6 |
| b | 0 | 1, 2, 5 | 10 |
| c | 1 | 2, 4, 6 | 1 |
| d | 1 | 3, 5, 7 | 13 |
| x | 0 | 1, 3, 4 | 7 |
| y | 1 | 3, 4, 6 | 2 |

**Peeling.** The counts of cells 0 to 7 are 1, 1, 3, 1, 2, 2, 1, 1. The middle segments carry the load: cell 2 is used by three keys. The queue starts with cells 0, 1, 3, 6, 7. Cell 0 gives a, which brings cell 4 to count 1. Cell 1 gives b, which brings cells 2 and 5 to count 1. Cell 3 gives d, which empties cells 5 and 7. Cell 6 gives c. The order is (a, 0), (b, 1), (d, 3), (c, 6): the end segments 0 and 3 start the peeling, as described above.

**Assignment.** Backwards: $B[6] = 1 \oplus B[2] \oplus B[4] = 1$, $B[3] = 13 \oplus B[5] \oplus B[7] = 13$, $B[1] = 10 \oplus B[2] \oplus B[5] = 10$, $B[0] = 6 \oplus B[2] \oplus B[4] = 6$. So $B = [6, 10, 0, 13, 0, 0, 1, 0]$.

**Queries.** For a, b, c and d the xors are $6$, $10$, $1$ and $13$, their fingerprints. For x, $B[1] \oplus B[3] \oplus B[4] = 10 \oplus 13 \oplus 0 = 7 = \mathrm{fp}(x)$, a false positive. For y, $13 \oplus 0 \oplus 1 = 12 \ne 2$, so y is rejected.

## Correctness

The proof is that of the xor filter: in the peeling order, the cell $c_i$ of $x_i$ is used by no later key, so the backward assignment sets each $c_i$ once and never changes a cell of $x_i$ afterwards, which makes invariant (X) true. BUILD ends with probability 1 because each try succeeds with the same positive probability. For the sizes above, the table has at least $n + t + 2$ cells, which gives a configuration that peels in one round: a private cell for each key and one spare cell in each segment. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| build | $\Theta(n)$ expected |
| query | one hash, three cell reads |
| space | $(t + 2) L r$ bits, about $1.125 n r$ for large $n$ |

**False positive rate.** For a key $x \notin S$, under ideal hashing, $\mathrm{fp}(x)$ is uniform and independent of the table and of the cells of $x$, so a query returns true with probability exactly $2^{-r}$. The argument is that of the [xor filter](/xor-filter/).

**Space.** For $r = 8$ the filter takes about $9.0$ bits per key for $n = 10^6$, against $9.84$ for an xor filter and $11.5$ for a Bloom filter with the rate $2^{-8}$. Graf and Lemire report that the three-wise filter is within 13 percent of the lower bound $\log_2(1/\varepsilon)$, and a four-wise form, with cells in four consecutive segments, within 8 percent, at a somewhat higher query cost.

**Build time.** Each try is a linear pass as for the xor filter. Graf and Lemire report that binary fuse filters are faster to build than xor filters in their experiments, in part because the cells of each key lie in a window of three segments, which helps the cache when the keys are processed in the order of their start segments.

## Variants

- **Four-wise binary fuse filter.** Four cells in four consecutive segments, about $1.075 n$ cells for large $n$ in the reference code.
- **Xor filter.** The special case of three large blocks with no coupling; see the [xor filter](/xor-filter/).
- **Ribbon filter.** Each key has a run of $w$ consecutive cells and the system is solved by Gaussian elimination on a band matrix, which allows overheads of a few percent; see the [ribbon filter](/ribbon-filter/).
- **Retrieval.** With an arbitrary value in place of the fingerprint, the same table stores a static function, as in the [Bloomier filter](/bloomier-filter/).

## When to use it

Use a binary fuse filter in place of an xor filter whenever the set is static and has more than a few thousand keys: it is smaller and builds faster, with the same query. For very small sets the size factor is large, and a plain Bloom filter or a sorted list of fingerprints can be smaller. For sets that change, use a [cuckoo filter](/cuckoo-filter/), a [quotient filter](/quotient-filter/) or a Bloom filter.

## Pitfalls

- **Duplicate keys.** Two copies of one key can never be peeled. Remove them first; the Python code does.
- **Too few segments.** The size factor 1.125 relies on many segments. Using it for a small set with only a few segments makes peeling fail most of the time; the size rule above raises the factor for small $n$.
- **A segment length that is not a power of 2.** The reference code depends on it for its bit tricks. The Python code works for any $L$, but its sizes follow the reference rule.
- **The start segment.** It must be uniform on $\{0, \ldots, t - 1\}$, not on all $t + 2$ segments, or some cells fall outside the table.
- **Expecting dynamic updates.** As with every peeling filter, a change of the set needs a rebuild.

## Implementations

The Python class follows the main block, with the size rule of the reference code, BLAKE2b for the start segment, the offsets and the fingerprint, and a FIFO queue for peeling. It removes duplicate keys first.

## History

Dietzfelbinger and Walzer (2019) introduced fuse graphs, random hypergraphs whose edges lie in a small window of consecutive segments, and showed that their peeling thresholds come close to the threshold of solvability. Graf and Lemire (2022) turned this into the binary fuse filter with power-of-2 segments, a size rule for finite $n$, and three-wise and four-wise forms, and showed in experiments that it is smaller and faster to build than their [xor filter](/xor-filter/) of 2020.

## References
