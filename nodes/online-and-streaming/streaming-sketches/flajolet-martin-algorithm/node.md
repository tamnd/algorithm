---
tag: YQ5W45
kind: algorithm
slug: flajolet-martin-algorithm
name: Flajolet-Martin algorithm
aliases:
- probabilistic counting
- FM sketch
- FM algorithm
- AMS distinct elements estimator
area: online-and-streaming/streaming-sketches
level: core
summary: Estimates distinct elements from the maximum number of trailing zeros over hashed items.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {n: the universe size, d: the number of distinct items}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 1985
  people: [Philippe Flajolet, G. Nigel Martin, Noga Alon, Yossi Matias, Mario Szegedy]
  note: Flajolet and Martin published the bitmap counter in 1985, with an analysis for an ideal random hash. Alon, Matias and Szegedy proved a constant factor bound with pairwise independent hashing in 1996.
prereqs: [distinct-elements-problem, hash-function, geometric-distribution, chebyshev-inequality]
see_also: [flajolet-martin-sketch, pcsa, loglog-counting, hyperloglog, kmv-sketch, median-trick, k-wise-independent-hashing, morris-counter]
sources:
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pp. 182 to 209 (the bitmap, the constant 0.77351, the mean and the standard deviation of R)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147 (the F_0 estimate with a linear hash over a finite field and its factor c bound)
  - paper: doi:10.1145/237814.237823
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, STOC 1996
    locator: the conference version
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2 (count distinct)
---

The Flajolet-Martin algorithm estimates the number $d$ of distinct items in a stream with one bitmap of about $\log_2 n$ bits. It hashes each item, records in the bitmap the number of trailing zeros of the hash value, and at the end finds $R$, the position of the lowest bit that is still 0. A hash value with $r$ trailing zeros has probability $2^{-(r+1)}$, so $R$ is near $\log_2 d$, and the estimate is $2^R/\varphi$ with $\varphi \approx 0.77351$. Repeated items give the same hash and change nothing. Flajolet and Martin (1985) analysed it for an ideal random hash. Alon, Matias and Szegedy (1996) gave a version that keeps only the largest number of trailing zeros, and proved with pairwise independent hashing that it is within a factor 3 of $d$ with constant probability. This page proves that bound in full. The data structure view, with many bitmaps, is the [Flajolet-Martin sketch](/flajolet-martin-sketch/), and the averaged version is [PCSA](/pcsa/). On this page $n$ is the universe size, $d$ is the number of distinct items, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

Flip a coin until it comes up heads, and count the tails before it. A run of 5 tails happens about once in 64 tries. So if someone tells you the longest run they saw, you can guess how many times they tried. The algorithm uses the hash of each item as the coin flips: the trailing zeros of the hash value are the run of tails. Because the hash of an item is always the same, an item seen twice is one try, not two. The algorithm keeps a row of bits and marks each run length it has seen. Short runs are all marked soon, and the first gap in the marks is a good sign of how many different items came by. One row gives only a rough answer, often off by a factor of 2.

## The problem

The input is a stream $a_1, \ldots, a_m$ of items from a universe of size $n$. The output is an estimate of $d = F_0$, the number of distinct items. This is the [distinct elements problem](/distinct-elements-problem/). The algorithm has one pass and a state of $O(\log n)$ bits, plus the seed of the hash function.

## The algorithm

Let $h$ map items to $L$-bit integers, with $L \ge \log_2 n$, and let $\rho(y)$ be the number of trailing zeros of $y$, with $\rho(0) = L$.

```pseudo id=main
FM-COUNT(σ, h)
L1  B ← 0                                   ▷ a bitmap of L + 1 bits
L2  for each item x of σ do
L3      r ← ρ(h(x))                          ▷ trailing zeros of the hash value
L4      set bit r of B
L5  R ← the smallest r with bit r of B equal to 0
L6  return 2^R / φ                           ▷ φ ≈ 0.77351
```

Line L4 sets bit $r$ when some item has exactly $r$ trailing zeros. Bit 0 is set by half of the distinct items, bit 1 by a quarter, and so on. Line L5 finds the first gap.

