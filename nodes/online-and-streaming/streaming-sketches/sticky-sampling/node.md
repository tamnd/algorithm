---
tag: VTF6WC
kind: algorithm
slug: sticky-sampling
name: Sticky sampling
aliases:
- Manku-Motwani sticky sampling
area: online-and-streaming/streaming-sketches
level: core
summary: Samples items with a decreasing rate and keeps exact counts for sampled items.
solves: [frequent-items-problem]
model: streaming-model
complexity:
  vars: {s: the support, m: the stream length}
  time: {amortized: O(1) expected}
  space: {expected: O((1/ε) log(1/(s δ)))}
properties: {online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [frequent-items-problem, frequency-vector, epsilon-delta-guarantee, stream-sampling]
see_also: [lossy-counting, sample-and-hold, misra-gries-summary, space-saving, reservoir-sampling, union-bound]
sources:
  - url: https://www.vldb.org/conf/2002/S10P03.pdf
    title: Gurmeet Singh Manku and Rajeev Motwani, Approximate frequency counts over data streams, Proceedings of the 28th International Conference on Very Large Data Bases (VLDB), 2002, pages 346 to 357
    locator: Section 4.1, Sticky Sampling, with the theorem that it uses at most (2/ε) log(1/(sδ)) entries in expectation
---

Sticky sampling is a randomized summary for frequent items on an insertion-only stream, by Manku and Motwani (2002). An item enters the table when one of its occurrences is sampled, and from then on all its occurrences are counted exactly, so the entry "sticks". The sampling rate falls by half each time the stream length doubles, and at each change of rate the table is thinned so that it looks as if the new rate had been used from the start. For support $s$, error $\varepsilon$ and failure probability $\delta$, the expected number of entries is at most $2t$ with $t = (1/\varepsilon) \ln(1/(s\delta))$, which does not depend on the stream length.

## In plain words

You keep a notebook of items and their tallies. When an item is already in the notebook, add one to its tally. When it is new, flip a weighted coin, and write it down only if the coin says so. Early on, the coin always says yes. Later it says yes less and less often, because the stream is longer and a frequent item will be caught soon anyway.

Each time the coin gets weaker, you go over the notebook and remove the start of each tally, as if the weaker coin had been used from the beginning. Some tallies drop to zero and leave the notebook. So the notebook stays small, and a frequent item is caught early and loses only a few occurrences.

## The problem

The input is a stream $a_1, \ldots, a_N$ in the [cash register model](/cash-register-model/), with [frequency vector](/frequency-vector/) $f$. As in the paper, $N$ is the stream length; the complexity fields call it $m$. Given a support $s$, an error $\varepsilon < s$ and a failure probability $\delta$, the output must, with probability at least $1 - \delta$, report every item with $f_x \ge sN$ with an estimate at most $\varepsilon N$ below $f_x$, and no item with $f_x < (s - \varepsilon) N$. This is the $\varepsilon$-approximate [frequent items problem](/frequent-items-problem/) with the [epsilon-delta guarantee](/epsilon-delta-guarantee/).

## The algorithm

Let $t = (1/\varepsilon) \ln(1/(s\delta))$. The rate $r$ is 1 for the first $2t$ items, 2 for the next $2t$, 4 for the next $4t$, and so on: for $r \ge 2$, the rate is $r$ while $rt < N \le 2rt$. The table $S$ maps items to positive counts.

```pseudo id=main
STICKY-UPDATE(S, x)                      ▷ one occurrence of x
L1  N ← N + 1
L2  while N > 2rt do                     ▷ the end of a phase
L3      ADJUST(S, 2r);  r ← 2r
L4  if x ∈ S then S[x] ← S[x] + 1
L5  else with probability 1/r insert x with S[x] ← 1

ADJUST(S, r′)                            ▷ thin from rate r to rate r′ = 2r
L6  for each y ∈ S do
L7      with probability 1/2 keep S[y] as it is
L8      else S[y] ← S[y] − 1 − G, with G the number of failures before the first success of coins with success 1/r′, cut at S[y] − 1
L9      if S[y] = 0 then remove y from S

STICKY-ESTIMATE(S, x)
L10 if x ∈ S then return S[x] else return 0

STICKY-REPORT(S)
L11 return each x ∈ S with S[x] ≥ (s − ε) N
```

**The ideal state.** Imagine that each occurrence is sampled with probability $1/r$, independently, and that an item's entry counts its occurrences from the first sampled one. Call this the ideal state at rate $r$. Lines L4 and L5 keep this state for new occurrences. ADJUST maps the ideal state at rate $r$ to the ideal state at rate $2r$: an occurrence sampled at rate $r$ stays sampled at rate $2r$ with probability $1/2$ (line L7), and if it does not, each later occurrence, which was not tested before, is sampled with probability $1/r'$ (line L8). So at all times the table has exactly the distribution of the ideal state at the current rate.

**The rule in the paper.** Manku and Motwani write ADJUST with fair coins only: for each entry, toss a fair coin until heads and subtract 1 for each tails. They state that this gives exactly the state of the new rate. That is true for the first change, from rate 1 to rate 2, but not after it. An item whose first 3 occurrences fall in the first phase has its entry start at its second occurrence with probability $1/4$ after the change to rate 4 with fair coins, while the ideal state at rate 4 gives $(3/4)(1/4) = 3/16$. The fair-coin rule removes too little, so its estimates are no lower than the ideal ones, but its table can be much larger than $2t$. The tests of this page check both facts. The rule above, with a fair coin for the first step and coins of success $1/r'$ for the later steps, is the one for which the analysis of the paper holds.

## Example

Take $s = 0.9$, $\varepsilon = 0.5$ and $\delta = 0.5$, so $t = 2 \ln(1/0.45) \approx 1.6$. The rate is 1 for $N \le 3$, 2 for $4 \le N \le 6$, and 4 for $7 \le N \le 12$. Let the stream start with $x, x, x$, followed by other items.

- After the third item, $S[x] = 3$, since the rate was 1.
- At $N = 4$, ADJUST to rate 2. With probability $1/2$ the count stays 3. Otherwise, each of the two later occurrences is tried with probability $1/2$. So the count is 3, 2, 1 or 0 with probabilities $1/2, 1/4, 1/8, 1/8$. These are the ideal probabilities at rate 2: the entry starts at occurrence $l$ with probability $(1/2)^l$.
- At $N = 7$, ADJUST to rate 4. Now the count is 3, 2, 1 or 0 with probabilities $1/4$, $3/16$, $9/64$ and $27/64$, the ideal ones at rate 4. With fair coins only, they would be $1/4$, $1/4$, $3/16$ and $5/16$.

## Correctness

**Theorem.** At each time, with probability at least $1 - \delta$, every item with $f_x \ge sN$ is in $S$ with $S[x] \ge f_x - \varepsilon N$. Always, $S[x] \le f_x$. So line L11 reports every item with $f_x \ge sN$ and no item with $f_x < (s - \varepsilon) N$, with probability at least $1 - \delta$.

The estimate of $x$ is low by more than $\varepsilon N$ only if the first $\lfloor \varepsilon N \rfloor + 1$ occurrences of $x$ were all left out in the ideal state. If $r = 1$, nothing is left out. If $r \ge 2$, then $N > rt$, so this has probability at most $(1 - 1/r)^{\varepsilon N} \le e^{-\varepsilon N / r} < e^{-\varepsilon t} = s\delta$. There are at most $1/s$ items with $f_x \ge sN$, so a [union bound](/union-bound/) gives a failure probability below $\delta$. Counts are never too large, because an entry counts only occurrences that happened. The full proof, including that ADJUST gives the ideal state, is below.

## Complexity

- **Expected space.** In the ideal state at rate $r$, item $x$ has an entry with probability $1 - (1 - 1/r)^{f_x} \le f_x / r$. So the expected number of entries is at most $N/r$. For $r = 1$, $N \le 2t$, and for $r \ge 2$, $N \le 2rt$. In both cases the expected number of entries is at most $2t = (2/\varepsilon) \ln(1/(s\delta))$. This is the bound of the paper.
- **Time.** Lines L1 to L5 take $O(1)$ expected time with a hash table. ADJUST takes $O(|S|)$ time when $G$ is drawn in one step by [inverse transform sampling](/inverse-transform-sampling/), as $G = \lfloor \ln U / \ln(1 - 1/r') \rfloor$. A phase of rate $r$ has $rt$ items, or $2t$ for $r = 1$, and the table has $O(t)$ entries in expectation, so the amortized cost of ADJUST is $O(1)$ for each item.
- **Random bits.** One coin for each new item and $O(1)$ coins for each entry at each change of rate.

## Properties

- **Randomized.** The guarantee holds with probability $1 - \delta$ at each time, not for all times together.
- **One-sided.** Counts are never too large.
- **Space independent of $N$.** The expected size depends on $s$, $\varepsilon$ and $\delta$ only. Lossy counting has a worst-case bound that grows like $\log(\varepsilon N)$.
- **Needs $s$ in advance.** The support $s$ enters $t$. Lossy counting needs only $\varepsilon$, and any support $s > \varepsilon$ can be asked at query time.

## Variants and improvements

- **Lossy counting.** The deterministic method of the same paper, [lossy counting](/lossy-counting/), uses $O((1/\varepsilon) \log(\varepsilon N))$ entries in the worst case. Manku and Motwani found it better in practice.
- **Sample and hold.** [Sample and hold](/sample-and-hold/) by Estan and Varghese, from the same year, uses the same "sample, then count exactly" idea with a fixed rate, for flows in network routers, and gives unbiased estimates.
- **Deterministic counters.** [Misra-Gries](/misra-gries-summary/) and [Space-Saving](/space-saving/) give the guarantee with probability 1 and $\lceil 1/\varepsilon \rceil$ counters, which is less than $2t$ whenever $s\delta < e^{-1/2}$ and $1/\varepsilon$ is an integer.

## When to use it

Sticky sampling is mainly of historical and teaching value. It shows how sampling with a falling rate gives memory that does not grow with the stream. For frequent items in practice, the deterministic counter-based summaries need less memory and give a guarantee with probability 1. If you implement sticky sampling, use the change of rate on this page, not the fair-coin rule.

## Pitfalls

- **Fair coins at every change of rate.** As above, this keeps too many entries after the second change, and the expected space can be well above $2t$. On a stream of runs of 10 equal items, with $t = 10$ and 40 seeded runs until rate 256, the fair-coin rule keeps about 46 entries on average while the rule above keeps about 19.
- **Counting the sampled occurrence twice.** Line L5 inserts the count 1 for the sampled occurrence. Inserting 0 and then adding 1 later loses it.
- **Changing the rate after the item.** The rate for item $N$ must be set before line L4, as in line L2. Otherwise the first item of a phase is sampled with the old rate.
- **A union bound over all items.** The bound $\delta$ covers the at most $1/s$ items with $f_x \ge sN$. It does not say that every estimate is within $\varepsilon N$.

## Implementations

## History

Gurmeet Singh Manku and Rajeev Motwani presented sticky sampling together with lossy counting at VLDB 2002. Sticky sampling builds on the idea of counting samples of Gibbons and Matias (1998), in which a sampled value is counted exactly from then on. The paper states that the change of rate with fair coins leaves the table exactly in the state of the new rate; as shown above, this holds only for the first change, and the rule with coins of success $1/r'$ after the first step restores the analysis.

## References
