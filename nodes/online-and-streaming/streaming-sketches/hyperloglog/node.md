---
tag: ZE356T
kind: algorithm
slug: hyperloglog
name: HyperLogLog
aliases:
- HLL
- HyperLogLog counter
- HyperLogLog sketch
area: online-and-streaming/streaming-sketches
level: core
summary: Harmonic-mean estimator over LogLog registers giving about 1.04/sqrt(m) relative error.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {m: the number of registers, n: the universe size}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(m log log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 2007
  people: [Philippe Flajolet, Éric Fusy, Olivier Gandouet, Frédéric Meunier]
  note: Flajolet, Fusy, Gandouet and Meunier presented HyperLogLog at the 2007 Conference on Analysis of Algorithms, with an analysis for an ideal hash and empirical range corrections.
prereqs: [loglog-counting, distinct-elements-problem, hash-function]
see_also: [hyperloglog-plus-plus, loglog-counting, pcsa, linear-counting, kmv-sketch, flajolet-martin-algorithm, mergeable-summaries, cardinality-estimation]
sources:
  - paper: doi:10.46298/dmtcs.3545
    title: Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog, the analysis of a near-optimal cardinality estimation algorithm, AofA 2007, DMTCS Proceedings
    locator: Theorem 1; Figure 3; Section 4
  - paper: doi:10.1007/978-3-540-39658-1_55
    title: Marianne Durand and Philippe Flajolet, Loglog counting of large cardinalities, ESA 2003
    locator: pp. 605 to 617
  - paper: doi:10.1145/2452376.2452456
    title: Stefan Heule, Marc Nunkesser and Alexander Hall, HyperLogLog in practice, algorithmic engineering of a state of the art cardinality estimation algorithm, EDBT 2013
    locator: pp. 683 to 692 (the measured bias of the raw estimate for small counts)
  - paper: doi:10.1145/78922.78925
    title: Kyu-Young Whang, Brad T. Vander-Zanden and Howard M. Taylor, A linear-time probabilistic counting algorithm for database applications, ACM Transactions on Database Systems 15(2), 1990
    locator: pp. 208 to 229 (the linear counting estimate used for small counts)
---

HyperLogLog estimates the number $d$ of distinct items in a stream with $m$ registers of 5 bits each. It has the same state and the same update as [LogLog](/loglog-counting/): the first bits of the hash of an item choose a register, and the register keeps the largest position $\rho$ of the leftmost 1 bit in the rest of the hash. The difference is the query. HyperLogLog combines the registers with a harmonic mean, $E = \alpha_m m^2 / \sum_j 2^{-M[j]}$, which is much less sensitive to the few registers that are too large. Flajolet, Fusy, Gandouet and Meunier (2007) proved, for an ideal random hash, that the relative standard error is $\beta_m/\sqrt m$ with $\beta_\infty = \sqrt{3\ln 2 - 1} \approx 1.03896$, so about $1.04/\sqrt m$. With $m = 2048$ the error is about 2.3% in 1280 bytes. For small and very large counts, the paper adds corrections that it chose from simulations. On this page $m = 2^b$ is the number of registers, $d$ is the number of distinct items, $n$ is the universe size, the hash has 32 bits, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

Hash each item into a string of random looking bits. Among many different items, the longest run of leading zeros tells you roughly how many there were: a run of 20 zeros takes about a million tries. HyperLogLog splits the items into many groups with the first few bits of the hash, and remembers only the longest run in each group. Each group gives a rough guess for its share of the items. A plain average of these guesses would be pulled up by a few unlucky groups with very long runs. So HyperLogLog uses a harmonic mean, an average of the inverses, which damps those large values. The result is accurate to a few percent with a few kilobytes, and the sketches of two streams combine by taking the larger value in each group.

## The problem

The input is a stream of items from a universe of size $n$, with repeats. The output is an estimate of the number $d$ of distinct items, with a relative error that falls like $1/\sqrt m$. This is the [distinct elements problem](/distinct-elements-problem/), and the database form of it is [cardinality estimation](/cardinality-estimation/).

## The algorithm

Let $h$ map items to 32-bit integers, and let $b \in \{4, \ldots, 16\}$. For a hash value $y$, $j$ is its first $b$ bits and $w$ its other $32 - b$ bits. $\rho(w)$ is the position of the leftmost 1 of $w$, counted from 1, with $\rho(0) = 33 - b$.

```pseudo id=main
HYPERLOGLOG(σ, h, b)
L1  M[0..m−1] ← 0                            ▷ m = 2^b registers
L2  for each item x of σ do
L3      y ← h(x)
L4      j ← the first b bits of y;  w ← the other 32 − b bits
L5      M[j] ← max(M[j], ρ(w))
L6  E ← α_m · m² / Σ_j 2^(−M[j])              ▷ the raw estimate
L7  return CORRECT(E, M)                      ▷ small and large range
```

**The constant.** $\alpha_{16} = 0.673$, $\alpha_{32} = 0.697$, $\alpha_{64} = 0.709$, and $\alpha_m = 0.7213/(1 + 1.079/m)$ for $m \ge 128$. The limit is $\alpha_\infty = 1/(2\ln 2) \approx 0.72135$.

**The corrections of line L7.** Let $V$ be the number of registers equal to 0.

- **Small range.** If $E \le \tfrac52 m$ and $V > 0$, return $m \ln(m/V)$, the [linear counting](/linear-counting/) estimate from the empty registers.
- **Middle range.** If $E \le 2^{32}/30$, return $E$.
- **Large range.** Otherwise return $-2^{32}\ln(1 - E/2^{32})$, which undoes the effect of collisions of 32-bit hash values.

## Example

Let $b = 4$, so $m = 16$, and the stream $a, b, c, a, d, b$ with $d = 4$. The rest $w$ has 28 bits.

| item | register $j$ | $w$ | $\rho(w)$ |
|---|---|---|---|
| a | 0 | $2^{25}$ | 3 |
| b | 5 | $2^{27}$ | 1 |
| c | 9 | $2^{20}$ | 8 |
| d | 0 | $2^{26}$ | 2 |

Register 0 keeps $\max(3, 2) = 3$, register 5 holds 1, register 9 holds 8, and the other 13 registers are 0. The repeats of $a$ and $b$ change nothing. Then
$$\sum_j 2^{-M[j]} = 13 + 2^{-3} + 2^{-1} + 2^{-8} \approx 13.629, \qquad E = \frac{0.673 \cdot 256}{13.629} \approx 12.64.$$
Since $E \le 40 = \tfrac52 m$ and $V = 13$, line L7 returns $16\ln(16/13) \approx 3.32$, against $d = 4$. The raw value 12.64 shows why the small range correction is needed: with most registers at 0, the harmonic mean is close to $\alpha_m m$.

## Correctness

The proof page proves the parts that do not depend on the fine asymptotics.

- **The state.** Each register is the maximum of $\rho$ over the distinct items in its bucket. So repeats and order do not matter, and the register by register maximum of two sketches with the same hash and the same $b$ is exactly the sketch of the union.
- **The law of a register.** For an ideal hash and a Poisson number of items with mean $\lambda$, the registers are independent and $\Pr[M[j] \le r] = \exp(-\mu 2^{-r})$, with $\mu = \lambda/m$.
- **Why a harmonic mean.** In the same model $\mathbb{E}[2^{-M[j]}]$ has an exact series, and $\mu\,\mathbb{E}[2^{-M[j]}]$ is close to $1/(2\ln 2)$. So $m / \sum_j 2^{-M[j]}$ estimates $\mu$ up to the factor $\alpha_\infty$, and $\alpha_m m^2/\sum_j 2^{-M[j]}$ estimates $\lambda$.
- **The two corrections.** The number $V$ of empty registers has mean $m e^{-\lambda/m}$, so $m\ln(m/V)$ inverts it. The number of distinct 32-bit hash values of $d$ items has mean $2^{32}(1 - (1 - 2^{-32})^d)$, and the large range formula inverts its approximation $2^{32}(1 - e^{-d/2^{32}})$.

**What is cited, and for which hash.** Theorem 1 of the paper says, for a fully random hash function and $d \to \infty$, that $\mathbb{E}[E]/d = 1 + \delta_1(d) + o(1)$ with $|\delta_1(d)| < 5 \cdot 10^{-5}$ for $m \ge 16$, and that the relative standard error is $\beta_m/\sqrt m + \delta_2(d) + o(1)$ with a similar tiny $\delta_2$. The values are $\beta_{16} = 1.106$, $\beta_{32} = 1.070$, $\beta_{64} = 1.054$, $\beta_{128} = 1.046$ and $\beta_\infty = \sqrt{3\ln 2 - 1} \approx 1.03896$. These are asymptotic statements for an ideal hash; they are not tail bounds and do not cover hash families with limited independence.

**What is empirical.** The thresholds $\tfrac52 m$ and $2^{32}/30$, the choice to use linear counting below the first threshold, and the claim that the corrected estimate keeps an error near $1.04/\sqrt m$ over the whole range, come from the simulations of Section 4 of the paper, not from a proof. Heule, Nunkesser and Hall (2013) later measured a clear bias of the raw estimate for $d$ up to about $5m$, which the corrections do not remove, and fixed it in [HyperLogLog++](/hyperloglog-plus-plus/).

## Complexity

- **Update time.** $O(1)$ word operations: one hash, a shift, a count of leading zeros and a maximum. Most updates do not change any register.
- **Query time.** $O(m)$ for the sum of line L6 and the count $V$. An implementation can keep $\sum_j 2^{-M[j]}$ and $V$ up to date at each change of a register, and then a query is $O(1)$.
- **Space.** $m$ registers. With a 32-bit hash and $b \ge 4$, $\rho \le 29$, so 5 bits per register always suffice, and $5m$ bits in total, plus the seed of $h$. In general, all registers are below $\log_2 d + 1 + c$ with probability $1 - 2^{-c}$, so $O(\log\log n)$ bits per register (proved on the [LogLog](/loglog-counting/) proof page, and the same proof applies).
- **Accuracy (cited).** About $1.04/\sqrt m$ for an ideal hash: 26% for $m = 16$, 6.5% for $m = 256$, 1.6% for $m = 4096$. The paper states that it counts beyond $10^9$ with a typical accuracy of 2% in 1.5 kB.
- **Optimality.** For a constant error, $O(m\log\log n)$ bits is close to the $\Omega(1/\varepsilon^2 + \log n)$ lower bound of the [distinct elements problem](/distinct-elements-problem/), but not equal to it. The algorithm of Kane, Nelson and Woodruff (2010) reaches the bound.

## Properties

- **Duplicate-insensitive and order-insensitive.** The state is a function of the set of distinct items.
- **Mergeable.** The register by register maximum is the sketch of the union, bit for bit. See [mergeable summaries](/mergeable-summaries/).
- **Same state as LogLog.** A LogLog sketch can be read with the HyperLogLog estimate.
- **Asymptotically unbiased for an ideal hash (cited).** The bias is below $5 \cdot 10^{-5}$ in relative terms as $d \to \infty$, for $m \ge 16$.
- **No deletions.** A maximum cannot be undone. For deletions, use a [linear sketch](/linear-sketch/).
- **Intersections are poor.** $|A \cap B|$ from $|A| + |B| - |A \cup B|$ has error relative to $|A \cup B|$. For small overlaps use the [KMV sketch](/kmv-sketch/) or MinHash.

## Variants and improvements

- **[HyperLogLog++](/hyperloglog-plus-plus/).** A 64-bit hash, so no large range correction; an empirical bias table for small counts; a sparse representation that is nearly exact for small $d$.
- **A better small range estimator.** Later work replaced the threshold rule by estimators that use the whole histogram of register values, with smaller bias across the range.
- **Register compression.** The register values are concentrated near $\log_2(d/m)$, so 4-bit registers with a common offset, or an entropy coder, save space.
- **Sliding windows.** Keep, for each register, the times of the recent large values, to count the distinct items of the last $W$ items.
- **[LogLog](/loglog-counting/) and Super-LogLog.** The arithmetic mean of the same registers, error $1.30/\sqrt m$ and $1.05/\sqrt m$.

## When to use it

Use HyperLogLog to count distinct items in large data with little memory, especially when you need many counts at once, or need to merge counts from many machines or time periods. Databases and analytics systems offer it as an approximate COUNT DISTINCT. Use the HyperLogLog++ form, or another form with a good small range estimate, when many counts are small. Use [linear counting](/linear-counting/) when you know $d$ is at most a few times the number of bits you can spend, and the [KMV sketch](/kmv-sketch/) when you also need intersections or an unbiased estimate.

## Pitfalls

- **The raw estimate of line L6 for small counts.** For $d$ below about $\tfrac52 m$, many registers are 0 and $E$ is much too large. Line L7 must apply the small range correction; even then there is a bias up to about $5m$.
- **A 32-bit hash for large counts in line L3.** With about $10^8$ distinct items or more, 32-bit hash values collide often. The large range correction of line L7 helps, but a 64-bit hash is the real fix.
- **Overlapping bits in line L4.** The register index and $w$ must come from disjoint bits of the hash value.
- **The wrong $\alpha_m$ in line L6.** The table values are for $m = 16, 32, 64$; using $0.7213$ for $m = 16$ makes the estimate about 7% too large.
- **A weak or keyed-wrong hash in line L3.** The analysis assumes an ideal hash. A hash with structure on the keys, or different hashes on different machines, breaks the estimate and the merge.
- **Adversarial streams.** If an attacker knows the hash, it can choose items that set large registers and inflate the count. Use a secret seed.

## Implementations

## History

Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier presented HyperLogLog at the 2007 Conference on Analysis of Algorithms. It came after probabilistic counting with stochastic averaging (Flajolet and Martin 1985) and LogLog counting (Durand and Flajolet 2003). The main change was the harmonic mean, and the paper analysed it with Mellin transforms and a Poisson model, for an ideal hash. In 2013 Heule, Nunkesser and Hall of Google described HyperLogLog++, the engineered form with a 64-bit hash, bias correction and a sparse representation. HyperLogLog is now built into many databases, stream processors and caches.

## References
