---
tag: 3PR4D2
kind: algorithm
slug: space-saving
name: Space-Saving algorithm
aliases:
- Metwally-Agrawal-El Abbadi algorithm
- SpaceSaving
- Stream-Summary algorithm
area: online-and-streaming/streaming-sketches
level: core
summary: Replaces the minimum counter on overflow, overestimating counts with a bounded error.
solves: [frequent-items-problem, frequency-estimation]
model: streaming-model
complexity:
  vars: {m: the stream length, k: the number of counters}
  time: {expected: O(1)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [frequent-items-problem, frequency-vector, cash-register-model, misra-gries-summary]
see_also: [lossy-counting, count-min-sketch, mergeable-summaries, boyer-moore-majority, sliding-window-heavy-hitters, frequency-estimation, sample-and-hold]
sources:
  - paper: doi:10.1007/978-3-540-30570-5_27
    title: Ahmed Metwally, Divyakant Agrawal and Amr El Abbadi, Efficient computation of frequent and top-k elements in data streams, ICDT 2005, LNCS 3363
    locator: pages 398 to 412, the Space-Saving algorithm, the Stream-Summary structure, and the bound of m/k on the error of each counter
  - paper: doi:10.1145/2500128
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, ACM Transactions on Database Systems 38(4), 2013 (conference version PODS 2012)
    locator: Section 2, the isomorphism between SpaceSaving with k counters and Misra-Gries with k - 1 counters, and the merge
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the SpaceSaving summary)
---

The Space-Saving algorithm keeps $k$ items with counters and answers frequency queries on an insertion-only stream. When a new item arrives and all counters are in use, it takes over the smallest counter and adds one to it. After $m$ items, with $\mu$ the smallest counter, each estimate satisfies $f_x \le \hat f_x \le f_x + \mu \le f_x + m/k$. So the estimates are never too small, and each item with more than $m/k$ occurrences has a counter. The algorithm is deterministic, uses $\Theta(k)$ words, and with the Stream-Summary structure it takes $O(1)$ expected time for each item. It is a solution of the $\varepsilon$-approximate [frequent items problem](/frequent-items-problem/) with $k = \lceil 1/\varepsilon \rceil$, and its state is the [Misra-Gries summary](/misra-gries-summary/) with $k - 1$ counters, shifted by $\mu$.

## In plain words

You have $k$ boxes, each with a name and a tally. When an item arrives and its name is on a box, add one to that tally. When it is new and a box is free, write its name on the free box with a tally of one.

When it is new and all boxes are full, find the box with the smallest tally. Erase the old name, write the new name, and add one to the tally. The new item now carries the tally of the item it replaced, so its tally can be too large, but never too small.

The tallies always add up to the number of items seen. So the smallest of $k$ tallies is at most the stream length divided by $k$, and no tally is too large by more than that.

## The problem

The input is a stream $\sigma = a_1, \ldots, a_m$ of items from a universe of size $n$, in the [cash register model](/cash-register-model/). Let $f_x$ be the count of $x$, the entry of the [frequency vector](/frequency-vector/). The summary must answer the query "estimate $f_x$" for any $x$ at any time, with an additive error of at most $m/k$. As a consequence it can report at most $k$ candidates that contain every item with $f_x > m/k$, and it gives a top-$j$ list ordered by the estimates. This is the deterministic, counter-based answer to the [frequent items problem](/frequent-items-problem/) and to [frequency estimation](/frequency-estimation/).

## The algorithm

The summary is a table $T$ of at most $k$ items, each with a counter $T[x]$ and an error $\epsilon[x]$, and the length $m$. Let $\mu$ be the smallest counter in $T$ when $|T| = k$, and $\mu = 0$ when $|T| < k$.

```pseudo id=main
SS-UPDATE(T, x)                          ▷ one occurrence of x
L1  m ← m + 1
L2  if x ∈ T then
L3      T[x] ← T[x] + 1
L4  else if |T| < k then
L5      T[x] ← 1;  ε[x] ← 0
L6  else y ← an item of T with the smallest counter;  μ ← T[y]
L7      remove y from T
L8      T[x] ← μ + 1;  ε[x] ← μ             ▷ x takes over the counter of y

SS-ESTIMATE(T, x)
L9  if x ∈ T then return T[x]
L10 else return μ                        ▷ 0 while |T| < k
```

