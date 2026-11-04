---
tag: 3RBEYS
kind: data-structure
slug: bloom-filter
name: Bloom filter
area: data-structures/probabilistic-structures
level: intro
summary: Bit array with k hash functions giving a space-efficient approximate set with no deletions.
model: word-ram
complexity:
  vars: {n: the number of inserted keys, m: the number of bits, k: the number of hash functions}
  time: {worst: Θ(k)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [approximate-membership, false-positive-rate, hash-function, bit-vector]
see_also: [bloom-filter-optimal-hash-count, counting-bloom-filter, cuckoo-filter, xor-filter, scalable-bloom-filter, bloom-filter-lower-bound, log-structured-merge-tree, bloom-join]
sources:
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970
    locator: pages 422 to 426 (Method 2, the bit array with several hash codes, and its analysis)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the standard filter, the false positive rate, the optimal number of hash functions, union, intersection and halving)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.5 (Bloom filters and the analysis of the false positive probability)
  - paper: doi:10.1002/rsa.20208
    title: Adam Kirsch and Michael Mitzenmacher, Less hashing, same performance, building a better Bloom filter, Random Structures and Algorithms 33(2), 2008
    locator: pages 187 to 218 (two hash functions and the positions h1 + i h2)
  - paper: doi:10.1016/j.ipl.2008.05.018
    title: Prosenjit Bose and others, On the false-positive rate of Bloom filters, Information Processing Letters 108(4), 2008
    locator: pages 210 to 213 (the classical formula is a lower bound on the true rate)
  - paper: doi:10.1145/2674005.2674994
    title: Bin Fan, Dave G. Andersen, Michael Kaminsky and Michael Mitzenmacher, Cuckoo filter, practically better than Bloom, CoNEXT 2014
    locator: pages 75 to 88 (the comparison of space with Bloom filters)
---

A Bloom filter stores a set as an array of $m$ bits and answers membership queries with [false positives](/false-positive-rate/) but never false negatives. To insert a key it sets the bits at $k$ positions given by $k$ [hash functions](/hash-function/); a query answers "maybe present" if all $k$ bits are 1 and "absent" otherwise. After $n$ inserts the false positive rate is about $(1 - e^{-kn/m})^k$, and with the best $k$ it needs only $1.44 \log_2(1/\varepsilon)$ bits per key for a rate $\varepsilon$, whatever the size of the keys. Burton Bloom described it in 1970, and it is the standard solution of the [approximate membership problem](/approximate-membership/) when keys are only inserted.

## In plain words

Take a row of light switches, all off. To store a word, you feed it to a few different scramblers. Each scrambler names one switch, and you turn those switches on. To check a word later, you feed it to the same scramblers and look at the switches that they name.

If one of them is off, the word was never stored: storing it would have turned that switch on. If all of them are on, the word was probably stored. But other words may have turned on those switches by chance, so the answer can be wrong. This wrong "yes" gets more likely as more switches are on.

You cannot take a word out. Turning off its switches could also turn off a switch that another stored word needs.

## The abstract type

A Bloom filter is a filter for the incremental version of the [approximate membership problem](/approximate-membership/). It has two operations: INSERT$(x)$ adds $x$ to the set $S$, and QUERY$(x)$ returns *true* for each $x \in S$ and returns *true* for a key $x \notin S$ only with a small probability. It has no delete and no enumeration of the keys. Two filters with the same $m$ and the same hash functions can be merged into a filter of the union.

## Representation

The filter is a [bit vector](/bit-vector/) $B[0 \ldots m-1]$ and $k$ hash functions $h_1, \ldots, h_k$ from the universe $U$ to $\{0, \ldots, m-1\}$. The hash functions are fixed when the filter is created, and the same ones are used for each operation.

**Invariant (B).** For each inserted key $x$ and each $i \in \{1, \ldots, k\}$, $B[h_i(x)] = 1$.

The filter stores no key and no count. Its state is only the set of positions that are 1, which is the union of the sets $\{h_1(x), \ldots, h_k(x)\}$ over the inserted keys.

## Operations

```pseudo id=main
CREATE(m, k)
L1  B ← an array of m bits, all 0
L2  choose hash functions h_1, ..., h_k : U → {0, ..., m − 1}

INSERT(B, x)
L3  for i ← 1 to k do
L4      B[h_i(x)] ← 1

QUERY(B, x)
L5  for i ← 1 to k do
L6      if B[h_i(x)] = 0 then return false     ▷ x was never inserted
L7  return true                                ▷ x is in S, or a false positive
```

**Insert.** Lines L3 and L4 set the $k$ bits of $x$. A bit that is already 1 stays 1. Two of the positions of $x$ can be equal; then $x$ sets fewer than $k$ bits.

