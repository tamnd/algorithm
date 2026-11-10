---
tag: C80D8X
kind: data-structure
slug: greenwald-khanna-summary
name: Greenwald-Khanna summary
aliases:
- GK summary
- GK quantile summary
- Greenwald-Khanna quantile summary
area: online-and-streaming/streaming-sketches
level: core
summary: Deterministic quantile summary that keeps sorted tuples (v, g, Δ) with g + Δ ≤ 2εn and answers every rank query within εn, in O((1/ε) log(εn)) tuples.
model: word-ram
complexity:
  vars: {n: the stream length, ε: the rank accuracy, s: the number of stored tuples}
  time: {worst: O(s^2), amortized: O(s + s^2 ε)}
  space: {extra: O((1/ε) log(ε n))}
properties: {online: true, deterministic: true, mergeable: false}
history:
  year: 2001
  people: [Michael Greenwald, Sanjeev Khanna]
  note: Greenwald and Khanna gave the summary at SIGMOD 2001. Assadi, Joshi, Prabhu and Shah gave a simpler form with a complete proof of the space bound in 2023.
prereqs: [quantile-summary-problem, order-statistic, binary-search, streaming-model]
see_also: [kll-sketch, q-digest, t-digest, munro-paterson-algorithm, misra-gries-summary, mergeable-summaries, sliding-window-quantiles, comparison-model]
sources:
  - paper: doi:10.1145/375663.375670
    title: Michael Greenwald and Sanjeev Khanna, Space-efficient online computation of quantile summaries, SIGMOD 2001
    locator: pp. 58 to 66 (the tuples (v, g, Δ), the bands, COMPRESS and the space bound in O((1/ε) log(εn)))
  - url: https://arxiv.org/abs/2303.06288
    title: Sepehr Assadi, Nirmit Joshi, Milind Prabhu and Vihan Shah, Generalizing Greenwald-Khanna streaming quantile summaries for weighted inputs, ICDT 2023
    locator: Section 2 (time steps, band values, Observation 2.8, Invariant 1, Claim 2.1), Section 4 (Algorithm 2, Theorem 2 and Lemma 4.1, the space bound)
  - url: https://arxiv.org/abs/1905.03838
    title: Graham Cormode and Pavel Veselý, A tight lower bound for comparison-based quantile summaries, PODS 2020
    locator: the main theorem (every deterministic comparison-based summary needs Ω((1/ε) log(εn)) items)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Summaries for Ordered Data (the GK summary)
---

The Greenwald-Khanna summary (GK summary) answers rank and quantile queries over a stream with a deterministic error of at most $\varepsilon n$ in rank, where $n$ is the number of items so far. It keeps a sorted list of stream items, and with each item two counts that bound its rank from below and from above. It merges neighbors while the bounds stay tight enough, and keeps $O((1/\varepsilon)\log(\varepsilon n))$ tuples. Cormode and Veselý proved in 2020 that no deterministic comparison-based summary can do better, so the GK summary is optimal in its class. On this page $n$ is the stream length, the stream $\sigma$ is insertion only ([cash register model](/cash-register-model/)), and the items come from any totally ordered set.

## In plain words

You want to know the median, or the value that is larger than 99 percent of the data, but you cannot keep all of the data. The GK summary keeps a short sorted list of values seen so far. For each kept value it remembers how many items lie between it and the kept value before it, and how unsure it is about that count. When two neighbors together stand for few enough items, the summary removes one of them and gives its count to the other. To answer a question about position r, it walks the list and returns a kept value whose position is surely close to r. The answer is never off by more than a fixed fraction of the stream.

## The abstract type

The summary solves the [quantile summary problem](/quantile-summary-problem/) for insertion-only streams. It supports two operations.

- **Insert(x)** adds one item $x$ of the stream.
- **Query(r)**, for $1 \le r \le n$, returns a stored item $v$ whose rank lies within $\varepsilon n$ of $r$.