The error $\epsilon[x]$ records the counter that $x$ took over, so $T[x] - \epsilon[x]$ is a lower bound of $f_x$. To find the smallest counter in $O(1)$ time, Metwally, Agrawal and El Abbadi keep the **Stream-Summary** structure: a sorted linked list of buckets, one for each distinct counter value, each with the items that have this value. An increment moves an item from its bucket to the next value, which is the next bucket or a new one, so each line of SS-UPDATE takes $O(1)$ time with a hash table from items to their buckets.

**Merge.** Two summaries with the same $k$ merge through the isomorphism of the Correctness section. Map each one to its Misra-Gries summary, $T[x] - \mu$ for the items with $T[x] > \mu$. Merge these two with MG-MERGE of the [Misra-Gries summary](/misra-gries-summary/), which gives counters $C$ for the combined length $m = m_1 + m_2$. Then put back $D = \lfloor (m - \sum_y C[y]) / k \rfloor$: the merged estimate is $C[x] + D$ for $x \in C$ and $D$ for other items.

## Example

Take $k = 3$ and $\sigma = a, b, a, c, a, b, d, a, b$, with $m = 9$. The same stream is the example of the [Misra-Gries summary](/misra-gries-summary/) with 2 counters.

| $t$ | $a_t$ | line | $T$ after the step, as item: counter | $\mu$ |
|---|---|---|---|---|
| 1 | a | L5 | a: 1 | 0 |
| 2 | b | L5 | a: 1, b: 1 | 0 |
| 3 | a | L3 | a: 2, b: 1 | 0 |
| 4 | c | L5 | a: 2, b: 1, c: 1 | 1 |
| 5 | a | L3 | a: 3, b: 1, c: 1 | 1 |
| 6 | b | L3 | a: 3, b: 2, c: 1 | 1 |
| 7 | d | L6 to L8 | a: 3, b: 2, d: 2 with $\epsilon[d] = 1$ | 2 |
| 8 | a | L3 | a: 4, b: 2, d: 2 | 2 |
| 9 | b | L3 | a: 4, b: 3, d: 2 | 2 |

The counters add up to $9 = m$. The true counts are $f_a = 4$, $f_b = 3$, $f_c = 1$ and $f_d = 1$. The estimates are $\hat f_a = 4$, $\hat f_b = 3$, $\hat f_d = 2$, and $\hat f_c = \mu = 2$. Each one is at least the true count and too large by at most $\mu = 2 \le m/k = 3$. The lower bound for $d$ is $T[d] - \epsilon[d] = 1$, which is exact. If we subtract $\mu = 2$ from each counter and keep the positive ones, we get $\{a: 2, b: 1\}$, which is the final Misra-Gries summary of the same stream.

## Correctness

**Theorem.** After $m$ updates, $\sum_x T[x] = m$, and for every item $x$,
$$ f_x \;\le\; \hat f_x \;\le\; f_x + \mu \;\le\; f_x + \frac{m}{k} . $$
For each $x \in T$, also $T[x] - \epsilon[x] \le f_x$. So each item with $f_x > m/k$ is in $T$.

Each update adds exactly 1 to the sum of the counters: line L3 and line L5 add 1, and lines L6 to L8 remove a counter $\mu$ and add a counter $\mu + 1$. When the table is full, the $k$ counters are each at least $\mu$ and add up to $m$, so $k\mu \le m$. The smallest counter never falls, because counters only grow and the one that is removed is replaced by a larger one. An item $x$ that is not in $T$ has $f_x \le \mu$: when it was removed, its true count was at most its counter, which was the smallest one, and $\mu$ has not fallen since. So when $x$ takes over a counter in line L8, its new counter $\mu + 1$ is at least its new true count, and its counter is too large by at most $\epsilon[x] = \mu$. The full proof is below.

**Isomorphism with Misra-Gries.** Run the [Misra-Gries summary](/misra-gries-summary/) with $k - 1$ counters on the same stream. Then after each item, its counters are exactly $\max(T[x] - \mu, 0)$, and its number of decrement steps is exactly $\mu$ (Agarwal et al. 2012). The proof checks four cases of SS-UPDATE, and it shows that a Misra-Gries decrement step happens exactly when $\mu$ grows by one. So the Space-Saving estimate is the Misra-Gries estimate plus the number of decrement steps, and the two summaries hold the same information. This gives the merge and its bound $D \le m/k$.

## Complexity