**Query.** Lines L5 and L6 check the $k$ bits of $x$ and stop at the first 0. A 0 proves that $x$ was never inserted. If all bits are 1, line L7 returns true.

**Union.** For two filters with the same $m$ and the same hash functions, the bitwise OR of the arrays is exactly the filter that inserting both sets would give.

**Intersection.** The bitwise AND of the arrays has a 1 at each position of each key in both sets, so it is a valid filter for the intersection. It can have more 1 bits than the filter of the intersection, so its false positive rate can be higher.

**Estimating the size.** If $X$ bits are 1, then $\hat n = -\frac{m}{k} \ln\!\left(1 - \frac{X}{m}\right)$ estimates the number of distinct inserted keys. It inverts the expected count $\mathbb{E}[X] \approx m(1 - e^{-kn/m})$.

## Example

Let $m = 16$ and $k = 3$, and suppose that the hash functions give these positions.

| key | $h_1$ | $h_2$ | $h_3$ |
|---|---|---|---|
| cat | 1 | 6 | 11 |
| dog | 4 | 6 | 13 |
| owl | 2 | 9 | 13 |
| fox | 3 | 9 | 11 |
| emu | 2 | 4 | 11 |

Insert cat, dog and owl.

| after | bits that are 1 | number of 1 bits |
|---|---|---|
| insert cat | 1, 6, 11 | 3 |
| insert dog | 1, 4, 6, 11, 13 | 5 |
| insert owl | 1, 2, 4, 6, 9, 11, 13 | 7 |

Bit 6 was already set by cat when dog came, and bit 13 by dog when owl came. So the three inserts set 7 bits, not 9.

- QUERY(cat) checks bits 1, 6 and 11. All are 1, so it returns true, which is right.
- QUERY(fox) checks bit 3 first. It is 0, so it returns false. Fox was never inserted.
- QUERY(emu) checks bits 2, 4 and 11. All are 1, set by owl, dog and cat. It returns true although emu was never inserted. This is a false positive.

With 7 of the 16 bits set, a key whose 3 positions are independent and uniform is a false positive with probability $(7/16)^3 \approx 0.084$. The formula $(1 - (1 - 1/16)^9)^3$, which uses the expected number of set bits, gives $0.086$.

## Correctness

Bits never change from 1 to 0, and INSERT$(x)$ sets each bit $B[h_i(x)]$. So invariant (B) holds after each operation, and QUERY returns true for each inserted key: a Bloom filter has no false negatives. A query returns false only when it sees a 0 bit at a position of $x$, which by (B) proves that $x$ was not inserted. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory probes |
|---|---|---|
| create | $\Theta(m)$ bit writes, or $O(1)$ with zeroed memory | none |
| insert | $k$ hash evaluations | $k$ |
| query, key in $S$ | $k$ hash evaluations | $k$ |
| query, key not in $S$ | at most $k$ | at most $1/(1 - X/m)$ in expectation |
| union, intersection | $\Theta(m / w)$ word operations | $\Theta(m/w)$ |
| space | $m$ bits | |

The model is the [word RAM](/word-ram/) with words of $w$ bits, and a hash evaluation counts as one step. The probes are random positions, so each one is usually a cache miss. A query for an absent key stops at the first 0 bit; with ideal hashing each probe finds a 0 with probability $1 - X/m$, where $X$ is the number of 1 bits, which gives the expected probe count of the table.