The rank of an item is its position in the sorted order of the $n$ items. When values repeat, the summary keeps equal values apart by their arrival number, so the rank is the position in the order of (value, arrival number). For a value $v$ that occurs several times, the returned answer is correct when some copy of $v$ has rank in $[r - \varepsilon n, r + \varepsilon n]$. A quantile query for $\phi \in (0, 1]$ is Query($\lceil \phi n \rceil$).

## Representation

The summary stores a list of tuples $e_1, \ldots, e_s$, sorted by value. Tuple $e_i$ holds:

| field | meaning |
|---|---|
| $v_i$ | a stream item |
| $g_i$ | $r_{\min}(e_i) - r_{\min}(e_{i-1})$, the number of items that $e_i$ stands for |
| $\Delta_i$ | $r_{\max}(e_i) - r_{\min}(e_i)$, the uncertainty in the rank of $v_i$ |
| $b_i$ | the band value, a small integer that grows with the age of the tuple |

Here $r_{\min}(e_i) = g_1 + \cdots + g_i$ and $r_{\max}(e_i) = r_{\min}(e_i) + \Delta_i$. The summary also stores $n$, the smallest item $x_{\min}$, and a chunk length $\ell = \lceil 1/(2\varepsilon) \rceil$. The stream is cut into time steps of $\ell$ items, and $t = \lfloor n/\ell \rfloor \le 2\varepsilon n$ is the number of finished steps. Two invariants hold after each operation:

- **(R) rank bounds.** $r_{\min}(e_i) \le \operatorname{rank}(v_i) \le r_{\max}(e_i)$ for each $i$.
- **(C) cap.** $g_i + \Delta_i \le \max(1, t)$ for each $i$, and the last tuple holds the largest item with $\Delta_s = 0$.

## Operations

The form below follows Assadi, Joshi, Prabhu and Shah (Algorithm 2). It is a cleaner form of the original GK algorithm, and the two behave in almost the same way.

```pseudo id=main
GK-INSERT(Q, x)
L1  n ← n + 1; if x < x_min then x_min ← x
L2  i ← the first index with v_i > x
L3  if there is no such i then append (x, 1, 0) with band 0          ▷ a new maximum
L4  else insert (x, 1, g_i + Δ_i − 1) with band 0 just before e_i
L5  if n is a multiple of ℓ then t ← n / ℓ                            ▷ end of a time step
L6      for each tuple from an earlier step: if t is a multiple of 2^b then b ← b + 1
L7      while some e_i with i < s has b_i ≤ b_(i+1) and G*_i + g_(i+1) + Δ_(i+1) ≤ t do
L8          g_(i+1) ← g_(i+1) + G*_i; delete e_i and seg(e_i)

GK-QUERY(Q, r)
L9  if r − εn ≤ 1 then return x_min
L10 j ← the smallest index with r_max(e_j) > r + εn
L11 if there is no such j then return v_s
L12 return v_(j−1)
```

The segment $\mathrm{seg}(e_i)$ is the longest run of tuples just before $e_i$ whose band values are all strictly less than $b_i$, and $G^*_i$ is the sum of the $g$ values of $e_i$ and its segment. Line L8 removes the whole run and moves its count to $e_{i+1}$. So the values $r_{\min}$ of the tuples that stay do not change.

The band value of a tuple is 0 in the step in which it arrives. In each later step $t$, line L6 raises it by one when $t$ is a multiple of $2^b$. So a tuple of age $a$ steps has a band value close to $\log_2 a$. Tuples of a high band are old, and old tuples arrived when the cap $t$ was small, so their $\Delta$ is small. Line L7 merges a tuple only into a neighbor of the same or a higher band, which keeps the small $\Delta$ values alive.

## Example

Take $\varepsilon = 0.1$, so $\ell = 5$, and the stream of 20 items 12, 3, 17, 8, 1 | 15, 6, 10, 4, 14 | 9, 2, 19, 7, 11 | 5, 18, 13, 16, 20, cut into four steps. The table gives the tuples $(v, g, \Delta)$ and the bands after each step, as computed by the implementation.

