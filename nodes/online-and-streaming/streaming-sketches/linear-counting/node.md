---
tag: 738TN4
kind: algorithm
slug: linear-counting
name: Linear counting
aliases:
- bitmap counting
- linear probabilistic counting
- linear counting algorithm
area: online-and-streaming/streaming-sketches
level: core
summary: Estimates distinct elements from the fraction of empty bits in a hashed bitmap.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {m: the number of bits of the bitmap}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(m)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 1990
  people: [Kyu-Young Whang, Brad T. Vander-Zanden, Howard M. Taylor]
  note: Whang, Vander-Zanden and Taylor published linear counting in ACM Transactions on Database Systems in 1990, with its bias, its variance and a rule for the size of the bitmap.
prereqs: [distinct-elements-problem, hash-function, balls-into-bins]
see_also: [hyperloglog, hyperloglog-plus-plus, pcsa, kmv-sketch, bloom-filter, coupon-collector-problem, mergeable-summaries, distinct-elements-problem]
sources:
  - paper: doi:10.1145/78922.78925
    title: Kyu-Young Whang, Brad T. Vander-Zanden and Howard M. Taylor, A linear-time probabilistic counting algorithm for database applications, ACM Transactions on Database Systems 15(2), 1990
    locator: pp. 208 to 229 (the estimator, its bias and standard error, and the map size table)
  - paper: doi:10.46298/dmtcs.3545
    title: Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog, the analysis of a near-optimal cardinality estimation algorithm, AofA 2007
    locator: Figure 3 (linear counting as the small range correction)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2 (count distinct)
---

Linear counting estimates the number $d$ of distinct items with a bitmap of $m$ bits. Each item is hashed to a position in the bitmap, and that bit is set. At the end, with $U$ the number of bits that are still 0, the estimate is
$$\hat d = -m \ln\frac{U}{m} = m \ln\frac{m}{U}.$$
The reason is that each bit stays 0 with probability $(1 - 1/m)^d \approx e^{-d/m}$, so $U \approx m e^{-d/m}$, and the estimate solves this for $d$. Whang, Vander-Zanden and Taylor (1990) showed that the bias is about $(e^t - t - 1)/2$ and the relative standard error about $\sqrt{m(e^t - t - 1)}/d$, with load factor $t = d/m$. The space is linear in $d$, hence the name, but with a small constant: the load factor can be 5 or more. It is very accurate for small counts, and [HyperLogLog](/hyperloglog/) and [HyperLogLog++](/hyperloglog-plus-plus/) use it for their small range. On this page $m$ is the size of the bitmap, $d$ is the number of distinct items, $t = d/m$, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

Throw balls at random into a row of boxes. If you throw few balls, most boxes stay empty. If you throw many, few stay empty. So the number of empty boxes tells you how many balls you threw. Linear counting does this with items and bits. Each distinct item is a ball, and its hash value says which box it lands in. The same item always lands in the same box, so repeats change nothing. Two balls in the same box look like one, but the formula already takes that into account. The method fails only when every box is full, so the row of boxes must not be too short for the count you expect.

## The problem

The input is a stream of items, with repeats. The output is an estimate of the number $d$ of distinct items. This is the [distinct elements problem](/distinct-elements-problem/). Linear counting is for the case where a bitmap of size proportional to $d$, with a small constant, is affordable, for example a column of a database table with up to a few million distinct values.

## The algorithm

Let $h$ map items to positions $0, \ldots, m - 1$.

```pseudo id=main
LINEAR-COUNT(σ, h, m)
L1  B[0..m−1] ← 0                            ▷ a bitmap of m bits
L2  for each item x of σ do
L3      j ← h(x)
L4      B[j] ← 1
L5  U ← the number of j with B[j] = 0
L6  return m ln(m / U)                       ▷ infinite if U = 0
```

Line L6 is undefined when $U = 0$, the case where the bitmap is full. The size $m$ must make this unlikely; see the Pitfalls.

## Example

Let $m = 8$ and the stream $a, b, c, a, d, e, b, f$ with $d = 6$, and let the hash values be $a \mapsto 3$, $b \mapsto 0$, $c \mapsto 6$, $d \mapsto 3$, $e \mapsto 1$, $f \mapsto 0$.

| bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| set by | b, f | e | | a, d | | | c | |
| value | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |

Two pairs collide, so only 4 bits are set and $U = 4$. The estimate is $8\ln(8/4) = 8\ln 2 \approx 5.55$, against $d = 6$. The formula counts on collisions: 4 set bits give an estimate above 4.

A second example shows the size of the bitmap. For $d = 10^6$ and a relative standard error of 1%, the formula $\sqrt{m(e^t - t - 1)}/d = 0.01$ gives $m \approx 154{,}000$ bits, about 19 kB, at load factor $t \approx 6.5$. Then $\mathbb{E}[U] \approx m e^{-t} \approx 235$, so a full bitmap is very unlikely. [HyperLogLog](/hyperloglog/) reaches 1% with about 10,800 registers of 5 bits, about 6.8 kB, and its size does not grow with $d$.

## Correctness

