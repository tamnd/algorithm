---
tag: 86TWSR
kind: algorithm
slug: flajolet-martin-sketch
name: Flajolet-Martin sketch
aliases:
- probabilistic counting
- FM sketch
area: data-structures/probabilistic-structures
level: core
summary: Estimates distinct count from the maximum number of trailing zeros among hashed values.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {n: the number of distinct items, m: the number of bitmaps, L: the bits per bitmap}
  time: {worst: Θ(1)}
  space: {extra: Θ(m L)}
properties: {deterministic: false, online: true, mergeable: true}
history:
  year: 1985
  people: [Philippe Flajolet, G. Nigel Martin]
  note: Flajolet and Martin published probabilistic counting with stochastic averaging in the Journal of Computer and System Sciences.
prereqs: [distinct-elements-problem, hash-function, streaming-model, geometric-distribution]
see_also: [flajolet-martin-algorithm, hyperloglog, kmv-sketch, cardinality-estimation, ams-sketch, bloom-filter, morris-counter]
sources:
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pages 182 to 209 (the bitmap, the constant 0.77351, the standard error 0.78 over the square root of m of PCSA)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pages 137 to 147 (the estimate of F0 within a constant factor with pairwise independent hashing)
  - paper: doi:10.1007/978-3-540-39658-1_55
    title: Marianne Durand and Philippe Flajolet, Loglog counting of large cardinalities, ESA 2003
    locator: pages 605 to 617 (keeping only the largest position, in log log n bits per register)
---

The Flajolet-Martin sketch estimates the number of distinct items in a stream in a few hundred bytes. It hashes each item to a random bit string and records in a bitmap the number of trailing zeros of the hash. A hash ends in $r$ zeros with probability $2^{-(r+1)}$, so if $n$ distinct items have been seen, the bits up to about $\log_2 n$ are set and the bits beyond are 0. The position $R$ of the lowest 0 bit therefore estimates $\log_2 n$. Repeats of an item give the same hash, so they change nothing. With $m$ bitmaps and *stochastic averaging*, the method of Flajolet and Martin (1985) called PCSA has a standard error of about $0.78/\sqrt{m}$. This page is about the bitmap structure; the general method, and its use as one of the first [streaming](/streaming-model/) algorithms, are on the page [Flajolet-Martin algorithm](/flajolet-martin-algorithm/).

## In plain words

Flip a coin until it shows heads, and write down how many tails came first. One run of four tails is rare: about one try in 32 gives it. So if somebody tells you that the longest run they saw was four tails, they probably made about 30 tries.

The sketch does the same with items. Each item is turned into a fixed random string of coin flips, and the sketch marks how many tails it starts with. The same item always gives the same string, so seeing it twice changes nothing. The first mark that is still missing tells about how many different items there were.

One such guess can be off by a factor of two. So the sketch splits the items into many groups, makes a guess in each group, and takes the average.

## The problem

The [distinct elements problem](/distinct-elements-problem/): read a stream $a_1, a_2, \ldots$ of items from a universe $U$, and at any time output an estimate of $n = |\{a_1, a_2, \ldots\}|$, the number of distinct items so far. An exact answer needs memory linear in $n$, so the sketch gives an estimate $\hat n$ with a small relative error, and two sketches of two streams must combine into a sketch of their union.

## The algorithm

Let $h$ be a [hash function](/hash-function/) from $U$ to integers of $w$ bits, and let $\rho(q)$ be the number of trailing zero bits of an integer $q > 0$. The sketch has $m$ bitmaps $B_0, \ldots, B_{m-1}$ of $L$ bits.

