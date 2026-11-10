---
tag: 6P4C0W
kind: algorithm
slug: misra-gries-summary
name: Misra-Gries summary
aliases:
- Frequent algorithm
- Misra-Gries frequent items
- MG summary
area: online-and-streaming/streaming-sketches
level: core
summary: Keeps k-1 counters and decrements all on collision, underestimating counts by at most n/k.
solves: [frequent-items-problem, frequency-estimation]
model: streaming-model
complexity:
  vars: {m: the stream length, k: "the parameter, so k - 1 counters"}
  time: {worst: O(k), amortized: O(1)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [boyer-moore-majority, frequent-items-problem, frequency-vector, cash-register-model]
see_also: [space-saving, lossy-counting, count-min-sketch, mergeable-summaries, majority-element-problem, sliding-window-heavy-hitters, frequency-estimation]
sources:
  - paper: doi:10.1016/0167-6423(82)90012-0
    title: Jayadev Misra and David Gries, Finding repeated elements, Science of Computer Programming 2(2), 1982
    locator: pages 143 to 152, the algorithm with k - 1 counters and the proof that every item with more than m/k occurrences keeps a counter
  - paper: doi:10.1145/2500128
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, ACM Transactions on Database Systems 38(4), 2013 (conference version PODS 2012)
    locator: Section 2 (the merge of two MG summaries by subtracting the k-th largest counter, and the isomorphism with SpaceSaving)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the Misra-Gries summary)
  - paper: "Richard M. Karp, Scott Shenker and Christos H. Papadimitriou, A simple algorithm for finding frequent elements in streams and bags, ACM Transactions on Database Systems 28(1), 2003, pages 51 to 55"
    locator: the rediscovery of the algorithm, with O(1) time for each item
---

The Misra-Gries summary keeps at most $k - 1$ items with counters and answers frequency queries on an insertion-only stream. After $m$ items, its estimate $\hat f_x$ of the count of each item $x$ satisfies $f_x - m/k \le \hat f_x \le f_x$, so each item with more than $m/k$ occurrences keeps a counter. It is deterministic, uses $\Theta(k)$ words, and takes $O(1)$ amortized time for each item. It solves the $\varepsilon$-approximate [frequent items problem](/frequent-items-problem/) with $k = \lceil 1/\varepsilon \rceil$, and it generalizes the [Boyer-Moore majority vote](/boyer-moore-majority/), which is the case $k = 2$.

## In plain words

You have a few boxes, each with a name and a tally. When an item arrives and its name is on a box, add one to that tally. When it is new and a box is free, write its name on the free box with a tally of one.

When it is new and all boxes are full, take one from every tally, and throw the new item away too. Empty any box whose tally drops to zero. Each such step removes several items at the same time, one from each box and the new one. So such steps cannot happen often, and a name that arrives very often always keeps its box.

A tally is never too large. It is too small by at most the number of these removal steps.

## The problem

The input is a stream $\sigma = a_1, \ldots, a_m$ of items from a universe of size $n$, in the [cash register model](/cash-register-model/): each item adds 1 to its count. Let $f_x$ be the count of $x$, the entry of the [frequency vector](/frequency-vector/). The summary must answer a query "estimate $f_x$" for any $x$ at any time, with an additive error of at most $m/k$. As a consequence it can report a list of at most $k - 1$ candidates that contains every item with $f_x > m/k$. This is the deterministic, counter-based answer to the [frequent items problem](/frequent-items-problem/) and to [frequency estimation](/frequency-estimation/).

## The algorithm

The summary is a dictionary $C$ from items to positive counters, with $|C| \le k - 1$, and the length $m$.

```pseudo id=main
MG-UPDATE(C, x)                          ▷ one occurrence of x
L1  m ← m + 1
L2  if x ∈ C then C[x] ← C[x] + 1
L3  else if |C| < k − 1 then C[x] ← 1
L4  else for each y ∈ C do               ▷ |C| = k − 1 and x is new
L5          C[y] ← C[y] − 1
L6          if C[y] = 0 then remove y from C

MG-ESTIMATE(C, x)
L7  if x ∈ C then return C[x] else return 0

MG-MERGE(C1, C2)                         ▷ two summaries with the same k
L8  C ← C1 + C2                          ▷ add the counters of equal items
L9  if |C| ≥ k then
L10     c ← the k-th largest counter of C
L11     subtract c from each counter, and remove each counter that is not positive
L12 return C
```

