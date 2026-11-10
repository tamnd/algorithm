---
tag: XQTWXT
kind: algorithm
slug: sliding-hyperloglog
name: Sliding HyperLogLog
aliases:
- SHLL
- sliding window HyperLogLog
area: online-and-streaming/sliding-windows
level: research
summary: HyperLogLog in which each register keeps a short list of (time, rank) pairs, so that the registers of any window of length w <= W can be read exactly at query time.
solves: [sliding-window-distinct-count]
model: word-ram
complexity:
  vars: {m: the number of registers, n: the number of distinct items in a window}
  time: {amortized: O(1), worst: O(log n)}
  space: {extra: O(m log n)}
properties: {online: true, deterministic: false}
history:
  year: 2010
  people: [Yousra Chabchoub, Georges Hébrail]
  note: Chabchoub and Hébrail presented Sliding HyperLogLog at the ICDM 2010 workshops, after the Sliding MinCount algorithm of Fusy and Giroire (2007).
prereqs: [hyperloglog, sliding-window-model, time-based-window, hash-function]
see_also: [hyperloglog, sliding-window-distinct-count, hyperloglog-plus-plus, smooth-histogram, kmv-sketch, linear-counting, sliding-window-maximum, distinct-elements-problem]
sources:
  - paper: doi:10.1109/ICDMW.2010.18
    title: Yousra Chabchoub and Georges Hébrail, Sliding HyperLogLog, estimating cardinality in a data stream over a sliding window, IEEE ICDM Workshops 2010
    locator: pp. 1297 to 1303
  - url: https://hal.science/hal-00465313
    title: Yousra Chabchoub and Georges Hébrail, Sliding HyperLogLog, estimating cardinality in a data stream, preprint hal-00465313, 2010
    locator: Section III (the List of Future Possible Maxima, its update, the accuracy and the memory of 5 m E(L_n) bytes)
  - paper: doi:10.1137/1.9781611972979.9
    title: Éric Fusy and Frédéric Giroire, Estimating the number of active flows in a data stream over a sliding window, ANALCO 2007
    locator: pp. 223 to 231 (Sliding MinCount and the same list update)
  - paper: doi:10.46298/dmtcs.3545
    title: Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog, the analysis of a near-optimal cardinality estimation algorithm, AofA 2007, DMTCS Proceedings
    locator: Theorem 1 (the standard error 1.04/sqrt(m)) and Figure 3 (the estimate with its range corrections)
---

Sliding HyperLogLog estimates the number of distinct items that arrived in the last $w$ time units, for each $w$ up to a fixed $W$, in a [time-based window](/time-based-window/). It keeps the $m$ registers of [HyperLogLog](/hyperloglog/), but each register stores a short list of pairs (time, rank) instead of one rank: the pairs that can still be the largest rank of some future window. At query time it reads, in each register, the largest rank in the window, and applies the HyperLogLog estimate, so the answer is the one that HyperLogLog would give on the window. Chabchoub and Hébrail introduced it in 2010; it solves the [sliding window distinct count](/sliding-window-distinct-count/).

## In plain words

HyperLogLog hashes each item, sends it to one of many registers, and keeps in each register the largest "rank", a number that is large for rare hash values. It cannot forget, so it cannot count only the recent items. Sliding HyperLogLog keeps, for each register, the times of the ranks that may still matter. When a new item comes, older entries with a rank that is not larger are useless: the new entry is newer and at least as large. Entries that are too old are also deleted. What is left is a short list whose ranks go down as the times go up. For any window, the largest rank in the window is the first entry that is new enough.

## The problem

The input is a stream of pairs $(\tau_k, x_k)$, an item $x_k$ with a timestamp $\tau_k$, where the timestamps do not decrease. A window length $W$ is fixed. At a time $\tau$ at or after the last timestamp, a query with $0 \le w \le W$ asks for the number $n$ of distinct items $x_k$ with $\tau - w \le \tau_k \le \tau$. The answer may have a small relative error. A [count-based window](/count-based-window/) is the case $\tau_k = k$.

## The algorithm