| after step | $t$ | tuples $(v, g, \Delta)$ | bands |
|---|---|---|---|
| 1 | 1 | (1,1,0) (3,1,0) (8,1,0) (12,1,0) (17,1,0) | 0 0 0 0 0 |
| 2 | 2 | (3,2,0) (4,1,0) (8,2,0) (12,2,0) (14,1,0) (17,2,0) | 1 0 1 1 0 1 |
| 3 | 3 | (3,3,0) (4,1,0) (8,3,0) (9,1,1) (12,3,0) (17,3,0) (19,1,0) | 1 1 1 0 1 1 0 |
| 4 | 4 | (4,4,0) (8,4,0) (12,4,0) (13,1,2) (17,4,0) (19,2,0) (20,1,0) | 2 2 2 0 2 1 0 |

After step 1 the cap is $t = 1$, and no merge is allowed, since any merge gives $g \ge 2$. In step 3 the item 9 arrives when its successor in the list is (12, 2, 0), so line L4 gives it $\Delta = 2 + 0 - 1 = 1$. In step 4 the item 13 gets $\Delta = 3 + 0 - 1 = 2$ in the same way from its successor (17, 3, 0). After 20 items the summary keeps 7 tuples for 20 items, and its minimum is $x_{\min} = 1$.

Query(10): $r - \varepsilon n = 8 > 1$, so line L10 runs with the threshold $r + \varepsilon n = 12$. The values of $r_{\max}$ are 4, 8, 12, 15, 17, 19, 20. The first one above 12 is 15, at the tuple of 13, so line L12 returns the item before it, 12. The true rank of 12 is 12, and $|12 - 10| = 2 = \varepsilon n$. Query(1) returns $x_{\min} = 1$ by line L9, and Query(20) returns 20 by line L11.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts. First, line L4 keeps invariant (R): a new item $x$ lies strictly between $v_{i-1}$ and $v_i$, so its rank is at least $r_{\min}(e_{i-1}) + 1$ and at most $r_{\max}(e_i)$ after the insert, which is what the tuple $(x, 1, g_i + \Delta_i - 1)$ claims. Deletions do not change $r_{\min}$ or $\Delta$ of any tuple that stays. Second, line L4 does not raise the largest value of $g + \Delta$, and line L7 merges only while the result is at most $t$, so invariant (C) holds. Third, with $g_j + \Delta_j \le 2\varepsilon n$, the tuple just before the first $r_{\max}$ above $r + \varepsilon n$ has $r_{\max} \le r + \varepsilon n$ and $r_{\min} = r_{\max}(e_j) - g_j - \Delta_j > r - \varepsilon n$, so its rank is within $\varepsilon n$ of $r$.

## Complexity

**Space.** Each tuple holds one item and three small integers, so the summary takes $O(s)$ words, plus $O(1)$ words for $n$, $x_{\min}$ and $\ell$. Greenwald and Khanna proved $s = O((1/\varepsilon)\log(\varepsilon n))$ for their algorithm. Assadi, Joshi, Prabhu and Shah proved the same bound for the form on this page (Theorem 2 and Lemma 4.1). A sketch of their argument is in the proof file. The proof counts two kinds of tuples that the loop of line L7 cannot delete. A tuple with a higher band than its right neighbor is of type 1, and there are $O(\ell)$ of them for each band value. A tuple whose merge would break the cap is of type 2; it stands for many items of a recent band, and there are again $O(\ell)$ of them for each band. There are $O(\log t)$ band values, so $s = O(\ell \log t) = O((1/\varepsilon)\log(\varepsilon n))$. The tests check $s \le (1/\varepsilon)\log_2(2\varepsilon n) + 2$ on sorted and random streams with $n$ up to 6000. In those runs $s$ was 15 to 42 for $\varepsilon = 0.05$ and $0.02$.

**Lower bound.** Cormode and Veselý (2020) proved that each deterministic comparison-based summary that answers all rank queries within $\varepsilon n$ must store $\Omega((1/\varepsilon)\log(\varepsilon n))$ items. So the GK summary is optimal among deterministic comparison-based summaries. The [quantile summary problem](/quantile-summary-problem/) page gives the other bounds.

