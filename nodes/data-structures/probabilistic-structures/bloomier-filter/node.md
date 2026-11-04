---
tag: 8T9R6F
kind: data-structure
slug: bloomier-filter
name: Bloomier filter
area: data-structures/probabilistic-structures
level: advanced
summary: Approximate function table that returns stored values for keys in a set.
model: word-ram
complexity:
  vars: {n: the number of keys, q: the bits per check cell, r: the bits per value}
  time: {worst: Θ(1)}
  space: {extra: Θ(n (q + r))}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [approximate-membership, hypergraph, peeling-decoding, hash-function]
see_also: [xor-filter, ribbon-filter, binary-fuse-filter, perfect-hashing, minimal-perfect-hash-function, bloom-filter, xor-gaussian-elimination]
sources:
  - paper: "Bernard Chazelle, Joe Kilian, Ronitt Rubinfeld and Ayellet Tal, The Bloomier filter, an efficient data structure for static support lookup tables, Proceedings of the Fifteenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2004)"
    locator: the immutable and mutable Bloomier filters, the encoding of the matched hash index with a mask, and the construction from a peeling order
  - paper: doi:10.1007/978-3-540-70575-8_32
    title: Martin Dietzfelbinger and Rasmus Pagh, Succinct data structures for retrieval and approximate membership, ICALP 2008
    locator: pages 385 to 396 (retrieval by linear equations, the space-efficient form of the same idea)
  - paper: doi:10.1002/rsa.20061
    title: Michael Molloy, Cores in random hypergraphs and Boolean formulas, Random Structures and Algorithms 27(1), 2005
    locator: pages 124 to 135 (the threshold for an empty 2-core of a random 3-uniform hypergraph, about 1.222 cells per key)
  - paper: doi:10.1145/3376122
    title: Thomas Mueller Graf and Daniel Lemire, Xor filters, faster and smaller than Bloom and cuckoo filters, ACM Journal of Experimental Algorithmics 25, 2020
    locator: Section 3 (peeling with three segments and a table of 1.23 n + 32 cells)
---

A Bloomier filter stores a function $f$ from a fixed set $S$ of $n$ keys to values of $r$ bits, without storing the keys. A lookup of a key $x \in S$ returns $f(x)$ exactly, and a lookup of a key outside $S$ returns "not in the set" except with a small probability $\varepsilon$. It takes $O(1)$ time and about $1.23 n (\log_2(3/\varepsilon) + r)$ bits. Chazelle, Kilian, Rubinfeld and Tal introduced it in 2004, as a [Bloom filter](/bloom-filter/) that answers "which value?" in place of "is it there?". It also lets the value of a key in $S$ change in place. Its main idea, a table of cells solved key by key along a peeling order of a random [hypergraph](/hypergraph/), is the base of the [xor filter](/xor-filter/) and of later retrieval structures.

## In plain words

You have a fixed list of words, each with a small number, and you want to look up the number of a word without storing the words.

Each word is given three cells of a table. When you look up a word, you combine its three cells with a simple bit operation, and the result says which one of the three cells is its "own" cell. A second table holds the number of each word at its own cell.

To build the tables, find a word that has a cell no other remaining word uses, put it aside, and repeat. Then fill the cells in the reverse order, so that each word's answer comes out right and later words do not disturb it.

For a word not on the list, the three cells give a random result, which is almost never a valid choice, so the lookup says "not there".

## The abstract type

The **retrieval problem with membership**: build from a function $f : S \to \{0, \ldots, 2^r - 1\}$ with $S \subseteq U$ and $|S| = n$. LOOKUP$(x)$ returns $f(x)$ for each $x \in S$, and for $x \notin S$ returns $\bot$ with probability at least $1 - \varepsilon$. SET$(x, v)$ for $x \in S$ changes $f(x)$ to $v$. There is no insert or delete of keys: $S$ is fixed at build time.

## Representation

Choose $s$ and a table size $M = 3s$. A hash function gives each key $x$ three cells $h_0(x) \in [0, s)$, $h_1(x) \in [s, 2s)$ and $h_2(x) \in [2s, 3s)$, one in each third, and a mask $\mu(x)$ of $q$ bits. The structure has two arrays of $M$ cells: $T$ with $q$ bits per cell and $R$ with $r$ bits per cell.

A *peeling order* is a sequence $(x_1, c_1), \ldots, (x_n, c_n)$ of all keys of $S$, each with one of its cells $c_i = h_{\tau_i}(x_i)$, such that $c_i$ is not a cell of any later key $x_{i+1}, \ldots, x_n$. The index $\tau(x_i) = \tau_i \in \{0, 1, 2\}$ names the key's own cell.

**Invariant (E).** For each $x \in S$,
$$ \mu(x) \oplus T[h_0(x)] \oplus T[h_1(x)] \oplus T[h_2(x)] = \tau(x) \quad\text{and}\quad R[h_{\tau(x)}(x)] = f(x). $$