The proof page proves the exact mean and variance of $U$ for an ideal hash:
$$\mathbb{E}[U] = m\Big(1 - \frac1m\Big)^d, \qquad \mathrm{Var}(U) = m(m-1)\Big(1 - \frac2m\Big)^d + m\Big(1 - \frac1m\Big)^d - m^2\Big(1 - \frac1m\Big)^{2d}.$$
For large $m$ and fixed $t = d/m$, $\mathbb{E}[U] \approx m e^{-t}$ and $\mathrm{Var}(U) \approx m e^{-t}(1 - (1+t)e^{-t})$. The estimate of line L6 is the inverse of the map $d \mapsto m e^{-d/m}$ applied to $U$. A second order expansion of $\ln$ around $\mathbb{E}[U]$, given as a sketch on the proof page, gives the bias and the variance:

- **Bias.** With the approximation $\mathbb{E}[U] \approx m e^{-t}$, as in the paper, $\mathbb{E}[\hat d] - d \approx (e^t - t - 1)/2$. With the exact $\mathbb{E}[U]$, the first order term adds $t/2$, so the bias is about $(e^t - 1)/2$: 0.86 for $m = d = 200$, where the exact value is 0.865. Either way it is a small number of items, not a fraction of $d$.
- **Standard error.** $\mathrm{sd}(\hat d)/d \approx \sqrt{m(e^t - t - 1)}/d = \sqrt{(e^t - t - 1)/m}\,/\,t$.

Strictly, $\hat d$ is infinite with positive probability once $d \ge m$, so its mean is infinite. The bias and the variance above are those of the estimate on the event $U > 0$, which has probability near 1 when $m e^{-t}$ is large.

## Complexity

- **Update time.** $O(1)$: one hash and one bit set.
- **Query time.** $O(m/w)$ word operations with a population count over words of $w$ bits, or $O(1)$ if the number of set bits is kept as bits change.
- **Space.** $m$ bits plus the seed of $h$. For a fixed relative error the needed $m$ grows linearly in $d$, but the load factor $t$ can be large: the error depends on $m$ through $\sqrt{(e^t - t - 1)/m}/t$.
- **Accuracy.** About $\sqrt{(e^t - t - 1)/m}/t$ relative standard error. For $t \to 0$ this tends to $1/\sqrt{2m}$, so the estimate is almost exact for $d \ll m$.

## Properties

- **Duplicate-insensitive and order-insensitive.** The bitmap depends only on the set of distinct items.
- **Mergeable.** The OR of two bitmaps with the same $h$ and $m$ is the bitmap of the union. See [mergeable summaries](/mergeable-summaries/).
- **Very accurate for small counts.** This is why HyperLogLog uses it in its small range.
- **Fails when full.** $U = 0$ gives no estimate. The size must be chosen from an upper bound on $d$.
- **Not scale free.** Unlike HyperLogLog, the memory for a fixed error grows with $d$.
- **No deletions.** A bit set by one item may also be set by another. A [counting Bloom filter](/counting-bloom-filter/) style array of counters would allow deletions at a higher cost.

## Variants and improvements

- **The exact inverse.** Use $\hat d' = \ln(U/m)/\ln(1 - 1/m)$, the inverse of the exact mean $m(1 - 1/m)^d$. This removes the $t/2$ term of the bias.
- **Small range of register sketches.** In HyperLogLog, the $m$ registers play the role of the bits, and a register equal to 0 counts as an empty bit. HyperLogLog++ also uses it at the fine precision $2^{25}$ of its sparse form.
- **Multi-resolution bitmaps.** Sample the items at rates $1, 1/2, 1/4, \ldots$ into separate small bitmaps, and use the one whose load is in a good range. This removes the need to know an upper bound on $d$.
- **[Bloom filters](/bloom-filter/).** A Bloom filter with $k$ hash functions gives the same kind of estimate of the number of inserted items from its fraction of zero bits, $-(m/k)\ln(U/m)$.
- **[PCSA](/pcsa/) and [HyperLogLog](/hyperloglog/).** Sketches whose size grows only like $\log d$ or $\log\log d$ per bucket, for large counts.

## When to use it

Use linear counting when you know an upper bound on $d$, the bound is not too large, and you want a very accurate estimate with simple code, for example the number of distinct values of a column in a database with up to a few million rows. Use it also as the small range part of a register sketch. When $d$ may be very large or is unknown, use [HyperLogLog](/hyperloglog/), whose memory does not grow with $d$.

## Pitfalls

- **A full bitmap at line L6.** If $U = 0$ the logarithm is infinite. Choose $m$ so that $m e^{-t}$ is at least about 10 at the largest $d$ you expect; then $\Pr[U = 0] \approx e^{-m e^{-t}}$ is below $5 \cdot 10^{-5}$.
- **A hash range that is not $0, \ldots, m-1$ in line L3.** Reducing a hash value with $\bmod m$ is uniform only if $m$ divides the range, or nearly so. A power of 2 for $m$ avoids the issue.
- **The bias for large loads.** At $t = 6$ the bias is about 200 items. That is small against $d = 6m$, but it is not 0.
- **Merging bitmaps of different sizes or hashes.** The OR is only valid for the same $h$ and $m$.
- **Counting $m - U$ as the answer.** The number of set bits underestimates $d$, because of collisions; line L6 corrects for them.

## Implementations

## History

Kyu-Young Whang, Brad T. Vander-Zanden and Howard M. Taylor published linear counting in 1990, for database query optimization, where the number of distinct values of a column guides the choice of a join method. They derived the mean and the variance of the number of empty bits, the bias and the standard error of the estimate, and a table of bitmap sizes for given counts and errors. The estimator is the same as the classical estimate of a population size from the number of empty cells in an occupancy problem.

## References