**Time.** Line L2 is a [binary search](/binary-search/), $O(\log s)$ comparisons. With a sorted array, line L4 moves $O(s)$ words. Lines L6 to L8 run once every $\ell$ items. The simple scan in the implementation repeats passes over the list until no merge applies, which costs $O(s^2)$ in the worst case, so $O(s^2/\ell) = O(s^2 \varepsilon)$ amortized per item. Assadi et al. give an implementation with $O(\log(1/\varepsilon) + \log\log(\varepsilon n))$ worst-case time per update (Theorem 2). A query is one scan of $O(s)$ steps, or $O(\log s)$ with stored prefix sums.

## Variants

- **The original GK algorithm.** Greenwald and Khanna insert each item, and run COMPRESS every $\lfloor 1/(2\varepsilon) \rfloor$ items. COMPRESS merges a tuple and its descendants in a tree of bands. The rule here is the same in effect.
- **Greedy GK.** Merge any tuple whose merge keeps $g + \Delta \le t$, with no bands and no segments. Assadi et al. prove $O((1/\varepsilon)\log^2(\varepsilon n))$ tuples for a greedy rule with bands (their Algorithm 1). The plain greedy rule, often called GKAdaptive, works well in practice but has no proven bound of $O((1/\varepsilon)\log(\varepsilon n))$.
- **Weighted streams.** Assadi et al. extend the summary to items with weights.
- **Sliding windows.** See [sliding window quantiles](/sliding-window-quantiles/) for summaries of the last $W$ items.
- **Randomized summaries.** The [KLL sketch](/kll-sketch/) keeps $O((1/\varepsilon)\log\log(1/\delta))$ items and is mergeable, but its guarantee holds with probability $1 - \delta$.

## When to use it

Use the GK summary when you need a deterministic guarantee on every query, the stream fits in one process, and items arrive one by one. It works for any ordered type, since it only compares items. If you must merge summaries from many machines, use the [KLL sketch](/kll-sketch/) or the [q-digest](/q-digest/): GK summaries are not known to be fully mergeable with the same space (see [mergeable summaries](/mergeable-summaries/)). If the values are integers from a small universe and you want a simple tree, the [q-digest](/q-digest/) is an option.

## Pitfalls

- **Return a value from the right side of the gap.** The query returns the tuple just before the first $r_{\max}$ above $r + \varepsilon n$. Returning the first tuple with $r_{\min} \ge r$ can miss by up to $2\varepsilon n$.
- **Keep the minimum apart.** Merges can remove the first tuple, so the first stored value may not be the minimum. Without $x_{\min}$, queries with small $r$ can fail when the first tuple has a large $g$.
- **Never delete the last tuple.** It holds the maximum with $\Delta = 0$, and queries for large $r$ rely on it.
- **Ties.** With repeated values, place a new copy after the equal values (the order by arrival number). Then invariant (R) holds for each copy, and the test for a correct answer uses the range of ranks of the value.
- **The cap.** The merge test must use $t = \lfloor n/\ell \rfloor$, not $2\varepsilon n$, at the time of the merge, so that the cap never exceeds $2\varepsilon n$ later.
- **Mid-step queries.** A query between two compressions is still correct, because insertion never raises the largest $g + \Delta$.

## Implementations

## History

Munro and Paterson (1980) gave multi-pass selection with small memory and, as a one-pass by-product, approximate quantiles; see the [Munro-Paterson algorithm](/munro-paterson-algorithm/). Manku, Rajagopalan and Lindsay (1998) built on it a one-pass summary with $O((1/\varepsilon)\log^2(\varepsilon n))$ space that needs $n$ in advance. Greenwald and Khanna (2001) gave the first deterministic summary with $O((1/\varepsilon)\log(\varepsilon n))$ space and no knowledge of $n$. Their space proof was long, and Assadi, Joshi, Prabhu and Shah (2023) gave a shorter one for the form on this page. Cormode and Veselý (2020) proved the matching lower bound for comparison-based summaries.

## References