- **Space.** At most $k$ items, $k$ counters, $k$ errors, and $m$. That is $\Theta(k)$ words.
- **Update.** With Stream-Summary and a hash table, each update is $O(1)$ expected time, or $O(1)$ worst-case time with a dictionary that has worst-case $O(1)$ operations. A binary heap on the counters gives $O(\log k)$. A linear scan for the smallest counter gives $O(k)$.
- **Query.** One lookup, and $\mu$ is the first bucket of Stream-Summary.
- **Top $j$.** The buckets are sorted, so the $j$ largest counters are at the end of the list, in $O(j)$ time.
- **Merge.** $O(k)$ with a selection of the $k$-th largest counter, or $O(k \log k)$ with a sort.

## Properties

- **Deterministic.** There are no random choices, and the bound holds on every stream and at every time.
- **One-sided, from above.** Each estimate is an upper bound of the true count, and $T[x] - \epsilon[x]$ is a lower bound. Misra-Gries gives only the lower bound.
- **Exact while small.** While at most $k$ distinct items have arrived, all counters are exact.
- **Insertion only.** A deletion cannot be undone after a counter is taken over. For the [turnstile model](/turnstile-model/), use the [count-min sketch](/count-min-sketch/) or the [count sketch](/count-sketch/).
- **Mergeable.** Through the isomorphism, the summary is one of the [mergeable summaries](/mergeable-summaries/).

## Variants and improvements

- **Weighted updates.** An update $(x, w)$ with $w > 0$ adds $w$ to $T[x]$, or takes over the smallest counter $\mu$ and sets it to $\mu + w$. The same proof gives the error bound $W/k$, where $W$ is the total weight. With weights, Stream-Summary no longer gives $O(1)$ time, and a heap gives $O(\log k)$.
- **Guaranteed top-$k$.** Metwally, Agrawal and El Abbadi use the lower bounds $T[x] - \epsilon[x]$ to tell when the reported top-$j$ list is certainly correct: an item is certainly in the top $j$ when its lower bound is at least the $(j+1)$-th largest counter.
- **Tail bounds.** The bound of Berinde, Cormode, Indyk and Strauss (2009) also holds here: the error is at most $F_1^{\mathrm{res}(j)}/(k - j)$ for each $j < k$, where $F_1^{\mathrm{res}(j)}$ is the total count without the $j$ largest counts. On skewed streams this is much less than $m/k$.
- **Unbiased Space-Saving.** Ting (2018) replaces the label of the smallest counter only with probability $1/(\mu + 1)$. Then each estimate is unbiased, which helps when you sum estimates over a subset of items.
- **Sliding windows.** For heavy hitters in the most recent items only, see [sliding-window heavy hitters](/sliding-window-heavy-hitters/).

## When to use it

Use Space-Saving for heavy hitters and top-$k$ lists on an insertion-only stream, when you want a deterministic guarantee, estimates that never miss an occurrence, and $O(1)$ time for each item. It is the summary that experimental studies of frequent items most often recommend for insertion-only data. Use the [Misra-Gries summary](/misra-gries-summary/) when one fewer counter matters or a lower bound is what you need. Use a sketch such as the [count-min sketch](/count-min-sketch/) when items can be deleted.

## Pitfalls

- **Returning 0 for an item without a counter.** The upper bound needs $\hat f_x = \mu$ for items not in $T$. An item can occur up to $\mu$ times without a counter, so 0 is not an upper bound.
- **Reading counters as counts.** In the example, $d$ has counter 2 but occurs once. Use $T[x] - \epsilon[x]$ when you need a value that is certainly not too large.
- **Scanning for the smallest counter.** A linear scan makes each update $O(k)$. That is fine for small $k$, but it loses the main practical advantage. Keep Stream-Summary or a heap.
- **Using $k$ counters with the bound $m/(k+1)$.** With $k$ counters the bound is $m/k$, one counter more than Misra-Gries needs for the same bound.
- **Merging by adding counters.** If an item has a counter in one summary only, its estimate in the other summary is that summary's $\mu$, not 0. A merge that adds counters and keeps the $k$ largest ignores this, and the merged estimate is then not an upper bound. The merge through Misra-Gries above has a proof.

## Implementations

## History

Ahmed Metwally, Divyakant Agrawal and Amr El Abbadi presented Space-Saving and the Stream-Summary structure at ICDT 2005, for frequent items and top-$k$ queries over click streams in Internet advertising. In 2008, a comparison of frequent items algorithms by Cormode and Hadjieleftheriou found it among the most accurate and fastest of them on insertion-only streams. In 2012, Agarwal, Cormode, Huang, Phillips, Wei and Yi showed that it is isomorphic to the much older [Misra-Gries summary](/misra-gries-summary/) of 1982, and so that it is mergeable.

## References
