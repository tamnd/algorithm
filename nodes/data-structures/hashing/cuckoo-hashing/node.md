---
tag: FHYWMC
kind: data-structure
slug: cuckoo-hashing
name: Cuckoo hashing
aliases:
- cuckoo hash table
- two-choice cuckoo hashing
area: data-structures/hashing
level: core
summary: Two tables with two hash functions and worst-case O(1) lookup, using eviction on insert.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of keys in the table, r: the number of cells of each table}
  time: {worst: O(1), expected: O(1) amortized}
  space: {extra: Θ(n)}
prereqs: [hash-table, open-addressing, universal-hashing, load-factor]
see_also: [cuckoo-hashing-load-threshold, cuckoo-filter, power-of-two-choices, perfect-hashing, linear-probing, robin-hood-hashing, hopscotch-hashing, tabulation-hashing]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.002
    title: Rasmus Pagh and Flemming Friche Rodler, Cuckoo hashing, Journal of Algorithms 51(2), 2004
    locator: pages 122 to 144 (the algorithm with MaxLoop, and the analysis of insertion)
  - paper: doi:10.1007/s00224-004-1195-x
    title: Dimitris Fotakis, Rasmus Pagh, Peter Sanders and Paul Spirakis, Space efficient hash tables with worst case constant access time, Theory of Computing Systems 38, 2005
    locator: pages 229 to 248 (d-ary cuckoo hashing)
  - paper: doi:10.1137/080728743
    title: Adam Kirsch, Michael Mitzenmacher and Udi Wieder, More robust hashing, cuckoo hashing with a stash, SIAM Journal on Computing 39, 2009
    locator: pages 1543 to 1561 (the stash)
  - paper: doi:10.1145/2220357.2220361
    title: Mihai Pătrașcu and Mikkel Thorup, The power of simple tabulation hashing, Journal of the ACM 59, 2012
    locator: the section on cuckoo hashing with simple tabulation
---

Cuckoo hashing is a [hash table](/hash-table/) with two tables $T_1$ and $T_2$ of $r$ cells each and two [hash functions](/hash-function/) $h_1$ and $h_2$, in which each key $k$ is stored either in $T_1[h_1(k)]$ or in $T_2[h_2(k)]$. A search or a delete looks at these two cells only, so it takes $O(1)$ time in the worst case. An insert puts the new key in its first cell and, if that cell is full, moves the old key to its other cell, and so on, like a cuckoo chick that pushes the other eggs out of the nest. Pagh and Rodler proved that, when $r \ge (1 + \varepsilon) n$ and the hash functions are random enough, an insert takes $O(1)$ expected amortized time.

## In plain words

Each item has two possible homes, one in each of two rows of boxes. To find an item, you look in its two homes and nowhere else. So a search never takes more than two looks.

To add an item, put it in its home in the first row. If an old item was there, take the old item out and move it to its other home, in the second row. If that box was full too, take that item out and move it to its other home, and so on, until an item lands in an empty box. Sometimes the moves go around in a circle and never end. Then the table picks two new rules to compute the homes and puts every item in again. If the rows have enough boxes, this is rare.

## The abstract type

Cuckoo hashing implements the [dictionary](/dictionary/) abstract type on a finite map $D$ with distinct keys: `insert(T, k, v)` sets $D(k) = v$, `search(T, k)` returns $D(k)$ or NIL, `delete(T, k)` removes $k$, and `size(T)` returns $n = |D|$. Like each hash table, it needs only an equality test and hash functions on the keys, and it does not support ordered queries.

## Representation

The fields are two arrays $T_1[0 \ldots r-1]$ and $T_2[0 \ldots r-1]$, each cell empty (NIL) or holding one pair $(k, v)$; two hash functions $h_1, h_2$ from keys to $\{0, \ldots, r-1\}$; the count $n$; a constant $\varepsilon$ with $0 < \varepsilon \le 1$; and the bound $\text{MaxLoop} = \lceil 3 \log_{1+\varepsilon} r \rceil$ of Pagh and Rodler.