Let $m = 2^b$. A [hash function](/hash-function/) $h$ maps items to 64-bit strings. The first $b$ bits of $h(x)$ give the register $j$, and the rank $\rho(x)$ is the position of the first 1-bit in the other $64 - b$ bits, counting from 1 (and $65 - b$ if they are all 0). Register $j$ keeps a list $L_j$ of pairs (time, rank), oldest first. Chabchoub and Hébrail call it the List of Future Possible Maxima (LFPM).

```pseudo id=main
SHLL-UPDATE(τ, x)            ▷ timestamps do not decrease
L1  j ← the first b bits of h(x); r ← ρ(x)
L2  while L_j is not empty and its oldest pair has time < τ − W do remove that pair
L3  while L_j is not empty and its newest pair has rank ≤ r do remove that pair
L4  append (τ, r) to L_j as its newest pair

SHLL-QUERY(w, τ)              ▷ 0 ≤ w ≤ W; τ is at or after the last timestamp
L5  for j ← 1 to m do
L6      M_j ← the rank of the oldest pair of L_j with time ≥ τ − w, or 0 if there is none
L7  E ← α_m m² / Σ_j 2^(−M_j)
L8  if E ≤ 5m/2 and V > 0, where V is the number of j with M_j = 0, then return m ln(m/V)
L9  return E
```

Lines L7 to L9 are the HyperLogLog estimate, with the constant $\alpha_m \approx 0.7213/(1 + 1.079/m)$ and the [linear counting](/linear-counting/) estimate for small values. After line L4 the ranks in $L_j$ strictly decrease from the oldest pair to the newest one, so line L6 can stop at the first pair that is new enough, or use binary search.

## Example

Take $W = 5$ and one register $j$ that receives items at the times $1, 2, 3, 4, 5, 7, 8, 10$ with the ranks $2, 1, 3, 1, 2, 2, 1, 1$.

| $\tau$ | rank | $L_j$ after the update | what changed |
|---|---|---|---|
| 1 | 2 | (1, 2) | |
| 2 | 1 | (1, 2), (2, 1) | rank 1 is less than 2, so (1, 2) stays |
| 3 | 3 | (3, 3) | rank 3 removes both pairs |
| 4 | 1 | (3, 3), (4, 1) | |
| 5 | 2 | (3, 3), (5, 2) | rank 2 removes (4, 1) |
| 7 | 2 | (3, 3), (7, 2) | equal rank 2 removes (5, 2) |
| 8 | 1 | (3, 3), (7, 2), (8, 1) | |
| 10 | 1 | (7, 2), (10, 1) | time 3 is less than $10 - 5$; rank 1 removes (8, 1) |

At $\tau = 8$, a query with $w = 5$ covers the times 3 to 8; the oldest pair with time at least 3 is (3, 3), so $M_j = 3$, the largest rank among the items at the times 3, 4, 5, 7 and 8. With $w = 4$ the oldest pair with time at least 4 is (7, 2), and $M_j = 2$, the largest rank among the times 4 to 8. At $\tau = 10$ with $w = 2$, the pair is (10, 1) and $M_j = 1$, the largest rank of the items at times 8 and 10.

## Correctness

The full proof is on the [proof page](proofs/correctness.md). The key fact is: an item of register $j$ is in $L_j$ when it is not too old and no later item of the register has a rank that is at least as large. Take a window that starts at a time $u \ge \tau - W$, and let $e$ be the last item of the window with the largest rank of the window. Each later item is in the window, so it has a smaller rank, and $e$ is in the list. The ranks in the list decrease, so the oldest pair with time at least $u$ has a rank at least that of $e$, and it cannot have more. So $M_j$ is the register of HyperLogLog run on the items of the window, for each $j$, and the answer is the HyperLogLog estimate of the window. For an ideal random hash, its standard error is about $1.04/\sqrt{m}$ (Flajolet et al., Theorem 1), as Chabchoub and Hébrail note.

## Complexity