## Operations

```pseudo id=main
BUILD(f, q, r)
L1  repeat choose hash functions h_0, h_1, h_2 and μ
L2  until PEEL(S) gives a peeling order (x_1, c_1), ..., (x_n, c_n)
L3  T ← M cells of q bits, all 0; R ← M cells of r bits
L4  for i ← n down to 1 do                              ▷ reverse peeling order
L5      τ ← the index with h_τ(x_i) = c_i
L6      T[c_i] ← τ ⊕ μ(x_i) ⊕ (the T cells of x_i other than c_i)
L7      R[c_i] ← f(x_i)

LOOKUP(x)
L8  τ ← μ(x) ⊕ T[h_0(x)] ⊕ T[h_1(x)] ⊕ T[h_2(x)]
L9  if τ ∈ {0, 1, 2} then return R[h_τ(x)]
L10 return ⊥

SET(x, v)                                               ▷ precondition: x is in S
L11 τ ← as in line L8; R[h_τ(x)] ← v

PEEL(S)
L12 count[c] ← the number of keys with cell c, for each cell c
L13 while some cell c has count[c] = 1 do append (the key x at c, c) to the order and remove x from its three cells
L14 return the order if it has all n keys, else fail
```

**Peeling.** Lines L12 to L14 repeatedly take a cell used by exactly one remaining key. That key is the next one in the order, and its own cell is the cell found, which no later key uses. The code finds the single key at a cell in $O(1)$ time by keeping, for each cell, the exclusive or of the indices of the keys there. If the peeling stops early, the remaining keys form a 2-core of the hypergraph, and line L1 tries new hash functions.

**Assignment.** Lines L4 to L7 run over the order backwards. When $x_i$ is processed, its own cell $c_i$ is still 0 and is set so that its equation holds. Each later write, for $x_{i-1}, \ldots, x_1$, is to a cell $c_j$ with $j < i$, which by the peeling order is not a cell of $x_i$. So the equation of $x_i$ stays true.

**Lookup and set.** Line L8 recomputes $\tau$, line L9 reads the value at the key's own cell, and line L11 overwrites it. SET does not touch $T$, so it keeps all equations.

## Example

Take $s = 2$, so $M = 6$, with $q = 4$ and $r = 3$, and these cells and masks.

| key | $h_0, h_1, h_2$ | $\mu$ | $f$ |
|---|---|---|---|
| a | 0, 2, 4 | 9 | 7 |
| b | 0, 3, 5 | 4 | 2 |
| c | 1, 3, 4 | 12 | 5 |
| d | 1, 2, 5 | 3 | not in $S$ |
| e | 0, 3, 4 | 7 | not in $S$ |

**Peel.** The counts of cells 0 to 5 are 2, 1, 1, 2, 2, 1. Cell 1 has only c, so c comes first with own cell 1; removing c leaves b alone at cell 3 and a alone at cell 4. Cell 2 has only a, so a is next with own cell 2. Then cell 5 has only b. The order is (c, 1), (a, 2), (b, 5).

**Assign, backwards.**
- b: own cell 5 is $h_2$, so $\tau = 2$. $T[5] = 2 \oplus 4 \oplus T[0] \oplus T[3] = 6$, and $R[5] = 2$.
- a: own cell 2 is $h_1$, so $\tau = 1$. $T[2] = 1 \oplus 9 \oplus T[0] \oplus T[4] = 8$, and $R[2] = 7$.
- c: own cell 1 is $h_0$, so $\tau = 0$. $T[1] = 0 \oplus 12 \oplus T[3] \oplus T[4] = 12$, and $R[1] = 5$.

So $T = [0, 12, 8, 0, 0, 6]$ and $R = [0, 5, 7, 0, 0, 2]$.

**Look up.**
- a: $9 \oplus 0 \oplus 8 \oplus 0 = 1$, so the answer is $R[h_1(a)] = R[2] = 7$. Similarly b gives $\tau = 2$ and value 2, and c gives $\tau = 0$ and value 5.
- e: $7 \oplus 0 \oplus 0 \oplus 0 = 7$, which is not in $\{0, 1, 2\}$, so the answer is $\bot$.
- d: $3 \oplus 12 \oplus 8 \oplus 6 = 1$, so the answer is $R[2] = 7$. This is a false positive, which happens with probability $3/16$ for $q = 4$.

## Correctness

Each key $x_i$ sets its own cell in line L6 so that its equation holds, and the later writes go to cells of earlier keys in the peeling order, which are not cells of $x_i$. So invariant (E) holds after BUILD, and SET keeps it. By (E), LOOKUP$(x)$ for $x \in S$ computes $\tau = \tau(x)$ and returns $R[h_{\tau(x)}(x)] = f(x)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory probes |
|---|---|---|
| build | $O(n)$ per attempt, $O(1)$ attempts in expectation | |
| lookup | $O(1)$ | 3 cells of $T$ and 1 of $R$ |
| set | $O(1)$ | 3 cells of $T$ and 1 of $R$ |
| space | $M(q + r)$ bits with $M \approx 1.23 n$ | |

