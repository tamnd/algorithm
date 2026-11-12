---
tag: 131BXM
kind: data-structure
slug: cuckoo-filter
name: Cuckoo filter
area: data-structures/probabilistic-structures
level: core
summary: Approximate set using cuckoo hashing of key fingerprints, supporting deletion.
model: word-ram
complexity:
  vars: {n: the number of stored keys, m: the number of buckets, b: the slots per bucket, f: the bits per fingerprint}
  time: {worst: Θ(b)}
  space: {extra: Θ(m b f)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [approximate-membership, cuckoo-hashing, fingerprinting, false-positive-rate]
see_also: [bloom-filter, counting-bloom-filter, quotient-filter, xor-filter, cuckoo-hashing-load-threshold, union-bound]
sources:
  - paper: doi:10.1145/2674005.2674994
    title: Bin Fan, Dave G. Andersen, Michael Kaminsky and Michael Mitzenmacher, Cuckoo filter, practically better than Bloom, CoNEXT 2014
    locator: pages 75 to 88, Sections 3 and 4 (partial-key cuckoo hashing, insert, lookup and delete, the fingerprint size, the space per key and the comparison with Bloom filters)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the Bloom filter baseline)
---

A cuckoo filter stores a short fingerprint of each key in a table of buckets, and moves fingerprints between two candidate buckets as in [cuckoo hashing](/cuckoo-hashing/). A query compares the fingerprint of the key with the entries of its two buckets, so it reads at most two buckets. Unlike a [Bloom filter](/bloom-filter/), it supports deletes, and for false positive rates below a few percent it also uses less space. The trick that makes it work is *partial-key cuckoo hashing*: the second bucket is computed from the first bucket and the fingerprint alone, so a fingerprint can move without its key. Fan, Andersen, Kaminsky and Mitzenmacher introduced it in 2014.

## In plain words

Each stored word becomes a short code, say 8 bits. Each word has two allowed shelves, and its code must sit on one of them. A shelf holds four codes.

To look up a word, compute its code and its two shelves, and look for the code there. If it is not there, the word was never stored. If it is there, the word was probably stored, but another word with the same code and shelves gives the same answer.

To store a word when both shelves are full, push out a code that is there and move it to its own other shelf. That can push out another code, and so on. The code and its present shelf give its other shelf, so the words are not needed. To remove a word, delete one copy of its code from one of its shelves.

## The abstract type

The filter solves the dynamic version of the [approximate membership problem](/approximate-membership/) for a multiset $S$ of keys. INSERT$(x)$ adds one copy of $x$, or reports that the filter is full and changes nothing. DELETE$(x)$ removes one copy of $x$, and is allowed only when $x$ has a copy in $S$. QUERY$(x)$ returns true for each $x$ in $S$, and returns true for an $x$ not in $S$ with probability at most about $2b/2^f$.

## Representation

The table $T$ has $m$ buckets, with $m$ a power of two, and each bucket holds up to $b$ fingerprints of $f$ bits. The value 0 marks an empty slot. A hash function gives each key $x$ a fingerprint $\phi(x) \in \{1, \ldots, 2^f - 1\}$ and a first bucket $i_1(x)$. A second hash function $g$ on fingerprints defines
$$ \mathrm{alt}(i, \phi) = i \oplus (g(\phi) \bmod m), \qquad i_2(x) = \mathrm{alt}(i_1(x), \phi(x)). $$
Since $\oplus$ is exclusive or, $\mathrm{alt}(\mathrm{alt}(i, \phi), \phi) = i$: from either bucket of a fingerprint, $\mathrm{alt}$ gives the other one. A single *victim* slot holds one fingerprint and its bucket when an insert has run out of kicks.

**Invariant (T).** Give each stored fingerprint $\phi$ in bucket $j$ (or in the victim slot with bucket $j$) the token $(\phi, \{j, \mathrm{alt}(j, \phi)\})$, and give each copy of a key $x$ in $S$ the token $(\phi(x), \{i_1(x), i_2(x)\})$. Then the two multisets of tokens are equal.

## Operations