**The AMS version.** Keep only $Z = \max_x \rho(h(x))$, the highest bit that line L4 sets, in place of the bitmap, and return $2^{Z + 1/2}$. Use a pairwise independent hash $h(x) = Ax + b$ over $\mathrm{GF}(2)$, with a random $L \times L$ bit matrix $A$ and a random vector $b$. Run $t$ copies with independent seeds and return the median.

## Example

Take the stream $a, b, c, a, d, e, b, f$ with $d = 6$ and these 8-bit hash values.

| item | $h(x)$ | $\rho$ |
|---|---|---|
| a | 01101100 | 2 |
| b | 10010001 | 0 |
| c | 00101010 | 1 |
| d | 10110000 | 4 |
| e | 01010011 | 0 |
| f | 10100110 | 1 |

The second $a$ and the second $b$ set bits that are already set. The bitmap is $B = 10111$ in binary: bits 0, 1, 2 and 4 are set, and bit 3 is not. So $R = 3$ and the estimate is $8/\varphi \approx 10.34$, against $d = 6$. The AMS version keeps $Z = 4$ and returns $2^{4.5} \approx 22.6$. Both are within the expected range of one copy, which is wide.

For $d = 6$ and an ideal random hash, bit $r$ is set with probability $1 - (1 - 2^{-(r+1)})^6$: 0.984 for bit 0, 0.822 for bit 1, 0.551 for bit 2, 0.321 for bit 3 and 0.174 for bit 4. The bits below $\log_2 d$ are almost surely set, and the bits well above are almost surely not.

## Correctness

The state after the stream depends only on the set of distinct items, not on their order or their repeats, because line L4 sets the same bit for each copy of an item. The OR of two bitmaps with the same $h$ is the bitmap of the union of the two streams. For a fully random hash, bit $r$ is 0 with probability $(1 - 2^{-(r+1)})^d$, so $\Pr[R > r] \le d/2^{r+1}$ and $\Pr[R \le r] \le \sum_{j \le r} e^{-d/2^{j+1}}$. Both tails fall fast away from $\log_2 d$, which shows that $2^R$ is within a constant factor of $d$ with constant probability.

For the AMS version with pairwise independent hashing, let $Y_r$ be the number of distinct items whose hash has at least $r$ trailing zeros. Then $Z \ge r$ exactly when $Y_r \ge 1$, $\mathbb{E}[Y_r] = d/2^r$ and $\mathrm{Var}(Y_r) \le d/2^r$. [Markov's inequality](/markov-inequality/) on $Y_r$ bounds the chance that the estimate is $3d$ or more by $\sqrt 2/3$, and [Chebyshev's inequality](/chebyshev-inequality/) bounds the chance that it is $d/3$ or less by $\sqrt 2/3$. The proofs are on the proof page.

## Complexity

The space and the time below are proved on the proof page, except the moments of $R$, which are cited.

- **Update time.** $O(1)$ word operations per item: one hash, one count of trailing zeros and one OR. The matrix hash of the AMS version costs $O(L)$ word operations, and a hash over the field $\mathrm{GF}(2^L)$ costs one field multiplication.
- **Query time.** $O(1)$: the lowest zero bit of $B$ is the lowest set bit of $\lnot B$.
- **Space.** The bitmap has $L + 1 = O(\log n)$ bits. The AMS state $Z$ has $O(\log\log n)$ bits. The seed of the matrix hash has $L^2 + L$ bits, and the seed of $h(x) = ax + b$ over $\mathrm{GF}(2^L)$ has $2L$ bits, so one AMS copy uses $O(\log n)$ bits with the field hash. The median of $t$ copies uses $O(t \log n)$ bits.
- **Accuracy of one bitmap (cited).** For a fully random hash, Flajolet and Martin show that $\mathbb{E}[R] = \log_2(\varphi d)$ up to a periodic term of amplitude below $10^{-5}$ and an $o(1)$ term, and that the standard deviation of $R$ is about 1.12. So one bitmap is often off by a factor of 2.
- **Accuracy of AMS (proved).** Each side fails with probability at most $\sqrt 2/3 \approx 0.471$. By the one-sided [median trick](/median-trick/), the median of $t$ copies is outside $[d/3, 3d]$ with probability at most $2(4q(1-q))^{t/2}$ for $q = \sqrt 2/3$, so $t \approx 611\ln(2/\delta)$ copies give probability $1 - \delta$. The constant is poor; the proof is the point.

