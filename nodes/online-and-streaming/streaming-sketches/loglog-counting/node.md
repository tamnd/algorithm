---
tag: 919CZB
kind: algorithm
slug: loglog-counting
name: LogLog counting
aliases:
- LogLog
- LogLog algorithm
- Durand-Flajolet LogLog
area: online-and-streaming/streaming-sketches
level: core
summary: Keeps the maximum rank per bucket, using log log n bits per bucket.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {m: the number of registers, n: the universe size}
  time: {worst: O(1), average: O(1)}
  space: {extra: O(m log log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 2003
  people: [Marianne Durand, Philippe Flajolet]
  note: Durand and Flajolet presented LogLog counting at ESA 2003, with its analysis for an ideal hash and the Super-LogLog truncation rule.
prereqs: [pcsa, flajolet-martin-algorithm, distinct-elements-problem]
see_also: [hyperloglog, hyperloglog-plus-plus, pcsa, flajolet-martin-algorithm, kmv-sketch, linear-counting, mergeable-summaries, poisson-distribution]
sources:
  - paper: doi:10.1007/978-3-540-39658-1_55
    title: Marianne Durand and Philippe Flajolet, Loglog counting of large cardinalities, ESA 2003, LNCS 2832
    locator: pp. 605 to 617 (the algorithm, the constant α_m, the standard error 1.30/√m and Super-LogLog)
  - paper: doi:10.46298/dmtcs.3545
    title: Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog, the analysis of a near-optimal cardinality estimation algorithm, AofA 2007
    locator: Section 1 (the comparison with LogLog)
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pp. 182 to 209 (stochastic averaging)
---

LogLog counting estimates the number $d$ of distinct items with $m$ small registers. Each item is hashed; the first bits of the hash choose a register, and the register keeps the largest value of $\rho$, the position of the leftmost 1 bit in the rest of the hash. A register then holds about $\log_2(d/m)$, so it needs only about $\log_2\log_2 n$ bits, 5 bits for a 32-bit hash. The estimate is $\alpha_m\, m\, 2^{\bar M}$, where $\bar M$ is the arithmetic mean of the registers and $\alpha_m \to 0.39701$. Durand and Flajolet (2003) proved, for an ideal random hash, that the relative standard error is about $1.30/\sqrt m$. It is the step from [PCSA](/pcsa/), which keeps a bitmap per bucket, to [HyperLogLog](/hyperloglog/), which keeps the same registers but uses a harmonic mean. On this page $m = 2^b$ is the number of registers, $d$ is the number of distinct items, $n$ is the universe size, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

Hash each item to a string of random looking bits. The chance that the string starts with $r - 1$ zeros and then a 1 is $2^{-r}$. So among $d$ different items, the longest run of leading zeros is near $\log_2 d$. Remembering only that longest run takes very few bits: a number near 30 fits in 5 bits. One such number is a rough guess. LogLog splits the items into $m$ groups with the first bits of the hash, keeps the longest run in each group, and averages the $m$ runs. Two raised to the average, times $m$ and a fixed constant, is the estimate. Repeated items give the same hash, so they change nothing.

## The problem

The input is a stream of items from a universe of size $n$, with repeats. The output is an estimate of the number $d$ of distinct items, with a relative error that falls like $1/\sqrt m$. This is the [distinct elements problem](/distinct-elements-problem/).

## The algorithm

Let $h$ map items to $L$-bit integers. For a hash value $y$, let $j$ be its first $b$ bits and $w$ the other $L - b$ bits. Let $\rho(w)$ be the position of the leftmost 1 in $w$, counted from 1, with $\rho(0) = L - b + 1$.

```pseudo id=main
LOGLOG(σ, h, b)
L1  M[0..m−1] ← 0                            ▷ m = 2^b registers
L2  for each item x of σ do
L3      y ← h(x)
L4      j ← the first b bits of y;  w ← the other L − b bits
L5      M[j] ← max(M[j], ρ(w))
L6  return α_m · m · 2^((1/m) Σ_j M[j])
```

The constant of line L6 is
$$\alpha_m = \left(\Gamma(-1/m)\,\frac{1 - 2^{1/m}}{\ln 2}\right)^{-m}, \qquad \alpha_\infty = \frac{e^{-\gamma}\sqrt 2}{2} \approx 0.39701,$$
with $\gamma$ Euler's constant. It is 0.312 for $m = 4$, 0.376 for $m = 16$, 0.392 for $m = 64$ and 0.397 for $m = 1024$. The relative gap $1 - \alpha_m/\alpha_\infty$ is about $0.84/m$.

## Example

Let $b = 2$, so $m = 4$, with 32-bit hash values and the stream $a, b, c, a, d, e, b$ with $d = 5$. The rest $w$ has 30 bits.

| item | register $j$ | $w$ | $\rho(w)$ |
|---|---|---|---|
| a | 0 | $2^{27}$ | 3 |
| b | 1 | $2^{29}$ | 1 |
| c | 2 | $2^{25}$ | 5 |
| d | 0 | $2^{29}$ | 1 |
| e | 3 | $2^{28}$ | 2 |

A 30-bit $w = 2^{27}$ has 2 leading zeros and then a 1, so $\rho = 3$. Register 0 sees $a$ and $d$ and keeps $\max(3, 1) = 3$. The registers are $[3, 1, 5, 2]$, with mean $11/4$, and the estimate is $\alpha_4 \cdot 4 \cdot 2^{11/4} \approx 0.312 \cdot 4 \cdot 6.73 \approx 8.40$, against $d = 5$. With 4 registers and 5 items the estimate is rough; the guarantee is for many registers and $d \gg m$.

## Correctness

Each register is the maximum of $\rho$ over the distinct items of its bucket, so the state depends only on the set of distinct items, and the register by register maximum of two sketches with the same hash is the sketch of the union. For an ideal hash, $\Pr[\rho(w) > r] = 2^{-r}$. If the number of items is Poisson with mean $\lambda$, the registers are independent, and each has the exact law $\Pr[M \le r] = \exp(-\mu 2^{-r})$ with $\mu = \lambda/m$. This law has mean $\log_2\mu + \gamma/\ln 2 + 1/2$ up to a tiny periodic term, which is where $\alpha_\infty = 2^{-\gamma/\ln 2 - 1/2} = e^{-\gamma}/\sqrt 2$ comes from. The proof page proves the exact law and the bound on the size of the registers.

The constant $\alpha_m$ for finite $m$, the asymptotic unbiasedness and the standard error $\beta_m/\sqrt m$, with $\beta_{128} = 1.30540$ and $\beta_\infty = \sqrt{\pi^2/6 + (\ln 2)^2/12} \approx 1.29806$, are theorems of Durand and Flajolet for a fully random hash, and are cited here.

## Complexity

- **Update time.** $O(1)$ word operations: one hash, a shift, a count of leading zeros and a maximum.
- **Query time.** $O(m)$: a sum of the registers and one power of 2.
- **Space.** $m$ registers. With probability at least $1 - 2^{-c}$, every register is below $\log_2 d + 1 + c$, so each register needs $\lceil\log_2(\log_2 n + 2 + c)\rceil = O(\log\log n)$ bits (proved). For a 32-bit hash and $b \ge 2$, $\rho \le 31$ and 5 bits always suffice. The total is $O(m \log\log n)$ bits plus the seed of $h$.
- **Accuracy (cited).** Relative standard error about $1.30/\sqrt m$ for an ideal hash and large $d/m$. So $m = 1024$ registers of 5 bits, 640 bytes, give about 4%.
- **Accuracy of Super-LogLog (cited, empirical constant).** Keep only the $\lfloor 0.7m \rfloor$ smallest registers in the mean, with a matching constant. The error drops to about $1.05/\sqrt m$.

## Properties

- **Duplicate-insensitive and order-insensitive.** The state is a function of the set of distinct items.
- **Mergeable.** The register by register maximum is exact for the union. See [mergeable summaries](/mergeable-summaries/).
- **Asymptotically unbiased (cited).** The constant $\alpha_m$ makes the estimate unbiased as $d \to \infty$, up to a tiny periodic term.
- **Sensitive to large registers.** The arithmetic mean gives weight to the largest registers, which have the heaviest tail. HyperLogLog and the truncation of Super-LogLog both reduce this.
- **Biased for small counts.** For $d$ near or below $m$, many registers are 0 and the estimate is about $\alpha_m m$, not near $d$.
- **No deletions.** A maximum cannot be undone.

## Variants and improvements

- **Super-LogLog.** The truncation rule above, and a restriction of the register size. Durand and Flajolet report an error of about $1.05/\sqrt m$.
- **[HyperLogLog](/hyperloglog/).** The same registers, with $\rho$ counted the same way, but the estimate is $\alpha_m m^2 \big/ \sum_j 2^{-M[j]}$, a harmonic mean. The error is about $1.04/\sqrt m$, with a proof, and it has small and large range corrections.
- **[HyperLogLog++](/hyperloglog-plus-plus/).** A 64-bit hash, an empirical bias correction and a sparse form for small counts.
- **[PCSA](/pcsa/).** Keeps a bitmap per bucket; more bits per bucket, error $0.78/\sqrt m$.
- **Small range correction.** As in HyperLogLog, use [linear counting](/linear-counting/) on the number of zero registers when $d$ is small.

## When to use it

LogLog is mainly of historical and teaching value: it is the simplest register sketch with a full analysis. For new systems, use [HyperLogLog](/hyperloglog/) or HyperLogLog++, which use the same registers and the same update, with a smaller error and a better treatment of small counts. A system that already stores LogLog registers can switch to the HyperLogLog estimate without changing the state.

## Pitfalls

- **The trailing or leading convention in line L5.** $\rho$ here counts from 1, the position of the leftmost 1. Counting trailing zeros from 0, as in Flajolet-Martin, also works, but then $\alpha_m$ must change by a factor of 2.
- **Overlapping bits in line L4.** The register index and $w$ must come from disjoint bits of the hash.
- **The constant in line L6.** $\alpha_m$ is far from $\alpha_\infty$ for small $m$: 0.312 at $m = 4$ against 0.397. Use the formula, or $m \ge 64$.
- **Small counts in line L6.** With many registers at 0, the estimate is too large. Add a small range correction.
- **A short hash in line L3.** With a 32-bit hash, counts near $2^{32}$ fill the high values of the registers and hash collisions bias the count down.

## Implementations

## History

Marianne Durand and Philippe Flajolet presented LogLog counting at ESA 2003, under the title "Loglog counting of large cardinalities". The name says that each register needs only $\log\log n$ bits, against $\log n$ bits for a bitmap of PCSA. Their abstract notes that a memory smaller than the abstract itself is enough to estimate the number of distinct words in the works of Shakespeare within a few percent. Four years later, Flajolet, Fusy, Gandouet and Meunier replaced the arithmetic mean by the harmonic mean, which gave HyperLogLog.

## References
