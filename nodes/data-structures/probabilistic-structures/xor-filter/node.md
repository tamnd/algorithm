---
tag: 6QE9XB
kind: data-structure
slug: xor-filter
name: Xor filter
area: data-structures/probabilistic-structures
level: advanced
summary: Static approximate set built by solving XOR equations over fingerprints, using little space.
model: word-ram
complexity:
  vars: {n: the number of keys, r: the bits per fingerprint}
  time: {worst: Θ(1)}
  space: {extra: Θ(n r)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [approximate-membership, fingerprinting, hypergraph, peeling-decoding]
see_also: [binary-fuse-filter, ribbon-filter, bloomier-filter, bloom-filter, cuckoo-filter, bloom-filter-lower-bound, false-positive-rate]
sources:
  - paper: doi:10.1145/3376122
    title: Thomas Mueller Graf and Daniel Lemire, Xor filters, faster and smaller than Bloom and cuckoo filters, ACM Journal of Experimental Algorithmics 25, 2020
    locator: Sections 3 and 4 (the table of 1.23 n + 32 cells in three blocks, construction by peeling, the rate 2^-r, and the experiments)
  - paper: doi:10.1002/rsa.20061
    title: Michael Molloy, Cores in random hypergraphs and Boolean formulas, Random Structures and Algorithms 27(1), 2005
    locator: pages 124 to 135 (the threshold for an empty 2-core of a random 3-uniform hypergraph, about 1.222 cells per key)
  - paper: doi:10.1007/978-3-540-70575-8_32
    title: Martin Dietzfelbinger and Rasmus Pagh, Succinct data structures for retrieval and approximate membership, ICALP 2008
    locator: pages 385 to 396 (approximate membership from a retrieval structure that stores fingerprints)
---

An xor filter stores a fixed set $S$ of $n$ keys for approximate membership queries. It is an array $B$ of about $1.23 n$ cells of $r$ bits, split into three blocks. Each key $x$ has one cell $h_j(x)$ in each block and an $r$-bit fingerprint $\mathrm{fp}(x)$, and the array is built so that $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \mathrm{fp}(x)$ for each key of $S$. A query computes the three cells and the fingerprint and compares. A key of $S$ is always accepted, and any other key is accepted with probability $2^{-r}$. The array is found by peeling a random hypergraph, in linear expected time. The space is about $1.23 \log_2(1/\varepsilon)$ bits per key for a rate $\varepsilon$, against $1.44 \log_2(1/\varepsilon)$ for a [Bloom filter](/bloom-filter/). Graf and Lemire introduced it in 2020.

## In plain words

Each key gets a short code, its fingerprint, and three places in a table, one in each third. The table is filled so that, for every stored key, the three numbers in its places combine to give exactly its code. The combination used is exclusive or, which acts on each bit on its own.

To check a key, read its three places, combine them, and compare with its code. For a stored key they always match. For any other key the result is close to a random number, so it matches the code only by chance, for example once in 256 tries with 8-bit codes.

Filling the table is the hard part. It works by finding a key that has a place no other key uses, putting it aside, and repeating. The keys are then written back in reverse order. The table cannot change after that.

## The abstract type

The filter solves the static [approximate membership problem](/approximate-membership/). BUILD$(S)$ makes the filter from a set $S$ of $n$ keys. QUERY$(x)$ returns true for each $x \in S$, and true for an $x \notin S$ with probability $\varepsilon = 2^{-r}$. There is no insert or delete; a changed set needs a new build.

## Representation

Let $\ell = \lceil (\lfloor 1.23 n \rfloor + 32)/3 \rceil$. The filter has an array $B[0 \ldots 3\ell - 1]$ of $r$-bit cells, with block $j$ the cells $j\ell$ to $j\ell + \ell - 1$, and [hash functions](/hash-function/) $h_0, h_1, h_2$ and $\mathrm{fp}$, where $h_j(x)$ is a cell of block $j$ and $\mathrm{fp}(x)$ is an $r$-bit value, as in [fingerprinting](/fingerprinting/). The three cells of a key are in different blocks, so they are distinct.

**Invariant (X).** For each $x \in S$, $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \mathrm{fp}(x)$.

The keys and their cells form a 3-uniform [hypergraph](/hypergraph/): the cells are the vertices and each key is an edge with three vertices. The equations (X) are a linear system over the bits, with one unknown cell value for each vertex. Building the filter means solving it, and the [peeling](/peeling-decoding/) algorithm solves it when the hypergraph has an empty 2-core.

## Operations

```pseudo id=main
BUILD(S, r)
L1  ℓ ← ⌈(⌊1.23 n⌋ + 32) / 3⌉
L2  repeat choose h_0, h_1, h_2, fp at random until PEEL(S) succeeds with order (x_1, c_1), ..., (x_n, c_n)
L3  B ← an array of 3ℓ cells of r bits, all 0
L4  for t ← n down to 1 do
L5      B[c_t] ← fp(x_t) ⊕ the two cells of x_t other than c_t

PEEL(S)
L6  for each cell c: count[c] ← the number of keys with c among their cells;  xor[c] ← the xor of their indices
L7  Q ← a queue of the cells c with count[c] = 1
L8  while Q is not empty: take c from Q; if count[c] = 1 then x ← the key xor[c], append (x, c) to the order
L9      and remove x from its three cells, adding each cell whose count becomes 1 to Q
L10 succeed when the order has all n keys

QUERY(B, x)
L11 return fp(x) = B[h_0(x)] ⊕ B[h_1(x)] ⊕ B[h_2(x)]
```

**Peeling.** A cell with count 1 belongs to exactly one remaining key, and the xor of the indices at that cell is the index of that key, so line L8 finds it without a list. Removing the key can bring other cells to count 1. If the queue runs empty with keys left, the remaining keys form a 2-core, in which each cell has 0 or at least 2 keys, and line L2 tries new hash functions.

**Assignment.** The key $x_t$ was the only remaining key at $c_t$ when it was peeled, so no key peeled after it uses $c_t$. Going backwards, line L5 sets $B[c_t]$ after all cells of later keys are set, and nothing written later touches the cells of $x_t$. So the equation of $x_t$ holds at the end.

**The table size.** For a random 3-uniform hypergraph with $n$ edges, peeling succeeds with high probability when the number of vertices is above about $1.222 n$, and fails with high probability below it (Molloy 2005). Graf and Lemire use $1.23 n + 32$ cells, where the 32 makes small sets peel easily. In tests of the Python code with this size, about one build in twenty needed a second try.

## Example

Let $\ell = 3$, so the cells are 0 to 8 in blocks $\{0, 1, 2\}$, $\{3, 4, 5\}$, $\{6, 7, 8\}$, and $r = 4$. Let $S = \{a, b, c, d\}$ with these values.

| key | $h_0, h_1, h_2$ | fp |
|---|---|---|
| a | 0, 3, 6 | 5 |
| b | 0, 4, 7 | 9 |
| c | 1, 4, 6 | 3 |
| d | 2, 5, 8 | 12 |
| x | 1, 3, 7 | 15 |
| y | 2, 4, 8 | 7 |

**Peeling.** The counts of cells 0 to 8 are 2, 1, 1, 1, 2, 1, 2, 1, 1, so the queue starts with cells 1, 2, 3, 5, 7, 8. Cell 1 gives c, and removing c brings cells 4 and 6 to count 1. Cell 2 gives d, which empties cells 5 and 8. Cell 3 gives a, which brings cell 0 to count 1 and empties cell 6. Cell 5 now has count 0 and is skipped. Cell 7 gives b. The order is (c, 1), (d, 2), (a, 3), (b, 7).

**Assignment.** Backwards: $B[7] = 9 \oplus B[0] \oplus B[4] = 9$, $B[3] = 5 \oplus B[0] \oplus B[6] = 5$, $B[2] = 12 \oplus B[5] \oplus B[8] = 12$, and $B[1] = 3 \oplus B[4] \oplus B[6] = 3$. So $B = [0, 3, 12, 5, 0, 0, 0, 9, 0]$.

**Queries.** For a, $0 \oplus 5 \oplus 0 = 5$; for b, $0 \oplus 0 \oplus 9 = 9$; for c, $3 \oplus 0 \oplus 0 = 3$; for d, $12 \oplus 0 \oplus 0 = 12$. All match. For x, $B[1] \oplus B[3] \oplus B[7] = 3 \oplus 5 \oplus 9 = 15 = \mathrm{fp}(x)$, a false positive. For y, $12 \oplus 0 \oplus 0 = 12 \ne 7$, so y is rejected.

## Correctness

The order found by peeling has the property that the cell $c_t$ of $x_t$ is a cell of no later key $x_{t'}$, $t' > t$. So in the backward loop each $c_t$ is written once, and after it is written, no cell of $x_t$ is written again. The equation of $x_t$ is made true at line L5 and stays true, which gives invariant (X), and QUERY returns true for each key of $S$. BUILD ends with probability 1, because each try succeeds with a probability that is positive and the same for every try. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory |
|---|---|---|
| build | $\Theta(n)$ expected | $3\ell$ counts and xors, and the order, during the build |
| query | three hash words and three cell reads | |
| space | $3\ell r \approx 1.23 n r + 32 r$ bits | |

**False positive rate.** For a key $x \notin S$, under ideal hashing, $\mathrm{fp}(x)$ is uniform and independent of the table, so QUERY$(x)$ returns true with probability exactly $2^{-r}$. The proof is in [the complexity proof](proofs/complexity.md).

**Space against other filters.** For a rate $\varepsilon = 2^{-r}$ the filter uses $1.23 \log_2(1/\varepsilon)$ bits per key for large $n$, which is 23 percent above the [space lower bound](/bloom-filter-lower-bound/) $\log_2(1/\varepsilon)$.

| rate | lower bound | xor filter | Bloom filter |
|---|---|---|---|
| $2^{-8} \approx 0.0039$ | 8 | 9.84 | 11.5 |
| $2^{-16}$ | 16 | 19.7 | 23.1 |

The xor filter is smaller than a Bloom filter for every rate of the form $2^{-r}$, since $1.23 < 1.44$. The [binary fuse filter](/binary-fuse-filter/) reduces the factor 1.23 to about 1.125 or less, and the [ribbon filter](/ribbon-filter/) to a few percent above 1.

**Build time.** Each try takes $\Theta(n)$ time: line L6 is one pass over the keys, and each key is taken from the queue once and removes itself from three cells. The number of tries is geometric with a success probability that tends to 1 for large $n$ at this table size, so the expected build time is $\Theta(n)$.

## Variants

- **Xor+ filter.** Graf and Lemire also give a compressed form that stores the many zero cells of one block with a rank structure, at some cost in query time.
- **Binary fuse filter.** Cells of a key are in three consecutive segments of a table with many small segments, which peels at a smaller size and with better locality; see the [binary fuse filter](/binary-fuse-filter/).
- **Ribbon filter.** The equations are solved by Gaussian elimination on a band matrix instead of by peeling, which allows a table very close to $n$ cells; see the [ribbon filter](/ribbon-filter/).
- **Retrieval.** The same table with an arbitrary $r$-bit value $v(x)$ in place of $\mathrm{fp}(x)$ stores a static function, as in the [Bloomier filter](/bloomier-filter/). The filter is the case $v = \mathrm{fp}$, as Dietzfelbinger and Pagh (2008) observed.
- **Four hash functions.** Edges with four cells peel at a larger size, about $1.30 n$, but allow other trade-offs. The three-block form is the usual one.

## When to use it

Use an xor filter for a set that is built once and queried many times, when space and query speed both matter: for example, a filter for each immutable file of a [log-structured merge tree](/log-structured-merge-tree/), or a list of known-bad items that is shipped to clients. Each query reads exactly three cells, with no branches on the data. If keys must be added, use a [cuckoo filter](/cuckoo-filter/), a [quotient filter](/quotient-filter/) or a Bloom filter. If the smallest space or a faster build matters, use a [binary fuse filter](/binary-fuse-filter/).

## Pitfalls

- **Duplicate keys.** Two copies of one key are two edges with the same three cells, which can never be peeled, so the build loops for ever. Remove duplicates first; the Python code does.
- **Weak hash functions.** The analysis needs hash values close to random. A hash with structure can give a 2-core for every seed.
- **Mixing up the fingerprint and the cells.** The fingerprint must be independent of the three cells. If it is computed from the same bits, keys with the same cells also have the same fingerprint, and the rate grows.
- **Small $r$.** With $r = 1$ the rate is one half; the space bound holds, but the filter is of little use. Typical values are $r = 8$ or $r = 16$, because they fit a byte or a word.
- **Expecting dynamic updates.** Changing one key can change the peeling order of many others. There is no update short of a rebuild.

## Implementations

The Python class follows the main block, with BLAKE2b for the three cells and the fingerprint, a FIFO queue for peeling, and a new seed when peeling fails. It removes duplicate keys first.

## History

Peeling of random 3-uniform hypergraphs to solve xor equations was used for [minimal perfect hash functions](/minimal-perfect-hash-function/) and for the Bloomier filter of Chazelle, Kilian, Rubinfeld and Tal (2004), and the threshold of about 1.222 cells per key was found by Molloy (2005). Dietzfelbinger and Pagh (2008) showed that a retrieval structure for fingerprints gives a filter close to the space lower bound. Graf and Lemire (2020) designed the xor filter around this idea with three blocks, $1.23 n + 32$ cells and fingerprints of 8 or 16 bits, and showed in experiments that it is faster and smaller than Bloom and cuckoo filters for static sets. They later gave the [binary fuse filter](/binary-fuse-filter/).

## References