## Properties

- **Duplicate-insensitive.** The state is a function of the set of distinct items.
- **Mergeable.** The OR of bitmaps, or the maximum of the values $Z$, is the sketch of the union, when both sketches use the same hash. See [mergeable summaries](/mergeable-summaries/).
- **Not linear, no deletions.** A set bit cannot be cleared when an item leaves, because other items may have set it. For deletions see the [turnstile model](/turnstile-model/).
- **Randomized through the hash only.** For a fixed hash the algorithm is deterministic. The guarantee is over the choice of $h$, for each fixed stream.
- **Biased.** $2^R/\varphi$ is not unbiased; $\varphi$ corrects the bias of $R$ on the log scale.

## Variants and improvements

- **Several hash functions.** Run $m$ bitmaps with independent hashes and use the mean of their $R$ values. The error falls like $1/\sqrt m$, but each item costs $m$ hashes.
- **[PCSA](/pcsa/).** One hash per item: its low bits choose one of $m$ bitmaps, and the rest goes into that bitmap. The standard error is about $0.78/\sqrt m$.
- **[LogLog](/loglog-counting/) and [HyperLogLog](/hyperloglog/).** Keep only the largest position per bucket, as in the AMS version, in $O(\log\log n)$ bits per bucket. HyperLogLog combines the buckets with a harmonic mean, for a standard error of about $1.04/\sqrt m$.
- **[KMV](/kmv-sketch/) and BJKST.** Keep the $k$ smallest hash values, for an $(\varepsilon, \delta)$ guarantee with limited independence.
- **[Linear counting](/linear-counting/).** A bitmap indexed by the full hash value, good for small counts.
- **Optimal space.** Kane, Nelson and Woodruff (2010) reach $O(1/\varepsilon^2 + \log n)$ bits, the lower bound.

## When to use it

Use one Flajolet-Martin bitmap to learn the order of magnitude of a count distinct, or to teach the idea of the hash sketches. For an accurate estimate use [PCSA](/pcsa/) or, in practice, [HyperLogLog](/hyperloglog/). Use the AMS version when you need a proof under a hash family with a short seed, not a model of an ideal hash.

## Pitfalls

- **Highest set bit in line L5.** Line L5 uses the lowest zero, not the highest set bit. The highest set bit is the AMS statistic $Z$, which has a different bias, and $2^Z/\varphi$ is wrong.
- **Forgetting $\varphi$ in line L6.** $2^R$ alone overestimates by a factor of about $1/0.77351 \approx 1.29$.
- **A short hash in line L3.** If $L$ is close to $\log_2 d$, the high bits of the bitmap fill up and $R$ stops growing. Use $L \ge \log_2 n + 4$, or a 64-bit hash.
- **A weak hash in line L3.** If $h$ keeps the structure of the keys, for example the identity on integers, then multiples of 8 all have 3 or more trailing zeros, and the estimate depends on the keys, not on their number.
- **The case $h(x) = 0$ in line L3.** It has $L$ trailing zeros by the convention $\rho(0) = L$; the bitmap needs $L + 1$ bits for it.
- **Merging with different hashes.** The OR of bitmaps built with different $h$ is not the sketch of anything.

## Implementations

## History

Philippe Flajolet and G. Nigel Martin presented probabilistic counting at FOCS in 1983 and published the full paper in the Journal of Computer and System Sciences in 1985. They wanted to estimate the number of distinct values in a database column in one pass, to plan queries. Their analysis, with Mellin transforms, assumed an ideal random hash and gave the constant $\varphi \approx 0.77351$. Alon, Matias and Szegedy, in their 1996 paper on frequency moments, observed that a linear hash and the largest number of trailing zeros already give a constant factor estimate, with a short proof. That paper started the theory of streaming algorithms, and the AMS version is the standard first proof for $F_0$.

## References
