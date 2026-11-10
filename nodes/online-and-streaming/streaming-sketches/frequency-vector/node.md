---
tag: XR46ET
kind: concept
slug: frequency-vector
name: Frequency vector
aliases:
- count vector
- stream vector
- frequency moments vector
area: online-and-streaming/streaming-sketches
level: intro
summary: The vector of net counts per item that a stream defines.
prereqs: [streaming-model]
see_also: [cash-register-model, turnstile-model, linear-sketch, frequency-moment-problem, distinct-elements-problem, frequent-items-problem, join-size-estimation-problem, entropy-estimation-problem]
sources:
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147, Section 1 (the frequency moments F_k of a sequence)
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: Chapter Data Streaming, Formal Aspects, section Data Stream Models (the signal A as a vector updated by the stream)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction
---

The frequency vector of a stream is the vector $f \in \mathbb{Z}^n$ whose entry $f_i$ is the net count of item $i$: the number of times $i$ occurs, or the sum of the changes made to $i$. Most streaming problems ask for a function of $f$, such as the number of nonzero entries, the largest entry, or a norm. The stream is then only a way to give $f$ one change at a time, and the algorithm must answer without storing $f$. On this page $n$ is the universe size and $m$ is the number of updates.

## In plain words

Picture a row of $n$ boxes, one for each possible item, each with a number in it. At the start every box holds 0. Each update of the stream says "add this amount to that box". In a stream of sales, the amount is always 1. In a stream that also has returns, it can be negative. The row of numbers at the end is the frequency vector. Many questions about a stream are really questions about this row: how many boxes are not 0, which boxes hold the largest numbers, or how large the numbers are in total. The order in which the updates came does not change the row.

## The idea

A stream of updates $(i_1, \Delta_1), \ldots, (i_m, \Delta_m)$ with $i_j \in [n]$ defines
$$f = \sum_{j=1}^{m} \Delta_j\, e_{i_j}, \qquad f_i = \sum_{j : i_j = i} \Delta_j,$$
where $e_i$ is the $i$-th unit vector. A plain stream of items is the case $\Delta_j = 1$. The update models differ only in what $f$ can do: in the [cash register model](/cash-register-model/) each $\Delta_j > 0$; in the strict [turnstile model](/turnstile-model/) $f \ge 0$ at all times; in the general turnstile model $f$ is any integer vector.

**Norms and moments.** For $p > 0$, the $p$-th frequency moment is $F_p = \sum_i |f_i|^p$, and the $\ell_p$ norm is $\|f\|_p = F_p^{1/p}$. The special cases have their own names.

| quantity | formula | meaning |
|---|---|---|
| $F_0 = \|f\|_0$ | $|\{i : f_i \ne 0\}|$ | the number of distinct items |
| $F_1 = \|f\|_1$ | $\sum_i |f_i|$ | the stream length, for unit insertions |
| $F_2 = \|f\|_2^2$ | $\sum_i f_i^2$ | the self-join size, the repeat rate |
| $\|f\|_\infty$ | $\max_i |f_i|$ | the count of the most frequent item |

$F_0$ is the [distinct elements problem](/distinct-elements-problem/), $F_2$ is the target of the [AMS sketch](/ams-sketch/), and the general $F_p$ is the [frequency moment problem](/frequency-moment-problem/). An item $i$ is a $\phi$-heavy hitter for $\ell_1$ if $|f_i| \ge \phi\|f\|_1$, and for $\ell_2$ if $|f_i| \ge \phi\|f\|_2$. The empirical entropy is $H = -\sum_i (|f_i|/\|f\|_1)\log_2(|f_i|/\|f\|_1)$, the subject of [entropy estimation](/entropy-estimation-problem/).