**False positives.** With ideal hashing, for $x \notin S$ the mask $\mu(x)$ is uniform on $q$ bits and independent of $T$ and of the cells of $x$, so $\tau$ in line L8 is uniform, and $\Pr[\text{LOOKUP}(x) \ne \bot] = 3/2^q$. The proof is in [the complexity proof](proofs/complexity.md). For a rate $\varepsilon$ this needs $q = \lceil \log_2(3/\varepsilon) \rceil$.

**Peeling.** For a random 3-uniform hypergraph with $n$ edges and $M = cn$ vertices, the 2-core is empty with probability tending to 1 when $c > 1.222$ and the core is large when $c < 1.222$; this is the threshold of Molloy (2005). With $M = 1.23 n + O(1)$ cells in three thirds, as in the code and in the xor filter, the peeling succeeds with a constant probability, so $O(1)$ attempts suffice in expectation for large $n$. Each attempt takes $O(n)$ time.

**Space.** For $\varepsilon = 2^{-8}$ and $r = 4$, $q = \lceil \log_2(768) \rceil = 10$ and the space is about $1.23 \cdot 14 \approx 17.2$ bits per key. A [dictionary](/dictionary/) that stores the keys would need the keys themselves, and a [minimal perfect hash function](/minimal-perfect-hash-function/) with a value array would need about $1.44$ bits per key plus $r$, but would return a value for each key, with no way to say $\bot$.

## Variants

- **Xor filter.** Drop $R$, and let $T$ hold the fingerprint directly: the equation becomes $T[h_0] \oplus T[h_1] \oplus T[h_2] = \text{fingerprint}(x)$. This is the [xor filter](/xor-filter/), the case $r = 0$ with the check folded in, and it gives the rate $2^{-q}$ in $1.23 q$ bits per key.
- **Retrieval without membership.** Store $f(x)$ in place of $\tau$ and drop $R$: $T[h_0] \oplus T[h_1] \oplus T[h_2] = f(x)$. A lookup of $x \notin S$ then returns some value, and the space is $1.23 r$ bits per key. Dietzfelbinger and Pagh (2008) showed that with more hash functions and [Gaussian elimination](/xor-gaussian-elimination/) the factor $1.23$ falls to $1 + o(1)$.
- **Faster and smaller builds.** The [binary fuse filter](/binary-fuse-filter/) uses overlapping segments to reach about $1.13$ cells per key, and the [ribbon filter](/ribbon-filter/) solves a banded linear system to come within a few percent of $r$ bits per key.
- **Mutable and immutable forms.** Chazelle et al. treat both a fixed table and a mutable one, in which the values of keys of $S$ can change. This page follows the mutable form, with the separate value table $R$.

## When to use it

Use a Bloomier filter when a fixed set of keys has small values that must be read fast, keys outside the set must be rejected most of the time, and the keys are too large to store: for example a router table from many addresses to a few next hops, or a map from words to a class. Use the [xor filter](/xor-filter/) when only membership is needed, and plain retrieval without $\bot$ when each query is known to be a key of $S$. Do not use it when keys are added or removed: the whole structure must be built again.

## Pitfalls

- **Repeated keys.** If a key appears twice in the input, its two copies share all cells, so neither can ever have a cell of its own, and the peeling never succeeds. Remove repeats first; the code takes a mapping, which has none.
- **Three equal cells.** If two of the cells of a key are equal, the xor of line L8 cancels them. Use one cell in each third of the table, as the code does.
- **A table that is too small.** Below about 1.222 cells per key the peeling fails almost always, and the loop of line L1 never ends. For small $n$ the threshold is larger in practice; the code grows the table by 10 percent after each 10 failed seeds.
- **Wrong values for absent keys.** A false positive returns a real stored value, not a random one. If a wrong value is costly, make $q$ larger or check the result elsewhere.
- **SET on an absent key.** The precondition matters. SET$(x, v)$ for a false positive $x$ overwrites the value of the key whose own cell it hits. The code refuses only when $\tau \notin \{0, 1, 2\}$.

## Implementations

The Python class builds the structure in its constructor and follows the main block, with BLAKE2b for the cells and the mask, a queue for the peeling, and retries with a new seed. The method `_tau` holds line L8, which `lookup` and `set` share.

## History

Chazelle, Kilian, Rubinfeld and Tal (2004) introduced the Bloomier filter, and named it after the Bloom filter, which answers only membership. Their construction by a greedy order on a random hypergraph is the same peeling process as in the decoding of erasure codes and in the analysis of 2-cores, whose threshold for three hash functions Molloy (2005) determined. Dietzfelbinger and Pagh (2008) recast the problem as solving a linear system over GF(2), and Graf and Lemire (2020) turned the membership case into the practical [xor filter](/xor-filter/).

## References