```pseudo id=main
CREATE(m, L)
L1  B_0, ..., B_{m−1} ← bitmaps of L bits, all 0
L2  choose a hash function h : U → {0, ..., 2^w − 1}

ADD(x)
L3  y ← h(x); j ← y mod m; q ← ⌊y / m⌋
L4  if q > 0 and ρ(q) < L then B_j[ρ(q)] ← 1

ESTIMATE()
L5  S ← 0
L6  for j ← 0 to m − 1 do S ← S + R_j    ▷ R_j: the index of the lowest 0 bit of B_j
L7  return (m / φ) · 2^{S/m}             ▷ φ = 0.77351
```

**Add.** Line L3 uses the low part of the hash to choose one bitmap $j$, and the rest of the hash for the bit. Line L4 sets bit $\rho(q)$ of that bitmap. So each item costs one hash and one bit write.

**Estimate.** In one bitmap that has seen $n_j$ items, bit $r$ is set with probability $1 - (1 - 2^{-(r+1)})^{n_j}$: close to 1 for $2^r \ll n_j$ and close to 0 for $2^r \gg n_j$. So the lowest 0 bit $R_j$ is near $\log_2 n_j$. Flajolet and Martin showed that $\mathbb{E}[R] \approx \log_2(\varphi n)$ for one bitmap, with $\varphi = 0.77351$. Each bitmap sees about $n/m$ items, so lines L5 to L7 average the $R_j$ and return $(m/\varphi) \cdot 2^{\bar R}$.

**Merge.** The bitwise OR of two sketches with the same $m$, $L$ and $h$ is the sketch of the union of the two sets.

## Example

Take $m = 2$ bitmaps of $L = 8$ bits and these hash values.

| item | $y = h(x)$ | $j = y \bmod 2$ | $q = \lfloor y/2 \rfloor$ | $\rho(q)$ |
|---|---|---|---|---|
| a | 12 | 0 | 6 = 110 | 1 |
| b | 7 | 1 | 3 = 11 | 0 |
| c | 4 | 0 | 2 = 10 | 1 |
| d | 16 | 0 | 8 = 1000 | 3 |
| e | 9 | 1 | 4 = 100 | 2 |
| f | 2 | 0 | 1 = 1 | 0 |
| g | 11 | 1 | 5 = 101 | 0 |

Read the stream a b c a d e f g b, which has 9 items and 7 distinct ones.

- $B_0$ gets bit 1 (from a and c), bit 3 (from d) and bit 0 (from f). It is $\{0, 1, 3\}$, so $R_0 = 2$.
- $B_1$ gets bit 0 (from b and g) and bit 2 (from e). It is $\{0, 2\}$, so $R_1 = 1$.

The second a and the second b set bits that are already set. ESTIMATE computes $S = 3$ and returns $(2/0.77351) \cdot 2^{1.5} \approx 7.31$. The true count is 7. With so few bitmaps, an error of 50 percent would also be normal.

## Correctness

The sketch is a function of the set of distinct items: $B_j[r] = 1$ exactly when some item $x$ that has been seen has $h(x) \bmod m = j$ and $\rho(\lfloor h(x)/m \rfloor) = r$. Each ADD$(x)$ sets one bit that depends only on $x$, and bits are never cleared, so repeats and the order of the stream do not change the state, and the OR of two sketches is the sketch of the union. With ideal hashing, the single bitmap estimate $2^R$ is within a constant factor of $n$ with constant probability: $\Pr[2^R \ge c n] \le 1/c$ and $\Pr[2^R < n/c] \le e^{-c}/(1 - e^{-c})$ when $c$ and $n/c$ are powers of two. The proofs are in [the correctness proof](proofs/correctness.md) and [the complexity proof](proofs/complexity.md). The constant $\varphi$ and the error $0.78/\sqrt{m}$ come from the exact analysis of Flajolet and Martin, which this page does not repeat.

## Complexity

| step | time | memory |
|---|---|---|
| add | one hash and $O(1)$ word operations | |
| estimate | $O(m L)$, or $O(m)$ with a lowest-zero instruction | |
| merge | $O(m L / w)$ | |
| space | | $m L$ bits |