**Invariant.**

- **(C1) Placement.** Each pair $(k, v)$ of the table is in $T_1[h_1(k)]$ or in $T_2[h_2(k)]$.
- **(C2) Distinct keys.** No key occurs in two cells.
- **(C3) Count.** $n$ is the number of full cells.
- **(C4) Space.** $r \ge (1 + \varepsilon) n$.

The map is $D = \{(k, v) : (k, v)$ is in a cell of $T_1$ or $T_2\}$.

## Operations

```pseudo id=main
CUCKOO-SEARCH(T, k)
L1  if T1[h1(k)] holds key k then return its value
L2  if T2[h2(k)] holds key k then return its value
L3  return NIL

CUCKOO-INSERT(T, k, v)
L4  if T1[h1(k)] or T2[h2(k)] holds key k then replace its value by v; return
L5  if r < (1 + ε)(n + 1) then REHASH(T, 2r, ∅)
L6  x ← (k, v)
L7  repeat MaxLoop times
L8      swap x and T1[h1(key of x)]
L9      if x = NIL then n ← n + 1; return
L10     swap x and T2[h2(key of x)]
L11     if x = NIL then n ← n + 1; return
L12 REHASH(T, r, {x})                        ▷ x is the pair without a cell

CUCKOO-DELETE(T, k)
L13 if T1[h1(k)] holds key k then T1[h1(k)] ← NIL; n ← n − 1
L14 else if T2[h2(k)] holds key k then T2[h2(k)] ← NIL; n ← n − 1

REHASH(T, r′, X)                             ▷ put all pairs and the pairs of X into new tables
L15 S ← the pairs of T1 and T2, together with X
L16 r ← r′; pick new h1, h2 at random; empty T1 and T2 with r cells each; n ← 0
L17 place each pair of S by lines L6 to L11; if one fails, go back to line L16
```

**Search.** Lines L1 to L3 look at the two cells where $k$ can be, by (C1). The cost is two hash values and two comparisons, so $O(1)$ in the worst case.

**Insert.** Line L4 handles a key that is already present. Line L5 doubles the tables when a new key would break (C4). Lines L6 to L11 are the eviction walk: $x$ is the pair that has no cell. Line L8 puts $x$ in its cell of $T_1$ and takes out the pair that was there, which becomes the new $x$. If the cell was empty, the walk ends. Line L10 does the same in $T_2$. The walk stops after MaxLoop rounds. Then line L12 calls REHASH with the pair that still has no cell.

**Delete.** Lines L13 and L14 clear the cell that holds $k$. No other pair moves, and no tombstone is needed, because a search never goes past the two cells of its key.

**Rehash.** Line L15 collects every pair. Line L16 picks new hash functions, for example new random members of a [universal family](/universal-hash-family/), and empties the tables. Line L17 puts the pairs back with the eviction walk. If one walk fails, it starts again with new functions.

## Example

Take $r = 11$, $\varepsilon = 0.1$, so $\text{MaxLoop} = \lceil 3 \log_{1.1} 11 \rceil = 76$. To keep the numbers simple, let $h_1(k) = k \bmod 11$ and $h_2(k) = \lfloor k / 11 \rfloor \bmod 11$. Insert the keys 20, 50, 53, 75, 100, 67, 105, 3, 36 and 39, in this order. Condition (C4) holds up to $n = 10$, since $11 \ge 1.1 \cdot 10$.