- **Space.** The ranks in a list strictly decrease and are in $\{1, \ldots, 65 - b\}$, so a list has at most $65 - b$ pairs. With an ideal random hash, the expected length of a list is at most $H_D \le 1 + \ln D$, where $D$ is the number of distinct items of that register in one window (proof page). For $n$ distinct items in the window, $D$ is about $n/m$, which gives $m \ln(n/m)$ pairs, the bound that Chabchoub and Hébrail give. Each pair is a timestamp and a rank of 6 bits; they count 5 bytes per pair.
- **Update time.** Each pair is appended once and removed at most once, so lines L2 and L3 take $O(1)$ amortized time per item. In the worst case one update removes a whole list, $O(\log n)$ pairs for a hash of $O(\log n)$ bits.
- **Query time.** $O(m)$ registers, each with a scan of its list, so $O(m \log n)$ in the worst case and $O(m \log \log n)$ with binary search.

HyperLogLog itself needs $O(m \log \log n)$ bits. Sliding HyperLogLog pays for the windows with a factor of about $\ln(n/m)$ pairs per register, each with a full timestamp.

## Properties

- **Exact registers.** For each window length $w \le W$ and each query time, the registers are exactly those of HyperLogLog on the items of the window, with the same hash. All error results of HyperLogLog carry over.
- **All window lengths at once.** One structure answers each $w \le W$, so it can report the count of the last minute and the last hour from the same lists.
- **Duplicates.** A repeated item has the same hash, so its new pair removes its old pair in line L3. A list never holds two pairs of one item.
- **Randomized.** The algorithm is deterministic for a fixed hash, but the error bounds and the expected list length hold for a random hash.
- **Merging.** Two structures with the same hash and the same $W$ merge register by register: take the union of the two lists and remove each pair that has a later pair with a rank at least as large.

## Variants and improvements

- **Sliding MinCount.** Fusy and Giroire (2007) apply the same list to the smallest hash values of MinCount. Chabchoub and Hébrail state that its standard error is about $1.3/\sqrt{m}$, larger than the $1.04/\sqrt{m}$ of the HyperLogLog version.
- **HyperLogLog++.** The bias correction and the sparse representation of [HyperLogLog++](/hyperloglog-plus-plus/) apply to the registers of line L6 without change.
- **Smooth histograms.** The number of distinct items is a [smooth function](/smooth-function/), so a [smooth histogram](/smooth-histogram/) with HyperLogLog or [KMV](/kmv-sketch/) instances also gives a window estimate, for one fixed $W$. Braverman, Grigorescu, Lang, Woodruff and Zhou (2018) give a nearly optimal space bound with more refined methods; see the [sliding window distinct count](/sliding-window-distinct-count/).
- **Monotone queues.** The list of a register is the monotone queue of the [sliding window maximum](/sliding-window-maximum/), applied to the ranks of one register; with a fixed $w = W$ it computes the same maximum.

## When to use it

Use it to count distinct flows, users or keys over the last minutes or hours of a stream, when several window lengths must be answered from one structure, for example in network monitoring. When only the whole stream matters, plain [HyperLogLog](/hyperloglog/) is smaller. When the window is small enough to store, keep a hash map of the last time of each item and count exactly.

## Pitfalls

- **Timestamps out of order.** The list assumes nondecreasing times. An item that arrives late with an old timestamp breaks the order of the list; buffer and sort the input first, or drop late items.
- **Expiry only on update.** Line L2 removes old pairs only from the register that receives the item. Registers that receive nothing keep old pairs until their next item. Line L6 must still test the time of each pair, and a query at a time later than the last item must use that time, not the last timestamp.
- **The equal-rank case.** Line L3 must remove pairs with a rank equal to $r$, not only smaller ones. Keeping them is still correct but makes the lists longer.
- **Window boundaries.** The paper uses a closed window $[\tau - w, \tau]$ and removes pairs with time less than $\tau - W$. Mixing this with a half-open window gives answers that are off by the items of one time step.

## Implementations

## History

Fusy and Giroire (2007) introduced the list of future possible maxima for Sliding MinCount, to estimate the number of active flows in a network over a sliding window. Chabchoub and Hébrail (2010) applied the same list to the registers of HyperLogLog, which Flajolet, Fusy, Gandouet and Meunier had presented in 2007, and tested it on synthetic traffic and on traces of the Abilene network. They argue that the mean list length is at most about $\ln(n/m)$ for large $n$ by a comparison with Sliding MinCount.

## References