```pseudo id=main
CREATE(m, b, f)
L1  T ← m empty buckets of b slots; victim ← none

INSERT(T, x)
L2  if victim ≠ none then return false                  ▷ the filter is full
L3  φ ← φ(x); i ← i_1(x)
L4  if T[i] or T[alt(i, φ)] has an empty slot then put φ there; return true
L5  i ← i or alt(i, φ), chosen at random
L6  repeat MaxKicks times
L7      swap φ with a random entry of T[i]              ▷ φ is now the evicted entry
L8      i ← alt(i, φ)                                   ▷ its other bucket
L9      if T[i] has an empty slot then put φ there; return true
L10 victim ← (i, φ); return true                        ▷ stored, but now full

QUERY(T, x)
L11 φ ← φ(x); i_1 ← i_1(x); i_2 ← alt(i_1, φ)
L12 return φ ∈ T[i_1] or φ ∈ T[i_2] or victim = (i_1 or i_2, φ)

DELETE(T, x)                                            ▷ precondition: x is in S
L13 φ ← φ(x); i_1 ← i_1(x); i_2 ← alt(i_1, φ)
L14 if φ ∈ T[i_1] or φ ∈ T[i_2] then remove one copy of φ from that bucket
L15     if victim ≠ none then put the victim back, by lines L4 to L10; return true
L16 if victim = (i_1 or i_2, φ) then victim ← none; return true
L17 return false
```

**Insert.** Line L4 puts the fingerprint in a free slot of one of its two buckets. If both are full, lines L5 to L9 evict a random entry and move it to its other bucket, which line L8 finds with $\mathrm{alt}$ and no key. After MaxKicks evictions (500 in the paper), line L10 keeps the last evicted fingerprint in the victim slot. So no stored fingerprint is ever lost, but the next insert fails at line L2 until a delete makes room.

**Query.** Line L12 reads two buckets and the victim slot.

**Delete.** Line L14 removes one copy of $\phi(x)$ from one of the two buckets of $x$. The removed entry may belong to another key $y$, but only one with the same fingerprint and the same two buckets, so it has the same token, and $y$'s query still finds the copy that $x$ left. If a victim is waiting, line L15 tries to put it back.

## Example

Take $m = 4$ buckets of $b = 2$ slots, and for the example let $g(\phi) = \phi$, so $\mathrm{alt}(i, \phi) = i \oplus (\phi \bmod 4)$. The keys have these fingerprints and buckets.

| key | $\phi$ | $i_1$ | $i_2$ |
|---|---|---|---|
| a | 5 | 0 | 1 |
| b | 6 | 0 | 2 |
| c | 9 | 0 | 1 |
| d | 7 | 1 | 2 |
| e | 13 | 0 | 1 |
| x | 7 | 2 | 1 |
| y | 3 | 3 | 0 |

Insert b, a, c, d. Bucket 0 takes b and a, and is full; c goes to its second bucket 1, and so does d. The table is $T = [\{6, 5\}, \{9, 7\}, \{\}, \{\}]$.

Insert e: buckets 0 and 1 are full. Choose bucket 0 and evict its entry 6. Its other bucket is $\mathrm{alt}(0, 6) = 0 \oplus 2 = 2$, which is empty. Now $T = [\{13, 5\}, \{9, 7\}, \{6\}, \{\}]$. The fingerprint 6 moved without the key b; b still finds it, since bucket 2 is one of its buckets.

- QUERY(e) finds 13 in bucket 0 and returns true.
- QUERY(y) looks for 3 in buckets 3 and 0, does not find it, and returns false.
- QUERY(x) looks for 7 in buckets 2 and 1, finds the 7 of d, and returns true. This is a false positive, and x has exactly the token of d, so DELETE(x) would remove d.
- DELETE(a) removes 5 from bucket 0, and then QUERY(a) returns false.

## Correctness

Each operation keeps invariant (T). An insert adds one fingerprint at one of its two buckets. An eviction moves a fingerprint $\phi$ from bucket $j$ to $\mathrm{alt}(j, \phi)$, which keeps its token, because $\{j, \mathrm{alt}(j, \phi)\} = \{\mathrm{alt}(j, \phi), j\}$. A delete removes an entry whose token equals the token of $x$. By (T), each key of $S$ has a matching token, which is an entry $\phi(x)$ in $T[i_1(x)]$, in $T[i_2(x)]$ or in the victim slot, so QUERY returns true. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory probes |
|---|---|---|
| query | $O(b)$ | 2 buckets |
| delete | $O(b)$, plus a reinsert of the victim | 2 buckets |
| insert, free slot | $O(b)$ | 2 buckets |
| insert, with evictions | $O(b \cdot \text{MaxKicks})$ in the worst case | up to MaxKicks + 2 buckets |
| space | $m b f$ bits | |

**False positive rate.** With ideal hashing, a query for a key $x \notin S$ is a false positive with probability at most
$$ \frac{2b + 1}{2^f - 1}, $$
by the [union bound](/union-bound/) over the at most $2b$ entries of its two buckets and the victim. The proof is in [the complexity proof](proofs/complexity.md). For a target rate $\varepsilon$ this needs $f \approx \log_2(2b/\varepsilon)$, which is $\log_2(1/\varepsilon) + 3$ for $b = 4$.