| key | $h_1$ | $h_2$ | the walk |
|---|---|---|---|
| 20 | 9 | 1 | 20 to $T_1[9]$ |
| 50 | 6 | 4 | 50 to $T_1[6]$ |
| 53 | 9 | 4 | 53 to $T_1[9]$, 20 out to $T_2[1]$ |
| 75 | 9 | 6 | 75 to $T_1[9]$, 53 out to $T_2[4]$ |
| 100 | 1 | 9 | 100 to $T_1[1]$ |
| 67 | 1 | 6 | 67 to $T_1[1]$, 100 out to $T_2[9]$ |
| 105 | 6 | 9 | 105 to $T_1[6]$, 50 out to $T_2[4]$, 53 out to $T_1[9]$, 75 out to $T_2[6]$ |
| 3 | 3 | 0 | 3 to $T_1[3]$ |
| 36 | 3 | 3 | 36 to $T_1[3]$, 3 out to $T_2[0]$ |
| 39 | 6 | 3 | 39 to $T_1[6]$, 105 out to $T_2[9]$, 100 out to $T_1[1]$, 67 out to $T_2[6]$, 75 out to $T_1[9]$, 53 out to $T_2[4]$, 50 out to $T_1[6]$, 39 out to $T_2[3]$ |

At the end, the full cells are $T_1[1] = 100$, $T_1[3] = 36$, $T_1[6] = 50$, $T_1[9] = 75$, and $T_2[0] = 3$, $T_2[1] = 20$, $T_2[3] = 39$, $T_2[4] = 53$, $T_2[6] = 67$, $T_2[9] = 105$. The insert of 39 moves seven old keys, and 39 itself is pushed out of its first cell and ends in its second cell. A search for 67 looks at $T_1[1] = 100$ and then at $T_2[6] = 67$.

A walk can fail. The keys 1, 122 and 243 all have $h_1 = 1$ and $h_2 = 0$. Two cells cannot hold three keys, so the third insert moves the keys around these two cells until MaxLoop rounds pass, and then line L12 rehashes.

## Correctness

Each operation keeps (C1) to (C4) and returns what the dictionary asks for. Search is correct because by (C1) a pair with key $k$ can only be in the two cells that it looks at. The eviction walk keeps a weaker form of (C1): each pair in a cell is in one of its own two cells, and exactly one pair, $x$, has no cell. When $x$ becomes NIL, every pair has a cell again, and the set of pairs is the old set plus $(k, v)$. Delete clears the only cell with key $k$. REHASH starts from all pairs and ends only when all of them are placed by the same walk. Insert can run forever in theory, if each new pair of hash functions fails, but each REHASH succeeds with positive probability, so an insert ends with probability 1. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Search and delete.** Each looks at two cells, so each takes $O(1)$ time in the worst case, with no assumption on the keys or on the hash functions. This is the main point of cuckoo hashing.

**Insert.** Without a rehash, an insert takes $O(\text{MaxLoop}) = O(\log r)$ time in the worst case. With rehashes, it has no worst-case bound. Pagh and Rodler prove this bound: if $r \ge (1 + \varepsilon) n$ for a constant $\varepsilon > 0$, MaxLoop is $\lceil 3 \log_{1+\varepsilon} r \rceil$, and $h_1, h_2$ are drawn from a family with enough independence (they use a construction of Siegel with $O(\log n)$-wise independence), then an insert takes $O(1)$ expected amortized time, and a rehash is needed with probability $O(1/n^2)$ for each insert.

*Proof sketch, not a full proof.* Draw the cuckoo graph: one vertex for each cell, and one edge $\{T_1[h_1(k)], T_2[h_2(k)]\}$ for each key. The keys fit exactly when each connected component has at most one cycle. The walk of an insert follows a path in the component of the new edge, and it visits each cell at most twice, so its length is at most a constant times the size of that component, unless the component has two cycles. When $r \ge (1 + \varepsilon) n$, this random graph is below the threshold where a large component appears. The expected size of a component is $O(1)$, and a path of length $\ell$ exists with probability that falls like $(1 + \varepsilon)^{-\ell}$. So a walk longer than $3 \log_{1+\varepsilon} r$ is rare, and the expected cost of the rehashes is $O(1)$ for each insert. The full proof, with the independence that it needs, is in the paper of Pagh and Rodler.

