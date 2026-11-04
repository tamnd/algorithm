---
tag: K1BXC2
kind: data-structure
slug: ribbon-filter
name: Ribbon filter
area: data-structures/probabilistic-structures
level: research
summary: Space-efficient static approximate set built from solving banded linear systems over GF(2).
model: word-ram
complexity:
  vars: {n: the number of keys, r: the bits per fingerprint, w: the ribbon width}
  time: {worst: Θ(w)}
  space: {extra: Θ(n r)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [xor-filter, gaussian-elimination, xor-gaussian-elimination]
see_also: [binary-fuse-filter, bloomier-filter, bloom-filter-lower-bound, log-structured-merge-tree, approximate-membership, bloom-filter]
sources:
  - paper: "Peter C. Dillinger and Stefan Walzer, Ribbon filter, practically smaller than Bloom and Xor, arXiv:2103.02515 (2021)"
    locator: the standard ribbon, on-the-fly banded elimination, back substitution, the homogeneous variant, and the space and time experiments
  - paper: "Peter C. Dillinger, Lorenz Hübschle-Schneider, Peter Sanders and Stefan Walzer, Fast succinct retrieval and approximate membership using ribbon, 20th International Symposium on Experimental Algorithms (SEA 2022), arXiv:2109.01892"
    locator: bumped ribbon retrieval and its overhead, and the comparison with other retrieval structures
  - paper: "Martin Dietzfelbinger and Stefan Walzer, Efficient Gauss elimination for near-quadratic matrices with one short random block per row, with applications, 27th European Symposium on Algorithms (ESA 2019)"
    locator: the matrix with one random block of w columns per row and the analysis of its elimination
---

A ribbon filter stores a fixed set $S$ of $n$ keys for approximate membership queries, like an [xor filter](/xor-filter/), but solves its xor equations by a fast form of [Gaussian elimination](/gaussian-elimination/) instead of peeling. Each key $x$ gets a start $s(x)$, a random $w$-bit coefficient row $c(x)$, and an $r$-bit fingerprint $\mathrm{fp}(x)$. The filter is an array $Z$ of $m$ values of $r$ bits with $\bigoplus_{j : c_j(x) = 1} Z[s(x) + j] = \mathrm{fp}(x)$ for every key. Since each row's ones lie in a band of width $w$ starting at $s(x)$, the matrix is close to a band matrix, and the system can be solved one key at a time in a table indexed by the leading column. With $w = 64$ this works for $m$ only a few percent above $n$, so the filter uses close to $\log_2(1/\varepsilon)$ bits per key for a rate $\varepsilon = 2^{-r}$. Dillinger and Walzer introduced it in 2021.

## In plain words

An xor filter stores, for each key, an equation: the combination of three table cells must give the key's code. It solves all equations by setting aside keys one by one. That needs a table about 23 percent larger than the number of keys.

A ribbon filter lets each equation use a short run of nearby cells, chosen at random, instead of three cells. Equations whose runs start at the same place are combined, which moves the start of one of them further along. Every equation then gets a place of its own, and the table can be filled from the end back to the start.

Because each equation only touches a short stretch of the table, all of this is fast. And the table needs to be only a few percent larger than the number of keys.

## The abstract type

The filter solves the static [approximate membership problem](/approximate-membership/). BUILD$(S)$ makes the filter from a set $S$ of $n$ keys, and QUERY$(x)$ returns true for each $x \in S$, and true for an $x \notin S$ with probability $2^{-r}$. There are no updates.

## Representation

The filter has a width $w$, a number of rows $m \ge w$, and an array $Z[0 \ldots m-1]$ of $r$-bit values. [Hash functions](/hash-function/) give each key $x$:

- a start $s(x) \in \{0, \ldots, m - w\}$;
- a coefficient row $c(x) \in \{0, 1\}^w$ with $c_0(x) = 1$, where bit $j$ stands for row $s(x) + j$ of $Z$;
- a fingerprint $\mathrm{fp}(x) \in \{0, \ldots, 2^r - 1\}$.

**Invariant (R).** For each $x \in S$, $\bigoplus_{j : c_j(x) = 1} Z[s(x) + j] = \mathrm{fp}(x)$.

These are $n$ linear equations over $\mathrm{GF}(2)$, one for each key, with $r$ right-hand sides at once, and $Z$ is a solution. During the build, the filter keeps a table of *stored rows* $(C[i], B[i])$, where $C[i]$ is either 0 or a $w$-bit row whose lowest set bit is column $i$, as in [xor Gaussian elimination](/xor-gaussian-elimination/) in echelon form.

## Operations

```pseudo id=main
BUILD(S, r, w)
L1  m ← ⌈(1 + δ) n⌉ + w;  C, B ← arrays of m rows, all 0
L2  repeat with new hash functions until INSERT-ROW succeeds for every x ∈ S, starting with empty C and B

INSERT-ROW(s, c, b)                    ▷ c has bit 0 set; bit j of c is column s + j
L3  loop
L4      if C[s] = 0 then C[s] ← c; B[s] ← b; return success
L5      c ← c ⊕ C[s];  b ← b ⊕ B[s]
L6      if c = 0 then return (success if b = 0, else failure)
L7      j ← the index of the lowest set bit of c;  s ← s + j;  c ← c shifted right by j

BACK-SUBSTITUTE
L8  for i ← m − 1 down to 0 do
L9      Z[i] ← B[i] ⊕ the xor of Z[i + j] over the bits j ≥ 1 of C[i]     ▷ Z[i] ← 0 when C[i] = 0

QUERY(Z, x)
L10 return fp(x) = the xor of Z[s(x) + j] over the bits j of c(x)
```

**On-the-fly elimination.** Lines L3 to L7 add one equation to a system in echelon form. If the leading column $s$ is free, the row is stored there. Otherwise it is xored with the stored row of that column, which clears its lowest bit, and the row moves to its new lowest set bit. The row stays $w$ bits wide relative to its current start, because both rows of a xor have their bits in $[s, s + w)$. A row that becomes 0 is a sum of stored rows: it is redundant if its right side is also 0, which happens for a repeated key, and contradicts them otherwise, which makes the build try new hash functions.

**Back substitution.** Each stored row $i$ has leading column $i$ and other columns above $i$, so going from the last row to the first, line L9 knows all other values and sets $Z[i]$ to satisfy row $i$. Rows with $C[i] = 0$ are free, and the filter sets them to 0.

**The overhead.** Let $\delta$ be the relative overhead, $m \approx (1 + \delta) n$. The build fails when some column range receives more independent rows than it has columns. Wider rows spread each key over more columns and allow smaller $\delta$. In tests of the Python code with 3000 keys and $m = \lceil (1 + \delta) n \rceil + w$, all builds failed for $w = 16$ up to $\delta = 0.1$; for $w = 32$, 9 of 10 succeeded at $\delta = 0.1$; and for $w = 64$, all succeeded from $\delta = 0.02$. Dillinger and Walzer analyse how small $\delta$ can be for a given $w$.

## Example

Let $w = 4$, $m = 6$ and $r = 4$. A row is written as the set of its columns.

| key | $s$ | columns | fp |
|---|---|---|---|
| a | 0 | 0, 1, 3 | 5 |
| b | 0 | 0, 1, 2 | 9 |
| c | 1 | 1, 3 | 3 |
| d | 2 | 2, 5 | 12 |
| x | 1 | 1, 2 | 15 |
| y | 2 | 2, 3, 4 | 1 |

**Elimination.** a is stored at row 0. b also starts at column 0, so it is xored with row 0: columns $\{0, 1, 2\} \oplus \{0, 1, 3\} = \{2, 3\}$ with right side $9 \oplus 5 = 12$, and it is stored at row 2. c is stored at row 1. d starts at column 2, which is taken: $\{2, 5\} \oplus \{2, 3\} = \{3, 5\}$ with right side $12 \oplus 12 = 0$, and it is stored at row 3. The stored rows are now
$$ 0 : \{0, 1, 3\} \to 5, \quad 1 : \{1, 3\} \to 3, \quad 2 : \{2, 3\} \to 12, \quad 3 : \{3, 5\} \to 0. $$

**Back substitution.** Rows 5 and 4 are free, so $Z[5] = Z[4] = 0$. Then $Z[3] = 0 \oplus Z[5] = 0$, $Z[2] = 12 \oplus Z[3] = 12$, $Z[1] = 3 \oplus Z[3] = 3$, and $Z[0] = 5 \oplus Z[1] \oplus Z[3] = 6$. So $Z = [6, 3, 12, 0, 0, 0]$.

**Queries.** For a, $Z[0] \oplus Z[1] \oplus Z[3] = 6 \oplus 3 \oplus 0 = 5$. For b, $6 \oplus 3 \oplus 12 = 9$. For c, $3 \oplus 0 = 3$, and for d, $12 \oplus 0 = 12$. All match. For x, $Z[1] \oplus Z[2] = 15 = \mathrm{fp}(x)$, a false positive. For y, $12 \oplus 0 \oplus 0 = 12 \ne 1$, so y is rejected.

Adding a second copy of a gives a row that becomes 0 with right side 0, which is skipped. A key with the row of a but fingerprint 6 would become 0 with right side $6 \oplus 5 \ne 0$, and the build would need new hash functions.

## Correctness

Each operation of lines L5 and L7 replaces a row by its xor with a stored row, or shifts the index of its columns, so every equation of a key is a xor of stored rows, and every stored row is a xor of key equations. The system of stored rows therefore has the same solutions as the system of the keys. The stored rows have distinct leading columns, so back substitution solves them, and invariant (R) holds. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| build | expected $O(n w)$ bit operations for the elimination, $O(m w)$ for back substitution |
| query | the xor of up to $w$ values, $\Theta(w)$ in the row-major layout |
| space | $m r \approx (1 + \delta) n r$ bits |

**False positive rate.** For $x \notin S$, $c(x) \ne 0$ and $\mathrm{fp}(x)$ is uniform and independent of $Z$, so QUERY$(x)$ returns true with probability exactly $2^{-r}$. The proof is in [the complexity proof](proofs/complexity.md).

**Word operations.** On a machine with $w$-bit words, a row is one word, and each step of lines L5 and L7 is a few word operations. Dillinger and Walzer store $Z$ column by column, so that a query is $r$ parity computations of a $w$-bit word, and the elimination of one key takes a small expected number of steps.

**Space against other filters.** For a rate $2^{-8}$, the [space lower bound](/bloom-filter-lower-bound/) is 8 bits per key, an xor filter uses 9.84 and a [binary fuse filter](/binary-fuse-filter/) about 9.0 for large $n$. A ribbon filter with $w = 64$ and $\delta = 0.05$ uses about 8.4. The SEA 2022 paper on bumped ribbon retrieval reports overheads below one percent with fast queries.

## Variants

- **Homogeneous ribbon.** All right sides are 0 during the build, and the free rows of $Z$ are filled with random values, so the system is always solvable and no retry is needed. The query still compares with $\mathrm{fp}(x)$. The rate is then slightly above $2^{-r}$, because $Z$ is a random solution and not an exact fit. Dillinger and Walzer describe it.
- **Bumped ribbon retrieval.** Keys in ranges that are too full are bumped to a second structure, which allows very small overhead with fast construction (Dillinger, Hübschle-Schneider, Sanders and Walzer).
- **Fractional bits per key.** With an interleaved column layout, different blocks of $Z$ can use $r$ or $r + 1$ bits, which gives any rate between the powers of 2.
- **Retrieval.** With an arbitrary $r$-bit value $v(x)$ in place of $\mathrm{fp}(x)$, the same structure stores a static function, as in the [Bloomier filter](/bloomier-filter/).

## When to use it

Use a ribbon filter for a static set when space is the main cost, for example for the filters of the many immutable files of a [log-structured merge tree](/log-structured-merge-tree/): the RocksDB key-value store offers a ribbon filter policy for this. Its build is slower than that of a Bloom filter and needs memory for the stored rows, and its query reads a band of $w$ values instead of three cells, so for the fastest queries a [binary fuse filter](/binary-fuse-filter/) or a blocked Bloom filter can be better.

## Pitfalls

- **Width and overhead.** A small $w$ with a small $\delta$ makes the build fail for every seed. Use $w = 64$ or more for overheads of a few percent.
- **The leading bit.** Bit 0 of $c(x)$ must be 1, or a query for a key whose row is 0 compares $\mathrm{fp}(x)$ with 0, and the elimination has no leading column for it.
- **Starts near the end.** The start must be at most $m - w$, so that every column of the row exists.
- **Repeated keys.** These are harmless here, since they give redundant rows, unlike in peeling filters. Two different keys with the same hash values and different fingerprints are not, and force a retry.
- **Expecting updates.** Adding a key can be done by one more elimination step only while the system stays solvable, and removing one is not supported; plan for rebuilds.

## Implementations

The Python class follows the main block with rows as Python integers, the start, row and fingerprint from BLAKE2b, and a new seed when a row contradicts the stored ones. It stores $Z$ row by row, so a query costs $\Theta(w)$ steps.

## History

Dietzfelbinger and Walzer (2019) studied linear systems with one short random block of ones per row and showed that they can be solved fast by elimination in the order of the starting positions, with small overhead. Dillinger and Walzer (2021) turned this into the ribbon filter, with on-the-fly elimination, back substitution, the homogeneous form, and an implementation that was added to RocksDB. Dillinger, Hübschle-Schneider, Sanders and Walzer (2022) added bumping for retrieval with very small overhead.

## References
