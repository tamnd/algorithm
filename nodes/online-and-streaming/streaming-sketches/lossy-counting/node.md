---
tag: 1P92W2
kind: algorithm
slug: lossy-counting
name: Lossy counting
aliases:
- Manku-Motwani lossy counting
area: online-and-streaming/streaming-sketches
level: core
summary: Processes the stream in buckets and prunes low-count entries at bucket boundaries.
solves: [frequent-items-problem, frequency-estimation]
model: streaming-model
complexity:
  vars: {m: the stream length}
  time: {amortized: O(1)}
  space: {extra: O((1/ε) log(ε m))}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [frequent-items-problem, frequency-vector, cash-register-model]
see_also: [sticky-sampling, misra-gries-summary, space-saving, count-min-sketch, sample-and-hold, frequency-estimation]
sources:
  - url: https://www.vldb.org/conf/2002/S10P03.pdf
    title: Gurmeet Singh Manku and Rajeev Motwani, Approximate frequency counts over data streams, Proceedings of the 28th International Conference on Very Large Data Bases (VLDB), 2002, pages 346 to 357
    locator: Section 4.2, Lossy Counting, with the lemmas on the error and the theorem that it uses at most (1/ε) log(εN) entries
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the comparison of counter-based summaries)
  - paper: doi:10.1145/1562764.1562789
    title: Graham Cormode and Marios Hadjieleftheriou, Finding the frequent items in streams of data, Communications of the ACM 52(10), 2009
    locator: the description of lossy counting and its experimental comparison with Misra-Gries and SpaceSaving
---

Lossy counting is a deterministic summary for frequent items on an insertion-only stream, by Manku and Motwani (2002). It cuts the stream into buckets of $w = \lceil 1/\varepsilon \rceil$ items. Each item in the table has a count since it entered and an error term $\Delta$, the number of earlier buckets. At the end of each bucket, entries with small count plus error are deleted. After $N$ items, every estimate is low by at most $\lfloor N/w \rfloor \le \varepsilon N$, and the table holds at most $(1/\varepsilon) \cdot H_B \approx (1/\varepsilon) \ln(\varepsilon N)$ entries, where $B$ is the number of buckets.

## In plain words

You count items in rounds of a fixed size, say 100 items for an error of 1 percent. When a new item arrives, you start a tally for it. You also write down how many full rounds have gone by, because the item could have appeared once in each of them and been forgotten.

At the end of each round, you look at every tally. If the tally plus the note is no more than the number of rounds so far, the item is rare, so you throw its tally away. A forgotten item can have lost at most one occurrence for each round. So each tally is low by at most the number of rounds, which is 1 percent of the stream.

## The problem

The input is a stream $a_1, \ldots, a_N$ of items in the [cash register model](/cash-register-model/), with [frequency vector](/frequency-vector/) $f$. The paper writes $N$ for the stream length, and this page follows it; the complexity fields call it $m$. For a support $s$ and an error $\varepsilon < s$, the output must be an $\varepsilon$-*deficient synopsis*: every item with $f_x \ge sN$ is reported, no item with $f_x < (s - \varepsilon) N$ is reported, and each reported estimate is at most $\varepsilon N$ below the true count. This is the $\varepsilon$-approximate [frequent items problem](/frequent-items-problem/), and the estimates also answer [frequency estimation](/frequency-estimation/) queries.

## The algorithm

The table $D$ maps items to pairs $(f, \Delta)$. The current bucket is $b = \lceil N / w \rceil$.

```pseudo id=main
LC-UPDATE(D, x)                          ▷ one occurrence of x
L1  N ← N + 1
L2  b ← ⌈N / w⌉                          ▷ the current bucket
L3  if x ∈ D then D[x].f ← D[x].f + 1
L4  else insert x into D with f = 1 and Δ = b − 1
L5  if N mod w = 0 then                  ▷ the end of bucket b
L6      remove each y ∈ D with D[y].f + D[y].Δ ≤ b

LC-ESTIMATE(D, x)
L7  if x ∈ D then return D[x].f else return 0

LC-REPORT(D, s)                          ▷ the support s must be larger than ε
L8  return each x ∈ D with D[x].f ≥ (s − ε) N
```

The value $f + \Delta$ is an upper bound of the true count, and $f$ is a lower bound. Line L6 removes an item when even its upper bound is at most $b$. A removed item is not lost forever: if it occurs again, line L4 starts a new entry with $\Delta = b - 1$, which covers the count it lost.

**Fast pruning.** Group the entries by the key $f + \Delta$. A new entry has key $b$, and keys only grow. After the pruning at the end of bucket $b - 1$, every key is at least $b$. So line L6 removes exactly the group with key $b$, and the cost of each removal is paid by the insertion of the entry. With a hash table, each update takes $O(1)$ amortized expected time.

## Example

Take $w = 3$, so $\varepsilon = 1/3$, and $\sigma = a, b, a, c, a, b, d, a, b$, with $N = 9$ and three buckets. The table shows $D$ as item $(f, \Delta)$.

| bucket $b$ | items | $D$ before the pruning | removed, as $f + \Delta \le b$ | $D$ after |
|---|---|---|---|---|
| 1 | a, b, a | a (2, 0), b (1, 0) | b, as $1 \le 1$ | a (2, 0) |
| 2 | c, a, b | a (3, 0), c (1, 1), b (1, 1) | c and b, as $2 \le 2$ | a (3, 0) |
| 3 | d, a, b | a (4, 0), d (1, 2), b (1, 2) | d and b, as $3 \le 3$ | a (4, 0) |