**False positive rate.** Assume ideal hashing: the values $h_i(y)$ for all keys $y$ and all $i$ are independent and uniform on $\{0, \ldots, m-1\}$. After $n$ inserts, a fixed bit is still 0 with probability $(1 - 1/m)^{kn}$. A key $x \notin S$ is a false positive when its $k$ positions all hold a 1, which has probability exactly $\mathbb{E}[(X/m)^k]$. By [Jensen's inequality](/jensens-inequality/) this is at least
$$ \varepsilon \ge \left(1 - \left(1 - \tfrac{1}{m}\right)^{kn}\right)^k \approx \left(1 - e^{-kn/m}\right)^k, $$
and the number $X$ of 1 bits is concentrated near its mean, so for large $m$ the rate is close to this value. The proof is in [the complexity proof](proofs/complexity.md).

**Best number of hash functions.** For fixed $m$ and $n$, the value $(1 - e^{-kn/m})^k$ is smallest at $k = (m/n) \ln 2$, where half of the bits are 1 and the rate is $2^{-k} \approx 0.6185^{m/n}$. This is the [optimal hash count theorem](/bloom-filter-optimal-hash-count/). For a target rate $\varepsilon$ the filter then needs
$$ \frac{m}{n} = \frac{\log_2(1/\varepsilon)}{\ln 2} \approx 1.44 \log_2(1/\varepsilon) $$
bits per key, which is $\log_2 e \approx 1.44$ times the [lower bound](/bloom-filter-lower-bound/) of $\log_2(1/\varepsilon)$.

| bits per key $m/n$ | best integer $k$ | rate $(1 - e^{-k n/m})^k$ |
|---|---|---|
| 4 | 3 | 0.147 |
| 8 | 6 | 0.0216 |
| 10 | 7 | 0.00819 |
| 16 | 11 | 0.000459 |
| 20 | 14 | 0.0000671 |

## Variants

- **Double hashing.** Compute two hash values $a$ and $b$ and use the positions $a + i b \bmod m$ for $i = 0, \ldots, k-1$. Kirsch and Mitzenmacher (2008) proved that the false positive rate tends to the same limit as with $k$ independent hash functions. The Python code uses this. It is the same idea as [double hashing](/double-hashing/) in open addressing.
- **Partitioned filter.** Split the array into $k$ parts of $m/k$ bits, and let $h_i$ choose a bit of part $i$. The $k$ positions of a key are then always distinct. The rate is slightly higher for the same $m$.
- **Blocked filter.** Let one hash choose a block of one cache line, and put all $k$ bits of the key in that block. A query then costs one cache miss. The rate is higher, because the blocks get uneven loads.
- **Counting Bloom filter.** Replace each bit by a small counter to allow deletes. See the [counting Bloom filter](/counting-bloom-filter/).
- **Growing sets.** The [scalable Bloom filter](/scalable-bloom-filter/) adds filters as the set grows. The [stable Bloom filter](/stable-bloom-filter/) forgets old keys of a stream.
- **Values and counts.** The [Bloomier filter](/bloomier-filter/) stores a value for each key, and the [spectral Bloom filter](/spectral-bloom-filter/) estimates multiplicities.
- **Smaller filters.** For the same rate, a [cuckoo filter](/cuckoo-filter/) or a [quotient filter](/quotient-filter/) uses less space when $\varepsilon$ is small and also allows deletes. Static sets fit in less space in an [xor filter](/xor-filter/) or a [ribbon filter](/ribbon-filter/).

## When to use it

Use a Bloom filter in front of a slow exact lookup when most queries are for absent keys and a few extra lookups are acceptable, for example one filter for each file of a [log-structured merge tree](/log-structured-merge-tree/), or a filter sent over the network in a [Bloom join](/bloom-join/). It is simple, it has a fixed size, it never fails on insert, and its union is a bitwise OR. Choose a cuckoo filter when you need deletes, or when the target rate is small: Fan et al. (2014) report that their space-optimized cuckoo filter uses less space than a Bloom filter for rates below about 3 percent. Choose an xor, binary fuse or ribbon filter when the set is static. Do not use a Bloom filter when the number of keys is unknown and can grow much beyond the planned capacity.

## Pitfalls

- **Clearing bits to delete.** Setting the bits of $x$ back to 0 in line L4 breaks invariant (B) for each other key that shares one of those bits, and gives false negatives. Use a [counting Bloom filter](/counting-bloom-filter/) instead.
- **Too many keys.** The rate of the table holds only for the planned $n$. With twice as many keys as planned at 10 bits per key and $k = 7$, the rate rises from 0.008 to about 0.14. Size $m$ for the largest $n$ you expect.
- **Correlated hash functions.** Positions such as $h(x) + i \bmod m$ for $i = 0, \ldots, k - 1$ put the bits of a key next to each other, so keys that collide on $h$ collide on all $k$ bits. Use independent hashes or double hashing with a nonzero step.
- **A zero step in double hashing.** If $b \equiv 0 \pmod m$, all $k$ positions are the same bit. The code makes $b$ odd, which helps only when $m$ is a power of two or odd; for a general $m$, take $b$ from $\{1, \ldots, m-1\}$.
- **A seeded hash that changes between runs.** Python's built-in `hash` of a string changes from one process to the next. A filter built in one run and loaded in the next then has false negatives. Use a hash with an explicit seed, as the code does.
- **Union of different filters.** The OR of two arrays is a filter of the union only if both have the same $m$, the same $k$ and the same hash functions.

## Implementations

The Python class follows the main block with BLAKE2b and double hashing, and adds `union` and a count of the 1 bits.

## History

Burton Bloom published the method in 1970 as "Method 2" of his paper on hash coding with allowable errors. His motivating example was a hyphenation program: a filter of the words that need the slow dictionary lets most words use simple rules. Broder and Mitzenmacher's survey (2004) made the structure widely known in networking, and Kirsch and Mitzenmacher (2008) showed that two hash functions suffice. Bose et al. (2008) showed that the classical formula for the rate is not exact.

## References