**Inequalities (proved here).** For each $f \in \mathbb{Z}^n$,
$$\|f\|_\infty \le \|f\|_2 \le \|f\|_1 \le \sqrt{F_0}\,\|f\|_2, \qquad F_2 \le \|f\|_\infty\, \|f\|_1, \qquad F_0 \le \|f\|_1.$$
*Proof.* The largest term of $\sum_i f_i^2$ is $\|f\|_\infty^2$, so $\|f\|_\infty \le \|f\|_2$. Also $(\sum_i |f_i|)^2 \ge \sum_i f_i^2$, since the cross terms are nonnegative. The Cauchy-Schwarz inequality over the $F_0$ nonzero entries gives $\sum_i |f_i| \le \sqrt{F_0}\,(\sum_i f_i^2)^{1/2}$. Next, $\sum_i f_i^2 \le \max_i |f_i| \cdot \sum_i |f_i|$. Last, each nonzero integer has $|f_i| \ge 1$. $\square$

So an $\ell_2$ heavy hitter guarantee is stronger than an $\ell_1$ one: each $\phi$-heavy hitter for $\ell_1$ is also one for $\ell_2$, because $\|f\|_2 \le \|f\|_1$.

**Order does not matter.** The vector $f$ depends only on the multiset of updates. So any query that is a function of $f$ has the same answer for each order of the stream, and an algorithm for it can process the parts of a split stream on different machines. A [linear sketch](/linear-sketch/) $Sf$ uses this directly. Questions about the order, such as the longest increasing run, or about recent items, as in the [sliding window model](/sliding-window-model/), are not functions of $f$.

## Examples

**A plain stream.** Let $n = 4$, with items $a, b, c, d$ as $1, 2, 3, 4$, and let the stream be $a, b, a, c, a, b$. Then $f = (3, 2, 1, 0)$, and
- $F_0 = 3$, $F_1 = 6 = m$, $F_2 = 9 + 4 + 1 = 14$, $\|f\|_\infty = 3$;
- the check of the inequalities: $3 \le \sqrt{14} \approx 3.74 \le 6 \le \sqrt 3 \cdot \sqrt{14} \approx 6.48$, and $14 \le 3 \cdot 6 = 18$;
- with $\phi = 0.4$, item $a$ is the only $\ell_1$ heavy hitter, since $3 \ge 2.4$ and $2 < 2.4$; for $\ell_2$ the bar is $0.4\sqrt{14} \approx 1.50$, so $a$ and $b$ are both heavy.

**A turnstile stream.** The updates $(a, +3), (b, +2), (a, -1), (c, -2)$ give $f = (2, 2, -2, 0)$. This is a general turnstile stream: $f_c < 0$. Here $F_0 = 3$ and $\|f\|_1 = 6$, but the sum of the updates is $3 + 2 - 1 - 2 = 2$. So in the turnstile models the stream length and the total weight do not give $\|f\|_1$.

**Two streams.** The inner product $\langle f, g \rangle = \sum_i f_i g_i$ of the vectors of two streams is the size of the join of two relations on the key $i$. See [join size estimation](/join-size-estimation-problem/).

## Where it is used

- **Problem statements.** Distinct elements ($F_0$), the frequency moments $F_p$, heavy hitters, point queries ($f_i$ for a given $i$), [L0 sampling](/l0-sampling-problem/) (a random $i$ with $f_i \ne 0$), entropy and join sizes are all defined on $f$.
- **Error bounds.** Sketch guarantees are stated in norms of $f$: the [count-min sketch](/count-min-sketch/) has error $\varepsilon\|f\|_1$, the [count sketch](/count-sketch/) has error $\varepsilon\|f\|_2$, and the [Misra-Gries summary](/misra-gries-summary/) has error $\varepsilon m$.
- **Linear sketches.** A sketch of the form $Sf$ for a random matrix $S$ supports deletions and merges, because $S(f + g) = Sf + Sg$.
- **Graph streams.** For a graph stream, $f$ can be the vector of edge multiplicities, or one vector per vertex, as in the [AGM sketch](/agm-graph-sketch/).
- **Lower bounds.** Reductions from communication problems build two vectors $x$ and $y$ held by two players, and the stream gives $f = x + y$ or $f = x - y$.

## References