Lines L4 to L6 are the *decrement step*. It lowers all $k - 1$ counters by one and drops the arriving item, so it removes $k$ units of count in total. This is the key to the bound. A merge adds the two dictionaries, which can give up to $2k - 2$ counters, and then cuts them back to at most $k - 1$ by subtracting the $k$-th largest counter. The merge is from Agarwal et al. (2012).

## Example

Take $k = 3$, so 2 counters, and $\sigma = a, b, a, c, a, b, d, a, b$, with $m = 9$.

| $t$ | $a_t$ | line | $C$ after the step | $m - \sum C$ |
|---|---|---|---|---|
| 1 | a | L3 | a: 1 | 0 |
| 2 | b | L3 | a: 1, b: 1 | 0 |
| 3 | a | L2 | a: 2, b: 1 | 0 |
| 4 | c | L4 to L6 | a: 1 | 3 |
| 5 | a | L2 | a: 2 | 3 |
| 6 | b | L3 | a: 2, b: 1 | 3 |
| 7 | d | L4 to L6 | a: 1 | 6 |
| 8 | a | L2 | a: 2 | 6 |
| 9 | b | L3 | a: 2, b: 1 | 6 |

The true counts are $f_a = 4$, $f_b = 3$, $f_c = 1$ and $f_d = 1$. There were 2 decrement steps, so each estimate is low by at most 2, which is at most $m/k = 3$. Here $\hat f_a = 2$ and $\hat f_b = 1$ are both low by exactly 2, and $\hat f_c = \hat f_d = 0$.

**A merge.** With $k = 3$, the stream $a, a, a, b$ gives $C_1 = \{a: 3, b: 1\}$ and the stream $b, b, c, c$ gives $C_2 = \{b: 2, c: 2\}$. Line L8 gives $\{a: 3, b: 3, c: 2\}$. This has $3 = k$ counters, and the third largest is $c = 2$, so line L11 gives $\{a: 1, b: 1\}$. The true counts of the concatenation are $f_a = 3$, $f_b = 3$ and $f_c = 2$, with $m = 8$. Each error is at most $(8 - 2)/3 = 2$.

## Correctness

**Theorem.** After any sequence of updates and merges that produces a summary of a stream of length $m$, for every item $x$,
$$ f_x - \frac{m - \sum_y C[y]}{k} \;\le\; \hat f_x \;\le\; f_x, \qquad\text{so}\qquad f_x - \frac{m}{k} \le \hat f_x \le f_x . $$

The invariant is that the *slack* $m - \sum_y C[y]$ grows by at least $k$ each time any single estimate can fall by 1. In an update, the slack grows by 0 in lines L2 and L3, and by exactly $k$ in a decrement step, while each estimate falls by at most 1. In a merge, the slacks add, and line L11 lowers each estimate by at most $c$ while it removes at least $kc$ from the sum, because the $k$ largest counters each lose $c$. So $k(f_x - \hat f_x)$ is at most the slack, and the slack is at most $m$ because the counters are not negative. The full proof, with the merge, is below.

An item with $f_x > m/k$ has $\hat f_x > 0$, so it is in $C$. With $k = \lceil 1/\varepsilon \rceil$, the error is at most $\varepsilon m$.

## Complexity

- **Space.** At most $k - 1$ items and $k - 1$ counters, plus $m$. That is $\Theta(k)$ words, or $O(k(\log n + \log m))$ bits.
- **Update, worst case.** A decrement step touches all $k - 1$ counters, so $O(k)$ time.
- **Update, amortized.** Each decrement step lowers $k - 1$ counters by 1. A counter unit that is removed was added by an earlier update, and each update adds at most 1. So over $m$ updates there are at most $m/(k-1)$ decrement steps, of cost $O(k)$ each, and the total time is $O(m)$. The amortized time is $O(1)$ for each item. This counts a dictionary operation as $O(1)$, which holds in expectation for a hash table with [universal hashing](/universal-hashing/). Demaine, López-Ortiz and Munro, and Karp, Shenker and Papadimitriou, gave structures with $O(1)$ worst-case time for each item.
- **Query.** One dictionary lookup.
- **Merge.** $O(k)$ for the sum and a [selection](/median-of-medians/) of the $k$-th largest counter, or $O(k \log k)$ with a sort.