The bitmaps need $L \ge \log_2(n/m) + 4$ bits or so, because higher bits are almost never set; $L = 32$ covers counts beyond $10^{10}$ for $m \le 64$. So the space is $O(m \log n)$ bits. The standard error of PCSA is about $0.78/\sqrt{m}$: $m = 64$ bitmaps of 32 bits, 256 bytes in all, give about 10 percent.

## Properties

- **Duplicate insensitive.** Repeats of an item never change the state.
- **Order insensitive and mergeable.** The state is a function of the set, and the OR of two sketches is the sketch of the union, so the sketches of parts of a distributed data set can be combined.
- **Insert only.** An item cannot be removed: a bit may be set by several items. For streams with deletions, use a [linear sketch](/linear-sketch/).
- **Randomized.** The randomness is in $h$. For a fixed $h$ there are inputs on which it fails, so the error bounds hold for a random $h$ and a fixed input.

## Variants and improvements

- **LogLog and HyperLogLog.** Keep only the largest $\rho$ seen in each group, which needs $\log_2 \log_2 n$ bits per register instead of $\log_2 n$. LogLog (Durand and Flajolet 2003) averages these maxima, and [HyperLogLog](/hyperloglog/) uses a harmonic mean, with a standard error of $1.04/\sqrt{m}$ in much less space than PCSA.
- **Pairwise independent hashing.** Alon, Matias and Szegedy (1999) showed that the largest $\rho$ with a pairwise independent hash gives an estimate within a constant factor with constant probability, without the assumption of ideal hashing.
- **Order statistics.** The [KMV sketch](/kmv-sketch/) keeps the $k$ smallest hash values and estimates $n$ from the $k$-th smallest, which also allows set operations.
- **Small counts.** For $n$ below about $10m$ many bitmaps are empty and PCSA overestimates. Practical versions count the empty groups and use linear counting $m \ln(m/V)$ there, where $V$ is the number of empty bitmaps.

## When to use it

Use the Flajolet-Martin sketch to count distinct values in a stream or a large table when an error of a few percent is acceptable, when the count must be kept in a fixed small memory, or when counts of parts must be combined, as in the query optimizer of a database. For new systems, [HyperLogLog](/hyperloglog/) or [HyperLogLog++](/hyperloglog-plus-plus/) gives the same accuracy in about a third of the space, with registers of 6 bits in place of bitmaps of 32 bits. Use an exact [hash table](/hash-table/) when the count is small.

## Pitfalls

- **Taking the highest set bit.** The highest set bit of $B_j$ is very sensitive to one unlucky item with many trailing zeros. PCSA uses the lowest 0 bit, which is much more stable.
- **Forgetting $\varphi$.** The raw value $2^{\bar R}$ is biased: without the factor $1/\varphi \approx 1.29$, the estimate is about 23 percent too small.
- **Small counts.** With $n < 10m$ or so, many bitmaps hold only a few items, and the estimate is too large. Correct for small counts or use fewer bitmaps.
- **Weak hash functions.** A hash with poor low bits, such as the identity on integers, makes the bit pattern depend on the data. Use a well-mixed hash with a fixed seed.
- **Different hash functions.** Two sketches can be merged only if they use the same hash function and the same $m$ and $L$.

## Implementations

The Python function `estimate` follows the main block. It stores each bitmap as one integer, hashes with BLAKE2b, and adds `merge` and `rank`.

## History

Flajolet and Martin presented probabilistic counting at FOCS 1983 and published the full analysis in 1985, motivated by estimating the number of distinct values of an attribute in a database. Their work is one of the first [streaming](/streaming-model/) algorithms. Alon, Matias and Szegedy (1999) gave a version with a limited independence hash function. Durand and Flajolet (2003) reduced the space with LogLog, and Flajolet, Fusy, Gandouet and Meunier (2007) with [HyperLogLog](/hyperloglog/).

## References