**Space.** The two tables have $2r \ge 2(1 + \varepsilon) n$ cells, so the space is $\Theta(n)$ and the [load factor](/load-factor/) $n / (2r)$ is less than $1/2$. A load near $1/2$ is the limit for two hash functions: the [load threshold of cuckoo hashing](/cuckoo-hashing-load-threshold/) is $1/2$.

| operation | cost |
|---|---|
| search | $O(1)$ worst case (2 cells) |
| delete | $O(1)$ worst case (2 cells) |
| insert | $O(1)$ expected amortized; $O(\log r)$ worst case without a rehash |
| rehash | $O(n)$ expected |
| space | $2r$ cells, $\Theta(n)$ |

## Variants

- **d-ary cuckoo hashing.** Fotakis, Pagh, Sanders and Spirakis give each key $d$ cells. With $d = O(\log(1/\varepsilon))$ hash functions, the table works at a load of $1 - \varepsilon$.
- **Buckets.** Each cell holds a few keys, for example 4. This also raises the load at which the table works, with fewer hash functions.
- **A stash.** Kirsch, Mitzenmacher and Wieder add a small constant-size stash for the keys that do not fit. A search also looks in the stash. This makes a rehash much less likely.
- **One table.** Both hash functions index the same array of $2r$ cells. The analysis is almost the same.
- **Simple tabulation.** Pătrașcu and Thorup show that cuckoo hashing works with [tabulation hashing](/tabulation-hashing/), with a failure probability of $O(n^{-1/3})$ for each set of $n$ keys.
- **Cuckoo filter.** A [cuckoo filter](/cuckoo-filter/) stores short fingerprints instead of keys, as a compact replacement for a [Bloom filter](/bloom-filter/).

## When to use it

Use cuckoo hashing when the worst case of a search matters more than the cost of an insert: a search reads two cells, which suits hardware tables, network routers and lookups that must meet a deadline. The two reads are independent, so they can run in parallel. Do not use the two-table form at a high load: above a total load of $1/2$ inserts fail. [Linear probing](/linear-probing/) and [Robin Hood hashing](/robin-hood-hashing/) work at higher loads and have better cache behaviour on inserts. For a fixed set of keys with worst-case $O(1)$ search, [perfect hashing](/perfect-hashing/) is an alternative.

## Pitfalls

- **No bound on the walk.** Without the bound of line L7, a cycle in the cuckoo graph makes the insert loop forever. The test with the keys 1, 122 and 243 catches it.
- **Losing the last pair.** When the walk fails, the pair $x$ that has no cell is not in the tables. If line L12 rehashes only the pairs of $T_1$ and $T_2$, this pair is lost. REHASH must also place $x$, as the set $X$ of line L15 does.
- **Insert without the test of line L4.** If a present key is inserted again, the walk can put a second copy in its other cell, which breaks (C2). A later delete then removes only one copy.
- **The same function twice.** If $h_1 = h_2$, two keys with the same first cell also share the second cell, and three such keys always fail. The two functions must be drawn independently.
- **A load that is too high.** Without line L5, the tables fill up and the rehashes become more and more frequent. Keep $r \ge (1 + \varepsilon) n$.
- **Weak hash functions.** The theorem needs hash functions with enough independence. With a simple function such as $k \bmod r$, as in the example, an adversary or a regular set of keys can force many rehashes.

## Implementations

The Python version takes a factory that makes a new pair of hash functions for a given $r$. The default factory draws $h_i(k) = ((a_i \cdot \text{hash}(k) + b_i) \bmod p) \bmod r$ with $p = 2^{61} - 1$ and random $a_i, b_i$. The tests pass the functions of the example.

## History

Rasmus Pagh and Flemming Friche Rodler presented cuckoo hashing at the European Symposium on Algorithms in 2001 and published the journal version in 2004. Their paper gives the eviction walk, the bound MaxLoop and the proof of the expected amortized $O(1)$ insert. The $d$-ary version of Fotakis, Pagh, Sanders and Spirakis appeared at STACS 2003, and the stash of Kirsch, Mitzenmacher and Wieder at ESA 2008.

## References