## Properties

- **Deterministic.** There are no random choices, and the bound holds on every stream and at every time.
- **One-sided.** Each estimate is a lower bound of the true count.
- **Insertion only.** A deletion cannot be undone once a decrement step has removed counts. For the [turnstile model](/turnstile-model/), use a sketch such as the [count-min sketch](/count-min-sketch/).
- **Mergeable.** Two summaries with the same $k$ merge into one with the same guarantee for the combined stream, so the summary is one of the [mergeable summaries](/mergeable-summaries/).

## Variants and improvements

- **Space-Saving.** [Space-Saving](/space-saving/) with $k$ counters replaces the smallest counter instead of decrementing all. Its counters minus its smallest counter are exactly the Misra-Gries counters with $k - 1$ counters (Agarwal et al. 2012). So it gives upper bounds where Misra-Gries gives lower bounds.
- **Lossy counting.** [Lossy counting](/lossy-counting/) gets the same one-sided error with a different rule, pruning at fixed times, and uses $O((1/\varepsilon) \log(\varepsilon m))$ entries in the worst case.
- **Tail bounds.** Berinde, Cormode, Indyk and Strauss (2009) showed that the error of each estimate is also at most $F_1^{\mathrm{res}(j)}/(k - j)$ for each $j < k$, where $F_1^{\mathrm{res}(j)}$ is the total count without the $j$ largest counts. So the summary is much better than $m/k$ on skewed streams.
- **Second pass.** On stored data, a second pass that counts the $k - 1$ candidates exactly gives the exact list of items with $f_x > m/k$.
- **Weighted updates.** An update $(x, w)$ with $w > 0$ can be done in one step: add $w$, and if the table overflows, subtract the smallest counter as in a merge.

## When to use it

Use it for heavy hitters on an insertion-only stream when you want a deterministic guarantee and the smallest state: $k - 1$ counters for error $m/k$, with no hash functions. Use [Space-Saving](/space-saving/) instead when you want estimates that are never too small, or a top-$k$ list in order. Use the [count-min sketch](/count-min-sketch/) or the [count sketch](/count-sketch/) when items can be deleted, or when you want a linear sketch that you can subtract.

## Pitfalls

- **Counting the arrival in a decrement step.** In line L4 the new item is dropped. Code that also inserts it with count 1 when the decrement frees a counter breaks the "removes $k$ units" argument. The bound then fails: with $k = 3$ and $\sigma = a, a, b, c, b$, that code ends with $\{b: 1\}$, so $\hat f_a = 0$ while $f_a = 2 > m/k = 5/3$.
- **Using $k$ counters with the bound $m/k$.** With $k$ counters the bound is $m/(k+1)$. Mixing the two conventions gives a wrong threshold for reporting. This page uses $k - 1$ counters and the bound $m/k$, as Misra and Gries did.
- **Reporting candidates as heavy hitters.** The list of line L7 holds every item with $f_x > m/k$, but it can also hold light items. Report only items with $\hat f_x \ge (\phi - \varepsilon) m$, or check them in a second pass.
- **Merging by keeping the $k - 1$ largest sums.** Without the subtraction of line L11, the dropped counters are lost without a matching increase of the slack, and after a few merges the error can exceed $m/k$. With $k = 4$, the parts $0, 1, 0, 3, 1, 0, 5$, then $3, 5$, then $5, 3, 4, 1, 5$, merged in that order this way, give $\hat f_5 = 0$ while $f_5 = 4 > 14/4$.

## Implementations

## History

Jayadev Misra and David Gries published the algorithm in 1982 in *Finding repeated elements*, as the generalization of the majority vote of Boyer and Moore to the items that occur more than $m/k$ times. Twenty years later it was found again for network streams by Demaine, López-Ortiz and Munro (2002), who called it Frequent, and by Karp, Shenker and Papadimitriou (2003), both with $O(1)$ time for each item. Agarwal, Cormode, Huang, Phillips, Wei and Yi showed in 2012 that the summary is mergeable with no growth in error, and that it is isomorphic to Space-Saving.

## References
