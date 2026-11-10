---
tag: XJNY1D
kind: concept
slug: mergeable-summaries
name: Mergeable summaries
aliases:
- mergeable sketches
- distributed sketches
- mergeability
area: online-and-streaming/streaming-sketches
level: core
summary: Summaries of disjoint streams that combine into a summary of their union.
prereqs: [streaming-model, epsilon-delta-guarantee, misra-gries-summary]
see_also: [linear-sketch, misra-gries-summary, space-saving, kll-sketch, hyperloglog, kmv-sketch, reservoir-sampling, coreset]
sources:
  - paper: doi:10.1145/2213556.2213562
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, PODS 2012
    locator: pp. 23 to 34 (Section 1.1, the definition; Section 2, heavy hitters; Section 3, quantiles)
  - paper: doi:10.1145/2500128
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, ACM Transactions on Database Systems 38(4), 2013
    locator: Article 26 (the journal version)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1 (the operations of a summary, including merge)
---

A summary is mergeable if two summaries of two data sets can be combined into a summary of the union of the data sets, with the same size bound and the same error bound as each input. Agarwal, Cormode, Huang, Phillips, Wei and Yi (2012) made this precise: the error must not grow with the number of merges, for any order and any tree of merges. A mergeable summary can be computed in parallel on many machines, and the parts can be combined in any way. [Linear sketches](/linear-sketch/) merge by addition, [HyperLogLog](/hyperloglog/) by a maximum per register, the [KMV sketch](/kmv-sketch/) by the smallest values of a union, and the [Misra-Gries summary](/misra-gries-summary/) by a sum of counters followed by a subtraction. On this page $n$ is the total size of the data, and $\varepsilon$ is the error parameter.

## In plain words

Many machines each see a part of the data, and each one keeps a small summary of its part. You want a summary of all the data, but you do not want to send the data. A summary is mergeable when you can combine two summaries into one summary of both parts, and the result is as small and as accurate as if one machine had seen both parts from the start. Then you can combine the summaries in pairs, in a chain or in any other order, and the final summary is still good. A sum or a maximum is mergeable in this way. Many approximate summaries are too, but each needs its own combine rule.

## The idea

**Definition (Agarwal et al. 2012).** Let $S(D, \varepsilon)$ be a summary of a multiset $D$ with error parameter $\varepsilon$. The summary is mergeable if there is an algorithm that, from any $S(D_1, \varepsilon)$ and $S(D_2, \varepsilon)$, produces a valid $S(D_1 \uplus D_2, \varepsilon)$. Three points are part of the definition.

- **The error does not grow.** The output has the same $\varepsilon$ as the inputs, not $2\varepsilon$ or $\varepsilon + \varepsilon'$.
- **The size does not grow.** The output obeys the same size bound as the inputs, as a function of $\varepsilon$ (and at most polylogarithmic in $n$).
- **Any merge tree.** The merges can form any binary tree over the parts, with the parts of any size. For a randomized summary, the error bound holds with the stated probability for every merge tree that is fixed in advance.

A streaming update is a merge with a summary of one item. So a mergeable summary is also a streaming summary, but the converse is false: a streaming summary may need its input one item at a time.

**Exact mergeable summaries.** Count, sum, minimum and maximum merge exactly. The mean merges as the pair (sum, count). The variance merges as the triple $(n, \mu, M)$ with $M = \sum (x - \mu)^2$: for parts $a$ and $b$, with $\Delta = \mu_b - \mu_a$,
$$n = n_a + n_b, \quad \mu = \mu_a + \Delta\,\frac{n_b}{n}, \quad M = M_a + M_b + \Delta^2\,\frac{n_a n_b}{n}.$$
The last identity follows from $\sum_{x \in a}(x - \mu)^2 = M_a + n_a(\mu_a - \mu)^2$, the same for $b$, and $n_a(\mu_a - \mu)^2 + n_b(\mu_b - \mu)^2 = \Delta^2 n_a n_b/n$.

**Misra-Gries is mergeable (proved here).** A Misra-Gries summary with $k$ counters keeps estimates $\hat f_i \le f_i$ (with $\hat f_i = 0$ for items without a counter). Let $\hat n = \sum_i \hat f_i$ be the sum of its counters. The invariant is
$$0 \le f_i - \hat f_i \le \frac{n - \hat n}{k + 1} \quad \text{for each item } i.$$
The merge rule is: add the two sets of counters item by item, giving at most $2k$ counters; let $C$ be the $(k+1)$-th largest counter, or 0 if there are at most $k$; subtract $C$ from each counter and drop the counters that are not positive.