**Load and space.** With $b = 4$, Fan et al. (2014) report that inserts succeed until about 95 percent of the slots are full; this is an experimental figure, related to the [load threshold of cuckoo hashing](/cuckoo-hashing-load-threshold/) with buckets. The space per key is then about $(\log_2(1/\varepsilon) + 3)/0.95$ bits.

| rate $\varepsilon$ | $f$ for $b = 4$ | cuckoo bits per key at 95 percent | Bloom bits per key |
|---|---|---|---|
| 0.03 | 9 | 9.5 | 7.3 |
| 0.01 | 10 | 10.5 | 9.6 |
| 0.001 | 14 | 14.7 | 14.4 |
| 0.0001 | 17 | 17.9 | 19.2 |

The space-optimized variant with semi-sorted buckets saves one more bit per entry. With it, Fan et al. report less space than a Bloom filter for rates below about 3 percent.

**Insert time.** There is no proven bound on the number of evictions of partial-key cuckoo hashing. In practice the average stays small until the table is close to full, and grows fast near the load limit.

## Variants

- **Semi-sorting.** Sort the 4 fingerprints of a bucket and encode the sorted sequence of their top bits with one index into a table of the possible sequences, which saves 1 bit per entry.
- **Bucket size.** With $b = 2$ the load limit is about 84 percent and with $b = 8$ about 98 percent, but the rate needs $f$ to grow with $\log_2 b$. Fan et al. found $b = 4$ the best for practical rates.
- **Counting filters.** A [counting Bloom filter](/counting-bloom-filter/) also allows deletes, but at about four times the space of a Bloom filter. A [quotient filter](/quotient-filter/) stores fingerprints in one array with linear probing, and allows merging and resizing.
- **Static sets.** An [xor filter](/xor-filter/) or a [binary fuse filter](/binary-fuse-filter/) needs about $1.23 f$ or $1.13 f$ bits per key with a rate of $2^{-f}$, less than a cuckoo filter, but cannot be changed after it is built.

## When to use it

Use a cuckoo filter in memory when keys are inserted and deleted, the rate should be about 3 percent or less, and a query should touch only two cache lines. Use a Bloom filter when the filter must never refuse an insert, when filters must be merged by a bitwise OR, or when the rate is large. Do not use a cuckoo filter if the same key can be inserted more than $2b$ times, because its copies have only $2b$ slots.

## Pitfalls

- **Deleting a false positive.** If QUERY$(x)$ is a false positive and DELETE$(x)$ runs, it removes the fingerprint of another key, which then gives a false negative. Delete only keys that are known to be present.
- **Too many copies of a key.** All copies of $x$ need slots in the same two buckets. The $2b + 1$-th copy makes the insert evict for MaxKicks rounds and fill the victim slot, and the filter is then full.
- **The number of buckets must be a power of two.** Otherwise $i \oplus (g(\phi) \bmod m)$ can fall outside the table. For other sizes use $\mathrm{alt}(i, \phi) = (g(\phi) - i) \bmod m$, which is also its own inverse.
- **Using the fingerprint as the offset.** If $\mathrm{alt}(i, \phi) = i \oplus \phi$, the two buckets of a key are close for small fingerprints. Hash the fingerprint first, as the code does.
- **Small fingerprints for large tables.** There are only $2^f - 1$ fingerprints, so a bucket has at most $2^f - 1$ different other buckets. Fan et al. show that inserts start to fail early when $f$ is much smaller than about $\log_2(n)/b$.
- **A full filter.** An insert can fail when the table is far below its capacity, by bad luck. The caller must handle the failure, for example by building a larger filter.

## Implementations

The Python class follows the main block with BLAKE2b, a seeded random choice of the evicted entry, and the victim slot of the reference code of Fan et al. The pseudocode line L4 is the first loop of the helper `_place`, which DELETE also uses to put the victim back.

## History

Pagh and Rodler introduced [cuckoo hashing](/cuckoo-hashing/) in 2001, and its use for fingerprints was the obstacle: a moved fingerprint has no key from which to compute its other bucket. Fan, Andersen, Kaminsky and Mitzenmacher (2014) solved this with partial-key cuckoo hashing, in which the other bucket depends only on the present bucket and the fingerprint. They gave the bucket size 4, the semi-sorting trick and the comparison with Bloom filters.

## References