The true counts are $f_a = 4$, $f_b = 3$, $f_c = f_d = 1$. The estimate of $a$ is exact. The estimate of $b$ is 0, which is low by exactly $\lfloor 9/3 \rfloor = 3 = \varepsilon N$: the item $b$ appears once in each bucket and is removed at the end of each one. So the bound is tight. With $s = 1/2$, line L8 reports the items with $f \ge (1/2 - 1/3) \cdot 9 = 1.5$, which is only $a$. No item has $f_x \ge sN = 4.5$, and $a$ with $f_a = 4 \ge 1.5$ may be reported.

## Correctness

**Theorem.** After $N$ items, for every item $x$,
$$ f_x - \left\lfloor \frac{N}{w} \right\rfloor \;\le\; \hat f_x \;\le\; f_x, $$
where $\hat f_x$ is the estimate of line L7. Each entry has $f \le f_x \le f + \Delta$. So for $s > \varepsilon$, line L8 reports every item with $f_x \ge sN$ and no item with $f_x < (s - \varepsilon) N$.

The key fact is that an item without an entry has $f_x \le \lfloor N/w \rfloor$, the number of completed buckets. It holds because an entry is removed at the end of bucket $b$ only when its upper bound $f + \Delta$ is at most $b$. When the item comes back in a later bucket $b'$, its earlier count is at most $b' - 1 = \Delta$, so the new entry again has $f_x \le f + \Delta$. And $\Delta \le b - 1 \le \lfloor N / w \rfloor$ for each entry. The full proof is below.

## Complexity

- **Space.** Let $B = \lfloor N / w \rfloor$ be the number of completed buckets. After the pruning at the end of bucket $B$, there are at most $w H_B \le w (1 + \ln B)$ entries, where $H_B = 1 + 1/2 + \cdots + 1/B$. During a bucket, at most $w$ more entries come in. So the space is $O((1/\varepsilon) \log(\varepsilon N))$ entries for $N \ge 2w$, which is the bound of Manku and Motwani. The proof uses the fact that an entry that survives $i$ prunings occurred at least $i$ times in the last $i$ buckets, and only $jw$ items fit in the last $j$ buckets.
- **Time.** $O(1)$ amortized expected time for each item with the grouping by $f + \Delta$. A plain scan of $D$ at each bucket end costs $O(\log(\varepsilon N))$ amortized time for each item.
- **Query.** One lookup for an estimate, and one scan of $D$ for a report.

## Properties

- **Deterministic.** The bound holds on every stream and at every time.
- **One-sided, from below.** Each estimate is at most the true count, and $f + \Delta$ is an upper bound.
- **Not of fixed size.** The table grows like $\log(\varepsilon N)$ in the worst case. Misra-Gries and Space-Saving keep $O(1/\varepsilon)$ counters always.
- **Insertion only.** Deletions break the pruning rule. Use a [linear sketch](/linear-sketch/) such as the [count-min sketch](/count-min-sketch/) for turnstile streams.

## Variants and improvements

- **Frequent item sets.** Manku and Motwani apply the same rule to sets of items in market basket data. They keep $\beta$ buckets of transactions in memory at a time and count the subsets of each transaction in a batch.
- **Sticky sampling.** The randomized method of the same paper, [sticky sampling](/sticky-sampling/), uses a number of entries that does not depend on $N$, at the cost of a failure probability $\delta$.
- **Random data.** Manku and Motwani also show that when the items with very low counts are drawn independently from a fixed distribution, the expected number of entries is at most $7/\varepsilon$.
- **Counters of fixed number.** [Misra-Gries](/misra-gries-summary/) and [Space-Saving](/space-saving/) meet the same guarantee with $O(1/\varepsilon)$ counters in the worst case, and they are mergeable.

## When to use it

Use lossy counting when you want a deterministic $\varepsilon N$ guarantee with both a lower and an upper bound for each counted item, and a simple rule that is easy to apply to item sets. On real data its table is usually small. When a hard limit on memory matters, or when you must merge summaries, use [Space-Saving](/space-saving/) or [Misra-Gries](/misra-gries-summary/).

## Pitfalls

- **Forgetting $\Delta$.** If a new entry starts with $\Delta = 0$, the pruning test becomes $f \le b$. A frequent item that first appears late is then removed at the end of each bucket until it occurs more than $b$ times in one bucket, and its estimate can be low by much more than $\varepsilon N$. Also $f + \Delta$ is then no longer an upper bound.
- **A support at most $\varepsilon$.** With $s \le \varepsilon$, the threshold of line L8 is not positive, and an item with $f_x \ge sN$ can have no entry. The guarantee needs $s > \varepsilon$.
- **Rounding $w$ down.** The bound $\lfloor N/w \rfloor \le \varepsilon N$ needs $w \ge 1/\varepsilon$, so $w = \lceil 1/\varepsilon \rceil$. With a floating point $\varepsilon$ such as $1/3$, compute $w$ from an exact fraction.

## Implementations

## History

Gurmeet Singh Manku and Rajeev Motwani presented lossy counting and sticky sampling at VLDB 2002, for frequency counts and frequent item sets over streams. They proved the space bound of $(1/\varepsilon) \log(\varepsilon N)$ entries. The paper made the $\varepsilon$-deficient synopsis, with support $s$ and error $\varepsilon$, the standard way to state the approximate frequent items problem. Later comparisons by Cormode and Hadjieleftheriou found that Space-Saving is usually faster and smaller in practice.

## References