*Proof that the invariant holds after a merge.* Let the inputs have sizes $n_1, n_2$, counter sums $\hat n_1, \hat n_2$ and errors $e_1(i), e_2(i)$ that satisfy the invariant. After the addition, the error of item $i$ is $e_1(i) + e_2(i)$. The subtraction lowers each estimate by at most $C$, so the new error is at most $e_1(i) + e_2(i) + C$, and estimates stay at most $f_i$. At least $k + 1$ counters are $C$ or more, and each of them loses $C$, so the new counter sum is $\hat n \le \hat n_1 + \hat n_2 - (k+1)C$. Then
$$f_i - \hat f_i \le \frac{n_1 - \hat n_1}{k+1} + \frac{n_2 - \hat n_2}{k+1} + C \le \frac{n_1 + n_2 - \hat n}{k+1}.$$
At most $k$ counters remain. A summary of one item is exact and satisfies the invariant, so every merge tree gives $0 \le f_i - \hat f_i \le n/(k+1)$, and $k = \lceil 1/\varepsilon \rceil$ gives error $\varepsilon n$. $\square$

The same paper shows that [SpaceSaving](/space-saving/) is mergeable, through a correspondence with Misra-Gries, and gives randomized mergeable summaries for quantiles and for $\varepsilon$-approximations of range spaces.

## Examples

**Misra-Gries, $k = 2$.** The first part is the stream $a, a, a, b$, with summary $\{a{:}3, b{:}1\}$. The second part is $c, c, b$, with summary $\{c{:}2, b{:}1\}$. Both are exact, since each part has at most 2 distinct items.

| step | counters | counter sum |
|---|---|---|
| add item by item | $a{:}3$, $b{:}2$, $c{:}2$ | 7 |
| $C$ = third largest | 2 | |
| subtract and drop | $a{:}1$ | 1 |

The bound is $(n - \hat n)/(k+1) = (7 - 1)/3 = 2$. The true counts are $a{:}3$, $b{:}2$, $c{:}2$, and each error is exactly 2, so the bound is tight here.

**HyperLogLog.** Two sketches with the same hash and the same number of registers merge by the maximum of each register: $[3, 1, 0, 2]$ and $[1, 4, 0, 2]$ give $[3, 4, 0, 2]$. This is the sketch of the union, bit for bit, because each register is the maximum of a function of the items that hash to it. The same holds for [LogLog](/loglog-counting/), and the bitmaps of [PCSA](/pcsa/) and [linear counting](/linear-counting/) merge by OR.

**KMV.** With $k = 3$, the hash values $\{0.05, 0.11, 0.30\}$ and $\{0.08, 0.11, 0.40\}$ merge into the 3 smallest of the union $\{0.05, 0.08, 0.11, 0.30, 0.40\}$, which is $\{0.05, 0.08, 0.11\}$. The value 0.11 is in both inputs because the same item is in both parts; it counts once.

**Linear sketches.** With the same random matrix $S$, $Sf + Sg = S(f + g)$. This needs the same seeds on every machine. Two [count-min sketches](/count-min-sketch/) with different hash functions cannot be merged.

**Samples.** A [reservoir sample](/reservoir-sampling/) of size $k$ from $n_1$ items and one from $n_2$ items merge into a uniform sample of the union: draw how many of the $k$ come from each part from the hypergeometric distribution, and take that many from each sample at random. A bottom-$k$ sample, which keeps the $k$ items with the smallest random tags, merges like KMV.

**Non-examples.** The exact median is not mergeable in small space: the medians of two parts do not give the median of the union. A summary whose merge doubles $\varepsilon$, such as some quantile summaries built for one stream, is mergeable only a fixed number of times.

## Where it is used

- **Distributed and parallel systems.** Each worker summarizes its part, and the summaries are combined in a tree or a reduce step. Query engines use HyperLogLog and KMV (often called theta sketches) for count distinct in this way.
- **Data cubes and time series.** Keep one summary per hour, and merge them to answer a query for any range of hours.
- **Sensor networks.** Each node merges the summaries of its children and sends one summary up the tree.
- **Quantiles.** The [KLL sketch](/kll-sketch/), the [q-digest](/q-digest/) and the [t-digest](/t-digest/) are used because they merge, with KLL having a proved mergeable guarantee.
- **Robustness to boosting.** For a randomized mergeable summary, the [median trick](/median-trick/) over $O(\log(1/\delta))$ independent copies, merged copy by copy, gives probability $1 - \delta$.
- **Coresets.** A [coreset](/coreset/) of the union is often a coreset of two coresets, which is merge and reduce, but with error that adds up over the levels of the tree unless the construction is mergeable in the strict sense.

## References
