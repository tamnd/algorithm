---
tag: 1T1SSZ
kind: algorithm
slug: pcsa
name: Probabilistic counting with stochastic averaging
aliases:
- PCSA
- stochastic averaging counting
- Flajolet-Martin with stochastic averaging
area: online-and-streaming/streaming-sketches
level: core
summary: Splits the stream into buckets and averages Flajolet-Martin bitmaps to reduce variance.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {m: the number of bitmaps, n: the universe size}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(m log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 1985
  people: [Philippe Flajolet, G. Nigel Martin]
  note: Flajolet and Martin introduced stochastic averaging in the same 1985 paper as the bitmap counter, to get the accuracy of m hash functions at the cost of one.
prereqs: [flajolet-martin-algorithm, distinct-elements-problem, hash-function]
see_also: [flajolet-martin-sketch, loglog-counting, hyperloglog, linear-counting, kmv-sketch, mergeable-summaries, epsilon-delta-guarantee, poisson-distribution]
sources:
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pp. 182 to 209 (stochastic averaging, the standard error 0.78/√m and the bias 1 + 0.31/m)
  - paper: doi:10.1007/978-3-540-39658-1_55
    title: Marianne Durand and Philippe Flajolet, Loglog counting of large cardinalities, ESA 2003
    locator: pp. 605 to 617 (the comparison with PCSA)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2 (count distinct)
---

Probabilistic counting with stochastic averaging, or PCSA, estimates the number $d$ of distinct items with $m$ [Flajolet-Martin](/flajolet-martin-algorithm/) bitmaps and one hash per item. The hash value of an item chooses one bitmap with its low part, and its high part sets a bit in that bitmap as in the Flajolet-Martin counter. Each bitmap then sees about $d/m$ distinct items. With $S$ the sum of the positions $R_j$ of the lowest zero bit of each bitmap, the estimate is $(m/\varphi)\,2^{S/m}$, with $\varphi \approx 0.77351$. Flajolet and Martin (1985) showed, for an ideal random hash, a relative standard error of about $0.78/\sqrt m$ and a bias factor of about $1 + 0.31/m$. With 64 bitmaps of 32 bits, that is about 10% error in 256 bytes. On this page $m$ is the number of bitmaps, $d$ is the number of distinct items, $n$ is the universe size, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

One Flajolet-Martin bitmap gives a rough count, often off by a factor of 2. To do better you could keep many bitmaps, each with its own hash function, and average them, but then each item costs many hashes. PCSA uses one hash per item and splits the items into $m$ groups at random, with part of the hash value. Each group keeps its own bitmap, and so each bitmap counts about one $m$-th of the distinct items. The average of the bitmap readings gives the count of one group, and $m$ times that gives the whole count. The average of many readings varies much less than one reading, so the error falls like one over the square root of $m$.

## The problem

The input is a stream of items from a universe of size $n$, with repeats. The output is an estimate of $d = F_0$, the number of distinct items, with a relative error that the user can choose through $m$. This is the [distinct elements problem](/distinct-elements-problem/).

## The algorithm

Let $h$ map items to integers $y$ with $L$ bits. Write $y = j + m w$ with $0 \le j < m$, so $j$ is the bucket and $w$ the rest. Let $\rho(w)$ be the number of trailing zeros of $w$.

```pseudo id=main
PCSA(σ, h, m)
L1  B[0..m−1] ← 0                           ▷ m bitmaps
L2  for each item x of σ do
L3      y ← h(x)
L4      j ← y mod m;  w ← ⌊y / m⌋            ▷ bucket and rest
L5      set bit ρ(w) of B[j]
L6  S ← Σ_j (the smallest r with bit r of B[j] equal to 0)
L7  return (m / φ) · 2^(S/m)                 ▷ φ ≈ 0.77351
```

Line L4 uses the low part of $y$ for the bucket and the high part for the bitmap, so the two are independent for a random hash. Line L7 is the Flajolet-Martin estimate $2^{\bar R}/\varphi$ of one bucket, with $\bar R = S/m$ the average position, times $m$.

## Example

Let $m = 4$, with 8-bit hash values, and the stream $a, b, c, a, d, e, b, f$ with $d = 6$.

| item | $y$ | $j = y \bmod 4$ | $w = \lfloor y/4 \rfloor$ | $\rho(w)$ |
|---|---|---|---|---|
| a | 0100 | 0 | 1 | 0 |
| b | 1001 | 1 | 2 | 1 |
| c | 1010 | 2 | 2 | 1 |
| d | 0111 | 3 | 1 | 0 |
| e | 1100 | 0 | 3 | 0 |
| f | 1011 | 3 | 2 | 1 |

The repeats of $a$ and $b$ change nothing. The bitmaps are $B = [1, 10, 10, 11]$ in binary, and their lowest zero bits are at positions $1, 0, 0, 2$. So $S = 3$ and the estimate is $(4/\varphi)\,2^{3/4} \approx 8.70$. With $d = 6$ and $m = 4$, the buckets hold only 1 or 2 items each, and this is the range where PCSA is biased upward; the guarantee is for $d$ much larger than $m$.

## Correctness

As in the Flajolet-Martin counter, each bitmap depends only on the set of distinct items that fall in its bucket, so repeats and order do not matter, and the OR of two sketches with the same $h$ is the sketch of the union. For a fully random hash, the bucket and the rest of each item are independent, and given the sizes $d_0, \ldots, d_{m-1}$ of the buckets, the bitmaps are independent Flajolet-Martin bitmaps of $d_j$ items. If the number of items is Poisson, the buckets are exactly independent with Poisson sizes, and the variance of $S/m$ is the variance of one position divided by $m$. This explains the $1/\sqrt m$ law; the proof page proves these facts.

The exact constants are cited. For a fully random hash, Flajolet and Martin show that the estimate has relative standard error about $0.78/\sqrt m$ and mean about $d(1 + 0.31/m)$ for large $d/m$. The constant 0.78 is $\ln 2$ times the standard deviation, about 1.12, of the position $R$ of one bitmap.

## Complexity

- **Update time.** $O(1)$ word operations: one hash, a division by $m$ (a shift if $m$ is a power of 2), a count of trailing zeros and an OR.
- **Query time.** $O(m)$: one lowest zero bit per bitmap, and one power of 2.
- **Space.** $m$ bitmaps of about $L - \log_2 m$ bits each, with $L \ge \log_2 n + 4$, so $O(m \log n)$ bits, plus the seed of $h$. A common choice is 32 bits per bitmap.
- **Accuracy (cited).** Relative standard error about $0.78/\sqrt m$ and bias factor about $1 + 0.31/m$, for a fully random hash and large $d/m$. For a target error $\varepsilon$, $m \approx (0.78/\varepsilon)^2$: $m = 64$ gives about 9.8%, and $m = 1024$ about 2.4%.
- **From a standard error to a guarantee.** The standard error is not an $(\varepsilon, \delta)$ bound by itself. See the [(ε, δ) guarantee](/epsilon-delta-guarantee/) page for the step through Chebyshev's inequality.

## Properties

- **Duplicate-insensitive and order-insensitive.** The state is a function of the set of distinct items.
- **Mergeable.** The OR of the bitmaps, bucket by bucket, is the sketch of the union. See [mergeable summaries](/mergeable-summaries/).
- **One hash per item.** This is the gain over $m$ independent hash functions with the same accuracy.
- **Biased for small counts.** With no items, all positions are 0 and the estimate is $m/\varphi$, not 0. The guarantee needs $d$ well above $m$.
- **No deletions.** A bit set by one item may also have been set by another.

## Variants and improvements

- **Several hash functions.** The original form: $m$ independent bitmaps, each fed every item, and the mean of the positions. Same accuracy, $m$ times the update cost.
- **Small range correction.** Count the empty bitmaps $V$ and use [linear counting](/linear-counting/), $m\ln(m/V)$, when $d$ is small compared with $m$. HyperLogLog uses the same correction.
- **[LogLog](/loglog-counting/).** Keep only the largest position in each bucket, in $O(\log\log n)$ bits, with error $1.30/\sqrt m$. Per bit of memory it is better than PCSA, which spends $O(\log n)$ bits per bucket.
- **[HyperLogLog](/hyperloglog/).** LogLog registers with a harmonic mean, error $1.04/\sqrt m$.
- **Compressed PCSA.** The bitmaps have low entropy: the low bits are almost all 1 and the high bits almost all 0. An entropy coder stores them in much less than 32 bits each, and later work showed that compressed PCSA can beat HyperLogLog per bit of memory.
- **[KMV](/kmv-sketch/).** A different statistic, with an unbiased estimate and proofs under limited independence.

## When to use it

Use PCSA when you want a count distinct with a known error, mergeable sketches, and simple code, and memory is not the main limit. Its bitmaps are easy to OR in a database or over a network. When memory per sketch matters, [HyperLogLog](/hyperloglog/) gives a smaller error for the same number of bits. When $d$ may be small compared with $m$, add the linear counting correction.

## Pitfalls

- **Overlapping bits in line L4.** The bucket and the rest must come from disjoint parts of the hash value. If $w$ includes the bits of $j$, the positions in a bucket are not uniform.
- **Mean of estimates in line L7.** Line L7 averages the positions and then takes one power of 2. The mean of the $m$ values $2^{R_j}/\varphi$ has a different, larger bias.
- **Small counts in line L7.** For $d$ near or below $m$, many bitmaps are empty and the estimate is too large, $m/\varphi$ for an empty stream. Use the small range correction.
- **Too few bits per bitmap in line L5.** The rest $w$ has $L - \log_2 m$ bits. If that is close to $\log_2(d/m)$, the high bits fill and the estimate stops growing.
- **Merging sketches with different $h$ or $m$.** The OR is only valid for the same hash and the same split.

## Implementations

## History

Flajolet and Martin introduced stochastic averaging in their 1985 paper, as the practical form of probabilistic counting. They wrote it for estimating the number of distinct values in a database relation in one pass, and they analysed it with Mellin transforms, for an ideal hash. Durand and Flajolet (2003) replaced the bitmaps by single registers in LogLog counting, and Flajolet, Fusy, Gandouet and Meunier (2007) gave HyperLogLog. The stochastic averaging step, one hash that picks a bucket, is used by all of them.

## References
